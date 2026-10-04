# Agent guide

This repository owns Computer MCP's organization profile and visual identity:
`DESIGN.md`, the renderer and exports in `Brand/`, and the reusable brand check.
Product meaning stays with the main repository's ProductIdentity; text rendered
into images must match it. Preserve repository visibility and integration
ownership.

- Change `DESIGN.md` or `Brand/config.json`, re-render, and commit the exports
  with their manifest. Never edit exports by hand.
- Before committing, run `npm --prefix Brand run lint` and
  `python3 Brand/brand.py check`.
- Deliver artwork to other repositories only with `python3 Brand/brand.py sync`,
  through a pull request in each repository.

Keep `.agent/` local and untracked. Profile content must be understandable from
committed artifacts alone.
