# Série Minérale — renders

Gemini 3.5 Flash is a text-only model: it cannot generate images.
Use **Nano Banana 2** (`gemini-3.1-flash-image`), Google's Gemini image model.
It works with the same Gemini API key.

| File | View | Aspect ratio |
|---|---|---|
| `view-01-hero-wide.txt` | Wide-angle hero, 24 mm | 3:2 |
| `view-02-fireplace-closeup.txt` | Fireplace close-up, 85 mm | 4:5 |
| `view-03-seating-area.txt` | Seating area, 35 mm | 3:2 |
| `view-04-evening-lighting.txt` | Evening lighting, 28 mm | 16:9 |

## Option A — script (all four at once)

    ./generate.sh

It saves `view-01-hero-wide.png` … `view-04-evening-lighting.png` in this folder.

## Option B — by hand in Google AI Studio

1. Open aistudio.google.com and pick the model **Nano Banana 2** (gemini-3.1-flash-image).
2. Set the aspect ratio from the table above.
3. Paste the full text of one `.txt` file and run it.
4. Download the image and save it here with the same name, ending in `.png`.

Use one chat per view so earlier images don't influence the next one.
`render-prompts.md` has the full brief, camera notes and Midjourney versions.
