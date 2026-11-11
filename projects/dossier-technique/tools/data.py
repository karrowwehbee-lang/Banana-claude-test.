"""KAÏRA — Dossier technique d'architecture intérieure : données relevées.

Every value carries a status:
  'v' = vérifiée : cote écrite sur le plan coté source (plan-rdc-cote-2D)
  'd' = déduite  : relevée à l'échelle sur un plan ou mesurée sur un rendu frontal (méthode dans README.md)
  'c' = à confirmer : impossible à déterminer avec précision à partir des documents du projet

Units: centimetres. Plan coordinates: X towards the east, Y towards the north.

Sources
  RDC architecture  : sources/plans/plan-rdc-cote-2D.png (scale 1,080 cm/px, checked on 16 written dimensions)
  RDC furniture     : sources/plans/plan-rdc-amenagement.png (top view of the 3D model, 1,507 cm/px;
                      software grid = 100,0 cm, registered on the 2D plan outline)
  Étage 1           : sources/plans/plan-etage1-amenagement.png (top view, same 1 m grid -> 1,805 cm/px)
  Heights, elevations: frontal renders, wall plane calibrated on a plan dimension (see ELEV_SOURCES)
"""

# ---------------------------------------------------------------- conversions
S_RDC = 1.080          # cm per px, 2D plan
O_RDC = (267, 963)     # px of the inner south-west corner of the living room (origin)


def rdc(px, py):
    return ((px - O_RDC[0]) * S_RDC, (O_RDC[1] - py) * S_RDC)


def tv_rdc(u, v):
    """RDC top view (3D model) -> plan cm."""
    return rdc(248 + (u - 31) * 1.395, 138 + (v - 46) * 1.395)


S_ET = 1.805           # cm per px, first-floor top view (1 m grid = 55,4 px)


def et(u, v):
    return ((u - 44.5) * S_ET, (505 - v) * S_ET)


def rect_rdc(x0, x1, y0, y1):
    (a, b), (c, d) = rdc(x0, y1), rdc(x1, y0)
    return (a, b, c, d)          # X0, Y0, X1, Y1 (Y0 < Y1)


def rect_tv(u0, u1, v0, v1):
    (a, b), (c, d) = tv_rdc(u0, v1), tv_rdc(u1, v0)
    return (a, b, c, d)


def rect_et(u0, u1, v0, v1):
    (a, b), (c, d) = et(u0, v1), et(u1, v0)
    return (a, b, c, d)


# ---------------------------------------------------------------- RDC architecture (2D plan, px rectangles)
RDC_WALLS = [  # (x0, x1, y0, y1, kind)  kind: 'ext' exterior wall, 'int' interior wall
    (248, 1350, 138, 157, "ext"), (248, 1350, 963, 982, "ext"),
    (248, 267, 138, 982, "ext"), (1332, 1350, 138, 982, "ext"),
    (359, 378, 157, 552, "int"), (815, 834, 157, 552, "int"),
    (267, 359, 419, 438, "int"),
    (267, 873, 552, 570, "int"), (873, 890, 552, 611, "int"),
    (834, 958, 258, 277, "int"), (1026, 1040, 258, 277, "int"), (1031, 1040, 157, 277, "int"),
    (834, 880, 407, 426, "int"), (958, 1043, 407, 426, "int"),
    (1043, 1060, 398, 474, "int"), (1060, 1332, 455, 474, "int"),
    (970, 989, 547, 714, "int"), (970, 1332, 695, 714, "int"),
    (1306, 1332, 933, 963, "int"),
]
# openings cut in walls: (wall axis 'h' or 'v', from, to, wall px band (a, b), kind, label, status)
RDC_OPENINGS = [
    ("h", 510, 643, (138, 157), "window", None, "d"),          # north window of the room outside the scope
    ("h", 617, 808, (552, 570), "glazed", "Baie vitrée 206,8", "v"),
    ("v", 572, 633, (248, 267), "window", "F1", "d"),
    ("v", 900, 961, (248, 267), "window", "F2", "d"),
    ("h", 607.5, 758.5, (963, 982), "door", "Porte d'entrée", "d"),
    ("h", 855, 922, (963, 982), "window", "F3", "d"),
    ("h", 1029, 1134, (963, 982), "window", "F4", "d"),
    ("v", 184, 297, (1332, 1350), "window", "F5", "d"),
    ("h", 880, 958, (407, 426), "door", "Porte ch. d'amis", "d"),
    ("h", 958, 1026, (258, 277), "door", None, "d"),
]
RDC_STAIR = dict(x0=989, x1=1343, y_up=(478, 570), y_mid=(570, 596), y_low=(596, 691),
                 treads=[989 + i * 25.8 for i in range(11)], landing=(1247, 1343))

# Written dimensions of the source plan (all 'v'): (label, value, px from, px to, axis, offset side)
RDC_GIVEN = {
    "1122": 1122.0, "472": 472.0, "315.8": 315.8, "426.6": 426.6, "424": 424.0, "303.6": 303.6,
    "130": 130.0, "322.2": 322.2, "378.1": 378.1, "206.8": 206.8, "69.8": 69.8,
    "85.8": 85.8, "142": 142.0, "163": 163.0, "237": 237.0, "32": 32.0,
}

# ---------------------------------------------------------------- rooms
H_SEJ = 284     # 'd' : rendus 07 (282-288), 08 (286), 10 (284), 09 (cohérent) -> 284
H_AMIS = 285    # 'd' : rendus chambre-amis-02 (285) et -01 (cohérent)
H_ET_SEJ = 289  # 'd' : rendu etage1-sejour-01 (largeur de mur issue de la vue de dessus)
H_PRINC = 292   # 'd' : rendu chambre-principale-05 (±5)

