// KAÏRA — Meuble TV « PIVOT » : meuble central entre le lit et le placard, TV sur panneau, 40 cm d'encombrement.
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


// Repère : x = largeur de la chambre, z positif vers le placard, mur de tête de lit à z = -2.6, placard à z = +2.8
const UP = (q.get('tv') || 'up') === 'up';
const BRASS = new THREE.MeshStandardMaterial({ color: '#b8925a', metalness: 1, roughness: 0.28 });
const LIN = (c) => new THREE.MeshStandardMaterial({ color: c, roughness: 1 });
const floor = new THREE.Mesh(new THREE.PlaneGeometry(6, 7), new THREE.MeshStandardMaterial({ map: T.oak, roughness: 0.55 }));
floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, 0.1); floor.receiveShadow = true; scene.add(floor);
box(-2.4, 2.4, CH, CH + 0.1, -2.8, 3.0, new THREE.MeshStandardMaterial({ color: '#f4f1ec', roughness: 0.9 }));
box(-2.4, 2.4, 0, CH, -2.8, -2.6, M.plaster); box(-2.6, -2.4, 0, CH, -2.8, 3.0, M.plaster); box(2.4, 2.6, 0, CH, -2.8, 3.0, M.plaster);
box(-2.4, 2.4, 0, CH, 2.8, 3.0, M.plaster);
// fenêtre sur le mur droit
box(2.38, 2.40, 0.6, 2.4, -1.6, -0.2, new THREE.MeshStandardMaterial({ color: '#fff6e6', emissive: '#fff1da', emissiveIntensity: 0.9 }));
const g = new THREE.PlaneGeometry(0.6, 2.6, 24, 1); { const p = g.attributes.position; for (let i = 0; i < p.count; i++) p.setZ(i, Math.sin(p.getX(i) * 40) * 0.02); }
for (const z of [-1.85, 0.05]) { const c = new THREE.Mesh(g, new THREE.MeshStandardMaterial({ color: '#efe7da', roughness: 1, side: THREE.DoubleSide })); c.rotation.y = -Math.PI / 2; c.position.set(2.3, 1.3, z); scene.add(c); }

// ---------- Lit 180 × 200 + tête de lit tapissée (contexte) ----------
for (let x = -1.5; x < 1.5; x += 0.15) { const p = new THREE.Mesh(new RoundedBoxGeometry(0.144, 1.3, 0.09, 4, 0.03), LIN('#8e7b6a')); p.position.set(x + 0.075, 0.65, -2.555); p.castShadow = p.receiveShadow = true; scene.add(p); }
box(-1.5, 1.5, 1.30, 1.33, -2.6, -2.5, BRASS);
box(-0.95, 0.95, 0.06, 0.30, -2.5, -0.40, M.smoked); box(-0.9, 0.9, 0, 0.06, -2.45, -0.45, M.gap);
const rb = (x0, x1, y0, y1, z0, z1, m, r = 0.05) => { const b = new THREE.Mesh(new RoundedBoxGeometry(x1 - x0, y1 - y0, z1 - z0, 4, r), m); b.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); b.castShadow = b.receiveShadow = true; scene.add(b); };
rb(-0.9, 0.9, 0.30, 0.56, -2.45, -0.45, LIN('#f0ebe2')); rb(-0.92, 0.92, 0.50, 0.62, -1.8, -0.42, LIN('#f4f0e9'));
rb(-0.94, 0.94, 0.57, 0.65, -1.0, -0.55, new THREE.MeshStandardMaterial({ color: '#8a4f2c', roughness: 0.95 }), 0.04);
for (const x of [-0.45, 0.45]) rb(x - 0.36, x + 0.36, 0.56, 0.98, -2.45, -2.28, LIN('#f4f0e9'), 0.07);
for (const x of [-0.42, 0.42]) rb(x - 0.27, x + 0.27, 0.58, 0.9, -2.28, -2.14, LIN('#d9ccb6'), 0.06);
for (const x of [-1.32, 1.32]) { box(x - 0.25, x + 0.25, 0.38, 0.56, -2.5, -2.1, M.smoked); }
// ---------- Placard (contexte) : façades chêne fumé cannelé, poignées laiton ----------
box(-2.4, 2.4, 0, 0.06, 2.2, 2.8, M.gap); box(-2.4, 2.4, 0.06, CH - 0.02, 2.22, 2.8, M.smoked);
for (let x = -2.38; x < 2.38; x += 0.045) { const f = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, CH - 0.12, 10, 1, false, Math.PI / 2, Math.PI), M.smoked); f.position.set(x + 0.012, CH / 2 + 0.02, 2.22); scene.add(f); }
for (let x = -1.8; x <= 1.8; x += 0.6) { box(x - 0.002, x + 0.002, 0.08, CH - 0.04, 2.205, 2.22, M.gap, false); box(x - 0.03, x - 0.018, 0.9, 1.5, 2.19, 2.205, BRASS); }
// tapis
box(-1.6, 1.6, 0, 0.012, -1.6, 1.5, new THREE.MeshStandardMaterial({ color: '#cdbba0', roughness: 1 }), false);

