// Render every Computer MCP brand asset from DESIGN.md and config.json into Exports/.
// Usage: node Brand/render.mjs   (after `npm ci` and `npx playwright install --only-shell chromium`)

import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import YAML from 'yaml';
import { chromium } from 'playwright';
import { appIcon, fullBleedIcon, glyph, iconComposer } from './icons.mjs';

const BRAND = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.dirname(BRAND);
const EXPORTS = path.join(BRAND, 'Exports');
const CACHE = path.join(BRAND, '.cache', 'fonts');
const INPUTS = ['DESIGN.md', 'Brand/config.json', 'Brand/icons.mjs', 'Brand/render.mjs', 'Brand/package.json', 'Brand/package-lock.json'];

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const config = JSON.parse(fs.readFileSync(path.join(BRAND, 'config.json'), 'utf8'));
const design = YAML.parse(fs.readFileSync(path.join(ROOT, 'DESIGN.md'), 'utf8').match(/^---\n([\s\S]*?)\n---\n/)[1]);
const c = design.colors, t = design.typography, r = design.rounded;

async function fonts() {
  fs.mkdirSync(CACHE, { recursive: true });
  const faces = [];
  for (const font of config.fonts) {
    const file = path.join(CACHE, `${font.sha256}.ttf`);
    if (!fs.existsSync(file)) {
      const response = await fetch(font.url);
      if (!response.ok) throw new Error(`Font download failed: ${font.family}`);
      fs.writeFileSync(file, Buffer.from(await response.arrayBuffer()));
    }
    if (sha256(fs.readFileSync(file)) !== font.sha256) throw new Error(`Font digest mismatch: ${font.family}`);
    faces.push(`@font-face{font-family:'${font.family}';src:url('file://${file}');font-weight:${font.weight};font-display:block}`);
  }
  return faces.join('\n');
}

function typo(name, extra = {}) {
  const v = { ...t[name], ...extra };
  return [
    `font-family:'${v.fontFamily}','Noto Sans SC'`,
    `font-size:${v.fontSize}`,
    `font-weight:${v.fontWeight}`,
    `line-height:${v.lineHeight}`,
    v.letterSpacing && `letter-spacing:${v.letterSpacing}`,
    v.fontVariation && `font-variation-settings:${v.fontVariation}`,
  ].filter(Boolean).join(';');
}

const dataUri = (svg) => `data:image/svg+xml;base64,${Buffer.from(svg).toString('base64')}`;
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

function palette(mode) {
  const dark = mode === 'dark';
  return {
    dark,
    bg: dark ? c['surface-dark'] : c.surface,
    raised: dark ? c['surface-raised-dark'] : c['surface-raised'],
    fg: dark ? c['on-surface-dark'] : c['on-surface'],
    muted: dark ? c['on-surface-muted-dark'] : c['on-surface-muted'],
    line: dark ? c['line-dark'] : c.line,
    accent: dark ? c['accent-text-dark'] : c['accent-text'],
    rail: dark ? c['link-rail-dark'] : c['link-rail'],
    ok: dark ? c['success-dark'] : c.success,
    shadow: dark ? '0 24px 48px -16px rgba(0,0,0,.6)' : '0 1px 0 rgba(0,0,0,.05),0 22px 40px -14px rgba(10,16,30,.30)',
  };
}

const page = (faces, w, h, css, body) => `<!doctype html><html><head><meta charset="utf-8"><style>
${faces}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${w}px;height:${h}px;overflow:hidden}
body{position:relative;-webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.pl{position:absolute;border-radius:${r.lg}}
${css}
</style></head><body>${body}</body></html>`;

// Planes offset up and to the right; front is the top-right plane.
function stack(p, { x, y, w, h, off }, labels = {}, front = '') {
  const label = (role) => `display:flex;align-items:flex-end;padding:0 18px 12px;${typo(role, { fontWeight: 600, lineHeight: 1.2 })};white-space:nowrap`;
  return `
    <div class="pl" style="left:${x - 2 * off}px;top:${y + 2 * off}px;width:${w}px;height:${h}px;background:${c['plane-back']};color:${c['on-plane-back']};${label('code-md')}">${labels.workspace || ''}</div>
    <div class="pl" style="left:${x - off}px;top:${y + off}px;width:${w}px;height:${h}px;background:${c.tertiary};color:${c['on-accent']};box-shadow:${p.shadow};${label('label-md')}">${labels.capabilities || ''}</div>
    <div class="pl" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;background:${p.raised};border:1px solid ${p.line};box-shadow:${p.shadow};color:${p.fg}">${front}</div>`;
}