ROOMS = {
    "sejour": dict(
        level="RDC", name="Séjour — salon et salle à manger", short="Séjour RDC", height=H_SEJ,
        poly=[(0, 0), (1122.1, 0), (1122.1, 32.4), (1150.2, 32.4), (1150.2, 268.9), (759.2, 268.9),
              (759.2, 424.4), (672.8, 424.4), (672.8, 380.2), (654.5, 380.2), (654.5, 424.4), (0, 424.4)],
        sources=["rdc-salon-01 … 11", "plan-rdc-cote-2D", "plan-rdc-amenagement"],
    ),
    "amis": dict(
        level="RDC", name="Chambre d'amis", short="Chambre d'amis", height=H_AMIS,
        poly=[(856.4, 548.6), (1150.2, 548.6), (1150.2, 870.5), (834.8, 870.5), (834.8, 740.9),
              (612.4, 740.9), (612.4, 600.5), (838.1, 600.5), (838.1, 610.2), (856.4, 610.2)],
        sources=["chambre-amis-01 … 04", "plan-rdc-cote-2D", "plan-rdc-amenagement"],
    ),
    "etsejour": dict(
        level="ÉTAGE 1", name="Séjour de l'étage", short="Séjour étage 1", height=H_ET_SEJ,
        poly=[(0, 0), (402.5, 0), (402.5, 524.4), (0, 524.4)],
        sources=["etage1-sejour-01 … 09", "plan-etage1-amenagement"],
    ),
    "princ": dict(
        level="ÉTAGE 1", name="Chambre principale", short="Chambre principale", height=H_PRINC,
        poly=[(816.3, -126.4), (1499.5, -126.4), (1499.5, 250.9), (605.6, 250.9), (605.6, 128.2),
              (816.3, 128.2)],
        sources=["chambre-principale-01 … 05", "plan-etage1-amenagement"],
    ),
}

# ---------------------------------------------------------------- furniture (plan) — all 'd' (top views)
def _circ(c, r, conv):
    x, y = conv(*c)
    return ("circ", x, y, r * (1.507 if conv is tv_rdc else S_ET))


FURN = {
    "sejour": [
        ("rect", rect_tv(45, 323, 394, 630), "rug", "Tapis"),
        ("rect", rect_tv(464, 701, 485, 628), "rug", "Tapis"),
        ("rect", rect_tv(123, 295, 356, 377.5), "custom", "M1"),
        ("rect", rect_tv(51, 107, 400, 532), "sofa", "Canapé modulaire crème"),
        ("rect", rect_tv(105, 288, 553, 626), "sofa", "Canapé modulaire cuir taupe"),
        ("rect", rect_tv(148, 246, 450, 527), "table", "Tables basses gigognes"),
        ("rect", rect_tv(505, 666, 523, 586), "table", "Table travertin"),
        ("rect", rect_tv(787, 807, 515, 600), "custom", "M4"),
        ("rect", rect_tv(667, 790, 616, 636), "custom", "M3"),
        _circ((455, 371), 12, tv_rdc) + ("deco", "Jarre"),
        _circ((712, 478), 14, tv_rdc) + ("deco", "Olivier"),
    ] + [_circ((u, v), 11, tv_rdc) + ("chair", "") for u, v in
         [(550, 509), (600, 509), (646, 509), (550, 602), (600, 602), (646, 602), (487, 555), (683, 555)]],
    "amis": [
        ("rect", rect_tv(647, 757, 65, 185), "bed", "Lit plateforme"),
        ("rect", rect_tv(612, 806, 245, 271), "custom", "M6"),
        ("rect", rect_tv(450, 484, 145, 238), "custom", "M8"),
        _circ((622, 87), 16, tv_rdc) + ("deco", "Chevet"),
        _circ((778, 87), 15, tv_rdc) + ("deco", "Chevet"),
        _circ((774, 232), 15, tv_rdc) + ("deco", "Pouf"),
    ],
    "etsejour": [
        ("rect", rect_et(77, 251, 321, 465), "rug", "Tapis"),
        ("rect", rect_et(79, 235, 216, 234), "custom", "M9"),
        ("rect", rect_et(252.5, 267.5, 415.4, 505), "custom", "M10"),
        ("rect", rect_et(75, 245, 410, 464), "sofa", "Canapé d'angle"),
        ("rect", rect_et(141, 203, 345, 386), "table", "Tables basses"),
        _circ((92, 342), 20, et) + ("chair", "Fauteuil"),
        _circ((245, 357), 12, et) + ("deco", "Pouf"),
        _circ((67, 227), 10, et) + ("deco", "Plante"),
        _circ((250, 230), 10, et) + ("deco", "Plante"),
    ],
    "princ": [
        ("rect", rect_et(730, 867, 405, 537), "bed", "Lit"),
        ("rect", rect_et(715, 737, 435, 502), "sofa", "Banc"),
        ("rect", rect_et(630, 646, 422, 515), "custom", "M13"),
        ("rect", rect_et(497, 536, 445, 573), "custom", "M12"),
        ("rect", rect_et(385, 410, 370, 402), "chair", "Fauteuil"),
    ],
}

# ---------------------------------------------------------------- first floor architecture (top view px rectangles)
ET_WALLS = [
    (35, 44, 14, 514, "ext"), (35, 689, 14, 24, "ext"), (679, 689, 14, 214, "ext"),
    (35, 885, 205, 214, "int"), (875, 885, 205, 584, "ext"), (35, 496, 505, 514, "ext"),
    (487, 496, 434, 584, "ext"), (487, 885, 575, 584, "ext"), (268, 277, 205, 514, "int"),
    (277, 875, 356, 366, "int"), (371, 380, 366, 443, "int"), (371, 527, 434, 443, "int"),
    (679, 689, 214, 357, "int"),
    (249, 258, 24, 109, "oos"), (371, 380, 24, 109, "oos"), (509, 518, 24, 109, "oos"),
    (249, 518, 109, 118, "oos"), (343, 407, 118, 205, "oos"),
]
ET_OPENINGS = [   # positions from renders / curtains of the 3D model — never written on a plan
    ("v", 251.6, 338.4, (268, 277), "door", "Porte double", "d"),        # etage1-sejour-08
    ("h", 55, 100, (505, 514), "window", "baie ?", "c"),                  # curtains only
    ("h", 170, 255, (505, 514), "window", "baie ?", "c"),
    ("v", 250, 500, (35, 44), "window", "baies ?", "c"),
    ("h", 570, 670, (575, 584), "window", "baie ?", "c"),
    ("h", 715, 810, (575, 584), "window", "baie ?", "c"),
    ("h", 800, 870, (356, 366), "glazed", "baie vitrée ?", "c"),           # chambre-principale-03 / -05
]

