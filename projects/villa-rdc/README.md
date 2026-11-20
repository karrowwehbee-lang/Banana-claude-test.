# Villa — Ground floor (RDC) · KAÏRA concept v1

Spaces designed: **Salon principal** (≈ 41.5 m²) and **Chambre d'amis** (≈ 10.2 m²).
Architecture as supplied: walls, openings and staircase unchanged.
Assumptions to confirm: ceiling height 2.80 m; the 2.68 m south opening is the glazed entrance;
the 2.07 m opening on the salon's north wall is an internal opening (shown with fluted glass);
the 32 cm square in the south-east corner is a column or duct.

| File | Content |
|---|---|
| `renders/plan-layout-rdc.png` | Furniture layout drawn on the original plan, with numbered legend |
| `renders/render-salon-hero.png` | Salon: towards the travertine fire wall |
| `renders/render-salon-reverse.png` | Salon: towards the gallery zone and library lounge |
| `renders/render-library.png` | Library lounge: walnut library wall and bar niche |
| `renders/render-guest.png` | Guest bedroom: upholstered headboard wall |

The renders are 3D massing concepts built to the plan dimensions (three.js, `tools/scene.js`).
They fix layout, proportions, materials and light. They are a base for the final
photorealistic renders (D5 / V-Ray / Corona), not a replacement for them.

Re-render: serve `tools/` together with the `three` package (0.169.0) and run
`node tools/render.js <www-dir> renders`.

## Console LIGNE (mur habillé à côté d'une porte)

| File | Content |
|---|---|
| `renders/console-front.png`, `console-angle.png`, `console-detail.png` | 3D views (`tools/console.js`, wall width set with `?wall=1.40`) |
| `renders/console-fiche-technique.png` | Elevation, section A-A and schedule, in mm |
