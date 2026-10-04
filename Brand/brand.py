#!/usr/bin/env python3
"""Check Computer MCP brand exports and deliver them to consumer repositories.

    python3 Brand/brand.py check                         exports match the manifest and current inputs
    python3 Brand/brand.py sync <checkout> [--repository NAME]
                                                         copy exports into a consumer and rewrite its lock
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

BRAND = Path(__file__).resolve().parent
ROOT = BRAND.parent
EXPORTS = BRAND / "Exports"
VERIFIER = ROOT / ".github/workflows/brand-check.yml"
LOCK = ".github/brand/brand.lock.json"
CONFIG = json.loads((BRAND / "config.json").read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finish(errors, success):
    print("\n".join(errors) or success, flush=True)
    return 1 if errors else 0


def check():
    manifest = json.loads((EXPORTS / "manifest.json").read_text())
    errors = [
        f"Exports are stale for {name}; run node Brand/render.mjs"
        for name, expected in manifest["inputs"].items()
        if digest(ROOT / name) != expected
    ]
    present = {p.relative_to(EXPORTS).as_posix() for p in EXPORTS.rglob("*") if p.is_file() and p.name != ".DS_Store"}
    present.discard("manifest.json")
    errors += [f"Export not in manifest: {name}" for name in sorted(present - manifest["exports"].keys())]
    errors += [f"Missing export: {name}" for name in sorted(manifest["exports"].keys() - present)]
    errors += [
        f"Export drift: {name}"
        for name, expected in manifest["exports"].items()
        if name in present and digest(EXPORTS / name) != expected
    ]
    return finish(errors, f"{len(present)} brand exports match their manifest")


def repository_of(checkout):
    url = subprocess.run(
        ["git", "-C", str(checkout), "remote", "get-url", "origin"], capture_output=True, text=True, check=True
    ).stdout.strip()
    return url.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1].rsplit(":", 1)[-1]


def resolve(repository):
    member = next((m for m in CONFIG["members"] if m["repository"] == repository), None)
    spec = CONFIG["consumers"].get(repository)
    if spec is None:
        if member is None:
            raise SystemExit(f"{repository} is not a brand consumer or member")
        spec = json.loads(json.dumps(CONFIG["consumers"]["@member"]).replace("{repository}", repository))
    values = {f"@headline.{locale}": text for locale, text in CONFIG["copy"]["headline"].items()}
    if member:
        values["@title"] = member["title"]
    entries = {name: [values.get(item, item) for item in items] for name, items in spec["entries"].items()}
    return spec, entries


def deliveries(spec):
    for target, source in spec["files"].items():
        origin = EXPORTS / source
        if source.endswith("/"):
            for file in sorted(p for p in origin.rglob("*") if p.is_file()):
                yield target + file.relative_to(origin).as_posix(), file
        else:
            yield target, origin


def inside(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise SystemExit(f"Delivery path escapes the checkout: {name}")
    return path


def verify(root):
    workflow = VERIFIER.read_text()
    script = workflow.split("<<'PY'\n", 1)[1].split("\n          PY\n", 1)[0]
    return subprocess.run([sys.executable, "-"], input=textwrap.dedent(script), text=True, cwd=root).returncode


def sync(checkout, repository):
    if check():
        return 1
    root = Path(checkout).resolve()
    repository = repository or repository_of(root)
    spec, entries = resolve(repository)
    lock_path = inside(root, LOCK)
    previous = json.loads(lock_path.read_text())["files"] if lock_path.exists() else {}
    files = {}
    for target, source in deliveries(spec):
        path = inside(root, target)
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, path)
        files[target] = digest(path)
    for stale in previous.keys() - files.keys():
        inside(root, stale).unlink(missing_ok=True)
    lock = {
        "schema_version": 2,
        "authority": CONFIG["authority"],
        "revision": digest(EXPORTS / "manifest.json"),
        "consumer": repository,
        "files": files,
        "entries": entries,
    }
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")
    print(f"Delivered {len(files)} brand files to {repository}", flush=True)
    return verify(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check")
    deliver = commands.add_parser("sync")
    deliver.add_argument("checkout")
    deliver.add_argument("--repository")
    args = parser.parse_args()
    return check() if args.command == "check" else sync(args.checkout, args.repository)


if __name__ == "__main__":
    sys.exit(main())
