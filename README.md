# Computer MCP organization

This repository owns the organization profile, the visual identity and the
conventions every Computer MCP repository shares. It holds rules, data and
documents; reusable workflows and their checks live in
[computer-mcp/github-workflows](https://github.com/computer-mcp/github-workflows).

- `profile/README.md` is the public organization entry point, generated from
  `profile/catalog.json`. The catalog lists each public repository with its
  outcome sentence, icon, kind, title and About sentence, grouped by the
  reader's job. `profile/assets/` holds the organization's mark and avatar.
- `MAINTENANCE.md` holds the cross-repository conventions and the declared
  GitHub settings. The community files (`CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `GOVERNANCE.md`, `SECURITY.md`, `SUPPORT.md`,
  `.github/ISSUE_TEMPLATE/` and the pull request template) apply to every
  repository without its own version.
- [VERSIONING.md](VERSIONING.md) holds shared version, tag, release-record,
  plugin compatibility and dependency rules.
- `DESIGN.md` is the design system: tokens, components, the icon family and
  composition rules, with the icon entries in its Iconography section.
- `.github/design/icons/<name>/` holds each icon's original layers, where it
  has any, and its `provenance.json`; `.github/design/fonts/` holds the bundled
  fonts with their licenses.
- `.github/assets/social-preview/social-preview.png` is this repository's own
  social preview.

Product meaning and copy belong to the main repository's
[ProductIdentity](https://github.com/computer-mcp/computer-mcp/blob/master/Documentation/Architecture/ProductIdentity.md).
Text in the catalog and in rendered images must match it, and each
repository's `about` equals its GitHub About.

## Updating icons

Icons come from two generators in the
[showxu/skills](https://github.com/showxu/skills) repository:
`skills/apple-app-icon-design/scripts/app_icons.py` renders the App icons
through Icon Composer from Xcode, and
`skills/apple-framework-icon-design/scripts/design_icons.py` renders the
component icons. Python 3 and `rsvg-convert` are also required.

1. Edit the entry in DESIGN.md's Iconography section, and the layers in
   `.github/design/icons/<name>/layers/` for an App icon.
2. Lint: `python3 <skills>/apple-framework-icon-design/scripts/design_icons.py DESIGN.md --lint`
   and `python3 <skills>/apple-app-icon-design/scripts/app_icons.py DESIGN.md --name <name> --lint`.
3. Render into an ignored directory: `design_icons.py DESIGN.md --out <dir> --png`,
   or `app_icons.py DESIGN.md --name <name> --style liquid-glass --out <dir>`,
   and review the App icon in every macOS rendition with Icon Composer.
4. Copy each consumed file into its repository through that repository's
   pull request and record it in the icon's `provenance.json`: the
   repository, path, generator output path and SHA-256, with the skill
   commit, command, renderer and verification date.

Member logos are `.github/assets/logo/logo-light.png` and `logo-dark.png`. A
component icon uses the generator's PNG for both; an App icon uses its macOS
Default and Dark renditions. The Homebrew tap and the website use the App
icon.

## Profile and social previews

The `github-readme-design` toolchain in the skills repository
(`skills/github-readme-design/scripts`) renders the profile and every social
preview from DESIGN, the catalog and the bundled fonts. Install it into an
ignored directory with `npm ci --ignore-scripts`, then:

```sh
node <toolchain>/src/cli.ts design lint --design DESIGN.md
node <toolchain>/src/cli.ts profile render --design DESIGN.md --catalog profile/catalog.json --out profile/README.md
node <toolchain>/src/cli.ts social-preview render --design DESIGN.md --fonts .github/design/fonts \
  --catalog profile/catalog.json --repository <name> --icon <logo-light.png> \
  --out <repository>/.github/assets/social-preview/social-preview.png
```

`profile check` and `social-preview check` compare the committed files
without overwriting them. A repository's social preview is committed in that
repository and rendered with `--repository .github` for this one.

## Social previews and avatar

GitHub has no API for a repository's social preview or the organization
avatar. After a repository's pull request merges, upload its
`.github/assets/social-preview/social-preview.png` in the repository's
settings under Social preview. A public repository's preview is current when
the image at its GraphQL `openGraphImageUrl` has the same SHA-256 as that
file. Upload `profile/assets/avatar.png` as the organization avatar in the
organization's settings.
