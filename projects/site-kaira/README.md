# KAÏRA Interior Design — website

Live prototype (private artifact): https://claude.ai/artifact/BtVkXmJJDUfEKhrgzP7pFv
Deployable site: `dist/` (also `livrables/KAIRA-site-web.zip`) — see `dist/LISEZ-MOI.md` to put it online.

Pages (hash routes): home `#home` · `#projects` · `#project-villa`, `#project-residential`, `#project-workspaces`,
`#project-rooftop`, `#project-retail`, `#project-kids` · `#studio` · `#services` · `#contact`.

Stack: React 18.3.1 + htm, GSAP 3.12.5 + ScrollTrigger, Lenis 1.1.13 (CDN), Cormorant Garamond + Jost.
Effects: preloader, curtain page transitions, Ken Burns hero slider with parallax and dimension line, scroll-revealed
statement, cursor-following project previews, pinned horizontal gallery, scroll-scrubbed image reveals (clip + scale),
lightbox with keyboard and swipe, sticky service media, filters and grid/index views, custom cursor, reduced-motion support.

Build: `python3 build.py` (inlines the wordmark from projects/kaira-logo and image sizes; writes `index.html` and `dist/`).
Content lives in `src/site.html` (PROJECTS, SERVICES, STEPS, CONFIG). Images: `img/` — web JPEGs (q80) of the studio's
renders, whole and unretouched; drawings are children's-room concept drawings only (no client plans).
