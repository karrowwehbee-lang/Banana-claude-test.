// KAÏRA — Chambre (modèle Blender du client) : lit, tête de lit, plafond architectural, éclairage.
// Reconstitution de l'architecture et des matériaux de la capture : marbre vert central, colonnes chêne cannelé + LED, panneaux blancs, chevets chêne, parquet chêne.
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
const W = 1600, H = 1000;
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


// ================= ARCHITECTURE EXISTANTE (d'après la capture Blender) =================
// Repère : x = largeur, mur du marbre à z = 0, la chambre s'étend vers z positif. Unités : m.
const RW = 3.9, RD = 4.6, CEIL = 2.80, DROP = 2.60;     // dimensions estimées sur la capture (à recaler sur le .blend)
const xL = -RW / 2, xR = RW / 2;
const LIGHTOAK = tex(1024, 2048, oakFloor('#b07a4f'), 1, 1); LIGHTOAK.repeat.set(RW / 1.3, RD / 3.0);
const OAK = (rx = 1, ry = 1) => { const t = tex(512, 1024, grain('#a8714a'), rx, ry); return new THREE.MeshStandardMaterial({ map: t, roughness: 0.5 }); };
const WHITE = new THREE.MeshStandardMaterial({ color: '#f1efea', roughness: 0.6 });
const BRASS = new THREE.MeshStandardMaterial({ color: '#b8925a', metalness: 1, roughness: 0.28 });
const fl = new THREE.Mesh(new THREE.PlaneGeometry(RW, RD), new THREE.MeshStandardMaterial({ map: LIGHTOAK, roughness: 0.45 }));
fl.rotation.x = -Math.PI / 2; fl.position.set(0, 0, RD / 2); fl.receiveShadow = true; scene.add(fl);
// murs
box(xL - 0.2, xR + 0.2, 0, CEIL + 0.2, -0.25, -0.05, WHITE);
box(xL - 0.2, xL, 0, CEIL + 0.2, -0.25, RD + 0.2, WHITE); box(xR, xR + 0.2, 0, CEIL + 0.2, -0.25, RD + 0.2, WHITE);
box(xL - 0.2, xR + 0.2, 0, CEIL + 0.2, RD, RD + 0.2, WHITE);
// panneaux muraux blancs à joints creux (mur du fond)
box(xL, xR, 0, CEIL, -0.05, 0, WHITE);
for (const x of [-1.25, 1.25]) box(x - 0.004, x + 0.004, 0, DROP, 0.0, 0.002, M.gap, false);
for (const s of [-1, 1]) box(s > 0 ? 0.62 : xL, s > 0 ? xR : -0.62, 1.30, 1.306, 0.0, 0.002, M.gap, false);
// marbre vert central (Verde Guatemala / Verde Alpi), plein hauteur, halo LED périphérique
function verde(g, w, h) {
  g.fillStyle = '#3c4a34'; g.fillRect(0, 0, w, h);
  for (let i = 0; i < 260; i++) { const x = rnd() * w, y = rnd() * h, r = rr(20, 120); const gr = g.createRadialGradient(x, y, 0, x, y, r);
    gr.addColorStop(0, ['#2c3826', '#56634a', '#45523b', '#6b7558'][i % 4]); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.globalAlpha = 0.5; g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  g.globalAlpha = 1;
  const layer = (blur, fn) => { const c = document.createElement('canvas'); c.width = w; c.height = h; fn(c.getContext('2d')); g.filter = `blur(${blur}px)`; g.drawImage(c, 0, 0); g.filter = 'none'; };
  const veins = (lg, col, n, w0, w1, a) => { for (let k = 0; k < n; k++) { let x = rnd() * w, y = rr(-0.1, 1.1) * h, ang = rr(-2.2, -0.9); lg.strokeStyle = col; lg.lineCap = 'round';
    for (let st = 0; st < 200; st++) { const nx = x + Math.cos(ang) * 7, ny = y + Math.sin(ang) * 7; lg.globalAlpha = a * rr(0.4, 1); lg.lineWidth = rr(w0, w1); lg.beginPath(); lg.moveTo(x, y); lg.lineTo(nx, ny); lg.stroke();
      x = nx; y = ny; ang += rr(-0.14, 0.14); if (rnd() < 0.02) { ang += rr(-0.9, 0.9); } } } };
  layer(5, lg => veins(lg, '#a9b39a', 8, 6, 18, 0.35));
  layer(0.8, lg => { veins(lg, '#eef0e4', 9, 0.8, 2.6, 0.9); veins(lg, '#d8dcc8', 18, 0.3, 1.0, 0.6); });
}
const VT = (() => { const c = document.createElement('canvas'); c.width = 512; c.height = 1280; verde(c.getContext('2d'), 512, 1280); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; })();
const VERDE = new THREE.MeshPhysicalMaterial({ map: VT, roughness: 0.22, clearcoat: 0.6, clearcoatRoughness: 0.15 });
box(-0.60, 0.60, 0, CEIL, 0.0, 0.04, VERDE);
for (const x of [-0.605, 0.605]) { const st = new THREE.Mesh(new THREE.BoxGeometry(0.006, CEIL, 0.01), M.glow); st.position.set(x, CEIL / 2, 0.01); scene.add(st);
  const l = new THREE.SpotLight('#ffcf96', 2.5, 3.2, 0.25, 1, 2); l.position.set(x, CEIL - 0.05, 0.08); l.target.position.set(x, 0, 0.08); scene.add(l, l.target); }
// colonnes chêne : partie haute pleine, partie basse cannelée, LED à la jonction
for (const cx of [-1.72, 1.72]) {
  box(cx - 0.15, cx + 0.15, 1.30, DROP, 0.0, 0.14, OAK(1, 2));
  box(cx - 0.15, cx + 0.15, 0, 1.28, 0.0, 0.11, OAK(1, 2));
  for (let x = cx - 0.14; x < cx + 0.14; x += 0.025) { const f = new THREE.Mesh(new THREE.CylinderGeometry(0.011, 0.011, 1.28, 10, 1, false, -Math.PI / 2, Math.PI), OAK(0.05, 1)); f.position.set(x + 0.011, 0.64, 0.11); scene.add(f); }
  const st = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.008, 0.01), M.glow); st.position.set(cx, 1.292, 0.12); scene.add(st);
  const l = new THREE.SpotLight('#ffc98a', 4, 2.0, 0.6, 0.9, 2); l.position.set(cx, 1.27, 0.13); l.target.position.set(cx, 0, 0.13); scene.add(l, l.target);
}
// chevets chêne existants (2 tiroirs)
for (const cx of [-1.25, 1.25]) {
  box(cx - 0.30, cx + 0.30, 0.02, 0.48, 0.02, 0.47, OAK(1, 0.5));
  box(cx - 0.30, cx + 0.30, 0.245, 0.252, 0.468, 0.472, M.gap, false);
  box(cx - 0.29, cx + 0.29, 0, 0.02, 0.04, 0.45, M.gap);
}
// mur droit : grandes façades blanches encadrées (placard / baie)
for (let z = 0.6; z < RD - 0.5; z += 1.05) { box(xR - 0.03, xR, 0.05, 2.35, z, z + 1.0, WHITE); box(xR - 0.04, xR - 0.03, 0.12, 2.28, z + 0.07, z + 0.93, new THREE.MeshStandardMaterial({ color: '#faf9f6', roughness: 0.4 })); }
// mur gauche : porte affleurante
box(xL, xL + 0.03, 0, 2.3, 0.4, 1.3, WHITE); box(xL + 0.03, xL + 0.035, 0, 2.3, 0.4, 0.404, M.gap, false);

