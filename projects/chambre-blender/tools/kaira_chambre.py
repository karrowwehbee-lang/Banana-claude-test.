"""KAÏRA Interior Design — Aménagement de la chambre (script Blender 4.x / 5.x)

Ajoute dans TON fichier .blend, sans toucher à l'architecture existante :
  1. Tête de lit flottante rembourrée (bouclé crème, cadre chêne, filet laiton)
  2. Lit 180 × 200 sur sommier tapissé + linge de lit + plaid vert sauge + coussin cognac
  3. Banc en bout de lit (velours vert, piètement laiton)
  4. Plafond architectural : faux plafond périphérique, caisson central avec gorge LED,
     bande de lames chêne dans l'axe du marbre
  5. Éclairage : gorges LED 2700 K, rasants sur le marbre, suspensions de chevet, fill doux
  6. Réglages de rendu Cycles + une caméra cadrée comme ta vue

UTILISATION
  a. Ouvre ton .blend.
  b. Place le curseur 3D AU SOL, au milieu du panneau de marbre, contre le mur
     (Shift + clic droit, ou N > View > 3D Cursor).
  c. Règle INTO_ROOM ci-dessous : l'axe qui part du mur de marbre vers l'intérieur de la chambre.
  d. Vérifie les cotes du bloc RÉGLAGES (hauteur sous plafond, largeur du marbre, etc.).
  e. Onglet Scripting > Open > ce fichier > Run Script.
  Tout est créé dans la collection « KAIRA_Amenagement » : la supprimer annule tout.
"""
import math
import bpy
import bmesh
from mathutils import Vector, Matrix

# ------------------------------------------------------------------ RÉGLAGES
INTO_ROOM = "-Y"          # axe mur de marbre -> chambre : "X", "-X", "Y" ou "-Y"
CEILING = 2.80            # hauteur sous plafond brute (m)
DROP = 2.60               # sous-face du faux plafond périphérique
MARBLE_W = 1.20           # largeur du panneau de marbre
TRAY_W, TRAY_D = 3.10, 3.30   # caisson central (largeur, profondeur depuis le mur)
ROOM_W, ROOM_D = 3.90, 4.60   # chambre (pour le faux plafond périphérique)
NIGHTSTAND_X = 1.25       # entraxe chevet / axe du lit (pour les suspensions)
MATTRESS = (1.80, 2.00)   # 160 × 200 ou 180 × 200
ADD_CEILING = True
ADD_CAMERA = True
# ---------------------------------------------------------------------------

COL_NAME = "KAIRA_Amenagement"
origin = bpy.context.scene.cursor.location.copy()
axes = {"Y": (Vector((1, 0, 0)), Vector((0, 1, 0))), "-Y": (Vector((-1, 0, 0)), Vector((0, -1, 0))),
        "X": (Vector((0, -1, 0)), Vector((1, 0, 0))), "-X": (Vector((0, 1, 0)), Vector((-1, 0, 0)))}
U, F = axes[INTO_ROOM]            # U = largeur (gauche -> droite vue depuis la chambre), F = profondeur
BASIS = Matrix(((U.x, F.x, 0), (U.y, F.y, 0), (U.z, F.z, 1)))


def P(x, d, z):
    """Point local (x = largeur, d = distance au mur, z = hauteur) -> monde."""
    return origin + U * x + F * d + Vector((0, 0, z))


col = bpy.data.collections.get(COL_NAME) or bpy.data.collections.new(COL_NAME)
if col.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(col)


# ------------------------------------------------------------------ matériaux
def mat(name, color, rough=0.5, metal=0.0, emit=None, strength=0.0, sheen=0.0, coat=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    for key, val in (("Sheen Weight", sheen), ("Coat Weight", coat)):
        if key in b.inputs:
            b.inputs[key].default_value = val
    if emit:
        for key in ("Emission Color", "Emission"):
            if key in b.inputs:
                b.inputs[key].default_value = (*emit, 1)
                break
        b.inputs["Emission Strength"].default_value = strength
    return m


def srgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)


MAT = {
    "boucle": mat("KAIRA_Boucle_Creme", srgb("#ece4d6"), 1.0, sheen=0.4),
    "linen_taupe": mat("KAIRA_Lin_Taupe", srgb("#9c8a78"), 0.95, sheen=0.3),
    "sheet": mat("KAIRA_Linge_Blanc", srgb("#f4f1ea"), 0.9, sheen=0.3),
    "pillow2": mat("KAIRA_Lin_Sable", srgb("#dccfbb"), 0.95, sheen=0.3),
    "velvet": mat("KAIRA_Velours_Sauge", srgb("#4b5a3e"), 0.7, sheen=1.0),
    "cognac": mat("KAIRA_Cuir_Cognac", srgb("#8a5a34"), 0.45, coat=0.2),
    "oak": bpy.data.materials.get("bois maron") or mat("KAIRA_Chene", srgb("#a8714a"), 0.5),   # réutilise ton chêne s'il existe
    "brass": mat("KAIRA_Laiton_Brosse", srgb("#b8925a"), 0.28, metal=1.0),
    "white": mat("KAIRA_Plafond_Blanc", srgb("#f3f1ec"), 0.85),
    "gap": mat("KAIRA_Joint_Creux", srgb("#1e1b18"), 1.0),
    "led": mat("KAIRA_LED_2700K", (1, 0.62, 0.3), 1.0, emit=(1.0, 0.66, 0.36), strength=25.0),
    "opal": mat("KAIRA_Verre_Opalin", srgb("#fff4e2"), 0.35, emit=(1.0, 0.8, 0.55), strength=6.0),
}


