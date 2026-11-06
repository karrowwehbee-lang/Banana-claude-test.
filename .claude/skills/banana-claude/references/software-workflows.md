# Software & architectural workflows

Give step-by-step instructions with menu paths or shortcuts when you are confident
of them. Software menus change between versions: if unsure, describe the tool's
function and tell the user to check it for their version.

## General project setup (all tools)

- Units: metric, millimetres (or the client's standard). Set this before modelling.
- Use one clear naming convention, e.g. `KAIRA_[Project]_[Room]_[Element]_[v01]`.
- Model to real dimensions only; never scale furniture by eye.
- Keep a project material library with consistent names that match the
  specification (e.g. `STN_CalacattaViola_Honed`, `WD_SmokedOak_Matte`).
- Back up and version files (v01, v02…); keep a change log for client revisions.

## Revit (BIM, documentation)

- Start from a template with KAÏRA title blocks, line styles, text styles, view
  templates and dimension styles.
- Model walls, floors and ceilings with correct layered assemblies (structure,
  insulation, finish) so sections are accurate.
- Use **families** for furniture, joinery and lighting; set type parameters for
  W/D/H and material so schedules update automatically.
- Create views: plans (furniture, ceiling/RCP, lighting, electrical, finishes),
  elevations per wall, sections, 3D views and detail callouts.
- Use **schedules** for furniture (FF&E), doors, lighting, finishes and quantities.
- Use phases (Existing / New construction) for renovation projects.
- Export: PDF sheet sets for the client; DWG for consultants; IFC for BIM
  coordination; FBX or a live-link plugin to Enscape/D5/Twinmotion for rendering.

## SketchUp (fast concept and design development)

- Model with **groups and components**; never leave loose geometry. Make repeated
  items components so edits update everywhere.
- Organize with **tags** (e.g. Walls, Joinery, Furniture, Lighting, Decor) and the
  Outliner; use scenes for saved views.
- Draw walls from accurate survey dimensions; use the Tape Measure and guides.
- Use LayOut for presentation drawings with dimensions and title blocks.
- Render with V-Ray, Enscape or D5 (live link); assign PBR materials with correct
  real-world texture sizes (e.g. a 600 × 1200 tile texture mapped at 600 × 1200).
- Keep the model light: purge unused components and materials, use proxies for
  heavy assets such as plants.

## Blender (high-end visualization)

- Scene units: Metric, unit scale 1.0, length in millimetres or metres.
- Import from SketchUp/Revit via FBX, OBJ or glTF; check scale and apply transforms
  (Ctrl+A → All Transforms).
- Use **Cycles** for final photoreal renders; Eevee for quick previews.
- Color management: AgX (or Filmic in older versions) for natural highlights.
- Lighting: HDRI environment for daylight, Sun lamp for direct light, area lights
  in windows (portals) to reduce noise, IES profiles for artificial fixtures.
- Materials: Principled BSDF with full PBR maps (base color, roughness, normal,
  displacement); add subtle roughness variation and bevels (Bevel modifier or
  shader bevel) — sharp 90° edges look CGI.
- Camera: 24–35 mm, height 1.2–1.4 m; use **shift X/Y** instead of tilting to keep
  verticals straight.
- Render: denoising on, enough samples for clean shadows (start ~512–1024 and adjust),
  render passes for post-production.

## Handover between tools

| From → To | Format | Check |
|---|---|---|
| Revit → render engine | Live link or FBX | Materials renamed and mapped |
| SketchUp → Blender | FBX / glTF | Scale, normals, smoothing |
| Revit ↔ consultants | DWG / IFC | Layers, coordinates, versions |
| Any → client | PDF, JPG/PNG renders, MP4 walkthrough | Branding, resolution |

## Drawing standards for interiors

- Common scales: plans 1:50 (1:100 overall), elevations 1:20–1:50, joinery and
  furniture 1:10–1:20, details 1:1–1:5.
- Every sheet: KAÏRA title block, project, drawing number, scale, date, revision,
  north arrow on plans.
- Dimension to finished faces; note "all dimensions to be verified on site".
