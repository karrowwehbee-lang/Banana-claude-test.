// Capture chaque publication HTML en JPEG 1080 × 1080 (qualité 95).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1080 }, deviceScaleFactor: 1 });
  for (const name of cfg.jobs) {
    await p.goto('file://' + path.join(cfg.build, name + '.html'), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(cfg.out, name + '.jpg'), type: 'jpeg', quality: 95 });
  }
  await b.close();
})();
