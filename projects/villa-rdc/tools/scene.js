// KAÏRA — Villa ground floor: 3D concept scene (three.js).
// Plan coordinates are in metres, same origin as the layout plan:
// inner south-west corner of the living room, x = east, y = north.
// World mapping: X = x, Y = height, Z = -y.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const params = new URLSearchParams(location.search);
const VIEW = params.get('view') || 'salon-hero';
const W = +(params.get('w') || 1600), H = +(params.get('h') || 1000);
const CH = 2.8;           // ceiling height (assumed, to confirm)
const T = 0.2;            // wall thickness

// ---------- deterministic random ----------
let seed = 7;
const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
const rr = (a, b) => a + (b - a) * rnd();

// ---------- procedural textures ----------
function canvasTex(w, h, draw, repeatX = 1, repeatY = 1, srgb = true) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeatX, repeatY);
  t.anisotropy = 8; if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
const shade = (hex, k) => {
  const c = new THREE.Color(hex); c.offsetHSL(0, 0, k); return '#' + c.getHexString();
};
function speckle(g, w, h, n, col, a, s = 2) {
  g.fillStyle = col;
  for (let i = 0; i < n; i++) { g.globalAlpha = a * rnd(); g.fillRect(rnd() * w, rnd() * h, s * rnd() + 0.5, s * rnd() + 0.5); }
  g.globalAlpha = 1;
}
const oakDraw = (base) => (g, w, h) => {      // planks run along canvas Y
  const planks = 8, pw = w / planks;
  for (let p = 0; p < planks; p++) {
    let y = -rr(0, h);
    while (y < h) {
      const len = rr(h * 0.45, h * 0.9);
      g.fillStyle = shade(base, rr(-0.025, 0.025));
      g.fillRect(p * pw, y, pw, len);
      for (let k = 0; k < 26; k++) {          // grain
        g.strokeStyle = shade(base, rr(-0.12, 0.02)); g.globalAlpha = rr(0.15, 0.45);
        g.lineWidth = rr(0.5, 1.6); g.beginPath();
        const x0 = p * pw + rr(2, pw - 2); g.moveTo(x0, y);
        for (let t = 0; t <= 1; t += 0.1) g.lineTo(x0 + Math.sin(t * 6 + k) * rr(1, 4), y + t * len);
        g.stroke();
      }
      g.globalAlpha = 0.8; g.fillStyle = shade(base, -0.18); g.fillRect(p * pw, y, pw, 1.5);
      y += len;
    }
    g.globalAlpha = 0.8; g.fillStyle = shade(base, -0.2); g.fillRect(p * pw, 0, 1.5, h);
  }
  g.globalAlpha = 1;
};
const stoneDraw = (base, banded = true) => (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  if (banded) for (let i = 0; i < 70; i++) {
    g.fillStyle = shade(base, rr(-0.07, 0.05)); g.globalAlpha = rr(0.15, 0.5);
    const y = rnd() * h, bh = rr(2, 26); g.beginPath(); g.moveTo(0, y);
    for (let x = 0; x <= w; x += w / 16) g.lineTo(x, y + Math.sin(x * 0.01 + i) * 4);
    g.lineTo(w, y + bh); g.lineTo(0, y + bh); g.fill();
  }
  g.fillStyle = shade(base, -0.25);
  for (let i = 0; i < 500; i++) { g.globalAlpha = rr(0.2, 0.6); g.beginPath(); g.ellipse(rnd() * w, rnd() * h, rr(1, 7), rr(0.5, 2), 0, 0, 7); g.fill(); }
  g.globalAlpha = 1; speckle(g, w, h, 4000, '#fff', 0.15);
};
const plasterDraw = (base) => (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 160; i++) {
    const x = rnd() * w, y = rnd() * h, r = rr(30, 160);
    const gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, shade(base, rr(-0.04, 0.03))); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.globalAlpha = 0.05; g.fillStyle = gr; g.fillRect(x - r, y - r, r * 2, r * 2);
  }
  g.globalAlpha = 1; speckle(g, w, h, 6000, shade(base, -0.05), 0.12, 1.2);
};
const grainDraw = (base) => (g, w, h) => {       // vertical veneer
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 260; i++) {
    g.strokeStyle = shade(base, rr(-0.1, 0.06)); g.globalAlpha = rr(0.2, 0.6); g.lineWidth = rr(0.5, 3);
    const x0 = rnd() * w; g.beginPath(); g.moveTo(x0, 0);
    for (let y = 0; y <= h; y += h / 20) g.lineTo(x0 + Math.sin(y * 0.006 + i) * 3, y);
    g.stroke();
  }
  g.globalAlpha = 1;
};
const fabricDraw = (base, loops = true) => (g, w, h) => {
  g.fillStyle = base; g.fillRect(0, 0, w, h);
  speckle(g, w, h, loops ? 26000 : 9000, shade(base, -0.12), 0.5, loops ? 3 : 1.5);
  speckle(g, w, h, loops ? 16000 : 5000, shade(base, 0.08), 0.5, loops ? 3 : 1.5);
};

const TEX = {
  oak: canvasTex(1024, 2048, oakDraw('#6a5040'), 1, 1),
  trav: canvasTex(1024, 1024, stoneDraw('#d8c5a6'), 1, 1),
  travLight: canvasTex(1024, 1024, stoneDraw('#e4d6bf'), 1, 1),
  plaster: canvasTex(1024, 1024, plasterDraw('#ece4d7'), 1, 1),
  walnut: canvasTex(512, 1024, grainDraw('#5a3c2a'), 1, 1),
  smokedOak: canvasTex(512, 1024, grainDraw('#6b5240'), 1, 1),
  boucle: canvasTex(512, 512, fabricDraw('#ebe2d4'), 1, 1),
  linen: canvasTex(512, 512, fabricDraw('#e9e2d6', false), 1, 1),
  wool: canvasTex(512, 512, fabricDraw('#d9ccb8'), 1, 1),
  taupe: canvasTex(512, 512, fabricDraw('#8e7b6a', false), 1, 1),
};
TEX.oak.repeat.set(1 / 1.76, 1 / 3.6);   // 8 planks × 22 cm, 3.6 m texture length

