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
const DARK = () => { const t = T.smoked.clone(); t.needsUpdate = true; t.repeat.set(1, 2); return new THREE.MeshStandardMaterial({ map: t, color: '#5a4a40', roughness: 0.45 }); };
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
const scene = new THREE.Scene(); scene.background = new THREE.Color('#2a2420');
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.25;

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
box(XL - 0.25, XL - 0.02, 0, CH, -0.2, 0.55, M.plaster); box(XL - 0.02, XL, 0, SOF, -0.2, 0.55, DARK()); box(XL - 0.02, XL, SOF, CH, -0.2, 0.55, M.plaster);                               // retour gauche
box(WALL + 0.02, WALL + 0.25, 0, CH, -0.2, 0.55, M.plaster); box(WALL, WALL + 0.02, 0, SOF, -0.2, 0.55, DARK()); box(WALL, WALL + 0.02, SOF, CH, -0.2, 0.55, M.plaster);                           // retour droit
box(-4, XL - 0.25, 0, CH, 0.35, 0.55, M.plaster); box(WALL + 0.25, 4, 0, CH, 0.35, 0.55, M.plaster);
box(XL, WALL, SOF, CH, -0.2, 0.55, M.plaster);
box(XL, 0, 0, SOF, -0.2, -0.0, M.plaster);                                   // retombée
box(XL, WALL, SOF - 0.004, SOF, 0.02, 0.03, M.gap, false);
{ const strip = new THREE.Mesh(new THREE.BoxGeometry(WALL - XL - 0.1, 0.004, 0.012), M.glow); strip.position.set((XL + WALL) / 2, SOF - 0.006, 0.09); scene.add(strip); }
// porte affleurante peinte comme les murs, ouverture par poussée : elle s'efface
box(-DOOR, -0.003, 0.01, SOF - 0.003, -0.2, 0.02, DARK());
box(-0.10, -0.088, 0.9, 1.5, 0.02, 0.035, M.bronze);
box(-0.003, 0, 0.01, SOF, -0.2, 0.02, M.gap, false); box(XL, -DOOR, 0.01, SOF, -0.2, 0.02, M.gap, false);
box(-DOOR, 0, 0, 0.01, -0.2, 0.02, M.gap, false);

