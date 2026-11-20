"""Fiche technique console LIGNE : élévation + coupe (mm)."""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "renders"
S = 0.25                      # px per mm
WALL, CH, TOP, D, TH = 1400, 2800, 800, 350, 40
CX0, CX1 = 100, 1300
MW, MH, MZ = 620, 1050, 1180
ex, ey = 120, 120            # elevation origin (top-left of ceiling line)
def X(x): return ex + x * S
def Y(z): return ey + (CH - z) * S
L = []
def r(x0, z0, x1, z1, fill="none", st="#2b2622", w=1.4, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    L.append(f'<rect x="{X(x0):.1f}" y="{Y(z1):.1f}" width="{(x1-x0)*S:.1f}" height="{(z1-z0)*S:.1f}" fill="{fill}" stroke="{st}" stroke-width="{w}"{d}/>')
def t(x, y, s, size=13, anchor="middle", col="#3a2f28", fam="Helvetica"):
    L.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{col}" font-family="{fam}">{s}</text>')
def dimh(x0, x1, ypx, label):
    L.append(f'<line x1="{X(x0):.1f}" y1="{ypx}" x2="{X(x1):.1f}" y2="{ypx}" stroke="#7a4a2a" stroke-width="1"/>')
    for x in (x0, x1): L.append(f'<line x1="{X(x):.1f}" y1="{ypx-6}" x2="{X(x):.1f}" y2="{ypx+6}" stroke="#7a4a2a"/>')
    t((X(x0)+X(x1))/2, ypx-5, label, 12, col="#7a4a2a")
def dimv(xpx, z0, z1, label):
    L.append(f'<line x1="{xpx}" y1="{Y(z0):.1f}" x2="{xpx}" y2="{Y(z1):.1f}" stroke="#7a4a2a" stroke-width="1"/>')
    for z in (z0, z1): L.append(f'<line x1="{xpx-6}" y1="{Y(z):.1f}" x2="{xpx+6}" y2="{Y(z):.1f}" stroke="#7a4a2a"/>')
    L.append(f'<text x="{xpx-8}" y="{(Y(z0)+Y(z1))/2:.1f}" font-size="12" fill="#7a4a2a" font-family="Helvetica" text-anchor="middle" transform="rotate(-90 {xpx-8} {(Y(z0)+Y(z1))/2:.1f})">{label}</text>')

# ----- ÉLÉVATION -----
t(ex, ey - 40, "ÉLÉVATION", 15, "start", fam="Georgia")
r(-450, 0, 0, 2200, "#efe9df"); t(X(-225), Y(1100), "PORTE", 12, col="#8a7a6a")
r(0, 0, WALL, CH, "#f3ece2")
for x in range(15, WALL, 30): L.append(f'<line x1="{X(x):.1f}" y1="{Y(CH-10):.1f}" x2="{X(x):.1f}" y2="{Y(20):.1f}" stroke="#c9b49a" stroke-width="0.6"/>')
r(0, 0, WALL, 20, "#2b2622")
# mirror arch
cx, rad = X(WALL/2), MW/2*S
L.append(f'<path d="M{cx-rad:.1f},{Y(MZ):.1f} L{cx-rad:.1f},{Y(MZ+MH-MW/2):.1f} A{rad:.1f},{rad:.1f} 0 0 1 {cx+rad:.1f},{Y(MZ+MH-MW/2):.1f} L{cx+rad:.1f},{Y(MZ):.1f} Z" fill="#e6d6bd" stroke="#8a6a43" stroke-width="3"/>')
# console
r(CX0, TOP-TH, CX1, TOP, "#e4d6bf"); r(CX0+40, TOP-TH-140, CX1-320, TOP-TH, "#7a5a44")
L.append(f'<line x1="{X(CX0+60):.1f}" y1="{Y(TOP-TH-135):.1f}" x2="{X(CX1-340):.1f}" y2="{Y(TOP-TH-135):.1f}" stroke="#c9a46a" stroke-width="2"/>')
r(CX1-290, 0, CX1-30, TOP-TH, "#e4d6bf")
L.append(f'<line x1="{X(CX0+50):.1f}" y1="{Y(TOP-TH-2):.1f}" x2="{X(CX1-50):.1f}" y2="{Y(TOP-TH-2):.1f}" stroke="#f0b860" stroke-width="2" stroke-dasharray="3 2"/>')
dimh(0, WALL, Y(CH) - 18, "1400 (mur, à confirmer)")
dimh(CX0, CX1, Y(TOP) - 50, "1200")
dimh(0, CX0, Y(TOP) - 50, "100"); dimh(CX1, WALL, Y(TOP) - 50, "100")
dimh(CX1-290, CX1-30, Y(0) + 22, "Ø 260")
dimh(WALL/2 - MW/2, WALL/2 + MW/2, Y(MZ + MH) - 14, "620")
dimv(X(WALL) + 40, 0, TOP, "800"); dimv(X(WALL) + 40, MZ, MZ + MH, "1050")
dimv(X(WALL) + 70, 0, MZ, "1180"); dimv(X(WALL) + 40, MZ + MH, CH, "570")

# ----- COUPE -----
sx = X(WALL) + 230
def XS(d): return sx + d * S
t(sx, ey - 40, "COUPE A-A", 15, "start", fam="Georgia")
L.append(f'<rect x="{XS(-120):.1f}" y="{Y(CH):.1f}" width="{120*S:.1f}" height="{CH*S:.1f}" fill="url(#hatch)" stroke="#2b2622"/>')
L.append(f'<rect x="{XS(0):.1f}" y="{Y(CH-10):.1f}" width="{60*S:.1f}" height="{(CH-30)*S:.1f}" fill="#8a6a50" stroke="#2b2622"/>')
L.append(f'<rect x="{XS(60):.1f}" y="{Y(MZ+MH):.1f}" width="{25*S:.1f}" height="{MH*S:.1f}" fill="#c9a46a" stroke="#2b2622"/>')
L.append(f'<rect x="{XS(60):.1f}" y="{Y(TOP):.1f}" width="{D*S:.1f}" height="{TH*S:.1f}" fill="#e4d6bf" stroke="#2b2622"/>')
L.append(f'<rect x="{XS(60):.1f}" y="{Y(TOP-TH):.1f}" width="{(D-30)*S:.1f}" height="{140*S:.1f}" fill="#7a5a44" stroke="#2b2622"/>')
L.append(f'<rect x="{XS(60+D/2-130):.1f}" y="{Y(TOP-TH):.1f}" width="{260*S:.1f}" height="{(TOP-TH)*S:.1f}" fill="#e4d6bf" stroke="#2b2622" stroke-dasharray="4 3"/>')
L.append(f'<path d="M{XS(-60):.1f},{Y(TOP-TH-150):.1f} L{XS(260):.1f},{Y(TOP-TH-5):.1f}" stroke="#1d1b19" stroke-width="2.5" stroke-dasharray="6 3"/>')
t(XS(-130), Y(TOP-TH-150)+4, "équerre acier cachée", 11, "end", col="#1d1b19")
L.append(f'<line x1="{XS(60)}" y1="{Y(TOP)+-30}" x2="{XS(60+D)}" y2="{Y(TOP)-30}" stroke="#7a4a2a"/>'); t(XS(60+D/2), Y(TOP)-35, "350", 12, col="#7a4a2a")
L.append(f'<line x1="{XS(0)}" y1="{Y(CH)-12}" x2="{XS(60)}" y2="{Y(CH)-12}" stroke="#7a4a2a"/>'); t(XS(30), Y(CH)-17, "60", 12, col="#7a4a2a")

# ----- NOMENCLATURE -----
nx = XS(560)
items = [
 ("A", "Habillage mural", "Cannelures noyer massif ou plaqué, demi-ronds 30 mm, vernis mat 10 %. Ép. 60 mm. Joint creux 10 mm côté porte, plafond et sol."),
 ("B", "Miroir arche", "620 × 1050, verre miroir bronze clair 6 mm, cadre laiton brossé 10 mm, LED halo 2700 K à l'arrière."),
 ("C", "Plateau", "Travertin Classico adouci, rebouché, 1200 × 350, chant 40 mm en onglet. Hauteur 800."),
 ("D", "Tiroir suspendu", "Noyer, 840 × 140, coulisses à sortie totale + ouverture par poussée, lèvre laiton (prise)."),
 ("E", "Pied sculptural", "Colonne travertin plein Ø 260, H 760, collée et goujonnée sous le plateau."),
 ("F", "Lumière", "Ruban LED 2700 K IRC ≥ 90 sous le plateau, profilé diffusant, variateur."),
 ("G", "Fixation", "Équerres acier noyées dans le mur (mur porteur ou renfort à valider)."),
]
t(nx, ey - 40, "NOMENCLATURE", 15, "start", fam="Georgia")
y = ey
for k, h, d in items:
    L.append(f'<circle cx="{nx+9}" cy="{y-4}" r="10" fill="#7a4a2a"/>'); t(nx+9, y, k, 11, col="#fff")
    t(nx+28, y, h, 14, "start", fam="Georgia")
    words, line, yy = d.split(), "", y + 20
    for w_ in words:
        if len(line + w_) > 52: t(nx+28, yy, line, 12, "start", col="#6a5a4c"); yy += 17; line = ""
        line += w_ + " "
    t(nx+28, yy, line, 12, "start", col="#6a5a4c"); y = yy + 32
title = ('<text x="120" y="915" font-family="Georgia" font-size="28" letter-spacing="7" fill="#2b2622">KAÏRA</text>'
         '<text x="270" y="915" font-family="Helvetica" font-size="14" fill="#7a6a5c">Console LIGNE — mur habillé · fiche technique v1 · cotes en mm · à vérifier sur site</text>')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="950" viewBox="0 0 1500 950">
<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#9c8a74" stroke-width="1"/></pattern></defs>
<rect width="1500" height="950" fill="#fbf8f3"/>{"".join(L)}{title}</svg>'''
(OUT / "console-fiche-technique.svg").write_text(svg, encoding="utf-8")
