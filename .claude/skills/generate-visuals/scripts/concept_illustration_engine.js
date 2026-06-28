// Pleasur.AI concept-illustration engine (NEW visual type, 2026-06-28).
// The rare ~6% "illustration" slot: a SINGLE illustrative image for an ABSTRACT concept
// (e.g. "AI memory", "your data stays private") where a screenshot / chart / table doesn't fit.
//
// AI is allowed here but in a NARROW, GATED lane (operator policy): an extreme, specific,
// STRUCTURED prompt -> Nano Banana (Replicate), then a HARD VISION GATE. If the result reads
// as "AI slop", generic, or off-brand -> CUT it (do NOT ship; iterate or abandon).
// See CONCEPT-ILLUSTRATION-RECIPE.md + VISUAL-CRITIQUE-LOOP.md (Concept illustration checklist).
//
// Anti-slop is LOCKED into the prompt: strict brand palette, ZERO text (the #1 AI tell — the
// metaphor must carry the meaning; any label is composited deterministically later), NO AI-drawn
// logo, no watermark/artifacts, hard SFW (public indexed blog, even though the product is adult).
// The ONLY creative variable is `metaphor` — write it richly + specifically; that is the craft.
//
// Usage: node concept_illustration_engine.js --content c.json --out raw.png [--style editorial-vector] [--aspect 16:9]
//   REPLICATE_API_KEY must be in env (pipeline injects via doppler) — mandatory, no fallback.
//   c.json: { "concept","metaphor","mood"?,"style"?,"aspect"? }
//   Optional logo afterward (where appropriate): python composite_logo.py --in raw.png --out final.png
const fs = require('fs');

function arg(name, def) { const i = process.argv.indexOf('--' + name); return i > -1 ? process.argv[i + 1] : def; }
const key = process.env.REPLICATE_API_KEY;
const out = arg('out', 'concept.png');
const contentPath = arg('content', null);
const ASPECTS = ['1:1', '2:3', '3:2', '3:4', '4:3', '4:5', '5:4', '9:16', '16:9', '21:9'];
if (!key) { console.log('FATAL: REPLICATE_API_KEY not set (mandatory — no fallback).'); process.exit(1); }

// NOTE the metaphor describes WHAT to depict, never the finish (no "glowing/glossy/3D" — that is
// the style's job; finish words in the metaphor produce the generic glossy-blob look).
const DEFAULT = {
  concept: 'AI memory — your companion remembers what matters to you',
  metaphor: 'a single friendly rounded chat-bubble that cradles a small, tidy constellation of memory ' +
    'tokens inside it — just three or four clean, simple icons (a coffee cup, a small birthday cake, a ' +
    'little heart) joined by thin connecting threads like a constellation, so the bubble reads as a mind ' +
    'gently holding a few cherished personal memories together',
  mood: 'warm, intelligent, reassuring',
  style: 'editorial-vector',
  aspect: '16:9',
};
const c = contentPath ? JSON.parse(fs.readFileSync(contentPath, 'utf8')) : DEFAULT;
const style = arg('style', c.style || 'editorial-vector');
const aspect = arg('aspect', c.aspect || '16:9');
if (!c.concept || !c.metaphor) { console.log('FATAL: content needs both "concept" and "metaphor".'); process.exit(1); }
if (!ASPECTS.includes(aspect)) { console.log('FATAL: aspect must be one of ' + ASPECTS.join(', ')); process.exit(1); }

// Locked anti-slop / SFW / no-text / no-logo tail — identical across styles. This is the gate-in-prompt.
const RULES =
  'DO NOT (hard constraints): NO text, letters, numbers, words, captions, labels, or UI mock-text ' +
  'anywhere in the image — the metaphor ALONE must carry the meaning (text is the #1 AI tell and it garbles). ' +
  'NO logo or wordmark. NO watermark, NO signature, NO stray marks, NO visual noise. Do NOT crop or cut off ' +
  'any element — keep everything fully inside the frame with comfortable margins. It must NOT look like a ' +
  'generic 3D render, clay/plasticine, stock photo, AI collage, or corporate-memphis blob-people. ' +
  'SFW and tasteful for a public blog: absolutely no nudity, no sexual or suggestive content, no romantic ' +
  'physical contact, no skin-focus. FINISH: crisp, cohesive, intentional, magazine-quality — designed, not ' +
  'auto-generated. Aspect ratio ' + aspect + '. High resolution.';

