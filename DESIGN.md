---
version: alpha
name: Computer MCP
description: Your computer as a compact machine whose screen lights amber when a chat works on it, on a violet field. Ivory, ink, violet and amber.
colors:
  primary: "#17161F"
  secondary: "#5F5B70"
  tertiary: "#5A4BF5"
  tertiary-dark: "#8B80FF"
  on-tertiary: "#FFFFFF"
  on-tertiary-dark: "#121019"
  tertiary-hover: "#4A3BE0"
  signal: "#FFB347"
  signal-dark: "#FFC266"
  on-signal: "#17161F"
  neutral: "#F4EFE3"
  surface: "#FBF8F1"
  surface-raised: "#FFFFFF"
  on-surface: "#17161F"
  on-surface-muted: "#5F5B70"
  line: "#E7E1D3"
  surface-dark: "#121019"
  surface-raised-dark: "#1C1A26"
  on-surface-dark: "#F4EFE3"
  on-surface-muted-dark: "#A9A4BA"
  line-dark: "#2C2938"
  accent-text: "#5A4BF5"
  accent-text-dark: "#8B80FF"
  computer-case: "#F4EFE3"
  computer-case-dark: "#E9E2D2"
  computer-edge: "#DDD5C3"
  computer-edge-dark: "#BFB6A3"
  computer-chin: "#E3DAC6"
  computer-chin-dark: "#CFC5B0"
  link-rail: "#E6E2FF"
  link-rail-dark: "#2A2547"
  success: "#1A7A43"
  success-dark: "#5FD08A"
  danger: "#B42318"
  danger-dark: "#FF8A8A"
  caution: "#FFCC00"
  focus: "#5A4BF5"
  focus-dark: "#8B80FF"
typography:
  headline-display:
    fontFamily: Inter
    fontSize: 80px
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Inter
    fontSize: 56px
    fontWeight: 600
    lineHeight: 1.07
    letterSpacing: -0.005em
  headline-md:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.125
    letterSpacing: 0.004em
  headline-sm:
    fontFamily: Inter
    fontSize: 22px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.004em
  headline-zh:
    fontFamily: Noto Sans SC
    fontSize: 64px
    fontWeight: 600
    lineHeight: 1.14
    letterSpacing: 0em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.011em
  body-md:
    fontFamily: Inter
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.53
    letterSpacing: -0.011em
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: -0.006em
  label-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: -0.01em
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.6
rounded:
  none: 0px
  sm: 6px
  md: 12px
  lg: 20px
  xl: 28px
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  section: 112px
  content-max: 1180px
  gutter: 24px
  link-width: 40px
