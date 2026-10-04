# Computer MCP organization

This repository owns the organization profile and the visual identity every
Computer MCP repository shares.

- `profile/README.md` is the public organization entry point.
- `DESIGN.md` is the design system: tokens, components, the icon family and
  composition rules.
- `Brand/` holds the renderer, its configuration and the rendered `Exports/`
  with their `manifest.json`.
- `.github/workflows/brand-check.yml` is the reusable workflow each repository
  calls to verify its brand lock.

Product meaning and copy belong to the main repository's
[ProductIdentity](https://github.com/computer-mcp/computer-mcp/blob/master/Documentation/Architecture/ProductIdentity.md).
Text rendered into images (`Brand/config.json` `copy` and `members`) must match it.

## Updating the brand

1. Edit `DESIGN.md` or `Brand/config.json`.
2. Render: `npm ci --prefix Brand`, `npx --prefix Brand playwright install --only-shell chromium`,
   then `node Brand/render.mjs`.
3. Preview each macOS rendition of the App icon with Icon Composer's `ictool
   Brand/Exports/app/AppIcon.icon --export-image --platform macOS --rendition <name>`
   for Default, Dark, ClearLight, ClearDark, TintedLight and TintedDark.
4. Check: `npm --prefix Brand run lint` and `python3 Brand/brand.py check`.
5. Commit `DESIGN.md`, `Brand/` and the exports together.

## Delivering to a repository

`python3 Brand/brand.py sync <checkout>` copies the files that repository uses,
removes files its previous lock delivered and no longer needs, rewrites its
`.github/brand/brand.lock.json`, and verifies the lock. Images that ship with a
repository's packaged documentation live in `Documentation/Brand/`; social
previews stay in `.github/brand/`. Commit the result through a pull request in
that repository. Each repository's CI calls the shared check:

```yaml
jobs:
  brand:
    uses: computer-mcp/.github/.github/workflows/brand-check.yml@<commit>
```
