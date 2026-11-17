# KAÏRA — Dossier technique : Douche principale, Étage 1 (villa)

Dossier indépendant, même identité, même qualité et même organisation que le dossier technique de la villa
(`projects/dossier-technique`) : A3 paysage, cartouche KAÏRA, numérotation des planches et références des dessins.

**Statut : indice 0, 81 planches A3 paysage — dossier complet de conception et d'architecture intérieure, en attente de la
confirmation de Karen que tous les éléments ont été transmis (la mention « Document de travail » est retirée à ce moment-là).**

Construction : `python3 tools/build.py --previews` → `build/` (non versionné) : HTML, PDF
`KAIRA-Douche-principale-Etage1-Dossier-A3.pdf`, aperçus PNG.
- `tools/build.py` : les 9 sections ; pages de conception au gabarit éditorial du dossier de conception de la villa,
  planches techniques avec le cadre et le cartouche du dossier technique de la villa.
- `tools/palette.py` : 9 couleurs (HEX relevés), 18 matériaux (visuel, finition, emplacement), 17 fiches mobilier et équipements.
- `tools/details.py` : rendus, 39 détails D01–D39, 14 planches de détails.
- `tools/geom.py`, `tools/views_dpe.py`, `tools/tech.py` : cotes et dessins (plans, élévations, coupes, mobilier, éclairage,
  installations).

Règles de Karen (17/11/2026) :
- Nom de l'espace partout : « Douche principale – Étage 1 » (pas « salle d'eau ») ; l'enceinte vitrée = « cabine de douche ».
- Détails = agrandissements signalés, extraits des rendus sans retouche, numérotés et légendés ; le rendu original reste
  présenté en entier et en grand sur la même planche, avec la zone encadrée.
- Plan coté IMG_7771 (sources/05.png) : partie gauche en L = salle d'eau ; la partie chambre n'est jamais mélangée aux
  dessins. Sa cote « 478 » ≈ 386 à l'échelle : « À VÉRIFIER », rien n'est corrigé.

## Organisation (n° de planche KAI-DPE-Nxx : N = section)

| Planches | Contenu |
|---|---|
| 000–002 | Couverture, sommaire, méthode, sources et conventions |
| 100–106 | 1. Concept : présentation, intention architecturale, ambiance, style et principes, aménagement (5 zones), moodboard |
| 200–205 | 2. Couleurs : palette générale, principales, secondaires, accents (HEX), couleurs dans l'espace |
| 300–309 | 3. Matériaux et finitions : vue d'ensemble, 7 familles, nomenclature |
| 400–415 | 4. Détails décoratifs : index, 14 planches (D01–D39, extraits signalés) |
| 500–514 | 5. Dossier technique : plan coté, repérage, élévations A–F, coupes AA–BB, dimensions des équipements, mobilier M1–M2, revêtements, installations |
| 600–604 | 6. Éclairage : plan d'éclairage, gorge lumineuse (principe), miroir et décoratif, points lumineux |
| 700–706 | 7. Mobilier et équipements : 17 fiches |
| 800–807 | 8. Rendus 3D : 7 rendus entiers avec point de vue, élévations, matériaux et détails associés |
| 901–999 | 9. Synthèse : planche de synthèse, synthèse esthétique, points à confirmer, dos |

## Cotes (même convention que le dossier villa)

- **vérifiée** : écrite sur un plan coté fourni par Karen.
- **≈ déduite** : mesurée à l'échelle sur un document du projet (vue de dessus 3D, grille 1 m = 1,805 cm/px ; rendu frontal calibré).
- **COTE À CONFIRMER** : aucune source ; jamais inventée.

## Ce qui existe déjà

- `dossier-client/sources/plans/plan-etage1-amenagement.png` : vue de dessus de l'étage. En haut, quatre pièces carrelées
  (deux grandes en L, deux petites) **sans équipements** : la douche principale n'y est pas identifiable.
- 7 rendus de la salle d'eau reçus le 17/11 (sources/01–04, 06–08).

## Images reçues

Copies exactes dans `sources/`, inventaire dans `sources/INVENTAIRE.md` (à venir).
