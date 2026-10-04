---
version: alpha
name: Computer MCP
description: Your computer as a stack of capability planes, reached from the chat through one secure link. Paper, ink and vermilion.
colors:
  primary: "#16181D"
  secondary: "#5B6270"
  tertiary: "#FF5A36"
  neutral: "#F4F1EA"
  surface: "#FBFAF6"
  surface-raised: "#FFFFFF"
  on-surface: "#16181D"
  on-surface-muted: "#5B6270"
  line: "#E2DDD2"
  surface-dark: "#121418"
  surface-raised-dark: "#1C1F25"
  on-surface-dark: "#F4F1EA"
  on-surface-muted-dark: "#A3A9B5"
  line-dark: "#2C3038"
  on-accent: "#16181D"
  accent-hover: "#E84A27"
  accent-text: "#C2410C"
  accent-text-dark: "#FF7352"
  plane-back: "#3A3F48"
  on-plane-back: "#B8BEC9"
  link-rail: "#F2D6CC"
  link-rail-dark: "#3B2621"
  success: "#1A7A43"
  success-dark: "#5FD08A"
  danger: "#B42318"
  danger-dark: "#FF8A8A"
  caution: "#FFB224"
  focus: "#3D6BFF"
  icon-body: "#16181D"
  icon-plane-back: "#3A3F48"
  icon-plane-mid: "#FF5A36"
  icon-plane-front: "#F4F1EA"
  icon-glyph: "#16181D"
typography:
  headline-display:
    fontFamily: Bricolage Grotesque
    fontSize: 88px
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: -0.035em
    fontVariation: "'opsz' 96, 'wdth' 88"
  headline-lg:
    fontFamily: Bricolage Grotesque
    fontSize: 56px
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: -0.03em
    fontVariation: "'opsz' 72, 'wdth' 90"
  headline-md:
    fontFamily: Bricolage Grotesque
    fontSize: 32px
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: -0.02em
  headline-sm:
    fontFamily: Bricolage Grotesque
    fontSize: 22px
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: -0.01em
  headline-zh:
    fontFamily: Noto Sans SC
    fontSize: 68px
    fontWeight: 800
    lineHeight: 1.12
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Bricolage Grotesque
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.6
    fontVariation: "'opsz' 18"
  body-md:
    fontFamily: Bricolage Grotesque
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
    fontVariation: "'opsz' 14"
  body-sm:
    fontFamily: Bricolage Grotesque
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.55
    fontVariation: "'opsz' 12"
  label-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.02em
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.06em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 450
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
  plane-offset: 48px
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
    textColor: "{colors.on-accent}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.md}"
    padding: 14px
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.on-accent}"
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
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-accent}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 10px
  plane-workspace:
    backgroundColor: "{colors.plane-back}"
    textColor: "{colors.on-plane-back}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
    padding: 20px
  plane-capabilities:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-accent}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
    padding: 20px
  plane-result:
    backgroundColor: "{colors.surface-raised}"
    textColor: "{colors.on-surface}"
    typography: "{typography.code-md}"
    rounded: "{rounded.lg}"
    padding: 20px
  plane-result-dark:
    backgroundColor: "{colors.surface-raised-dark}"
    textColor: "{colors.on-surface-dark}"
    typography: "{typography.code-md}"
    rounded: "{rounded.lg}"
    padding: 20px
  link-rail:
    backgroundColor: "{colors.link-rail}"
    width: "{spacing.link-width}"
  link-rail-dark:
    backgroundColor: "{colors.link-rail-dark}"
    width: "{spacing.link-width}"
  link-active:
    backgroundColor: "{colors.tertiary}"
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
  app-icon-body:
    backgroundColor: "{colors.icon-body}"
    size: 824px
  app-icon-plane-workspace:
    backgroundColor: "{colors.icon-plane-back}"
    rounded: "{rounded.plane}"
  app-icon-plane-capabilities:
    backgroundColor: "{colors.icon-plane-mid}"
    rounded: "{rounded.plane}"
  app-icon-plane-result:
    backgroundColor: "{colors.icon-plane-front}"
    textColor: "{colors.icon-glyph}"
    rounded: "{rounded.plane}"
