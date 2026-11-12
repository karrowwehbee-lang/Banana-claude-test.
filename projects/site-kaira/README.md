# KAÏRA Interior Design — website prototype

Homepage (React 18 + htm, GSAP 3.12 ScrollTrigger, Lenis smooth scroll), published as a private artifact:
https://claude.ai/artifact/BtVkXmJJDUfEKhrgzP7pFv

- `src/home.html` — page source; `build.py` inlines the KAÏRA wordmark (from `projects/kaira-logo`) → `index.html`.
- `img/` — web JPEGs (quality 80) of the studio's renders: whole images, no crop or retouch in the files
  (the hero and parallax frames show them full-bleed on screen).

Sections: preloader · full-screen hero slider (Ken Burns, parallax, ceiling-height dimension line) · studio statement
(scroll-revealed) · project index with cursor-following previews and full-screen project galleries · pinned horizontal
gallery "Inside the villa" · studio & process · services · contact (prototype form, nothing is sent) · footer.
Next pages to build: Studio, Projects, individual project pages, Services, Contact.