# ---------------------------------------------------------------- elevations
# element tuples
#   ('zone', x0, x1, z0, z1, mat)            wall finish zone
#   ('rzone', x0, x1, z0, z1, mat, corners)  rounded panel, corners = 'tl tr br bl' subset, radius 10
#   ('open', x0, x1, z0, z1, kind, label)    opening (kind: window, door, door2, glazed)
#   ('tv', x0, x1, z0, z1)
#   ('box', x0, x1, z0, z1, mat, label)      custom furniture / object in front of the wall
#   ('vline', x, z0, z1, kind)               kind: 'joint' | 'led'
#   ('hline', z, x0, x1, kind)
#   ('art', x0, x1, z0, z1, label)
#   ('note', x, z, text)                     callout text in the drawing
#   ('dash', x0, x1, z0, z1, label)          outline only, position indicative
# dims: list of chains ('h' or 'v', [(coord, status_of_segment_ending_here)...], offset level)

ELEV = {}

ELEV["sejour"] = {
    "A": dict(
        title="Mur A — Nord (mur TV)", width=654.7, view="Vue vers le nord", src="rdc-salon-07",
        calib="Baie vitrée 206,8 + trumeaux 378,1 / 69,8 (cotes du plan source) ; téléviseur 75\" contrôlé à ±1 %",
        els=[
            ("zone", 0, 43.7, 0, H_SEJ, "enduit"), ("hline", 224.2, 0, 43.7, "joint"),
            ("zone", 43.7, 102.5, 0, H_SEJ, "chene"), ("hline", 224.2, 43.7, 102.5, "joint"),
            ("zone", 102.5, 120.8, 0, H_SEJ, "miroir"),
            ("zone", 120.8, 176.0, 0, H_SEJ, "cannelure"),
            ("vline", 177.4, 0, H_SEJ, "led"),
            ("zone", 177.4, 347.4, 0, H_SEJ, "enduit"),
            ("rzone", 120.8, 176.0, 60.7, 225.2, "chene", "tr br"),
            ("rzone", 192.1, 347.4, 60.7, 225.2, "chene", "tl bl"),
            ("tv", 144.3, 311.5, 86.4, 179.2),
            ("box", 347.4, 382.3, 53.7, H_SEJ, "laque", "Colonne niches"),
            ("box", 352.0, 377.7, 117.2, 148.4, "niche", ""), ("box", 352.0, 377.7, 151.6, 186.1, "niche", ""),
            ("box", 352.0, 377.7, 188.4, 226.1, "niche", ""),
            ("box", 117.7, 377.0, 19.8, 53.7, "laque", "M1"),
            ("vline", 186.8, 19.8, 53.7, "joint"), ("vline", 315.0, 19.8, 53.7, "joint"),
            ("open", 378.1, 584.9, 0, 280.3, "glazed", "Porte vitrée 2 vantaux"),
            ("vline", 481.5, 0, 280.3, "joint"),
            ("zone", 584.9, 634.6, 0, H_SEJ, "chene"), ("hline", 224.2, 584.9, 634.6, "joint"),
            ("zone", 634.6, 654.7, 0, H_SEJ, "enduit"), ("hline", 224.2, 634.6, 654.7, "joint"),
        ],
        dims=[
            ("h", [(0, None), (378.1, "v"), (584.9, "v"), (654.7, "v")], 1),
            ("h", [(0, None), (43.7, "d"), (102.5, "d"), (120.8, "d"), (176.0, "d"), (192.1, "d"),
                   (347.4, "d"), (382.3, "d")], 2),
            ("h", [(117.7, None), (377.0, "d")], 3),
            ("t", [(144.3, None), (311.5, "d")], 1),
            ("v", [(0, None), (19.8, "d"), (53.7, "d"), (60.7, "d"), (86.4, "d"), (179.2, "d"),
                   (225.2, "d"), (H_SEJ, "d")], 1),
            ("v", [(0, None), (280.3, "d")], 2, 584.9),
        ],
        notes=["Plafond central au-dessus de la gorge lumineuse : hauteur à confirmer.",
               "M1 : meuble suspendu laqué crème, profondeur ≈ 32 (vue de dessus), 3 façades.",
               "Panneaux chêne arrondis rétroéclairés : épaisseur à confirmer."],
    ),
    "B": dict(
        title="Mur B — Nord (salle à manger, mur d'escalier)", width=390.8, view="Vue vers le nord",
        src="rdc-salon-06 (vue de 3/4)", calib="Segments 85,8 / 142 / 163 : cotes du plan source",
        els=[
            ("zone", 0, 390.8, 0, H_SEJ, "enduit"),
            ("vline", 85.8, 0, H_SEJ, "joint"), ("vline", 227.8, 0, H_SEJ, "joint"),
            ("note", 195, 150, "Grand tableau (personnage au chapeau) : position et dimensions à confirmer"),
            ("note", 195, 120, "Nature des segments 85,8 / 142 / 163 du plan source : à confirmer"),
        ],
        dims=[("h", [(0, None), (85.8, "v"), (227.8, "v"), (390.8, "v")], 1),
              ("v", [(0, None), (H_SEJ, "d")], 1)],
        notes=["Aucun rendu frontal de ce mur : seules les cotes du plan source sont reportées."],
    ),
    "C": dict(
        title="Mur C — Est (salle à manger)", width=236.5, view="Vue vers l'est", src="rdc-salon-01 (vue de 3/4)",
        calib="Longueur 237 : cote du plan source",
        els=[
            ("zone", 0, 236.5, 0, H_SEJ, "enduit"),
            ("dash", 84.5, 212.5, 70, 90, "M4 — console murale (emprise en plan relevée ; hauteur à confirmer)"),
            ("note", 118, 190, "Colonne marbre veiné + console : dimensions à confirmer"),
        ],
        dims=[("h", [(0, None), (236.5, "v")], 1), ("h", [(84.5, None), (212.5, "d")], 2),
              ("v", [(0, None), (H_SEJ, "d")], 1)],
        notes=["Console : longueur ≈ 128, profondeur ≈ 30 (vue de dessus). Hauteur de pose à confirmer."],
    ),
    "D": dict(
        title="Mur D — Sud (salle à manger, entrée, salon)", width=1122.1, view="Vue vers le sud",
        src="rdc-salon-08, -09, -10",
        calib="Porte d'entrée 163 (plan source) ; distance porte–fenêtre F3 vérifiée sur le rendu 10",
        els=[
            ("zone", 0, 1122.1, 0, H_SEJ, "enduit"),
            ("box", 0, 139.7, 0, H_SEJ, "chene", "M3 — bibliothèque"),
            ("box", 139.7, 184.7, 0, H_SEJ, "chene", ""),
            ("open", 184.7, 299.1, 100, 225, "window", "F4"), ("vline", 241.9, 100, 225, "joint"),
            ("zone", 299.1, 309.4, 0, H_SEJ, "chene"),
            ("dash", 312, 400, 89.5, 217.4, "Œuvre rouge (largeur à confirmer)"),
            ("zone", 403.9, 414.3, 0, H_SEJ, "chene"),
            ("open", 414.3, 487.1, 100, 225, "window", "F3"),
            ("hline", 229.5, 414.3, 581.1, "joint"), ("hline", 104, 414.3, 581.1, "joint"),
            ("vline", 487.1, 0, H_SEJ, "joint"),
            ("zone", 581.1, 591.3, 0, H_SEJ, "chene"),
            ("open", 591.3, 754.4, 0, 235, "door2", "Porte d'entrée 2 vantaux"),
            ("zone", 764.4, 825.0, 105, H_SEJ, "chene"), ("zone", 764.4, 825.0, 0, 105, "cannelure"),
            ("hline", 105, 764.4, 825.0, "led"),
            ("zone", 903.9, 965.6, 105, H_SEJ, "chene"), ("zone", 903.9, 965.6, 0, 105, "cannelure"),
            ("hline", 105, 903.9, 965.6, "led"),
            ("zone", 1044.6, 1107.0, 105, H_SEJ, "chene"), ("zone", 1044.6, 1107.0, 0, 105, "cannelure"),
            ("hline", 105, 1044.6, 1107.0, "led"),
        ],
        dims=[
            ("h", [(0, None), (1122.1, "v")], 1),
            ("h", [(0, None), (184.7, "d"), (299.1, "d"), (414.3, "d"), (487.1, "d"), (591.3, "d"),
                   (754.4, "d"), (1122.1, "d")], 2),
            ("h", [(754.4, None), (764.4, "d"), (825.0, "d"), (903.9, "d"), (965.6, "d"), (1044.6, "d"),
                   (1107.0, "d"), (1122.1, "d")], 3),
            ("v", [(0, None), (100, "d"), (225, "d"), (H_SEJ, "d")], 1, 184.7),
            ("v", [(0, None), (105, "d"), (235, "d"), (H_SEJ, "d")], 1, 1122.1),
        ],
        notes=["Fenêtres F3 et F4 : allège ≈ 100, linteau ≈ 225 (±5) relevés sur les rendus 09 et 10.",
               "Porte d'entrée : ≈ 163 × 235, deux vantaux bois foncé, sens d'ouverture à confirmer.",
               "M3 : bibliothèque chêne toute hauteur, profondeur ≈ 23 ; répartition des étagères à confirmer.",
               "Colonnes chêne : partie haute pleine, partie basse cannelée, ligne LED à ≈ 105."],
    ),
    "E": dict(
        title="Mur E — Ouest (mur tableau)", width=424.4, view="Vue vers l'ouest", src="rdc-salon-11",
        calib="Longueur 424 (plan source) ; hauteur cohérente avec les murs A et D",
        els=[
            ("zone", 0, 424.4, 0, H_SEJ, "enduit"),
            ("open", 2.2, 68.0, None, None, "window", "F2"),
            ("open", 356.4, 422.3, None, None, "window", "F1"),
            ("vline", 78.7, 0, H_SEJ, "joint"), ("vline", 116.6, 0, H_SEJ, "joint"),
            ("vline", 293.5, 0, H_SEJ, "joint"), ("vline", 325.4, 0, H_SEJ, "joint"),
            ("hline", 216.9, 78.7, 325.4, "joint"), ("hline", 273.8, 78.7, 325.4, "joint"),
            ("art", 136.9, 271.3, 21, 210.7, "Œuvre — ligne abstraite"),
            ("dash", 29.5, 76.9, 0, H_SEJ, "Rideau"), ("dash", 327.6, 376.8, 0, H_SEJ, "Rideau"),
        ],
        dims=[
            ("h", [(0, None), (424.4, "v")], 1),
            ("h", [(0, None), (2.2, "d"), (68.0, "d"), (78.7, "d"), (116.6, "d"), (293.5, "d"), (325.4, "d"),
                   (356.4, "d"), (422.3, "d"), (424.4, "d")], 2),
            ("t", [(136.9, None), (271.3, "d")], 1),
            ("v", [(0, None), (21, "d"), (210.7, "d"), (216.9, "d"), (273.8, "d"), (H_SEJ, "d")], 1),
        ],
        notes=["Fenêtres F1 et F2 : largeurs relevées sur le plan source ; allège et linteau à confirmer.",
               "Œuvre posée en partie basse (bas ≈ 21) : fixation à confirmer."],
    ),
}

