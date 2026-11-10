// Capture chaque page HTML du feed v2 en JPEG (taille lue dans le fichier de tâches).
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: cfg.width, height: cfg.height }, deviceScaleFactor: 1 });
  for (const job of cfg.jobs) {
    await p.goto('file://' + job.html, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: job.out, type: 'jpeg', quality: 95 });
  }
  await b.close();
})();
