// KAÏRA — Console « LIGNE » : mur habillé + console, à côté d'une porte.
// Unités : mètres. Le mur de console va de x = 0 (côté porte) à x = WALL (angle).
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const q = new URLSearchParams(location.search);
const VIEW = q.get('view') || 'front';
const W = 1600, H = 1100;
const WALL = +(q.get('wall') || 1.40);   // largeur du petit mur (hypothèse)
const CH = 2.8, CLAD = 0.06;             // hauteur sous plafond, épaisseur habillage

let seed = 11; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647); const rr = (a, b) => a + (b - a) * rnd();
const shade = (h, k) => { const c = new THREE.Color(h); c.offsetHSL(0, 0, k); return '#' + c.getHexString(); };
function tex(w, h, draw, rx = 1, ry = 1) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rx, ry); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
const grain = base => (g, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 220; i++) { g.strokeStyle = shade(base, rr(-0.09, 0.05)); g.globalAlpha = rr(0.2, 0.6); g.lineWidth = rr(0.5, 2.5);
    const x0 = rnd() * w; g.beginPath(); g.moveTo(x0, 0); for (let y = 0; y <= h; y += h / 20) g.lineTo(x0 + Math.sin(y * 0.006 + i) * 3, y); g.stroke(); } g.globalAlpha = 1; };
const stone = base => (g, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 60; i++) { g.fillStyle = shade(base, rr(-0.06, 0.05)); g.globalAlpha = rr(0.15, 0.45); const y = rnd() * h; g.fillRect(0, y, w, rr(2, 22)); }
  g.fillStyle = shade(base, -0.25); for (let i = 0; i < 450; i++) { g.globalAlpha = rr(0.2, 0.6); g.beginPath(); g.ellipse(rnd() * w, rnd() * h, rr(1, 7), rr(0.5, 2), 0, 0, 7); g.fill(); } g.globalAlpha = 1; };
const plaster = base => (g, w, h) => { g.fillStyle = base; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 9000; i++) { g.fillStyle = shade(base, rr(-0.05, 0.03)); g.globalAlpha = 0.12; g.fillRect(rnd() * w, rnd() * h, 2, 2); } g.globalAlpha = 1; };
const oakFloor = base => (g, w, h) => { const n = 6, pw = w / n;
  for (let p = 0; p < n; p++) { let y = -rr(0, h); while (y < h) { const L = rr(h * 0.5, h * 0.9); g.fillStyle = shade(base, rr(-0.025, 0.025)); g.fillRect(p * pw, y, pw, L);
    for (let k = 0; k < 20; k++) { g.strokeStyle = shade(base, rr(-0.1, 0.02)); g.globalAlpha = rr(0.15, 0.4); g.beginPath(); const x0 = p * pw + rr(2, pw - 2); g.moveTo(x0, y); g.lineTo(x0 + rr(-3, 3), y + L); g.stroke(); }
    g.globalAlpha = 0.8; g.fillStyle = shade(base, -0.2); g.fillRect(p * pw, y, pw, 1.5); y += L; } g.fillRect(p * pw, 0, 1.5, h); } g.globalAlpha = 1; };

const T = { walnut: tex(512, 1024, grain('#5a3c2a')), trav: tex(1024, 1024, stone('#d8c5a6')), plaster: tex(1024, 1024, plaster('#ece4d7'), 2, 2),
  oak: tex(1024, 2048, oakFloor('#6a5040'), 3, 1.5), smoked: tex(512, 1024, grain('#6b5240')) };
const M = {
  walnut: (rx = 1, ry = 1) => { const t = T.walnut.clone(); t.needsUpdate = true; t.repeat.set(rx, ry); return new THREE.MeshStandardMaterial({ map: t, roughness: 0.45 }); },
  trav: (rx = 1, ry = 1) => { const t = T.trav.clone(); t.needsUpdate = true; t.repeat.set(rx, ry); return new THREE.MeshStandardMaterial({ map: t, roughness: 0.5 }); },
  plaster: new THREE.MeshStandardMaterial({ map: T.plaster, roughness: 0.95 }),
  smoked: new THREE.MeshStandardMaterial({ map: T.smoked, roughness: 0.5 }),
  bronze: new THREE.MeshStandardMaterial({ color: '#8a6a43', metalness: 1, roughness: 0.3 }),
  mirror: new THREE.MeshStandardMaterial({ color: '#e2cfb2', metalness: 1, roughness: 0.14, envMapIntensity: 2.2 }),
  gap: new THREE.MeshStandardMaterial({ color: '#221d19', roughness: 1 }),
  ceramic: new THREE.MeshStandardMaterial({ color: '#e9e1d3', roughness: 0.35 }),
  dark: new THREE.MeshStandardMaterial({ color: '#2b241f', roughness: 0.4, metalness: 0.5 }),
  glow: new THREE.MeshBasicMaterial({ color: '#ffd7a0' }),
};