---

# Computer MCP

## Overview

Computer MCP lets the chat people already use reach their own computers. ChatGPT can read and write
code and run commands there, use local CLI tools, MCP servers, Skills and Computer Use, and hand work
to Codex, Claude Code or Cursor when that helps. Each computer decides what it allows.

The visual system draws that model directly. The computer is a **stack of planes** — the authorized
workspace at the back, the capabilities in the middle, the result in front. The chat is a separate
card, and one **secure link** runs from it into the stack; calls travel along the link as small
packets. Everything that belongs to the active path — the request, the link and the capability
plane it reaches — is vermilion.

The look is warm, tactile and exact: paper and ink, crisp offset shadows, monospace labels. It
should feel like a well-made tool that runs on your own machine, not a cloud service. Audience:
developers and people who want ChatGPT to code and operate their computer for them. Tone: direct,
concrete, unhurried. Density: generous on marketing surfaces, compact in reference material.

This file owns visual tokens and rules for every public surface: the App icon, component icons,
README headers, social cards, the organization profile and the website. Product meaning, the
tagline and voice belong to the App's Product Identity document. The App's own interface follows
the system appearance and Apple's Human Interface Guidelines; the brand appears only in its icon and
About window.

## Colors

- **Ink (#16181D):** text, the App icon body and code surfaces. Never pure black.
- **Slate (#5B6270):** secondary text, captions and metadata.
- **Vermilion (#FF5A36):** the active path and the primary action. Labels on vermilion are ink;
  vermilion text on light surfaces uses **#C2410C**, and on dark surfaces **#FF7352**. Hover
  darkens the fill to **#E84A27**.
- **Paper (#F4F1EA):** chips and the front plane of the App icon.
- **Graphite (#3A3F48):** the workspace plane, with **#B8BEC9** labels.
- **Link rail (#F2D6CC; #3B2621 on dark):** the band under the active link.
- **Surfaces:** page **#FBFAF6** and raised **#FFFFFF** in light mode; **#121418** and **#1C1F25**
  in dark mode, with lines **#E2DDD2** and **#2C3038**.
- **Status:** success **#1A7A43** (**#5FD08A** on dark), removals **#B42318** (**#FF8A8A** on dark),
  caution **#FFB224** with ink text for actions that need confirmation.
- **Focus (#3D6BFF):** keyboard focus rings only; never decorative.

Every surface exists in light and dark and follows the viewer's system appearance. Text pairs meet
WCAG AA in both modes.

## Typography

**Bricolage Grotesque** (OFL) carries display and body text; its optical-size axis tightens
headlines (opsz 96, width 88) and opens body text (opsz 14). **JetBrains Mono** (OFL) carries labels,
packets, commands and code. Chinese text uses **Noto Sans SC** (OFL), heavy for headlines.

Text rendered into images — headers, social cards and icons — uses only these bundled fonts, so every
platform shows the same result. Live web text may fall back to system fonts only after the bundled
web fonts.

## Layout

A 12-column grid capped at 1180px with 24px gutters; marketing sections are separated by 112px and
spacing follows a 4px unit. Reference pages use a single 720px reading column.

- **Hero:** copy on the left; on the right, the chat card sits high and the stack sits low, with the
  link leaving the chat card, bending once and entering the top of the stack. Packets sit on the
  vertical run of the link.
- **README header (1280 × 320, light and dark):** icon and name on the left, one supporting line,
  and a small stack-and-link motif breaking the right edge.
- **Social card (1280 × 640):** icon and name at the top left, the headline below, capability chips at
  the bottom and the motif on the right.
- **Website:** compact sticky navigation with the App icon, product name, core links, language switch
  and download action; the hero; capability examples for files and commands, CLI, MCP, Skills,
  Computer Use and coding-agent hand-off; how hosts connect and how permissions work on each
  computer; a dated, sourced comparison with related products; three setup steps with a first safe
  tool call; FAQ, closing line and organization footer. The homepage is Chinese by default with a
  complete English version.

## Elevation & Depth

Depth comes from **offset stacking**, not blur. A plane sits 48px up and to the right of the plane
beneath it and casts a short, crisp shadow (`0 1px 0 rgba(0,0,0,.05), 0 22px 40px -14px
rgba(10,16,30,.30)`). At most three planes stack. The chat card uses the same shadow. The link runs
on the page plane, beneath cards and planes. In dark mode, shadows deepen
(`0 24px 48px -16px rgba(0,0,0,.6)`) and raised surfaces add a 1px line border.

## Shapes

Planes and cards use a 20px radius; buttons 12px; chips 6px; packets are fully rounded. The link is a
straight band with round caps that bends at most once. At 1024 scale the App icon uses a 64px plane
radius; the body is the macOS rounded rectangle on the 824px grid.

## Icon Family

- **Structure:** an ink body carrying a centred three-plane stack — graphite workspace, vermilion
  capabilities, paper result — each plane 58px up and to the right of the one beneath it. The mark
  is the computer alone; the chat card and the link appear only in compositions around it. No
  isometric projection; avoid any resemblance to cube marks.
- **Glyph:** the front plane carries one ink glyph with a 9% stroke. The App uses the **local node**
  (a dot inside a ring). Each component swaps only this glyph: computer-use pointer, apple-cli
  prompt, codex braces, swift-format aligned bars, claude speech bracket, cursor text caret, trae play
  wedge, homebrew-tap install tray.
- **Small sizes:** at 32px and below, drop the workspace plane and thicken the glyph.
- **App icon:** delivered as an Icon Composer document on an ink background with three depth groups
  — the result plane with its glyph, the capabilities plane and the workspace plane — plus a legacy
  `AppIcon.icns` for macOS 14 and 15.
- **Never:** vendor logos, the Apple or Swift logo, SF Symbols or SF Pro inside brand artwork. The
  swift-sdk fork keeps its upstream identity.

## Components

- **Primary button:** vermilion fill, ink JetBrains Mono label, 12px radius.
- **Secondary button:** raised surface with a 1px line border.
- **Chat card:** raised surface, 20px radius, a title row naming the chat, and the request as a
  vermilion bubble with ink text.
- **Planes:** graphite workspace plane labelled with the authorized folder; vermilion capabilities
  plane labelled "Tools you allow"; raised result plane with the computer's name, a connected
  status, the touched file and a passing command. Capability chips beside the composition name
  Files, Shell, CLI, MCP, Skills and Computer Use.
- **Link and packets:** a link-rail band with a 6px vermilion line; packets are raised pills naming
  the tool, such as `file.write`.
- **Status:** green for success, red for removals, caution badge for actions awaiting confirmation.
- **Chip and code block:** paper chip with a mono label; ink code block with paper text and a
  vermilion prompt.

## Do's and Don'ts

- Do keep vermilion for the active path and the primary action only.
- Do show both the chat and the computer whenever the link appears.
- Do stack at most three planes, offset up and to the right.
- Do render every image text with the bundled OFL fonts, in both light and dark.
- Don't use gradients on planes, or rotate them.
- Don't draw clouds, globes or padlocks; the link carries the meaning.
- Don't put text inside the App icon.

## Responsive

Breakpoints are 900px, 600px and 370px. Below 900px the hero stacks copy above the illustration, the
link becomes vertical and the plane offset halves to 24px. Below 600px the stack collapses to two
planes and the display size drops to 52px (Chinese 44px); side margins are 24px, and 16px below
370px. Touch targets stay at least 44px. Controls keep visible focus, meaningful selected states,
keyboard operation and reduced-motion support.

## Iteration Guide

Change tokens here first, then regenerate every asset with the organization renderer and deliver
them through each repository's brand lock. A new component swaps only the front-plane glyph and
never introduces a new color. Check the App icon in every macOS rendition, including Clear and
Tinted, before delivery. The repository README lists the render, check and delivery commands.
