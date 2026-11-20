# Dossier client KAÏRA — Villa (RDC + Étage 1)

PDF : `livrables/KAIRA-Dossier-de-conception-Villa.pdf` (A4 paysage, 29 pages).

Reconstruire :
1. `python3 tools/tv_off.py` — écrans TV éteints (sources intactes, sorties dans build/tvoff)
2. `python3 tools/swatches.py` — nuanciers relevés dans les rendus (build/swatches)
3. `python3 tools/build_book.py` — compose build/dossier.html (styles : tools/book.css)
4. `node tools/make_pdf.js build ../../livrables/KAIRA-Dossier-de-conception-Villa.pdf` (Playwright)

Provisoire en attendant la charte officielle : logo typographique, polices Cormorant Garamond + Jost, nom du projet (`PROJECT` dans build_book.py).
