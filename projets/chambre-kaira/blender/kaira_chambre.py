"""
KAÏRA Interior Design — Chambre : aménagement (lit, tête de lit, plafond, éclairage)

Deux usages :

1. Dans TON fichier Blender (Scripting > Open > Run Script), avec BUILD_SHELL = False.
   Le script crée une collection « KAIRA_Amenagement » rattachée à un Empty
   « KAIRA_Origine ». Place cet Empty au pied du panneau en marbre, au sol, au
   centre du panneau, axe Y pointant vers l'intérieur de la chambre
   (Snap sur la face du marbre, puis rotation si besoin). Tout suit.
   Ajuste ROOM_W / ROOM_D / CEIL_H à tes cotes avant de lancer.

2. En ligne de commande pour reconstruire la pièce et rendre les vues :
   python kaira_chambre.py --shell --render out_dir

Unités : mètres. Axe X = largeur du mur de tête, Y = vers la porte, Z = hauteur.
"""
import bpy, bmesh, math, sys, os, random
from mathutils import Vector

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
BUILD_SHELL = "--shell" in ARGS          # recrée murs/marbre/colonnes/chevets (absent de ton fichier)
RENDER_DIR = ARGS[ARGS.index("--render") + 1] if "--render" in ARGS else None
SAMPLES = int(ARGS[ARGS.index("--samples") + 1]) if "--samples" in ARGS else 256
VIEWS = ARGS[ARGS.index("--views") + 1].split(",") if "--views" in ARGS else ["v1", "v2", "v3"]

# ---------------- cotes (à ajuster à ton modèle) ----------------
ROOM_W = 4.60      # largeur du mur de tête
ROOM_D = 5.40      # profondeur
CEIL_H = 2.85      # hauteur sous dalle
DROP_H = 2.62      # sous-face du faux-plafond périphérique
MARBLE_W = 1.30
COL_X, COL_W = 1.50, 0.42          # axes des colonnes chêne
BED_W, BED_L = 2.00, 2.15          # cadre pour matelas 180 x 200
HB_W, HB_H = 2.24, 1.22            # tête de lit

random.seed(4)

# ---------------- helpers ----------------
if BUILD_SHELL:
    bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

col = bpy.data.collections.get("KAIRA_Amenagement") or bpy.data.collections.new("KAIRA_Amenagement")
if col.name not in scene.collection.children:
    scene.collection.children.link(col)
origin = bpy.data.objects.get("KAIRA_Origine")
if origin is None:
    origin = bpy.data.objects.new("KAIRA_Origine", None)
    origin.empty_display_type = "ARROWS"; origin.empty_display_size = 0.5
    col.objects.link(origin)

def link(ob, shell=False):
    target = col
    if shell:
        target = bpy.data.collections.get("KAIRA_Existant") or bpy.data.collections.new("KAIRA_Existant")
        if target.name not in scene.collection.children:
            scene.collection.children.link(target)
    target.objects.link(ob)
    ob.parent = origin
    return ob

def box(name, x0, x1, y0, y1, z0, z1, mat, bevel=0.002, seg=2, shell=False):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    sx, sy, sz = x1 - x0, y1 - y0, z1 - z0
    for v in bm.verts:
        v.co.x *= sx; v.co.y *= sy; v.co.z *= sz
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    me.materials.append(mat)
    if bevel:
        m = ob.modifiers.new("Bevel", "BEVEL"); m.width = bevel; m.segments = seg; m.limit_method = "ANGLE"
    return link(ob, shell)

