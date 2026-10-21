"""Verify reproducible plugin archives and publish their verified release bundle.

The GitHub boundary has four operations: get JSON, list paginated JSON,
download bytes, and send a mutation. Tests supply an in-memory implementation.
"""

import argparse
from datetime import datetime
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tomllib
from urllib.error import HTTPError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import zipfile


RECEIPT = "release-receipt.json"
SUMS = "SHA256SUMS"
WORKFLOW = "computer-mcp/.github/.github/workflows/plugin-release.yml@"
SHA = r"[0-9a-f]{40}"
HASH = r"[0-9a-f]{64}"
VERSION = r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-(?:alpha|beta|rc)\.[1-9][0-9]*)?"
ARCHIVE = r"[A-Za-z0-9][A-Za-z0-9_.-]*\.zip"


class ReleaseError(ValueError):
    pass


class APIError(ReleaseError):
    def __init__(self, status, path):
        self.status = status
        super().__init__(f"GitHub API returned {status}: {path}")


def require(condition, message):
    if not condition:
        raise ReleaseError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()


def positive(value):
    return type(value) is int and value > 0


def digest_value(value):
    require(isinstance(value, str) and re.fullmatch("sha256:" + HASH, value),
            "Expected a GitHub SHA-256 digest")
    return value[7:]


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, new_url):
        require(urlsplit(new_url).scheme == "https", "Refusing a non-HTTPS redirect")
        redirected = super().redirect_request(request, fp, code, message, headers, new_url)
        if redirected is not None:
            redirected.remove_header("Authorization")
        return redirected


class GitHub:
    """REST transport; credentials are sent only to the GitHub API or uploader."""

    def __init__(self, token):
        self.token = token
        self.opener = build_opener(SafeRedirect())

    def _request(self, method, path, data=None, content_type="application/json", binary=False):
        host = "https://uploads.github.com" if method == "POST" and "/assets?" in path else "https://api.github.com"
        require(path.startswith("/repos/") and not path.startswith("//"), "Invalid GitHub API path")
        headers = {"Authorization": f"Bearer {self.token}", "X-GitHub-Api-Version": "2022-11-28",
                   "Accept": "application/octet-stream" if binary else "application/vnd.github+json",
                   "Content-Type": content_type}
        body = data if isinstance(data, bytes) else json.dumps(data).encode() if data is not None else None
        try:
            with self.opener.open(Request(host + path, data=body, headers=headers, method=method), timeout=60) as response:
                content = response.read()
        except HTTPError as error:
            raise APIError(error.code, path) from None
        return content if binary else json.loads(content) if content else None

    def get(self, path):
        return self._request("GET", path)

    def list(self, path, key=None):
        result = []
        for page in range(1, 10001):
            separator = "&" if "?" in path else "?"
            response = self.get(f"{path}{separator}per_page=100&page={page}")
            items = response[key] if key else response
            require(isinstance(items, list), "Invalid GitHub list response")
            result.extend(items)
            if len(items) < 100:
                return result
        raise ReleaseError("GitHub pagination exceeded its limit")

    def download(self, path):
        return self._request("GET", path, binary=True)

    def send(self, method, path, data=None, content_type="application/json"):
        return self._request(method, path, data, content_type)


def repository_path(repository):
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository), "Invalid repository")
    return f"/repos/{repository}"


def resolve(api, repository, ref, publish):
    root = repository_path(repository)
    if re.fullmatch("v" + VERSION, ref):
        tag = api.get(f"{root}/git/ref/tags/{quote(ref, safe='')}")
        require(tag["object"]["type"] == "tag", "Release requires an annotated tag")
        annotated = api.get(f"{root}/git/tags/{tag['object']['sha']}")
        require(annotated.get("tag") == ref and annotated["object"]["type"] == "commit",
                "Annotated tag must point directly to the release commit")
        verification = annotated.get("verification", {})
        require(verification.get("verified") is True and verification.get("reason") == "valid",
                "Tag signature must pass GitHub verification")
        commit = annotated["object"]["sha"]
        tag_name = ref
    else:
        require(not publish, "Publishing requires a signed annotated vX.Y.Z tag")
        require(re.fullmatch(r"[0-9a-f]{7,40}", ref), "Dry-run ref must be a version tag or commit")
        commit = api.get(f"{root}/commits/{ref}")["sha"]
        tag_name = None
    require(re.fullmatch(SHA, commit), "Invalid resolved commit")
    return commit, tag_name


