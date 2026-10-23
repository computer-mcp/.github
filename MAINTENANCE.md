# Maintenance

These conventions apply to every Computer MCP repository.
[VERSIONING.md](VERSIONING.md) owns shared version, tag, release-record, plugin
compatibility and dependency rules. Each repository owns its version sources,
release procedure and written exceptions.

## Branches and changes

- The default branch is `master`. A fork keeps its upstream branch names; the
  MCP Swift SDK fork's default branch is its maintained release branch.
- Changes land through pull requests with passing checks and are squash merged.
  Merged branches are deleted automatically.
- Maintainer commits use the owner's name `showxu` and noreply email
  `10173746+showxu@users.noreply.github.com`, and are SSH-signed as described
  under [Signing](#signing). Commits that GitHub makes, such as squash merges
  and the Computer MCP Updater App's proposals, are signed by GitHub.
  Dependabot may author changes.
- Pull request titles and commit subjects follow Conventional Commits:
  `type(scope)!: subject`, with optional scope and `!`. Types are `build`,
  `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`, `revert`, `style`
  and `test`.
- Commits and pull requests carry no tool or agent attribution, such as
  generated-by lines or co-author trailers for tools; real human co-authors may
  be credited.
- Committed content contains no paths from a maintainer's machine, such as
  `/Users/<name>/`, and no references into local `.agent/` task state.
- The [source policy](https://github.com/computer-mcp/github-workflows#source-policy)
  checks pull request titles, added content and added or modified paths, and
  requires default-branch commits to be verified and committed by GitHub or the
  owner.
- Each public repository enforces these rules with a `default branch` ruleset
  that has no bypass: it blocks deletion and force pushes, requires signed
  commits, and accepts only squash-merged pull requests whose required checks
  pass. The host repository, `computer-mcp`, whose pull requests often build on
  one another, merges through a merge queue instead of requiring branches to be
  up to date: the queue squash merges each pull request only after its own
  required checks pass on its queued result, and its CI also runs on
  `merge_group` events. Automation proposes its changes as pull requests that merge
  automatically once those checks pass. It acts through the Computer MCP
  Updater GitHub App, installed only where automation proposes changes: the
  App's installation token has GitHub create each proposal commit through the
  API, which GitHub signs, and opens the pull request, whose checks then run on
  their own. A commit made with `git commit` in a workflow is unsigned, and a
  pull request opened with the workflow token waits for manual approval before
  its checks run.

## Signing

Configure signing in each repository checkout with the owner's registered SSH
signing key; do not change global Git configuration:

```sh
git config user.name showxu
git config user.email 10173746+showxu@users.noreply.github.com
git config gpg.format ssh
git config user.signingkey ~/.ssh/signing_key.pub
git config commit.gpgsign true
git config tag.gpgsign true
git config gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
```

Replace the key and allowed-signers paths with the local signing
configuration. The allowed-signers file holds the signer's email followed by
the SSH public key, which is registered as a signing key on GitHub. Verify
commits with `git verify-commit HEAD`.

## Licenses

- The App, the plugins and the website use the Functional Source License 1.1
  with the Apache 2.0 future license (FSL-1.1-ALv2). Their `LICENSE` files are
  identical, and each release becomes available under Apache-2.0 two years
  after publication.
- Apple CLI and the Homebrew tap use Apache-2.0. The MCP Swift SDK fork keeps
  its upstream license. This repository has no license of its own.
- A license change applies from the next release; published releases keep the
  license they shipped with. Bundled third-party material keeps its own
  license, listed in the repository's `THIRD_PARTY_NOTICES.md`.

## Plugins

After a plugin release, its `notify-catalog.yml` workflow asks the website to
refresh the plugin catalog through the Computer MCP Release Notifier GitHub App.

## GitHub settings

`python3 Scripts/check-settings.py` compares the organization's live settings
with this section and the rulesets above, and lists every difference. Run it
with an organization owner's `gh` login after changing a repository setting,
an App or an Actions credential, and update this section in the same change.

- Every repository allows only squash merges and deletes merged branches. Its
  workflows, like the organization default, get a read-only token that cannot
  approve pull requests.
- Each public repository's `default branch` ruleset requires at least one
  check; each repository's CI owns which. The `computer-mcp` default branch
  ruleset is the only ruleset with a merge queue, and its required checks do
  not also require an up-to-date branch.
- Only these GitHub Apps are installed. Each has exactly the listed
  permissions, is installed only on the listed repositories and subscribes to
  no events:

| App | Permissions | Installed on | Credentials | Stored in |
| --- | --- | --- | --- | --- |
| `computer-mcp-release-notifier` | `actions: write` | `computer-mcp.github.io` | `CATALOG_APP` | `plugin-claude`, `plugin-codex`, `plugin-computer-use`, `plugin-cursor`, `plugin-swift-format` |
| `computer-mcp-updater` | `contents: write`, `pull_requests: write` | `computer-mcp.github.io`, `homebrew-tap` | `AUTOMATION_APP` | `computer-mcp.github.io`, `homebrew-tap` |

- A repository that uses an App keeps the App's client ID in the
  `<credentials>_CLIENT_ID` variable and its private key in the
  `<credentials>_PRIVATE_KEY` secret. No repository and not the organization
  holds any other Actions secret or variable.

## Repository layout

- The root `README.md` is the entry point. `Documentation/Architecture/` holds
  current design truth, `Documentation/Reference/` operating detail and
  `Documentation/Decisions/` accepted rationale.
- Repository-specific automation lives in lowercase `scripts/`, created only
  when needed. Executable scripts use kebab-case names with an extension;
  imported Python modules use snake_case. Reusable workflows and the checks
  more than one repository needs live in
  [computer-mcp/github-workflows](https://github.com/computer-mcp/github-workflows),
  which repositories pin by full commit SHA; this repository holds only rules,
  data, documents and thin callers.
- GitHub presentation assets live in `.github/assets/`: `logo/` with
  `logo-light.png` and `logo-dark.png`, `social-preview/social-preview.png`,
  and `terminal/` or `screenshots/` where the product has them.
- `AGENTS.md` carries the shared first-principles and canonical-artifact
  sections, then routes agents through the repository's own documents.
  `.agent/` stays local and untracked.

## Community files

GitHub applies this repository's community files to every repository that has
no version of its own:

- `CODE_OF_CONDUCT.md`, `SUPPORT.md`, `GOVERNANCE.md`, the issue templates and
  the pull request template live only here.
- `CONTRIBUTING.md` and `SECURITY.md` here are fallbacks. A repository keeps a
  short `CONTRIBUTING.md` with its own build and verification commands and its
  contribution terms, and its own `SECURITY.md` only when its security scope
  differs.
- A repository's own `.github/ISSUE_TEMPLATE/` replaces these templates
  entirely, so repository-specific fields belong in the shared templates.
- `LICENSE`, `.github/CODEOWNERS`, `.github/dependabot.yml` and workflows are
  not inherited; each repository carries its own.
- The MCP Swift SDK fork keeps its upstream files.
