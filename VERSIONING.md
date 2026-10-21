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
