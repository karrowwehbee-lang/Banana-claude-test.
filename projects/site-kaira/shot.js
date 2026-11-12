const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined });
  const out = process.argv[2];
  for (const [name, vp] of [['desk', { width: 1440, height: 900 }], ['phone', { width: 390, height: 844 }]]) {
    const ctx = await b.newContext({ viewport: vp, ignoreHTTPSErrors: true, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push('pageerror ' + e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push('console ' + m.text()); });
    p.on('requestfailed', r => errs.push('failed ' + r.url().slice(0, 90)));
    await p.goto('file://' + __dirname + '/index.html', { waitUntil: 'networkidle' });
    await p.waitForTimeout(3200);
    await p.screenshot({ path: `${out}/${name}-1.png` });
    const H = await p.evaluate(() => document.documentElement.scrollHeight);
    const W = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
    for (const y of [0.9, 1.6, 2.6, 3.6, 4.6, 6]) {
      await p.mouse.wheel(0, vp.height * (y === 0.9 ? 0.9 : 0.8));
      await p.evaluate((yy) => window.scrollTo(0, yy), Math.round(vp.height * y));
      await p.waitForTimeout(900);
      await p.screenshot({ path: `${out}/${name}-y${y}.png` });
    }
    await p.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
    await p.waitForTimeout(900);
    await p.screenshot({ path: `${out}/${name}-end.png` });
    console.log(name, 'height', H, 'scrollW/innerW', W, 'errors', JSON.stringify(errs.slice(0, 8)));
    await ctx.close();
  }
  await b.close();
})();