const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.setSize(W, H); renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color('#e9e3da');
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.4;

// box from extents: x (along wall), z (height), d (distance out from the wall face, toward the room)
function box(x0, x1, z0, z1, d0, d1, m, cast = true) {
  const b = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, z1 - z0, d1 - d0), m);
  b.position.set((x0 + x1) / 2, (z0 + z1) / 2, (d0 + d1) / 2); b.castShadow = cast; b.receiveShadow = true; scene.add(b); return b;
}
function cyl(x, d, r, z0, z1, m, rTop = r, seg = 64) {
  const c = new THREE.Mesh(new THREE.CylinderGeometry(rTop, r, z1 - z0, seg), m); c.position.set(x, (z0 + z1) / 2, d);
  c.castShadow = c.receiveShadow = true; scene.add(c); return c;
}

// ---------- architecture (d'après la vue Revit : niche entre deux retours, porte à gauche, retombée en haut) ----------
const DOOR = +(q.get('door') || 0.90), SOF = 2.45;          // largeur porte, sous-face de la retombée
const floor = new THREE.Mesh(new THREE.PlaneGeometry(8, 6), new THREE.MeshStandardMaterial({ map: T.oak, roughness: 0.55 }));
floor.rotation.x = -Math.PI / 2; floor.position.set(0.5, 0, 2); floor.receiveShadow = true; scene.add(floor);
box(-4, 4, CH, CH + 0.1, -0.3, 5, new THREE.MeshStandardMaterial({ color: '#f4f1ec', roughness: 0.9 }));      // plafond
const XL = -DOOR - 0.02;                                                       // face du retour gauche
box(XL - 0.25, XL, 0, CH, -0.2, 0.55, M.plaster);                               // retour gauche
box(WALL, WALL + 0.25, 0, CH, -0.2, 0.55, M.plaster);                           // retour droit
box(-4, XL - 0.25, 0, CH, 0.35, 0.55, M.plaster); box(WALL + 0.25, 4, 0, CH, 0.35, 0.55, M.plaster);
box(XL, WALL, SOF, CH, -0.2, 0.55, M.plaster);
box(XL, 0, 0, SOF, -0.2, -0.0, M.plaster);                                   // retombée
box(XL, WALL, SOF - 0.004, SOF, 0.02, 0.03, M.gap, false);
{ const strip = new THREE.Mesh(new THREE.BoxGeometry(WALL - XL - 0.1, 0.004, 0.012), M.glow); strip.position.set((XL + WALL) / 2, SOF - 0.006, 0.09); scene.add(strip); }
// porte affleurante peinte comme les murs, ouverture par poussée : elle s'efface
box(-DOOR, -0.003, 0.01, SOF - 0.003, -0.2, 0.02, M.plaster);
box(-0.003, 0, 0.01, SOF, -0.2, 0.02, M.gap, false); box(XL, -DOOR, 0.01, SOF, -0.2, 0.02, M.gap, false);
box(-DOOR, 0, 0, 0.01, -0.2, 0.02, M.gap, false);

