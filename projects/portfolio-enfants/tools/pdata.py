"""KAÏRA — Portfolio « Chambres d'enfants » : contenu des projets.

All dimensions are PROPOSED concept dimensions (cm), drawn to be coherent with the furniture visible on
each render (standard sizes: crib 60 × 120, bed 90 × 200, wardrobe depth 60, shelves 35…). They are not
site measurements and are labelled as such on every technical page.

Renders: sources/recus/NN.png — used whole and unmodified.
Images 02 and 03 (inspirations from other studios) are not presented as KAÏRA projects.

Elevation elements (wall coordinates, x from the left end of the wall seen from inside, z from the floor):
  ('rect', x0, x1, z0, z1, mat, opts)   opts: lines=[x], hsplits=[z], knobs=[(x, z, r, mat)], grips=[(x, z0, z1)],
                                                flutes=True, label='M1'
  ('arch', x0, x1, z0, ztop, mat, opts)  rectangle with a semicircular top; opts: led=True, label
  ('scallops', x0, x1, z0, tops, mat)    row of arched upholstered panels (one top height per panel)
  ('cloud', x0, x1, z0, z1, mat, led)
  ('crib', x0, x1, z0, z1, zmat)          ('canopy', cx, zc, x0, x1)
  ('window', x0, x1, z0, z1)              ('curtain', x0, x1, z0, z1, mat)
  ('motif', x0, x1, z0, z1, label)        ('bear', cx, cz, r, mat)    ('bunny', cx, cz, w)
  ('shelf', x0, x1, z, led)               ('ledh', x0, x1, z)   ('ledv', x, z0, z1)
  ('sconce', cx, cz)                      ('cloudlamp', x0, x1, z0, z1)   ('dome', cx, zb, r)
  ('mattress', x0, x1, z0, z1)            ('spot', x)
"""

PROJECTS = []


def P(**kw):
    PROJECTS.append(kw)
    return kw