// ---------- 1. Panneau ONYX miel rétroéclairé, cadre laiton ----------
function onyx(g, w, h) {
  const gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, '#f2c27a'); gr.addColorStop(0.5, '#e6a85a'); gr.addColorStop(1, '#f5d39a');
  g.fillStyle = gr; g.fillRect(0, 0, w, h);
  const layer = (blur, fn) => { const c = document.createElement('canvas'); c.width = w; c.height = h; fn(c.getContext('2d')); g.filter = `blur(${blur}px)`; g.drawImage(c, 0, 0); g.filter = 'none'; };
  // bandes ondulées typiques de l'onyx
  layer(5, lg => { for (let i = 0; i < 70; i++) { lg.strokeStyle = ['#b86a2c', '#fff0cf', '#d18a40', '#8a4a1c'][i % 4]; lg.globalAlpha = rr(0.15, 0.55); lg.lineWidth = rr(3, 30);
    const y0 = rnd() * h * 1.3 - h * 0.15, amp = rr(20, 90), f = rr(0.004, 0.012), ph = rnd() * 6; lg.beginPath();
    for (let x = 0; x <= w; x += 6) lg.lineTo(x, y0 + Math.sin(x * f + ph) * amp + x * 0.35); lg.stroke(); } });
  layer(1, lg => { for (let i = 0; i < 60; i++) { lg.strokeStyle = i % 2 ? '#7a3d16' : '#fff6e0'; lg.globalAlpha = rr(0.3, 0.7); lg.lineWidth = rr(0.5, 2);
    const y0 = rnd() * h * 1.3 - h * 0.15, amp = rr(20, 90), f = rr(0.004, 0.012), ph = rnd() * 6; lg.beginPath();
    for (let x = 0; x <= w; x += 6) lg.lineTo(x, y0 + Math.sin(x * f + ph) * amp + x * 0.35); lg.stroke(); } });
}
function bookmatchOnyx() {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 2048; const g = c.getContext('2d');
  const half = document.createElement('canvas'); half.width = 512; half.height = 2048; onyx(half.getContext('2d'), 512, 2048);
  g.drawImage(half, 0, 0); g.save(); g.translate(1024, 0); g.scale(-1, 1); g.drawImage(half, 0, 0); g.restore();
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const OT = bookmatchOnyx();
const ONYX = new THREE.MeshPhysicalMaterial({ map: OT, emissive: '#ffffff', emissiveMap: OT, emissiveIntensity: 0.6, roughness: 0.3, clearcoat: 0.2 });
box(0, WALL, 0, SOF, 0, 0.035, new THREE.MeshStandardMaterial({ color: '#c9a25e', metalness: 1, roughness: 0.25 }));     // cadre laiton brossé
box(0.03, WALL - 0.03, 0.03, SOF - 0.03, 0.035, 0.055, ONYX);                                                              // onyx 20 mm
{ const l = new THREE.RectAreaLight ? null : null; }
for (const [x, z] of [[WALL * 0.3, 1.0], [WALL * 0.7, 1.0], [WALL * 0.5, 1.9]]) { const pl = new THREE.PointLight('#ffb866', 2.4, 3.5, 2); pl.position.set(x, z, 1.1); scene.add(pl); }

// ---------- 2. Console flottante Nero Marquina + lame laiton ----------
const NERO = (() => { const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d');
  g.fillStyle = '#141313'; g.fillRect(0, 0, 1024, 512);
  for (let i = 0; i < 14; i++) { g.strokeStyle = '#e8e4dc'; g.globalAlpha = rr(0.25, 0.8); g.lineWidth = rr(0.5, 2.2); let x = rnd() * 1024, y = rnd() * 512, a = rr(-0.6, 0.6); g.beginPath(); g.moveTo(x, y);
    for (let k = 0; k < 120; k++) { x += Math.cos(a) * 8; y += Math.sin(a) * 8; a += rr(-0.15, 0.15); g.lineTo(x, y); } g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return new THREE.MeshPhysicalMaterial({ map: t, roughness: 0.18, clearcoat: 0.8, clearcoatRoughness: 0.1 }); })();
const BRASS = new THREE.MeshStandardMaterial({ color: '#c9a25e', metalness: 1, roughness: 0.22 });
const CW = WALL - 0.16, CX0 = 0.08, CX1 = CX0 + CW, D = 0.42, TOP = 0.82, BOX = 0.24;
box(CX0, CX1, TOP - BOX, TOP, 0.055, 0.055 + D, NERO);                                   // caisson marbre noir monolithe (tiroirs push-latch)
box(CX0 + 0.004, CX1 - 0.004, TOP - BOX + 0.04, TOP - BOX + 0.046, 0.055 + D - 0.002, 0.055 + D + 0.004, BRASS);   // filet laiton
box(CX0 + CW / 2 - 0.002, CX0 + CW / 2 + 0.002, TOP - BOX + 0.05, TOP - 0.01, 0.055 + D - 0.001, 0.055 + D + 0.002, new THREE.MeshStandardMaterial({ color: '#000' }), false);
// lame laiton verticale sculpturale côté droit (pied)
box(CX1 - 0.30, CX1 - 0.27, 0, TOP - BOX, 0.07, 0.055 + D - 0.02, BRASS);
box(CX1 - 0.40, CX1 - 0.17, 0, 0.01, 0.07, 0.055 + D - 0.02, BRASS);
{ const strip = new THREE.Mesh(new THREE.BoxGeometry(CW - 0.08, 0.004, 0.01), new THREE.MeshBasicMaterial({ color: '#ffcf8a' })); strip.position.set(CX0 + CW / 2, TOP - BOX - 0.003, 0.055 + D - 0.04); scene.add(strip);
  const sp = new THREE.SpotLight('#ffb866', 3, 1.5, 1.3, 1, 2); sp.position.set(CX0 + CW / 2, TOP - BOX - 0.02, 0.3); sp.target.position.set(CX0 + CW / 2, 0, 0.3); scene.add(sp, sp.target); }

// ---------- 3. Art de la table : carafe, verres, plateau laiton, sculpture ----------
const Z = 0.055 + D / 2, CRYS = new THREE.MeshPhysicalMaterial({ color: '#ffffff', roughness: 0.02, transmission: 1, thickness: 0.02, ior: 1.5, transparent: true, opacity: 0.35 });
box(CX0 + 0.10, CX0 + 0.55, TOP, TOP + 0.012, Z - 0.13, Z + 0.10, BRASS);
cyl(CX0 + 0.22, Z - 0.02, 0.075, TOP + 0.012, TOP + 0.16, CRYS, 0.075); cyl(CX0 + 0.22, Z - 0.02, 0.022, TOP + 0.16, TOP + 0.30, CRYS, 0.03);
cyl(CX0 + 0.22, Z - 0.02, 0.07, TOP + 0.014, TOP + 0.08, new THREE.MeshStandardMaterial({ color: '#4a0f14', roughness: 0.1, transparent: true, opacity: 0.85 }), 0.07);
for (const [x, z] of [[0.36, -0.06], [0.45, 0.02], [0.48, -0.08]]) { cyl(CX0 + x, Z + z, 0.035, TOP + 0.012, TOP + 0.10, CRYS, 0.04); cyl(CX0 + x, Z + z, 0.004, TOP + 0.10, TOP + 0.17, CRYS); cyl(CX0 + x, Z + z, 0.04, TOP + 0.17, TOP + 0.26, CRYS, 0.045); }
{ const s = new THREE.Mesh(new THREE.TorusKnotGeometry(0.09, 0.025, 160, 24, 2, 3), new THREE.MeshStandardMaterial({ color: '#1a1716', metalness: 0.6, roughness: 0.3 })); s.position.set(CX1 - 0.18, TOP + 0.13, Z - 0.02); s.castShadow = true; scene.add(s); }
box(CX1 - 0.27, CX1 - 0.09, TOP, TOP + 0.02, Z - 0.10, Z + 0.06, NERO);
cyl(CX0 + CW * 0.62, Z + 0.02, 0.09, TOP, TOP + 0.36, new THREE.MeshStandardMaterial({ color: '#141210', roughness: 0.35 }), 0.05);
// ---------- light & camera ----------
scene.add(new THREE.HemisphereLight('#f4ede2', '#6c5a4a', 0.25));
const key = new THREE.DirectionalLight('#ffe6c4', 0.9); key.position.set(-2.5, 3.5, 4); key.castShadow = true;
key.shadow.mapSize.set(4096, 4096); key.shadow.bias = -0.0004; Object.assign(key.shadow.camera, { left: -3, right: 3, top: 3, bottom: -1, near: 0.5, far: 12 }); scene.add(key);
for (const x of []) { const sp = new THREE.SpotLight('#ffd4a0', 4, 4, 0.45, 0.8, 2); sp.position.set(x, SOF - 0.02, 0.35); sp.target.position.set(x, 0.8, 0.02); scene.add(sp, sp.target); }

const V = { front: { pos: [(WALL - DOOR) / 2, 1.3, 3.2], look: [(WALL - DOOR) / 2, 1.2, 0], fov: 50 },
            angle: { pos: [-1.9, 1.35, 2.4], look: [WALL / 2 + 0.1, 0.95, 0.1], fov: 50 },
            detail: { pos: [WALL - 0.2, 1.2, 1.1], look: [CX0 + 0.35, 0.9, 0.2], fov: 50 } }[VIEW];
const cam = new THREE.PerspectiveCamera(V.fov, W / H, 0.05, 50); cam.position.set(...V.pos); cam.lookAt(...V.look);
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(scene, cam));
const ao = new GTAOPass(scene, cam, W, H); ao.updateGtaoMaterial({ radius: 0.12, scale: 1.2, samples: 16 }); ao.blendIntensity = 0.8; comp.addPass(ao);
comp.addPass(new OutputPass()); comp.render(); window.__done = true;
