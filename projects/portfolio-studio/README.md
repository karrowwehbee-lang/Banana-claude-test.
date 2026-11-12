# KAÏRA Interior Design — Portfolio du studio (A4 paysage, 30 pages)

| Fichier | Usage |
|---|---|
| `livrables/KAIRA-Portfolio-Studio-HD.pdf` (≈ 83 Mo) | Impression et présentation : rendus originaux intégrés sans aucune modification (PNG au pixel près, JPEG octet pour octet) |
| `livrables/KAIRA-Portfolio-Studio-light.pdf` (≈ 5 Mo) | WhatsApp / e-mail : même mise en page, images recompressées en JPEG (1500 px, qualité 80), sans recadrage ni changement de couleur |

## Structure
Cover · About the Studio (Karen Wehbe, fondatrice) · Creative Vision · Services (8) · Selected Projects (sommaire visuel) ·
**01 Villa** (ouverture, concept, plans RDC et étage, 4 pages de rendus, matériaux, mobilier sur mesure, détails) ·
**02 Residential Interiors** (ouverture, salles à manger, séjours, cuisines, séjour et entrée, détails) ·
**03 Workspaces** · **04 Rooftop Bar & Lounge** · **05 Retail Showroom** (2 pages) ·
**06 Children's Rooms** (collection, dessin technique) · Design Process · Contact.

Nouveaux rendus : `sources/recus/01–16.jpg` (inventaire : `sources/INVENTAIRE.md`). Non retenus : 10 et 11 (showroom,
rendus plus schématiques) ; 07 (écran allumé) uniquement en détail recadré sans l'écran.

## Choix
- Textes en anglais (marque internationale, intitulés demandés en anglais).
- Aucune date, ville, cliente ou référence inventée ; coordonnées manquantes marquées « to be completed ».
- Vues avec écran de télévision allumé écartées des grandes pages ; recadrages (zooms) uniquement sur les pages Materials et Interior Details, les fichiers sources restent intacts.
- Plans et élévations repris du dossier technique (`projects/dossier-technique`) et du portfolio enfants (`projects/portfolio-enfants`).

## Reconstruire
`python3 tools/build.py --previews`