// ================= PROPOSITION KAÏRA =================
// 1. Plafond architectural : faux plafond périphérique à 2,60 m, caisson central à 2,80 m avec gorge LED,
//    bande de lames chêne dans l'axe du marbre (1,20 m) qui prolonge le mur au-dessus du lit.
const TX0 = -1.55, TX1 = 1.55, TZ0 = 0.0, TZ1 = 3.3;
box(xL, xR, DROP, CEIL + 0.1, TZ1, RD, WHITE);                                    // retombée côté pied
box(xL, TX0, DROP, CEIL + 0.1, 0, TZ1, WHITE); box(TX1, xR, DROP, CEIL + 0.1, 0, TZ1, WHITE);
box(TX0, TX1, CEIL, CEIL + 0.1, 0, TZ1, WHITE);                                    // fond du caisson
for (const [a, b, c, d] of [[TX0 - 0.002, TX0 + 0.01, TZ0, TZ1], [TX1 - 0.01, TX1 + 0.002, TZ0, TZ1]]) box(a, b, DROP - 0.002, DROP + 0.002, c, d, M.gap, false);
{ const cove = (x0, x1, z0, z1) => { const s = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, 0.006, z1 - z0), M.glow); s.position.set((x0 + x1) / 2, DROP + 0.05, (z0 + z1) / 2); scene.add(s); };
  cove(TX0 - 0.06, TX0 - 0.05, 0.1, TZ1 - 0.05); cove(TX1 + 0.05, TX1 + 0.06, 0.1, TZ1 - 0.05); cove(TX0, TX1, TZ1 + 0.05, TZ1 + 0.06);
  for (const [x, z] of [[TX0 + 0.1, 1.0], [TX0 + 0.1, 2.4], [TX1 - 0.1, 1.0], [TX1 - 0.1, 2.4], [0, TZ1 - 0.1]]) { const p = new THREE.PointLight('#ffcf96', 0.9, 2.2, 2); p.position.set(x, CEIL - 0.08, z); scene.add(p); } }