# ===================================================================================== 1. DOUCEUR LAPIN
P(
    key="lapin", num="01", img="01.png", name="Douceur Lapin", type="Nurserie",
    tagline="Une nurserie cocon en rose poudré, où l'arche et le lapin composent un paysage de douceur.",
    facts=[("Typologie", "Nurserie, 0 – 3 ans"), ("Surface proposée", "≈ 17,3 m² (480 × 360)"),
           ("Hauteur sous plafond", "270 (proposée)"), ("Palette", "Rose poudré · crème · blanc laqué"),
           ("Signature", "Arches lumineuses, motif lapin")],
    concept=[
        "Douceur Lapin imagine la première chambre comme un cocon. L'arche — déclinée en niche autour du berceau, "
        "en panneaux superposés et en bibliothèque — dessine un paysage enveloppant, sans angle vif, à hauteur du regard "
        "de l'adulte comme de l'enfant.",
        "Le lapin est le fil narratif du projet : il apparaît en lumière sur le panneau rose, se retrouve dans les "
        "peluches, le lapin à bascule et les illustrations encadrées, toujours avec retenue.",
    ],
    ambiance="Rose poudré, crème et blanc laqué composent une palette tendre, réchauffée par une lumière dorée. "
             "Le voilage du ciel de lit, les rideaux et la laine du tapis absorbent le son et adoucissent chaque geste.",
    lumiere="Niche cintrée rétroéclairée, étagères et bibliothèque éclairées en sous-face, socle lumineux de la commode "
            "et applique lapin : uniquement des sources indirectes, idéales pour les réveils de nuit.",
    palette=["rose_arche", "creme_mur", "creme_commode", "laine", "vegetal"],
    room=dict(W=480, D=360, H=270),
    mats={"rose": ("rose_arche", "velvet"), "rose2": ("rose_rideau", "velvet"), "creme": ("creme_commode", "flat"),
          "niche": ("creme_mur", "flat"), "blanc": ("#FFFFFF", "flat"), "rideau": ("rose_rideau", "sheer"),
          "voilage": ("voilage", "sheer"), "socle": ("#E9E1D8", "flat"), "velours": ("velours_rose", "velvet")},
    materials=[
        ("Laque mate crème", "Commode à langer, bibliothèque, étagères", "creme_commode", "flat"),
        ("Rose poudré", "Panneaux arches, coussins, linge", "rose_arche", "velvet"),
        ("Enduit lisse crème", "Murs et niche cintrée", "creme_mur", "flat"),
        ("Voilage rose", "Ciel de lit, rideaux de la baie", "voilage", "sheer"),
        ("Velours rose", "Pouf citrouille", "velours_rose", "velvet"),
        ("Laine bouclée", "Tapis rond motif nuages", "laine", "dots"),
        ("Sol clair poli", "Revêtement de sol", "sol", "flat"),
        ("Végétal", "Plantes retombantes", "vegetal", "leaf"),
    ],
    elements=[
        "Baie toute hauteur habillée d'un voilage et de rideaux rose poudré sur rail au plafond",
        "Niche cintrée rétroéclairée encadrant le berceau",
        "Panneaux arches superposés en rose poudré",
        "Applique lapin et nuage rétroéclairée",
        "Ciel de lit en voilage rose, couronne à pompons et guirlande lumineuse",
        "Mobile nuages et étoiles au-dessus du berceau",
        "Spots encastrés au plafond",
        "Tapis rond en laine à motif nuages, pouf citrouille en velours rose",
        "Lapin à bascule, peluches, paniers et illustrations encadrées",
    ],
    walls={
        "A": dict(title="Mur A — baie, arches et niche du berceau", W=480, els=[
            ("window", 20, 140, 0, 240), ("curtain", 20, 140, 0, 265, "voilage"),
            ("curtain", 4, 30, 0, 265, "rideau"), ("curtain", 130, 158, 0, 265, "rideau"),
            ("arch", 160, 205, 0, 235, "rose", {}), ("arch", 195, 235, 0, 205, "rose2", {}),
            ("arch", 160, 200, 0, 120, "rose2", {}), ("bunny", 212, 168, 30),
            ("arch", 245, 405, 0, 240, "niche", {"led": True, "label": "M3"}),
            ("crib", 259, 391, 0, 95, 48), ("canopy", 325, 238, 262, 388),
            ("arch", 415, 475, 0, 255, "creme", {"led": True, "label": "M2"}),
            ("rect", 415, 475, 8, 68, "creme", {"grips": [(445, 55, 62)]}),
            ("shelf", 419, 471, 110, True), ("shelf", 419, 471, 155, True), ("shelf", 419, 471, 200, True),
            ("spot", 90), ("spot", 325),
        ], dims=[("h", [0, 20, 140, 160, 235, 245, 405, 415, 475, 480], 1), ("h", [0, 480], 2),
                 ("v", [0, 95, 240, 270], 245), ("v", [0, 68, 110, 155, 200, 255, 270], 480),
                 ("v", [0, 120, 205, 235], 160)]),
        "D": dict(title="Mur D — commode à langer et étagères", W=360, els=[
            ("rect", 205, 315, 0, 8, "socle", {}), ("ledh", 205, 315, 4),
            ("rect", 200, 320, 8, 90, "creme", {"hsplits": [35.3, 62.6], "grips": [(260, 30, 30), (260, 57, 57), (260, 85, 85)],
                                                "label": "M1"}),
            ("rect", 212, 308, 90, 100, "rose", {}),
            ("shelf", 200, 320, 140, True), ("shelf", 200, 320, 180, True),
        ], dims=[("h", [0, 200, 320, 360], 1), ("v", [0, 8, 90, 100, 140, 180, 270], 320)]),
    },
    plan=dict(items=[
        ("rect", (0, 200, 55, 320), "built", "M1"), ("rect", (0, 200, 25, 320), "dash", ""),
        ("rect", (160, 357, 235, 360), "built", ""), ("rect", (245, 355, 405, 360), "built", ""),
        ("rect", (259, 294, 391, 360), "furn", "Lit bébé 60 × 120"),
        ("rect", (415, 325, 475, 360), "built", "M2"),
        ("circ", (300, 165), 100, "rug", ""), ("circ", (405, 115), 30, "furn", ""),
        ("rect", (120, 115, 205, 150), "furn", ""),
    ], windows=[("N", 20, 140)], doors=[("S", 330, 420, "right")],
        dims=[("x", [0, 20, 140, 245, 405, 415, 475, 480], 360, 9), ("x", [0, 480], 0, -10),
              ("y", [0, 200, 320, 360], 0, -9), ("y", [0, 360], 480, 10), ("y", [294, 360], 391, 5),
              ("x", [0, 55], 200, -4)],
        labels=[(300, 175, "Tapis Ø 200"), (405, 115, "Pouf"), (330, 30, "Porte 90")]),
    section=dict(title="Coupe AA — berceau et niche (vue vers l'ouest)", D=360, H=270, cut_x=325, els=[
        ("ghost", 40, 160, 8, 90, "M1 commode (mur D)"), ("ghostline", 40, 160, 140), ("ghostline", 40, 160, 180),
        ("recess", 0, 10, 0, 240, "Niche cintrée (profondeur 10)"),
        ("prof", 0, 66, 0, 95, "furn", "Lit bébé"), ("mattress", 3, 63, 40, 48),
        ("canopy", 33, 238), ("spotc", 120),
    ], dims=[("h", [0, 10, 66, 360], 1), ("v", [0, 48, 95, 240, 270], 0)]),
    furniture=[
        ("M1", "Commode à langer", "L 120 · P 55 · H 90 (+ socle 8)",
         "Laque mate crème, poignées encastrées, plan à langer amovible, socle en retrait éclairé par LED.",
         ("D", 195, 325, 0, 105), (55, 90, [8, 35.3, 62.6], 8)),
        ("M2", "Bibliothèque cintrée", "L 60 · P 35 · H 255",
         "Laque crème, fond éclairé, trois tablettes avec LED en sous-face, caisson bas fermé h 60.",
         ("A", 410, 480, 0, 262), (35, 255, [8, 68, 110, 155, 200], 8)),
        ("M3", "Niche cintrée rétroéclairée", "L 160 · H 240 · prof. 10",
         "Enduit lisse crème, profil LED périphérique 2700 K. Encadre le berceau et porte le ciel de lit.",
         ("A", 240, 410, 0, 245), (10, 240, [], 0)),
        ("M4", "Panneaux arches", "45 × 235 · 40 × 205 · 40 × 120",
         "Trois panneaux superposés en MDF laqué rose poudré, applique lapin intégrée, fixation murale invisible.",
         ("A", 155, 240, 0, 240), (3, 235, [], 0)),
        ("M5", "Étagères flottantes ×2", "L 120 · P 25 · ép. 4",
         "Laque crème, ruban LED en sous-face, fixations invisibles ; au-dessus de la commode à 140 et 180.",
         ("D", 195, 325, 125, 190), (25, 4, [], 0)),
    ],
)