components:
  page:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface}"
  page-caption:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.on-surface-muted}"
  page-metadata:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.secondary}"
  page-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-surface-dark}"
  page-dark-caption:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.on-surface-muted-dark}"
  accent-text:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.accent-text}"
    typography: "{typography.label-md}"
  accent-text-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.accent-text-dark}"
    typography: "{typography.label-md}"
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 14px
  button-primary-hover:
    backgroundColor: "{colors.tertiary-hover}"
    textColor: "{colors.on-tertiary}"
  button-primary-dark:
    backgroundColor: "{colors.tertiary-dark}"
    textColor: "{colors.on-tertiary-dark}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 14px
  button-secondary:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 14px
  button-secondary-dark:
    backgroundColor: "{colors.surface-raised-dark}"
    textColor: "{colors.on-surface-dark}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 14px
  chat-card:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 18px
  chat-card-dark:
    backgroundColor: "{colors.surface-raised-dark}"
    textColor: "{colors.on-surface-dark}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 18px
  chat-request:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.on-signal}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 10px
  chat-request-dark:
    backgroundColor: "{colors.signal-dark}"
    textColor: "{colors.on-signal}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 10px
  computer-case:
    backgroundColor: "{colors.computer-case}"
  computer-case-dark:
    backgroundColor: "{colors.computer-case-dark}"
  computer-edge:
    backgroundColor: "{colors.computer-edge}"
    width: 1.5px
  computer-edge-dark:
    backgroundColor: "{colors.computer-edge-dark}"
    width: 1.5px
  computer-chin:
    backgroundColor: "{colors.computer-chin}"
  computer-chin-dark:
    backgroundColor: "{colors.computer-chin-dark}"
  computer-screen:
    backgroundColor: "{colors.signal}"
    textColor: "{colors.on-signal}"
    typography: "{typography.code-md}"
  computer-screen-dark:
    backgroundColor: "{colors.signal-dark}"
    textColor: "{colors.on-signal}"
    typography: "{typography.code-md}"
  link-rail:
    backgroundColor: "{colors.link-rail}"
    width: "{spacing.link-width}"
  link-rail-dark:
    backgroundColor: "{colors.link-rail-dark}"
    width: "{spacing.link-width}"
  link-active:
    backgroundColor: "{colors.signal}"
    width: 6px
  packet:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: 6px
  packet-dark:
    backgroundColor: "{colors.surface-raised-dark}"
    textColor: "{colors.on-surface-dark}"
    typography: "{typography.label-md}"
    rounded: "{rounded.full}"
    padding: 6px
  status-success:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.success}"
    typography: "{typography.code-md}"
  status-success-dark:
    backgroundColor: "{colors.surface-raised-dark}"
    textColor: "{colors.success-dark}"
    typography: "{typography.code-md}"
  status-removed:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.danger}"
    typography: "{typography.code-md}"
  status-removed-dark:
    backgroundColor: "{colors.surface-raised-dark}"
    textColor: "{colors.danger-dark}"
    typography: "{typography.code-md}"
  badge-caution:
    backgroundColor: "{colors.caution}"
    textColor: "{colors.primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 4px
  chip:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.on-surface}"
    typography: "{typography.label-md}"
    rounded: "{rounded.sm}"
    padding: 6px
  code-block:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral}"
    typography: "{typography.code-md}"
    rounded: "{rounded.md}"
    padding: 16px
  divider:
    backgroundColor: "{colors.line}"
    height: 1px
  divider-dark:
    backgroundColor: "{colors.line-dark}"
    height: 1px
  focus-ring:
    backgroundColor: "{colors.focus}"
    width: 2px
  focus-ring-dark:
    backgroundColor: "{colors.focus-dark}"
    width: 2px
---

# Computer MCP

## Overview

Computer MCP lets the chat people already use reach their own computers. ChatGPT can read and write
code and run commands there, use local CLI tools, MCP servers, Skills and Computer Use, and hand
work to Codex, Claude Code or Cursor when that helps. Each computer decides what it allows.

The visual system draws that model directly. The computer is the **compact machine** of the App icon
— an ivory case, a recessed chin and a screen. The chat is a separate card, and one **secure link**
runs from its request into the computer; calls travel along the link as small packets. Everything
that belongs to the active path — the request, the link and the screen it lights — is amber. Each
member repository shows the same computer with its own glyph on the screen. Violet is the field the
computer stands on and the color of actions: buttons and links.

The look is warm, tactile and exact: ivory and ink with one violet field and one amber light,
crisp offset shadows, plain system type. It
should feel like a well-made tool that runs on your own machine, not a cloud service. Audience:
developers and people who want ChatGPT to code and operate their computer for them. Tone: direct,
concrete, unhurried. Density: generous on marketing surfaces, compact in reference material.

This file owns visual tokens and rules for every public surface: the App icon, component icons,
README headers, social cards, the organization profile and the website. Product meaning, the
tagline and voice belong to the App's Product Identity document. The App's own interface follows
the system appearance and Apple's Human Interface Guidelines; the brand appears only in its icon and
About window.

## Colors