def soft(name, x, y, z, dims, mat, rot=(0, 0, 0), level=2, round_=0.45, puff=0.0, shell=False):
    """Coussins, couette : boîte aux arêtes arrondies + subdivision = volume souple."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= dims[0]; v.co.y *= dims[1]; v.co.z *= dims[2]
    r = min(dims) * round_
    bmesh.ops.bevel(bm, geom=list(bm.edges), offset=r, segments=2, affect="EDGES", profile=0.5)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = (x, y, z); ob.rotation_euler = rot
    me.materials.append(mat)
    s = ob.modifiers.new("Subsurf", "SUBSURF"); s.levels = level; s.render_levels = level
    if puff:
        s.levels = s.render_levels = 3
        c = ob.modifiers.new("Gonflant", "CAST"); c.cast_type = "SPHERE"; c.factor = puff
        c.use_x = False; c.use_z = False; c.use_y = True
    for p in me.polygons: p.use_smooth = True
    return link(ob, shell)

def pillow(name, x, y, z, dims, mat, rot=(0, 0, 0), shell=False):
    """Coussin : sphère aplatie en coussin (Cast cuboïde) = faces bombées, coins pincés."""
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=24, radius=0.5)
    for v in bm.verts:
        v.co.x *= dims[0]; v.co.y *= dims[1]; v.co.z *= dims[2]
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.location = (x, y, z); ob.rotation_euler = rot
    me.materials.append(mat)
    c = ob.modifiers.new("Forme", "CAST"); c.cast_type = "CUBOID"; c.factor = 0.62; c.use_y = False
    ob.modifiers.new("Lissage", "SUBSURF").levels = 1
    for p in me.polygons: p.use_smooth = True
    return link(ob, shell)

def emitter(name, x0, x1, y0, y1, z0, z1, color, strength, shell=False):
    m = mat_emit(name + "_mat", color, strength)
    return box(name, x0, x1, y0, y1, z0, z1, m, bevel=0, shell=shell)

def light(name, kind, loc, rot=(0, 0, 0), energy=10, temp=2700, size=(0.1, 0.1), spot=None):
    ld = bpy.data.lights.new(name, kind)
    ld.energy = energy
    ld.use_temperature = True; ld.temperature = temp
    if kind == "AREA":
        ld.shape = "RECTANGLE"; ld.size, ld.size_y = size
    if kind in ("POINT", "SPOT"):
        ld.shadow_soft_size = size[0]
    if kind == "SPOT" and spot:
        ld.spot_size, ld.spot_blend = spot
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc; ob.rotation_euler = rot
    return link(ob)

# ---------------- materials ----------------
def new_mat(name):
    m = bpy.data.materials.get(name)
    if m: return m, None
    m = bpy.data.materials.new(name); m.use_nodes = True
    return m, m.node_tree

def principled(nt):
    return nt.nodes["Principled BSDF"]

def obj_coords(nt, scale=(1, 1, 1), rot=(0, 0, 0)):
    n = nt.nodes
    tc = n.new("ShaderNodeTexCoord"); info = n.new("ShaderNodeObjectInfo")
    mul = n.new("ShaderNodeVectorMath"); mul.operation = "SCALE"
    nt.links.new(info.outputs["Random"], mul.inputs["Scale"]); mul.inputs[0].default_value = (37.0, 53.0, 11.0)
    add = n.new("ShaderNodeVectorMath"); add.operation = "ADD"
    nt.links.new(tc.outputs["Object"], add.inputs[0]); nt.links.new(mul.outputs[0], add.inputs[1])
    mp = n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = scale; mp.inputs["Rotation"].default_value = rot
    nt.links.new(add.outputs[0], mp.inputs["Vector"])
    return mp.outputs["Vector"]

def ramp(nt, src, stops):
    r = nt.nodes.new("ShaderNodeValToRGB")
    els = r.color_ramp.elements
    while len(els) > 2: els.remove(els[-1])
    for i, (pos, col) in enumerate(stops):
        e = els[i] if i < 2 else els.new(pos)
        e.position = pos; e.color = (*col, 1)
    nt.links.new(src, r.inputs["Fac"])
    return r.outputs["Color"]

def srgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c)

def mat_wood(name, dark, light_, rough=0.48, vertical=True, planks=False):
    m, nt = new_mat(name)
    if not nt: return m
    p = principled(nt); n = nt.nodes
    v = obj_coords(nt, scale=(70, 70, 1.6) if vertical else (1.6, 70, 70))
    if planks:
        v = obj_coords(nt, scale=(70, 1.6, 70))  # fil le long de Y
    grain = n.new("ShaderNodeTexNoise"); grain.inputs["Scale"].default_value = 1.0
    grain.inputs["Detail"].default_value = 9; grain.inputs["Roughness"].default_value = 0.62; grain.inputs["Distortion"].default_value = 0.4
    nt.links.new(v, grain.inputs["Vector"])
    col_ = ramp(nt, grain.outputs["Fac"], [(0.32, srgb(dark)), (0.68, srgb(light_))])
    big = n.new("ShaderNodeTexNoise"); big.inputs["Scale"].default_value = 2.2; big.inputs["Detail"].default_value = 3
    nt.links.new(obj_coords(nt), big.inputs["Vector"])
    mix = n.new("ShaderNodeMix"); mix.data_type = "RGBA"; mix.blend_type = "OVERLAY"; mix.inputs["Factor"].default_value = 0.35
    nt.links.new(col_, mix.inputs["A"]); nt.links.new(big.outputs["Color"], mix.inputs["B"])
    final = mix.outputs["Result"]
    bmp = n.new("ShaderNodeBump"); bmp.inputs["Strength"].default_value = 0.08
    nt.links.new(grain.outputs["Fac"], bmp.inputs["Height"]); nt.links.new(bmp.outputs["Normal"], p.inputs["Normal"])
    nt.links.new(final, p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    return m

def mat_marble(name):
    """Marbre vert à veines blanches (d'après ta capture)."""
    m, nt = new_mat(name)
    if not nt: return m
    p = principled(nt); n = nt.nodes
    base = n.new("ShaderNodeTexNoise"); base.inputs["Scale"].default_value = 1.4
    base.inputs["Detail"].default_value = 12; base.inputs["Distortion"].default_value = 1.8
    nt.links.new(obj_coords(nt), base.inputs["Vector"])
    green = ramp(nt, base.outputs["Fac"], [(0.3, srgb("#1B271A")), (0.75, srgb("#3E5236"))])
    out = green
    for sc, dist, w, inten in ((0.9, 4.0, 0.010, 0.95), (2.2, 5.0, 0.006, 0.55), (5.0, 3.0, 0.004, 0.25)):
        vn = n.new("ShaderNodeTexNoise"); vn.inputs["Scale"].default_value = sc
        vn.inputs["Detail"].default_value = 10; vn.inputs["Distortion"].default_value = dist
        nt.links.new(obj_coords(nt, scale=(1, 1, 0.55)), vn.inputs["Vector"])
        r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
        e[0].position = 0.5 - w; e[0].color = (0, 0, 0, 1); e[1].position = 0.5; e[1].color = (1, 1, 1, 1)
        e2 = e.new(0.5 + w); e2.color = (0, 0, 0, 1)
        nt.links.new(vn.outputs["Fac"], r.inputs["Fac"])
        mx = n.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.inputs["Factor"].default_value = inten
        mm = n.new("ShaderNodeMath"); mm.operation = "MULTIPLY"; mm.inputs[1].default_value = inten
        nt.links.new(r.outputs["Color"], mm.inputs[0])
        nt.links.new(mm.outputs[0], mx.inputs["Factor"])
        nt.links.new(out, mx.inputs["A"]); mx.inputs["B"].default_value = (*srgb("#E9EDE2"), 1)
        out = mx.outputs["Result"]
    nt.links.new(out, p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = 0.2
    p.inputs["Coat Weight"].default_value = 0.08; p.inputs["Coat Roughness"].default_value = 0.2
    return m

def mat_plain(name, hexcol, rough=0.6, metal=0.0, sheen=0.0, bump=None, sss=0.0):
    m, nt = new_mat(name)
    if not nt: return m
    p = principled(nt)
    p.inputs["Base Color"].default_value = (*srgb(hexcol), 1)
    p.inputs["Roughness"].default_value = rough; p.inputs["Metallic"].default_value = metal
    p.inputs["Sheen Weight"].default_value = sheen; p.inputs["Sheen Roughness"].default_value = 0.35
    p.inputs["Subsurface Weight"].default_value = sss
    if bump:
        kind, scale, strength = bump
        n = nt.nodes
        tex = n.new("ShaderNodeTexVoronoi" if kind == "voronoi" else "ShaderNodeTexNoise")
        tex.inputs["Scale"].default_value = scale
        nt.links.new(obj_coords(nt), tex.inputs["Vector"])
        b = n.new("ShaderNodeBump"); b.inputs["Strength"].default_value = strength
        nt.links.new(tex.outputs["Distance" if kind == "voronoi" else "Fac"], b.inputs["Height"])
        nt.links.new(b.outputs["Normal"], p.inputs["Normal"])
    return m

def mat_emit(name, hexcol, strength):
    m, nt = new_mat(name)
    if not nt: return m
    p = principled(nt)
    p.inputs["Base Color"].default_value = (0, 0, 0, 1)
    p.inputs["Emission Color"].default_value = (*srgb(hexcol), 1); p.inputs["Emission Strength"].default_value = strength
    return m

M = {
    "oak": mat_wood("KAIRA_Chene", "#6E4A2A", "#AC8350", vertical=True),
    "oak_h": mat_wood("KAIRA_Chene_H", "#6E4A2A", "#AC8350", vertical=False),
    "floor": mat_wood("KAIRA_Parquet", "#8E6A42", "#C59E6A", rough=0.42, vertical=False),
    "floor_y": mat_wood("KAIRA_Parquet_Y", "#8E6A42", "#C59E6A", rough=0.42, planks=True),
    "marble": mat_marble("KAIRA_Marbre_Vert"),
    "paint": mat_plain("KAIRA_Laque_Blanc", "#EEEBE5", rough=0.5),
    "plaster": mat_plain("KAIRA_Plafond", "#F1EEE8", rough=0.9),
    "shadow": mat_plain("KAIRA_Ombre", "#0E0B09", rough=1.0),
    "boucle": mat_plain("KAIRA_Boucle_Sable", "#D2C3AD", rough=0.95, sheen=0.6, bump=("voronoi", 420, 0.35)),
    "linen": mat_plain("KAIRA_Lin_Ivoire", "#EDE6DA", rough=0.9, sheen=0.4, bump=("noise", 260, 0.12)),
    "linen_mocha": mat_plain("KAIRA_Lin_Moka", "#6B5240", rough=0.9, sheen=0.4, bump=("noise", 220, 0.15)),
    "velvet": mat_plain("KAIRA_Velours_Foret", "#2F3E2C", rough=0.75, sheen=1.0),
    "bronze": mat_plain("KAIRA_Bronze", "#8C6A43", rough=0.3, metal=1.0),
    "rug": mat_plain("KAIRA_Tapis_Laine", "#C9BBA5", rough=1.0, sheen=0.3, bump=("noise", 140, 0.5)),
    "alabaster": mat_emit("KAIRA_Albatre", "#FFB872", 3.5),
    "ceramic": mat_plain("KAIRA_Ceramique", "#B5A894", rough=0.65),
    "ceramic_w": mat_plain("KAIRA_Ceramique_Blanc", "#E9E2D6", rough=0.45),
    "book1": mat_plain("KAIRA_Livre_1", "#C9B79C", rough=0.7),
    "book2": mat_plain("KAIRA_Livre_2", "#3B4A3A", rough=0.7),
}
WARM = "#FFC98E"

# =========================================================
# 1. EXISTANT (reconstruit d'après la capture — ignoré dans ton fichier)
# =========================================================
X0, X1 = -ROOM_W / 2, ROOM_W / 2
if BUILD_SHELL:
    S = dict(shell=True)
    box("Sol_support", X0 - 0.1, X1 + 0.1, -0.1, ROOM_D + 0.6, -0.03, -0.002, M["shadow"], bevel=0, **S)
    pw = 0.19; x = X0
    while x < X1:
        y = -random.uniform(0, 1.2)
        while y < ROOM_D + 0.5:
            L = random.uniform(1.4, 2.2)
            box("Lame_parquet", x + 0.0012, min(x + pw, X1) - 0.0012, max(y, 0) + 0.0012, min(y + L, ROOM_D + 0.5) - 0.0012, -0.014, 0.0, M["floor_y"], bevel=0.0012, seg=1, **S)
            y += L
        x += pw
    box("Mur_tete", X0, X1, -0.12, 0, 0, CEIL_H, M["paint"], bevel=0, **S)
    box("Mur_gauche", X0 - 0.12, X0, 0, ROOM_D + 0.5, 0, CEIL_H, M["paint"], bevel=0, **S)
    box("Mur_droit", X1, X1 + 0.12, 0, ROOM_D + 0.5, 0, CEIL_H, M["paint"], bevel=0, **S)
    box("Mur_entree", X0, X1, ROOM_D + 0.5, ROOM_D + 0.62, 0, CEIL_H, M["paint"], bevel=0, **S)
    # habillage blanc à joints (mur de tête)
    for (a, b) in ((X0, -MARBLE_W / 2 - 0.04), (MARBLE_W / 2 + 0.04, X1)):
        xs = [a + (b - a) * i / 3 for i in range(4)]
        for i in range(3):
            for (z0, z1) in ((0.0, 1.86), (1.86, CEIL_H)):
                box("Panneau_blanc", xs[i] + 0.002, xs[i + 1] - 0.002, 0, 0.025, z0 + 0.002, z1 - 0.002, M["paint"], bevel=0.0015, **S)
    # marbre vert + LED latérales
    box("Marbre_vert", -MARBLE_W / 2, MARBLE_W / 2, 0.0, 0.05, 0, CEIL_H, M["marble"], bevel=0.001, **S)
    for sx in (-1, 1):
        x = sx * (MARBLE_W / 2 + 0.02)
        emitter("LED_marbre", x - 0.006, x + 0.006, 0.006, 0.02, 0.02, CEIL_H - 0.02, WARM, 60, **S)
    # colonnes chêne : haut lisse, bas cannelé, LED à la jonction
    for sx in (-1, 1):
        cx = sx * COL_X
        box("Colonne_chene_haut", cx - COL_W / 2, cx + COL_W / 2, 0.025, 0.085, 1.66, 2.76, M["oak"], **S)
        box("Colonne_fond", cx - COL_W / 2, cx + COL_W / 2, 0.025, 0.05, 0, 1.66, M["oak"], bevel=0, **S)
        me = bpy.data.meshes.new("Cannelure")
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, segments=12, radius1=0.011, radius2=0.011, depth=1.64, cap_ends=True)
        bm.to_mesh(me); bm.free()
        fl = bpy.data.objects.new("Cannelures", me); me.materials.append(M["oak"])
        for p in me.polygons: p.use_smooth = True
        n = int((COL_W - 0.01) / 0.026)
        fl.location = (cx - COL_W / 2 + 0.016, 0.06, 0.82)
        ar = fl.modifiers.new("Array", "ARRAY"); ar.count = n; ar.use_relative_offset = False
        ar.use_constant_offset = True; ar.constant_offset_displace = (0.026, 0, 0)
        link(fl, shell=True)
        emitter("LED_colonne", cx - COL_W / 2 + 0.02, cx + COL_W / 2 - 0.02, 0.06, 0.075, 1.652, 1.658, WARM, 40, **S)
        light("LED_colonne_L", "AREA", (cx, 0.068, 1.65), (0, 0, 0), energy=4, temp=2700, size=(COL_W - 0.04, 0.012))
        # chevet chêne deux tiroirs (existant)
        x0, x1 = cx - 0.30, cx + 0.30
        box("Chevet_caisson", x0, x1, 0.09, 0.53, 0.0, 0.50, M["oak_h"], **S)
        box("Chevet_tiroir_1", x0 + 0.004, x1 - 0.004, 0.53, 0.55, 0.26, 0.496, M["oak_h"], **S)
        box("Chevet_tiroir_2", x0 + 0.004, x1 - 0.004, 0.53, 0.55, 0.004, 0.252, M["oak_h"], **S)
    # placards blancs à gauche, panneaux moulurés à droite
    for i in range(6):
        y0 = 0.9 + i * 0.6
        box("Porte_placard", X1 - 0.022, X1, y0 + 0.002, y0 + 0.598, 0.0, DROP_H - 0.003, M["paint"], **S)
    for i in range(3):
        y0 = 1.0 + i * 1.25
        for (z0, z1) in ((0.12, 1.0), (1.12, DROP_H - 0.15)):
            for (a, b, c, d) in ((y0, y0 + 1.1, z0, z0 + 0.02), (y0, y0 + 1.1, z1 - 0.02, z1), (y0, y0 + 0.02, z0, z1), (y0 + 1.08, y0 + 1.1, z0, z1)):
                box("Moulure", X0, X0 + 0.018, a, b, c, d, M["paint"], bevel=0.004, **S)

# =========================================================
# 2. AMÉNAGEMENT KAÏRA
# =========================================================
# --- tête de lit : capitonnage en canaux verticaux, bouclé sable, chapeau bronze
HB_Y0 = 0.055
n_ch = 10; chw = HB_W / n_ch
for i in range(n_ch):
    a = -HB_W / 2 + i * chw
    box("TeteDeLit_canal", a + 0.003, a + chw - 0.003, HB_Y0, HB_Y0 + 0.095, 0.20, HB_H, M["boucle"], bevel=0.035, seg=5)
box("TeteDeLit_fond", -HB_W / 2, HB_W / 2, HB_Y0, HB_Y0 + 0.06, 0.20, HB_H, M["shadow"], bevel=0)
box("TeteDeLit_chapeau_bronze", -HB_W / 2 - 0.004, HB_W / 2 + 0.004, HB_Y0, HB_Y0 + 0.1, HB_H, HB_H + 0.008, M["bronze"], bevel=0.001)

# --- lit plateforme en lévitation
BY0 = HB_Y0 + 0.1
box("Lit_socle_retrait", -BED_W / 2 + 0.12, BED_W / 2 - 0.12, BY0 + 0.12, BY0 + BED_L - 0.12, 0, 0.09, M["shadow"], bevel=0)
emitter("Lit_LED_plinthe", -BED_W / 2 + 0.13, BED_W / 2 - 0.13, BY0 + BED_L - 0.135, BY0 + BED_L - 0.125, 0.086, 0.09, WARM, 25)
for sx in (-1, 1):
    emitter("Lit_LED_plinthe_cote", sx * (BED_W / 2 - 0.13) - 0.005, sx * (BED_W / 2 - 0.13) + 0.005, BY0 + 0.14, BY0 + BED_L - 0.14, 0.086, 0.09, WARM, 25)
box("Lit_cadre_bouclé", -BED_W / 2, BED_W / 2, BY0, BY0 + BED_L, 0.09, 0.34, M["boucle"], bevel=0.035, seg=5)
box("Matelas", -0.9, 0.9, BY0 + 0.05, BY0 + 2.05, 0.34, 0.55, M["linen"], bevel=0.05, seg=5)
# couette : plateau + retombées sur les côtés et au pied
duvet = soft("Couette_lin_ivoire", 0, BY0 + 1.33, 0.585, (2.02, 1.68, 0.07), M["linen"], round_=0.4)
d = duvet.modifiers.new("Plis", "DISPLACE"); t = bpy.data.textures.new("plis", "CLOUDS"); t.noise_scale = 0.3; d.texture = t; d.strength = 0.01; d.mid_level = 0.5
for sx in (-1, 1):
    soft("Couette_retombee", sx * 1.0, BY0 + 1.33, 0.47, (0.045, 1.68, 0.25), M["linen"], round_=0.4)
soft("Couette_retombee_pied", 0, BY0 + 2.17, 0.47, (2.04, 0.045, 0.25), M["linen"], round_=0.4)
soft("Couette_retour", 0, BY0 + 0.56, 0.625, (2.0, 0.26, 0.07), M["linen"], round_=0.45)
# plaid moka posé en travers
soft("Plaid_moka", 0, BY0 + 1.80, 0.625, (2.08, 0.48, 0.016), M["linen_mocha"], round_=0.45)
for sx in (-1, 1):
    soft("Plaid_moka_retombee", sx * 1.03, BY0 + 1.80, 0.50, (0.018, 0.48, 0.24), M["linen_mocha"], round_=0.45)
# coussins (appuyés sur la tête de lit)
for sx in (-1, 1):
    pillow("Oreiller_euro", sx * 0.46, BY0 + 0.13, 0.87, (0.66, 0.20, 0.64), M["linen"], rot=(math.radians(12), 0, 0))
    pillow("Oreiller", sx * 0.44, BY0 + 0.31, 0.73, (0.64, 0.17, 0.44), M["linen"], rot=(math.radians(28), 0, 0))
pillow("Coussin_velours_foret", -0.05, BY0 + 0.45, 0.69, (0.58, 0.15, 0.32), M["velvet"], rot=(math.radians(32), 0, 0))
pillow("Coussin_moka", 0.33, BY0 + 0.51, 0.67, (0.42, 0.14, 0.28), M["linen_mocha"], rot=(math.radians(34), 0, math.radians(-10)))

# --- banc de pied de lit (chêne + bouclé)
FY = BY0 + BED_L + 0.18
box("Banc_assise_bouclé", -0.72, 0.72, FY, FY + 0.42, 0.36, 0.45, M["boucle"], bevel=0.03, seg=4)
box("Banc_plateau_chene", -0.74, 0.74, FY - 0.01, FY + 0.43, 0.32, 0.36, M["oak_h"])
for sx in (-1, 1):
    box("Banc_pied", sx * 0.66 - 0.04, sx * 0.66 + 0.04, FY + 0.02, FY + 0.40, 0.0, 0.32, M["oak"])

# --- tapis laine
box("Tapis_laine", -1.55, 1.55, 0.95, 4.55, 0.0, 0.012, M["rug"], bevel=0.004)

# --- suspensions albâtre & bronze au-dessus des chevets
for sx in (-1, 1):
    x = sx * COL_X; y = 0.34
    me = bpy.data.meshes.new("Suspension"); bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=48, radius1=0.085, radius2=0.085, depth=0.30, cap_ends=True); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    sh = bpy.data.objects.new("Suspension_albatre", me); sh.location = (x, y, 1.18 + 0.15); me.materials.append(M["alabaster"]); link(sh)
    me = bpy.data.meshes.new("Cape"); bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=48, radius1=0.092, radius2=0.092, depth=0.02, cap_ends=True); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    cp = bpy.data.objects.new("Suspension_cape_bronze", me); cp.location = (x, y, 1.49); me.materials.append(M["bronze"]); link(cp)
    box("Suspension_cable", x - 0.002, x + 0.002, y - 0.002, y + 0.002, 1.50, DROP_H, M["bronze"], bevel=0)
    light("Suspension_lumiere", "POINT", (x, y, 1.15), energy=12, temp=2400, size=(0.05, 0.05))
    # styling sur chevets
    box("Livre", x - 0.16, x + 0.08, 0.20, 0.42, 0.50, 0.525, M["book1"])
    box("Livre", x - 0.15, x + 0.07, 0.21, 0.41, 0.525, 0.545, M["book2"])
    me = bpy.data.meshes.new("Vase"); bm = bmesh.new()
    bmesh.ops.create_cone(bm, segments=40, radius1=0.06, radius2=0.04, depth=0.22, cap_ends=True); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    va = bpy.data.objects.new("Vase_ceramique", me); va.location = (x + 0.18, 0.30, 0.61); me.materials.append(M["ceramic"] if sx < 0 else M["ceramic_w"]); link(va)