# ===================================================================================== 2. JUNGLE DOUCE
P(
    key="jungle", num="02", img="06.png", name="Jungle Douce", type="Nurserie évolutive",
    tagline="Une jungle apaisée, illustrée comme un livre d'images, qui grandit avec l'enfant.",
    facts=[("Typologie", "Nurserie évolutive, 0 – 6 ans"), ("Surface proposée", "≈ 20,2 m² (440 × 460)"),
           ("Hauteur sous plafond", "270 · 260 sous faux-plafond"), ("Palette", "Vert olive · crème · chêne · caramel"),
           ("Signature", "Fresque jungle, façades en arches")],
    concept=[
        "Jungle Douce raconte une jungle tranquille plutôt qu'exubérante. La fresque — girafe, singe et grandes feuilles — "
        "se lit comme une illustration de livre, posée sur un fond crème qui laisse respirer la pièce.",
        "Le mobilier sur mesure reprend la forme de l'arche en vert olive, de la bibliothèque aux façades de l'armoire : "
        "il relie la fresque aux rangements et donne à la chambre une écriture unique.",
    ],
    ambiance="Vert olive, crème, chêne naturel et touches caramel : une palette végétale et chaleureuse. Les lames de chêne, "
             "le bouclé et la laine tuftée apportent du relief au toucher.",
    lumiere="Gorge lumineuse circulaire au plafond, suspension nuage, bibliothèque et étagères éclairées, applique double "
            "globe sur le panneau de chêne. Le bureau suspendu prépare déjà les années suivantes.",
    palette=["olive", "creme", "chene", "girafe", "caramel"],
    room=dict(W=440, D=460, H=270),
    mats={"olive": ("olive", "flat"), "creme": ("creme", "flat"), "chene": ("chene", "wood"), "lames": ("chene", "flutes"),
          "fond": ("fresque_fond", "flat"), "blanc": ("#FFFFFF", "flat"), "voilage": ("voilage", "sheer"),
          "rideau": ("creme", "sheer"), "socle": ("#E9E1D8", "flat")},
    materials=[
        ("Laque vert olive", "Bibliothèque cintrée, arches de l'armoire, tiroirs du bureau", "olive", "flat"),
        ("Laque crème", "Armoire, plateau du bureau", "creme", "flat"),
        ("Chêne naturel", "Lames murales, étagère ouverte", "chene", "flutes"),
        ("Fresque peinte", "Mur du berceau : girafe, singe, feuillages", "girafe", "flat"),
        ("Feuillage olive", "Motifs de la fresque et du tapis", "feuillage", "leaf"),
        ("Bouclé caramel", "Pouf citrouille", "caramel", "dots"),
        ("Bouclé crème", "Tabouret du bureau", "boucle", "dots"),
        ("Voilage naturel", "Ciel de lit, rideaux", "voilage", "sheer"),
        ("Laine tuftée", "Tapis rond motif feuilles", "laine", "dots"),
    ],
    elements=[
        "Fresque murale peinte : girafe, singe et grandes feuilles sur fond crème",
        "Gorge lumineuse circulaire Ø 220 au plafond, suspension nuage au centre",
        "Ciel de lit en voilage naturel au-dessus du berceau",
        "Panneau de lames de chêne avec applique double globe",
        "Façades d'armoire en arches vert olive, boutons ronds en chêne",
        "Baie toute hauteur avec voilage, bureau à la lumière naturelle",
        "Tapis rond en laine à motif de feuilles, pouf citrouille caramel, tabouret bouclé",
        "Jouets en bois, girafe et dinosaure en peluche, plantes retombantes",
    ],
    walls={
        "A": dict(title="Mur A — fresque, berceau et bibliothèque cintrée", W=440, els=[
            ("motif", 95, 375, 0, 270, "Fresque murale peinte — girafe, singe, grandes feuilles (selon rendu)"),
            ("arch", 0, 90, 0, 245, "olive", {"led": True, "label": "M1"}),
            ("rect", 4, 86, 0, 60, "olive", {"lines": [45], "knobs": [(40, 45, 2.5, "chene"), (50, 45, 2.5, "chene")]}),
            ("shelf", 4, 86, 95, True), ("shelf", 4, 86, 140, True), ("shelf", 4, 86, 185, True),
            ("crib", 170, 300, 0, 95, 48), ("canopy", 235, 232, 172, 298),
            ("rect", 380, 430, 25, 240, "lames", {"flutes": True, "label": "M5"}), ("sconce", 405, 150),
            ("spot", 220),
        ], dims=[("h", [0, 90, 170, 300, 380, 430, 440], 1), ("h", [0, 440], 2),
                 ("v", [0, 60, 95, 140, 185, 245, 270], 90), ("v", [0, 48, 95], 300), ("v", [0, 25, 240, 270], 440)]),
        "B": dict(title="Mur B — armoire, étagère, bureau et baie", W=460, els=[
            ("rect", 0, 180, 0, 250, "creme", {"lines": [45, 90, 135], "label": "M2"}), ("rect", 0, 180, 250, 270, "creme", {}),
            ("arch", 3, 87, 0, 120, "olive", {}), ("arch", 93, 177, 0, 165, "olive", {}),
            ("rect", 0, 180, 0, 0.5, "creme", {"knobs": [(45, 100, 3.5, "chene"), (135, 145, 3.5, "chene")]}),
            ("rect", 180, 230, 0, 250, "chene", {"label": "M3"}),
            ("shelf", 182, 228, 70, True), ("shelf", 182, 228, 115, True), ("shelf", 182, 228, 160, True),
            ("shelf", 182, 228, 205, True),
            ("rect", 235, 355, 52, 67, "olive", {"lines": [295], "label": "M4"}), ("rect", 235, 355, 67, 70, "creme", {}),
            ("rect", 350, 355, 0, 52, "creme", {}),
            ("window", 362, 450, 0, 240), ("curtain", 362, 450, 0, 265, "voilage"),
            ("curtain", 352, 372, 0, 265, "rideau"), ("curtain", 440, 460, 0, 265, "rideau"),
        ], dims=[("h", [0, 45, 90, 135, 180, 230, 235, 355, 362, 450, 460], 1), ("h", [0, 460], 2),
                 ("v", [0, 120, 165, 250, 270], 180), ("v", [0, 70, 115, 160, 205, 250], 230),
                 ("v", [0, 52, 70], 355)]),
    },
    plan=dict(items=[
        ("rect", (0, 425, 90, 460), "built", "M1"), ("rect", (380, 455, 430, 460), "built", ""),
        ("rect", (170, 394, 300, 460), "furn", "Lit bébé 60 × 120"),
        ("rect", (380, 280, 440, 460), "built", "M2"), ("rect", (405, 230, 440, 280), "built", "M3"),
        ("rect", (390, 105, 440, 225), "built", "M4"),
        ("circ", (220, 230), 110, "rug", ""), ("circ", (220, 230), 110, "ceil", ""),
        ("circ", (110, 120), 35, "furn", ""), ("circ", (350, 165), 20, "furn", ""),
    ], windows=[("E", 10, 98)], doors=[("S", 40, 130, "left")],
        dims=[("x", [0, 90, 170, 300, 380, 430, 440], 460, 9), ("x", [0, 440], 0, -10),
              ("y", [0, 10, 98, 105, 225, 230, 280, 460], 440, 10), ("y", [0, 460], 0, -10),
              ("y", [394, 460], 300, 5)],
        labels=[(220, 236, "Tapis Ø 220 · gorge plafond Ø 220"), (110, 120, "Pouf"), (85, 25, "Porte 90")]),
    section=dict(title="Coupe AA — berceau et gorge circulaire (vue vers l'est)", D=460, H=270, cut_x=235, ceiling=(120, 340, 260),
                 els=[("ghost", 0, 180, 0, 250, "M2 armoire (mur B)"), ("ghost", 180, 230, 0, 250, ""),
                      ("ghost", 235, 355, 52, 70, "M4 bureau"), ("ghostwin", 362, 450, 0, 240),
                      ("prof", 0, 66, 0, 95, "furn", "Lit bébé"), ("mattress", 3, 63, 40, 48), ("canopy", 33, 232),
                      ("cloudlamp", 200, 260, 205, 235)],
                 dims=[("h", [0, 66, 120, 340, 460], 1), ("v", [0, 48, 95, 260, 270], 0)]),
    furniture=[
        ("M1", "Bibliothèque cintrée olive", "L 90 · P 35 · H 245",
         "Laque vert olive, fond éclairé, trois tablettes LED, caisson bas à deux portes h 60.",
         ("A", 0, 95, 0, 250), (35, 245, [60, 95, 140, 185], 0)),
        ("M2", "Armoire à façades en arches", "L 180 · P 60 · H 250 (+ bandeau 20)",
         "Quatre portes laquées crème, arches en laque olive, boutons ronds en chêne Ø 7.",
         ("B", 0, 180, 0, 270), (60, 270, [250], 0)),
        ("M3", "Étagère ouverte éclairée", "L 50 · P 35 · H 250",
         "Chêne naturel, quatre tablettes avec LED en sous-face.",
         ("B", 178, 232, 0, 255), (35, 250, [70, 115, 160, 205], 0)),
        ("M4", "Bureau suspendu", "L 120 · P 50 · H 70",
         "Plateau laqué crème, deux tiroirs vert olive, joue latérale ; hauteur adaptée à l'enfant, réglable.",
         ("B", 230, 360, 0, 80), (50, 70, [52, 67], 0)),
        ("M5", "Panneau de lames de chêne", "L 50 · H 215",
         "Lames verticales en chêne naturel, applique double globe opaline intégrée.",
         ("A", 375, 440, 20, 245), (4, 215, [], 0)),
    ],
)