for (let x = -0.60; x < 0.60; x += 0.06) box(x + 0.005, x + 0.045, CEIL - 0.04, CEIL, 0, 2.3, OAK(0.05, 2));   // lames chêne au plafond
box(-0.62, 0.62, CEIL - 0.045, CEIL - 0.04, 2.3, 2.32, BRASS);
// 2. Tête de lit : panneau flottant 2 300 × 1 150, rembourré bouclé crème, cadre chêne + filet laiton ;
//    le marbre reste visible au-dessus (1 650 mm de marbre libre).
box(-1.15, 1.15, 0.30, 1.15, 0.04, 0.10, OAK(2, 1));
{ const hb = new THREE.Mesh(new RoundedBoxGeometry(2.20, 0.80, 0.10, 6, 0.04), new THREE.MeshStandardMaterial({ map: tex(512, 512, (g, w, h) => { g.fillStyle = '#ece4d6'; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 26000; i++) { g.fillStyle = shade('#ece4d6', rr(-0.12, 0.08)); g.globalAlpha = 0.5; g.fillRect(rnd() * w, rnd() * h, 3 * rnd() + 1, 3 * rnd() + 1); } }, 4, 2), roughness: 1 }));
  hb.position.set(0, 0.73, 0.14); hb.castShadow = hb.receiveShadow = true; scene.add(hb);
  for (const x of [-0.55, 0, 0.55]) box(x - 0.003, x + 0.003, 0.34, 1.12, 0.188, 0.19, M.gap, false); }
