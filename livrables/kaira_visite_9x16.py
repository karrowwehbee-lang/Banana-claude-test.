"""KAÏRA Interior Design — Visite vidéo cinématique 9:16 (TikTok / Instagram Reels) dans Blender.

Ce script s'utilise dans TON fichier .blend, en 4 étapes. Change la valeur de ETAPE puis clique sur Run Script
(onglet Scripting). Rien dans ton architecture, ton mobilier ou tes matériaux n'est modifié : le script ajoute
uniquement des caméras (collection « KAIRA_Visite ») et, à la fin, une scène de montage séparée.

  ETAPE = "1_PREPARER"  crée 2 caméras repères par plan : S01_debut et S01_fin, S02_debut… (22 caméras).
                        Tu les places toi-même dans la maison (voir le guide : Ctrl+Alt+Pavé0).
  ETAPE = "2_ANIMER"    crée les caméras animées CAM_01 à CAM_11 : trajet fluide du repère « début »
                        au repère « fin », avec accélération et freinage progressifs. Régle le format 9:16.
  ETAPE = "3_RENDRE"    rend chaque plan en images PNG (dossier KAIRA_visite/ à côté du .blend).
                        Relançable : les images déjà rendues ne sont pas recalculées.
  ETAPE = "4_MONTER"    crée la scène « KAIRA_Montage » : enchaînements, fondus, titres, logo, musique,
                        export MP4 H.264 1080 × 1920. Il reste à faire Rendu > Rendre l'animation (Ctrl+F12).

Testé avec Blender 4.2 LTS. Pour 4.3+ et 5.x, les noms d'API qui ont changé sont gérés automatiquement.
"""
import math
import os
import bpy
from mathutils import Vector

ETAPE = "1_PREPARER"

# ------------------------------------------------------------------ RÉGLAGES
FPS = 30
RESOLUTION = (1080, 1920)          # 9:16 vertical. Mettre (2160, 3840) pour une version 4K.
POIGNEE = 12                       # images ajoutées avant/après chaque plan pour les fondus (0,4 s)
FONDU = 12                         # durée d'un fondu enchaîné, en images
DOSSIER = "//KAIRA_visite/"        # « // » = à côté du fichier .blend
REGLER_CYCLES = True               # applique les réglages de rendu conseillés (étape 3)
ECHANTILLONS = 256                 # 128 = plus rapide, 512 = plus propre
PLANS_A_RENDRE = []                # [] = tous ; ex. [1, 2] pour ne rendre que les plans 1 et 2
MUSIQUE = ""                       # chemin d'un fichier audio libre de droits (optionnel)
LOGO_IMAGE = ""                    # chemin du logo KAÏRA en PNG transparent (optionnel)
POLICE = ""                        # chemin d'un fichier .ttf/.otf pour les titres (optionnel)
TITRES_PIECES = True               # petit titre en bas de l'image au début de chaque pièce

# n, nom, secondes, focale (mm), transition vers le plan suivant ("coupe" ou "fondu"), titre de pièce
PLANS = [
    (1, "Ouverture — le seuil",             4, 20, "fondu", "Salon principal"),
    (2, "Révélation du salon",              6, 20, "coupe", None),
    (3, "Le mur TV",                        5, 22, "fondu", None),
    (4, "Sous la ligne de lumière",         5, 20, "coupe", "Salle à manger"),
    (5, "Détail — bibliothèque et marbre",  4, 35, "fondu", None),
    (6, "Entrée dans la chambre d'amis",    5, 18, "coupe", "Chambre d'amis"),
    (7, "Le mur de marbre",                 4, 22, "fondu", None),
    (8, "Arrivée à l'étage",                6, 20, "coupe", "Séjour"),
    (9, "Bois et lumière",                  4, 24, "fondu", None),
    (10, "Vers la suite",                   6, 18, "fondu", "Chambre principale"),
    (11, "Finale — l'écrin",                6, 22, "fin", None),
]
DUREE_LOGO = 3
# ---------------------------------------------------------------------------

COL = "KAIRA_Visite"
sc = bpy.context.scene


def collection():
    c = bpy.data.collections.get(COL)
    if c is None:
        c = bpy.data.collections.new(COL)
        sc.collection.children.link(c)
    return c


def reglage_format(scene):
    scene.render.resolution_x, scene.render.resolution_y = RESOLUTION
    scene.render.resolution_percentage = 100
    scene.render.fps, scene.render.fps_base = FPS, 1.0


