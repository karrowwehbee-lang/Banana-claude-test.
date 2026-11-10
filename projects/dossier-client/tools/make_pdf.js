// Génère le PDF (A4 paysage) et, en option, un aperçu PNG de chaque page, à partir de build/dossier.html.
// Usage : node make_pdf.js <dossier build> <fichier.pdf> [dossier aperçus]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const build = path.resolve(process.argv[2]);
  const out = process.argv[3];
  const previews = process.argv[4];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto('file://' + path.join(build, 'dossier.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: out, width: '297mm', height: '210mm', printBackground: true, preferCSSPageSize: true });
  if (previews) {
    const els = await p.$$('section.page');
    for (let i = 0; i < els.length; i++) {
      await els[i].screenshot({ path: path.join(previews, `p${String(i + 1).padStart(2, '0')}.png`) });
    }
  }
  await b.close();
})();