// ================= 3 DIRECTIONS (paramètre ?v=A|B|C) =================
const VAR = q.get('v') || 'A', ZC = 0.55;
const blackTV = new THREE.MeshStandardMaterial({ color: '#0d0d0e', roughness: 0.25, metalness: 0.3 });
const screen = (y0) => { box(-0.615, 0.615, y0, y0 + 0.71, ZC - 0.07, ZC - 0.045, blackTV);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(1.21, 0.69), new THREE.MeshStandardMaterial({ color: '#15181c', roughness: 0.08, metalness: 0.2 })); scr.rotation.y = Math.PI; scr.position.set(0, y0 + 0.355, ZC - 0.071); scene.add(scr); };
const NERO = (() => { const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d'); g.fillStyle = '#141313'; g.fillRect(0, 0, 1024, 512);
  for (let i = 0; i < 14; i++) { g.strokeStyle = '#e8e4dc'; g.globalAlpha = rr(0.25, 0.8); g.lineWidth = rr(0.5, 2.2); let x = rnd() * 1024, y = rnd() * 512, a = rr(-0.6, 0.6); g.beginPath(); g.moveTo(x, y);
    for (let k = 0; k < 120; k++) { x += Math.cos(a) * 8; y += Math.sin(a) * 8; a += rr(-0.15, 0.15); g.lineTo(x, y); } g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return new THREE.MeshPhysicalMaterial({ map: t, roughness: 0.18, clearcoat: 0.8, clearcoatRoughness: 0.1 }); })();
const STEEL = new THREE.MeshStandardMaterial({ color: '#1c1b1a', metalness: 0.7, roughness: 0.45 });
if (VAR === 'A') {
  // A — MONOLITHE : bloc travertin plein + mât acier noir, TV qui flotte
  box(-0.66, 0.66, 0, 0.04, ZC - 0.19, ZC + 0.19, M.gap);
  box(-0.70, 0.70, 0.04, 0.42, ZC - 0.225, ZC + 0.225, M.trav(1.4, 0.5));
  box(-0.045, 0.045, 0.42, 1.38, ZC - 0.04, ZC + 0.04, STEEL);
  box(-0.62, 0.62, 0.70, 1.42, ZC - 0.045, ZC + 0.0, STEEL);                     // dos acier qui habille la TV
  screen(0.71);
  cyl(0.48, ZC, 0.05, 0.42, 0.62, M.ceramic, 0.03); { const s2 = new THREE.Mesh(new THREE.SphereGeometry(0.07, 32, 24), M.dark); s2.position.set(-0.5, 0.49, ZC); scene.add(s2); }
} else if (VAR === 'B') {
  // B — NOIR & LAITON : meuble marbre noir, panneau laqué noir cannelé avec cadre laiton et halo LED
  box(-0.86, 0.86, 0, 0.08, ZC - 0.2, ZC + 0.2, BRASS);
  box(-0.90, 0.90, 0.08, 0.50, ZC - 0.225, ZC + 0.225, NERO);
  for (const side of [-1, 1]) box(-0.002, 0.002, 0.1, 0.48, ZC + side * 0.2255 - 0.002, ZC + side * 0.2255 + 0.002, M.gap, false);
  box(-0.75, 0.75, 0.50, 1.55, ZC - 0.03, ZC + 0.03, new THREE.MeshPhysicalMaterial({ color: '#111', roughness: 0.3, clearcoat: 1 }));
  for (let x = -0.735; x < 0.74; x += 0.03) { const f = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.04, 10, 1, false, -Math.PI / 2, Math.PI), new THREE.MeshPhysicalMaterial({ color: '#111', roughness: 0.35, clearcoat: 1 })); f.position.set(x, 1.025, ZC + 0.03); scene.add(f); }
  for (const [x0, x1, y0, y1] of [[-0.76, 0.76, 1.55, 1.565], [-0.765, -0.75, 0.5, 1.565], [0.75, 0.765, 0.5, 1.565]]) box(x0, x1, y0, y1, ZC - 0.035, ZC + 0.035, BRASS);
  const halo = new THREE.Mesh(new THREE.BoxGeometry(1.48, 0.004, 0.04), M.glow); halo.position.set(0, 1.56, ZC); scene.add(halo);
  screen(0.70);
  cyl(0.70, ZC, 0.05, 0.5, 0.8, new THREE.MeshStandardMaterial({ color: '#b8925a', metalness: 1, roughness: 0.3 }), 0.03);
} else {
  // C — DOUX & ARRONDI : base arrondie laquée grège, plateau chêne clair, panneau en arche tapissé bouclé
  const sh = new THREE.Shape(); const r = 0.21, l = 0.6; sh.moveTo(-l, -r); sh.lineTo(l, -r); sh.absarc(l, 0, r, -Math.PI / 2, Math.PI / 2, false); sh.lineTo(-l, r); sh.absarc(-l, 0, r, Math.PI / 2, Math.PI * 1.5, false);
  const ex = (z0, z1, m, sc = 1) => { const ge = new THREE.ExtrudeGeometry(sh, { depth: z1 - z0 - 0.01, bevelEnabled: true, bevelThickness: 0.005, bevelSize: 0.005, bevelSegments: 3, curveSegments: 64 });
    const me = new THREE.Mesh(ge, m); me.rotation.x = -Math.PI / 2; me.scale.set(sc, sc, 1); me.position.set(0, z0 + 0.005, ZC); me.castShadow = me.receiveShadow = true; scene.add(me); };
  ex(0, 0.06, M.gap, 0.94); ex(0.06, 0.47, new THREE.MeshPhysicalMaterial({ color: '#d8cfc2', roughness: 0.35, clearcoat: 0.4 }));
  const oakL = new THREE.MeshStandardMaterial({ map: T.smoked, color: '#e8d2b4', roughness: 0.5 }); ex(0.47, 0.50, oakL, 1.01);
  const arch = new THREE.Shape(); const AW = 0.72, AH = 1.10; arch.moveTo(-AW, 0); arch.lineTo(AW, 0); arch.lineTo(AW, AH - AW); arch.absarc(0, AH - AW, AW, 0, Math.PI, false); arch.lineTo(-AW, 0);
  const ag = new THREE.ExtrudeGeometry(arch, { depth: 0.05, bevelEnabled: true, bevelThickness: 0.025, bevelSize: 0.025, bevelSegments: 6, curveSegments: 64 });
  const am = new THREE.Mesh(ag, M.boucle ? M.boucle : new THREE.MeshStandardMaterial({ color: '#ebe2d4', roughness: 1 })); am.position.set(0, 0.50, ZC - 0.025); am.castShadow = am.receiveShadow = true; scene.add(am);
  screen(0.74);
  cyl(-0.62, ZC, 0.07, 0.5, 0.72, M.ceramic, 0.04); cyl(0.6, ZC, 0.1, 0.5, 0.53, oakL, 0.1);
}