function mat(o) { return new THREE.MeshStandardMaterial(o); }
function texMat(tex, rx, ry, extra = {}) {
  const t = tex.clone(); t.needsUpdate = true; t.repeat.set(rx, ry);
  return mat({ map: t, ...extra });
}
const M = {
  plaster: (rx = 1, ry = 1) => texMat(TEX.plaster, rx, ry, { roughness: 0.95 }),
  trav: (rx = 1, ry = 1) => texMat(TEX.trav, rx, ry, { roughness: 0.55 }),
  travL: (rx = 1, ry = 1) => texMat(TEX.travLight, rx, ry, { roughness: 0.5 }),
  walnut: (rx = 1, ry = 1) => texMat(TEX.walnut, rx, ry, { roughness: 0.45 }),
  smoked: (rx = 1, ry = 1) => texMat(TEX.smokedOak, rx, ry, { roughness: 0.5 }),
  boucle: () => texMat(TEX.boucle, 3, 3, { roughness: 1, bumpMap: TEX.boucle, bumpScale: 1.2 }),
  linen: () => texMat(TEX.linen, 3, 3, { roughness: 0.95 }),
  wool: (rx = 3, ry = 3) => texMat(TEX.wool, rx, ry, { roughness: 1, bumpMap: TEX.wool, bumpScale: 2 }),
  taupe: () => texMat(TEX.taupe, 3, 3, { roughness: 0.9 }),
  bronze: mat({ color: '#8a6a43', metalness: 1, roughness: 0.32 }),
  blackSteel: mat({ color: '#1d1b19', metalness: 0.8, roughness: 0.45 }),
  velvetGreen: new THREE.MeshPhysicalMaterial({ color: '#2f4a3c', roughness: 0.75, sheen: 1, sheenColor: new THREE.Color('#7fa08a'), sheenRoughness: 0.4 }),
  cognac: mat({ color: '#8a4f2c', roughness: 0.5 }),
  ceramic: mat({ color: '#e9e1d3', roughness: 0.35 }),
  glass: new THREE.MeshPhysicalMaterial({ color: '#ffffff', metalness: 0, roughness: 0.05, transmission: 0.95, transparent: true, opacity: 0.15 }),
  fluted: new THREE.MeshPhysicalMaterial({ color: '#efe9df', roughness: 0.35, transmission: 0.6, transparent: true, opacity: 0.75 }),
  sheer: new THREE.MeshStandardMaterial({ color: '#f6f1e8', roughness: 1, transparent: true, opacity: 0.55, side: THREE.DoubleSide }),
  white: mat({ color: '#f4f1ec', roughness: 0.9 }),
  shadowGap: mat({ color: '#2a2622', roughness: 1 }),
};

// ---------- scene ----------
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H); renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color('#dfe7ea');
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.45;

const add = (mesh, cast = true, recv = true) => { mesh.castShadow = cast; mesh.receiveShadow = recv; scene.add(mesh); return mesh; };
// box from plan extents: x0..x1, y0..y1 (plan), z0..z1 (height)
function box(x0, x1, y0, y1, z0, z1, material, cast = true) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, z1 - z0, y1 - y0), material);
  m.position.set((x0 + x1) / 2, (z0 + z1) / 2, -(y0 + y1) / 2);
  return add(m, cast);
}
function rbox(x0, x1, y0, y1, z0, z1, material, r = 0.04) {
  const m = new THREE.Mesh(new RoundedBoxGeometry(x1 - x0, z1 - z0, y1 - y0, 4, r), material);
  m.position.set((x0 + x1) / 2, (z0 + z1) / 2, -(y0 + y1) / 2);
  return add(m);
}
function cyl(x, y, r, z0, z1, material, seg = 64, rTop = r) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rTop, r, z1 - z0, seg), material);
  m.position.set(x, (z0 + z1) / 2, -y); return add(m);
}

