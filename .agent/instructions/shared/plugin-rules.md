---
description: Keep a Computer MCP plugin free of vendor software and host authority, and validate its package before handoff.
---
## Plugin Rules

- Read `README.md`, `CONTRIBUTING.md` and `computer-mcp-plugin.toml` before
  editing. Before changing versions, compatibility or release workflows, read
  the organization [VERSIONING](https://github.com/computer-mcp/.github/blob/master/VERSIONING.md)
  and this repository's release reference.
- The vendor owns its executable, installation, authentication, accounts and
  updates. Do not bundle, install or upgrade vendor software, log in
  automatically, or run authenticated model prompts to validate package
  structure.
- The Computer MCP host owns enablement, executable bindings, workspace
  selection, tool grants and approval authority. Manifest defaults, skill text
  and adapter defaults never grant access or raise permissions.
- When the plugin ships interface data such as `cli-tree.json`, generate it
  only from verified native `--help` and `--version` output, keep its coverage
  explicitly partial, and never hand-edit generated output.
- Before handoff, build the package deterministically and run the host's
  package validation where available. Do not publish repositories or releases
  implicitly.