# --- plafond architectural
# Faux-plafond périphérique à 2,62 m, caisson central rehaussé (dalle à 2,85 m) au-dessus du lit,
# gorge lumineuse sur tout le pourtour du caisson, fente de 18 cm le long du mur de tête
# (le marbre et les colonnes montent jusqu'à la dalle, éclairés par un lécheur linéaire).
CX0, CX1, CY0, CY1 = -1.45, 1.45, 0.75, 3.95
SLOT = 0.18
box("Dalle", X0, X1, 0, ROOM_D + 0.5, CEIL_H, CEIL_H + 0.05, M["plaster"], bevel=0)
def drop(name, x0, x1, y0, y1):
    box(name, x0, x1, y0, y1, DROP_H, CEIL_H, M["plaster"], bevel=0.002)
drop("FauxPlafond_arriere", X0, X1, SLOT, CY0 - 0.10)
drop("FauxPlafond_avant", X0, X1, CY1 + 0.10, ROOM_D + 0.5)
drop("FauxPlafond_gauche", X0, CX0 - 0.10, CY0 - 0.10, CY1 + 0.10)
drop("FauxPlafond_droit", CX1 + 0.10, X1, CY0 - 0.10, CY1 + 0.10)
# lèvre de la gorge (débord de 10 cm) + LED vers le haut
for (nm, x0, x1, y0, y1) in (("Gorge_arriere", CX0 - 0.10, CX1 + 0.10, CY0 - 0.10, CY0),
                             ("Gorge_avant", CX0 - 0.10, CX1 + 0.10, CY1, CY1 + 0.10),
                             ("Gorge_gauche", CX0 - 0.10, CX0, CY0, CY1),
                             ("Gorge_droite", CX1, CX1 + 0.10, CY0, CY1)):
    box(nm, x0, x1, y0, y1, DROP_H, DROP_H + 0.035, M["plaster"], bevel=0.002)
