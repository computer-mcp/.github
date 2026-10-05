# Maintenance

These conventions apply to every Computer MCP repository. Each repository's
`Documentation/Architecture/VersioningAndRelease.md`, or its README where it
has none, owns that repository's own version and release rules; this file holds
only what they share.

## Branches and changes

- The default branch is `master`. A fork keeps its upstream branch names; the
  MCP Swift SDK fork's default branch is its maintained release branch.
- Changes land through pull requests with passing checks and are squash merged.
  Merged branches are deleted automatically.
- Commits and tags are signed.
- Each public repository enforces these rules with a `default branch` ruleset
  that has no bypass: it blocks deletion and force pushes, requires signed
  commits, and accepts only squash-merged pull requests whose required checks
  pass. Automation proposes its changes as pull requests that merge
  automatically once those checks pass. It has GitHub create each proposal
  commit through the API with the workflow token, which GitHub signs, because
  a commit made with `git commit` in a workflow is unsigned and cannot merge.

## Versions

Versions follow [Semantic Versioning 2.0.0](https://semver.org/):

- While a component is `0.x`, fixes increment the patch number; new
  capabilities and incompatible changes increment the minor number.
- Prereleases use `-alpha.N`, `-beta.N` and `-rc.N`.
- `1.0.0` marks a stable public interface; from then on, incompatible changes
  increment the major number.
- Documentation, CI and cleanup changes alone do not require a release.

## Tags and release records

- New tags are signed annotated `vX.Y.Z` tags. The MCP Swift SDK fork tags
  `X.Y.Z-computer-mcp.N`. Published tags and release assets are never moved or
  replaced; a later fix ships as a new version.
- The GitHub Release is the formal record. Each releasing repository keeps a
  `CHANGELOG.md` with an `## Unreleased` section and
  `## X.Y.Z — YYYY-MM-DD` sections.
- Per-version process files are not committed. Release notes and reports are
  rendered from the changelog and version-independent templates.

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

Each plugin declares `minimum_host` in `computer-mcp-plugin.toml`. After a
release, its `notify-catalog.yml` workflow asks the website to refresh the
plugin catalog.

## Repository layout

- The root `README.md` is the entry point. `Documentation/Architecture/` holds
  current design truth, `Documentation/Reference/` operating detail and
  `Documentation/Decisions/` accepted rationale.
- Scripts live in `Scripts/`. Executable scripts use kebab-case names with an
  extension; imported Python modules use snake_case.
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
