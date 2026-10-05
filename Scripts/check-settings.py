#!/usr/bin/env python3
"""Compare the organization's live GitHub settings with MAINTENANCE.md.

    python3 Scripts/check-settings.py    list every difference, using an organization owner's gh login
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ORG = "computer-mcp"
MAINTENANCE = Path(__file__).resolve().parent.parent / "MAINTENANCE.md"
SECTION = "## GitHub settings"
COLUMNS = ["App", "Permissions", "Installed on", "Credentials", "Stored in"]
READ_ONLY = {"default_workflow_permissions": "read", "can_approve_pull_request_reviews": False}
MERGES = {
    "allow_squash_merge": True,
    "allow_merge_commit": False,
    "allow_rebase_merge": False,
    "delete_branch_on_merge": True,
}
RULES = {"deletion", "non_fast_forward", "required_signatures", "pull_request", "required_status_checks"}


class ApiError(Exception):
    pass


def gh(path):
    result = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if result.returncode:
        raise ApiError(f"gh api {path}: {result.stderr.strip() or result.stdout.strip()}")
    return json.loads(result.stdout)


def expected_apps():
    text = MAINTENANCE.read_text()
    if SECTION not in text:
        raise SystemExit(f"MAINTENANCE.md has no {SECTION!r} section")
    section = text.split(SECTION, 1)[1].split("\n## ", 1)[0]
    rows = [line.strip().strip("|").split("|") for line in section.splitlines() if line.startswith("|")]
    if not rows or [cell.strip() for cell in rows[0]] != COLUMNS:
        raise SystemExit(f"MAINTENANCE.md: the GitHub Apps table must have the columns {', '.join(COLUMNS)}")
    apps = {}
    for row in rows[2:]:
        cells = [re.findall(r"`([^`]+)`", cell) for cell in row]
        try:
            (slug,), permissions, installed, (prefix,), stored = cells
            permissions = dict(permission.split(": ") for permission in permissions)
        except ValueError:
            raise SystemExit(f"MAINTENANCE.md: malformed GitHub Apps row: |{'|'.join(row)}|")
        apps[slug] = {"permissions": permissions, "installed": sorted(installed), "prefix": prefix, "stored": stored}
    return apps


def ruleset_problems(repo):
    ids = [ruleset["id"] for ruleset in gh(f"repos/{ORG}/{repo}/rulesets?includes_parents=false") if ruleset["name"] == "default branch"]
    if not ids:
        return [f"{repo}: no default branch ruleset"]
    ruleset = gh(f"repos/{ORG}/{repo}/rulesets/{ids[0]}")
    rules = {rule["type"]: rule.get("parameters", {}) for rule in ruleset["rules"]}
    problems = []
    if ruleset["enforcement"] != "active":
        problems.append(f"{repo}: default branch ruleset is {ruleset['enforcement']}")
    if ruleset["conditions"]["ref_name"]["include"] != ["~DEFAULT_BRANCH"]:
        problems.append(f"{repo}: default branch ruleset targets {ruleset['conditions']['ref_name']['include']}")
    if ruleset["bypass_actors"]:
        problems.append(f"{repo}: default branch ruleset has bypass actors")
    if missing := RULES - rules.keys():
        problems.append(f"{repo}: default branch ruleset lacks {', '.join(sorted(missing))}")
    else:
        if rules["pull_request"]["allowed_merge_methods"] != ["squash"]:
            problems.append(f"{repo}: default branch ruleset allows {rules['pull_request']['allowed_merge_methods']}")
        if not rules["required_status_checks"]["required_status_checks"]:
            problems.append(f"{repo}: default branch ruleset requires no checks")
    return problems


def app_problems(apps, notes):
    problems = []
    installed = {installation["app_slug"]: installation for installation in gh(f"orgs/{ORG}/installations?per_page=100")["installations"]}
    for slug in sorted(installed.keys() - apps.keys()):
        problems.append(f"{slug}: installed but not listed in MAINTENANCE.md")
    for slug, app in apps.items():
        installation = installed.get(slug)
        if not installation:
            problems.append(f"{slug}: not installed")
            continue
        permissions = {name: access for name, access in installation["permissions"].items() if name != "metadata"}
        if permissions != app["permissions"]:
            problems.append(f"{slug}: permissions {permissions}, expected {app['permissions']}")
        if installation["events"]:
            problems.append(f"{slug}: subscribes to {', '.join(installation['events'])}")
        if installation["repository_selection"] != "selected":
            problems.append(f"{slug}: installed on all repositories")
            continue
        try:
            listed = gh(f"user/installations/{installation['id']}/repositories?per_page=100")["repositories"]
        except ApiError:
            notes.append(
                f"{slug}: installed repositories not checked; GitHub lists them only to a personal access token, "
                "so compare them on the App's installation page"
            )
            continue
        repositories = sorted(repository["name"] for repository in listed)
        if repositories != app["installed"]:
            problems.append(f"{slug}: installed on {', '.join(repositories)}, expected {', '.join(app['installed'])}")
    return problems


def main():
    apps = expected_apps()
    credentials = {}
    for app in apps.values():
        for repo in app["stored"]:
            secrets, variables = credentials.setdefault(repo, (set(), set()))
            secrets.add(f"{app['prefix']}_PRIVATE_KEY")
            variables.add(f"{app['prefix']}_CLIENT_ID")

    try:
        problems, notes = [], []
        if (flow := gh(f"orgs/{ORG}/actions/permissions/workflow")) != READ_ONLY:
            problems.append(f"organization: workflow token {flow}")
        for kind in ("secrets", "variables"):
            if names := [item["name"] for item in gh(f"orgs/{ORG}/actions/{kind}?per_page=100")[kind]]:
                problems.append(f"organization: Actions {kind} {', '.join(names)}")

        repos = {repo["name"]: repo for repo in gh(f"orgs/{ORG}/repos?type=all&per_page=100") if not repo["archived"]}
        listed = set(credentials).union(*(app["installed"] for app in apps.values()))
        for repo in sorted(listed - repos.keys()):
            problems.append(f"{repo}: listed in MAINTENANCE.md but not in the organization")
        for repo in sorted(repos):
            detail = gh(f"repos/{ORG}/{repo}")
            if (merges := {name: detail[name] for name in MERGES}) != MERGES:
                problems.append(f"{repo}: merge settings {merges}")
            if (flow := gh(f"repos/{ORG}/{repo}/actions/permissions/workflow")) != READ_ONLY:
                problems.append(f"{repo}: workflow token {flow}")
            for kind, expected in zip(("secrets", "variables"), credentials.get(repo, (set(), set()))):
                names = {item["name"] for item in gh(f"repos/{ORG}/{repo}/actions/{kind}?per_page=100")[kind]}
                if names != expected:
                    problems.append(f"{repo}: Actions {kind} {sorted(names)}, expected {sorted(expected)}")
            if not detail["private"]:
                problems += ruleset_problems(repo)
        problems += app_problems(apps, notes)
    except ApiError as error:
        raise SystemExit(str(error))

    print("\n".join(problems + notes) or "GitHub settings match MAINTENANCE.md", flush=True)
    if problems:
        return 1
    if notes:
        print("Other GitHub settings match MAINTENANCE.md", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