ELEV["amis"] = {
    "A": dict(
        title="Mur A — Nord (tête de lit)", width=315.8, view="Vue vers le nord", src="chambre-amis-01",
        calib="Largeur 315,8 (plan source) ; hauteur recoupée sur le mur C",
        els=[
            ("zone", 0, 315.8, 0, H_AMIS, "panneau"),
            ("hline", 40.6, 0, 52.1, "joint"), ("hline", 40.6, 234.6, 315.8, "joint"),
            ("zone", 52.1, 87.0, 0, H_AMIS, "lames"),
            ("vline", 87.0, 0, H_AMIS, "joint"),
            ("zone", 229.0, 234.6, 55.4, H_AMIS, "miroir"),
            ("box", 64.6, 247.2, 0, 52.5, "tissu", "Tête de lit (lit plateforme)"),
            ("vline", 155.9, 0, 52.5, "joint"),
            ("dash", 298.0, 315.8, 0, H_AMIS, "Rideau"),
        ],
        dims=[("h", [(0, None), (315.8, "v")], 1),
              ("h", [(0, None), (52.1, "d"), (87.0, "d"), (229.0, "d"), (234.6, "d"), (315.8, "d")], 2),
              ("t", [(64.6, None), (247.2, "d")], 1),
              ("v", [(0, None), (40.6, "d"), (52.5, "d"), (55.4, "d"), (H_AMIS, "d")], 1)],
        notes=["Lames chêne verticales toute hauteur ; profil et pas des lames à confirmer.",
               "Fente miroir verticale (≈ 6 cm) : épaisseur et fixation à confirmer."],
    ),
    "B": dict(
        title="Mur B — Est (fenêtre)", width=322.2, view="Vue vers l'est", src="chambre-amis-03 (vue de 3/4)",
        calib="Longueur 322,2 et fenêtre : plan source",
        els=[
            ("zone", 0, 322.2, 0, H_AMIS, "panneau"),
            ("open", 29.2, 151.2, None, None, "window", "F5"),
            ("dash", 15, 165, 0, H_AMIS, "Rideaux occultants + voilage"),
        ],
        dims=[("h", [(0, None), (322.2, "v")], 1), ("h", [(0, None), (29.2, "d"), (151.2, "d"), (322.2, "d")], 2),
              ("v", [(0, None), (H_AMIS, "d")], 1)],
        notes=["Fenêtre F5 : largeur relevée sur le plan source ; allège et linteau à confirmer."],
    ),
    "C": dict(
        title="Mur C — Sud (TV et coiffeuse)", width=293.8, view="Vue vers le sud", src="chambre-amis-02",
        calib="Longueur du mur relevée sur le plan source ; téléviseur 75\" contrôlé (166,8 × 93,3)",
        els=[
            ("zone", 0, 293.8, 0, H_AMIS, "panneau"),
            ("zone", 0, 19.8, 0, H_AMIS, "chene"),
            ("zone", 19.8, 80.1, 76, H_AMIS, "miroir"),
            ("zone", 80.1, 101.1, 0, H_AMIS, "chene"),
            ("zone", 139.8, 260.3, 0, H_AMIS, "marbre_clair"),
            ("tv", 115.6, 282.5, 86.2, 179.5),
            ("box", 105.5, 279.1, 48.8, 72.4, "chene", "M6"),
            ("box", 19.2, 112.1, 67.4, 85.7, "chene", "M7"),
        ],
        dims=[("h", [(0, None), (293.8, "d")], 1),
              ("h", [(0, None), (19.8, "d"), (80.1, "d"), (101.1, "d"), (139.8, "d"), (260.3, "d"), (293.8, "d")], 2),
              ("h", [(19.2, None), (112.1, "d")], 3), ("t", [(115.6, None), (282.5, "d")], 1),
              ("v", [(0, None), (48.8, "d"), (72.4, "d"), (86.2, "d"), (179.5, "d"), (H_AMIS, "d")], 1)],
        notes=["M6 : meuble suspendu chêne, plateau marbre, 3 tiroirs ; profondeur ≈ 39 (vue de dessus).",
               "M7 : coiffeuse suspendue chêne, plateau marbre ; hauteur de plateau à confirmer (≈ 80-85).",
               "Habillage marbre blanc veiné caramel toute hauteur (≈ 120 de large)."],
    ),
    "D": dict(
        title="Mur D — Ouest (alcôve, accès)", width=321.9, view="Vue vers l'ouest", src="aucun rendu",
        calib="Relevé à l'échelle sur le plan source",
        els=[
            ("zone", 0, 61.6, 0, H_AMIS, "panneau"),
            ("open", 61.6, 192.3, 0, H_AMIS, "passage", "Ouverture sur alcôve"),
            ("zone", 192.3, 321.9, 0, H_AMIS, "panneau"),
            ("note", 127, 140, "M8 — armoire de l'alcôve (en retrait)"),
        ],
        dims=[("h", [(0, None), (61.6, "d"), (192.3, "d"), (321.9, "d")], 1),
              ("v", [(0, None), (H_AMIS, "d")], 1)],
        notes=["Aucun rendu de ce mur : traitement et hauteur de l'ouverture à confirmer.",
               "Placard « 130 » du plan source non représenté dans la maquette 3D : à confirmer."],
    ),
}