def plage(i):
    """Plage d'images du plan i (index 0) sur la ligne de temps de la scène 3D : (début avec poignée, début visible, fin visible, fin avec poignée)."""
    t = 1
    for k in range(i):
        t += PLANS[k][2] * FPS + 2 * POIGNEE
    s = t + POIGNEE
    return t, s, s + PLANS[i][2] * FPS - 1, s + PLANS[i][2] * FPS - 1 + POIGNEE


# ================================================================== 1. PRÉPARER
def preparer():
    reglage_format(sc)
    c = collection()
    origine = sc.cursor.location.copy()
    for i, (n, nom, sec, focale, _, _) in enumerate(PLANS):
        for j, suffixe in enumerate(("debut", "fin")):
            nm = f"S{n:02d}_{suffixe}"
            if bpy.data.objects.get(nm):
                continue                      # déjà placé : on ne touche à rien
            cd = bpy.data.cameras.new(nm)
            cd.lens = focale
            cd.sensor_fit = "AUTO"
            cd.display_size = 0.25
            ob = bpy.data.objects.new(nm, cd)
            c.objects.link(ob)
            ob.location = origine + Vector((i * 0.6, j * 0.6, 1.6))
            ob.rotation_euler = (math.radians(90), 0, 0)
    print("KAÏRA : 22 caméras repères créées dans la collection", COL, "— place-les puis passe à l'étape 2_ANIMER.")


# ================================================================== 2. ANIMER
def cle_transform(ob, mat, frame):
    loc, rot, _ = mat.decompose()
    ob.location = loc
    if ob.rotation_mode != "QUATERNION":
        ob.rotation_mode = "QUATERNION"
    prev = ob.get("_kq")
    if prev is not None and rot.dot(Vector(prev)) < 0:   # évite les retournements de rotation
        rot.negate()
    ob["_kq"] = list(rot)
    ob.rotation_quaternion = rot
    ob.keyframe_insert("location", frame=frame)
    ob.keyframe_insert("rotation_quaternion", frame=frame)


def fcurves(ob):
    ad = ob.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    if hasattr(act, "fcurves"):
        try:
            return list(act.fcurves)
        except Exception:
            pass
    out = []                                     # Blender 4.4+ / 5.x : actions en couches
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for bag in getattr(strip, "channelbags", []):
                out += list(bag.fcurves)
    return out


def animer():
    reglage_format(sc)
    bpy.context.view_layer.update()            # positions des repères à jour
    c = collection()
    manquants = [f"S{n:02d}_{s}" for n, *_ in PLANS for s in ("debut", "fin") if not bpy.data.objects.get(f"S{n:02d}_{s}")]
    if manquants:
        raise RuntimeError("Repères manquants : " + ", ".join(manquants) + " — lance d'abord l'étape 1_PREPARER.")
    for m in [m for m in sc.timeline_markers if m.name.startswith("CAM_")]:
        sc.timeline_markers.remove(m)
    for i, (n, nom, sec, focale, _, _) in enumerate(PLANS):
        a, b = bpy.data.objects[f"S{n:02d}_debut"], bpy.data.objects[f"S{n:02d}_fin"]
        nm = f"CAM_{n:02d}"
        ob = bpy.data.objects.get(nm)
        if ob is None:
            cd = bpy.data.cameras.new(nm)
            ob = bpy.data.objects.new(nm, cd)
            c.objects.link(ob)
        ob.animation_data_clear()
        ob.data.animation_data_clear()
        if "_kq" in ob:
            del ob["_kq"]
        # optique reprise du repère « début » (focale, mise au point, ouverture)
        for attr in ("lens", "sensor_width", "sensor_fit", "clip_start", "clip_end", "shift_x", "shift_y"):
            setattr(ob.data, attr, getattr(a.data, attr))
        ob.data.dof.use_dof = a.data.dof.use_dof
        ob.data.dof.focus_distance = a.data.dof.focus_distance
        ob.data.dof.aperture_fstop = a.data.dof.aperture_fstop
        t0, s, e, t1 = plage(i)
        cle_transform(ob, a.matrix_world.copy(), t0)
        cle_transform(ob, b.matrix_world.copy(), t1)
        if a.data.lens != b.data.lens:            # zoom éventuel entre les deux repères
            ob.data.lens = a.data.lens; ob.data.keyframe_insert("lens", frame=t0)
            ob.data.lens = b.data.lens; ob.data.keyframe_insert("lens", frame=t1)
        for fc in fcurves(ob):                    # accélération / freinage progressifs, très doux
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.easing = "EASE_IN_OUT"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        mk = sc.timeline_markers.new(nm, frame=t0)
        mk.camera = ob
    sc.frame_start, sc.frame_end = 1, plage(len(PLANS) - 1)[3]
    sc.camera = bpy.data.objects["CAM_01"]
    sc.render.use_motion_blur = True
    total = sum(p[2] for p in PLANS) + DUREE_LOGO
    print(f"KAÏRA : 11 caméras animées. Durée finale ≈ {total} s. Vérifie avec Lecture (Espace) en vue caméra (Pavé 0).")


