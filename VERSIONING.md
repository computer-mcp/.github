# Versioning

These rules apply to every Computer MCP repository. Each repository's
`Documentation/Architecture/VersioningAndRelease.md`, or its README where it
has none, owns its version sources, release procedure and written exceptions.

## Versions

Versions follow [Semantic Versioning 2.0.0](https://semver.org/):

- While a component is `0.x`, fixes increment the patch number; new
  capabilities and incompatible changes increment the minor number.
- Prereleases use `-alpha.N`, `-beta.N` and `-rc.N`.
- `1.0.0` marks a stable public interface; from then on, incompatible changes
  increment the major number, compatible new capabilities increment the minor
  number, and fixes increment the patch number.
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

## Plugin versions and compatibility

Every `computer-mcp-plugin.toml` declares a required top-level positive integer
`plugin_api`, starting at `1`. It identifies the complete manifest schema and
runtime contract: contribution kinds and their fields, executable launch,
host-provided environment and arguments, and host checks. Any addition,
removal or reinterpretation of a manifest field, including an optional field,
or a change to the runtime contract defines a new plugin API version. A
manifest uses only the fields its declared API version defines.

The host declares a closed range of consecutive plugin API versions and
reports that range in `computer-mcp build-info` as `plugin_api`
with `minimum` and `maximum`. Removing support for the oldest API version is a
breaking host change. The host's
[Plugin API decision](https://github.com/computer-mcp/computer-mcp/blob/master/Documentation/Decisions/PluginAPI.md)
owns decoding and compatibility evaluation.

`compatibility.minimum_host` is the inclusive lower host-version bound;
`compatibility.maximum_host`, when present, is the exclusive upper bound.
These constrain host releases within one plugin API version, such as requiring
a host fix. A new manifest field is signalled by `plugin_api`.

The package's SemVer `version` is independent of `plugin_api`. A plugin can
release fixes and capabilities within the same API version; its package
version and the host's release version need not match that API number or one
another.

## Plugin release contents

A plugin Release contains the plugin ZIP archives, `release-receipt.json` and
`SHA256SUMS`. Archive names are exactly those in the tagged manifest's
`compatibility.artifacts`; without that declaration the package has one ZIP
archive. Each archive contains the tagged `computer-mcp-plugin.toml` at its root.
Builder metadata inside an Actions artifact is not a Release asset.

`release-receipt.json` schema **1** has these fields:

| Field | Meaning |
| --- | --- |
| `schema` | Integer `1` |
| `plugin_id`, `version`, `plugin_api` | Tagged manifest ID, SemVer and positive integer plugin API |
| `compatibility` | The manifest's compatibility table, including artifact declarations when present; `{}` if absent |
| `tag`, `commit` | Signed annotated version tag and its full source commit SHA; `tag` is `null` only for an untagged dry run |
| `archives` | Records sorted by name: `name` (ZIP basename), `size` (bytes), `sha256` (lowercase hexadecimal) |
| `ci` | `run_id`, `run_attempt` and `artifacts`: source Actions artifact records with `id` and `digest` (`sha256:` followed by lowercase hexadecimal), sorted by ID |
| `workflow` | `ref` (repository/workflow path with `@ref`) and `sha` (full commit of that release workflow) |
| `reproduction` | `rebuild`, or `ci-artifact-promotion` for the Codex exception below |

The receipt has no timestamps or machine paths. Encode it as UTF-8 JSON with
sorted object keys, two-space indentation, ASCII escapes and one trailing LF
(`json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"`).
`SHA256SUMS` contains lowercase SHA-256, two spaces, filename and LF, sorted by
filename. It covers every archive and the receipt; it does not hash itself.
Human acceptance results and their limits belong in the Release notes.

The reusable
[plugin release workflow](.github/workflows/plugin-release.yml) uses the
repository's default-branch `push` run of `.github/workflows/ci.yml` for the
exact source commit. It selects the latest successful matching run and rechecks
its latest attempt. The exact `ci_artifact` name selects one artifact
created within that attempt, with a recorded and verified API digest. Outputs
left from earlier attempts cannot supply a new release. The caller's build runs
in a separate job with no repository permissions or secret inputs and uploads
its archives as an Actions artifact. A fresh verification runner executes only
the pinned helper, reads the source manifest as data, checks both artifact
downloads against their API digests and requires byte equality between the
build and CI archives. The shared workflow's receipt records one source CI
artifact and `reproduction: rebuild`.

Plugin repositories must enable GitHub release immutability. Before any Release
write, the workflow verifies that repository setting through the API and
refuses publication if it is disabled or cannot be verified. The server rejects
asset mutations on immutable releases, including when another publisher makes a
draft public between this workflow's draft precheck and mutation request.
Enabling the setting does not lock previously published releases. The workflow
requires the Release's own `immutable: true` both when accepting an existing
public Release and in the response after publishing a draft. A public but
mutable Release fails with an error requiring the repository owner to handle it;
the workflow does not change it or report it as published.

Publication creates or resumes a commit-bound draft. It uploads the receipt
first, then the archives, then `SHA256SUMS`, and checks the complete asset set,
sizes and API digests before making the draft public. The uploaded receipt
freezes the CI run, attempt, artifact IDs and digests, and release workflow
reference and commit. Recovery reuses that receipt and the recorded artifacts.
It validates the recorded historical run attempt through the API: this
repository's default-branch `push` run of `.github/workflows/ci.yml`, completed
successfully at the exact source commit, with the artifact created within that
attempt. An unavailable or invalid recorded attempt fails recovery. Recovery
does not select a newer CI run or rewrite provenance after a CI rerun or
workflow update.

Verification passes the exact uploaded bundle artifact ID and every release
file's SHA-256 through job outputs. Publication downloads that ID and recomputes
every digest before any Release write. Retrying only a failed publish job uses
the original bundle and verification outputs even though the run attempt has
changed.

An interrupted asset in GitHub's `starter` state may be deleted and uploaded
again only while the Release is still a draft. Completed assets must have
expected names, sizes and matching digests; conflicts or unexpected assets fail
without replacement. If a frozen artifact expires or disappears, delete the
unpublished draft, obtain fresh successful CI artifacts, and rerun publication.
A public Release is never changed by the workflow. A repeat verifies the exact
asset set against the frozen receipt and reports it as published; CI artifact
retention does not invalidate an already complete public Release.

Dry runs perform the same source, CI, rebuild and assembly checks without any
Release writes or catalog credentials. A commit dry run omits tag and signature
checks and reports the signed tag still required for publication. See the
[consumer guide](Documentation/Reference/PluginRelease.md) for inputs, outputs,
the caller workflow and recovery operations.

### Codex promotion exception

The Codex plugin's native archives cannot be reproduced byte for byte. Its own
release workflow promotes the accepted CI artifacts, verifies signed annotated
tags, and uses schema 1 with `reproduction: ci-artifact-promotion`. Its `ci`
records every source artifact. Each archive record additionally has
`native_receipt`, an object with `name`, `size` and `sha256` for its native build
receipt. Those `<archive-stem>.receipt.json` files remain Release assets and
inputs to Codex's `check-package.py`; `SHA256SUMS` covers them as well as the
archives and unified receipt. Codex follows the same receipt-first draft,
frozen provenance, digest verification, publication and recovery rules. Its
repository owns native archive acceptance and the promotion implementation.

## Swift dependencies

`Package.swift` owns requirements; `Package.resolved` records selected versions
and revisions. Repositories that build executable artifacts commit
`Package.resolved`, and CI checks for lockfile drift.

| Dependency kind | Requirement |
| --- | --- |
| Organization fork or dependency below `1.0.0` | `exact:` |
| Dependency at `1.0.0` or later at a process, transport or security boundary, including swift-subprocess, swift-crypto and swift-nio | `.upToNextMinor(from:)` |
| Other dependency at `1.0.0` or later | `from:` (up to the next major version) |

The organization-fork rule takes precedence over the boundary rule. Shared
dependencies use these baseline versions:

| Dependency | Baseline | Requirement |
| --- | --- | --- |
| swift-subprocess | `1.0.2` | `.upToNextMinor(from: "1.0.2")` |
| MCP Swift SDK organization fork (`computer-mcp/swift-sdk`) | `0.13.1-computer-mcp.1` | `exact: "0.13.1-computer-mcp.1"` |
| Other dependencies | Each repository's currently resolved version is its lower bound | Requirement kind above |

The host, plugin-codex and apple-cli use the MCP Swift SDK organization fork.
The host's `Tools/Validation` deliberately keeps the unmodified upstream
`modelcontextprotocol/swift-sdk` at an exact upstream version as an independent
client for gateway interoperability checks. Its
[README](https://github.com/computer-mcp/computer-mcp/blob/master/Tools/Validation/README.md)
owns that exception and the package owns its current pin.
