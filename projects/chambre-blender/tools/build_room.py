"""Reconstitution de l'architecture existante (d'après la capture Blender du client) pour tester
kaira_chambre.py et produire un rendu Cycles. Dans le vrai projet, c'est le .blend du client
qui fournit cette architecture : ce fichier ne sert qu'à la prévisualisation.
Repère identique au script : curseur au sol au milieu du marbre, chambre vers -Y."""
import math, bpy

RW, RD, CEIL, DROP = 3.90, 4.60, 2.80, 2.60
def W(x, d, z): return (-x, -d, z)          # local (largeur, profondeur, hauteur) -> monde (INTO_ROOM = -Y)

def node_mat(name, build):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; b = nt.nodes["Principled BSDF"]; build(nt, b); return m

def simple(name, rgb, rough=0.5, metal=0.0, coat=0.0):
    def f(nt, b):
        b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
        b.inputs["Metallic"].default_value = metal; b.inputs["Coat Weight"].default_value = coat
    return node_mat(name, f)

def verde(nt, b):                     # marbre vert type Verde Guatemala : réseau de veines blanches
    n = nt.nodes; L = nt.links
    tc = n.new("ShaderNodeTexCoord"); nz = n.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 2.5; nz.inputs["Detail"].default_value = 8
    mix = n.new("ShaderNodeMix"); mix.data_type = "VECTOR"; mix.inputs["Factor"].default_value = 0.5
    L.new(tc.outputs["Object"], mix.inputs[4]); L.new(nz.outputs["Color"], mix.inputs[5])
    vo = n.new("ShaderNodeTexVoronoi"); vo.feature = "DISTANCE_TO_EDGE"; vo.inputs["Scale"].default_value = 4.5
    L.new(mix.outputs[1], vo.inputs["Vector"])
    vr = n.new("ShaderNodeValToRGB"); vr.color_ramp.elements[0].position = 0.0; vr.color_ramp.elements[0].color = (0.85, 0.88, 0.80, 1)
    vr.color_ramp.elements[1].position = 0.012; vr.color_ramp.elements[1].color = (0, 0, 0, 1)
    L.new(vo.outputs["Distance"], vr.inputs["Fac"])
    nz2 = n.new("ShaderNodeTexNoise"); nz2.inputs["Scale"].default_value = 4; nz2.inputs["Detail"].default_value = 10
    gr = n.new("ShaderNodeValToRGB"); gr.color_ramp.elements[0].color = (0.010, 0.020, 0.010, 1); gr.color_ramp.elements[1].color = (0.06, 0.085, 0.045, 1)
    L.new(nz2.outputs["Fac"], gr.inputs["Fac"])
    add = n.new("ShaderNodeMix"); add.data_type = "RGBA"; add.blend_type = "SCREEN"; add.inputs["Factor"].default_value = 1
    L.new(gr.outputs["Color"], add.inputs[6]); L.new(vr.outputs["Color"], add.inputs[7]); L.new(add.outputs[2], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.12; b.inputs["Coat Weight"].default_value = 0.4

def oak(scale_planks):
    def f(nt, b):
        n = nt.nodes; L = nt.links
        tc = n.new("ShaderNodeTexCoord"); mp = n.new("ShaderNodeMapping")
        if scale_planks: mp.inputs["Rotation"].default_value = (0, 0, 1.5708)
        L.new(tc.outputs["Object"], mp.inputs["Vector"])
        wv = n.new("ShaderNodeTexWave"); wv.wave_type = "BANDS"; wv.bands_direction = "Y" if scale_planks else "X"; wv.inputs["Scale"].default_value = 9
        wv.inputs["Distortion"].default_value = 2.5; wv.inputs["Detail"].default_value = 4; L.new(mp.outputs["Vector"], wv.inputs["Vector"])
        cr = n.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.33, 0.16, 0.07, 1); cr.color_ramp.elements[1].color = (0.46, 0.24, 0.11, 1)
        L.new(wv.outputs["Fac"], cr.inputs["Fac"]); out = cr.outputs["Color"]
        if scale_planks:
            br = n.new("ShaderNodeTexBrick"); br.inputs["Scale"].default_value = 1.0; br.inputs["Brick Width"].default_value = 1.8
            br.inputs["Row Height"].default_value = 0.18; br.inputs["Mortar Size"].default_value = 0.002
            br.inputs["Color1"].default_value = (1, 1, 1, 1); br.inputs["Color2"].default_value = (0.82, 0.8, 0.78, 1); br.inputs["Mortar"].default_value = (0.3, 0.3, 0.3, 1)
            L.new(mp.outputs["Vector"], br.inputs["Vector"])
            mul = n.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"; mul.inputs["Factor"].default_value = 1
            L.new(out, mul.inputs[6]); L.new(br.outputs["Color"], mul.inputs[7]); out = mul.outputs[2]
        L.new(out, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.4
    return f

M = {"white": simple("Archi_Blanc", (0.80, 0.79, 0.76), 0.55), "gap": simple("Archi_Joint", (0.02, 0.02, 0.02), 1),
     "verde": node_mat("Archi_Marbre_Vert", verde), "floor": node_mat("Archi_Parquet_Chene", oak(True)),
     "oak": node_mat("bois maron", oak(False))}
led = bpy.data.materials.new("Archi_LED"); led.use_nodes = True
pb = led.node_tree.nodes["Principled BSDF"]; pb.inputs["Emission Color"].default_value = (1, 0.62, 0.32, 1); pb.inputs["Emission Strength"].default_value = 30
M["led"] = led

def box(name, x0, x1, d0, d1, z0, z1, m):
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.active_object; o.name = name
    o.location = W((x0 + x1) / 2, (d0 + d1) / 2, (z0 + z1) / 2); o.scale = (abs(x1 - x0), abs(d1 - d0), abs(z1 - z0))
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True); o.data.materials.append(m); return o