- **Ink (#17161F):** text, the glyph on the computer's screen and code surfaces. Never pure black.
- **Slate (#5F5B70):** secondary text, captions and metadata.
- **Violet (#5A4BF5; #8B80FF on dark):** actions and navigation — primary buttons, links and the
  App icon's field. Labels on violet are white (#121019 on the dark-mode violet). Hover darkens the
  fill to **#4A3BE0**.
- **Amber (#FFB347; #FFC266 on dark):** the active path — the chat request, the active link and the
  screen it lights — plus the App icon's screen. Labels on amber are ink; amber is never used as
  text on light surfaces.
- **Ivory (#F4EFE3):** chips, the computer's case (**#DDD5C3** edge, **#E3DAC6** chin; **#E9E2D2**,
  **#BFB6A3** and **#CFC5B0** on dark) and text on code surfaces.
- **Product colors:** each component icon takes the main color of the product it serves, as listed
  in the [Icon Family](#icon-family); these colors appear only in those icons.
- **Link rail (#E6E2FF; #2A2547 on dark):** the band under the active link.
- **Surfaces:** page **#FBF8F1** and raised **#FFFFFF** in light mode; **#121019** and **#1C1A26**
  in dark mode, with lines **#E7E1D3** and **#2C2938**.
- **Status:** success **#1A7A43** (**#5FD08A** on dark), removals **#B42318** (**#FF8A8A** on dark),
  caution **#FFCC00** with ink text for actions that need confirmation — a badge only, distinct
  from the amber of the active path.
- **Focus (#5A4BF5; #8B80FF on dark):** keyboard focus rings only; never decorative.

Every surface exists in light and dark and follows the viewer's system appearance. Text pairs meet
WCAG AA in both modes.

## Typography

Interface text uses the platform's system typeface, the way Apple's own pages do: **SF Pro** for
Latin text, **PingFang SC** for Chinese and **SF Mono** for code on Apple devices, through the
system font stack on the web. Headlines are semibold with slightly tight tracking; labels, buttons
and navigation are set in the same sans in sentence case. Monospace is reserved for real code: tool
names, paths, commands and output.

Apple's font license does not cover brand artwork, so text rendered into images — headers, social
cards and icons — uses bundled open fonts that match the system faces: **Inter** (OFL) for Latin,
**Noto Sans SC** (OFL) for Chinese and **JetBrains Mono** (OFL) for code. The tokens above carry
these artwork faces; web text maps them to the system stack.

## Layout

A 12-column grid capped at 1180px with 24px gutters; marketing sections are separated by 112px and
spacing follows a 4px unit. Reference pages use a single 720px reading column.

- **Hero:** copy on the left; on the right, the chat card sits high and the computer sits low, with
  the link leaving the request, bending once and entering the top of the computer. Packets sit on
  the vertical run of the link.
- **README header (1280 × 320, light and dark):** icon and name on the left, one supporting line;
  on the right the request bubble, the link turning down into the top of the computer, and the
  member's glyph on its amber screen (the App's screen is plain amber).
- **Social card (1280 × 640):** icon and name at the top left with the headline below. The App card
  adds capability chips at the bottom and, on the right, the chat card, the link with its packets
  and the computer whose screen shows the command and its passing result. A member card carries its family eyebrow and its repository address, and links a typing bubble into the
  computer showing its glyph.
- **Website:** compact sticky navigation with the App icon, product name, core links, language
  switch and download action; the hero; capability examples for files and commands, CLI, MCP,
  Skills, Computer Use and coding-agent hand-off; how hosts connect and how permissions work on each
  computer; a dated, sourced comparison with related products; three setup steps with a first safe
  tool call; FAQ, closing line and organization footer. The homepage is Chinese by default with a
  complete English version.

## Elevation & Depth

Depth comes from **crisp shadows and layering**, not blur. Cards cast a short shadow (`0 1px 0
rgba(0,0,0,.05), 0 22px 40px -14px rgba(10,16,30,.30)`) and the computer casts a drop shadow
following its outline (`0 18px 26px rgba(10,16,30,.22)`; `0 22px 30px rgba(0,0,0,.55)` on dark); its
chin sits one layer behind its case. The link runs on the page plane, beneath cards and the
computer. In dark mode, shadows deepen (`0 24px 48px -16px rgba(0,0,0,.6)`) and raised surfaces add
a 1px line border.

## Shapes

Cards use a 20px radius; buttons 12px; chips 6px; packets are fully rounded. The link is a
straight band with round caps that bends at most once. The computer is drawn from the App icon's own
layers with continuous corners; component icons take the framework generator's slab geometry.

## Icon Family

- **Component icons:** plugins and the Homebrew tap are framework slabs, generated from the `icons`
  entries in [Iconography](#iconography) with the `apple-framework-icon-design` generator. Each slab
  takes the main color of the product it serves, and its three bands deepen from it: Claude's
  terracotta, Codex's blue, Cursor's graphite, Computer Use's sky-to-pink, Swift's orange,
  Homebrew's amber, and TRAE's black with green. The face carries the App's design grid and one
  glyph that follows the product's own mark: the Claude spark, the Codex cloud with a prompt, the
  Cursor cube, the Computer Use pointer, the Swift bird, the Homebrew mug and the TRAE pixel face.
- **App icons:** executables have Liquid Glass app icons on the App's violet field and design grid,
  generated from the `app_icons` entries with the `apple-app-icon-design` generator. The App is an
  original compact computer in ivory glass with an amber screen and a recessed chin, delivered as
  an Icon Composer document plus a legacy `AppIcon.icns` for macOS 14 and 15. Apple CLI is four
  glass tiles in the colors of Notes, Calendar and Mail, the fourth a dark terminal with a prompt.
- **Screen glyph:** in a member's compositions the computer's screen shows its icon's glyph flat in
  ink, with inlaid details in the screen's amber: a framework glyph's surface parts, and Apple
  CLI's prompt. The Homebrew tap's screen shows the icons of the App and Apple CLI it installs.
  Icons never carry the chat card or the link.
- **Never:** SF Symbols or SF Pro inside brand artwork. The swift-sdk fork keeps its upstream
  identity.

## Iconography

App icons are Liquid Glass icons generated from the `app_icons` entries with the
`apple-app-icon-design` generator. Their layers are original artwork in `Brand/app-icon/layers/`,
and both share its design grid. The App's layers are the computer's recessed chin, its amber screen
light and its ivory glass case; Apple CLI's are its three app tiles, its terminal tile and its
prompt. Accepted lint findings, each by design: four groups keep the grid and three materials
apart in each icon (the App's chin, screen light and case; Apple CLI's app tiles, terminal glass
and prompt); the grid lines run to the outline, so 0.7% of the grid falls outside the shape; the
grid lines are hairlines that fade below 32 px; the App's chin and case sit over the white grid; and
the App's case and chin share the ivory lightness, separated by depth rather than tone.

Component icons are generated from the `icons` entries with the `apple-framework-icon-design`
generator; their palette lint is clean. Glyphs are layered: each part has its own color, and parts
marked `surface` lie only on the glyph's top. The face texture is the App's design grid redrawn in
face units.

```json
{
  "app_icons": {
    "computer-mcp": {
      "background": "#5A4BF5",
      "gradient": true,
      "groups": [
        {
          "name": "Grid",
          "layers": [
            {
              "source": "Brand/app-icon/layers/grid.svg",
              "name": "grid",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.2
            }
          ],
          "shadow": {
            "kind": "none",
            "opacity": 0
          },
          "specular": false
        },
        {
          "name": "Base",
          "layers": [
            {
              "source": "Brand/app-icon/layers/crt-base.svg",
              "name": "crt-base",
              "fill": {
                "automatic-gradient": "#D8CDB0A6"
              }
            }
          ],
          "shadow": {
            "kind": "neutral",
            "opacity": 0.4
          },
          "translucency": {
            "enabled": true,
            "value": 0.35
          },
          "blur-material": 0.5,
          "refractivity": {
            "enabled": true,
            "strength": 0.6,
            "depth": 0
          }
        },
        {
          "name": "Light",
          "layers": [
            {
              "source": "Brand/app-icon/layers/crt-light.svg",
              "name": "crt-light",
              "fill": {
                "automatic-gradient": "#FFB347"
              }
            }
          ],
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.1
          }
        },
        {
          "name": "Computer",
          "layers": [
            {
              "source": "Brand/app-icon/layers/crt-body.svg",
              "name": "crt-body",
              "fill": {
                "automatic-gradient": "#F6EEDBA6"
              }
            }
          ],
          "shadow": {
            "kind": "neutral",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.35
          },
          "blur-material": 0.5,
          "refractivity": {
            "enabled": true,
            "strength": 0.6,
            "depth": 0
          }
        }
      ],
      "styles": {
        "liquid-glass": {
          "design_generation": 27
        }
      }
    },
    "apple-cli": {
      "background": "#5A4BF5",
      "gradient": true,
      "groups": [
        {
          "name": "Grid",
          "layers": [
            {
              "source": "Brand/app-icon/layers/grid.svg",
              "name": "grid",
              "fill": {
                "solid": "#FFFFFF"
              },
              "opacity": 0.2
            }
          ],
          "shadow": {
            "kind": "none",
            "opacity": 0
          },
          "specular": false
        },
        {
          "name": "Apps",
          "layers": [
            {
              "source": "Brand/app-icon/layers/apple-cli-notes.svg",
              "name": "apple-cli-notes",
              "fill": {
                "automatic-gradient": "#FFD60A"
              }
            },
            {
              "source": "Brand/app-icon/layers/apple-cli-calendar.svg",
              "name": "apple-cli-calendar",
              "fill": {
                "automatic-gradient": "#FF453A"
              }
            },
            {
              "source": "Brand/app-icon/layers/apple-cli-mail.svg",
              "name": "apple-cli-mail",
              "fill": {
                "automatic-gradient": "#0A84FF"
              }
            }
          ],
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.1
          }
        },
        {
          "name": "Terminal",
          "layers": [
            {
              "source": "Brand/app-icon/layers/apple-cli-terminal.svg",
              "name": "apple-cli-terminal",
              "fill": {
                "automatic-gradient": "#1D1B26D9"
              }
            }
          ],
          "shadow": {
            "kind": "neutral",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.35
          },
          "blur-material": 0.5,
          "refractivity": {
            "enabled": true,
            "strength": 0.6,
            "depth": 0
          }
        },
        {
          "name": "Prompt",
          "layers": [
            {
              "source": "Brand/app-icon/layers/apple-cli-prompt.svg",
              "name": "apple-cli-prompt",
              "fill": {
                "automatic-gradient": "#F6EEDB"
              }
            }
          ],
          "shadow": {
            "kind": "layer-color",
            "opacity": 0.5
          },
          "translucency": {
            "enabled": true,
            "value": 0.1
          }
        }
      ],
      "styles": {
        "liquid-glass": {
          "design_generation": 27
        }
      }
    }
  },
  "icons": {
    "plugin-claude": {
      "hue": 40,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.16,
      "custom_glyph": {
        "layers": [
          {
            "d": "M0.023 -0.039 L0.121 -0.886 A0.09 0.09 0 0 0 -0.059 -0.893 L-0.021 -0.041 Z M0.039 -0.023 L0.407 -0.531 A0.075 0.075 0 0 0 0.278 -0.609 L0.002 -0.046 Z M0.046 -0.0 L0.78 -0.335 A0.085 0.085 0 0 0 0.698 -0.484 L0.024 -0.039 Z M0.038 0.025 L0.714 0.158 A0.095 0.095 0 0 0 0.731 -0.031 L0.042 -0.018 Z M0.022 0.04 L0.728 0.568 A0.08 0.08 0 0 0 0.815 0.434 L0.046 0.003 Z M-0.005 0.045 L0.19 0.626 A0.07 0.07 0 0 0 0.318 0.571 L0.036 0.028 Z M-0.026 0.037 L-0.179 0.846 A0.09 0.09 0 0 0 -0.0 0.865 L0.018 0.042 Z M-0.04 0.022 L-0.459 0.56 A0.08 0.08 0 0 0 -0.325 0.647 L-0.003 0.046 Z M-0.046 -0.003 L-0.851 0.292 A0.095 0.095 0 0 0 -0.771 0.464 L-0.027 0.037 Z M-0.038 -0.025 L-0.676 -0.134 A0.075 0.075 0 0 0 -0.689 0.015 L-0.042 0.018 Z M-0.021 -0.041 L-0.645 -0.537 A0.085 0.085 0 0 0 -0.74 -0.396 L-0.045 -0.004 Z M0.002 -0.046 L-0.261 -0.718 A0.08 0.08 0 0 0 -0.405 -0.648 L-0.037 -0.026 Z",
            "fill": "oklch(0.97 0.012 70)",
            "round": 0.02
          },
          {
            "circle": [
              0,
              0,
              0.09
            ],
            "fill": "oklch(0.97 0.012 70)"
          }
        ]
      },
      "glyph_scale": 0.36,
      "face_colors": [
        "oklch(0.72 0.13 42)",
        "oklch(0.64 0.145 40)"
      ],
      "band_colors": [
        "oklch(0.58 0.145 39)",
        "oklch(0.51 0.135 37)",
        "oklch(0.44 0.12 35)"
      ],
      "glyph_side": "oklch(0.86 0.04 50)"
    },
    "plugin-codex": {
      "hue": 272,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.16,
      "custom_glyph": {
        "layers": [
          {
            "circle": [
              0,
              0,
              0.62
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              0.48,
              0.191,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              0.199,
              0.462,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              -0.199,
              0.462,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              -0.48,
              0.191,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              -0.48,
              -0.191,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              -0.199,
              -0.462,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              0.199,
              -0.462,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "circle": [
              0.48,
              -0.191,
              0.36
            ],
            "fill": {
              "colors": [
                "#FFFFFF",
                "oklch(0.9 0.045 280)"
              ],
              "from": [
                0,
                -0.9
              ],
              "to": [
                0,
                0.9
              ]
            }
          },
          {
            "d": "M-0.34 -0.22 L-0.12 0 L-0.34 0.22",
            "stroke": "oklch(0.5 0.25 268)",
            "width": 0.13,
            "surface": true
          },
          {
            "d": "M0.04 0.24 H0.34",
            "stroke": "oklch(0.5 0.25 268)",
            "width": 0.13,
            "surface": true
          }
        ]
      },
      "glyph_scale": 0.34,
      "face_colors": [
        "oklch(0.68 0.16 285)",
        "oklch(0.52 0.24 270)"
      ],
      "band_colors": [
        "oklch(0.46 0.24 270)",
        "oklch(0.4 0.22 270)",
        "oklch(0.34 0.19 271)"
      ],
      "glyph_side": "oklch(0.8 0.07 275)"
    },
    "plugin-cursor": {
      "hue": 85,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.12,
      "face": "graphite",
      "custom_glyph": {
        "layers": [
          {
            "d": "M0 -0.92 L0.8 -0.46 L0.8 0.46 L0 0.92 L-0.8 0.46 L-0.8 -0.46 Z",
            "fill": "oklch(0.44 0.006 85)",
            "round": 0.03
          },
          {
            "d": "M0 -0.92 L0 -0.46 L-0.8 -0.46 Z",
            "fill": "oklch(0.51 0.006 85)",
            "round": 0.03
          },
          {
            "d": "M-0.8 -0.46 L0 0 L-0.8 0.46 Z",
            "fill": "oklch(0.51 0.006 85)",
            "round": 0.03
          },
          {
            "d": "M-0.8 0.46 L0 0 L0 0.92 Z",
            "fill": "oklch(0.63 0.006 85)",
            "round": 0.03
          },
          {
            "d": "M0.44 0.161 L0.8 0.46 L0 0.92 Z",
            "fill": "oklch(0.63 0.006 85)",
            "round": 0.03
          },
          {
            "d": "M-0.8 -0.46 L0.8 -0.46 L0 0 Z",
            "fill": "oklch(0.97 0.004 85)",
            "round": 0.03,
            "surface": true
          },
          {
            "d": "M0.8 -0.46 L0 0.92 L0 0 Z",
            "fill": "oklch(0.88 0.004 85)",
            "round": 0.03,
            "surface": true
          }
        ]
      },
      "glyph_scale": 0.38,
      "face_colors": [
        "oklch(0.3 0.008 85)",
        "oklch(0.2 0.008 85)"
      ],
      "band_colors": [
        "oklch(0.27 0.008 85)",
        "oklch(0.33 0.008 85)",
        "oklch(0.4 0.008 85)"
      ],
      "glyph_side": "oklch(0.3 0.006 85)",
      "texture_color": "oklch(0.75 0.01 85)"
    },
    "plugin-computer-use": {
      "hue": 250,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.16,
      "custom_glyph": {
        "layers": [
          {
            "d": "M-0.62 -0.66 L0.80 -0.10 L0.10 0.12 L-0.12 0.82 Z",
            "fill": "#FFFFFF",
            "round": 0.3
          },
          {
            "d": "M-0.62 -0.66 L0.80 -0.10 L0.10 0.12 L-0.12 0.82 Z",
            "fill": {
              "colors": [
                "oklch(0.8 0.14 225)",
                "oklch(0.57 0.21 266)"
              ],
              "from": [
                -0.6,
                -0.6
              ],
              "to": [
                0.4,
                0.6
              ]
            },
            "round": 0.14,
            "surface": true
          }
        ]
      },
      "face_colors": [
        "oklch(0.79 0.135 236)",
        "oklch(0.78 0.13 330)"
      ],
      "band_colors": [
        "oklch(0.72 0.14 265)",
        "oklch(0.62 0.17 268)",
        "oklch(0.53 0.19 272)"
      ],
      "glyph_side": "oklch(0.62 0.15 262)"
    },
    "plugin-swift-format": {
      "hue": 40,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.16,
      "custom_glyph": {
        "layers": [
          {
            "d": "M0.18 -0.86 C0.66 -0.52 0.84 -0.02 0.64 0.40 C0.74 0.50 0.80 0.62 0.80 0.80 C0.70 0.66 0.58 0.62 0.46 0.64 C0.06 0.86 -0.48 0.74 -0.86 0.30 C-0.44 0.56 -0.02 0.52 0.22 0.30 C-0.12 0.08 -0.50 -0.28 -0.80 -0.62 C-0.42 -0.36 -0.10 -0.14 0.12 0.00 C-0.10 -0.26 -0.34 -0.56 -0.48 -0.82 C-0.12 -0.50 0.20 -0.24 0.40 -0.06 C0.50 -0.34 0.40 -0.62 0.18 -0.86 Z",
            "fill": "#FFFFFF",
            "round": 0.03
          }
        ]
      },
      "face_colors": [
        "oklch(0.78 0.16 62)",
        "oklch(0.66 0.21 36)"
      ],
      "band_colors": [
        "oklch(0.6 0.21 33)",
        "oklch(0.53 0.2 30)",
        "oklch(0.46 0.18 28)"
      ],
      "glyph_side": "oklch(0.86 0.06 45)"
    },
    "homebrew-tap": {
      "hue": 70,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.16,
      "custom_glyph": {
        "layers": [
          {
            "d": "M0.36 -0.10 H0.60 A0.18 0.18 0 0 1 0.78 0.08 V0.30 A0.18 0.18 0 0 1 0.60 0.48 H0.36",
            "stroke": "#FFFFFF",
            "width": 0.15
          },
          {
            "d": "M-0.64 -0.30 H0.36 V0.62 A0.18 0.18 0 0 1 0.18 0.80 H-0.46 A0.18 0.18 0 0 1 -0.64 0.62 Z",
            "fill": "#FFFFFF",
            "round": 0.03
          },
          {
            "circle": [
              -0.44,
              -0.4,
              0.21
            ],
            "fill": "#FFFFFF"
          },
          {
            "circle": [
              -0.12,
              -0.5,
              0.25
            ],
            "fill": "#FFFFFF"
          },
          {
            "circle": [
              0.18,
              -0.4,
              0.2
            ],
            "fill": "#FFFFFF"
          },
          {
            "d": "M-0.52 -0.14 H0.24 V0.58 A0.10 0.10 0 0 1 0.14 0.68 H-0.42 A0.10 0.10 0 0 1 -0.52 0.58 Z",
            "fill": {
              "colors": [
                "oklch(0.84 0.15 82)",
                "oklch(0.72 0.16 62)"
              ],
              "from": [
                0,
                -0.14
              ],
              "to": [
                0,
                0.68
              ]
            },
            "surface": true
          },
          {
            "circle": [
              -0.26,
              0.34,
              0.05
            ],
            "fill": "#FFFFFF",
            "surface": true
          },
          {
            "circle": [
              0.02,
              0.12,
              0.04
            ],
            "fill": "#FFFFFF",
            "surface": true
          },
          {
            "circle": [
              -0.08,
              0.48,
              0.035
            ],
            "fill": "#FFFFFF",
            "surface": true
          }
        ]
      },
      "glyph_scale": 0.34,
      "face_colors": [
        "oklch(0.86 0.15 88)",
        "oklch(0.76 0.16 72)"
      ],
      "band_colors": [
        "oklch(0.68 0.15 64)",
        "oklch(0.59 0.13 57)",
        "oklch(0.5 0.11 52)"
      ],
      "glyph_side": "oklch(0.88 0.05 75)"
    },
    "plugin-trae": {
      "hue": 155,
      "bands": 3,
      "glyph_rotation": -45,
      "texture": {
        "d": "M0 -0.6 V0.6 M-0.6 0 H0.6 M-0.25 -0.25 V0.25 M-0.25 -0.25 H0.25 M0.25 -0.25 V0.25 M-0.25 0.25 H0.25 M0.25 0.25 V0.452 Q0.25 0.47 0.268 0.47 H0.31 Q0.47 0.47 0.47 0.31 V0.25 Z M0.25 -0.25 V-0.452 Q0.25 -0.47 0.268 -0.47 H0.31 Q0.47 -0.47 0.47 -0.31 V-0.25 Z M-0.25 0.25 V0.452 Q-0.25 0.47 -0.268 0.47 H-0.31 Q-0.47 0.47 -0.47 0.31 V0.25 Z M-0.25 -0.25 V-0.452 Q-0.25 -0.47 -0.268 -0.47 H-0.31 Q-0.47 -0.47 -0.47 -0.31 V-0.25 Z",
        "width": 0.009
      },
      "texture_opacity": 0.12,
      "face": "graphite",
      "custom_glyph": {
        "layers": [
          {
            "d": "M-0.875 -0.625 h0.25 v0.25 h-0.25 Z M-0.625 -0.625 h0.25 v0.25 h-0.25 Z M-0.375 -0.625 h0.25 v0.25 h-0.25 Z M-0.125 -0.625 h0.25 v0.25 h-0.25 Z M0.125 -0.625 h0.25 v0.25 h-0.25 Z M0.375 -0.625 h0.25 v0.25 h-0.25 Z M0.625 -0.625 h0.25 v0.25 h-0.25 Z M0.625 -0.375 h0.25 v0.25 h-0.25 Z M0.625 -0.125 h0.25 v0.25 h-0.25 Z M0.625 0.125 h0.25 v0.25 h-0.25 Z M0.625 0.375 h0.25 v0.25 h-0.25 Z M-0.875 -0.375 h0.25 v0.25 h-0.25 Z M-0.875 -0.125 h0.25 v0.25 h-0.25 Z M-0.875 0.125 h0.25 v0.25 h-0.25 Z M-0.625 0.375 h0.25 v0.25 h-0.25 Z M-0.375 0.375 h0.25 v0.25 h-0.25 Z M-0.125 0.375 h0.25 v0.25 h-0.25 Z M0.125 0.375 h0.25 v0.25 h-0.25 Z M0.375 0.375 h0.25 v0.25 h-0.25 Z",
            "fill": "oklch(0.85 0.2 155)"
          },
          {
            "d": "M-0.162 -0.17 L0.008 0.0 L-0.162 0.17 L-0.333 0.0 Z M0.35 -0.17 L0.52 0.0 L0.35 0.17 L0.18 0.0 Z",
            "fill": "oklch(0.85 0.2 155)"
          }
        ]
      },
      "face_colors": [
        "oklch(0.3 0.006 260)",
        "oklch(0.21 0.006 260)"
      ],
      "band_colors": [
        "oklch(0.27 0.03 158)",
        "oklch(0.33 0.05 158)",
        "oklch(0.4 0.07 158)"
      ],
      "glyph_side": "oklch(0.55 0.14 158)",
      "texture_color": "oklch(0.8 0.08 158)"
    }
  }
}
```

## Components

- **Primary button:** violet fill, white label in the interface sans, 12px radius.
- **Secondary button:** raised surface with a 1px line border.
- **Chat card:** raised surface, 20px radius, a title row naming the chat, and the request as an
  amber bubble with ink text. Each member's request is one it serves, from `Brand/config.json`.
- **Command card:** the code block carrying real commands behind amber prompts, with a 1px line
  border in dark mode; it takes the chat card's place for the Homebrew tap, which people reach
  from a terminal.
- **Computer:** the App icon's machine drawn flat — ivory case with a hairline edge, recessed chin,
  amber screen carrying the member glyph or, for the App, the command and its result. Capability
  chips beside the composition name Files, Shell, CLI, MCP, Skills and Computer Use.
- **Link and packets:** a link-rail band with a 6px amber line; packets are raised pills naming
  the tool, such as `file.write`.
- **Status:** green for success, red for removals, caution badge for actions awaiting confirmation.
- **Chip and code block:** ivory chip with a sans label; ink code block with ivory text and an
  amber prompt.

## Do's and Don'ts

- Do keep amber for the active path and violet for actions and links; never set amber text on a
  light surface.
- Do show both the request — a chat, or a command card — and the computer whenever the link
  appears.
- Do draw the computer from the App icon's layers; never redraw or restyle it per surface.
- Do render every image text with the bundled OFL fonts, in both light and dark.
- Don't use gradients on cards or the computer, or rotate them.
- Don't draw clouds, globes or padlocks for the connection; the link carries it.
- Don't put text inside the App icon.

## Responsive

Breakpoints are 900px, 600px and 370px. Below 900px the hero stacks copy above the illustration, the
link becomes vertical and the computer scales down with the column. Below 600px the display size
drops to 52px (Chinese 44px); side margins are 24px, and 16px below
370px. Touch targets stay at least 44px. Controls keep visible focus, meaningful selected states,
keyboard operation and reduced-motion support.

## Iteration Guide

Change tokens here first, then regenerate every asset with the organization renderer and deliver
them through each repository's brand lock. A new component gets its own Iconography entry — a slab in the
colors of the product it serves, with a glyph that follows that product's mark — and the same glyph
on the computer's screen. Check the App icon in
every macOS rendition, including Clear and Tinted, before delivery. The repository README lists the
render, check and delivery commands.