def manifest_info(manifest, tag):
    plugin_id = manifest.get("id")
    version = manifest.get("version")
    require(isinstance(plugin_id, str) and re.fullmatch(r"[a-z0-9][a-z0-9._-]*", plugin_id),
            "Manifest requires a valid plugin id")
    require(isinstance(version, str) and re.fullmatch(VERSION, version), "Manifest requires a valid version")
    require(tag is None or tag == "v" + version, "Manifest version differs from the tag")
    require(positive(manifest.get("plugin_api")), "Manifest plugin_api must be a positive integer")
    compatibility = manifest.get("compatibility", {})
    require(isinstance(compatibility, dict), "Manifest compatibility must be a table")
    declared = compatibility.get("artifacts")
    names = None
    if declared is not None:
        require(isinstance(declared, list) and declared, "Manifest artifacts must be a nonempty array")
        names = [item.get("name") if isinstance(item, dict) else None for item in declared]
        require(all(isinstance(name, str) and re.fullmatch(ARCHIVE, name) for name in names),
                "Manifest artifact names must be ZIP basenames")
        require(len(set(names)) == len(names), "Manifest artifact names must be unique")
        names = sorted(names)
    return {"plugin_id": plugin_id, "version": version, "plugin_api": manifest["plugin_api"],
            "compatibility": compatibility}, names


def archive_names(names, declared):
    require(bool(names), "No plugin archives found")
    require(len(names) == len(set(names)) and all(re.fullmatch(ARCHIVE, name) for name in names),
            "Archive names must be unique ZIP basenames")
    require(sorted(names) == declared if declared is not None else len(names) == 1,
            "Archives differ from compatibility.artifacts (or the required single archive)")


def zip_entries(data):
    result = {}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for entry in archive.infolist():
            path = PurePosixPath(entry.filename)
            require(not path.is_absolute() and ".." not in path.parts and "\\" not in entry.filename
                    and "\x00" not in entry.filename, "Unsafe ZIP member")
            require(entry.filename not in result, "Duplicate ZIP member")
            mode = entry.external_attr >> 16
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR), "ZIP contains a special file")
            if not entry.is_dir():
                result[entry.filename] = archive.read(entry)
    return result


def ci_archives(data, declared):
    contents = zip_entries(data)
    archives = {}
    for path, content in contents.items():
        if path.endswith(".zip"):
            name = PurePosixPath(path).name
            require(name not in archives, "Duplicate CI archive basename")
            archives[name] = content
    archive_names(list(archives), declared)
    return archives


def check_run(run, repository, branch, commit):
    require(run.get("event") == "push" and run.get("head_branch") == branch
            and run.get("head_sha") == commit and run.get("path") == ".github/workflows/ci.yml"
            and run.get("head_repository", {}).get("full_name") == repository,
            "CI must be this repository's default-branch push run of ci.yml for the exact commit")