# ===================================================================================== 3. NUAGES
P(
    key="nuages", num="03", img="04.png", name="Nuages", type="Chambre petite enfance",
    tagline="Une alcôve sculptée entre deux armoires, sous un ciel de lames où flottent deux nuages de lumière.",
    facts=[("Typologie", "Chambre petite enfance, 2 – 6 ans"), ("Surface proposée", "≈ 16,3 m² (430 × 380)"),
           ("Hauteur sous plafond", "270 (proposée)"), ("Palette", "Vert olive · crème · chêne clair"),
           ("Signature", "Lit-alcôve à arches, nuages lumineux")],
    concept=[
        "Nuages construit la chambre autour d'une alcôve. Deux armoires toute hauteur encadrent le lit et forment un "
        "refuge à l'échelle de l'enfant, protégé, symétrique, rassurant.",
        "Le lit banquette, habillé de panneaux arrondis en velours olive, se lit comme une rangée de collines ; au-dessus, "
        "un panneau de lames rétroéclairé devient un ciel où flottent deux nuages lumineux.",
    ],
    ambiance="Crème, chêne clair et vert olive : une harmonie calme et naturelle. Les niches basses éclairées exposent "
             "livres et jouets à portée de main ; le reste disparaît derrière des façades lisses.",
    lumiere="Rétroéclairage périmétrique de l'alcôve, nuages lumineux, niches éclairées et spots encastrés : "
            "une veilleuse architecturale pour l'endormissement.",
    palette=["creme", "velours_olive", "lames", "chene", "laine"],
    room=dict(W=430, D=380, H=270),
    mats={"creme": ("creme", "flat"), "lames": ("lames", "flutes"), "velours": ("velours_olive", "velvet"),
          "chene": ("chene", "wood"), "blanc": ("#FFFFFF", "flat"), "socle": ("#E9E1D8", "flat"), "linge": ("linge", "flat")},
    materials=[
        ("Laque mate crème", "Armoires, soffite de l'alcôve", "creme", "flat"),
        ("Velours olive", "Lit banquette à arches", "velours_olive", "velvet"),
        ("Lames laquées sable", "Panneau cannelé rétroéclairé", "lames", "flutes"),
        ("Chêne clair", "Niches basses, colonne ouverte, boutons", "chene", "wood"),
        ("Laine bouclée crème", "Tapis rond à pois olive", "laine", "dots"),
        ("Coton imprimé", "Linge de lit à étoiles", "linge", "flat"),
        ("Parquet chêne clair", "Sol", "sol", "wood"),
    ],
    elements=[
        "Alcôve formée par deux armoires toute hauteur, soffite lumineux",
        "Panneau de lames verticales rétroéclairé sur toute la largeur de l'alcôve",
        "Deux nuages en découpe laquée, rétroéclairés",
        "Niches basses en chêne éclairées pour livres et jouets",
        "Colonne ouverte éclairée avec plante retombante",
        "Table et chaises d'enfant crème et olive, tapis rond à pois",
        "Cadres illustrés ourson et empreinte sur le mur latéral",
        "Baie toute hauteur sur le mur gauche, voilage et rideaux lin",
    ],
    walls={
        "A": dict(title="Mur A — alcôve, armoires et lit à arches", W=430, els=[
            ("rect", 0, 90, 0, 12, "creme", {}), ("rect", 0, 90, 12, 93, "chene", {"lines": [45], "hsplits": [52]}),
            ("ledh", 2, 88, 50), ("ledh", 2, 88, 91),
            ("rect", 0, 90, 93, 265, "creme", {"lines": [45], "knobs": [(45, 115, 5, "chene")], "label": "M1"}),
            ("rect", 0, 90, 265, 270, "creme", {}),
            ("rect", 90, 320, 30, 255, "lames", {"flutes": True, "label": "M3"}), ("rect", 90, 320, 255, 270, "creme", {}),
            ("ledh", 90, 320, 254), ("ledv", 91.5, 30, 254), ("ledv", 318.5, 30, 254),
            ("cloud", 125, 184, 143, 177, "blanc", True), ("cloud", 209, 298, 164, 216, "blanc", True),
            ("scallops", 100, 310, 30, [106, 106, 106, 106, 106], "velours"),
            ("rect", 90, 320, 0, 30, "velours", {"label": "M2"}), ("mattress", 200, 305, 30, 52),
            ("arch", 90, 125, 0, 95, "velours", {}), ("arch", 125, 162, 0, 82, "velours", {}),
            ("arch", 162, 200, 0, 65, "velours", {}), ("arch", 305, 320, 0, 100, "velours", {}),
            ("rect", 320, 400, 0, 12, "creme", {}), ("rect", 320, 400, 12, 93, "chene", {"lines": [360], "hsplits": [52]}),
            ("ledh", 322, 398, 50), ("ledh", 322, 398, 91),
            ("rect", 320, 400, 93, 265, "creme", {"lines": [360], "knobs": [(360, 115, 5, "chene")]}),
            ("rect", 320, 400, 265, 270, "creme", {}),
            ("rect", 400, 430, 0, 270, "chene", {"label": "M5"}), ("shelf", 402, 428, 60, True), ("shelf", 402, 428, 110, True),
            ("shelf", 402, 428, 160, True), ("shelf", 402, 428, 210, True), ("spot", 45), ("spot", 360),
        ], dims=[("h", [0, 45, 90, 320, 360, 400, 430], 1), ("h", [0, 430], 2), ("t", [125, 184, 209, 298], 1),
                 ("v", [0, 12, 52, 93, 265, 270], 90), ("v", [0, 30, 65, 82, 95, 106, 254], 320),
                 ("v", [164, 216], 298)]),
    },
    plan=dict(items=[
        ("rect", (0, 320, 90, 380), "built", "M1"), ("rect", (320, 320, 400, 380), "built", "M1"),
        ("rect", (400, 345, 430, 380), "built", "M5"), ("rect", (90, 377, 320, 380), "built", ""),
        ("rect", (90, 275, 320, 377), "furn", "Lit banquette M2 — couchage 90 × 200"),
        ("circ", (190, 165), 100, "rug", ""), ("circ", (360, 200), 30, "furn", ""),
        ("circ", (315, 180), 14, "furn", ""), ("circ", (405, 180), 14, "furn", ""), ("circ", (360, 247), 14, "furn", ""),
    ], windows=[("W", 120, 300)], doors=[("S", 300, 390, "right")],
        dims=[("x", [0, 90, 320, 400, 430], 380, 9), ("x", [0, 430], 0, -10),
              ("y", [0, 120, 300, 380], 0, -10), ("y", [0, 380], 430, 10), ("y", [275, 377, 380], 320, 5),
              ("y", [320, 380], 90, -4)],
        labels=[(190, 170, "Tapis Ø 200"), (360, 203, "Table Ø 60"), (345, 30, "Porte 90")]),
    section=dict(title="Coupe AA — alcôve et lit (vue vers l'ouest)", D=380, H=270, cut_x=205, els=[
        ("ghost", 0, 60, 93, 265, "M1 armoire (au-delà)"), ("ghost", 0, 60, 12, 93, ""),
        ("ghostwin", 80, 260, 0, 240),
        ("prof", 0, 3, 30, 255, "lames", ""), ("prof", 0, 60, 255, 270, "creme", ""),
        ("prof", 0, 105, 0, 30, "velours", "M2"), ("mattress", 12, 100, 30, 52), ("prof", 3, 15, 30, 106, "velours", ""),
        ("prof", 3, 5, 164, 216, "blanc", ""), ("led", 58, 255),
    ], dims=[("h", [0, 3, 15, 60, 105, 380], 1), ("v", [0, 30, 52, 106, 255, 270], 0)]),
    furniture=[
        ("M1", "Armoires et niches basses ×2", "L 90 et 80 · P 60 · H 270",
         "Façades laquées crème sans poignée, bouton rond en chêne Ø 10 ; niches basses en chêne éclairées (2 × 2).",
         ("A", 0, 92, 0, 270), (60, 270, [12, 52, 93, 265], 12)),
        ("M2", "Lit banquette à arches", "L 230 · P 105 · H 106 (couchage 90 × 200)",
         "Structure tapissée de velours olive, panneaux arrondis superposés, sommier intégré.",
         ("A", 88, 322, 0, 112), (105, 106, [30, 52], 0)),
        ("M3", "Panneau cannelé rétroéclairé", "L 230 · H 225",
         "Lames verticales laquées sable, LED périmétrique 2700 K dans le soffite et les joues.",
         ("A", 88, 322, 25, 270), (3, 225, [], 0)),
        ("M4", "Nuages lumineux", "59 × 34 et 89 × 52",
         "Découpes en MDF laqué blanc, montées à 15 mm du panneau, rétroéclairage LED.",
         ("A", 115, 305, 135, 225), (3, 52, [], 0)),
        ("M5", "Colonne ouverte", "L 30 · P 35 · H 270",
         "Chêne clair, quatre tablettes éclairées.",
         ("A", 398, 430, 0, 270), (35, 270, [60, 110, 160, 210], 0)),
    ],
)

