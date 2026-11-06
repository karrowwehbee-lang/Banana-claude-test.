// Usage: node render.js <wwwDir> <outDir> [views...]   (wwwDir serves scene.html, scene.js and ./three)
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const [www, out, ...views] = process.argv.slice(2);
const types = { '.js': 'text/javascript', '.html': 'text/html' };
const srv = http.createServer((q, r) => {
  const f = path.join(www, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); return r.end(); } r.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' }); r.end(d); });
}).listen(8765);
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  for (const v of (views.length ? views : ['salon-hero', 'salon-reverse', 'library', 'guest'])) {
    const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
    p.on('console', m => console.log(v, m.type(), m.text()));
    p.on('pageerror', e => console.log(v, 'ERR', e.message));
    await p.goto(`http://localhost:8765/scene.html?view=${v}`);
    await p.waitForFunction(() => window.__done, null, { timeout: 300000 });
    await p.screenshot({ path: path.join(out, `render-${v}.png`) });
    console.log('done', v); await p.close();
  }
  await b.close(); srv.close();
})();
