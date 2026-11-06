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
box(XL, WALL, SOF, CH, -0.2, 0.55, M.plaster);                                   // retombée
box(XL, WALL, SOF - 0.004, SOF, 0.02, 0.03, M.gap, false);
{ const strip = new THREE.Mesh(new THREE.BoxGeometry(WALL - XL - 0.1, 0.004, 0.012), M.glow); strip.position.set((XL + WALL) / 2, SOF - 0.006, 0.09); scene.add(strip); }
// porte dérobée : même cannelure que le mur, joint 3 mm, tirage laiton vertical
box(-DOOR, -0.003, 0.01, SOF - 0.003, -0.2, CLAD - 0.015, M.walnut(1.3, 2));
for (let x = -DOOR + 0.004; x < -0.02; x += 0.03) {
  const f = new THREE.Mesh(new THREE.CylinderGeometry(0.0125, 0.0125, SOF - 0.03, 12, 1, false, -Math.PI / 2, Math.PI), M.walnut(0.05, 2));
  f.position.set(x + 0.013, SOF / 2, CLAD - 0.015); f.receiveShadow = true; scene.add(f);
}
box(-0.003, 0, 0.01, SOF, -0.2, CLAD, M.gap, false);
box(-0.11, -0.095, 0.85, 1.45, CLAD, CLAD + 0.025, M.bronze);
// ---------- 1. Habillage mural : cannelures noyer, joint creux 10 mm ----------
box(0.0, WALL, 0, 0.02, 0, CLAD - 0.01, M.gap);                  // plinthe en retrait
box(0.0, WALL, 0.02, SOF, 0, CLAD - 0.015, M.walnut(2, 2));
const FL = 0.03;                                                           // cannelure 30 mm
for (let x = 0.01 + 0.004; x < WALL - 0.02; x += FL) {
  const f = new THREE.Mesh(new THREE.CylinderGeometry(0.0125, 0.0125, SOF - 0.03, 12, 1, false, -Math.PI / 2, Math.PI), M.walnut(0.05, 2));
  f.position.set(x + 0.013, SOF / 2 + 0.005, CLAD - 0.015); f.castShadow = false; f.receiveShadow = true; scene.add(f);
}
// ---------- 2. Miroir arche bronze, rétroéclairé ----------
const MW = Math.min(0.62, WALL * 0.5), MH = 1.0, MX = WALL / 2, MZ0 = 1.18;
{
  const s = new THREE.Shape(); s.moveTo(-MW / 2, 0); s.lineTo(MW / 2, 0); s.lineTo(MW / 2, MH - MW / 2); s.absarc(0, MH - MW / 2, MW / 2, 0, Math.PI, false); s.lineTo(-MW / 2, 0);
  const halo = new THREE.Mesh(new THREE.ShapeGeometry(s.clone(), 64), M.glow); halo.scale.set(1.04, 1.03, 1); halo.position.set(MX, MZ0 - 0.015, CLAD + 0.004); scene.add(halo);
  const back = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.02, bevelEnabled: false, curveSegments: 64 }), M.bronze); back.position.set(MX, MZ0, CLAD + 0.008); scene.add(back);
  const mir = new THREE.Mesh(new THREE.ShapeGeometry(s, 64), M.mirror); mir.scale.set(0.96, 0.975, 1); mir.position.set(MX, MZ0 + 0.012, CLAD + 0.029); scene.add(mir);
  
}
// ---------- 3. Console : plateau travertin suspendu + pied cylindrique + tiroir noyer ----------
const CW = Math.min(1.20, WALL - 0.15), CX0 = WALL - 0.075 - CW, CX1 = WALL - 0.075;   // 10 cm de dégagement de chaque côté
const D = 0.35, TOP = 0.80, TH = 0.04;
box(CX0, CX1, TOP - TH, TOP, CLAD, CLAD + D, M.trav(1.2, 0.4));                         // plateau travertin 40 mm (chant d'onglet)
box(CX0 + 0.04, CX1 - 0.32, TOP - TH - 0.14, TOP - TH, CLAD, CLAD + D - 0.03, M.walnut(1, 0.3));  // caisson tiroir suspendu
box(CX0 + 0.04, CX1 - 0.32, TOP - TH - 0.006, TOP - TH, CLAD + D - 0.03, CLAD + D - 0.024, M.gap, false);
box(CX0 + 0.06, CX1 - 0.34, TOP - TH - 0.14, TOP - TH - 0.13, CLAD + D - 0.03, CLAD + D - 0.02, M.bronze);   // lèvre bronze = prise
{ const strip = new THREE.Mesh(new THREE.BoxGeometry(CW - 0.1, 0.004, 0.01), M.glow); strip.position.set((CX0 + CX1) / 2, TOP - TH - 0.003, CLAD + 0.02); scene.add(strip);
  const l = new THREE.SpotLight('#ffc98a', 2.5, 1.6, 1.3, 0.9, 2); l.position.set((CX0 + CX1) / 2, TOP - TH - 0.02, CLAD + 0.06); l.target.position.set((CX0 + CX1) / 2, 0, CLAD); scene.add(l, l.target); }