# ================================================================== 3. RENDRE
def regler_cycles(scene):
    scene.render.engine = "CYCLES"
    cy = scene.cycles
    cy.samples = ECHANTILLONS
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except TypeError:
        pass
    cy.use_adaptive_sampling = True
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for t in ("OPTIX", "CUDA", "HIP", "METAL", "ONEAPI"):
            try:
                prefs.compute_device_type = t
                prefs.get_devices()
                if any(d.type == t for d in prefs.devices):
                    for d in prefs.devices:
                        d.use = d.type == t
                    cy.device = "GPU"
                    break
            except TypeError:
                continue
    except Exception:
        pass
    scene.render.use_persistent_data = True       # accélère les images suivantes
    scene.render.use_motion_blur = True
    scene.render.motion_blur_shutter = 0.5
    try:
        scene.view_settings.view_transform = "AgX"
    except TypeError:
        pass


def rendre():
    reglage_format(sc)
    if REGLER_CYCLES:
        regler_cycles(sc)
    im = sc.render.image_settings
    im.file_format, im.color_mode, im.compression = "PNG", "RGB", 15
    sc.render.use_overwrite = False               # reprise possible : images existantes ignorées
    sc.render.use_placeholder = True              # plusieurs ordinateurs peuvent rendre en parallèle
    a_rendre = PLANS_A_RENDRE or [p[0] for p in PLANS]
    fs, fe, cam = sc.frame_start, sc.frame_end, sc.camera
    for i, p in enumerate(PLANS):
        n = p[0]
        if n not in a_rendre:
            continue
        t0, _, _, t1 = plage(i)
        sc.camera = bpy.data.objects[f"CAM_{n:02d}"]
        sc.frame_start, sc.frame_end = t0, t1
        sc.render.filepath = f"{DOSSIER}S{n:02d}/image_"
        print(f"KAÏRA : rendu du plan {n:02d} ({t1 - t0 + 1} images)…")
        bpy.ops.render.render(animation=True)
    sc.frame_start, sc.frame_end, sc.camera = fs, fe, cam
    print("KAÏRA : rendus terminés dans", bpy.path.abspath(DOSSIER))


# ================================================================== 4. MONTER
def strips(se):
    return se.strips if hasattr(se, "strips") else se.sequences


def effet(coll, nom, kind, canal, debut, fin, s1=None, s2=None):
    for kw in (dict(input1=s1, input2=s2), dict(seq1=s1, seq2=s2)):
        kw = {k: v for k, v in kw.items() if v is not None}
        try:
            return coll.new_effect(name=nom, type=kind, channel=canal, frame_start=debut, frame_end=fin, **kw)
        except TypeError:
            continue
    raise RuntimeError("API du montage non reconnue")


def bornes(st, debut, fin):
    """Garde uniquement [debut, fin[ sur la ligne de montage (compatible 4.x et 5.x)."""
    for a, b in (("frame_final_start", "frame_final_end"), ("left_handle", "right_handle")):
        if hasattr(st, a):
            setattr(st, a, debut)
            setattr(st, b, fin)
            return


def texte(coll, nom, txt, canal, debut, fin, taille, y, police=None):
    t = effet(coll, nom, "TEXT", canal, debut, fin)
    t.text = txt
    t.font_size = int(taille * RESOLUTION[0] / 1080)
    t.location = (0.5, y)
    t.color = (1, 1, 1, 1)
    for a in ("align_x", "anchor_x"):
        if hasattr(t, a):
            setattr(t, a, "CENTER")
    for a in ("align_y", "anchor_y"):
        if hasattr(t, a):
            setattr(t, a, "CENTER")
    if police and os.path.exists(police):
        t.font = bpy.data.fonts.load(police, check_existing=True)
    if hasattr(t, "use_shadow"):
        t.use_shadow = True
    t.blend_type = "ALPHA_OVER"
    return t


def cle_opacite(st, valeurs):
    attr = "blend_alpha"
    for f, v in valeurs:
        setattr(st, attr, v)
        st.keyframe_insert(attr, frame=f)


