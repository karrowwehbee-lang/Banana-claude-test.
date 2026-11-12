# KAÏRA Interior Design — website (v2, cinematic "House" direction)

Live preview (private artifact): https://claude.ai/artifact/BtVkXmJJDUfEKhrgzP7pFv
Deployable site: `dist/` (also `livrables/KAIRA-site-web.zip`), self-contained — see `dist/LISEZ-MOI.md` to put it online.
v1 (first redesign) is kept in `src/archive/site-v1.html`.

Direction: inspired by the public preview of the GetLayers "House" template (architecture studio, scroll-driven
fly-through, statement words pinned to the corners, frosted panel, footer uncovered like a curtain). No GetLayers code or
asset is used: everything is original code built on KAÏRA's identity (arch emblem, KA monogram, wordmark, palette,
Cormorant Garamond + Jost) and the studio's own renders.

Home, in scroll order:
1. Loader — the KAÏRA arch draws itself, fills with the first room like a gauge, then opens to full screen.
2. Walk-through — four villa rooms opened like double doors, words in the corners ("Quiet by Design", "Light before
   Matter", "Walls drawn as Furniture", "Measured for Living"), room captions and ceiling heights (≈, from the dossier).
3. Manifesto — words light up as you scroll, small arch-shaped renders set in the text; Light · Matter · Measure.
4. Founder & studio — "Karen / Wehbe" letters climb apart while the arch grows to full screen; a frosted panel rises
   with the studio text and a render rides up behind the glass.
5. Disciplines — the eight services on a 3D drum, with the matching render in an arch.
6. Selected projects — the KA monogram filled with the villa, zoomed through; then each project opens from a window.
7. Process — eight steps that blur away around the active one, beside a render that tilts toward the cursor.
8. CTA, then the burgundy footer uncovered like a curtain, the KAÏRA letters rising one by one.

Pages: `#projects` (index with full-screen hover backdrop and filters) · `#project-<key>` (villa, residential,
workspaces, rooftop, retail, kids: cinematic hero, facts, palette, gallery with full-bleed / pair / arch / horizontal
sequence layouts, lightbox with whole renders, next project opened through the arch) · `#studio` (founder sequence,
stacked principle cards, process) · `#services` (sticky media list) · `#contact` (form, Formspree-ready).
Shared: fluted-oak slat page transitions, floating glass nav pill, custom cursor, film grain, reduced-motion fallback.

Stack: React 18.3.1 + htm 3.1.1, GSAP 3.12.5 + ScrollTrigger, Lenis 1.1.13 (CDN for the preview; local copies in
`vendor/` for `dist/`), fonts self-hosted in `dist/fonts/`.

Build:
- `python3 tools/images.py` makes `img/` from the originals listed in `projects/instagram-planning/library.json`.
  JPEG originals are copied byte for byte; PNG originals are saved once as JPEG q90 4:4:4 at the same size.
  `img/INTEGRITY.json` records the MD5 or PSNR of each file. Renders with a TV switched on are left out.
- `python3 build.py` writes `index.html` (artifact) and `dist/` (own domain). Content lives in `src/site.html`
  (SCENES, MANIFESTO, FOUNDER, STUDIO, PROJECTS, SERVICES, STEPS, CONFIG).