for (x, y, sx_, sy_, rz) in ((0, CY0 - 0.05, CX1 - CX0, 0.02, 0), (0, CY1 + 0.05, CX1 - CX0, 0.02, 0),
                             (CX0 - 0.05, (CY0 + CY1) / 2, 0.02, CY1 - CY0, 0), (CX1 + 0.05, (CY0 + CY1) / 2, 0.02, CY1 - CY0, 0)):
    light("Gorge_LED", "AREA", (x, y, DROP_H + 0.04), (math.pi, 0, 0) if False else (0, 0, 0), energy=0, temp=2700, size=(sx_, sy_))
gorge_lights = [o for o in col.objects if o.name.startswith("Gorge_LED")]
for o in gorge_lights:
    o.rotation_euler = (math.pi, 0, 0)  # AREA éclaire vers -Z localement : retournée vers le haut
# lécheur linéaire dans la fente (marbre + colonnes)
light("Lecheur_mur_tete", "AREA", (0, 0.10, CEIL_H - 0.01), (0, 0, 0), energy=0, temp=3000, size=(ROOM_W - 0.1, 0.03))
# encastrés basse luminance devant les placards
spots = []
for y in (1.5, 2.7, 3.9):
    spots.append(light("Encastre_placard", "SPOT", (X1 - 0.45, y, DROP_H - 0.002), (0, 0, 0), energy=0, temp=3000, size=(0.02, 0.02), spot=(math.radians(50), 0.6)))
    box("Encastre_anneau", X1 - 0.48, X1 - 0.42, y - 0.03, y + 0.03, DROP_H - 0.002, DROP_H, M["shadow"], bevel=0)