// pied sculptural : demi-colonne travertin Ø 26 cm sous l'extrémité côté angle
cyl(CX1 - 0.16, CLAD + D / 2, 0.13, 0, TOP - TH, M.trav(0.6, 1), 0.13);
box(CX1 - 0.29, CX1 - 0.03, 0, 0.012, CLAD + D / 2 - 0.13, CLAD + D / 2 + 0.13, M.gap, false);
// ---------- styling ----------
cyl(CX0 + 0.20, CLAD + 0.17, 0.09, TOP, TOP + 0.30, M.ceramic, 0.05);                      // vase
{ const br = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(CX0 + 0.2, TOP + 0.28, CLAD + 0.17), new THREE.Vector3(CX0 + 0.12, TOP + 0.55, CLAD + 0.2), new THREE.Vector3(CX0 + 0.02, TOP + 0.72, CLAD + 0.25)]), 24, 0.005, 6), M.dark); scene.add(br); }
cyl(CX0 + 0.62, CLAD + 0.2, 0.14, TOP, TOP + 0.04, M.dark, 0.16);                           // vide-poche bronze
box(CX0 + 0.42, CX0 + 0.62, TOP, TOP + 0.05, CLAD + 0.05, CLAD + 0.3, new THREE.MeshStandardMaterial({ color: '#c9b79a', roughness: 0.8 }));
const s = new THREE.Mesh(new THREE.SphereGeometry(0.06, 48, 32), M.dark); s.position.set(CX1 - 0.16, TOP + 0.06, CLAD + 0.18); s.castShadow = true; scene.add(s);

// ---------- light & camera ----------
scene.add(new THREE.HemisphereLight('#f4ede2', '#9c8670', 0.6));
const key = new THREE.DirectionalLight('#ffe6c4', 2.2); key.position.set(-2.5, 3.5, 4); key.castShadow = true;
key.shadow.mapSize.set(4096, 4096); key.shadow.bias = -0.0004; Object.assign(key.shadow.camera, { left: -3, right: 3, top: 3, bottom: -1, near: 0.5, far: 12 }); scene.add(key);
for (const x of [0.3, WALL - 0.3]) { const sp = new THREE.SpotLight('#ffd4a0', 4, 4, 0.45, 0.8, 2); sp.position.set(x, SOF - 0.02, 0.35); sp.target.position.set(x, 0.8, 0.02); scene.add(sp, sp.target); }

const V = { front: { pos: [(WALL - DOOR) / 2, 1.3, 3.2], look: [(WALL - DOOR) / 2, 1.2, 0], fov: 50 },
            angle: { pos: [-1.9, 1.35, 2.4], look: [WALL / 2 + 0.1, 0.95, 0.1], fov: 50 },
            detail: { pos: [WALL - 0.05, 1.10, 0.95], look: [CX0 + 0.35, 0.72, 0.15], fov: 50 } }[VIEW];
const cam = new THREE.PerspectiveCamera(V.fov, W / H, 0.05, 50); cam.position.set(...V.pos); cam.lookAt(...V.look);
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(scene, cam));
const ao = new GTAOPass(scene, cam, W, H); ao.updateGtaoMaterial({ radius: 0.12, scale: 1.2, samples: 16 }); ao.blendIntensity = 0.8; comp.addPass(ao);
comp.addPass(new OutputPass()); comp.render(); window.__done = true;