def select_ci(api, repository, commit, artifact_pattern):
    root = repository_path(repository)
    branch = api.get(root)["default_branch"]
    query = urlencode({"event": "push", "branch": branch, "head_sha": commit})
    runs = api.list(f"{root}/actions/workflows/ci.yml/runs?{query}", "workflow_runs")
    candidates = []
    for run in runs:
        try:
            check_run(run, repository, branch, commit)
        except ReleaseError:
            continue
        if run.get("status") == "completed" and run.get("conclusion") == "success":
            candidates.append(run)
    require(candidates, "No successful authoritative CI run found")
    run = api.get(f"{root}/actions/runs/{max(candidates, key=lambda item: item['id'])['id']}")
    check_run(run, repository, branch, commit)
    require(run.get("status") == "completed" and run.get("conclusion") == "success"
            and positive(run.get("run_attempt")), "Latest CI attempt must have succeeded")
    attempt = api.get(f"{root}/actions/runs/{run['id']}/attempts/{run['run_attempt']}")
    check_run(attempt, repository, branch, commit)
    require(attempt.get("id") == run["id"] and attempt.get("run_attempt") == run["run_attempt"]
            and attempt.get("status") == "completed" and attempt.get("conclusion") == "success",
            "Latest CI attempt must have succeeded")
    name = artifact_pattern.replace("${commit}", commit)
    require(name and "${" not in name, "ci_artifact must be an exact name, optionally containing ${commit}")
    # The artifacts endpoint spans attempts. Creation within the latest attempt
    # excludes outputs retained from a previous attempt or a partial rerun.
    started = datetime.fromisoformat(attempt["run_started_at"].replace("Z", "+00:00"))
    finished = datetime.fromisoformat(attempt["updated_at"].replace("Z", "+00:00"))
    artifacts = api.list(f"{root}/actions/runs/{run['id']}/artifacts", "artifacts")
    matching = [item for item in artifacts if item.get("name") == name
                and started <= datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")) <= finished]
    require(len(matching) == 1, "Expected exactly one named CI artifact from the latest attempt")
    artifact = matching[0]
    require(not artifact.get("expired"), "Selected CI artifact has expired; rerun CI before releasing")
    digest_value(artifact.get("digest"))
    require(positive(artifact.get("id")), "Invalid CI artifact ID")
    return {"run_id": run["id"], "run_attempt": run["run_attempt"],
            "artifacts": [{"id": artifact["id"], "digest": artifact["digest"]}]}


def get_ci_archives(api, repository, commit, ci, declared, recovering=False):
    root = repository_path(repository)
    recovery = "Recorded CI artifact is expired or missing; delete the unpublished draft release, then rerun release.yml to select fresh CI provenance"
    require(len(ci["artifacts"]) == 1, "Rebuild releases require one source CI artifact")
    source = ci["artifacts"][0]
    try:
        artifact = api.get(f"{root}/actions/artifacts/{source['id']}")
        if artifact.get("expired"):
            raise APIError(410, "recorded CI artifact")
        require(artifact.get("id") == source["id"] and artifact.get("digest") == source["digest"],
                "CI artifact digest or ID conflicts with provenance")
        require(artifact.get("workflow_run", {}).get("id") == ci["run_id"]
                and artifact.get("workflow_run", {}).get("head_sha") == commit,
                "CI artifact belongs to another run or commit")
        data = api.download(f"{root}/actions/artifacts/{source['id']}/zip")
    except APIError as error:
        if recovering and error.status in (404, 410):
            raise ReleaseError(recovery) from None
        raise
    require(sha256(data) == digest_value(source["digest"]), "Downloaded CI artifact digest mismatch")
    return ci_archives(data, declared)


def find_release(api, root, tag):
    if tag is None:
        return None
    matches = [release for release in api.list(f"{root}/releases") if release.get("tag_name") == tag]
    require(len(matches) <= 1, "Multiple releases for the tag")
    return matches[0] if matches else None


def release_assets(api, root, release):
    assets = api.list(f"{root}/releases/{release['id']}/assets")
    names = [asset["name"] for asset in assets]
    require(len(names) == len(set(names)), "Duplicate release asset names")
    return {asset["name"]: asset for asset in assets}


def read_asset(api, root, asset):
    require(asset.get("state") == "uploaded", "Release asset is incomplete")
    data = api.download(f"{root}/releases/assets/{asset['id']}")
    require(sha256(data) == digest_value(asset.get("digest")) and len(data) == asset.get("size"),
            "Release asset download differs from its API digest or size")
    return data


def validate_receipt(data):
    receipt = json.loads(data)
    require(isinstance(receipt, dict) and set(receipt) == {
        "schema", "plugin_id", "version", "plugin_api", "compatibility", "tag", "commit",
        "archives", "ci", "workflow", "reproduction"}, "Invalid release receipt fields")
    require(type(receipt["schema"]) is int and receipt["schema"] == 1, "Unsupported receipt schema")
    require(receipt["tag"] is None or isinstance(receipt["tag"], str) and re.fullmatch("v" + VERSION, receipt["tag"]),
            "Invalid receipt tag")
    _, declared = manifest_info({"id": receipt["plugin_id"], "version": receipt["version"],
                                "plugin_api": receipt["plugin_api"], "compatibility": receipt["compatibility"]}, receipt["tag"])
    require(isinstance(receipt["commit"], str) and re.fullmatch(SHA, receipt["commit"]), "Invalid receipt commit")
    require(receipt["reproduction"] == "rebuild", "Shared workflow requires rebuild reproduction")
    ci = receipt["ci"]
    require(isinstance(ci, dict) and set(ci) == {"run_id", "run_attempt", "artifacts"}
            and all(positive(ci[key]) for key in ("run_id", "run_attempt")), "Invalid receipt CI provenance")
    require(isinstance(ci["artifacts"], list) and len(ci["artifacts"]) == 1,
            "Rebuild receipt requires one CI artifact")
    source = ci["artifacts"][0]
    require(isinstance(source, dict) and set(source) == {"id", "digest"} and positive(source["id"]),
            "Invalid receipt artifact provenance")
    digest_value(source["digest"])
    workflow = receipt["workflow"]
    require(isinstance(workflow, dict) and set(workflow) == {"ref", "sha"}
            and isinstance(workflow["sha"], str) and re.fullmatch(SHA, workflow["sha"])
            and workflow["ref"] == WORKFLOW + workflow["sha"], "Invalid receipt workflow provenance")
    archives = receipt["archives"]
    require(isinstance(archives, list) and archives, "Receipt requires archive records")
    for item in archives:
        require(isinstance(item, dict) and set(item) == {"name", "size", "sha256"}
                and isinstance(item["name"], str) and re.fullmatch(ARCHIVE, item["name"])
                and positive(item["size"]) and isinstance(item["sha256"], str) and re.fullmatch(HASH, item["sha256"]),
                "Invalid receipt archive record")
    names = [item["name"] for item in archives]
    archive_names(names, declared)
    require(names == sorted(names) and data == canonical(receipt), "Receipt must use canonical schema 1 encoding")
    return receipt


def checksums(files):
    return "".join(f"{sha256(data)}  {name}\n" for name, data in sorted(files.items())).encode()


def assemble(receipt, archives):
    files = dict(archives)
    require(set(files) == {item["name"] for item in receipt["archives"]}, "Receipt archive set differs")
    for item in receipt["archives"]:
        data = files[item["name"]]
        require(len(data) == item["size"] and sha256(data) == item["sha256"], "Archive differs from receipt")
    files[RECEIPT] = canonical(receipt)
    validate_receipt(files[RECEIPT])
    files[SUMS] = checksums(files)
    return files


def check_assets(assets, files, draft, complete=False):
    require(set(assets) <= set(files), "Release contains unexpected assets")
    if complete:
        require(set(assets) == set(files), "Release asset set is incomplete")
    for name, asset in assets.items():
        if asset.get("state") == "starter" and draft and not complete:
            continue
        require(asset.get("state") == "uploaded" and asset.get("digest") == "sha256:" + sha256(files[name])
                and asset.get("size") == len(files[name]), f"Completed release asset conflicts: {name}")


def build_archives(checkout, command, output, declared):
    require(not output.exists(), "Build output directory must not exist")
    environment = {key: value for key, value in os.environ.items() if key not in ("GH_TOKEN", "GITHUB_TOKEN")}
    subprocess.run(["bash", "-euo", "pipefail", "-c", command + ' "$1"', "plugin-build", str(output)],
                   cwd=checkout, env=environment, check=True)
    require(output.is_dir() and not output.is_symlink(), "Build did not create an output directory")
    archives = {}
    for path in output.iterdir():
        require(path.is_file() and not path.is_symlink() and re.fullmatch(ARCHIVE, path.name),
                "Build output must contain only regular plugin ZIP archives")
        archives[path.name] = path.read_bytes()
    archive_names(list(archives), declared)
    return archives


def verify(api, repository, ref, publish, checkout, build, ci_artifact, workflow_ref, workflow_sha,
           output, build_output):
    root = repository_path(repository)
    commit, tag = resolve(api, repository, ref, publish)
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
    require(actual == commit, "Checkout differs from the resolved release commit")
    manifest = tomllib.loads((checkout / "computer-mcp-plugin.toml").read_text())
    info, declared = manifest_info(manifest, tag)
    release = find_release(api, root, tag)
    if release and release["draft"]:
        require(release["target_commitish"] == commit, "Draft release target differs from the verified commit")
    assets = release_assets(api, root, release) if release else {}
    receipt = None
    if RECEIPT in assets and assets[RECEIPT].get("state") == "uploaded":
        receipt = validate_receipt(read_asset(api, root, assets[RECEIPT]))
        require(all(receipt[key] == value for key, value in info.items())
                and receipt["tag"] == tag and receipt["commit"] == commit,
                "Frozen receipt differs from release source")
    if release and not release["draft"]:
        require(receipt is not None, "Published release lacks a complete receipt; it cannot be modified")
        expected = {item["name"] for item in receipt["archives"]} | {RECEIPT, SUMS}
        require(set(assets) == expected, "Published release asset set differs")
        archives = {item["name"]: read_asset(api, root, assets[item["name"]]) for item in receipt["archives"]}
    else:
        if receipt is None:
            ci = select_ci(api, repository, commit, ci_artifact)
        else:
            ci = receipt["ci"]
        archives = get_ci_archives(api, repository, commit, ci, declared, recovering=receipt is not None)
    rebuilt = build_archives(checkout, build, build_output, declared)
    require(rebuilt == archives, "Rebuilt archives differ byte for byte from the accepted archives")
    for data in archives.values():
        contents = zip_entries(data)
        require("computer-mcp-plugin.toml" in contents, "Archive lacks the root plugin manifest")
        require(tomllib.loads(contents["computer-mcp-plugin.toml"].decode()) == manifest,
                "Archive manifest differs from the release source")
    if receipt is None:
        receipt = dict(info, schema=1, tag=tag, commit=commit,
                       archives=[{"name": name, "size": len(data), "sha256": sha256(data)}
                                 for name, data in sorted(archives.items())], ci=ci,
                       workflow={"ref": workflow_ref, "sha": workflow_sha}, reproduction="rebuild")
    files = assemble(receipt, archives)
    if release:
        check_assets(assets, files, release["draft"], complete=not release["draft"])
    require(not output.exists(), "Release output directory must not exist")
    output.mkdir(parents=True)
    for name, data in files.items():
        (output / name).write_bytes(data)
    return {"commit": commit, "tag": tag or "", "receipt_sha256": sha256(files[RECEIPT])}


def load_bundle(directory, expected_receipt):
    require(directory.is_dir() and not directory.is_symlink()
            and (directory / RECEIPT).is_file() and not (directory / RECEIPT).is_symlink(),
            "Invalid verified bundle file set")
    data = (directory / RECEIPT).read_bytes()
    require(sha256(data) == expected_receipt, "Receipt differs from the verify job's digest")
    receipt = validate_receipt(data)
    expected = {item["name"] for item in receipt["archives"]} | {RECEIPT, SUMS}
    paths = list(directory.iterdir())
    require({path.name for path in paths} == expected
            and all(path.is_file() and not path.is_symlink() for path in paths), "Invalid verified bundle file set")
    files = {path.name: path.read_bytes() for path in paths}
    require(files == assemble(receipt, {item["name"]: files[item["name"]] for item in receipt["archives"]}),
            "Verified bundle checksums differ")
    return receipt, files


def publish_bundle(api, repository, directory, expected_receipt):
    receipt, files = load_bundle(directory, expected_receipt)
    root = repository_path(repository)
    require(receipt["tag"] is not None, "Cannot publish an untagged dry-run bundle")
    commit, tag = resolve(api, repository, receipt["tag"], True)
    require(commit == receipt["commit"], "Release tag moved after verification")
    release = find_release(api, root, tag)
    if release is None:
        release = api.send("POST", f"{root}/releases", {
            "tag_name": tag, "target_commitish": commit, "name": tag, "draft": True,
            "prerelease": "-" in receipt["version"]})
    release_id = release["id"]

    def current():
        observed = api.get(f"{root}/releases/{release_id}")
        require(observed["tag_name"] == tag, "Release tag changed")
        return observed

    def draft():
        observed = current()
        require(observed["draft"], "Release became public; rerun to verify its immutable assets")
        require(observed["target_commitish"] == commit, "Draft release target differs from the verified commit")

    release = current()
    assets = release_assets(api, root, release)
    check_assets(assets, files, release["draft"], complete=not release["draft"])
    if not release["draft"]:
        return {"published": "true", "release_id": str(release_id), "tag": tag}
    draft()
    # Receipt-first upload freezes provenance before any archive is exposed.
    for name in [RECEIPT, *sorted(item["name"] for item in receipt["archives"]), SUMS]:
        assets = release_assets(api, root, release)
        check_assets(assets, files, True)
        asset = assets.get(name)
        if asset and asset["state"] == "uploaded":
            continue
        if asset:
            draft()
            api.send("DELETE", f"{root}/releases/assets/{asset['id']}")
        draft()
        content_type = "application/zip" if name.endswith(".zip") else "application/json" if name == RECEIPT else "text/plain"
        uploaded = api.send("POST", f"{root}/releases/{release_id}/assets?{urlencode({'name': name})}",
                            files[name], content_type)
        check_assets({name: uploaded}, {name: files[name]}, True, complete=True)
    draft()
    check_assets(release_assets(api, root, release), files, True, complete=True)
    require(resolve(api, repository, tag, True) == (commit, tag), "Release tag moved during publication")
    draft()
    # Publishing changes only visibility; release notes remain operator-owned.
    published = api.send("PATCH", f"{root}/releases/{release_id}", {"draft": False})
    require(published.get("draft") is False and published.get("tag_name") == tag, "Release did not become public")
    check_assets(release_assets(api, root, published), files, False, complete=True)
    return {"published": "true", "release_id": str(release_id), "tag": tag}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("resolve", "verify", "publish"):
        command = commands.add_parser(name)
        command.add_argument("--repository", required=True)
        if name != "publish":
            command.add_argument("--ref", required=True)
            command.add_argument("--publish", choices=("true", "false"), required=True)
        if name == "verify":
            for flag in ("checkout", "output", "build-output"):
                command.add_argument("--" + flag, type=Path, required=True)
            for flag in ("build", "ci-artifact", "workflow-ref", "workflow-sha"):
                command.add_argument("--" + flag, required=True)
        if name == "publish":
            command.add_argument("--directory", type=Path, required=True)
            command.add_argument("--receipt-sha256", required=True)
    args = parser.parse_args()
    try:
        api = GitHub(os.environ["GH_TOKEN"])
        if args.command == "resolve":
            commit, tag = resolve(api, args.repository, args.ref, args.publish == "true")
            result = {"commit": commit, "tag": tag or ""}
        elif args.command == "verify":
            result = verify(api, args.repository, args.ref, args.publish == "true", args.checkout.resolve(),
                            args.build, args.ci_artifact, args.workflow_ref, args.workflow_sha,
                            args.output.resolve(), args.build_output.resolve())
            if args.publish == "false":
                print("Dry run: no Release writes. Publication requires a signed annotated v" +
                      tomllib.loads((args.checkout / "computer-mcp-plugin.toml").read_text())["version"] +
                      " tag at the verified commit; record manual acceptance in the Release notes.")
        else:
            result = publish_bundle(api, args.repository, args.directory, args.receipt_sha256)
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as output:
                for key, value in result.items():
                    output.write(f"{key}={value}\n")
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