// Wall along an axis with openings [{a, b, z0, z1}] (a/b along the wall).
function wall(axis, fixed, from, to, openings = [], material, glass = true) {
  const segs = [];
  const ops = [...openings].sort((p, q) => p.a - q.a);
  let cur = from;
  for (const o of ops) {
    if (o.a > cur) segs.push([cur, o.a, 0, CH]);
    if (o.z0 > 0) segs.push([o.a, o.b, 0, o.z0]);
    if (o.z1 < CH) segs.push([o.a, o.b, o.z1, CH]);
    cur = o.b;
  }
  if (cur < to) segs.push([cur, to, 0, CH]);
  const mk = (a, b, z0, z1) => axis === 'x'
    ? box(a, b, fixed - T, fixed, z0, z1, material)       // wall running east-west; fixed = y of inner face (room south of it) — see callers
    : box(fixed - T, fixed, a, b, z0, z1, material);
  segs.forEach(s => mk(...s));
  if (glass) for (const o of ops) if (o.glass !== false) {
    const mid = fixed - T / 2;
    if (axis === 'x') { box(o.a, o.b, mid - 0.01, mid + 0.01, o.z0, o.z1, M.glass, false);
      box(o.a, o.a + 0.05, mid - 0.04, mid + 0.04, o.z0, o.z1, M.blackSteel); box(o.b - 0.05, o.b, mid - 0.04, mid + 0.04, o.z0, o.z1, M.blackSteel);
      box(o.a, o.b, mid - 0.04, mid + 0.04, o.z1 - 0.05, o.z1, M.blackSteel); box(o.a, o.b, mid - 0.04, mid + 0.04, o.z0, o.z0 + 0.04, M.blackSteel);
      if (o.mullions) for (let i = 1; i < o.mullions; i++) { const xm = o.a + (o.b - o.a) * i / o.mullions; box(xm - 0.025, xm + 0.025, mid - 0.04, mid + 0.04, o.z0, o.z1, M.blackSteel); }
    } else { box(mid - 0.01, mid + 0.01, o.a, o.b, o.z0, o.z1, M.glass, false);
      box(mid - 0.04, mid + 0.04, o.a, o.a + 0.05, o.z0, o.z1, M.blackSteel); box(mid - 0.04, mid + 0.04, o.b - 0.05, o.b, o.z0, o.z1, M.blackSteel);
      box(mid - 0.04, mid + 0.04, o.a, o.b, o.z1 - 0.05, o.z1, M.blackSteel); box(mid - 0.04, mid + 0.04, o.a, o.b, o.z0, o.z0 + 0.04, M.blackSteel); }
  }
}
// helpers: walls with explicit thickness side
const wallX = (y, inside, x0, x1, ops, m) => wall('x', inside === 'south' ? y + T : y, x0, x1, ops, m);   // inside='south' → wall sits north of y
const wallY = (x, inside, y0, y1, ops, m) => wall('y', inside === 'west' ? x + T : x, y0, y1, ops, m);

// ---------- architecture (as supplied) ----------
const SAL = { xE: 11.51, yN: 4.25, xStair: 7.60, yStair: 2.69 };
// floor (smoked oak, wide plank) for salon + guest room + hall
{
  const f = new THREE.Mesh(new THREE.PlaneGeometry(12, 9.2), mat({ map: TEX.oak, roughness: 0.55 }));
  f.rotation.x = -Math.PI / 2; f.position.set(5.75, 0, -4.4); add(f, false, true);
  TEX.oak.repeat.set(12 / 1.76, 9.2 / 3.6); TEX.oak.rotation = Math.PI / 2;
}
// honed travertine threshold inlay at the entrance
box(3.67, 6.35, 0, 0.55, 0, 0.004, M.travL(2, 0.5), false);
// exterior ground + garden hint
{
  const g = new THREE.Mesh(new THREE.PlaneGeometry(60, 30), mat({ color: '#b9b29f', roughness: 1 }));
  g.rotation.x = -Math.PI / 2; g.position.set(5, -0.02, 15.2); add(g, false, true);
  const hedge = mat({ color: '#56664a', roughness: 1 });
  for (let i = 0; i < 9; i++) rbox(-2 + i * 1.8, -0.4 + i * 1.8, -6.5, -5.6, 0, rr(1.0, 1.6), hedge, 0.3);
  for (let i = 0; i < 5; i++) cyl(rr(-1, 12), rr(-9, -7), rr(0.15, 0.25), 0, 4, mat({ color: '#6c5a48' }));
  const wl = mat({ color: '#d6cdbc', roughness: 1 });
  box(-6, 18, -12, -11.5, 0, 2.2, wl);
}
// Salon: west wall (two narrow corner windows)
wallY(0, 'east', 0, SAL.yN, [{ a: 0.03, b: 0.70, z0: 0.5, z1: 2.4 }, { a: 3.57, b: 4.23, z0: 0.5, z1: 2.4 }], M.plaster(2, 1.2));
// south wall: glazed entrance (3.67–6.35) + two windows
wallX(0, 'north', -T, SAL.xE + T, [
  { a: 3.67, b: 6.35, z0: 0, z1: 2.5, mullions: 3 },
  { a: 6.35 + 0.0001, b: 7.05, z0: 0.6, z1: 2.5 },
  { a: 8.24, b: 9.36, z0: 0.6, z1: 2.5, mullions: 2 }], M.plaster(4, 1.2));
// east wall of salon
wallY(SAL.xE, 'west', 0, SAL.yStair, [], M.plaster(1, 1));
// corner column / duct (existing)
box(11.22, SAL.xE, 0, 0.32, 0, CH, M.plaster(0.3, 1));
// north wall of salon: 0 → 6.56 with the 2.07 m glazed opening
wallX(SAL.yN, 'south', -T, 6.56, [{ a: 3.77, b: 5.86, z0: 0.0, z1: 2.4, glass: false }], M.plaster(3, 1.2));
// fluted glass + bronze frame in the existing 2.07 m opening
box(3.77, 5.86, SAL.yN + 0.09, SAL.yN + 0.11, 0, 2.4, M.fluted, false);
for (let i = 0; i <= 6; i++) { const x = 3.77 + i * (2.09 / 6); box(x - 0.02, x + 0.02, SAL.yN + 0.07, SAL.yN + 0.13, 0, 2.4, M.bronze); }
box(3.77, 5.86, SAL.yN + 0.07, SAL.yN + 0.13, 2.36, 2.4, M.bronze);
// stub at 6.56–6.72 down to y 3.83
box(6.56, 6.72, 3.83, SAL.yN + T, 0, CH, M.plaster(0.2, 1));
// stair enclosure walls (west face x 7.60, south face y 2.69)
box(SAL.xStair, SAL.xStair + 0.2, SAL.yStair, 4.6, 0, CH, M.plaster(1, 1));
box(SAL.xStair, SAL.xE, SAL.yStair, SAL.yStair + 0.2, 0, CH, M.plaster(2, 1));
// hall beyond passage (dimmer)
box(6.3, 6.5, 4.4, 5.9, 0, CH, M.plaster(1, 1));
// ceiling (lime plaster) with shadow-gap cove
box(-0.3, 12, -0.3, 9.2, CH, CH + 0.2, M.white);