function link(p, points, width = 30) {
  const d = 'M' + points.map(([x, y]) => `${x} ${y}`).join(' L');
  return `<svg width="100%" height="100%" style="position:absolute;inset:0">
    <path d="${d}" fill="none" stroke="${p.rail}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" fill="none" stroke="${c.tertiary}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

const check = (color) => `<svg width="12" height="12" viewBox="0 0 12 12" style="vertical-align:-1px"><path d="M2 6.5 L5 9.5 L10.5 2.5" fill="none" stroke="${color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

const glyphSvg = (name, color, size) => `<svg width="${size}" height="${size}" viewBox="0 0 1024 1024">${glyph(name, { cx: 512, cy: 512, size: 1024, color, stroke: 9 })}</svg>`;

function header(faces, member, mode, locale = 'en') {
  const p = palette(mode);
  const icon = dataUri(appIcon(c, member.glyph));
  const front = `<div style="position:absolute;left:0;top:0;width:270px;height:100%;display:flex;align-items:center;justify-content:center">${glyphSvg(member.glyph, p.fg, 104)}</div>`;
  return page(faces, 1280, 320, `
    body{background:${p.bg};color:${p.fg}}
    .id{position:absolute;left:64px;top:0;height:320px;display:flex;align-items:center;gap:36px;z-index:2}
    .id img{width:184px;height:184px}
    .eyebrow{${typo('label-md')};color:${p.accent};margin-bottom:12px}
    h1{${typo('headline-lg')}}
    .line{${typo('body-lg', { fontSize: '21px' })};color:${p.muted};margin-top:12px;max-width:620px}
  `, `${link(p, [[1120, -20], [1120, 120]], 26)}
    ${stack(p, { x: 1010, y: 96, w: 300, h: 196, off: 34 }, {}, front)}
    <div class="id"><img src="${icon}"><div>${member.eyebrow ? `<div class="eyebrow">${esc(member.eyebrow)}</div>` : ''}<h1>${esc(member.title)}</h1><p class="line">${esc(member.line[locale])}</p></div></div>`);
}

function appSocial(faces, member, locale) {
  const p = palette('light');
  const zh = locale === 'zh-CN';
  const icon = dataUri(appIcon(c, member.glyph));
  const card = { x: 744, y: 64, w: 372 };
  const lx = 1200, ly = card.y + 66, F = { x: 868, y: 318, w: 380, h: 176, off: 40 };
  const result = `<div style="padding:16px 18px;${typo('code-md')}">
      <div style="display:flex;gap:10px;${typo('label-md')};color:${p.muted};margin-bottom:10px"><b style="font-weight:600;color:${p.fg}">MacBook Pro</b><span style="margin-left:auto;color:${p.ok}">● ${zh ? '已连接' : 'connected'}</span></div>
      <div style="color:${p.muted}">Sources/Checkout/Session.swift</div>
      <div><span style="color:${p.accent}">$</span> swift test</div>
      <div>${check(p.ok)} 128 tests passed · 6.2s</div></div>`;
  return page(faces, 1280, 640, `
    body{background:${p.bg};color:${p.fg}}
    .top{position:absolute;left:80px;top:72px;display:flex;align-items:center;gap:24px;z-index:2}
    .top img{width:112px;height:112px}
    .top b{${typo('headline-md', { fontSize: '38px' })}}
    h1{position:absolute;left:80px;top:${zh ? 252 : 240}px;width:${zh ? 600 : 610}px;${zh ? typo('headline-zh', { fontSize: '64px' }) : typo('headline-display', { fontSize: '68px' })};z-index:2}
    .chips{position:absolute;left:80px;bottom:72px;display:flex;gap:8px;z-index:2}
    .chip{${typo('label-md')};background:${c.neutral};color:${c['on-surface']};border:1px solid ${p.line};border-radius:${r.sm};padding:7px 10px}
    .card{position:absolute;z-index:2;background:${p.raised};border:1px solid ${p.line};border-radius:${r.lg};padding:16px 18px;box-shadow:${p.shadow}}
    .card .t{${typo('label-md')};color:${p.muted};margin-bottom:10px}
    .ask{${typo('body-md', { fontSize: '15px' })};background:${c.tertiary};color:${c['on-accent']};border-radius:16px 16px 6px 16px;padding:9px 13px;margin-left:auto;width:fit-content}
    .pk{position:absolute;z-index:3;${typo('code-md', { fontWeight: 600, lineHeight: 1.2 })};background:${p.raised};color:${p.fg};border:1px solid ${p.line};border-radius:999px;padding:6px 11px;box-shadow:0 6px 14px -6px rgba(10,16,30,.25)}
    .pk i{font-style:normal;color:${p.accent}}
  `, `${link(p, [[card.x + card.w - 20, ly], [lx, ly], [lx, F.y + 30]], 34)}
    <div class="card" style="left:${card.x}px;top:${card.y}px;width:${card.w}px"><div class="t">ChatGPT</div><div class="ask">${esc(config.copy.request[locale])}</div></div>
    <div class="pk" style="left:${lx - 58}px;top:${ly + 54}px"><i>→</i> file.write</div>
    <div class="pk" style="left:${lx - 54}px;top:${ly + 104}px"><i>→</i> shell.run</div>
    ${stack(p, F, { workspace: esc(config.copy.planes.workspace), capabilities: esc(config.copy.planes.capabilities[locale]) }, result)}
    <div class="top"><img src="${icon}"><b>${esc(member.title)}</b></div>
    <h1>${esc(config.copy.headline[locale]).replace('，', '，<br>')}</h1>
    <div class="chips">${config.copy.capabilities.map((x) => `<span class="chip">${esc(x)}</span>`).join('')}</div>`);
}

function memberSocial(faces, member) {
  const p = palette('light');
  const icon = dataUri(appIcon(c, member.glyph));
  const B = { x: 790, y: 96, w: 210, h: 150 }, F = { x: 904, y: 318, w: 330, h: 210, off: 42 };
  const front = `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${glyphSvg(member.glyph, p.fg, 140)}</div>`;
  return page(faces, 1280, 640, `
    body{background:${p.bg};color:${p.fg}}
    .top{position:absolute;left:80px;top:72px;display:flex;align-items:center;gap:24px;z-index:2}
    .top img{width:112px;height:112px}
    .eyebrow{${typo('label-md')};color:${p.accent};margin-bottom:8px}
    .top b{${typo('headline-md', { fontSize: '38px' })}}
    h1{position:absolute;left:80px;top:250px;width:640px;${typo('headline-display', { fontSize: '62px' })};z-index:2}
    .url{position:absolute;left:80px;bottom:76px;${typo('label-lg')};color:${p.muted}}
    .bubble{position:absolute;z-index:2;background:${p.raised};border:1px solid ${p.line};border-radius:28px;box-shadow:${p.shadow};display:flex;align-items:center;justify-content:center;gap:16px}
    .bubble i{width:18px;height:18px;border-radius:50%;background:${c['on-surface']}}
  `, `${link(p, [[B.x + B.w - 24, B.y + B.h / 2], [F.x + 200, B.y + B.h / 2], [F.x + 200, F.y + 30]], 34)}
    <svg style="position:absolute;left:0;top:0;z-index:2;overflow:visible" width="1280" height="640"><defs><filter id="lift" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#0a101e" flood-opacity=".22"/></filter></defs>
      <path filter="url(#lift)" d="M${B.x + 28} ${B.y} H${B.x + B.w - 28} Q${B.x + B.w} ${B.y} ${B.x + B.w} ${B.y + 28} V${B.y + B.h - 28} Q${B.x + B.w} ${B.y + B.h} ${B.x + B.w - 28} ${B.y + B.h} H${B.x + 96} L${B.x + 30} ${B.y + B.h + 46} L${B.x + 44} ${B.y + B.h} H${B.x + 28} Q${B.x} ${B.y + B.h} ${B.x} ${B.y + B.h - 28} V${B.y + 28} Q${B.x} ${B.y} ${B.x + 28} ${B.y} Z" fill="${p.raised}" stroke="${p.line}"/></svg>
    <div class="bubble" style="left:${B.x}px;top:${B.y}px;width:${B.w}px;height:${B.h}px;background:none;border:0;box-shadow:none"><i></i><i></i><i></i></div>
    ${stack(p, F, {}, front)}
    <div class="top"><img src="${icon}"><div><div class="eyebrow">${esc(member.eyebrow)}</div><b>${esc(member.title)}</b></div></div>
    <h1>${esc(member.line.en)}</h1>
    <div class="url">github.com/computer-mcp/${member.repository}</div>`);
}

const browser = await chromium.launch();
const context = await browser.newContext();
const written = new Set();

function write(name, data) {
  const file = path.join(EXPORTS, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, data);
  written.add(name);
}

async function shot(name, html, [w, h, scale = 1], transparent = false) {
  const tmp = path.join(os.tmpdir(), `computer-mcp-brand-${process.pid}.html`);
  fs.writeFileSync(tmp, html);
  const pg = await context.newPage({ deviceScaleFactor: scale });
  await pg.setViewportSize({ width: w, height: h });
  await pg.goto('file://' + tmp);
  await pg.evaluate(async () => {
    await Promise.all([...document.fonts].map((f) => f.load()));
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.decode()));
  });
  const png = await pg.screenshot({ clip: { x: 0, y: 0, width: w, height: h }, omitBackground: transparent });
  await pg.close();
  fs.rmSync(tmp);
  write(name, png);
}