# =========================================================
# 3. SCÈNES D'ÉCLAIRAGE
# =========================================================
def scene_preset(name):
    P = {
        "ambiance": dict(gorge=40, lecheur=55, spots=0, pend=10, world=0.004, fill=0, exposure=-0.9, wb=3050),
        "jour":     dict(gorge=18, lecheur=30, spots=0, pend=5,  world=0.02, fill=520, exposure=-1.0, wb=4600),
        "lecture":  dict(gorge=28, lecheur=40, spots=0, pend=12, world=0.004, fill=0, exposure=-0.8, wb=3050),
    }[name]
    for o in gorge_lights: o.data.energy = P["gorge"]
    bpy.data.objects["Lecheur_mur_tete"].data.energy = P["lecheur"]
    for s in spots: s.data.energy = P["spots"]
    for o in col.objects:
        if o.name.startswith("Suspension_lumiere"): o.data.energy = P["pend"]
    if BUILD_SHELL:
        w = scene.world or bpy.data.worlds.new("W"); scene.world = w; w.use_nodes = True
        w.node_tree.nodes["Background"].inputs[0].default_value = (0.9, 0.85, 0.8, 1)
        w.node_tree.nodes["Background"].inputs[1].default_value = P["world"]
        f = bpy.data.objects.get("Fenetre_jour")
        if f is None:
            ld = bpy.data.lights.new("Fenetre_jour", "AREA"); ld.shape = "RECTANGLE"; ld.size, ld.size_y = 3.2, 2.2
            ld.use_temperature = True; ld.temperature = 5600
            f = bpy.data.objects.new("Fenetre_jour", ld); f.location = (0.3, ROOM_D + 0.45, 1.5); f.rotation_euler = (math.radians(-90), 0, 0)
            link(f)
        f.data.energy = P["fill"]
    scene.view_settings.exposure = P["exposure"]
    scene.view_settings.use_white_balance = True
    scene.view_settings.white_balance_temperature = P["wb"]