# ------------------------------------------------------------------ géométrie
def block(name, x0, x1, d0, d1, z0, z1, material, bevel=0.0, segments=3):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    col.objects.link(ob)
    ob.scale = (abs(x1 - x0), abs(d1 - d0), abs(z1 - z0))
    ob.matrix_world = Matrix.Translation(P((x0 + x1) / 2, (d0 + d1) / 2, (z0 + z1) / 2)) @ BASIS.to_4x4() @ Matrix.Diagonal((*ob.scale, 1))
    ob.data.materials.append(material)
    if bevel:
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        ob.select_set(False)
        mod = ob.modifiers.new("Bevel", "BEVEL")
        mod.width, mod.segments, mod.limit_method = bevel, segments, "NONE"
        ob.modifiers.new("Smooth", "WEIGHTED_NORMAL")
        for p in ob.data.polygons:
            p.use_smooth = True
    return ob


def rod(name, x, d, z0, z1, r, material):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=z1 - z0, location=P(x, d, (z0 + z1) / 2), vertices=24)
    ob = bpy.context.active_object
    for c in ob.users_collection:
        c.objects.unlink(ob)
    col.objects.link(ob)
    ob.name = name
    ob.data.materials.append(material)
    return ob


def light(name, kind, x, d, z, energy, color=(1.0, 0.75, 0.5), size=0.1, aim=None, spot_deg=50):
    ld = bpy.data.lights.new(name, kind)
    ld.energy, ld.color = energy, color
    if kind == "AREA":
        ld.shape, ld.size = "RECTANGLE", size
    if kind == "SPOT":
        ld.spot_size, ld.spot_blend, ld.shadow_soft_size = math.radians(spot_deg), 0.6, 0.03
    if kind == "POINT":
        ld.shadow_soft_size = size
    ob = bpy.data.objects.new(name, ld)
    col.objects.link(ob)
    ob.location = P(x, d, z)
    if aim is not None:
        direction = P(*aim) - ob.location
        ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return ob


mw, md = MATTRESS
# 1. Tête de lit flottante : cadre chêne 2300 × 850 + coussin bouclé 2200 × 800 + filet laiton
block("KAIRA_TeteDeLit_Cadre", -1.15, 1.15, 0.04, 0.10, 0.30, 1.15, MAT["oak"], bevel=0.004)
block("KAIRA_TeteDeLit_Coussin", -1.10, 1.10, 0.09, 0.19, 0.33, 1.13, MAT["boucle"], bevel=0.04, segments=6)
for x in (-0.55, 0.0, 0.55):
    block(f"KAIRA_TeteDeLit_Joint_{x}", x - 0.003, x + 0.003, 0.188, 0.191, 0.36, 1.10, MAT["gap"])
block("KAIRA_TeteDeLit_Laiton", -1.15, 1.15, 0.04, 0.11, 1.15, 1.158, MAT["brass"])
# 2. Lit
block("KAIRA_Lit_Socle", -mw / 2 + 0.02, mw / 2 - 0.02, 0.25, md + 0.30, 0, 0.08, MAT["gap"])
block("KAIRA_Lit_Sommier", -mw / 2 - 0.05, mw / 2 + 0.05, 0.19, md + 0.36, 0.08, 0.34, MAT["linen_taupe"], bevel=0.04, segments=4)
block("KAIRA_Lit_Matelas", -mw / 2, mw / 2, 0.22, md + 0.30, 0.34, 0.58, MAT["sheet"], bevel=0.05, segments=5)
block("KAIRA_Lit_Couette", -mw / 2 - 0.03, mw / 2 + 0.03, 0.75, md + 0.34, 0.52, 0.64, MAT["sheet"], bevel=0.06, segments=6)
block("KAIRA_Lit_Plaid", -mw / 2 - 0.05, mw / 2 + 0.05, md - 0.15, md + 0.28, 0.60, 0.67, MAT["velvet"], bevel=0.04, segments=5)
for i, x in enumerate((-0.45, 0.45)):
    block(f"KAIRA_Oreiller_{i}", x - 0.37, x + 0.37, 0.24, 0.42, 0.58, 1.02, MAT["sheet"], bevel=0.08, segments=6)
    block(f"KAIRA_Coussin_{i}", x - 0.28, x + 0.28, 0.40, 0.55, 0.60, 0.94, MAT["pillow2"], bevel=0.07, segments=6)