// ---------- 1. Panneau marbre Calacatta Viola en livre ouvert, cadre bronze ----------
function viola(g, w, h) {
  g.fillStyle = '#efe8e1'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 9000; i++) { g.fillStyle = shade('#e6dcd2', rr(-0.03, 0.03)); g.globalAlpha = 0.25; g.fillRect(rnd() * w, rnd() * h, 3, 3); }
  const vein = (col, n, wmin, wmax, a) => { for (let k = 0; k < n; k++) {
    let x = rr(-0.2, 0.9) * w, y = rr(0, 1) * h, ang = rr(-0.9, -0.2);
    g.strokeStyle = col; g.lineCap = 'round';
    for (let st = 0; st < 260; st++) { const nx = x + Math.cos(ang) * 9, ny = y + Math.sin(ang) * 9 * -1;
      g.globalAlpha = a * rr(0.5, 1); g.lineWidth = rr(wmin, wmax); g.beginPath(); g.moveTo(x, y); g.lineTo(nx, ny); g.stroke();
      x = nx; y = ny; ang += rr(-0.12, 0.12); if (rnd() < 0.015) ang += rr(-0.6, 0.6); } } };
  const layer = (blur, fn) => { const c = document.createElement('canvas'); c.width = w; c.height = h; const lg = c.getContext('2d');
    const keep = g; g = lg; fn(); g = keep; g.filter = `blur(${blur}px)`; g.drawImage(c, 0, 0); g.filter = 'none'; };
  layer(9, () => vein('#7e4a56', 8, 16, 46, 0.8));
  layer(1.2, () => { vein('#4a1f2b', 10, 4, 12, 1); vein('#6a3542', 16, 1, 3, 0.9); });
}
function bookmatch() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 2048; const g = c.getContext('2d');
  const half = document.createElement('canvas'); half.width = 512; half.height = 2048; viola(half.getContext('2d'), 512, 2048);
  g.drawImage(half, 0, 0); g.save(); g.translate(1024, 0); g.scale(-1, 1); g.drawImage(half, 0, 0); g.restore();
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}
const MARBLE = new THREE.MeshPhysicalMaterial({ map: bookmatch(), roughness: 0.28, clearcoat: 0.3, clearcoatRoughness: 0.35 });
const PX0 = 0.0, PX1 = WALL;
box(PX0, PX1, 0, SOF, 0, 0.03, M.bronze);                                            // cadre bronze (visible en joint de 10 mm)
box(PX0 + 0.012, PX1 - 0.012, 0.012, SOF - 0.012, 0.03, 0.05, MARBLE);               // dalle marbre 20 mm
// lumière rasante depuis la retombée
for (const x of [0.25, WALL / 2, WALL - 0.25]) { const sp = new THREE.SpotLight('#ffd6a6', 2.2, 3.2, 0.75, 1.0, 2); sp.position.set(x, SOF - 0.02, 0.18); sp.target.position.set(x, 0.6, 0.05); scene.add(sp, sp.target); }

// ---------- 2. Buffet-console « ÉCRIN » : bouts arrondis, noyer, plateau marbre, socle bronze ----------
const BL = WALL - 0.10, BD = 0.45, BH = 0.78, BX = WALL / 2, BZ = 0.05 + BD / 2, PL = 0.10;
function stadium(len, dep, inset = 0) {
  const r = dep / 2 - inset, l = len / 2 - dep / 2, sh = new THREE.Shape();
  sh.moveTo(-l, -r); sh.lineTo(l, -r); sh.absarc(l, 0, r, -Math.PI / 2, Math.PI / 2, false); sh.lineTo(-l, r); sh.absarc(-l, 0, r, Math.PI / 2, Math.PI * 1.5, false); return sh;
}
function slab(len, dep, inset, z0, z1, m, bevel = 0.004) {
  const g = new THREE.ExtrudeGeometry(stadium(len, dep, inset), { depth: z1 - z0 - 2 * bevel, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelSegments: 3, curveSegments: 64 });
  const mesh = new THREE.Mesh(g, m); mesh.rotation.x = -Math.PI / 2; mesh.position.set(BX, z0 + bevel, BZ); mesh.castShadow = mesh.receiveShadow = true; scene.add(mesh); return mesh;
}
slab(BL - 0.12, BD, 0.05, 0, PL, M.bronze);                                         // socle bronze en retrait
slab(BL, BD, 0.0, PL, BH - 0.025, M.walnut(3, 1), 0.006);                          // corps noyer
slab(BL + 0.02, BD + 0.02, 0.0, BH - 0.025, BH, MARBLE, 0.003);                    // plateau marbre 25 mm
// façade : 2 portes à cannelures horizontales fines + lignes laiton
if (false) box(BX - (BL / 2 - BD / 2), BX + (BL / 2 - BD / 2), z, z + 0.004, BZ + BD / 2 - 0.002, BZ + BD / 2 + 0.002, M.gap, false);
box(BX - 0.002, BX + 0.002, PL + 0.02, BH - 0.04, BZ + BD / 2 - 0.002, BZ + BD / 2 + 0.003, M.gap, false);
box(BX - (BL / 2 - BD / 2), BX + (BL / 2 - BD / 2), BH - 0.035, BH - 0.029, BZ + BD / 2 - 0.001, BZ + BD / 2 + 0.004, M.bronze, false);

