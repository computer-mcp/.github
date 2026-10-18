// Computer MCP icon family. Geometry is drawn on Apple's 1024 canvas with the body on the
// 824 grid; glyphs live in a 100-unit box. Colors come from DESIGN.md tokens.

export const GLYPHS = {
  node: {
    strokes: ['M20 50 a30 30 0 1 0 60 0 a30 30 0 1 0 -60 0'],
    fills: ['M39 50 a11 11 0 1 0 22 0 a11 11 0 1 0 -22 0'],
  },
  pointer: { strokes: ['M32 16 L32 78 L46 65 L56 86 L67 81 L57 60 L76 60 Z'] },
  prompt: { strokes: ['M24 30 L46 50 L24 70', 'M56 72 L80 72'] },
  braces: {
    strokes: [
      'M40 18 C30 18 32 28 32 36 C32 44 28 50 20 50 C28 50 32 56 32 64 C32 72 30 82 40 82',
      'M60 18 C70 18 68 28 68 36 C68 44 72 50 80 50 C72 50 68 56 68 64 C68 72 70 82 60 82',
    ],
  },
  bars: { strokes: ['M22 30 L78 30', 'M36 50 L78 50', 'M36 70 L64 70'] },
  speech: { strokes: ['M30 22 L70 22 Q80 22 80 32 L80 54 Q80 64 70 64 L46 64 L32 78 L33 64 L30 64 Q20 64 20 54 L20 32 Q20 22 30 22 Z'] },
  caret: { strokes: ['M38 20 L62 20', 'M38 80 L62 80', 'M50 20 L50 80'] },
  play: { strokes: ['M34 22 L76 50 L34 78 Z'] },
  tray: { strokes: ['M50 16 L50 56', 'M34 42 L50 58 L66 42', 'M20 62 L20 80 L80 80 L80 62'] },
};

const SVG = (body, defs = '', size = 1024) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="${size}" height="${size}">${defs ? `<defs>${defs}</defs>` : ''}${body}</svg>\n`;

export function squircle(cx = 512, cy = 512, r = 412, n = 5, steps = 360) {
  let d = '';
  for (let i = 0; i < steps; i++) {
    const t = (i / steps) * 2 * Math.PI;
    const c = Math.cos(t), s = Math.sin(t);
    const x = cx + r * Math.sign(c) * Math.abs(c) ** (2 / n);
    const y = cy + r * Math.sign(s) * Math.abs(s) ** (2 / n);
    d += (i ? 'L' : 'M') + x.toFixed(2) + ' ' + y.toFixed(2);
  }
  return d + 'Z';
}

export function glyph(name, { cx, cy, size, color, stroke }) {
  const g = GLYPHS[name];
  if (!g) throw new Error(`Unknown glyph: ${name}`);
  const s = size / 100;
  const strokes = (g.strokes || [])
    .map((d) => `<path d="${d}" fill="none" stroke="${color}" stroke-width="${stroke}" stroke-linecap="round" stroke-linejoin="round"/>`)
    .join('');
  const fills = (g.fills || []).map((d) => `<path d="${d}" fill="${color}"/>`).join('');
  return `<g transform="translate(${cx - size / 2} ${cy - size / 2}) scale(${s})">${strokes}${fills}</g>`;
}

// The mark: three planes stacked up and to the right, centred on the canvas. Small renditions
// drop the workspace plane and thicken the glyph.
function geometry(small) {
  const W = 430, H = 324, R = 64, off = 58;
  const n = small ? 1 : 2;
  const x0 = 512 - (W + n * off) / 2, y0 = 512 - (H + n * off) / 2;
  const roles = small ? ['capabilities', 'result'] : ['workspace', 'capabilities', 'result'];
  const planes = roles.map((role, i) => ({ role, x: x0 + i * off, y: y0 + (n - i) * off }));
  const front = planes[n];
  return { W, H, R, planes, glyph: { cx: front.x + W / 2, cy: front.y + H / 2, size: small ? 236 : 210, stroke: small ? 12 : 9 } };
}

const planeFill = (c, role) => ({ workspace: c['icon-plane-back'], capabilities: c['icon-plane-mid'], result: c['icon-plane-front'] })[role];

// Layers in front-to-back order; each is a self-contained SVG fragment on the 1024 canvas.
function layers(c, glyphName, small) {
  const g = geometry(small);
  return [
    ['glyph', glyph(glyphName, { ...g.glyph, color: c['icon-glyph'] })],
    ...g.planes.slice().reverse().map((p) => [`plane-${p.role}`, `<rect x="${p.x}" y="${p.y}" width="${g.W}" height="${g.H}" rx="${g.R}" fill="${planeFill(c, p.role)}"/>`]),
  ];
}

const SHADOW = '<filter id="lift" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="16" stdDeviation="14" flood-color="#000" flood-opacity="0.35"/></filter>';
const LIFTED = new Set(['plane-capabilities', 'plane-result']);

function artwork(c, glyphName, small) {
  return layers(c, glyphName, small).reverse()
    .map(([name, body]) => (LIFTED.has(name) ? `<g filter="url(#lift)">${body}</g>` : body)).join('');
}

// Classic macOS rendition: squircle body on the 824 grid with a soft drop shadow.
export function appIcon(c, glyphName, { small = false } = {}) {
  const body = squircle();
  const defs = `<filter id="drop" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="12" stdDeviation="14" flood-color="#000" flood-opacity="0.28"/></filter>
    ${SHADOW}<clipPath id="body"><path d="${body}"/></clipPath>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>`;
  return SVG(`<path d="${body}" fill="#000" filter="url(#drop)"/><path d="${body}" fill="${c['icon-body']}"/>
    <g clip-path="url(#body)"><rect width="1024" height="1024" fill="url(#sheen)"/>${artwork(c, glyphName, small)}</g>`, defs);
}

// Full-bleed rendition for places that apply their own mask: avatars and touch icons.
const BLEED = 'translate(512 512) scale(1.2427) translate(-512 -512)';
export function fullBleedIcon(c, glyphName) {
  return SVG(`<rect width="1024" height="1024" fill="${c['icon-body']}"/><g transform="${BLEED}">${artwork(c, glyphName, false)}</g>`, SHADOW);
}

// Icon Composer document: square, unmasked layers on the full canvas, background as fill.
export function iconComposer(c, glyphName) {
  const hex = (h) => h.match(/[0-9a-f]{2}/gi).map((x) => (parseInt(x, 16) / 255).toFixed(5)).join(',');
  const parts = layers(c, glyphName, false);
  const files = Object.fromEntries(parts.map(([name, body]) => [`Assets/${name}.svg`, SVG(`<g transform="${BLEED}">${body}</g>`)]));
  const group = (names) => ({
    layers: names.map((name) => ({ 'image-name': `${name}.svg`, name })),
    shadow: { kind: 'neutral', opacity: 0.5 },
    translucency: { enabled: false, value: 0.5 },
  });
  const json = {
    fill: { solid: `srgb:${hex(c['icon-body'])},1.00000` },
    groups: [group(['glyph', 'plane-result']), group(['plane-capabilities']), group(['plane-workspace'])],
    'supported-platforms': { squares: ['macOS'] },
  };
  files['icon.json'] = JSON.stringify(json, null, 2) + '\n';
  return files;
}