box(-1.15, 1.15, 1.15, 1.158, 0.04, 0.11, BRASS);
// 3. Lit 180 × 200 sur sommier tapissé (lin taupe), socle en retrait
const rb = (x0, x1, y0, y1, z0, z1, m, r = 0.05) => { const b = new THREE.Mesh(new RoundedBoxGeometry(x1 - x0, y1 - y0, z1 - z0, 4, r), m); b.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2); b.castShadow = b.receiveShadow = true; scene.add(b); };
const LIN = c => new THREE.MeshStandardMaterial({ color: c, roughness: 1 });
box(-0.88, 0.88, 0, 0.08, 0.25, 2.30, M.gap);
rb(-0.95, 0.95, 0.08, 0.34, 0.19, 2.36, LIN('#9c8a78'), 0.04);
rb(-0.90, 0.90, 0.34, 0.58, 0.22, 2.30, LIN('#f3efe8'));
rb(-0.93, 0.93, 0.52, 0.64, 0.75, 2.34, LIN('#f6f3ee'), 0.06);
rb(-0.95, 0.95, 0.60, 0.67, 1.85, 2.28, new THREE.MeshPhysicalMaterial({ color: '#4b5a3e', roughness: 0.8, sheen: 1, sheenColor: new THREE.Color('#8fa07a') }), 0.04);   // plaid vert sauge (rappel du marbre)
for (const x of [-0.45, 0.45]) rb(x - 0.37, x + 0.37, 0.58, 1.02, 0.24, 0.42, LIN('#f7f4ef'), 0.08);
for (const x of [-0.42, 0.42]) rb(x - 0.28, x + 0.28, 0.60, 0.94, 0.40, 0.55, LIN('#dccfbb'), 0.07);
rb(-0.28, 0.28, 0.62, 0.86, 0.55, 0.69, new THREE.MeshStandardMaterial({ color: '#8a5a34', roughness: 0.6 }), 0.06);                // coussin cuir cognac
// 4. Suspensions de chevet : globe opalin + tige laiton, 1 400 mm du sol
for (const cx of [-1.25, 1.25]) {
  box(cx - 0.004, cx + 0.004, 1.48, DROP, 0.24, 0.248, BRASS, false);
  const glb = new THREE.Mesh(new THREE.SphereGeometry(0.11, 48, 32), new THREE.MeshStandardMaterial({ color: '#fff4e2', emissive: '#ffd39a', emissiveIntensity: 1.6, roughness: 0.4 }));
  glb.position.set(cx, 1.38, 0.244); scene.add(glb);
  const l = new THREE.PointLight('#ffc98a', 2.6, 3.5, 2); l.position.set(cx, 1.30, 0.30); l.castShadow = false; scene.add(l);
  cyl(cx + 0.12, 0.25, 0.07, 0.48, 0.52, BRASS, 0.08); box(cx - 0.18, cx + 0.02, 0.48, 0.52, 0.12, 0.32, LIN('#2f2924'));
}
// 5. Tapis laine 3 000 × 2 400 + banc en bout de lit
box(-1.5, 1.5, 0, 0.012, 0.9, 3.3, new THREE.MeshStandardMaterial({ color: '#d4c6b0', roughness: 1 }), false);
rb(-0.70, 0.70, 0.40, 0.48, 2.50, 2.92, new THREE.MeshPhysicalMaterial({ color: '#4b5a3e', roughness: 0.8, sheen: 1, sheenColor: new THREE.Color('#8fa07a') }), 0.04);
box(-0.66, 0.66, 0.36, 0.40, 2.53, 2.89, OAK(1, 0.2));
for (const x of [-0.62, 0.62]) for (const z of [2.56, 2.86]) cyl(x, z, 0.015, 0, 0.36, BRASS);

// ---------- lumière d'ambiance ----------
scene.add(new THREE.HemisphereLight('#f6efe4', '#a08060', 0.35));
const win = new THREE.DirectionalLight('#ffe9cc', 1.0); win.position.set(4, 3.5, 3); win.castShadow = true; win.shadow.mapSize.set(4096, 4096); win.shadow.bias = -0.0004;
Object.assign(win.shadow.camera, { left: -5, right: 5, top: 5, bottom: -2, near: 0.5, far: 15 }); scene.add(win);
for (const x of [-0.35, 0.35]) { const s = new THREE.SpotLight('#ffd4a0', 5, 4, 0.35, 0.7, 2); s.position.set(x, DROP - 0.02, 0.75); s.target.position.set(x * 0.5, 1.6, 0.0); scene.add(s, s.target); }   // rasants sur le marbre

const VIEWS = { front: { pos: [0.0, 1.40, 4.45], look: [0, 1.25, 0], fov: 62 },
                angle: { pos: [1.55, 1.45, 3.9], look: [-0.5, 0.95, 0.4], fov: 58 },
                ceiling: { pos: [0.6, 1.2, 3.8], look: [-0.1, 2.1, 0.8], fov: 64 } };
const V = VIEWS[VIEW] || VIEWS.front;
const cam = new THREE.PerspectiveCamera(V.fov, W / H, 0.05, 50); cam.position.set(...V.pos); cam.lookAt(...V.look);
const comp = new EffectComposer(renderer); comp.addPass(new RenderPass(scene, cam));
const ao = new GTAOPass(scene, cam, W, H); ao.updateGtaoMaterial({ radius: 0.25, scale: 1.2, samples: 16 }); ao.blendIntensity = 0.85; comp.addPass(ao);
comp.addPass(new OutputPass()); comp.render(); window.__done = true;
