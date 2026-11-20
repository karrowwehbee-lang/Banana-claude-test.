# KAÏRA — Dossier technique d'architecture intérieure (Villa RDC + Étage 1)

Second document, independent of the design dossier (`projects/dossier-client`, which is not modified).

PDF (A3 landscape, 58 sheets, 118 MB with the renders embedded losslessly): built in `build/` (not versioned).
The repository keeps it as two volumes under 100 MB (GitHub limit), same pages and numbering:
`livrables/KAIRA-Dossier-technique-Villa-A3-vol1-RDC.pdf` and `…-vol2-Etage.pdf`.

## Content

| Sheets | Content |
|---|---|
| 000–002 | Cover, contents, conventions (status of every dimension, method, sources) |
| 100–111 | General plans: RDC dimensioned plan and furniture plan, first floor (deduced) |
| 200–216 | Séjour RDC: plan, elevations A, B, C, D1, D2, E, sections AA and BB, custom furniture M1–M5, materials, renders |
| 300–310 | Chambre d'amis: plan, elevations A–D, section CC, M6–M8, materials, renders |
| 400–411 | Séjour étage 1: plan, elevations A–D, section DD, M9–M10, materials, renders |
| 500–510 | Chambre principale: plan, elevations A–D, section EE, M11–M13, materials, renders |
| 900 | Everything still to be confirmed on site |

## Dimension status

- **vérifiée** (black): written on the source plan `plan-rdc-cote-2D` — shown with its written value.
- **≈ déduite** (olive, italic): measured to scale on a plan, or on a frontal render calibrated on a known width.
- **À CONF.** (burgundy, dashed): cannot be determined from the project documents. Nothing is invented.

Method (details on sheet 002):
- RDC plan: 1.080 cm/px, checked on its 16 written dimensions.
- Top views of the 3D model: the software grid is exactly 100 cm once registered on the 2D plan → scale for furniture
  (RDC) and for the whole first floor (no dimensioned plan exists).
- Heights: one-point-perspective frontal renders; wall plane calibrated on a known width; checked with the 75" TVs
  (167 × 93 measured in three rooms) and with four renders of the living room (282–286 cm).
- Renders: original files from `projects/dossier-client/sources`, embedded whole and lossless (pixel check in build).

## Build

```
python3 tools/build.py --previews     # HTML + PDF (+ PNG previews of every sheet in build/)
python3 tools/split.py                # two volumes < 100 MB for the repository, and render integrity check
```

`tools/data.py` holds every measurement with its source and status; `tools/views.py` draws plans, elevations,
sections and key plans; `tools/build.py` lays out the sheets and the KAÏRA title block.