// ---------- Guest bedroom architecture ----------
const GB = { x0: 8.36, x1: 11.51, y0: 5.49, y1: 8.71 };
wallX(GB.y0, 'north', GB.x0 - T, GB.x1 + T, [], M.plaster(2, 1));             // south (headboard) wall
wallX(GB.y1, 'south', GB.x0 - T, GB.x1 + T, [], M.plaster(2, 1));             // north wall
wallY(GB.x1, 'west', GB.y0, GB.y1, [{ a: 7.19, b: 8.40, z0: 0.8, z1: 2.4 }], M.plaster(2, 1));  // east wall + window
wallY(GB.x0, 'east', GB.y0, GB.y1, [{ a: 6.10, b: 7.41, z0: 0, z1: 2.25, glass: false }], M.plaster(2, 1)); // west wall + door
// door leaf (smoked oak, flush, bronze pull) — closed
box(GB.x0 - 0.12, GB.x0 - 0.07, 6.40, 7.32, 0, 2.25, M.smoked(1, 2));
box(GB.x0 - 0.06, GB.x0 - 0.04, 6.50, 6.52, 0.8, 1.4, M.bronze);

// ================= FURNITURE — SALON =================
// 1 Travertine fire wall (x 0–0.40, y 0.72–3.52)
box(0, 0.40, 0.72, 3.52, 0, CH, M.trav(1.5, 1.5));
box(0.30, 0.41, 1.32, 2.92, 0.35, 0.72, mat({ color: '#141210', roughness: 1 }));    // fire box
{ const flame = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 0.16), new THREE.MeshBasicMaterial({ color: '#ffb066' }));
  flame.rotation.y = Math.PI / 2; flame.position.set(0.36, 0.44, -2.12); scene.add(flame);
  const fl = new THREE.PointLight('#ff9a4a', 2.2, 4, 2); fl.position.set(0.6, 0.5, -2.12); scene.add(fl); }
box(0.40, 0.70, 0.72, 3.52, 0, 0.30, M.trav(1.5, 0.3));                              // low travertine hearth bench
box(0.38, 0.41, 1.22, 3.02, 1.12, 2.02, mat({ color: '#111', roughness: 0.25, metalness: 0.2 })); // hidden TV (flush, art mode)
{ const a = canvasArtMat(); a.emissive = new THREE.Color('#ffffff'); a.emissiveMap = a.map; a.emissiveIntensity = 0.35;
  const sc = new THREE.Mesh(new THREE.PlaneGeometry(1.78, 0.88), a); sc.rotation.y = Math.PI / 2; sc.position.set(0.415, 1.57, -2.12); scene.add(sc); }
box(0.38, 0.40, 1.18, 3.06, 1.08, 1.12, M.bronze); box(0.38, 0.40, 1.18, 3.06, 2.02, 2.06, M.bronze);
// objects on the hearth
cyl(0.55, 3.2, 0.12, 0.30, 0.62, M.ceramic, 48, 0.07);
cyl(0.55, 0.95, 0.09, 0.30, 0.42, mat({ color: '#3b3029', roughness: 0.6 }));

// Rug (x 0.50–3.50, y 0.42–3.82)
box(0.5, 3.5, 0.42, 3.82, 0, 0.015, M.wool(4, 4), false).material.color.set('#cdbba0');