# ===================================================================================== 4. OURSON CARAMEL
P(
    key="ourson", num="04", img="05.png", name="Ourson Caramel", type="Chambre petite enfance",
    tagline="Sous une grande arche lumineuse, l'ourson veille sur un lit flottant aux têtes de lit en collines caramel.",
    facts=[("Typologie", "Chambre petite enfance, 2 – 6 ans"), ("Surface proposée", "≈ 19,0 m² (500 × 380)"),
           ("Hauteur sous plafond", "270 (proposée)"), ("Palette", "Caramel · crème · beige sable"),
           ("Signature", "Arche lumineuse, tête de lit festonnée")],
    concept=[
        "Ourson Caramel fait de l'arche le cœur de la chambre : une grande baie de lumière dessinée au mur accueille "
        "l'ourson, figure tutélaire, comme une fenêtre ouverte sur une histoire.",
        "La tête de lit festonnée, en velours caramel, dessine une ligne de collines au-dessus d'un lit plateforme "
        "qui semble flotter sur sa lumière ; la bibliothèque reprend la même courbe.",
    ],
    ambiance="Caramel, crème et beige sable : une palette chaude et gourmande, adoucie par le bouclé du pouf et la laine "
             "du tapis à pois. Le mur cannelé ajoute un rythme vertical discret.",
    lumiere="Contour LED de l'arche, socle lumineux du lit et de l'armoire, bibliothèques éclairées et suspension nuage : "
            "une lumière dorée, enveloppante, toujours indirecte.",
    palette=["caramel", "creme", "beige_arche", "lames", "laine"],
    room=dict(W=500, D=380, H=270),
    mats={"caramel": ("caramel", "velvet"), "creme": ("creme", "flat"), "beige": ("beige_arche", "flat"),
          "lames": ("lames", "flutes"), "ourson": ("ourson", "flat"), "blanc": ("#FFFFFF", "flat"), "socle": ("#E9E1D8", "flat")},
    materials=[
        ("Velours caramel", "Tête de lit festonnée, poignée de l'armoire", "caramel", "velvet"),
        ("Laque mate crème", "Armoire, bibliothèques, lit plateforme", "creme", "flat"),
        ("Enduit beige sable", "Arche murale", "beige_arche", "flat"),
        ("Lames laquées", "Mur cannelé", "lames", "flutes"),
        ("Motif ourson", "Découpe rétroéclairée dans l'arche", "ourson", "flat"),
        ("Bouclé crème", "Pouf citrouille", "boucle", "dots"),
        ("Laine bouclée", "Tapis rond à pois caramel", "laine", "dots"),
        ("Coton imprimé", "Linge de lit oursons", "linge", "flat"),
    ],
    elements=[
        "Grande arche murale beige sable avec contour lumineux",
        "Motif ourson en découpe rétroéclairée",
        "Tête de lit festonnée en cinq panneaux de velours caramel",
        "Lit plateforme flottant sur socle lumineux",
        "Bibliothèque cintrée éclairée et colonne de rangement ouverte",
        "Mur de lames verticales entre le lit et la bibliothèque",
        "Suspension nuage, lampe champignon caramel",
        "Table et chaises oreilles de lapin, cheval à bascule, pouf citrouille bouclé",
    ],
    walls={
        "A": dict(title="Mur A — arche, lit festonné et bibliothèques", W=500, els=[
            ("rect", 0, 90, 0, 8, "socle", {}), ("ledh", 0, 90, 4),
            ("rect", 0, 90, 8, 270, "creme", {"lines": [45], "knobs": [(45, 130, 9, "caramel")], "label": "M1"}),
            ("arch", 90, 165, 0, 250, "creme", {"led": True, "label": "M2"}), ("rect", 94, 161, 0, 23, "creme", {}),
            ("shelf", 94, 161, 70, True), ("shelf", 94, 161, 127, True), ("shelf", 94, 161, 183, True),
            ("arch", 180, 370, 25, 218, "beige", {"led": True, "label": "M5"}), ("bear", 322, 160, 26, "ourson"),
            ("cloudlamp", 190, 250, 228, 256),
            ("scallops", 182, 368, 25, [104, 118, 102, 107, 109], "caramel"),
            ("rect", 180, 390, 0, 8, "socle", {}), ("ledh", 180, 390, 4),
            ("rect", 170, 400, 8, 25, "creme", {"label": "M3"}), ("mattress", 185, 385, 25, 50),
            ("rect", 400, 440, 0, 270, "lames", {"flutes": True}),
            ("rect", 440, 500, 0, 70, "creme", {"label": "M6"}), ("rect", 440, 500, 70, 270, "creme", {}),
            ("shelf", 442, 498, 115, True), ("shelf", 442, 498, 160, True), ("shelf", 442, 498, 205, True),
            ("spot", 130),
        ], dims=[("h", [0, 90, 165, 180, 370, 400, 440, 500], 1), ("h", [0, 500], 2), ("t", [170, 400], 1),
                 ("t", [182, 368], 2), ("v", [0, 23, 70, 127, 183, 250, 270], 90),
                 ("v", [0, 8, 25, 50, 104, 118, 218, 270], 370)]),
    },
    plan=dict(items=[
        ("rect", (0, 320, 90, 380), "built", "M1"), ("rect", (90, 345, 165, 380), "built", "M2"),
        ("rect", (170, 280, 400, 380), "built", "M3"), ("rect", (185, 282, 385, 375), "dash", ""),
        ("rect", (400, 377, 440, 380), "built", ""), ("rect", (440, 345, 500, 380), "built", "M6"),
        ("circ", (270, 165), 100, "rug", ""), ("circ", (195, 140), 32, "furn", ""),
        ("circ", (70, 105), 30, "furn", ""), ("circ", (35, 150), 14, "furn", ""), ("circ", (110, 150), 14, "furn", ""),
        ("rect", (395, 110, 470, 140), "furn", ""),
    ], windows=[("W", 140, 330)], doors=[("S", 380, 470, "right")],
        dims=[("x", [0, 90, 165, 170, 400, 440, 500], 380, 9), ("x", [0, 500], 0, -10),
              ("y", [0, 140, 330, 380], 0, -10), ("y", [0, 380], 500, 10), ("y", [280, 380], 400, 5)],
        labels=[(270, 170, "Tapis Ø 200"), (70, 108, "Table Ø 60"), (425, 30, "Porte 90")]),
    section=dict(title="Coupe AA — lit plateforme et arche (vue vers l'ouest)", D=380, H=270, cut_x=280, els=[
        ("ghost", 0, 60, 8, 270, "M1 armoire (au-delà)"), ("ghostwin", 50, 240, 0, 240),
        ("prof", 0, 3, 25, 218, "beige", ""), ("prof", 0, 100, 8, 25, "creme", "M3"), ("prof", 10, 90, 0, 8, "socle", ""),
        ("mattress", 10, 95, 25, 50), ("prof", 3, 13, 25, 118, "caramel", ""), ("led", 50, 4),
        ("cloudlamp", 120, 180, 228, 256),
    ], dims=[("h", [0, 13, 90, 100, 380], 1), ("v", [0, 8, 25, 50, 118, 218, 270], 0)]),
    furniture=[
        ("M1", "Armoire deux portes", "L 90 · P 60 · H 270",
         "Laque crème, poignée ronde caramel Ø 18 à cheval sur les deux portes, socle en retrait éclairé.",
         ("A", 0, 92, 0, 270), (60, 270, [8], 8)),
        ("M2", "Bibliothèque cintrée", "L 75 · P 35 · H 250",
         "Laque crème, fond éclairé, trois tablettes LED, socle fermé h 23.",
         ("A", 88, 167, 0, 255), (35, 250, [23, 70, 127, 183], 0)),
        ("M3", "Lit plateforme flottant", "L 230 · P 100 · H 25 (couchage 90 × 200)",
         "Laque crème, socle en retrait de 10 avec ruban LED, matelas encastré.",
         ("A", 165, 405, 0, 55), (100, 25, [8], 8)),
        ("M4", "Tête de lit festonnée", "L 186 · H 102 à 118",
         "Cinq panneaux tapissés de velours caramel, hauteurs alternées, fixation sur tasseaux.",
         ("A", 175, 375, 20, 125), (10, 93, [], 0)),
        ("M5", "Arche murale lumineuse", "L 190 · H 218 (rayon 95)",
         "Enduit beige sable en léger retrait, contour LED, motif ourson en découpe rétroéclairée.",
         ("A", 175, 375, 20, 225), (3, 193, [], 0)),
        ("M6", "Mur cannelé et bibliothèque", "L 40 + 60 · P 35 · H 270",
         "Lames laquées crème, tablettes éclairées, caisson bas fermé h 70.",
         ("A", 398, 500, 0, 270), (35, 270, [70, 115, 160, 205], 0)),
    ],
)