// ---------- 3. Mise en scène ----------
const TOP = BH;
// lampe sculpturale : pied céramique en galets + abat-jour lin plissé
const lx = BX - BL / 2 + 0.30;
const sph = (x, z, r, d, m) => { const s = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), m); s.scale.y = 0.8; s.position.set(x, z, d); s.castShadow = true; scene.add(s); };
sph(lx, TOP + 0.08, 0.10, BZ, M.ceramic); sph(lx, TOP + 0.22, 0.085, BZ, M.ceramic); sph(lx, TOP + 0.34, 0.06, BZ, M.ceramic);
cyl(lx, BZ, 0.005, TOP + 0.38, TOP + 0.44, M.bronze);
cyl(lx, BZ, 0.20, TOP + 0.44, TOP + 0.66, new THREE.MeshStandardMaterial({ color: '#f1e7d4', roughness: 1, emissive: '#ffcf96', emissiveIntensity: 0.7, side: THREE.DoubleSide }), 0.15);
{ const l = new THREE.PointLight('#ffc98a', 2.2, 3, 2); l.position.set(lx, TOP + 0.52, BZ + 0.05); scene.add(l); }
// livres + bol bronze + sculpture
box(BX - 0.05, BX + 0.20, TOP, TOP + 0.04, BZ - 0.12, BZ + 0.08, new THREE.MeshStandardMaterial({ color: '#2f2924', roughness: 0.8 }));
box(BX - 0.03, BX + 0.18, TOP + 0.04, TOP + 0.07, BZ - 0.10, BZ + 0.06, new THREE.MeshStandardMaterial({ color: '#c9b79a', roughness: 0.8 }));
cyl(BX + 0.07, BZ - 0.02, 0.07, TOP + 0.07, TOP + 0.11, M.dark, 0.09);
{ const k = new THREE.Mesh(new THREE.TorusGeometry(0.11, 0.035, 32, 96), new THREE.MeshStandardMaterial({ color: '#d9cfc0', roughness: 0.6 }));
  k.position.set(BX + BL / 2 - 0.32, TOP + 0.145, BZ - 0.03); k.castShadow = true; scene.add(k);
  box(BX + BL / 2 - 0.40, BX + BL / 2 - 0.24, TOP, TOP + 0.025, BZ - 0.08, BZ + 0.02, M.trav(0.2, 0.2)); }
// grand vase + branche
cyl(BX + BL / 2 - 0.12, BZ + 0.02, 0.08, TOP, TOP + 0.42, new THREE.MeshStandardMaterial({ color: '#4a3a32', roughness: 0.7 }), 0.06);
{ const br = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(BX + BL / 2 - 0.12, TOP + 0.40, BZ), new THREE.Vector3(BX + BL / 2 - 0.20, TOP + 0.85, BZ + 0.05), new THREE.Vector3(BX + BL / 2 - 0.42, TOP + 1.25, BZ + 0.08)]), 32, 0.006, 6), M.dark); scene.add(br);
  for (let i = 0; i < 14; i++) { const lf = new THREE.Mesh(new THREE.SphereGeometry(0.03, 12, 8), new THREE.MeshStandardMaterial({ color: '#5c6b4a', roughness: 0.8 })); lf.scale.set(1, 0.35, 0.6);
    const t = 0.4 + i * 0.04; lf.position.set(BX + BL / 2 - 0.12 - t * 0.3 + rr(-0.06, 0.06), TOP + 0.4 + t * 0.85, BZ + rr(0, 0.1)); scene.add(lf); } }
const CX0 = BX - BL / 2, CX1 = BX + BL / 2, CLAD2 = 0;
// ---------- light & camera ----------
scene.add(new THREE.HemisphereLight('#f4ede2', '#9c8670', 0.6));
const key = new THREE.DirectionalLight('#ffe6c4', 2.2); key.position.set(-2.5, 3.5, 4); key.castShadow = true;
key.shadow.mapSize.set(4096, 4096); key.shadow.bias = -0.0004; Object.assign(key.shadow.camera, { left: -3, right: 3, top: 3, bottom: -1, near: 0.5, far: 12 }); scene.add(key);
for (const x of []) { const sp = new THREE.SpotLight('#ffd4a0', 4, 4, 0.45, 0.8, 2); sp.position.set(x, SOF - 0.02, 0.35); sp.target.position.set(x, 0.8, 0.02); scene.add(sp, sp.target); }

const V = { front: { pos: [(WALL - DOOR) / 2, 1.3, 3.2], look: [(WALL - DOOR) / 2, 1.2, 0], fov: 50 },
            angle: { pos: [-1.9, 1.35, 2.4], look: [WALL / 2 + 0.1, 0.95, 0.1], fov: 50 },
            detail: { pos: [WALL - 0.25, 1.15, 1.25], look: [CX0 + 0.45, 0.85, 0.2], fov: 50 } }[VIEW];
const cam = new THREE.PerspectiveCamera(V.fov, W / H, 0.05, 50); cam.position.set(...V.pos); cam.lookAt(...V.look);
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(scene, cam));
const ao = new GTAOPass(scene, cam, W, H); ao.updateGtaoMaterial({ radius: 0.12, scale: 1.2, samples: 16 }); ao.blendIntensity = 0.8; comp.addPass(ao);
comp.addPass(new OutputPass()); comp.render(); window.__done = true;
