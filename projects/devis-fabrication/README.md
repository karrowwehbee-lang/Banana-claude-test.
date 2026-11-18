# Villa KAÏRA — Devis descriptif et quantitatif de fabrication du mobilier

Document de consultation pour le fabricant (A3 paysage, 66 pages). **Aucun prix, aucun montant, aucun total financier** :
chaque référence est à chiffrer séparément, dans l'unité indiquée (pce, ens., m², ml).

Livrable : `livrables/KAIRA-Villa-Devis-fabrication-mobilier-A3.pdf`

## Contenu

| Section | Pages |
|---|---|
| 0 · Présentation | couverture, sommaire, périmètre et conventions, éléments exclus |
| 1 · Salon principal (RDC) | SAL-01 à SAL-09 + bordereau |
| 2 · Espace salle à manger (RDC) | SAM-01 à SAM-05 + bordereau |
| 3 · Chambre d'amis (RDC) | AMI-01 à AMI-08 + bordereau |
| 4 · Séjour (étage 1) | SEJ-01 à SEJ-05 + bordereau |
| 5 · Chambre principale (étage 1) | CHP-01 à CHP-06 + bordereau |
| 6 · Douche principale (étage 1) | DPE-01 à DPE-11 + bordereau |
| 7 · Synthèse quantitative | récapitulatif des 44 références ; totaux par espace et par nature ; surfaces, LED, menuiseries |
| 8 · Annexes | A — exclus ; B — hors fabrication (à approvisionner ou à confirmer) ; C — points à confirmer |

Chaque fiche : extrait agrandi du rendu (fenêtre sur le fichier original), élévation ou dessin coté (+ mur entier pour
situer l'élément), rendu entier avec la zone encadrée, et 17 rubriques (espace, désignation, référence, quantité,
dimensions, matériaux, supports, finitions et couleurs, revêtements, façades, poignées, ouverture, éclairage,
fabrication, pose, références rendu / élévation, observations).

## Exclusions (demandées par KAÏRA)

Placard de la chambre principale (dressing M12) · placard d'angle de la chambre d'amis (armoire de l'alcôve M8) · tous
les lits · toutes les tables de chevet · les téléviseurs. Les meubles TV, leurs structures, habillages muraux et
rangements sont inclus.

## Règles appliquées

- Rendus 3D : fichiers originaux, jamais recadrés ni retouchés ; les extraits sont des fenêtres sur l'original, signalées
  par un cadre sur le rendu entier de la même fiche.
- Cotes : écrites sur un plan (gras), relevées « ≈ » (italique), ou **DIMENSION À CONFIRMER** — aucune cote inventée.
- Matériaux : nommés comme sur les rendus ; sinon **FINITION À CONFIRMER** ; support non défini : **SUPPORT À CONFIRMER**.
  Aucune référence commerciale.
- Surfaces brutes calculées sur les élévations du dossier technique (`tools/surfaces.py`, grille de 1 cm).

## Outils

- `tools/surfaces.py` — surfaces d'habillage par mur et par finition (données `projects/dossier-technique/tools/data.py`).
- `tools/data_fab.py` — les 44 références, exclusions et éléments hors fabrication.
- `tools/build.py` — mise en page A3 (identité des dossiers KAÏRA) → `build/devis-fabrication.html` et le PDF.
  `python3 tools/build.py [--previews]`. Le build refuse tout texte de type prix (€, HT, TTC, prix unitaire).