ELEV["etsejour"] = {
    "A": dict(
        title="Mur A — Nord (mur TV)", width=402.5, view="Vue vers le nord", src="etage1-sejour-01",
        calib="Largeur 402,5 relevée sur la vue de dessus ; téléviseur 75\" contrôlé (168,6 × 93,6)",
        els=[
            ("zone", 0, 402.5, 0, H_ET_SEJ, "panneau"),
            ("hline", 38.6, 0, 54.3, "joint"),
            ("vline", 158.4, 0, H_ET_SEJ, "joint"), ("vline", 169.1, 0, H_ET_SEJ, "joint"),
            ("vline", 327.5, 0, H_ET_SEJ, "joint"),
            ("box", 54.3, 125.5, 49, H_ET_SEJ, "chene", "M9b — étagère éclairée"),
            ("box", 83.4, 93.6, 49, H_ET_SEJ, "marbre_clair", ""),
            ("hline", 94.1, 54.3, 83.4, "led"), ("hline", 141.0, 54.3, 83.4, "led"),
            ("hline", 187.7, 54.3, 83.4, "led"), ("hline", 237.8, 54.3, 83.4, "led"),
            ("hline", 117.2, 93.6, 125.5, "led"), ("hline", 164.4, 93.6, 125.5, "led"),
            ("hline", 212.1, 93.6, 125.5, "led"),
            ("tv", 152.6, 321.2, 87.8, 181.3),
            ("box", 62.3, 343.9, 17, 49, "chene", "M9a"),
            ("vline", 132.7, 17, 49, "joint"), ("vline", 203.1, 17, 49, "joint"), ("vline", 273.5, 17, 49, "joint"),
        ],
        dims=[("h", [(0, None), (402.5, "d")], 1),
              ("h", [(0, None), (54.3, "d"), (83.4, "d"), (93.6, "d"), (125.5, "d"), (158.4, "d"), (169.1, "d"),
                     (327.5, "d"), (402.5, "d")], 2),
              ("h", [(62.3, None), (343.9, "d")], 3), ("t", [(152.6, None), (321.2, "d")], 1),
              ("v", [(0, None), (17, "d"), (49, "d"), (87.8, "d"), (181.3, "d"), (H_ET_SEJ, "d")], 1)],
        notes=["M9a : meuble suspendu chêne, 4 façades, profondeur ≈ 32 (vue de dessus).",
               "M9b : étagère verticale chêne éclairée, montant central marbre ; tablettes à ±5.",
               "Panneaux muraux crème à joints creux."],
    ),
    "B": dict(
        title="Mur B — Est (mur d'entrée)", width=524.4, view="Vue vers l'est", src="etage1-sejour-08",
        calib="Longueur 524,4 (vue de dessus) ; hauteur reprise du mur A",
        els=[
            ("zone", 0, 524.4, 0, H_ET_SEJ, "panneau"),
            ("hline", 38.9, 0, 67.1, "joint"), ("hline", 38.9, 223.6, 362.6, "joint"),
            ("vline", 57.1, 0, H_ET_SEJ, "joint"), ("vline", 64.0, 0, H_ET_SEJ, "joint"),
            ("vline", 255.0, 0, H_ET_SEJ, "joint"), ("vline", 262.3, 0, H_ET_SEJ, "joint"),
            ("vline", 353.5, 0, H_ET_SEJ, "joint"),
            ("open", 67.1, 223.6, 0, 208.3, "door2", "Porte double chêne à oculus"),
            ("zone", 115.8, 134.0, 16, 188.8, "verre"), ("zone", 164.0, 181.3, 16, 188.8, "verre"),
            ("art", 272.6, 379.9, 63.4, 211.7, "Œuvre motif rouge"),
            ("box", 362.6, 524.4, 0, H_ET_SEJ, "chene", "M10 — bibliothèque éclairée"),
            ("hline", 76.6, 362.6, 524.4, "led"), ("hline", 102.3, 362.6, 524.4, "led"),
            ("hline", 157.8, 362.6, 524.4, "led"), ("hline", 208.7, 362.6, 524.4, "led"),
            ("hline", 231.0, 362.6, 524.4, "led"),
        ],
        dims=[("h", [(0, None), (524.4, "d")], 1),
              ("h", [(0, None), (67.1, "d"), (223.6, "d"), (272.6, "d"), (362.6, "d"), (524.4, "d")], 2),
              ("t", [(272.6, None), (379.9, "d")], 1),
              ("v", [(0, None), (63.4, "d"), (208.3, "d"), (211.7, "d"), (H_ET_SEJ, "d")], 1)],
        notes=["Porte double : ≈ 156 × 208, deux oculus vitrés verticaux ; sens d'ouverture à confirmer.",
               "M10 : bibliothèque chêne éclairée, profondeur ≈ 27 ; tablettes relevées à ±5."],
    ),
    "C": dict(
        title="Mur C — Sud (fenêtres)", width=402.5, view="Vue vers le sud", src="etage1-sejour-02 (vue de 3/4)",
        calib="Largeur relevée sur la vue de dessus",
        els=[
            ("zone", 0, 402.5, 0, H_ET_SEJ, "panneau"),
            ("dash", 22.5, 176.5, 0, H_ET_SEJ, "Baie + rideaux (position indicative)"),
            ("dash", 302.5, 383.5, 0, H_ET_SEJ, "Baie + rideaux (position indicative)"),
        ],
        dims=[("h", [(0, None), (402.5, "d")], 1), ("v", [(0, None), (H_ET_SEJ, "d")], 1)],
        notes=["Baies du mur sud : positions déduites des rideaux de la maquette ; largeurs, allèges et linteaux à confirmer."],
    ),
    "D": dict(
        title="Mur D — Ouest (fenêtres)", width=524.4, view="Vue vers l'ouest", src="etage1-sejour-03 (vue de 3/4)",
        calib="Longueur relevée sur la vue de dessus",
        els=[
            ("zone", 0, 524.4, 0, H_ET_SEJ, "panneau"),
            ("dash", 9, 460, 0, H_ET_SEJ, "Baies + rideaux sur la longueur (position indicative)"),
        ],
        dims=[("h", [(0, None), (524.4, "d")], 1), ("v", [(0, None), (H_ET_SEJ, "d")], 1)],
        notes=["Nombre, largeurs et hauteurs des baies du mur ouest : à confirmer."],
    ),
}

