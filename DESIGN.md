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
  icon-body: "#17161F"
  icon-plane-back: "#2B2740"
  icon-plane-mid: "#FFB347"
  icon-plane-front: "#F4EFE3"
  icon-glyph: "#17161F"
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
  plane: 64px
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
  component-icon-body:
    backgroundColor: "{colors.icon-body}"
    size: 824px
  component-icon-plane-workspace:
    backgroundColor: "{colors.icon-plane-back}"
    rounded: "{rounded.plane}"
  component-icon-plane-capabilities:
    backgroundColor: "{colors.icon-plane-mid}"
    rounded: "{rounded.plane}"
  component-icon-plane-result:
    backgroundColor: "{colors.icon-plane-front}"
    textColor: "{colors.icon-glyph}"
    rounded: "{rounded.plane}"
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

- **Ink (#17161F):** text, the component icon body and code surfaces. Never pure black.
- **Slate (#5F5B70):** secondary text, captions and metadata.
- **Violet (#5A4BF5; #8B80FF on dark):** actions and navigation — primary buttons, links and the
  App icon's field. Labels on violet are white (#121019 on the dark-mode violet). Hover darkens the
  fill to **#4A3BE0**.
- **Amber (#FFB347; #FFC266 on dark):** the active path — the chat request, the active link and the
  screen it lights — plus the App icon's screen and the middle plane of component icons. Labels on
  amber are ink; amber is never used as text on light surfaces.
- **Ivory (#F4EFE3):** chips, the computer's case (**#DDD5C3** edge, **#E3DAC6** chin; **#E9E2D2**,
  **#BFB6A3** and **#CFC5B0** on dark), the front plane of component icons and text on code
  surfaces.
- **Violet ink (#2B2740):** the back plane of component icons.
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
layers with continuous corners; component icons use a 64px plane radius on the 824px grid at 1024
scale.

## Icon Family

- **Structure:** component icons are an ink body carrying a centred three-plane stack — violet-ink
  workspace, amber capabilities, ivory result — each plane 58px up and to the right of the one
  beneath it. Icons never carry the chat card or the link; those appear only in compositions around the icons. No isometric projection; avoid any resemblance to cube marks.
- **Glyph:** the front plane carries one ink glyph with a 9% stroke; the same glyph appears on the
  computer's screen in that member's compositions. Each component swaps only this glyph:
  computer-use pointer, apple-cli prompt, codex braces, swift-format aligned bars, claude speech
  bracket, cursor text caret, trae play wedge, homebrew-tap install tray.
- **App icon:** an original compact computer in ivory glass with an amber screen and a recessed
  chin, over a violet design grid; defined by the `computer-mcp` entry in
  [Iconography](#iconography) and delivered as an Icon Composer document plus a legacy
  `AppIcon.icns` for macOS 14 and 15.
- **Never:** vendor logos, the Apple or Swift logo, SF Symbols or SF Pro inside brand artwork. The
  swift-sdk fork keeps its upstream identity.

## Iconography

The App icon is a Liquid Glass icon generated from this entry with the `apple-app-icon-design`
generator. Its layers are original artwork in `Brand/app-icon/layers/`: a design grid, the
computer's recessed chin, its amber screen light and its ivory glass case. Accepted lint findings,
each by design: four groups keep the grid, chin, screen light and case in separate materials; the
grid lines run to the outline, so 0.7% of the grid falls outside the shape; the grid lines are
hairlines that fade below 32 px; the chin and the case sit over the white grid; and the case and the
chin share the ivory lightness, separated by depth rather than tone.

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
    }
  }
}
```

## Components

- **Primary button:** violet fill, white label in the interface sans, 12px radius.
- **Secondary button:** raised surface with a 1px line border.
- **Chat card:** raised surface, 20px radius, a title row naming the chat, and the request as an
  amber bubble with ink text.
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
- Do show both the chat and the computer whenever the link appears.
- Do draw the computer from the App icon's layers; never redraw or restyle it per surface.
- Do render every image text with the bundled OFL fonts, in both light and dark.
- Don't use gradients on cards or the computer, or rotate them.
- Don't draw clouds, globes or padlocks; the link carries the meaning.
- Don't put text inside the App icon.

## Responsive

Breakpoints are 900px, 600px and 370px. Below 900px the hero stacks copy above the illustration, the
link becomes vertical and the computer scales down with the column. Below 600px the display size
drops to 52px (Chinese 44px); side margins are 24px, and 16px below
370px. Touch targets stay at least 44px. Controls keep visible focus, meaningful selected states,
keyboard operation and reduced-motion support.

## Iteration Guide

Change tokens here first, then regenerate every asset with the organization renderer and deliver
them through each repository's brand lock. A new component swaps only its glyph — on the front plane
of its icon and on the computer's screen — and never introduces a new color. Check the App icon in
every macOS rendition, including Clear and Tinted, before delivery. The repository README lists the
render, check and delivery commands.