const raster = (faces, svg, [w, h]) => page(faces, w, h, 'body{background:transparent}img{width:100%;height:100%;display:block}', `<img src="${dataUri(svg)}">`);

fs.rmSync(EXPORTS, { recursive: true, force: true });
const faces = await fonts();
const S = config.sizes;

for (const [name, data] of Object.entries(iconComposer(c, 'node'))) write(`app/AppIcon.icon/${name}`, data);
const app = appIcon(c, 'node');
write('app/app-icon.svg', app);
await shot('app/app-icon.png', raster(faces, app, S.app_icon), S.app_icon, true);
write('web/favicon.svg', appIcon(c, 'node', { small: true }));
await shot('web/favicon-32.png', raster(faces, appIcon(c, 'node', { small: true }), S.favicon), S.favicon, true);
await shot('web/apple-touch-icon.png', raster(faces, fullBleedIcon(c, 'node'), S.apple_touch_icon), S.apple_touch_icon);
await shot('web/avatar.png', raster(faces, fullBleedIcon(c, 'node'), S.avatar), S.avatar);

for (const member of config.members) {
  const repo = member.repository;
  const svg = appIcon(c, member.glyph);
  write(`icons/${repo}.svg`, svg);
  await shot(`icons/${repo}.png`, raster(faces, svg, S.icon), S.icon, true);
  for (const locale of Object.keys(member.line)) {
    const suffix = locale === 'en' ? '' : `-${locale}`;
    for (const mode of ['light', 'dark']) await shot(`headers/${repo}${suffix}-${mode}.png`, header(faces, member, mode, locale), S.header);
    await shot(`social/${repo}${suffix}.png`, repo === 'computer-mcp' ? appSocial(faces, member, locale) : memberSocial(faces, member), S.social);
  }
}

const pkg = JSON.parse(fs.readFileSync(path.join(BRAND, 'node_modules/playwright/package.json'), 'utf8'));
const manifest = {
  schema_version: 1,
  inputs: Object.fromEntries(INPUTS.map((name) => [name, sha256(fs.readFileSync(path.join(ROOT, name)))])),
  renderer: { playwright: pkg.version, chromium: browser.version(), node: process.version, platform: process.platform, architecture: process.arch },
  exports: Object.fromEntries([...written].sort().map((name) => [name, sha256(fs.readFileSync(path.join(EXPORTS, name)))])),
};
await browser.close();
fs.writeFileSync(path.join(EXPORTS, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`Rendered ${written.size} brand assets`);