ELEV["princ"] = {
    "A": dict(
        title="Mur A — Est (tête de lit)", width=377.3, view="Vue vers l'est", src="chambre-principale-05",
        calib="Largeur 377,3 relevée sur la vue de dessus ; hauteur ±5",
        els=[
            ("zone", 0, 377.3, 0, H_PRINC, "panneau"),
            ("zone", 0, 33.5, 184.2, H_PRINC, "chene"), ("zone", 0, 33.5, 0, 184.2, "cannelure"),
            ("hline", 184.2, 0, 33.5, "led"),
            ("vline", 50.6, 0, H_PRINC, "joint"), ("vline", 106.7, 0, H_PRINC, "joint"),
            ("hline", 184.2, 33.5, 134.2, "joint"),
            ("zone", 134.2, 232.0, 0, H_PRINC, "marbre_fonce"),
            ("vline", 134.2, 0, H_PRINC, "led"), ("vline", 232.0, 0, H_PRINC, "led"),
            ("zone", 232.0, 331.4, 0, H_PRINC, "miroir"),
            ("zone", 331.4, 365.6, 184.2, H_PRINC, "chene"), ("zone", 331.4, 365.6, 0, 184.2, "cannelure"),
            ("hline", 184.2, 331.4, 365.6, "led"),
            ("box", 3.5, 367.8, 0, 112.4, "tissu", "Tête de lit murale"),
            ("box", 82.3, 283.6, 0, 99.7, "tissu", "Tête de lit du lit"),
            ("dash", 19, 83, 0, 60, "Chevet"), ("dash", 282, 341, 0, 60, "Chevet"),
        ],
        dims=[("h", [(0, None), (377.3, "d")], 1),
              ("h", [(0, None), (33.5, "d"), (50.6, "d"), (106.7, "d"), (134.2, "d"), (232.0, "d"), (331.4, "d"),
                     (365.6, "d"), (377.3, "d")], 2),
              ("t", [(3.5, None), (367.8, "d")], 1),
              ("v", [(0, None), (99.7, "d"), (112.4, "d"), (184.2, "d"), (H_PRINC, "d")], 1)],
        notes=["Bande marbre brun-vert veiné rétroéclairée (≈ 98 de large) toute hauteur.",
               "Tête de lit murale tapissée sur presque toute la largeur ; épaisseur à confirmer.",
               "Chevets chêne 2 tiroirs : dimensions à confirmer (≈ 60 × 60 ht sur le rendu)."],
    ),
    "B": dict(
        title="Mur B — Ouest (dressing)", width=254.6, view="Vue vers l'ouest", src="chambre-principale-04 (vue de 3/4)",
        calib="Emprise du dressing relevée sur la vue de dessus",
        els=[
            ("zone", 0, 254.6, 0, H_PRINC, "panneau"),
            ("box", 3.7, 234.7, 0, H_PRINC, "chene", "M12 — dressing"),
        ] + [("vline", 3.7 + k * 46.2, 0, H_PRINC, "joint") for k in range(1, 5)] + [
            ("hline", 225, 3.7, 234.7, "joint"),
            ("note", 117, 120, "5 vantaux observés sur le rendu, largeurs supposées égales + niveau haut : à confirmer"),
        ],
        dims=[("h", [(0, None), (3.7, "d"), (234.7, "d"), (254.6, "d")], 1),
              ("v", [(0, None), (H_PRINC, "d")], 1)],
        notes=["M12 : dressing chêne ≈ 231 × 70 de profondeur, toute hauteur ; poignées intégrées.",
               "Hauteur du niveau haut et répartition intérieure à confirmer."],
    ),
    "C": dict(
        title="Mur C — Nord (baie vitrée)", width=683.2, view="Vue vers le nord", src="chambre-principale-03 (vue de 3/4)",
        calib="Longueur relevée sur la vue de dessus",
        els=[("zone", 0, 683.2, 0, H_PRINC, "panneau"),
             ("dash", 520, 680, 0, 250, "Baie vitrée coulissante (position indicative)")],
        dims=[("h", [(0, None), (683.2, "d")], 1), ("v", [(0, None), (H_PRINC, "d")], 1)],
        notes=["Baie vitrée près de l'angle nord-est : largeur et hauteur à confirmer."],
    ),
    "D": dict(
        title="Mur D — Sud (fenêtres)", width=683.2, view="Vue vers le sud", src="chambre-principale-05 (rideaux)",
        calib="Longueur relevée sur la vue de dessus",
        els=[("zone", 0, 683.2, 0, H_PRINC, "panneau"),
             ("dash", 124, 305, 0, H_PRINC, "Baie + rideaux (position indicative)"),
             ("dash", 377, 557, 0, H_PRINC, "Baie + rideaux (position indicative)")],
        dims=[("h", [(0, None), (683.2, "d")], 1), ("v", [(0, None), (H_PRINC, "d")], 1)],
        notes=["Baies du mur sud : positions déduites des rideaux ; dimensions à confirmer."],
    ),
}