// ---------- lumière ----------
scene.add(new THREE.HemisphereLight('#f4ede2', '#9c8670', 0.45));
const sun = new THREE.DirectionalLight('#ffe6c4', 2.2); sun.position.set(6, 3.5, -1); sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096); sun.shadow.bias = -0.0004;
Object.assign(sun.shadow.camera, { left: -4, right: 4, top: 4, bottom: -2, near: 0.5, far: 15 }); scene.add(sun);
for (const [x, z] of [[-1.32, -2.3], [1.32, -2.3]]) { const l = new THREE.PointLight('#ffc98a', 1.6, 3, 2); l.position.set(x, 0.85, z); scene.add(l);
  const b2 = new THREE.Mesh(new THREE.SphereGeometry(0.09, 32, 24), M.ceramic); b2.scale.y = 1.3; b2.position.set(x, 0.68, z); b2.castShadow = true; scene.add(b2);
  const sh = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.17, 0.2, 48, 1, true), new THREE.MeshStandardMaterial({ color: '#f1e7d4', emissive: '#ffcf96', emissiveIntensity: 0.6, side: THREE.DoubleSide })); sh.position.set(x, 0.88, z); scene.add(sh); }
for (const [x, z] of [[-1.2, 0.5], [1.2, 0.5], [0, 1.6], [-1.2, -1.5], [1.2, -1.5]]) { const s = new THREE.SpotLight('#ffd4a0', 4, 4, 0.6, 0.8, 2); s.position.set(x, CH - 0.05, z); s.target.position.set(x, 0, z); scene.add(s, s.target); }

const V = { bed:  { pos: [-1.5, 1.35, -1.6], look: [0.05, 0.95, 0.6], fov: 52 },
            dress: { pos: [1.9, 1.45, 2.1], look: [-0.1, 0.8, -0.6], fov: 55 },
            side: { pos: [2.1, 1.2, 0.5], look: [0, 0.8, 0.5], fov: 50 } }[VIEW] || { pos: [-1.9, 1.35, -1.9], look: [0.0, 0.9, 0.9], fov: 55 };
const cam = new THREE.PerspectiveCamera(V.fov, W / H, 0.05, 50); cam.position.set(...V.pos); cam.lookAt(...V.look);
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(scene, cam));
const ao = new GTAOPass(scene, cam, W, H); ao.updateGtaoMaterial({ radius: 0.2, scale: 1.2, samples: 16 }); ao.blendIntensity = 0.8; comp.addPass(ao);
comp.addPass(new OutputPass()); comp.render(); window.__done = true;