def monter():
    src = bpy.path.abspath(DOSSIER)
    m = bpy.data.scenes.get("KAIRA_Montage") or bpy.data.scenes.new("KAIRA_Montage")
    reglage_format(m)
    m.sequence_editor_clear() if m.sequence_editor else None
    se = m.sequence_editor_create()
    coll = strips(se)
    T, prev, pos = 1, None, []
    for i, (n, nom, sec, _, trans, titre) in enumerate(PLANS):
        d = sec * FPS
        dossier = os.path.join(src, f"S{n:02d}")
        files = sorted(f for f in os.listdir(dossier) if f.lower().endswith(".png")) if os.path.isdir(dossier) else []
        if not files:
            raise RuntimeError(f"Aucune image pour le plan {n:02d} dans {dossier} — lance l'étape 3_RENDRE.")
        canal = 1 + (i % 2)
        st = coll.new_image(name=f"S{n:02d}", filepath=os.path.join(dossier, files[0]), channel=canal, frame_start=T - POIGNEE)
        for f in files[1:]:
            st.elements.append(f)
        entree_fondu = i > 0 and PLANS[i - 1][4] == "fondu"
        sortie_fondu = trans == "fondu"
        bornes(st, T - (FONDU // 2 if entree_fondu else 0), T + d + (FONDU // 2 if sortie_fondu else 0))
        if entree_fondu and prev is not None:
            effet(coll, f"fondu_{n:02d}", "GAMMA_CROSS", 3, T - FONDU // 2, T + FONDU // 2, prev, st)
        pos.append((T, d, titre))
        prev, T = st, T + d
    premier, dernier = coll[f"S{PLANS[0][0]:02d}"], prev
    cle_opacite(premier, [(1, 0.0), (1 + 18, 1.0)])                       # fondu du noir
    cle_opacite(dernier, [(T - 24, 1.0), (T, 0.0)])                        # fondu au noir
    if TITRES_PIECES:
        for k, (t, d, titre) in enumerate(pos):
            if titre:
                f, a, b = max(1, FPS // 3), t + FPS // 3, t + FPS // 3 + int(1.6 * FPS)
                tt = texte(coll, f"titre_{k}", titre.upper(), 5, a, b, 34, 0.32, POLICE)   # au-dessus de la zone des légendes TikTok/Reels
                cle_opacite(tt, [(a, 0), (a + f, 1), (b - f, 1), (b, 0)])
    L = DUREE_LOGO * FPS
    if LOGO_IMAGE and os.path.exists(LOGO_IMAGE):
        lg = coll.new_image(name="logo", filepath=LOGO_IMAGE, channel=6, frame_start=T)
        bornes(lg, T, T + L)
        lg.blend_type = "ALPHA_OVER"
    else:
        lg = texte(coll, "logo", "KAÏRA", 6, T, T + L, 120, 0.52, POLICE)
        sub = texte(coll, "logo_sous_titre", "INTERIOR DESIGN", 7, T, T + L, 30, 0.45, POLICE)
        cle_opacite(sub, [(T, 0), (T + 15, 1), (T + L - 10, 1), (T + L, 0)])
    cle_opacite(lg, [(T, 0), (T + 15, 1), (T + L - 10, 1), (T + L, 0)])
    fin = T + L - 1
    if MUSIQUE and os.path.exists(MUSIQUE):
        mu = coll.new_sound(name="musique", filepath=MUSIQUE, channel=8, frame_start=1)
        bornes(mu, 1, fin + 1)
        for f, v in ((1, 0.0), (20, 1.0), (fin - 45, 1.0), (fin, 0.0)):
            mu.volume = v
            mu.keyframe_insert("volume", frame=f)
    m.frame_start, m.frame_end = 1, fin
    r = m.render
    r.image_settings.file_format = "FFMPEG"
    r.ffmpeg.format = "MPEG4"
    r.ffmpeg.codec = "H264"
    r.ffmpeg.constant_rate_factor = "HIGH"
    r.ffmpeg.ffmpeg_preset = "GOOD"
    r.ffmpeg.gopsize = FPS
    r.ffmpeg.audio_codec = "AAC" if MUSIQUE else "NONE"
    r.use_sequencer = True
    r.filepath = f"{DOSSIER}KAIRA_visite_9x16.mp4"
    if bpy.context.window:
        bpy.context.window.scene = m
    print(f"KAÏRA : montage prêt ({fin / FPS:.1f} s). Rendu > Rendre l'animation (Ctrl+F12) pour exporter le MP4.")


{"1_PREPARER": preparer, "2_ANIMER": animer, "3_RENDRE": rendre, "4_MONTER": monter}[ETAPE]()