# ---------------------------------------------------------------- materials (names from the design, tints sampled on renders)
MATERIALS = {   # (material, use, tint sampled on the renders or None) — references and finishes to confirm
    "sejour": [
        ("Chêne clair", "Panneaux muraux, colonnes, bibliothèque, panneaux TV arrondis", "#6A5442"),
        ("Laque crème", "Meuble TV suspendu, colonne à niches", "#A1988F"),
        ("Panneaux muraux crème", "Murs habillés à joints creux", "#978B80"),
        ("Lames cannelées", "Colonne du mur TV, soubassement des colonnes chêne", "#766759"),
        ("Bois foncé", "Porte d'entrée deux vantaux", "#251B13"),
        ("Miroir", "Bande verticale du mur TV", "#A19891"),
        ("Marbre blanc veiné", "Colonne et console (salle à manger)", "#97887A"),
        ("Travertin", "Table à manger", "#C2BAB2"),
        ("Parquet bois", "Sol", "#624D3E"),
        ("Cuir taupe foncé", "Canapé modulaire", "#4E463E"),
        ("Bouclé", "Chaises de salle à manger", "#AAA198"),
        ("Tapis clair", "Salon", "#9C9085"),
        ("Rideaux taupe + voilage", "Fenêtres F1, F2", "#42362D"),
        ("Éclairage LED", "Gorges de plafond, rétroéclairage TV, niches, colonnes", None),
    ],
    "amis": [
        ("Marbre blanc veiné caramel", "Habillage du mur TV", "#B6AFA9"),
        ("Lames chêne", "Mur tête de lit", "#82624B"),
        ("Panneaux muraux beige", "Murs", "#A1968E"),
        ("Chêne + plateau marbre", "Meuble TV et coiffeuse suspendus", "#6C503C"),
        ("Lin clair", "Lit plateforme tapissé", "#A1978F"),
        ("Cuir brun capitonné", "Pouf", "#483C33"),
        ("Miroir", "Fente verticale, miroir de coiffeuse", None),
        ("Métal noir", "Chevets ronds", None),
        ("Rideaux taupe + voilage", "Fenêtre F5", "#706154"),
    ],
    "etsejour": [
        ("Chêne", "Meuble TV, étagère, bibliothèque, porte double", "#563C27"),
        ("Marbre blanc veiné", "Montant de l'étagère, table basse", "#877B6D"),
        ("Panneaux crème à joints creux", "Murs", "#756758"),
        ("Tissu gris taupe", "Canapé d'angle, fauteuil", "#685E4D"),
        ("Cuir cognac", "Pouf à côtes, coussins", "#503726"),
        ("Tapis tissé", "Sol du salon", "#8D837A"),
        ("Parquet bois", "Sol", "#745B45"),
        ("Rideaux taupe + voilage", "Baies", "#786557"),
        ("Œuvre motif rouge", "Mur d'entrée", "#7B3931"),
    ],
    "princ": [
        ("Marbre brun foncé veiné", "Bande centrale rétroéclairée", "#312A1B"),
        ("Tissu clair", "Tête de lit murale", "#918376"),
        ("Tissu", "Banc capitonné", "#8D7E6F"),
        ("Chêne", "Colonnes, chevets, dressing", "#694E39"),
        ("Lames cannelées", "Soubassement des colonnes", "#A4978A"),
        ("Miroir", "Panneaux à droite de la tête de lit", None),
        ("Laiton", "Piètement du banc", None),
        ("Noir", "Meuble TV", "#19170D"),
        ("Kaki", "Linge de lit", "#3A3322"),
        ("Rideaux taupe + voilage", "Baies", "#695E54"),
    ],
}