// 2 Curved bouclé sofa (concave toward the fire)
{
  const C = new THREE.Vector2(-1.09, 2.12), R = 3.39, ang = Math.asin(1.5 / R) * 1.06;
  const sector = (r0, r1, a) => {
    const s = new THREE.Shape();
    s.absarc(C.x, C.y, r1, -a, a, false); s.absarc(C.x, C.y, r0, a, -a, true); return s;
  };
  const ext = (shape, z0, z1, m, bevel = 0.05) => {
    const g = new THREE.ExtrudeGeometry(shape, { depth: z1 - z0 - bevel * 2, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 5, curveSegments: 96 });
    const mesh = new THREE.Mesh(g, m); mesh.rotation.x = -Math.PI / 2; mesh.position.y = z0 + bevel; return add(mesh);
  };
  const B = M.boucle();
  ext(sector(R + 0.04, R + 0.96, ang), 0.0, 0.10, mat({ color: '#2b2622' }), 0.0);     // recessed plinth shadow
  ext(sector(R, R + 1.0, ang), 0.10, 0.30, B, 0.04);                                     // base
  ext(sector(R + 0.02, R + 0.74, ang * 0.98), 0.30, 0.44, B, 0.06);                      // seat cushion
  ext(sector(R + 0.70, R + 1.0, ang), 0.30, 0.78, B, 0.08);                               // back
  // scatter cushions
  [[-0.55, '#a8774f'], [-0.15, '#e7dccb'], [0.45, '#3d5246']].forEach(([t, col]) => {
    const a = t * ang, r = R + 0.62; const p = new THREE.Mesh(new RoundedBoxGeometry(0.5, 0.45, 0.16, 4, 0.07), mat({ color: col, roughness: 0.95 }));
    p.position.set(C.x + r * Math.cos(a), 0.62, -(C.y + r * Math.sin(a)));
    p.rotation.y = Math.PI / 2 - a; p.rotation.x = 0; add(p);
  });
}
// 3 Oval travertine coffee table on a sculpted base
{
  const top = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.06, 96), M.trav(1, 1));
  top.scale.set(0.34, 1, 0.76); top.position.set(1.52, 0.31, -2.12); add(top);
  const base = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 0.28, 96), M.trav(1, 1));
  base.scale.set(0.2, 1, 0.5); base.position.set(1.52, 0.14, -2.12); add(base);
  rbox(1.40, 1.66, 1.80, 2.05, 0.34, 0.39, mat({ color: '#2f2924', roughness: 0.5 }), 0.01);     // books
  rbox(1.42, 1.64, 1.82, 2.03, 0.39, 0.42, mat({ color: '#c9b79a', roughness: 0.8 }), 0.01);
  cyl(1.55, 2.45, 0.08, 0.34, 0.50, M.bronze, 48, 0.05);
}
// 4 Swivel lounge chairs (cognac leather shell, bouclé seat)
function swivel(x, y, faceDeg, shellMat, seatMat) {
  const grp = new THREE.Group();
  const seat = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.36, 0.16, 64), seatMat); seat.position.y = 0.36; grp.add(seat);
  const shell = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.42, 64, 1, true, Math.PI * 0.35, Math.PI * 1.3), shellMat);
  shell.material.side = THREE.DoubleSide; shell.position.y = 0.56; grp.add(shell);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(0.40, 0.04, 16, 64, Math.PI * 1.3), shellMat);
  rim.rotation.x = Math.PI / 2; rim.rotation.z = Math.PI * 0.85 - Math.PI * 0.5; rim.position.y = 0.77; grp.add(rim);
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.26, 0.28, 48), M.bronze); base.position.y = 0.14; grp.add(base);
  grp.position.set(x, 0, -y); grp.rotation.y = THREE.MathUtils.degToRad(faceDeg);
  grp.traverse(o => { if (o.isMesh) { o.castShadow = o.receiveShadow = true; } }); scene.add(grp);
}
swivel(1.50, 0.58, -60, mat({ color: '#8a4f2c', roughness: 0.5, side: THREE.DoubleSide }), M.boucle());
swivel(1.50, 3.66, 60, mat({ color: '#8a4f2c', roughness: 0.5, side: THREE.DoubleSide }), M.boucle());
// 5 Walnut console behind sofa + lamp
box(3.30, 3.65, 1.12, 3.12, 0.06, 0.74, M.walnut(1, 1));
box(3.33, 3.62, 1.15, 3.09, 0, 0.06, M.shadowGap);
cyl(3.47, 2.75, 0.10, 0.74, 1.10, M.ceramic, 48, 0.06);
cyl(3.47, 2.75, 0.20, 1.10, 1.38, mat({ color: '#f1e7d4', roughness: 1, emissive: '#ffcf96', emissiveIntensity: 0.6, side: THREE.DoubleSide }), 48, 0.17);
{ const l = new THREE.PointLight('#ffc98a', 2.5, 5, 2); l.position.set(3.47, 1.2, -2.75); scene.add(l); }
rbox(3.36, 3.58, 1.4, 1.75, 0.74, 0.80, mat({ color: '#3a302a' }), 0.01);
cyl(3.47, 2.0, 0.07, 0.74, 1.05, mat({ color: '#2e2924', roughness: 0.4 }), 48, 0.03);

// 7 Sculptural bronze pendant (ring Ø1.2) over the gallery zone
{
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.6, 0.035, 24, 128), M.bronze);
  ring.rotation.x = Math.PI / 2; ring.position.set(4.9, 2.2, -2.3); add(ring, false);
  const glow = new THREE.Mesh(new THREE.TorusGeometry(0.6, 0.012, 12, 128), new THREE.MeshBasicMaterial({ color: '#ffd9a6' }));
  glow.rotation.x = Math.PI / 2; glow.position.set(4.9, 2.165, -2.3); scene.add(glow);
  for (const a of [0, 2.1, 4.2]) box(4.9 + 0.6 * Math.cos(a) - 0.003, 4.9 + 0.6 * Math.cos(a) + 0.003, 2.3 + 0.6 * Math.sin(a) - 0.003, 2.3 + 0.6 * Math.sin(a) + 0.003, 2.2, CH, M.bronze, false);
  const l = new THREE.PointLight('#ffcf96', 3, 6, 2); l.position.set(4.9, 2.0, -2.3); scene.add(l);
}
// 8 Travertine plinth + bronze sculpture (x 6.03–6.45, y 3.78–4.20)
box(6.03, 6.45, 3.78, 4.20, 0, 0.9, M.trav(0.5, 1));
{ const s = new THREE.Mesh(new THREE.TorusKnotGeometry(0.16, 0.045, 160, 24, 2, 3), mat({ color: '#2b241f', metalness: 0.7, roughness: 0.4 }));
  s.position.set(6.24, 1.18, -3.99); add(s); }
// Large art piece on the north wall (left)
box(1.0, 2.7, SAL.yN - 0.06, SAL.yN - 0.03, 1.1, 2.25, canvasArtMat(), true);
function canvasArtMat() {
  const t = canvasTex(1024, 700, (g, w, h) => {
    g.fillStyle = '#e8dfd0'; g.fillRect(0, 0, w, h);
    g.fillStyle = '#b48a62'; g.globalAlpha = 0.85; g.beginPath(); g.arc(w * 0.38, h * 0.55, h * 0.32, 0, 7); g.fill();
    g.fillStyle = '#3f5246'; g.globalAlpha = 0.9; g.fillRect(w * 0.55, h * 0.18, w * 0.18, h * 0.66);
    g.fillStyle = '#2b2622'; g.globalAlpha = 0.8; g.fillRect(w * 0.12, h * 0.78, w * 0.7, 6);
    g.globalAlpha = 1; speckle(g, w, h, 8000, '#000', 0.08, 2);
  });
  return mat({ map: t, roughness: 0.9 });
}
box(0.98, 2.72, SAL.yN - 0.03, SAL.yN, 1.08, 2.27, M.bronze);

