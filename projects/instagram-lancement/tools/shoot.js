// Capture chaque slide HTML en JPEG (qualité 95). jobs.json : {w, h, jobs: [[html, jpg], ...]}
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: cfg.w || 1080, height: cfg.h || 1080 }, deviceScaleFactor: 1 });
  for (const [html, out] of cfg.jobs) {
    await p.goto('file://' + html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot(out.endsWith('.png') ? { path: out, type: 'png' } : { path: out, type: 'jpeg', quality: 95 });
  }
  await b.close();
})();
