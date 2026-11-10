"""KAÏRA — Audit d'une scène Blender avant rendu vidéo.
Usage : blender -b fichier.blend --python kaira_audit.py -- rapport.json
Relève : scènes, moteur et réglages de rendu, caméras, lumières, matériaux (textures manquantes,
émission), géométrie lourde, modificateurs, gestion des couleurs, fichiers externes."""
import bpy, json, os, sys

out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else None
R = {"blender": bpy.app.version_string, "fichier": bpy.data.filepath, "scenes": [], "alertes": []}
warn = R["alertes"].append

for sc in bpy.data.scenes:
    r, cy = sc.render, getattr(sc, "cycles", None)
    d = {"nom": sc.name, "moteur": r.engine, "resolution": [r.resolution_x, r.resolution_y, r.resolution_percentage],
         "fps": r.fps / r.fps_base, "images": [sc.frame_start, sc.frame_end], "camera": sc.camera.name if sc.camera else None,
         "flou_mouvement": r.use_motion_blur, "transform_vue": sc.view_settings.view_transform, "look": sc.view_settings.look,
         "exposition": sc.view_settings.exposure, "monde": sc.world.name if sc.world else None}
    if cy and r.engine == "CYCLES":
        d.update(echantillons=cy.samples, adaptatif=cy.use_adaptive_sampling, seuil_bruit=cy.adaptive_threshold,
                 debruitage=cy.use_denoising, debruiteur=getattr(cy, "denoiser", None), device=cy.device,
                 rebonds=[cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces, cy.transmission_bounces, cy.transparent_max_bounces],
                 caustiques=[cy.caustics_reflective, cy.caustics_refractive], clamp=[cy.sample_clamp_direct, cy.sample_clamp_indirect],
                 donnees_persistantes=r.use_persistent_data)
    if hasattr(sc, "eevee"):
        ev = sc.eevee
        d["eevee"] = {k: getattr(ev, k) for k in ("taa_render_samples", "use_raytracing", "use_shadows") if hasattr(ev, k)}
    R["scenes"].append(d)

cams = [o for o in bpy.data.objects if o.type == "CAMERA"]
R["cameras"] = [{"nom": o.name, "focale": round(o.data.lens, 1), "position": [round(v, 2) for v in o.matrix_world.translation],
                 "rotation_deg": [round(v * 57.2958, 1) for v in o.matrix_world.to_euler()], "dof": o.data.dof.use_dof,
                 "anime": bool(o.animation_data and o.animation_data.action)} for o in cams]
lights = [o for o in bpy.data.objects if o.type == "LIGHT"]
R["lumieres"] = [{"nom": o.name, "type": o.data.type, "puissance": round(o.data.energy, 1), "couleur": [round(c, 2) for c in o.data.color],
                  "rendu": not o.hide_render} for o in lights]

mats = []
for m in bpy.data.materials:
    if not m.users:
        continue
    info = {"nom": m.name, "utilisateurs": m.users, "textures": [], "emission": 0.0, "transmission": 0.0}
    if m.use_nodes and m.node_tree:
        for n in m.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image:
                im = n.image
                path = bpy.path.abspath(im.filepath) if im.filepath else ""
                ok = bool(im.packed_file) or (path and os.path.exists(path))
                info["textures"].append({"image": im.name, "taille": list(im.size), "trouvee": ok})
                if not ok:
                    warn(f"Texture manquante : {im.name} ({im.filepath}) dans le matériau {m.name}")
                if max(im.size) > 8192:
                    warn(f"Texture très lourde : {im.name} {tuple(im.size)}")
            if n.type == "BSDF_PRINCIPLED":
                es = n.inputs.get("Emission Strength")
                tw = n.inputs.get("Transmission Weight") or n.inputs.get("Transmission")
                if es and not es.is_linked:
                    info["emission"] = max(info["emission"], es.default_value)
                if tw and not tw.is_linked:
                    info["transmission"] = max(info["transmission"], tw.default_value)
            if n.type == "EMISSION":
                s = n.inputs.get("Strength")
                if s and not s.is_linked:
                    info["emission"] = max(info["emission"], s.default_value)
    mats.append(info)
R["materiaux"] = mats

geo = []
dg = bpy.context.evaluated_depsgraph_get()
for o in bpy.data.objects:
    if o.type != "MESH" or o.hide_render:
        continue
    mods = [(m.type, getattr(m, "render_levels", None)) for m in o.modifiers]
    for t, lv in mods:
        if t == "SUBSURF" and lv and lv > 2:
            warn(f"Subdivision rendu niveau {lv} sur {o.name} (2 suffit généralement)")
    try:
        n = len(o.evaluated_get(dg).data.polygons)
    except Exception:
        n = len(o.data.polygons)
    geo.append((n, o.name, mods))
geo.sort(reverse=True)
R["geometrie"] = {"objets": len(geo), "polygones_total": sum(g[0] for g in geo),
                  "plus_lourds": [{"objet": g[1], "polygones": g[0], "modificateurs": g[2]} for g in geo[:15]]}
missing = [i.filepath for i in bpy.data.images if i.filepath and not i.packed_file and not os.path.exists(bpy.path.abspath(i.filepath))]
R["fichiers_manquants"] = sorted(set(missing))
txt = json.dumps(R, ensure_ascii=False, indent=1, default=str)
if out:
    open(out, "w").write(txt)
print(txt[:4000])
