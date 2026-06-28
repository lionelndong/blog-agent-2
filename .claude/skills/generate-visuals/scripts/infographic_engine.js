// Pleasur.AI infographic engine (LOCKED recipe 2026-06-28).
// Style = hand-drawn-edu (hand-drawn illustration + CLEAN brand sans text) -> Nano Banana raster.
// Then run composite_logo.py to stamp the real logo. Content-driven.
//
// Usage: node infographic_engine.js --content content.json --out out.png [--style hand-drawn-edu]
//   REPLICATE_API_KEY must be in env (pipeline injects via doppler).
//   content.json: { "title","subtitle","takeaway","aspect"?, "items":[{icon,number,label,sublabel,color?}] }
const fs = require('fs');

function arg(name, def) { const i = process.argv.indexOf('--' + name); return i > -1 ? process.argv[i + 1] : def; }
const key = process.env.REPLICATE_API_KEY;
const out = arg('out', 'infographic.png');
const style = arg('style', 'hand-drawn-edu');
const contentPath = arg('content', null);
if (!key) { console.log('FATAL: REPLICATE_API_KEY not set (mandatory — no fallback).'); process.exit(1); }

const DEFAULT = {
  title: 'What 5,000 coins gets you', subtitle: 'your Standard plan, in plain numbers',
  takeaway: 'Text is unlimited — media spends coins.', aspect: '4:5 portrait',
  items: [
    { icon: 'camera', number: '500', label: 'AI images', sublabel: '10 coins each', color: 'blue' },
    { icon: 'microphone', number: '500', label: 'voice notes', sublabel: '10 coins each', color: 'mint' },
    { icon: 'phone-call', number: '100', label: 'call minutes', sublabel: '50 coins per minute', color: 'lavender' },
  ],
};
const c = contentPath ? JSON.parse(fs.readFileSync(contentPath, 'utf8')) : DEFAULT;
const palette = ['blue', 'mint', 'lavender', 'peach'];

function handDrawnEdu(c) {
  const cards = c.items.map((it, i) =>
    `Card ${i + 1} (${it.color || palette[i % 4]}): a hand-drawn ${it.icon} icon, big coral "${it.number}", "${it.label}"${it.sublabel ? `, small "${it.sublabel}"` : ''}.`
  ).join(' ');
  return `Create a premium HAND-DRAWN-ILLUSTRATION infographic — beautiful, polished, balanced and restrained (NOT messy, NOT cluttered). [TYPOGRAPHY OVERRIDE — HIGHEST PRIORITY]: EVERY piece of text (title, subtitle, numbers, labels) must be a CLEAN, MODERN, GEOMETRIC SANS-SERIF matching a premium tech blog (Geist / IBM Plex Sans) — crisp, evenly-spaced, perfectly legible — NEVER a handwritten, script, brush, or comic font. Only the ILLUSTRATION (card outlines, icons, doodles, connectors) is hand-drawn; the TEXT is always clean printed sans-serif. STYLE: warm cream paper-texture background (#F5F0E8 with subtle grain); the illustration is hand-drawn with a gentle wobble; macaron-pastel rounded cards as distinct zones — soft blue #A8D8EA, mint #B5E5CF, lavender #D5C6E0, peach #FFD5C2 — with wobbly hand-drawn outlines; CORAL-RED #E8655A for the big key numbers; color fills do not fully reach the outlines (casual feel); a few tasteful doodle decorations with restraint — small stars, sparkles, plus-signs, underlines (NOT cluttered); simple hand-drawn cartoon icons; generous whitespace, each zone breathes; premium, refined, magazine-quality. LAYOUT: a big bold clean sans-serif title on top, a small clean sans-serif subtitle, ${c.items.length} macaron pastel cards in a row, gentle hand-drawn connectors/doodles between them, a takeaway banner at the bottom. CONTENT — title (bold clean sans-serif): "${c.title}". Subtitle (clean sans-serif): "${c.subtitle}". ${cards} Bottom takeaway banner: "${c.takeaway}". Leave the bottom-right corner clean cream space — NO wordmark/logo/text there (a real logo is composited afterward). HARD RULES: spell every word and number EXACTLY as given, all fully inside the frame with comfortable margins; ALL text clean legible printed sans-serif (NEVER handwritten/script); restrained tasteful doodles; premium magazine-quality polish; clean empty bottom-right corner for the logo. Aspect ratio ${c.aspect || '4:5 portrait'}. High resolution.`;
}

const BUILDERS = { 'hand-drawn-edu': handDrawnEdu };
const prompt = (BUILDERS[style] || handDrawnEdu)(c);

(async () => {
  const r = await fetch('https://api.replicate.com/v1/models/google/nano-banana/predictions', {
    method: 'POST', headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', 'Prefer': 'wait' },
    body: JSON.stringify({ input: { prompt, output_format: 'png' } }), signal: AbortSignal.timeout(120000),
  });
  let pred = await r.json();
  console.log('infographic', style, '| http', r.status, '| status', pred.status);
  if (pred.error) { console.log('FATAL nano-banana error', JSON.stringify(pred.error).slice(0, 300)); process.exit(1); }
  let n = 0;
  while (pred.urls && pred.urls.get && (pred.status === 'processing' || pred.status === 'starting') && n < 30) {
    await new Promise(s => setTimeout(s, 3000)); n++;
    pred = await (await fetch(pred.urls.get, { headers: { Authorization: 'Bearer ' + key } })).json();
  }
  const url = Array.isArray(pred.output) ? pred.output[0] : pred.output;
  if (!url) { console.log('FATAL no output', JSON.stringify(pred).slice(0, 300)); process.exit(1); }
  fs.writeFileSync(out, Buffer.from(await (await fetch(url)).arrayBuffer()));
  console.log('SAVED', out);
})().catch(e => { console.log('FATAL', e.message); process.exit(1); });