// Sheer linen curtains at the south glazing
for (const [a, b] of [[3.55, 3.95], [6.25, 6.55], [7.05, 7.35], [8.05, 8.35], [9.36, 9.66]]) {
  const g = new THREE.PlaneGeometry(b - a, CH - 0.1, 24, 1);
  const pos = g.attributes.position; for (let i = 0; i < pos.count; i++) pos.setZ(i, Math.sin(pos.getX(i) * 40) * 0.025);
  const m = new THREE.Mesh(g, M.sheer); m.position.set((a + b) / 2, (CH - 0.1) / 2, -0.12); add(m, false, true);
}
box(3.4, 9.8, 0.08, 0.16, CH - 0.06, CH - 0.02, M.bronze, false);   // ceiling-recessed curtain track

// 9 Walnut library wall with bronze bar niche
{
  const xa = SAL.xStair + 0.2, xb = SAL.xE, y1 = SAL.yStair, y0 = y1 - 0.40;
  // north run
  box(xa, xb, y0, y1, 0, 0.08, M.shadowGap);
  box(xa, xb, y0 + 0.02, y1, 0.08, 0.86, M.walnut(6, 1));                       // closed base
  for (let x = xa + 0.6; x < xb - 0.1; x += 0.6) box(x - 0.003, x + 0.003, y0 + 0.015, y0 + 0.02, 0.1, 0.84, M.shadowGap, false);
  box(xa, xb, y1 - 0.02, y1, 0.86, CH, M.walnut(6, 2));                             // back panel
  const verts = [xa, 8.55, 9.40, 10.55, xb - 0.42];
  verts.forEach(x => box(x, x + 0.03, y0 + 0.04, y1, 0.86, CH, M.walnut(0.1, 2)));
  for (let z = 0.86; z < CH - 0.2; z += 0.38) {
    box(xa, xb - 0.42, y0 + 0.04, y1, z, z + 0.025, M.walnut(6, 0.1));
    const strip = new THREE.Mesh(new THREE.BoxGeometry(xb - 0.42 - xa, 0.006, 0.01), new THREE.MeshBasicMaterial({ color: '#ffd7a0' }));
    strip.position.set((xa + xb - 0.42) / 2, z + 0.37, -(y0 + 0.08)); scene.add(strip);
  }
  // bronze bar niche (9.43–10.55)
  box(9.43, 10.55, y1 - 0.025, y1 - 0.02, 0.86, 2.0, M.bronze);
  box(9.43, 10.55, y0 + 0.04, y1, 1.0, 1.02, mat({ color: '#d8cbb4', roughness: 0.3 }));
  for (let i = 0; i < 6; i++) cyl(9.6 + i * 0.17, y1 - 0.15, 0.035, 1.02, 1.32, mat({ color: ['#3a2a1a', '#6b3a1e', '#cfd8c8', '#2e3b2c'][i % 4], roughness: 0.15, metalness: 0.1 }), 24);
  for (let i = 0; i < 4; i++) cyl(9.7 + i * 0.22, y1 - 0.15, 0.035, 1.42, 1.52, M.glass, 24);
  // books & objects
  const bookCols = ['#e3d9c6', '#c2a882', '#5d4636', '#2f2a26', '#8c6d50', '#d6c8b0', '#47584a', '#a5876a'];
  for (let z = 0.885; z < CH - 0.4; z += 0.38) {
    for (let x = xa + 0.06; x < xb - 0.5;) {
      if (x > 9.40 && x < 10.58) { x = 10.6; continue; }
      if (rnd() < 0.18) { cyl(x + 0.1, y1 - 0.2, 0.08, z, z + rr(0.14, 0.28), M.ceramic, 32, 0.05); x += 0.35; continue; }
      const n = Math.floor(rr(4, 12));
      for (let i = 0; i < n && x < xb - 0.5; i++) { const t = rr(0.025, 0.045), hgt = rr(0.2, 0.31);
        box(x, x + t, y1 - 0.25, y1 - 0.03, z, z + hgt, mat({ color: bookCols[Math.floor(rnd() * 8)], roughness: 0.85 })); x += t + 0.002; }
      x += rr(0.15, 0.35);
    }
  }
  // east run (x 11.11–11.51, y 0.32–2.29), closed fluted doors
  box(SAL.xE - 0.40, SAL.xE, 0.32, y0, 0, 0.08, M.shadowGap);
  box(SAL.xE - 0.40, SAL.xE, 0.32, y0, 0.08, CH, M.walnut(1, 3));
  for (let y = 0.36; y < y0; y += 0.05) box(SAL.xE - 0.405, SAL.xE - 0.395, y, y + 0.02, 0.1, CH - 0.02, M.walnut(0.1, 3), false);
}
// 10 Green velvet lounge chairs + travertine side table + arc floor lamp
function loungeChair(x, y, faceDeg) {
  const g = new THREE.Group(), V = M.velvetGreen;
  const parts = [
    [new RoundedBoxGeometry(0.80, 0.30, 0.80, 5, 0.12), 0, 0.27, 0],
    [new RoundedBoxGeometry(0.62, 0.14, 0.62, 5, 0.06), 0, 0.46, 0.06],
    [new RoundedBoxGeometry(0.80, 0.50, 0.20, 5, 0.09), 0, 0.62, -0.30],
    [new RoundedBoxGeometry(0.16, 0.30, 0.70, 5, 0.07), -0.36, 0.55, 0.0],
    [new RoundedBoxGeometry(0.16, 0.30, 0.70, 5, 0.07), 0.36, 0.55, 0.0],
  ];
  parts.forEach(([geo, px, py, pz]) => { const m = new THREE.Mesh(geo, V); m.position.set(px, py, pz); g.add(m); });
  [[-0.3, -0.3], [0.3, -0.3], [-0.3, 0.3], [0.3, 0.3]].forEach(([a, b]) => { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.018, 0.12, 12), M.bronze); l.position.set(a, 0.06, b); g.add(l); });
  g.position.set(x, 0, -y); g.rotation.y = THREE.MathUtils.degToRad(faceDeg);
  g.traverse(o => { if (o.isMesh) o.castShadow = o.receiveShadow = true; }); scene.add(g);
}
box(8.3, 11.0, 0.15, 1.75, 0, 0.012, M.wool(3, 2), false);
loungeChair(8.95, 0.82, 60);
loungeChair(10.35, 0.82, -60);
cyl(9.65, 0.70, 0.25, 0, 0.48, M.trav(0.5, 0.5), 64, 0.25);
cyl(9.65, 0.70, 0.06, 0.48, 0.66, mat({ color: '#2f2924', roughness: 0.4 }), 32, 0.03);
{
  cyl(10.95, 1.75, 0.16, 0, 0.04, M.trav(0.3, 0.3));
  const curve = new THREE.QuadraticBezierCurve3(new THREE.Vector3(10.95, 0.04, -1.75), new THREE.Vector3(10.95, 2.4, -1.75), new THREE.Vector3(10.0, 1.95, -1.1));
  add(new THREE.Mesh(new THREE.TubeGeometry(curve, 48, 0.012, 8), M.bronze));
  cyl(10.0, 1.1, 0.16, 1.80, 1.95, mat({ color: '#8a6a43', metalness: 1, roughness: 0.3, side: THREE.DoubleSide }), 48, 0.05);
  const l = new THREE.SpotLight('#ffcf96', 6, 4, 0.9, 0.6, 2); l.position.set(10.0, 1.78, -1.1); l.target.position.set(9.9, 0, -0.9);
  scene.add(l, l.target);
}

