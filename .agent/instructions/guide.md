---
description: Route changes to computer-mcp organization data, conventions, design assets and shared instruction units.
---
# Organization Agent Guide

Read `README.md` first for repository purpose and entry points.

## Task Route

- For the public organization entry point, edit `profile/catalog.json` and
  regenerate `profile/README.md`; `README.md` gives the commands.
- For conventions shared by every repository, read `MAINTENANCE.md`.
- Before changing shared version, plugin compatibility or dependency rules,
  read `VERSIONING.md`.
- For repository settings, GitHub Apps and Actions credentials, change
  `MAINTENANCE.md` with the setting; the organization check in
  [computer-mcp/github-workflows](https://github.com/computer-mcp/github-workflows)
  compares it with live settings.
- For visual identity, read `DESIGN.md`. Icon sources and their provenance live
  in `.github/design/icons/`, fonts in `.github/design/fonts/`, and `README.md`
  gives the generator and toolchain commands.
- For a reusable workflow or a check more than one repository needs, work in
  `computer-mcp/github-workflows`; this repository keeps only thin callers.
- For positioning, the tagline and other text rendered into images, read the
  main repository's
  [ProductIdentity](https://github.com/computer-mcp/computer-mcp/blob/master/Documentation/Architecture/ProductIdentity.md).
- `.agent/instructions/shared/` holds the instruction units member plugins
  install; state only rules that hold for every member plugin, and regenerate
  the plugins after changing them.

## Repository Guardrails

- Text rendered into images must match ProductIdentity. Preserve repository
  visibility and integration ownership.
- Change `DESIGN.md` or `profile/catalog.json`, regenerate, and commit inputs
  and outputs together. Never edit generated files by hand.
- Before committing, lint DESIGN and check the profile with the
  `github-readme-design` toolchain.
- Deliver icons and social previews to other repositories through a pull
  request in each repository, and record each consumed copy in the icon's
  `provenance.json`.
- Profile content must be understandable from committed artifacts alone.
