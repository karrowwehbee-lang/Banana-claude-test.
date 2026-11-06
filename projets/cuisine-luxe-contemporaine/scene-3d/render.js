const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1800,height:1200}});
p.on('console',m=>{if(m.type()==='error'||m.type()==='warning')console.log('console:',m.text().slice(0,300))});
p.on('pageerror',e=>console.log('err',e.message));
await p.goto('http://localhost:8765/index.html');await p.waitForFunction(()=>window.ready,{timeout:120000});
const ids=(process.argv[2]||'v1,v2,v3,v4').split(',');
for(const id of ids){const t=Date.now();const d=await p.evaluate(i=>window.renderView(i),id);
fs.writeFileSync(id+'.jpg',Buffer.from(d.split(',')[1],'base64'));console.log(id,Date.now()-t,'ms');}
await b.close();})();
