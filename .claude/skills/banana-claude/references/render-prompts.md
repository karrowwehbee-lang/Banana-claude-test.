# Photorealistic 3D render prompts

## Prompt structure

Build every prompt in this order and keep each part concrete:

1. **Shot type & room** — "Editorial wide-angle interior photograph of a luxury
   contemporary living room…"
2. **Architecture** — ceiling height, windows, openings, structure, flooring.
3. **Key furniture** — main pieces with material and form.
4. **Materials & finishes** — 3–6 named materials with finish (honed, brushed, matte).
5. **Color palette** — tonal description, plus accent.
6. **Lighting** — time of day, direction of sunlight, artificial layers, color temperature.
7. **Styling** — a few curated objects, art, plants, books; avoid clutter.
8. **Camera** — focal length, height, angle, composition.
9. **Photography style** — editorial magazine, natural, soft contrast, true-to-life color.
10. **Quality** — photorealistic, physically accurate materials, high detail.

## Camera defaults

| Shot | Lens | Camera height | Notes |
|---|---|---|---|
| Wide establishing | 24–28 mm | 1.2–1.4 m | Two-point perspective, verticals straight |
| Medium / vignette | 35–50 mm | 1.0–1.3 m | Focus on a composition or corner |
| Detail | 85–100 mm | at detail | Shallow depth of field, material texture |
| Top-down (moodboard / table) | 50 mm | overhead | Flat lay, soft shadow |

Always ask for "vertical lines corrected, no distortion" for interiors.

## Lighting presets

- **Morning soft**: diffused daylight from large windows, cool-neutral, soft shadows.
- **Golden hour**: low warm sun raking across the floor, long shadows, 2700K interior
  lamps just on.
- **Overcast editorial**: even north light, gentle contrast, true colors — best for
  showing materials.
- **Evening ambience**: dusk outside (blue hour), warm 2700K layered artificial light,
  glowing coves and lamps.

## Template

```
Editorial interior photograph of a [room] in a [location/type of residence],
[architecture: ceiling height, windows, flooring].
[Main furniture with materials and forms].
Materials: [material 1], [material 2], [material 3], [metal accent].
Palette: [tonal base] with [accent].
Lighting: [preset / time of day], [artificial layers], warm 2700K.
Styling: [3–5 curated objects].
Shot on a [lens] lens at [height], [angle], two-point perspective,
vertical lines corrected.
Luxury contemporary design, editorial style of a high-end interiors magazine,
photorealistic, physically accurate materials, soft natural contrast, high detail.
```

## Tool-specific notes

- **Midjourney**: put the most important content first; finish with parameters,
  e.g. `--ar 3:2 --style raw`. Use `--ar 4:5` for social media portrait, `--ar 16:9`
  for presentations. Add `--no clutter, people, text, watermark` when needed.
- **Stable Diffusion / Flux**: use comma-separated descriptors; add a negative
  prompt: `distorted perspective, warped lines, cartoon, CGI look, oversaturated,
  low detail, clutter, text, watermark, people`.
- **Gemini / ChatGPT image / other natural-language models**: write full sentences;
  for edits, describe only what changes and say "keep everything else identical".
- **D5, V-Ray, Enscape, Lumion, Corona, Twinmotion** (real render engines): translate
  the prompt into settings rather than text — camera (focal length, height, two-point
  perspective), sun position and HDRI, exposure, white balance (≈ 5500–6500K for
  daylight scenes), material roughness and bump values, and post-production (subtle
  bloom, vignetting ≤ 10%, no heavy filters).

## Deliverable format

For a project, give one prompt per view, labelled:

```
View 01 — Wide establishing (24 mm) — [prompt]
View 02 — Seating vignette (35 mm) — [prompt]
View 03 — Material detail (85 mm) — [prompt]
View 04 — Evening ambience (28 mm) — [prompt]
```

Keep materials, palette and furniture identical across views so the set reads as one
project.