// ================= FURNITURE — GUEST BEDROOM =================
{
  const { x0, x1, y0, y1 } = GB;
  // 11 Upholstered channel headboard wall (taupe), full width, 1.35 high
  for (let x = x0; x < x1 - 0.01; x += 0.15) rbox(x + 0.003, Math.min(x + 0.15, x1) - 0.003, y0, y0 + 0.08, 0, 1.35, M.taupe(), 0.03);
  box(x0, x1, y0, y0 + 0.09, 1.35, 1.38, M.bronze);
  // wall sconces
  for (const x of [8.80, 11.05]) {
    box(x - 0.06, x + 0.06, y0 + 0.08, y0 + 0.11, 1.55, 1.70, M.bronze);
    cyl(x, y0 + 0.2, 0.07, 1.48, 1.62, mat({ color: '#f3e8d6', emissive: '#ffcf96', emissiveIntensity: 1.2 }), 32, 0.05);
    const l = new THREE.PointLight('#ffc98a', 1.6, 3.5, 2); l.position.set(x, 1.45, -(y0 + 0.3)); scene.add(l);
  }
  // art above headboard
  box(9.45, 10.45, y0 + 0.09, y0 + 0.12, 1.65, 2.35, canvasArtMat());
  // rug
  box(8.72, 11.12, 6.00, 8.00, 0, 0.012, M.wool(3, 3), false);
  // 12 Bed 160 × 200 on smoked oak platform (frame 170 × 210)
  box(9.07, 10.77, y0 + 0.09, y0 + 2.19, 0.06, 0.30, M.smoked(2, 2));
  box(9.12, 10.72, y0 + 0.14, y0 + 2.14, 0, 0.06, M.shadowGap);
  rbox(9.12, 10.72, y0 + 0.12, y0 + 2.12, 0.30, 0.55, M.linen(), 0.05);                  // mattress
  rbox(9.10, 10.74, y0 + 0.75, y0 + 2.16, 0.48, 0.60, mat({ color: '#f2ede4', roughness: 1 }), 0.05); // duvet
  rbox(9.08, 10.76, y0 + 1.55, y0 + 2.00, 0.55, 0.63, mat({ color: '#8a4f2c', roughness: 0.95 }), 0.04); // cognac throw
  for (const x of [9.50, 10.34]) rbox(x - 0.35, x + 0.35, y0 + 0.15, y0 + 0.30, 0.55, 0.95, mat({ color: '#f4f0e9', roughness: 1 }), 0.07);
  for (const x of [9.55, 10.29]) rbox(x - 0.25, x + 0.25, y0 + 0.30, y0 + 0.44, 0.58, 0.88, mat({ color: '#d9ccb6', roughness: 1 }), 0.06);
  rbox(9.66, 10.18, y0 + 0.44, y0 + 0.58, 0.60, 0.82, M.velvetGreen, 0.06);
  // 13 Floating oak nightstands
  for (const xa of [8.57, 10.82]) {
    box(xa, xa + 0.45, y0 + 0.09, y0 + 0.49, 0.38, 0.56, M.smoked(1, 0.5));
    box(xa + 0.02, xa + 0.43, y0 + 0.10, y0 + 0.47, 0.36, 0.38, M.shadowGap);
  }
  rbox(8.65, 8.85, 5.75, 5.90, 0.56, 0.60, mat({ color: '#2f2924' }), 0.01);
  cyl(11.0, 5.75, 0.06, 0.56, 0.80, M.ceramic, 32, 0.04);
  // 14 Existing wardrobe, refaced: fluted smoked oak, full height
  box(x0, x0 + 0.65, 7.41, y1, 0, 0.06, M.shadowGap);
  box(x0, x0 + 0.63, 7.41, y1, 0.06, CH - 0.02, M.smoked(1, 3));
  for (let y = 7.45; y < y1 - 0.02; y += 0.045) box(x0 + 0.63, x0 + 0.645, y, y + 0.022, 0.08, CH - 0.04, M.smoked(0.1, 3), false);
  box(x0 + 0.645, x0 + 0.66, 8.05, 8.07, 0.9, 1.5, M.bronze);
  // 15 Writing desk / vanity under the east window + chair
  box(x1 - 0.50, x1, 7.25, 8.35, 0.72, 0.75, M.walnut(1, 1));
  box(x1 - 0.48, x1 - 0.45, 7.27, 7.30, 0, 0.72, M.bronze); box(x1 - 0.48, x1 - 0.45, 8.30, 8.33, 0, 0.72, M.bronze);
  cyl(x1 - 0.22, 8.15, 0.07, 0.75, 1.05, M.ceramic, 32, 0.05);
  { const l = new THREE.PointLight('#ffc98a', 1.2, 3, 2); l.position.set(x1 - 0.22, 1.15, -8.15); scene.add(l); }
  const ch = new THREE.Group();
  const seat = new THREE.Mesh(new RoundedBoxGeometry(0.46, 0.08, 0.46, 4, 0.03), M.velvetGreen); seat.position.y = 0.46; ch.add(seat);
  const back = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.26, 48, 1, true, Math.PI * 0.6, Math.PI * 0.8), M.velvetGreen);
  back.material.side = THREE.DoubleSide; back.position.set(0, 0.68, 0); ch.add(back);
  [[-0.18, -0.18], [0.18, -0.18], [-0.18, 0.18], [0.18, 0.18]].forEach(([a, b]) => { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.012, 0.42, 10), M.bronze); l.position.set(a, 0.21, b); ch.add(l); });
  ch.position.set(10.70, 0, -7.80); ch.rotation.y = -Math.PI / 2; ch.traverse(o => { if (o.isMesh) o.castShadow = o.receiveShadow = true; }); scene.add(ch);
  // sheer at the east window
  const g = new THREE.PlaneGeometry(0.5, 2.5, 20, 1); const pos = g.attributes.position;
  for (let i = 0; i < pos.count; i++) pos.setZ(i, Math.sin(pos.getX(i) * 40) * 0.02);
  const cur = new THREE.Mesh(g, M.sheer); cur.rotation.y = -Math.PI / 2; cur.position.set(x1 - 0.06, 1.3, -6.95); add(cur, false);
  // pendant-free ceiling: two deep-recessed wall-washers
  for (const x of [9.3, 10.6]) { const s = new THREE.SpotLight('#ffd4a0', 4, 4, 0.5, 0.7, 2); s.position.set(x, CH - 0.05, -(y0 + 0.5)); s.target.position.set(x, 0.6, -(y0 + 0.05)); scene.add(s, s.target); }
}