function editorialVector(c) {
  return 'Create a single premium EDITORIAL CONCEPT ILLUSTRATION for a high-end technology blog — one ' +
    'clear, beautiful image that communicates ONE idea at a glance.\n\n' +
    'CONCEPT: ' + c.concept + '.\n' +
    'WHAT TO DEPICT (the visual metaphor): ' + c.metaphor + '.\n\n' +
    'ART DIRECTION — FLAT 2D vector editorial illustration in the polished house style of the best product ' +
    'blogs (Stripe, Linear, Intercom): clean geometric construction, confident simple shapes, flat color ' +
    'fills with smooth brand gradients, crisp edges, only a hint of soft flat shadow for separation, a faint ' +
    'paper grain, restrained detail, lots of calm negative space. It must read as a designed printed ' +
    'illustration. CRITICAL: matte and flat — NOT glossy, NOT a shiny 3D render, NOT a glass app-icon, NOT a ' +
    'single centered glossy emoji-blob, NO plastic specular highlights.' +
    (c.mood ? ' Mood: ' + c.mood + '.' : '') + '\n\n' +
    'COLOR — use ONLY the brand palette: primary blue #2E90FA and violet #8B5CF6 as the dominant colors ' +
    '(a smooth blue-to-violet gradient on the hero), with mint-green #22B276 and a warm coral #FF6B5C as ' +
    'small accents ONLY, all on a clean very-light cool-tinted background (#F5F8FE soft off-white). The hero ' +
    'must be unmistakably brand BLUE and VIOLET — NOT cyan, teal, turquoise, pink, or random colors.\n\n' +
    'COMPOSITION — ONE clear focal element placed with intent (centered or rule-of-thirds), wrapped in ' +
    'generous negative space; keep the interior simple and tidy (a few clean shapes, never a cluttered ' +
    'pile of tiny objects); balanced, calm, uncluttered.\n\n' + RULES;
}

function flatGeometric(c) {
  return 'Create a single premium CONCEPT ILLUSTRATION for a high-end technology blog — one clear, ' +
    'beautiful image that communicates ONE idea at a glance.\n\n' +
    'CONCEPT: ' + c.concept + '.\n' +
    'WHAT TO DEPICT (the visual metaphor): ' + c.metaphor + '.\n\n' +
    'ART DIRECTION — bold FLAT geometric paper-cut illustration: clean layered shapes with subtle drop ' +
    'shadows between layers (cut-paper collage feel), confident minimal forms, generous negative space, ' +
    'a faint grain. Modern, calm, premium editorial. NOT glossy, NOT 3D-rendered, NOT a glass app-icon, ' +
    'NOT photorealistic, NO plastic specular highlights, NO clutter.' +
    (c.mood ? ' Mood: ' + c.mood + '.' : '') + '\n\n' +
    'COLOR — use ONLY the brand palette: primary blue #2E90FA and violet #8B5CF6 as the dominant colors, ' +
    'with mint-green #22B276 and warm coral #FF6B5C as small accents ONLY, on a clean very-light cool ' +
    'background (#F5F8FE). Dominant brand BLUE and VIOLET — NOT cyan, teal, pink, or random colors.\n\n' +
    'COMPOSITION — ONE clear focal element, layered paper-cut depth, lots of negative space; tidy and ' +
    'uncluttered.\n\n' + RULES;
}

function luminousDark(c) {
  return 'Create a single premium CONCEPT ILLUSTRATION for a high-end technology blog — one clear, ' +
    'beautiful image that communicates ONE idea at a glance.\n\n' +
    'CONCEPT: ' + c.concept + '.\n' +
    'WHAT TO DEPICT (the visual metaphor): ' + c.metaphor + '.\n\n' +
    'ART DIRECTION — luminous, minimal, abstract tech illustration on a deep near-black background ' +
    '(#0A0E1A): glowing forms lit by a blue #2E90FA to violet #8B5CF6 gradient, soft volumetric glow, ' +
    'fine light threads and sparse drifting particles, subtle depth, premium dark-mode aesthetic, lots of ' +
    'dark negative space. Mint #22B276 and warm coral #FF6B5C only as rare accent sparks. Calm, intelligent, ' +
    'high-end.' + (c.mood ? ' Mood: ' + c.mood + '.' : '') + '\n\n' +
    'COMPOSITION — ONE clear focal element placed with intent, wrapped in generous dark negative space; a ' +
    'single coherent light source; balanced and uncluttered; cinematic restraint.\n\n' + RULES;
}

const BUILDERS = { 'editorial-vector': editorialVector, 'flat-geometric': flatGeometric, 'luminous-dark': luminousDark };
const build = BUILDERS[style] || editorialVector;
const prompt = build(c);

(async () => {
  const r = await fetch('https://api.replicate.com/v1/models/google/nano-banana/predictions', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', 'Prefer': 'wait' },
    body: JSON.stringify({ input: { prompt, aspect_ratio: aspect, output_format: 'png' } }),
    signal: AbortSignal.timeout(120000),
  });
  let pred = await r.json();
  console.log('concept-illustration', style, aspect, '| http', r.status, '| status', pred.status);
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
