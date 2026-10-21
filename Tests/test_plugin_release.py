"""Offline release verification, publication, interruption and recovery tests."""

import base64
from contextlib import redirect_stdout
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shlex
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "Scripts/plugin_release.py"
WORKFLOW = ROOT / ".github/workflows/plugin-release.yml"
spec = importlib.util.spec_from_file_location("plugin_release", SCRIPT)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)
REPOSITORY = "example/plugin-widget"
API_ROOT = "/repos/" + REPOSITORY
COMMIT = "a" * 40
WORKFLOW_SHA = "b" * 40
WORKFLOW_REF = release.WORKFLOW + WORKFLOW_SHA
TAG = "v0.2.0"
MANIFEST = b'id = "widget"\nversion = "0.2.0"\nplugin_api = 1\n[compatibility]\nminimum_host = "0.1.0"\n'


def zip_bytes(files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(entry, data)
    return output.getvalue()


class FakeGitHub:
    """The same four-operation API boundary as the real REST transport."""

    def __init__(self, archives):
        self.calls = []
        self.writes = []
        self.runs = {10: self.run()}
        self.artifacts = {}
        self.artifact_bytes = {}
        self.releases = {}
        self.assets = {}
        self.asset_bytes = {}
        self.next_id = 100
        self.fail = None
        self.tag_type = "tag"
        self.tag_commit = COMMIT
        self.verified = True
        self.reason = "valid"
        self.install_artifact(20, archives)

    def run(self, **changes):
        run = {"id": 10, "run_attempt": 1, "event": "push", "head_branch": "main",
               "head_sha": COMMIT, "head_repository": {"full_name": REPOSITORY},
               "path": ".github/workflows/ci.yml", "status": "completed", "conclusion": "success",
               "run_started_at": "2026-01-01T00:00:00Z", "updated_at": "2026-01-01T00:10:00Z"}
        run.update(changes)
        return run

    def install_artifact(self, artifact_id, archives, **changes):
        data = zip_bytes(dict({"dist/" + name: content for name, content in archives.items()},
                              **{"package-receipt.json": b'{"builder": "metadata"}\n'}))
        artifact = {"id": artifact_id, "name": "widget-" + COMMIT + "-3.13", "expired": False,
                    "digest": "sha256:" + release.sha256(data), "created_at": "2026-01-01T00:05:00Z",
                    "workflow_run": {"id": 10, "head_sha": COMMIT}}
        artifact.update(changes)
        self.artifacts[artifact_id] = artifact
        self.artifact_bytes[artifact_id] = data

    def rerun_ci(self, archives):
        self.runs[10] = self.run(run_attempt=2, run_started_at="2026-01-02T00:00:00Z",
                                updated_at="2026-01-02T00:10:00Z")
        self.install_artifact(21, archives, created_at="2026-01-02T00:05:00Z")

    def _record(self, method, path):
        self.calls.append((method, path))
        assert path.startswith(API_ROOT), path
        return path[len(API_ROOT):]

    def get(self, path):
        route = self._record("GET", path)
        if route == "":
            result = {"default_branch": "main"}
        elif route.startswith("/git/ref/tags/"):
            result = {"object": {"type": self.tag_type, "sha": "c" * 40}}
        elif route.startswith("/git/tags/"):
            result = {"tag": TAG, "object": {"type": "commit", "sha": self.tag_commit},
                      "verification": {"verified": self.verified, "reason": self.reason}}
        elif route.startswith("/commits/"):
            result = {"sha": COMMIT}
        elif route.startswith("/actions/runs/"):
            result = self.runs[int(route.split("/")[3])]
        elif route.startswith("/actions/artifacts/"):
            artifact_id = int(route.split("/")[3])
            if artifact_id not in self.artifacts:
                raise release.APIError(404, path)
            result = self.artifacts[artifact_id]
        elif route.startswith("/releases/"):
            result = self.releases[int(route.split("/")[2])]
        else:
            raise AssertionError(("GET", route))
        return copy.deepcopy(result)

    def list(self, path, key=None):
        route = self._record("LIST", path)
        if route.startswith("/actions/workflows/ci.yml/runs?"):
            assert key == "workflow_runs"
            result = list(self.runs.values())
        elif route.endswith("/artifacts"):
            assert key == "artifacts"
            run_id = int(route.split("/")[3])
            result = [item for item in self.artifacts.values() if item["workflow_run"]["id"] == run_id]
        elif route == "/releases":
            result = list(self.releases.values())
        elif route.endswith("/assets"):
            release_id = int(route.split("/")[2])
            result = [item for item in self.assets.values() if item["release_id"] == release_id]
        else:
            raise AssertionError(("LIST", route))
        return copy.deepcopy(result)

    def download(self, path):
        route = self._record("DOWNLOAD", path)
        if route.startswith("/actions/artifacts/"):
            return self.artifact_bytes[int(route.split("/")[3])]
        if route.startswith("/releases/assets/"):
            return self.asset_bytes[int(route.split("/")[3])]
        raise AssertionError(("DOWNLOAD", route))

    def _failure(self, step, when):
        if self.fail == (step, when):
            self.fail = None
            raise release.APIError(502, "injected " + step + " " + when)

    def add_draft(self):
        self.releases[50] = {"id": 50, "tag_name": TAG, "target_commitish": COMMIT, "name": TAG,
                             "draft": True, "prerelease": False, "body": "Operator acceptance notes"}
        return self.releases[50]

    def add_asset(self, name, data=b"", state="uploaded", release_id=50):
        self.next_id += 1
        asset = {"id": self.next_id, "release_id": release_id, "name": name, "state": state,
                 "digest": "sha256:" + release.sha256(data), "size": len(data)}
        self.assets[asset["id"]] = asset
        self.asset_bytes[asset["id"]] = data
        return asset

    def send(self, method, path, data=None, content_type="application/json"):
        route = self._record(method, path)
        if method == "POST" and route == "/releases":
            step = "draft"
        elif method == "POST" and "/assets?" in route:
            step = parse_qs(urlsplit(route).query)["name"][0]
        elif method == "PATCH":
            step = "publish"
        elif method == "DELETE":
            step = "delete"
        else:
            raise AssertionError((method, route))
        self._failure(step, "before")
        self.writes.append((step, copy.deepcopy(data)))
        if step == "draft":
            result = self.add_draft()
            result.update(data)
        elif step == "publish":
            result = self.releases[int(route.split("/")[2])]
            result.update(data)
        elif step == "delete":
            asset_id = int(route.split("/")[3])
            assert self.releases[self.assets[asset_id]["release_id"]]["draft"]
            del self.assets[asset_id]
            del self.asset_bytes[asset_id]
            result = None
        else:
            release_id = int(route.split("/")[2])
            assert self.releases[release_id]["draft"]
            assert not any(item["name"] == step for item in self.assets.values())
            result = self.add_asset(step, data, release_id=release_id)
        self._failure(step, "after")
        return copy.deepcopy(result)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="plugin release ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.checkout = self.root / "checkout"
        self.checkout.mkdir()
        self.output = self.root / "assets"
        self.build_output = self.root / "build"
        self.set_archives(MANIFEST, {"widget.zip": zip_bytes({"computer-mcp-plugin.toml": MANIFEST, "bin/tool": b"owned"})})
        self.api = FakeGitHub(self.archives)
        self.head = patch.object(release.subprocess, "check_output", return_value=COMMIT + "\n")
        self.head.start()
        self.addCleanup(self.head.stop)

    def set_archives(self, manifest, archives):
        self.manifest = manifest
        self.archives = archives
        (self.checkout / "computer-mcp-plugin.toml").write_bytes(manifest)
        (self.checkout / "build.py").write_text(
            "import base64, os, sys\nfrom pathlib import Path\n"
            "assert 'GH_TOKEN' not in os.environ and 'GITHUB_TOKEN' not in os.environ\n"
            "output = Path(sys.argv[1]); output.mkdir()\n" +
            "\n".join(f"(output / {name!r}).write_bytes(base64.b64decode({base64.b64encode(data)!r}))"
                      for name, data in archives.items()))

    def verify(self, **overrides):
        arguments = dict(api=self.api, repository=REPOSITORY, ref=TAG, publish=True,
                         checkout=self.checkout, build=shlex.quote(sys.executable) + " build.py",
                         ci_artifact="widget-${commit}-3.13", workflow_ref=WORKFLOW_REF,
                         workflow_sha=WORKFLOW_SHA, output=self.output, build_output=self.build_output)
        arguments.update(overrides)
        with patch.dict(os.environ, {"GH_TOKEN": "fake", "GITHUB_TOKEN": "fake"}):
            return release.verify(**arguments)

    def publish(self):
        return release.publish_bundle(self.api, REPOSITORY, self.output,
                                      release.sha256((self.output / release.RECEIPT).read_bytes()))

    def files(self):
        return {path.name: path.read_bytes() for path in self.output.iterdir()}

    def frozen_draft(self):
        self.verify()
        self.api.add_draft()
        self.api.add_asset(release.RECEIPT, (self.output / release.RECEIPT).read_bytes())

    def verify_again(self, **changes):
        return self.verify(output=self.root / "recovered", build_output=self.root / "rebuilt", **changes)

    def assert_no_writes(self, function, pattern):
        before = copy.deepcopy(self.api.writes)
        with self.assertRaisesRegex(release.ReleaseError, pattern):
            function()
        self.assertEqual(self.api.writes, before)

    def test_first_publication_order_contents_checksums_and_notes(self):
        outputs = self.verify()
        self.assertEqual(self.api.writes, [])
        result = self.publish()
        self.assertEqual(result, {"published": "true", "release_id": "50", "tag": TAG})
        self.assertEqual([step for step, _ in self.api.writes],
                         ["draft", release.RECEIPT, "widget.zip", release.SUMS, "publish"])
        self.assertEqual(self.api.releases[50]["body"], "Operator acceptance notes")
        files = self.files()
        receipt = json.loads(files[release.RECEIPT])
        self.assertEqual(set(receipt), {"schema", "plugin_id", "version", "plugin_api", "compatibility",
                                      "tag", "commit", "archives", "ci", "workflow", "reproduction"})
        self.assertEqual(receipt["schema"], 1)
        self.assertEqual(receipt["ci"], {"run_id": 10, "run_attempt": 1,
                                        "artifacts": [{"id": 20, "digest": self.api.artifacts[20]["digest"]}]})
        self.assertEqual(receipt["workflow"], {"ref": WORKFLOW_REF, "sha": WORKFLOW_SHA})
        self.assertEqual(receipt["reproduction"], "rebuild")
        self.assertEqual(outputs["receipt_sha256"], release.sha256(files[release.RECEIPT]))
        self.assertEqual(files[release.SUMS], release.checksums({name: data for name, data in files.items()
                                                              if name != release.SUMS}))
        self.assertEqual({item["name"]: self.api.asset_bytes[item["id"]] for item in self.api.assets.values()}, files)

    def test_failures_before_and_after_every_publication_step_are_recoverable(self):
        self.verify()
        expected = self.files()
        for step in ("draft", release.RECEIPT, "widget.zip", release.SUMS, "publish"):
            for when in ("before", "after"):
                with self.subTest(step=step, when=when):
                    self.api = FakeGitHub(self.archives)
                    self.api.fail = (step, when)
                    with self.assertRaises(release.APIError):
                        self.publish()
                    if self.api.releases and self.api.releases[50]["draft"]:
                        self.assertNotEqual(self.api.writes[-1][0], "publish")
                    result = self.publish()
                    self.assertEqual(result["published"], "true")
                    self.assertEqual({item["name"]: self.api.asset_bytes[item["id"]]
                                      for item in self.api.assets.values()}, expected)

    def test_partial_upload_recovery_freezes_ci_attempt_artifact_and_workflow(self):
        self.verify()
        original = self.files()
        self.api.fail = (release.SUMS, "before")
        with self.assertRaises(release.APIError):
            self.publish()
        changed = {"widget.zip": self.archives["widget.zip"] + b"new CI bytes"}
        self.api.rerun_ci(changed)
        self.api.calls.clear()
        self.verify_again(workflow_ref=release.WORKFLOW + "d" * 40, workflow_sha="d" * 40)
        recovered = {path.name: path.read_bytes() for path in (self.root / "recovered").iterdir()}
        self.assertEqual(recovered, original)
        self.assertFalse(any("/actions/runs/" in path or "/workflows/" in path for _, path in self.api.calls))
        self.assertIn(("DOWNLOAD", API_ROOT + "/actions/artifacts/20/zip"), self.api.calls)
        self.output = self.root / "recovered"
        self.publish()
        self.assertEqual([name for name, _ in self.api.writes].count(release.RECEIPT), 1)

    def test_starter_assets_at_each_upload_position_are_deleted_and_replaced(self):
        self.verify()
        files = self.files()
        for name in (release.RECEIPT, "widget.zip", release.SUMS):
            with self.subTest(name=name):
                self.api = FakeGitHub(self.archives)
                self.api.add_draft()
                if name != release.RECEIPT:
                    self.api.add_asset(release.RECEIPT, files[release.RECEIPT])
                self.api.add_asset(name, b"partial", state="starter")
                self.publish()
                self.assertIn("delete", [step for step, _ in self.api.writes])
                self.assertEqual({item["name"]: self.api.asset_bytes[item["id"]]
                                  for item in self.api.assets.values()}, files)

    def test_starter_deletion_failure_is_recoverable(self):
        self.frozen_draft()
        self.api.add_asset("widget.zip", state="starter")
        for when in ("before", "after"):
            with self.subTest(when=when):
                self.api.fail = ("delete", when)
                with self.assertRaises(release.APIError):
                    self.publish()
                if not any(item["name"] == "widget.zip" for item in self.api.assets.values()):
                    self.api.add_asset("widget.zip", state="starter")
        self.publish()

    def test_completed_digest_or_size_conflicts_are_never_overwritten(self):
        self.verify()
        for field, value in (("digest", "sha256:" + "0" * 64), ("size", 999), ("state", "unknown")):
            with self.subTest(field=field):
                self.api = FakeGitHub(self.archives)
                self.api.add_draft()
                asset = self.api.add_asset("widget.zip", self.archives["widget.zip"])
                asset[field] = value
                self.assert_no_writes(self.publish, "conflicts")

    def test_conflicting_frozen_receipt_is_refused_before_any_upload(self):
        self.verify()
        self.api.add_draft()
        self.api.add_asset(release.RECEIPT, b"another receipt")
        self.assert_no_writes(self.publish, "conflicts")

    def test_unexpected_and_duplicate_assets_are_refused(self):
        self.verify()
        for duplicate in (False, True):
            with self.subTest(duplicate=duplicate):
                self.api = FakeGitHub(self.archives)
                self.api.add_draft()
                name = "widget.zip" if duplicate else "unowned.txt"
                self.api.add_asset(name)
                if duplicate:
                    self.api.add_asset(name)
                self.assert_no_writes(self.publish, "Duplicate|unexpected")

    def test_recorded_artifact_expired_missing_or_gone_has_explicit_recovery(self):
        self.frozen_draft()
        for mode in ("expired", "missing", "gone"):
            with self.subTest(mode=mode):
                saved = copy.deepcopy(self.api.artifacts)
                if mode == "expired":
                    self.api.artifacts[20]["expired"] = True
                elif mode == "missing":
                    del self.api.artifacts[20]
                original = self.api.download

                def download(path):
                    if mode == "gone" and "/actions/artifacts/" in path:
                        raise release.APIError(410, path)
                    return original(path)

                with patch.object(self.api, "download", side_effect=download):
                    self.assert_no_writes(self.verify_again, "delete the unpublished draft release.*rerun release.yml")
                self.api.artifacts = saved

    def test_recovery_rejects_replaced_artifact_metadata_or_bytes(self):
        self.frozen_draft()
        for change in ("digest", "bytes", "run"):
            with self.subTest(change=change):
                with patch.dict(self.api.artifacts[20], {"digest": "sha256:" + "0" * 64} if change == "digest"
                                else {"workflow_run": {"id": 99}} if change == "run" else {}):
                    original = self.api.artifact_bytes[20]
                    if change == "bytes":
                        self.api.artifact_bytes[20] += b"changed"
                    self.assert_no_writes(self.verify_again, "digest|another run")
                    self.api.artifact_bytes[20] = original

    def test_public_release_repeat_is_read_only_even_after_ci_expiry(self):
        self.verify()
        self.publish()
        writes = copy.deepcopy(self.api.writes)
        self.api.artifacts.clear()
        self.api.calls.clear()
        self.verify_again()
        self.assertFalse(any("/actions/" in path for _, path in self.api.calls))
        self.output = self.root / "recovered"
        self.assertEqual(self.publish()["published"], "true")
        self.assertEqual(self.api.writes, writes)

    def test_public_release_incomplete_extra_starter_or_conflicting_assets_are_immutable(self):
        self.verify()
        self.publish()
        assets = copy.deepcopy(self.api.assets)
        for mode in ("missing", "extra", "starter", "digest"):
            with self.subTest(mode=mode):
                self.api.assets = copy.deepcopy(assets)
                asset_id = next(item["id"] for item in self.api.assets.values() if item["name"] == "widget.zip")
                if mode == "missing":
                    del self.api.assets[asset_id]
                elif mode == "extra":
                    self.api.add_asset("extra.txt")
                elif mode == "starter":
                    self.api.assets[asset_id]["state"] = "starter"
                else:
                    self.api.assets[asset_id]["digest"] = "sha256:" + "0" * 64
                self.assert_no_writes(self.publish, "incomplete|unexpected|conflicts")

    def test_release_becoming_public_before_mutation_cannot_be_changed(self):
        self.frozen_draft()
        self.api.add_asset("widget.zip", state="starter")
        original = self.api.get
        count = 0

        def get(path):
            nonlocal count
            if path.endswith("/releases/50"):
                count += 1
                if count == 2:
                    self.api.releases[50]["draft"] = False
            return original(path)

        with patch.object(self.api, "get", side_effect=get):
            self.assert_no_writes(self.publish, "became public")

    def test_upload_api_digest_mismatch_leaves_draft_unpublished(self):
        self.verify()
        original = self.api.send

        def send(*args):
            result = original(*args)
            if "/assets?" in args[1]:
                result["digest"] = "sha256:" + "0" * 64
            return result

        with patch.object(self.api, "send", side_effect=send):
            with self.assertRaisesRegex(release.ReleaseError, "conflicts"):
                self.publish()
        self.assertTrue(self.api.releases[50]["draft"])
        self.assertEqual([step for step, _ in self.api.writes], ["draft", release.RECEIPT])

    def test_draft_target_and_tag_movement_are_refused(self):
        self.verify()
        self.api.add_draft()["target_commitish"] = "d" * 40
        self.assert_no_writes(self.publish, "target differs")
        self.api.tag_commit = "d" * 40
        self.assert_no_writes(self.publish, "tag moved")

    def test_tag_movement_during_upload_prevents_publication(self):
        self.verify()
        original = self.api.send

        def send(*args):
            result = original(*args)
            if args[1].endswith("?name=SHA256SUMS"):
                self.api.tag_commit = "d" * 40
            return result

        with patch.object(self.api, "send", side_effect=send):
            with self.assertRaisesRegex(release.ReleaseError, "tag moved during"):
                self.publish()
        self.assertTrue(self.api.releases[50]["draft"])
        self.assertNotIn("publish", [step for step, _ in self.api.writes])

    def test_asset_change_before_final_check_prevents_publication(self):
        self.verify()
        original = self.api.send

        def send(*args):
            result = original(*args)
            if args[1].endswith("?name=SHA256SUMS"):
                asset = next(item for item in self.api.assets.values() if item["name"] == "widget.zip")
                asset["digest"] = "sha256:" + "0" * 64
            return result

        with patch.object(self.api, "send", side_effect=send):
            with self.assertRaisesRegex(release.ReleaseError, "conflicts"):
                self.publish()
        self.assertTrue(self.api.releases[50]["draft"])

    def test_cli_dry_run_reports_publication_conditions_and_outputs(self):
        output = self.root / "github-output"
        arguments = [str(SCRIPT), "verify", "--repository", REPOSITORY, "--ref", COMMIT,
                     "--publish", "false", "--checkout", str(self.checkout), "--build",
                     shlex.quote(sys.executable) + " build.py", "--ci-artifact", "widget-${commit}-3.13",
                     "--workflow-ref", WORKFLOW_REF, "--workflow-sha", WORKFLOW_SHA,
                     "--output", str(self.output), "--build-output", str(self.build_output)]
        stdout = io.StringIO()
        with patch.object(release, "GitHub", return_value=self.api), patch.object(sys, "argv", arguments), \
                patch.dict(os.environ, {"GH_TOKEN": "fake", "GITHUB_OUTPUT": str(output)}), redirect_stdout(stdout):
            self.assertEqual(release.main(), 0)
        self.assertIn("signed annotated v0.2.0", stdout.getvalue())
        self.assertIn("manual acceptance", stdout.getvalue())
        self.assertIn("commit=" + COMMIT + "\ntag=\nreceipt_sha256=", output.read_text())
        self.assertEqual(self.api.writes, [])

    def test_dry_run_tag_uses_identical_assembly_without_writes(self):
        self.verify()
        expected = self.files()
        self.verify_again(publish=False)
        self.assertEqual({path.name: path.read_bytes() for path in (self.root / "recovered").iterdir()}, expected)
        self.assertEqual(self.api.writes, [])

    def test_commit_dry_run_checks_ci_and_rebuild_without_tag_access(self):
        self.verify(ref=COMMIT, publish=False)
        receipt = json.loads((self.output / release.RECEIPT).read_bytes())
        self.assertIsNone(receipt["tag"])
        self.assertFalse(any("/git/" in path for _, path in self.api.calls))
        self.assert_no_writes(self.publish, "untagged")
        self.api.runs[10]["conclusion"] = "failure"
        self.assert_no_writes(lambda: self.verify_again(ref=COMMIT, publish=False), "successful authoritative CI")

    def test_tag_format_annotation_signature_and_manifest_version_checks(self):
        for change, pattern in (({"tag_type": "commit"}, "annotated"),
                                ({"verified": False}, "signature"),
                                ({"reason": "unknown_key"}, "signature")):
            with self.subTest(change=change), patch.multiple(self.api, **change):
                self.assert_no_writes(self.verify, pattern)
        for invalid in (COMMIT, "main", "v00.2.0", "v0.2.0-preview.1", "v0.2.0-rc.0"):
            with self.subTest(ref=invalid):
                self.assert_no_writes(lambda: self.verify(ref=invalid), "signed annotated")
        self.set_archives(MANIFEST.replace(b'0.2.0', b'0.2.1'), self.archives)
        self.assert_no_writes(self.verify, "version differs")

    def test_prerelease_tag_preserves_prerelease_status(self):
        manifest = MANIFEST.replace(b'0.2.0', b'0.2.0-rc.1')
        self.set_archives(manifest, {"widget.zip": zip_bytes({"computer-mcp-plugin.toml": manifest})})
        self.api = FakeGitHub(self.archives)
        original = self.api.get

        def get(path):
            result = original(path)
            if "/git/tags/" in path:
                result["tag"] = "v0.2.0-rc.1"
            return result

        with patch.object(self.api, "get", side_effect=get):
            self.verify(ref="v0.2.0-rc.1")
            self.publish()
        self.assertTrue(self.api.releases[50]["prerelease"])

    def test_invalid_plugin_api_is_refused(self):
        for replacement in (b"", b"plugin_api = 0\n", b"plugin_api = -1\n", b"plugin_api = true\n",
                            b'plugin_api = "1"\n', b"plugin_api = 1.0\n"):
            with self.subTest(replacement=replacement):
                (self.checkout / "computer-mcp-plugin.toml").write_bytes(MANIFEST.replace(b"plugin_api = 1\n", replacement))
                self.assert_no_writes(self.verify, "plugin_api")

    def test_wrong_checkout_commit_is_refused_before_build(self):
        with patch.object(release.subprocess, "check_output", return_value="d" * 40):
            self.assert_no_writes(self.verify, "Checkout differs")
        self.assertFalse(self.build_output.exists())

    def test_authoritative_ci_ignores_other_event_branch_commit_workflow_or_repository(self):
        for field, value in (("event", "pull_request"), ("event", "workflow_dispatch"), ("head_branch", "other"),
                             ("head_sha", "d" * 40), ("path", ".github/workflows/other.yml"),
                             ("head_repository", {"full_name": "fork/plugin-widget"})):
            with self.subTest(field=field, value=value):
                self.api.runs = {10: self.api.run(**{field: value})}
                self.assert_no_writes(self.verify, "No successful authoritative CI")

    def test_ci_requires_successful_latest_attempt(self):
        for state in ("failure", "cancelled", None):
            with self.subTest(state=state):
                self.api.runs = {10: self.api.run(run_attempt=2, conclusion=state)}
                self.assert_no_writes(self.verify, "successful authoritative CI")
        self.api.runs = {10: self.api.run(status="in_progress")}
        self.assert_no_writes(self.verify, "successful authoritative CI")

    def test_latest_successful_authoritative_run_is_selected(self):
        self.api.runs[9] = self.api.run(id=9)
        self.api.runs[11] = self.api.run(id=11, conclusion="failure")
        self.verify()
        receipt = json.loads((self.output / release.RECEIPT).read_bytes())
        self.assertEqual(receipt["ci"]["run_id"], 10)

    def test_ci_rerun_after_listing_cannot_reuse_previous_attempt_success(self):
        original = self.api.get

        def get(path):
            result = original(path)
            if path.endswith("/actions/runs/10"):
                result.update(run_attempt=2, conclusion="failure")
            return result

        with patch.object(self.api, "get", side_effect=get):
            self.assert_no_writes(self.verify, "Latest CI attempt")

    def test_latest_attempt_excludes_artifacts_left_by_earlier_attempts(self):
        self.api.rerun_ci(self.archives)
        result = self.verify()
        self.assertTrue(result["receipt_sha256"])
        receipt = json.loads((self.output / release.RECEIPT).read_bytes())
        self.assertEqual(receipt["ci"]["run_attempt"], 2)
        self.assertEqual(receipt["ci"]["artifacts"][0]["id"], 21)

    def test_attempt_specific_metadata_defines_artifact_creation_window(self):
        self.api.rerun_ci(self.archives)
        attempt = copy.deepcopy(self.api.runs[10])
        self.api.runs[10]["run_started_at"] = "2026-01-01T00:00:00Z"
        original = self.api.get

        def get(path):
            return copy.deepcopy(attempt) if path.endswith("/attempts/2") else original(path)

        with patch.object(self.api, "get", side_effect=get):
            self.verify()
        receipt = json.loads((self.output / release.RECEIPT).read_bytes())
        self.assertEqual(receipt["ci"]["artifacts"][0]["id"], 21)

    def test_ci_artifact_requires_one_exact_live_artifact_with_digest(self):
        for mode, pattern in (("missing", "exactly one"), ("duplicate", "exactly one"),
                              ("expired", "expired"), ("digest", "SHA-256"), ("old", "exactly one")):
            with self.subTest(mode=mode):
                self.api = FakeGitHub(self.archives)
                if mode == "missing":
                    self.api.artifacts[20]["name"] += "-other"
                elif mode == "duplicate":
                    self.api.install_artifact(21, self.archives)
                elif mode == "old":
                    self.api.artifacts[20]["created_at"] = "2025-01-01T00:00:00Z"
                elif mode == "digest":
                    self.api.artifacts[20]["digest"] = None
                else:
                    self.api.artifacts[20]["expired"] = True
                self.assert_no_writes(self.verify, pattern)

    def test_downloaded_ci_digest_mismatch_and_build_failure_are_read_only(self):
        self.api.artifact_bytes[20] += b"corrupt"
        self.assert_no_writes(self.verify, "digest mismatch")
        self.api = FakeGitHub(self.archives)
        with self.assertRaises(release.subprocess.CalledProcessError):
            self.verify(build="false")
        self.assertEqual(self.api.writes, [])
        self.assertFalse(self.output.exists())

    def test_rebuild_mismatch_is_read_only_for_publication_and_dry_run(self):
        self.api.install_artifact(20, {"widget.zip": self.archives["widget.zip"] + b"different"})
        for publish in (True, False):
            with self.subTest(publish=publish):
                self.assert_no_writes(lambda: self.verify(publish=publish, build_output=self.root / str(publish)),
                                      "byte for byte")

    def test_multiple_declared_archives_are_sorted_rebuilt_and_published(self):
        manifest = MANIFEST + b'[[compatibility.artifacts]]\nname = "z-arm64.zip"\n[[compatibility.artifacts]]\nname = "a-x86.zip"\n'
        self.set_archives(manifest, {name: zip_bytes({"computer-mcp-plugin.toml": manifest, "platform": name.encode()})
                                     for name in ("z-arm64.zip", "a-x86.zip")})
        self.api = FakeGitHub(self.archives)
        self.verify()
        self.publish()
        self.assertEqual([step for step, _ in self.api.writes],
                         ["draft", release.RECEIPT, "a-x86.zip", "z-arm64.zip", release.SUMS, "publish"])

    def test_invalid_artifact_declarations_are_refused(self):
        for declaration in (b'artifacts = []\n', b'artifacts = ["widget.zip"]\n',
                            b'artifacts = [{name = "../widget.zip"}]\n',
                            b'artifacts = [{name = "widget.zip"}, {name = "widget.zip"}]\n'):
            with self.subTest(declaration=declaration):
                (self.checkout / "computer-mcp-plugin.toml").write_bytes(MANIFEST + declaration)
                self.assert_no_writes(self.verify, "artifacts|artifact names")

    def test_archive_set_must_match_manifest_or_be_single(self):
        for manifest in (MANIFEST, MANIFEST + b'[[compatibility.artifacts]]\nname = "missing.zip"\n'):
            with self.subTest(manifest=manifest):
                self.set_archives(manifest, self.archives)
                self.api = FakeGitHub(dict(self.archives, **{"extra.zip": b"extra"}))
                self.assert_no_writes(self.verify, "Archives differ")

    def test_archive_manifest_must_equal_source(self):
        self.set_archives(MANIFEST, {"widget.zip": zip_bytes({"computer-mcp-plugin.toml": MANIFEST + b'platforms = ["macos"]\n'})})
        self.api = FakeGitHub(self.archives)
        self.assert_no_writes(self.verify, "manifest differs")

    def test_bundle_tampering_is_refused_before_release_writes(self):
        self.verify()
        expected = self.files()
        receipt_hash = release.sha256(expected[release.RECEIPT])
        for name in (release.RECEIPT, "widget.zip", release.SUMS, "extra.txt"):
            with self.subTest(name=name):
                (self.output / name).write_bytes(expected.get(name, b"") + b"tampered")
                self.assert_no_writes(lambda: release.publish_bundle(self.api, REPOSITORY, self.output, receipt_hash),
                                      "differ|file set")
                if name in expected:
                    (self.output / name).write_bytes(expected[name])
                else:
                    (self.output / name).unlink()

    def test_symlink_in_bundle_is_refused_before_reading_its_target(self):
        self.verify()
        data = (self.output / release.RECEIPT).read_bytes()
        (self.output / release.RECEIPT).unlink()
        (self.output / release.RECEIPT).symlink_to(self.root / "missing-target")
        self.assert_no_writes(lambda: release.publish_bundle(self.api, REPOSITORY, self.output, release.sha256(data)),
                              "file set")

    def test_invalid_frozen_receipt_or_source_is_rejected(self):
        self.frozen_draft()
        receipt_asset = next(item for item in self.api.assets.values() if item["name"] == release.RECEIPT)
        original = (self.output / release.RECEIPT).read_bytes()
        for mode in ("schema", "incomplete", "noncanonical", "commit", "plugin_api", "ci", "digest"):
            with self.subTest(mode=mode):
                receipt = json.loads(original)
                if mode == "schema":
                    receipt["schema"] = 2
                elif mode == "incomplete":
                    del receipt["ci"]
                elif mode == "commit":
                    receipt["commit"] = "d" * 40
                elif mode == "plugin_api":
                    receipt["plugin_api"] = 2
                elif mode == "ci":
                    receipt["ci"]["run_attempt"] = 0
                data = json.dumps(receipt).encode() if mode == "noncanonical" else release.canonical(receipt)
                self.api.asset_bytes[receipt_asset["id"]] = data
                receipt_asset["size"] = len(data)
                receipt_asset["digest"] = "sha256:" + ("0" * 64 if mode == "digest" else release.sha256(data))
                self.assert_no_writes(self.verify_again, "schema|fields|canonical|source|provenance|download differs")


class FormatAndTransportTests(unittest.TestCase):
    def test_unsafe_zip_paths_duplicate_names_and_symlinks_are_refused(self):
        for name in ("../widget.zip", "/widget.zip", "dir\\widget.zip"):
            with self.subTest(name=name), self.assertRaisesRegex(release.ReleaseError, "Unsafe"):
                release.zip_entries(zip_bytes({name: b"data"}))
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as archive:
            entry = zipfile.ZipInfo("widget.zip")
            entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(entry, b"target")
        with self.assertRaisesRegex(release.ReleaseError, "special file"):
            release.zip_entries(output.getvalue())
        with self.assertRaisesRegex(release.ReleaseError, "Duplicate CI"):
            release.ci_archives(zip_bytes({"a/widget.zip": b"one", "b/widget.zip": b"two"}), None)

    def test_pagination_consumes_all_pages(self):
        api = release.GitHub("fake")
        with patch.object(api, "get", side_effect=[{"items": list(range(100))}, {"items": [100]}]) as get:
            self.assertEqual(api.list(API_ROOT + "/example?filter=one", "items"), list(range(101)))
            self.assertIn("&per_page=100&page=2", get.call_args[0][0])

    def test_download_redirect_strips_token_and_requires_https(self):
        request = Request("https://api.github.com/repos/example/plugin/actions/artifacts/20/zip",
                          headers={"Authorization": "Bearer fake"})
        redirect = release.SafeRedirect()
        moved = redirect.redirect_request(request, None, 302, "Found", {}, "https://blob.example/archive.zip")
        self.assertFalse(moved.has_header("Authorization"))
        with self.assertRaisesRegex(release.ReleaseError, "non-HTTPS"):
            redirect.redirect_request(request, None, 302, "Found", {}, "http://blob.example/archive.zip")


class WorkflowBoundaryTests(unittest.TestCase):
    def test_workflow_helper_digest_matches_source_and_actions_are_pinned(self):
        workflow = WORKFLOW.read_text()
        self.assertEqual(re.findall(r"PLUGIN_RELEASE_SHA256: '([0-9a-f]{64})'", workflow),
                         [release.sha256(SCRIPT.read_bytes())])
        uses = re.findall(r"uses: (\S+)", workflow)
        self.assertTrue(uses)
        self.assertTrue(all(re.fullmatch(r"[^@]+@[0-9a-f]{40}", use) for use in uses))
        verify, publish = workflow.split("  verify:\n", 1)[1].split("  publish:\n", 1)
        self.assertIn("      contents: read\n      actions: read", verify)
        self.assertIn("      contents: write", publish)
        self.assertNotIn("actions: read", publish)
        self.assertNotIn("actions/checkout", publish)
        self.assertNotIn("secrets", workflow)
        self.assertNotIn("RELEASE_BUILD", publish)

    def test_publish_bootstrap_rejects_modified_helper_without_executing_it(self):
        workflow = WORKFLOW.read_text()
        script = workflow.rsplit("<<'PY'\n", 1)[1].split("\n          PY", 1)[0]
        import textwrap
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "plugin-release"
            root.mkdir()
            marker = root / "executed"
            (root / "plugin_release.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
            with patch.dict(os.environ, {"RUNNER_TEMP": directory, "PLUGIN_RELEASE_SHA256": release.sha256(SCRIPT.read_bytes())}):
                with self.assertRaisesRegex(SystemExit, "differs from this workflow pin"):
                    exec(compile(textwrap.dedent(script), str(WORKFLOW), "exec"), {})
            self.assertFalse(marker.exists())

    def test_bootstrap_loads_pinned_reusable_workflow_source_from_run_metadata(self):
        import textwrap
        workflow = WORKFLOW.read_text()
        script = workflow.split("<<'PY'\n", 1)[1].split("\n          PY", 1)[0]
        run = {"referenced_workflows": [{"path": WORKFLOW_REF, "sha": WORKFLOW_SHA},
                                         {"path": "example/caller/.github/workflows/other.yml@main", "sha": "c" * 40}]}
        responses = [io.BytesIO(json.dumps(run).encode()),
                     io.BytesIO(json.dumps({"content": base64.b64encode(SCRIPT.read_bytes()).decode()}).encode())]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            with patch.dict(os.environ, {"RUNNER_TEMP": directory, "PLUGIN_RELEASE_SHA256": release.sha256(SCRIPT.read_bytes()),
                                         "GH_REPOSITORY": REPOSITORY, "GH_RUN_ID": "12", "GH_TOKEN": "fake",
                                         "GITHUB_OUTPUT": str(output)}):
                with patch("urllib.request.urlopen", side_effect=responses) as urlopen:
                    exec(compile(textwrap.dedent(script), str(WORKFLOW), "exec"), {})
            self.assertEqual((Path(directory) / "plugin-release/plugin_release.py").read_bytes(), SCRIPT.read_bytes())
            self.assertEqual(output.read_text(), f"workflow_ref={WORKFLOW_REF}\nworkflow_sha={WORKFLOW_SHA}\n")
            self.assertEqual(urlopen.call_args[0][0].full_url,
                             "https://api.github.com/repos/computer-mcp/.github/contents/Scripts/plugin_release.py?ref=" + WORKFLOW_SHA)


if __name__ == "__main__":
    unittest.main()
