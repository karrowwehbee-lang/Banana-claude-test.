# KAÏRA — Dossier technique : Douche principale, Étage 1 (villa)

Dossier indépendant, même identité, même qualité et même organisation que le dossier technique de la villa
(`projects/dossier-technique`) : A3 paysage, cartouche KAÏRA, numérotation des planches et références des dessins.

**Statut : document de travail (indice 0), 22 planches. Rien n'est finalisé avant que Karen confirme que tous les éléments
ont été transmis (consigne du 17/11/2026).**

Construction : `python3 tools/build.py --previews` → `build/` (non versionné) : HTML, PDF de travail, aperçus PNG.
`tools/details.py` : rendus, 29 détails D01–D29 (zones en pixels du fichier original), planches 401–410.

Règles de Karen (17/11/2026) :
- Détails = agrandissements signalés, extraits des rendus sans retouche, numérotés et légendés ; le rendu original reste
  présenté en entier et en grand sur la même planche, avec la zone encadrée.
- Plan coté IMG_7771 (sources/05.png) : ne correspond pas à la salle d'eau → non utilisé ; ne jamais mélanger les plans
  des chambres avec ceux de la salle d'eau. Sa cote « 478 » ≈ 386 à l'échelle : « À vérifier », rien n'est corrigé.

## Organisation prévue (mêmes séries que le dossier villa)

| Planches | Contenu |
|---|---|
| 000–002 | Page de garde, sommaire, conventions (statut de chaque cote, méthode, sources) |
| 100 | Concept architectural et décoratif |
| 200–2xx | Plan d'aménagement coté, élévations de chaque mur, coupe(s) si nécessaire |
| 300–3xx | Rendus 3D en grand format, entiers, sans aucune modification |
| 400–4xx | Détails : revêtements muraux, carrelage et marbre, meuble vasque, robinetterie, miroirs, éclairage, douche et parois vitrées, niches, plafond et finitions, accessoires |
| 500–5xx | Planches matériaux et finitions (couleurs relevées sur les rendus) |
| 900 | Tout ce qui reste à confirmer |

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