block("KAIRA_Coussin_Cognac", -0.28, 0.28, 0.55, 0.69, 0.62, 0.86, MAT["cognac"], bevel=0.06, segments=6)
# 3. Banc en bout de lit
block("KAIRA_Banc_Assise", -0.70, 0.70, md + 0.50, md + 0.92, 0.40, 0.48, MAT["velvet"], bevel=0.04, segments=5)
block("KAIRA_Banc_Chene", -0.66, 0.66, md + 0.53, md + 0.89, 0.36, 0.40, MAT["oak"], bevel=0.003)
for x in (-0.62, 0.62):
    for d in (md + 0.56, md + 0.86):
        rod(f"KAIRA_Banc_Pied_{x}_{d}", x, d, 0, 0.36, 0.015, MAT["brass"])
# 4. Plafond architectural
if ADD_CEILING:
    tx = TRAY_W / 2
    block("KAIRA_FP_Pied", -ROOM_W / 2, ROOM_W / 2, TRAY_D, ROOM_D, DROP, CEILING, MAT["white"])
    block("KAIRA_FP_Gauche", -ROOM_W / 2, -tx, 0.0, TRAY_D, DROP, CEILING, MAT["white"])
    block("KAIRA_FP_Droite", tx, ROOM_W / 2, 0.0, TRAY_D, DROP, CEILING, MAT["white"])
    # gorges LED (rubans émissifs cachés dans le retour du faux plafond)
    block("KAIRA_LED_Gorge_G", -tx - 0.06, -tx - 0.05, 0.10, TRAY_D - 0.05, DROP + 0.05, DROP + 0.056, MAT["led"])
    block("KAIRA_LED_Gorge_D", tx + 0.05, tx + 0.06, 0.10, TRAY_D - 0.05, DROP + 0.05, DROP + 0.056, MAT["led"])
    block("KAIRA_LED_Gorge_P", -tx, tx, TRAY_D + 0.05, TRAY_D + 0.06, DROP + 0.05, DROP + 0.056, MAT["led"])
    # lames chêne 40 mm au pas de 60 mm dans l'axe du marbre, sur 2,30 m
    x = -MARBLE_W / 2
    i = 0
    while x < MARBLE_W / 2 - 0.01:
        block(f"KAIRA_Lame_{i:02d}", x + 0.005, x + 0.045, 0.0, 2.30, CEILING - 0.04, CEILING, MAT["oak"], bevel=0.002)
        x += 0.06
        i += 1
    block("KAIRA_Lames_Laiton", -MARBLE_W / 2 - 0.02, MARBLE_W / 2 + 0.02, 2.30, 2.32, CEILING - 0.045, CEILING - 0.04, MAT["brass"])
# 5. Éclairage
for i, x in enumerate((-NIGHTSTAND_X, NIGHTSTAND_X)):          # suspensions de chevet (globe opalin, centre à 1,38 m)
    rod(f"KAIRA_Suspension_Tige_{i}", x, 0.244, 1.48, DROP, 0.004, MAT["brass"])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=P(x, 0.244, 1.38), segments=48, ring_count=24)
    g = bpy.context.active_object
    for c in g.users_collection:
        c.objects.unlink(g)
    col.objects.link(g)
    g.name = f"KAIRA_Suspension_Globe_{i}"
    g.data.materials.append(MAT["opal"])
    bpy.ops.object.shade_smooth()
    light(f"KAIRA_Suspension_Lumiere_{i}", "POINT", x, 0.30, 1.30, 25, size=0.08)
for i, x in enumerate((-0.35, 0.35)):                             # rasants sur le marbre
    light(f"KAIRA_Rasant_Marbre_{i}", "SPOT", x, 0.75, DROP - 0.02, 60, aim=(x * 0.5, 0.0, 1.6), spot_deg=35)
light("KAIRA_Fill_Caisson", "AREA", 0, TRAY_D / 2, CEILING - 0.10, 40, size=1.5, aim=(0, TRAY_D / 2, 0))

# 6. Rendu Cycles + caméra
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.samples = 512
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 2400, 1600
try:
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
except TypeError:
    sc.view_settings.view_transform = "Filmic"
sc.view_settings.exposure = 0.3
if ADD_CAMERA:
    cd = bpy.data.cameras.new("KAIRA_Camera")
    cd.lens = 18
    cam = bpy.data.objects.new("KAIRA_Camera", cd)
    col.objects.link(cam)
    cam.location = P(0.0, ROOM_D - 0.15, 1.40)
    cam.rotation_euler = (P(0, 0, 1.25) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
print("KAÏRA : aménagement ajouté dans la collection", COL_NAME)