# custom furniture schedule (reference, room, name, dims (L, P, H) with status, notes)
CUSTOM = {
    "sejour": [
        ("M1", "Meuble TV suspendu laqué crème", [("L", 259, "d"), ("P", 32, "d"), ("H", 34, "d"), ("pose", 20, "d")],
         "3 façades ; fixation murale ; rétroéclairage sous meuble à confirmer"),
        ("M2", "Mur TV : colonne cannelée, miroir, panneaux chêne arrondis rétroéclairés, colonne à niches",
         [("L", 382.3, "d"), ("H", 284, "d"), ("P", None, "c")], "TV 75\" encastrée dans le panneau chêne ; épaisseurs à confirmer"),
        ("M3", "Bibliothèque chêne toute hauteur (mur sud)", [("L", 185, "d"), ("P", 23, "d"), ("H", 284, "d")],
         "panneau plein ≈ 45 côté fenêtre + étagères ouvertes asymétriques"),
        ("M4", "Console murale + colonne marbre (mur est)", [("L", 128, "d"), ("P", 30, "d"), ("H", None, "c")],
         "marbre blanc veiné ; hauteur de pose à confirmer"),
        ("M5", "Colonnes chêne + soubassement cannelé éclairé (×3, mur sud)",
         [("L", 61, "d"), ("H", 284, "d"), ("LED", 105, "d")], "entraxe ≈ 140 ; profondeur à confirmer"),
    ],
    "amis": [
        ("M6", "Meuble TV suspendu chêne, plateau marbre", [("L", 175, "d"), ("P", 39, "d"), ("H", 24, "d"), ("pose", 49, "d")],
         "3 tiroirs"),
        ("M7", "Coiffeuse suspendue chêne, plateau marbre + miroir", [("L", 93, "d"), ("P", None, "c"), ("H", 18, "d")],
         "hauteur de plateau à confirmer"),
        ("M8", "Armoire de l'alcôve", [("L", 140, "d"), ("P", 50, "d"), ("H", None, "c")],
         "façades chêne fumé (proposition initiale) à confirmer"),
    ],
    "etsejour": [
        ("M9a", "Meuble TV suspendu chêne", [("L", 282, "d"), ("P", 32, "d"), ("H", 32, "d"), ("pose", 17, "d")],
         "4 façades égales"),
        ("M9b", "Étagère verticale éclairée, montant marbre", [("L", 71, "d"), ("P", None, "c"), ("H", 240, "d")],
         "posée sur M9a ; 7 tablettes éclairées"),
        ("M10", "Bibliothèque chêne éclairée (mur d'entrée)", [("L", 162, "d"), ("P", 27, "d"), ("H", 289, "d")],
         "soubassement fermé ≈ 70 ; tablettes éclairées"),
    ],
    "princ": [
        ("M11", "Mur tête de lit : bande marbre, miroirs, colonnes chêne, tête de lit murale",
         [("L", 377.3, "d"), ("H", 292, "d"), ("P", None, "c")], "tête de lit murale ≈ 364 × 112"),
        ("M12", "Dressing chêne toute hauteur", [("L", 231, "d"), ("P", 70, "d"), ("H", 292, "d")], "5 vantaux + niveau haut"),
        ("M13", "Meuble TV noir mat (îlot face au lit)", [("L", 168, "d"), ("P", 29, "d"), ("H", None, "c")],
         "posé au sol ; hauteur à confirmer"),
    ],
}


# ---------------------------------------------------------------- split of the long south wall of the living room
def _clip(els, x0, x1):
    out = []
    for el in els:
        t = el[0]
        if t in ("zone", "rzone", "open", "tv", "box", "art", "dash"):
            a, b = max(el[1], x0), min(el[2], x1)
            if b - a <= 0.5:
                continue
            out.append((t, a - x0, b - x0) + tuple(el[3:]))
        elif t == "vline":
            if x0 <= el[1] <= x1:
                out.append((t, el[1] - x0) + tuple(el[2:]))
        elif t == "hline":
            a, b = max(el[2], x0), min(el[3], x1)
            if b - a > 0.5:
                out.append((t, el[1], a - x0, b - x0, el[4]))
        elif t == "note":
            if x0 <= el[1] <= x1:
                out.append((t, el[1] - x0) + tuple(el[2:]))
    return out


_D = ELEV["sejour"].pop("D")
_E = ELEV["sejour"].pop("E")
ELEV["sejour"]["D1"] = dict(
    title="Mur D1 — Sud, partie salle à manger", width=591.3, view="Vue vers le sud", src="rdc-salon-09, -10",
    calib="Fenêtre F4 (114,4) et porte d'entrée (163) relevées sur le plan source ; rendus 09 et 10",
    els=_clip(_D["els"], 0, 591.3),
    dims=[("h", [(0, None), (184.7, "d"), (299.1, "d"), (309.4, "d"), (403.9, "d"), (414.3, "d"), (487.1, "d"),
                 (581.1, "d"), (591.3, "d")], 1),
          ("h", [(0, None), (139.7, "d"), (184.7, "d")], 2),
          ("v", [(0, None), (100, "d"), (225, "d"), (H_SEJ, "d")], 1, 487.1),
          ("v", [(0, None), (89.5, "d"), (217.4, "d")], 1, 403.9),
          ("v", [(0, None), (H_SEJ, "d")], 1)],
    notes=["Fenêtres F3 et F4 : allège ≈ 100, linteau ≈ 225 (±5) relevés sur les rendus 09 et 10.",
           "M3 : bibliothèque chêne toute hauteur, profondeur ≈ 23 ; répartition des étagères à confirmer.",
           "Œuvre rouge : bas ≈ 90, haut ≈ 217 ; largeur à confirmer (rendu 09 partiel).",
           "Lecture de gauche à droite : de l'angle sud-est vers la porte d'entrée."],
)
ELEV["sejour"]["D2"] = dict(
    title="Mur D2 — Sud, entrée et salon", width=541.0, view="Vue vers le sud", src="rdc-salon-08, -10",
    calib="Porte d'entrée 163 (plan source) ; distance porte–fenêtre F3 vérifiée sur le rendu 10",
    els=_clip(_D["els"], 581.1, 1122.1),
    dims=[("h", [(0, None), (10.2, "d"), (173.3, "d"), (183.3, "d"), (243.9, "d"), (322.8, "d"), (384.5, "d"),
                 (463.5, "d"), (525.9, "d"), (541.0, "d")], 1),
          ("h", [(0, None), (541.0, "d")], 2),
          ("v", [(0, None), (235, "d"), (H_SEJ, "d")], 1, 173.3),
          ("v", [(0, None), (105, "d"), (H_SEJ, "d")], 1)],
    notes=["Porte d'entrée : ≈ 163 × 235, deux vantaux bois foncé, sens d'ouverture à confirmer.",
           "M5 : colonnes chêne (×3) ≈ 61 de large, partie basse cannelée, ligne LED à ≈ 105 ; profondeur à confirmer.",
           "Lecture de gauche à droite : de la porte d'entrée vers l'angle sud-ouest."],
)
ELEV["sejour"]["E"] = _E
for _r, _ks in (("sejour", "BC"), ("amis", "BD"), ("etsejour", "CD"), ("princ", "CD")):
    for _k in _ks:
        ELEV[_r][_k]["sparse"] = True
