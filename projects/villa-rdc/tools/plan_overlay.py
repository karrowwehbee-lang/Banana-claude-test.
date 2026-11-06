"""Draws the KAÏRA furniture layout on top of the original ground-floor plan.

Furniture is defined in centimetres (origin = inner south-west corner of the
living room, x east, y north) and converted to plan pixels, so the original
architecture is reproduced untouched underneath.
"""
import base64, pathlib

HERE = pathlib.Path(__file__).resolve().parent.parent
S = 1.081           # cm per pixel (checked against the 1122 / 424 / 315.8 dimensions)
OX, OY = 267, 963   # pixel position of the origin

def px(x, y):
    return OX + x / S, OY - y / S

def rect(x, y, w, h, fill, stroke="#2b2622", rx=0, dash=None, op=1):
    X, Y = px(x, y + h)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{X:.1f}" y="{Y:.1f}" width="{w/S:.1f}" height="{h/S:.1f}" rx="{rx/S:.1f}" '
            f'fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="1.4"{d}/>')

def circ(x, y, r, fill, stroke="#2b2622", dash=None, op=1):
    X, Y = px(x, y)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r/S:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="1.4"{d}/>'

def ell(x, y, rx, ry, fill):
    X, Y = px(x, y)
    return f'<ellipse cx="{X:.1f}" cy="{Y:.1f}" rx="{rx/S:.1f}" ry="{ry/S:.1f}" fill="{fill}" stroke="#2b2622" stroke-width="1.4"/>'

def tag(x, y, n):
    X, Y = px(x, y)
    return (f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="11" fill="#7a4a2a"/>'
            f'<text x="{X:.1f}" y="{Y+4:.1f}" font-size="12" fill="#fff" text-anchor="middle" font-family="Helvetica" font-weight="700">{n}</text>')

def label(x, y, t, size=15):
    X, Y = px(x, y)
    return f'<text x="{X:.1f}" y="{Y:.1f}" font-size="{size}" fill="#3a2f28" text-anchor="middle" font-family="Georgia" letter-spacing="2">{t}</text>'

# palette
STONE, OAK, WAL, FAB, RUG, BRZ, GRN = "#d9c7ad", "#8a6a4f", "#5b3f2c", "#ece4d8", "#f3ede4", "#9a7b4f", "#3f5246"

el = []
# ---------- Salon principal ----------
el += [rect(50, 42, 300, 340, RUG, stroke="#b8a68f", dash="6 4"),            # rug
       rect(0, 72, 40, 280, STONE),                                          # 1 travertine fire/media wall
       rect(230, 62, 100, 300, FAB, rx=45),                                  # 2 curved sofa
       rect(300, 62, 30, 300, "#ddd2c2", rx=15),
       ell(152, 212, 32, 75, STONE),                                         # 3 coffee table
       circ(150, 58, 40, FAB), circ(150, 366, 40, FAB),                      # 4 swivel chairs
       rect(330, 112, 35, 200, WAL),                                         # 5 console
       rect(367, 0, 268, 55, STONE, stroke="#9c8a74", dash="4 3", op=.5),    # 6 stone threshold
       circ(490, 230, 60, "none", stroke=BRZ, dash="5 4"),                   # 7 sculptural pendant
       rect(603, 378, 42, 42, STONE),                                        # 8 sculpture plinth
       rect(760, 229, 391, 40, WAL), rect(1111, 32, 40, 197, WAL),           # 9 walnut library
       rect(940, 231, 110, 36, BRZ),                                         # bar niche
       circ(895, 82, 42, GRN), circ(1035, 82, 42, GRN), circ(965, 70, 25, STONE),  # 10 lounge chairs
      ]
el += [tag(20, 212, 1), tag(280, 212, 2), tag(152, 212, 3), tag(150, 366, 4), tag(347, 212, 5),
       tag(500, 28, 6), tag(490, 230, 7), tag(624, 399, 8), tag(840, 249, 9), tag(965, 70, 10)]
el += [label(500, 330, "SALON PRINCIPAL", 17), label(500, 305, "≈ 41.5 m²", 12),
       label(955, 180, "LIBRARY LOUNGE", 13)]
# main circulation (entrance → stair / hall)
a, b, c = px(500, 10), px(560, 230), px(715, 410)
el.append(f'<path d="M{a[0]:.0f},{a[1]:.0f} Q{b[0]:.0f},{b[1]:.0f} {c[0]:.0f},{c[1]:.0f}" fill="none" '
          f'stroke="#b5462f" stroke-width="2.2" stroke-dasharray="8 6" marker-end="url(#arr)"/>')