# ===================================================================================== 5. NUAGE OLIVE
P(
    key="nuageolive", num="05", img="07.png", name="Nuage Olive", type="Chambre d'enfant avec bureau",
    tagline="Un grand nuage blanc découpé dans un mur de lames, et un mobilier sur mesure qui organise toute la vie de l'enfant.",
    facts=[("Typologie", "Chambre d'enfant, 4 – 10 ans"), ("Surface proposée", "≈ 19,8 m² (520 × 380)"),
           ("Hauteur sous plafond", "270 (proposée)"), ("Palette", "Vert olive · crème · bois clair"),
           ("Signature", "Mur cannelé au nuage lumineux, lit gigogne, bureau")],
    concept=[
        "Nuage Olive donne à l'enfant une chambre qui grandit avec lui. Un mur de lames de bois clair, découpé par un grand "
        "nuage blanc rétroéclairé, signe l'espace et sert de tête de lit monumentale.",
        "Autour, un ensemble sur mesure organise chaque usage : armoire, colonne de rangement olive, lit gigogne à tiroirs "
        "et bureau suspendu avec ses étagères, pour lire, dessiner et ranger.",
    ],
    ambiance="Vert olive, crème et bois clair : une palette fraîche et naturelle. Le velours de la tête de lit, la laine du "
             "tapis à pois et le bouclé du tabouret répondent à la ligne graphique des lames.",
    lumiere="Rétroéclairage du nuage, colonne et étagères éclairées, socle lumineux de l'armoire, suspension dôme et "
            "lampe de bureau : chaque zone a sa lumière.",
    palette=["creme", "velours_olive", "lames", "nuage", "laine"],
    room=dict(W=520, D=380, H=270),
    mats={"creme": ("creme", "flat"), "olive": ("velours_olive", "flat"), "velours": ("velours_olive", "velvet"),
          "lames": ("lames", "flutes"), "blanc": ("#FFFFFF", "flat"), "socle": ("#E9E1D8", "flat")},
    materials=[
        ("Laque mate crème", "Armoire, lit gigogne, étagères", "creme", "flat"),
        ("Laque vert olive", "Colonne de rangement, bureau", "velours_olive", "flat"),
        ("Velours olive", "Tête de lit, pouf citrouille", "pouf_olive", "velvet"),
        ("Lames bois clair", "Mur cannelé", "lames", "flutes"),
        ("Laque blanche", "Nuage en découpe rétroéclairé", "nuage", "flat"),
        ("Bouclé crème", "Tabouret du bureau", "boucle", "dots"),
        ("Laine bouclée", "Tapis rond à pois olive", "laine", "dots"),
        ("Coton imprimé", "Linge de lit oursons", "linge", "flat"),
    ],
    elements=[
        "Mur de lames verticales en bois clair",
        "Nuage blanc en découpe, rétroéclairé, en tête de lit",
        "Tête de lit en six panneaux arrondis de velours olive",
        "Colonne de rangement olive à niches éclairées",
        "Bureau suspendu olive, deux étagères flottantes éclairées",
        "Suspension dôme crème au-dessus du lit, lampe champignon olive",
        "Baie toute hauteur avec voilage et rideaux crème",
        "Tapis rond à pois olive, pouf citrouille en velours, voiture à pédales",
    ],
    walls={
        "A": dict(title="Mur A — armoire, colonne, mur cannelé et bureau", W=520, els=[
            ("rect", 0, 120, 0, 8, "socle", {}), ("ledh", 0, 120, 4),
            ("rect", 0, 120, 8, 270, "creme", {"lines": [40, 80], "grips": [(37, 80, 190), (83, 80, 190)], "label": "M1"}),
            ("rect", 120, 180, 0, 270, "olive", {"label": "M2"}),
            ("rect", 122, 178, 8, 36, "olive", {}), ("rect", 122, 178, 36, 65, "olive", {}),
            ("shelf", 122, 178, 65, False), ("shelf", 122, 178, 107, True), ("shelf", 122, 178, 151, True),
            ("shelf", 122, 178, 208, True), ("shelf", 122, 178, 254, True),
            ("rect", 185, 415, 0, 256, "lames", {"flutes": True, "label": "M5"}),
            ("cloud", 255, 415, 58, 200, "blanc", True),
            ("scallops", 195, 405, 36, [117] * 6, "velours"),
            ("rect", 185, 400, 0, 36, "creme", {"lines": [292.5], "label": "M3"}), ("mattress", 195, 395, 36, 58),
            ("rect", 410, 520, 55, 70, "olive", {"lines": [465], "label": "M6"}),
            ("shelf", 420, 510, 135, True), ("shelf", 420, 510, 167, True),
            ("dome", 265, 228, 30), ("spot", 60), ("spot", 460),
        ], dims=[("h", [0, 40, 80, 120, 180, 185, 400, 410, 520], 1), ("h", [0, 520], 2), ("t", [255, 415], 1),
                 ("t", [195, 405], 2), ("v", [0, 8, 36, 65, 107, 151, 208, 254, 270], 180),
                 ("v", [0, 36, 58, 117, 200, 256, 270], 400), ("v", [0, 55, 70, 135, 167, 270], 520)]),
    },
    plan=dict(items=[
        ("rect", (0, 320, 120, 380), "built", "M1"), ("rect", (120, 340, 180, 380), "built", "M2"),
        ("rect", (185, 377, 415, 380), "built", ""), ("rect", (185, 280, 400, 377), "built", "M3"),
        ("rect", (410, 330, 520, 380), "built", "M6"), ("rect", (420, 358, 510, 380), "dash", ""),
        ("circ", (290, 165), 110, "rug", ""), ("circ", (465, 295), 20, "furn", ""), ("circ", (60, 215), 32, "furn", ""),
    ], windows=[("E", 120, 330)], doors=[("S", 40, 130, "left")],
        dims=[("x", [0, 120, 180, 185, 400, 410, 520], 380, 9), ("x", [0, 520], 0, -10),
              ("y", [0, 120, 330, 380], 520, 10), ("y", [0, 380], 0, -10), ("y", [280, 377, 380], 400, 5),
              ("y", [330, 380], 520, 17)],
        labels=[(290, 170, "Tapis Ø 220"), (465, 270, "Tabouret"), (85, 25, "Porte 90")]),
    section=dict(title="Coupe AA — lit gigogne et mur cannelé (vue vers l'ouest)", D=380, H=270, cut_x=290, els=[
        ("ghost", 0, 60, 8, 270, "M1 armoire (au-delà)"), ("ghost", 0, 40, 0, 270, ""),
        ("prof", 0, 3, 0, 256, "lames", ""), ("prof", 3, 6, 58, 200, "blanc", ""),
        ("prof", 0, 100, 0, 36, "creme", "M3"), ("mattress", 10, 95, 36, 58), ("prof", 6, 16, 36, 117, "velours", ""),
        ("dome", 50, 228, 30),
    ], dims=[("h", [0, 6, 16, 100, 380], 1), ("v", [0, 36, 58, 117, 200, 256, 270], 0)]),
    furniture=[
        ("M1", "Armoire trois portes", "L 120 · P 60 · H 270",
         "Laque crème, poignées verticales encastrées, socle en retrait éclairé.",
         ("A", 0, 122, 0, 270), (60, 270, [8], 8)),
        ("M2", "Colonne de rangement olive", "L 60 · P 40 · H 270",
         "Laque vert olive, cinq niches éclairées, deux tiroirs en partie basse.",
         ("A", 118, 182, 0, 270), (40, 270, [8, 36, 65, 107, 151, 208, 254], 0)),
        ("M3", "Lit gigogne à tiroirs", "L 215 · P 100 · H 36 (couchage 90 × 200)",
         "Laque crème, deux grands tiroirs de rangement ou couchage d'appoint.",
         ("A", 183, 402, 0, 62), (100, 36, [], 0)),
        ("M4", "Tête de lit six panneaux", "L 210 · H 117",
         "Panneaux arrondis tapissés de velours olive, fixation sur tasseaux.",
         ("A", 190, 410, 30, 122), (10, 81, [], 0)),
        ("M5", "Mur cannelé et nuage", "L 230 · H 256 ; nuage 160 × 142",
         "Lames verticales bois clair, nuage en MDF laqué blanc en applique, LED périmétrique 2700 K.",
         ("A", 183, 417, 0, 262), (6, 256, [], 0)),
        ("M6", "Bureau suspendu et étagères", "L 110 · P 50 · H 70 ; étagères 90 × 22",
         "Laque olive, deux tiroirs ; étagères crème éclairées à 135 et 167.",
         ("A", 405, 520, 45, 175), (50, 70, [55], 0)),
    ],
)
