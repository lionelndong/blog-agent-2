// Step 4: render the final infographic FROM the SVG-blueprint reference (image-to-image).
// Usage: node .analysis/nano_refine.js <blueprint.png> <out.png>  (REPLICATE_API_KEY in env)
const key = process.env.REPLICATE_API_KEY;
const fs = require('fs');
const imgPath = process.argv[2] || '.analysis/blueprint.png';
const out = process.argv[3] || '.analysis/infographic_final.png';
if (!key) { console.log('MISSING REPLICATE_API_KEY'); process.exit(0); }

const dataUri = 'data:image/png;base64,' + fs.readFileSync(imgPath).toString('base64');
const prompt = `Re-render this reference blueprint as a polished, premium editorial infographic.
KEEP every word, number, and the exact layout/composition from the reference image — do not change or add any text.
Refine the three icons into clean modern flat line-icons (camera, microphone, phone), improve typography and spacing,
keep the soft off-white background and the deep purple (#534ab7) numbers, add subtle professional depth and crispness.
Style: a high-end Ahrefs-style blog data-graphic. Keep the "Pleasur.AI" wordmark.
IMPORTANT: keep ALL text fully inside the frame with comfortable margins on every side — do not crop or cut off any words, especially the title.`;

(async () => {
  const r = await fetch('https://api.replicate.com/v1/models/google/nano-banana/predictions', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/json', 'Prefer': 'wait' },
    body: JSON.stringify({ input: { prompt, image_input: [dataUri], output_format: 'png' } }),
    signal: AbortSignal.timeout(120000),
  });
  let pred = await r.json();
  console.log('http', r.status, '| status', pred.status);
  if (pred.error) { console.log('ERROR', JSON.stringify(pred.error).slice(0, 400)); return; }
  let n = 0;
  while (pred.urls && pred.urls.get && (pred.status === 'processing' || pred.status === 'starting') && n < 30) {
    await new Promise(s => setTimeout(s, 3000)); n++;
    pred = await (await fetch(pred.urls.get, { headers: { Authorization: 'Bearer ' + key } })).json();
  }
  const url = Array.isArray(pred.output) ? pred.output[0] : pred.output;
  if (!url) { console.log('no output:', JSON.stringify(pred).slice(0, 400)); return; }
  const ir = await fetch(url);
  fs.writeFileSync(out, Buffer.from(await ir.arrayBuffer()));
  console.log('SAVED', out);
})().catch(e => console.log('FATAL', e.message));