# ---------- Chambre d'amis ----------
el += [rect(872, 600, 240, 200, RUG, stroke="#b8a68f", dash="6 4"),
       rect(836, 549, 315, 9, "#6b5a4a"),                                    # 11 upholstered headboard wall
       rect(907, 558, 170, 210, FAB, rx=4),                                  # 12 bed 160x200
       rect(917, 568, 70, 35, "#fff", rx=6), rect(997, 568, 70, 35, "#fff", rx=6),
       rect(907, 680, 170, 88, "#c9b79d", rx=3),                             # throw
       rect(857, 560, 45, 40, OAK), rect(1082, 560, 45, 40, OAK),            # 13 floating nightstands
       rect(836, 741, 65, 130, OAK, op=.85),                                 # 14 existing wardrobe, refaced
       rect(1101, 725, 50, 110, WAL), circ(1072, 780, 22, GRN),              # 15 desk / vanity
      ]
el += [tag(990, 553, 11), tag(992, 720, 12), tag(880, 580, 13), tag(868, 806, 14), tag(1126, 780, 15),
       label(992, 835, "CHAMBRE D'AMIS", 13), label(992, 815, "≈ 10.2 m²", 11)]

legend = [
 "1  Travertine fireplace + hidden TV wall, 280 × 40",
 "2  Curved bouclé sofa, 300 × 100",
 "3  Oval travertine coffee table, 150 × 65 × 34",
 "4  Pair of swivel lounge chairs, Ø80",
 "5  Walnut console behind sofa, 200 × 35 × 72",
 "6  Honed stone threshold inlay (floor)",
 "7  Sculptural bronze pendant, Ø120",
 "8  Travertine plinth + sculpture, 42 × 42",
 "9  Walnut library wall + bronze bar niche (40 deep)",
 "10 Two green velvet lounge chairs + side table",
 "11 Upholstered acoustic headboard wall",
 "12 Bed 160 × 200 (frame 170 × 210)",
 "13 Floating oak nightstands, 45 × 40",
 "14 Existing wardrobe, refaced in smoked oak",
 "15 Writing desk / vanity 110 × 50 at window",
]
lx = 1735
leg = [f'<text x="{lx}" y="70" font-family="Georgia" font-size="34" letter-spacing="8" fill="#2b2622">KAÏRA</text>',
       f'<text x="{lx}" y="96" font-family="Helvetica" font-size="13" letter-spacing="3" fill="#7a6a5c">INTERIOR DESIGN</text>',
       f'<line x1="{lx}" y1="116" x2="{lx+400}" y2="116" stroke="#b8a68f"/>',
       f'<text x="{lx}" y="150" font-family="Georgia" font-size="20" fill="#2b2622">Villa — Ground floor</text>',
       f'<text x="{lx}" y="174" font-family="Helvetica" font-size="13" fill="#7a6a5c">Furniture layout · concept v1 · cm</text>']
for i, t in enumerate(legend):
    leg.append(f'<text x="{lx}" y="{220+i*30}" font-family="Helvetica" font-size="14" fill="#3a2f28">{t}</text>')
y0 = 220 + len(legend) * 30 + 20
leg += [f'<line x1="{lx}" y1="{y0}" x2="{lx+40}" y2="{y0}" stroke="#b5462f" stroke-width="2.2" stroke-dasharray="8 6"/>',
        f'<text x="{lx+52}" y="{y0+5}" font-family="Helvetica" font-size="14" fill="#3a2f28">Main circulation kept ≥ 120 cm clear</text>',
        f'<text x="{lx}" y="{y0+40}" font-family="Helvetica" font-size="12" fill="#7a6a5c">Architecture as supplied — walls, openings and</text>',
        f'<text x="{lx}" y="{y0+58}" font-family="Helvetica" font-size="12" fill="#7a6a5c">staircase unchanged. Openings to confirm on site.</text>']

img = base64.b64encode((HERE / "source/plan-rdc-clean.png").read_bytes()).decode()
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2180" height="1092" viewBox="0 0 2180 1092">
<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">
<path d="M0,0 L10,5 L0,10 z" fill="#b5462f"/></marker></defs>
<rect width="2180" height="1092" fill="#fbf8f3"/>
<image href="data:image/png;base64,{img}" x="0" y="0" width="1713" height="1092" opacity="0.9"/>
{''.join(el)}
{''.join(leg)}
</svg>'''
out = HERE / "renders/plan-layout-rdc.svg"
out.parent.mkdir(exist_ok=True)
out.write_text(svg)
print(out)
