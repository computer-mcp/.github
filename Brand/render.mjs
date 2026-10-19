// Render every Computer MCP brand asset from DESIGN.md and config.json into Exports/.
// Usage: APP_ICONS_SCRIPT=/path/to/app_icons.py node Brand/render.mjs

import { execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import YAML from 'yaml';
import { chromium } from 'playwright';
import { appIcon, glyph } from './icons.mjs';

const BRAND = path.dirname(new URL(import.meta.url).pathname);
const ROOT = path.dirname(BRAND);
const EXPORTS = path.join(BRAND, 'Exports');
const CACHE = path.join(BRAND, '.cache');
const INPUTS = [
  'DESIGN.md', 'Brand/config.json', 'Brand/icons.mjs', 'Brand/render.mjs', 'Brand/package.json', 'Brand/package-lock.json',
  ...fs.readdirSync(path.join(BRAND, 'app-icon', 'layers')).filter((name) => name.endsWith('.svg')).sort()
    .map((name) => `Brand/app-icon/layers/${name}`),
];
const APP_ICONS_SCRIPT = process.env.APP_ICONS_SCRIPT;
if (!APP_ICONS_SCRIPT?.trim()) throw new Error('Set APP_ICONS_SCRIPT to the apple-app-icon-design generator script (app_icons.py). Icon Composer from Xcode is required; IC_TOOL can select its ictool.');

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const config = JSON.parse(fs.readFileSync(path.join(BRAND, 'config.json'), 'utf8'));
const design = YAML.parse(fs.readFileSync(path.join(ROOT, 'DESIGN.md'), 'utf8').match(/^---\n([\s\S]*?)\n---\n/)[1]);
const c = design.colors, t = design.typography, r = design.rounded;

async function fonts() {
  const directory = path.join(CACHE, 'fonts');
  fs.mkdirSync(directory, { recursive: true });
  const faces = [];
  for (const font of config.fonts) {
    const file = path.join(directory, `${font.sha256}.ttf`);
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

const dataUri = (data, type = 'image/svg+xml') => `data:${type};base64,${Buffer.from(data).toString('base64')}`;
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
    signal: dark ? c['signal-dark'] : c.signal,
    rail: dark ? c['link-rail-dark'] : c['link-rail'],
    caseFill: dark ? c['computer-case-dark'] : c['computer-case'],
    caseEdge: dark ? c['computer-edge-dark'] : c['computer-edge'],
    chin: dark ? c['computer-chin-dark'] : c['computer-chin'],
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

// The App icon's computer, drawn flat from its own layers: chin, amber screen, ivory case.
// (cx, top) is the top centre of the case; h is the height of case and chin together.
const LAYER = (name) => {
  const svg = fs.readFileSync(path.join(BRAND, 'app-icon', 'layers', `${name}.svg`), 'utf8');
  return svg.slice(svg.indexOf('>') + 1, svg.lastIndexOf('</svg>')).replace(/fill="#[0-9A-Fa-f]{6}"/g, '');
};
const CASE = { x0: 240, y0: 196, x1: 784, y1: 782 };   // case and chin bounds in layer coordinates
const SCREEN = { x: 286, y: 240, w: 452, h: 344 };     // screen light bounds in layer coordinates

function computer(p, { cx, top, h }, screen = '') {
  const s = h / (CASE.y1 - CASE.y0), x = cx - ((CASE.x0 + CASE.x1) / 2) * s, y = top - CASE.y0 * s;
  const w = (CASE.x1 - CASE.x0) * s;
  const inset = `left:${x + SCREEN.x * s}px;top:${y + SCREEN.y * s}px;width:${SCREEN.w * s}px;height:${SCREEN.h * s}px`;
  return `<svg style="position:absolute;left:0;top:0;overflow:visible;filter:drop-shadow(${p.dark ? '0 22px 30px rgba(0,0,0,.55)' : '0 18px 26px rgba(10,16,30,.22)'})" width="1" height="1">
      <g transform="translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${s.toFixed(4)})">
        <g fill="${p.chin}">${LAYER('crt-base')}</g>
        <g fill="${p.signal}">${LAYER('crt-light')}</g>
        <g fill="${p.caseFill}" stroke="${p.caseEdge}" stroke-width="${(1.5 / s).toFixed(2)}">${LAYER('crt-body')}</g>
      </g></svg>
    <div style="position:absolute;${inset};display:flex;align-items:center;justify-content:center;color:${c['on-signal']}" data-w="${w.toFixed(0)}">${screen}</div>`;
}

function link(p, points, width = 30) {
  const d = 'M' + points.map(([x, y]) => `${x} ${y}`).join(' L');
  return `<svg width="100%" height="100%" style="position:absolute;inset:0">
    <path d="${d}" fill="none" stroke="${p.rail}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${d}" fill="none" stroke="${p.signal}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
}

const check = (color) => `<svg width="12" height="12" viewBox="0 0 12 12" style="vertical-align:-1px"><path d="M2 6.5 L5 9.5 L10.5 2.5" fill="none" stroke="${color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

const glyphSvg = (name, color, size) => `<svg width="${size}" height="${size}" viewBox="0 0 1024 1024">${glyph(name, { cx: 512, cy: 512, size: 1024, color, stroke: 9 })}</svg>`;

function header(faces, member, mode, locale = 'en') {
  const p = palette(mode);
  const isApp = member.repository === 'computer-mcp';
  const icon = isApp ? appIconPng : dataUri(appIcon(c, member.glyph));
  const screen = isApp ? '' : glyphSvg(member.glyph, c['on-signal'], 84);
  const ask = esc(config.copy.request[locale] ?? config.copy.request.en);
  return page(faces, 1280, 320, `
    body{background:${p.bg};color:${p.fg}}
    .id{position:absolute;left:64px;top:0;height:320px;display:flex;align-items:center;gap:36px;z-index:2}
    .id img{width:184px;height:184px}
    .eyebrow{${typo('label-md')};color:${p.accent};margin-bottom:12px}
    h1{${typo('headline-lg')}}
    .line{${typo('body-lg', { fontSize: '21px' })};color:${p.muted};margin-top:12px;max-width:560px}
    .req{position:absolute;left:688px;top:34px;width:290px;z-index:2;background:${p.raised};border:1px solid ${p.line};border-radius:${r.lg};padding:12px;box-shadow:${p.shadow}}
    .req div{${typo('body-md', { fontSize: '15px', lineHeight: 1.35 })};background:${p.signal};color:${c['on-signal']};border-radius:16px 16px 6px 16px;padding:9px 13px}
  `, `${link(p, [[972, 79], [1120, 79], [1120, 116]], 22)}
    ${computer(p, { cx: 1120, top: 116, h: 184 }, screen)}
    <div class="req"><div>${ask}</div></div>
    <div class="id"><img src="${icon}"><div>${member.eyebrow ? `<div class="eyebrow">${esc(member.eyebrow)}</div>` : ''}<h1>${esc(member.title)}</h1><p class="line">${esc(member.line[locale])}</p></div></div>`);
}

function appSocial(faces, member, locale) {
  const p = palette('light');
  const zh = locale === 'zh-CN';
  const icon = appIconPng;
  const card = { x: 744, y: 64, w: 372 };
  const lx = 1000, top = 268;
  const result = `<div style="${typo('code-md', { fontSize: '17px', lineHeight: 1.55 })};color:${c['on-signal']}">
      <div>$ swift test</div>
      <div>${check(c['on-signal'])} 128 tests passed</div></div>`;
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
    .ask{${typo('body-md', { fontSize: '15px' })};background:${p.signal};color:${c['on-signal']};border-radius:16px 16px 6px 16px;padding:9px 13px;margin-left:auto;width:fit-content}
    .pk{position:absolute;z-index:3;${typo('code-md', { fontWeight: 600, lineHeight: 1.2 })};background:${p.raised};color:${p.fg};border:1px solid ${p.line};border-radius:999px;padding:6px 11px;box-shadow:0 6px 14px -6px rgba(10,16,30,.25)}
    .pk i{font-style:normal;color:${p.accent}}
  `, `${link(p, [[lx, card.y + 60], [lx, top + 4]], 30)}
    <div class="card" style="left:${card.x}px;top:${card.y}px;width:${card.w}px"><div class="t">ChatGPT</div><div class="ask">${esc(config.copy.request[locale])}</div></div>
    <div class="pk" style="left:${lx + 26}px;top:${card.y + 128}px"><i>→</i> file.write</div>
    <div class="pk" style="left:${lx + 26}px;top:${card.y + 172}px"><i>→</i> shell.run</div>
    ${computer(p, { cx: lx, top, h: 300 }, result)}
    <div class="top"><img src="${icon}"><b>${esc(member.title)}</b></div>
    <h1>${esc(config.copy.headline[locale]).replace('，', '，<br>')}</h1>
    <div class="chips">${config.copy.capabilities.map((x) => `<span class="chip">${esc(x)}</span>`).join('')}</div>`);
}

function memberSocial(faces, member) {
  const p = palette('light');
  const icon = dataUri(appIcon(c, member.glyph));
  const B = { x: 760, y: 96, w: 210, h: 150 }, cx = 1060, top = 290;
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
  `, `${link(p, [[B.x + B.w - 24, B.y + B.h / 2], [cx, B.y + B.h / 2], [cx, top + 4]], 34)}
    <svg style="position:absolute;left:0;top:0;z-index:2;overflow:visible" width="1280" height="640"><defs><filter id="lift" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="16" flood-color="#0a101e" flood-opacity=".22"/></filter></defs>
      <path filter="url(#lift)" d="M${B.x + 28} ${B.y} H${B.x + B.w - 28} Q${B.x + B.w} ${B.y} ${B.x + B.w} ${B.y + 28} V${B.y + B.h - 28} Q${B.x + B.w} ${B.y + B.h} ${B.x + B.w - 28} ${B.y + B.h} H${B.x + 96} L${B.x + 30} ${B.y + B.h + 46} L${B.x + 44} ${B.y + B.h} H${B.x + 28} Q${B.x} ${B.y + B.h} ${B.x} ${B.y + B.h - 28} V${B.y + 28} Q${B.x} ${B.y} ${B.x + 28} ${B.y} Z" fill="${p.raised}" stroke="${p.line}"/></svg>
    <div class="bubble" style="left:${B.x}px;top:${B.y}px;width:${B.w}px;height:${B.h}px;background:none;border:0;box-shadow:none"><i></i><i></i><i></i></div>
    ${computer(p, { cx, top, h: 286 }, glyphSvg(member.glyph, c['on-signal'], 120))}
    <div class="top"><img src="${icon}"><div><div class="eyebrow">${esc(member.eyebrow)}</div><b>${esc(member.title)}</b></div></div>
    <h1>${esc(member.line.en)}</h1>
    <div class="url">github.com/computer-mcp/${member.repository}</div>`);
}

const written = new Set();

function write(name, data) {
  const file = path.join(EXPORTS, name);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, data);
  written.add(name);
}

function copyDirectory(source, target) {
  for (const entry of fs.readdirSync(source, { withFileTypes: true })) {
    const file = path.join(source, entry.name), name = `${target}/${entry.name}`;
    if (entry.isDirectory()) copyDirectory(file, name);
    else write(name, fs.readFileSync(file));
  }
}

function generateAppIcon() {
  fs.mkdirSync(CACHE, { recursive: true });
  const temporary = fs.mkdtempSync(path.join(CACHE, 'app-icon-'));
  const output = path.join(temporary, 'output');
  try {
    execFileSync('python3', [APP_ICONS_SCRIPT, path.join(ROOT, 'DESIGN.md'), '--name', 'computer-mcp', '--style', 'liquid-glass', '--out', output], { stdio: 'inherit' });
    const manifest = JSON.parse(fs.readFileSync(path.join(output, 'manifest.json'), 'utf8'));
    const png = fs.readFileSync(path.join(output, 'renditions', 'macOS-Default.png'));
    fs.rmSync(EXPORTS, { recursive: true, force: true });
    copyDirectory(path.join(output, 'computer-mcp.icon'), 'app/AppIcon.icon');
    write('app/app-icon.png', png);
    for (const name of ['favicon.svg', 'favicon-32.png', 'apple-touch-icon.png']) {
      write(`web/${name}`, fs.readFileSync(path.join(output, 'web', name)));
    }
    write('web/avatar.png', fs.readFileSync(path.join(output, 'web', 'avatar-1024.png')));
    return { png: dataUri(png, 'image/png'), renderer: manifest.renderer };
  } finally {
    fs.rmSync(temporary, { recursive: true, force: true });
  }
}

const app = generateAppIcon();
const appIconPng = app.png;
const faces = await fonts();
const browser = await chromium.launch();
const context = await browser.newContext();

async function shot(name, html, [w, h, scale = 1], transparent = false) {
  const tmp = path.join(CACHE, 'render.html');
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

const S = config.sizes;

for (const member of config.members) {
  const repo = member.repository;
  if (repo !== 'computer-mcp') {
    const svg = appIcon(c, member.glyph);
    write(`icons/${repo}.svg`, svg);
    await shot(`icons/${repo}.png`, raster(faces, svg, S.icon), S.icon, true);
  }
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
  renderer: { playwright: pkg.version, chromium: browser.version(), node: process.version, platform: process.platform, architecture: process.arch, ictool: app.renderer },
  exports: Object.fromEntries([...written].sort().map((name) => [name, sha256(fs.readFileSync(path.join(EXPORTS, name)))])),
};
await browser.close();
fs.writeFileSync(path.join(EXPORTS, 'manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(`Rendered ${written.size} brand assets`);