for o in gorge_lights: o.data.energy = 55
bpy.data.objects["Lecheur_mur_tete"].data.energy = 70

# =========================================================
# 4. RENDU (ligne de commande)
# =========================================================
if RENDER_DIR:
    os.makedirs(RENDER_DIR, exist_ok=True)
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = SAMPLES
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 8
    scene.render.resolution_x, scene.render.resolution_y = 1800, 1200
    scene.render.image_settings.file_format = "JPEG"; scene.render.image_settings.quality = 92
    scene.view_settings.view_transform = "AgX"
    cams = {
        # vue d'ensemble, même axe que ta capture
        "v1": dict(loc=(0.15, ROOM_D - 0.15, 1.35), tgt=(0.0, 0.0, 1.35), lens=22, shift=-0.07, preset="ambiance"),
        # trois-quarts en journée
        "v2": dict(loc=(1.85, 4.35, 1.40), tgt=(-0.55, 0.3, 1.40), lens=30, shift=-0.08, preset="jour"),
        # détail chevet, cannelures, suspension et canaux de la tête de lit
        "v3": dict(loc=(-0.25, 2.05, 1.05), tgt=(-1.30, 0.25, 1.05), lens=45, shift=-0.05, preset="lecture"),
    }
    for vid in VIEWS:
        c = cams[vid]
        camd = bpy.data.cameras.new(vid); camd.lens = c["lens"]; camd.sensor_width = 36; camd.shift_y = c["shift"]
        camd.clip_start = 0.05
        cam = bpy.data.objects.new("Cam_" + vid, camd); scene.collection.objects.link(cam)
        cam.location = c["loc"]
        d = Vector(c["tgt"]) - Vector(c["loc"]); d.z = 0  # caméra horizontale = verticales droites
        cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
        scene.camera = cam
        scene_preset(c["preset"])
        scene.render.filepath = os.path.join(RENDER_DIR, vid + ".jpg")
        bpy.ops.render.render(write_still=True)
        print("RENDERED", vid, flush=True)
