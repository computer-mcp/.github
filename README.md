# Computer MCP organization

This repository owns the organization profile, the visual identity and the
conventions every Computer MCP repository shares.

- `profile/README.md` is the public organization entry point.
- `MAINTENANCE.md` holds the cross-repository conventions. The community files
  (`CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`, `SECURITY.md`,
  `SUPPORT.md`, `.github/ISSUE_TEMPLATE/` and the pull request template) apply
  to every repository without its own version.
- [VERSIONING.md](VERSIONING.md) holds shared version, tag, release-record,
  plugin compatibility and dependency rules.
- `Scripts/check-settings.py` compares the organization's live GitHub settings,
  Apps and Actions credentials with `MAINTENANCE.md`.
- `DESIGN.md` is the design system: tokens, components, the icon family and
  composition rules.
- `Brand/` holds the renderer, its configuration, the App icon's original layers
  in `Brand/app-icon/layers/` and the rendered `Exports/` with their
  `manifest.json`.
- `.github/workflows/brand-check.yml` is the reusable workflow each repository
  calls to verify its brand lock.
- [PluginRuntime/](PluginRuntime/README.md) holds the shared Python plugin
  runtime and adoption instructions. `Scripts/plugin-runtime.py` syncs and
  checks copies; `.github/workflows/plugin-runtime.yml` verifies consumers
  against the runtime digest fixed by their workflow pin.
- `.github/workflows/plugin-release.yml` verifies and publishes reproducible
  plugin releases. The [consumer guide](Documentation/Reference/PluginRelease.md)
  describes its caller, inputs, outputs and recovery operations.

Product meaning and copy belong to the main repository's
[ProductIdentity](https://github.com/computer-mcp/computer-mcp/blob/master/Documentation/Architecture/ProductIdentity.md).
Text rendered into images (`Brand/config.json` `copy` and `members`) must match it.

## Updating the brand

Install Icon Composer from Xcode and set `APP_ICONS_SCRIPT` to the
`apple-app-icon-design` generator script (`skills/apple-app-icon-design/scripts/app_icons.py` in the
[showxu/skills](https://github.com/showxu/skills) repository). The manifest
records the script's SHA-256 next to the renderer versions. The generator finds
Icon Composer's `ictool` in the selected Xcode installation; set `IC_TOOL` to
select another export-capable renderer. Python 3 and `rsvg-convert` are also
required by the generator.

1. Edit `DESIGN.md` or `Brand/config.json`.
2. Render: `npm ci --prefix Brand`, `npx --prefix Brand playwright install --only-shell chromium`,
   then `node Brand/render.mjs`.
3. Preview each macOS rendition of the App icon with Icon Composer's `ictool
   Brand/Exports/app/AppIcon.icon --export-image --platform macOS --rendition <name>
   --output-file Brand/.cache/app-icon-preview.png --width 1024 --height 1024
   --scale 1 --design-generation <generation>`
   for Default, Dark, ClearLight, ClearDark, TintedLight and TintedDark, using
   the `design_generation` from the Iconography entry.
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

## Social previews and avatar

GitHub has no API for a repository's social preview or the organization
avatar. After a repository's brand pull request merges, upload its
`.github/brand/social.png` in the repository's settings under Social preview.
A public repository's preview is current when the image at its GraphQL
`openGraphImageUrl` has the same SHA-256 as that file. Upload
`profile/brand/avatar.png` as the organization avatar in the organization's
settings.