// ---------- daylight ----------
const sun = new THREE.DirectionalLight('#ffe6c4', VIEW === 'guest' ? 3.2 : 4.0);
if (VIEW === 'guest') sun.position.set(20, 9, -5.5); else sun.position.set(-3, 8.5, 12);
sun.target.position.set(VIEW === 'guest' ? 10 : 5, 0, VIEW === 'guest' ? -7 : -1.5);
sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02;
Object.assign(sun.shadow.camera, { left: -9, right: 9, top: 9, bottom: -9, near: 1, far: 40 });
scene.add(sun, sun.target);
scene.add(new THREE.HemisphereLight('#f4ede2', '#9c8670', 0.55));
// soft daylight bounce from the glazing (area-like fill)
for (const [x, y, z] of [[5.0, 1.5, -0.6], [8.8, 1.5, -0.6], [1.0, 1.5, -3.9], [11.0, 1.6, -7.8]]) {
  const l = new THREE.PointLight('#fff1dd', 2.2, 7, 1.6); l.position.set(x, y, z); scene.add(l);
}
// recessed ceiling washers along the fire wall and library
for (const [x, y, tx, ty] of [[0.9, 1.2, 0.4, 1.2], [0.9, 3.0, 0.4, 3.0], [8.3, 2.0, 8.3, 2.6], [9.9, 2.0, 9.9, 2.6], [11.0, 1.9, 11.0, 2.6]]) {
  const s = new THREE.SpotLight('#ffd4a0', 5, 5, 0.45, 0.8, 2); s.position.set(x, CH - 0.05, -y); s.target.position.set(tx, 0.8, -ty); scene.add(s, s.target);
}

// ---------- cameras ----------
const VIEWS = {
  'salon-hero':    { pos: [6.9, 1.35, -0.75], look: [0.4, 1.1, -2.3], fov: 62 },
  'salon-reverse': { pos: [0.75, 1.5, -0.45], look: [8.6, 1.0, -2.7], fov: 64 },
  'library':       { pos: [7.0, 1.30, -0.45], look: [10.6, 1.15, -2.2], fov: 60 },
  'guest':         { pos: [9.85, 1.5, -8.6], look: [9.95, 0.85, -5.6], fov: 70 },
};
const v = VIEWS[VIEW];
const camera = new THREE.PerspectiveCamera(v.fov, W / H, 0.05, 100);
camera.position.set(...v.pos); camera.lookAt(...v.look);

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
try {
  const ao = new GTAOPass(scene, camera, W, H);
  ao.updateGtaoMaterial({ radius: 0.35, distanceExponent: 1.5, thickness: 1, scale: 1.2, samples: 16 });
  ao.blendIntensity = 0.85;
  composer.addPass(ao);
} catch (e) { console.warn('AO disabled', e); }
composer.addPass(new OutputPass());
composer.render();
window.__done = true;