xL, xR = -RW / 2, RW / 2
box("Sol", xL, xR, 0, RD, -0.02, 0, M["floor"])
box("Plafond", xL - 0.2, xR + 0.2, -0.2, RD + 0.2, CEIL, CEIL + 0.1, M["white"])
box("Mur_Fond", xL - 0.2, xR + 0.2, -0.2, 0, 0, CEIL, M["white"])
box("Mur_G", xL - 0.2, xL, 0, RD, 0, CEIL, M["white"]); box("Mur_D", xR, xR + 0.2, 0, RD, 0, CEIL, M["white"])
box("Mur_Face", xL - 0.2, xR + 0.2, RD, RD + 0.2, 0, CEIL, M["white"])
for x in (-1.25, 1.25): box("Joint_V", x - 0.004, x + 0.004, -0.001, 0.002, 0, DROP, M["gap"])
box("Joint_H_G", xL, -0.62, -0.001, 0.002, 1.30, 1.306, M["gap"]); box("Joint_H_D", 0.62, xR, -0.001, 0.002, 1.30, 1.306, M["gap"])
box("Marbre_Vert", -0.60, 0.60, 0.0, 0.04, 0, CEIL, M["verde"])
for x in (-0.606, 0.606): box("LED_Marbre", x - 0.003, x + 0.003, 0.0, 0.01, 0, CEIL, M["led"])
for cx in (-1.72, 1.72):
    box("Colonne_Haut", cx - 0.15, cx + 0.15, 0, 0.14, 1.30, DROP, M["oak"])
    box("Colonne_Bas", cx - 0.15, cx + 0.15, 0, 0.10, 0, 1.28, M["oak"])
    x = cx - 0.14
    while x < cx + 0.14:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.011, depth=1.28, vertices=12, location=W(x + 0.011, 0.105, 0.64))
        c = bpy.context.active_object; c.data.materials.append(M["oak"]); bpy.ops.object.shade_smooth(); x += 0.025
    box("LED_Colonne", cx - 0.14, cx + 0.14, 0.10, 0.135, 1.286, 1.294, M["led"])
    ld = bpy.data.lights.new("Spot_Colonne", "SPOT"); ld.energy = 25; ld.color = (1, 0.72, 0.45); ld.spot_size = math.radians(70); ld.shadow_soft_size = 0.02
    lo = bpy.data.objects.new("Spot_Colonne", ld); bpy.context.scene.collection.objects.link(lo); lo.location = W(cx, 0.13, 1.27)
for cx in (-1.25, 1.25):
    box("Chevet", cx - 0.30, cx + 0.30, 0.02, 0.47, 0.02, 0.48, M["oak"]); box("Chevet_Joint", cx - 0.30, cx + 0.30, 0.468, 0.473, 0.245, 0.252, M["gap"])
    box("Chevet_Socle", cx - 0.29, cx + 0.29, 0.04, 0.45, 0, 0.02, M["gap"])
z = 0.6
while z < RD - 0.5:
    box("Facade_D", xR - 0.03, xR, z, z + 1.0, 0.05, 2.35, M["white"]); box("Facade_D_Joint", xR - 0.032, xR - 0.03, z + 1.0, z + 1.05, 0.05, 2.35, M["gap"]); z += 1.05
box("Porte_G_Joint", xL, xL + 0.004, 0.4, 0.404, 0, 2.3, M["gap"]); box("Porte_G_Joint2", xL, xL + 0.004, 1.3, 1.304, 0, 2.3, M["gap"])
# monde : nuit douce + lumière de jour discrète par le mur droit (baie hors champ)
w = bpy.data.worlds.new("Monde"); w.use_nodes = True; w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.018, 0.015, 1)
bpy.context.scene.world = w
