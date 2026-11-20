// Captures screens of the finished website (served locally) for the launch kit.  node launch_screens.js <outdir>
const { chromium } = require('playwright');
const OUT = process.argv[2], BASE = 'http://127.0.0.1:8765/';
const at = async (p, sel, f) => { await p.evaluate(([s, f]) => { const el = document.querySelector(s); const y = el.offsetTop + (el.offsetHeight - innerHeight) * f; lenis ? lenis.scrollTo(y, { immediate: true, force: true }) : scrollTo(0, y); }, [sel, f]); await p.waitForTimeout(1300); };
(async () => {
  const b = await chromium.launch();
  const d = await (await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 })).newPage();
  await d.goto(BASE + '#home'); await d.waitForTimeout(6500);
  await d.screenshot({ path: OUT + '/desktop-home.png' });
  await at(d, '.hero', .47); await d.screenshot({ path: OUT + '/desktop-walls.png' });
  await at(d, '.fs', 0); await d.screenshot({ path: OUT + '/desktop-founder.png' });
  await at(d, '.reel', .215); await d.screenshot({ path: OUT + '/desktop-reel.png' });
  const m = await (await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true })).newPage();
  await m.goto(BASE + '#home'); await m.waitForTimeout(6500);
  await m.screenshot({ path: OUT + '/phone-home.png' });
  await at(m, '.fs', 0); await m.screenshot({ path: OUT + '/phone-founder.png' });
  await at(m, '.reel', .025); await m.screenshot({ path: OUT + '/phone-reel.png' });
  await m.goto(BASE + '#project-villa'); await m.reload(); await m.waitForTimeout(6500);
  await m.screenshot({ path: OUT + '/phone-villa.png' });
  await b.close();
})();
