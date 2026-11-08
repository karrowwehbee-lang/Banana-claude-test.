# Projet SOCIAM — Chambre principale
**KAÏRA Interior Design · Aménagement intérieur · v1**

> **Base de travail** : capture de ton modèle Blender (`PROJET SOCIAM.blend`). Architecture et matériaux existants conservés :
> panneau en marbre vert rétro-éclairé, colonnes en chêne (haut lisse, bas cannelé, LED à la jonction), chevets en chêne deux tiroirs, habillage laqué blanc à joints, placards blancs, parquet chêne.
>
> **Hypothèses** (à recaler sur tes cotes réelles) : mur de tête 4,60 m, profondeur 5,40 m, hauteur sous dalle 2,85 m, marbre 1,30 m de large, axes des colonnes à ±1,50 m.

---

## 1. Concept — « Écrin vert »
Le marbre reste le sujet. Tout ce que l'on ajoute est plus bas, plus doux et plus clair que lui : une tête de lit basse en bouclé sable laisse le marbre libre au-dessus de 1,22 m, le plafond s'ouvre au-dessus du lit pour l'encadrer, et la lumière vient de la gorge et du mur, jamais d'un spot dans les yeux.

**Mots d'ambiance** : enveloppant · minéral · feutré · symétrique · apaisé

## 2. Implantation

| Élément | Position | Cotes clés |
|---|---|---|
| Lit 180 × 200 (cadre 200 × 215) | Axé sur le marbre | Passage de 10 cm entre cadre et chevets |
| Tête de lit | Contre le marbre, x = ±1,12 m | H 1,22 m — le marbre reste visible sur 1,63 m |
| Banc de pied de lit | 18 cm après le cadre | 1 480 × 440 × H 450 |
| Tapis laine | Sous les 2/3 du lit | 3 100 × 3 600 ; 1,00 m de dégagement devant les placards |
| Circulation au pied du lit | | ≥ 1,40 m jusqu'à l'entrée |

## 3. Palette (existant + ajouts)

| Rôle | Nom | HEX | Emploi |
|---|---|---|---|
| Base | Laque blanc chaud | `#EEEBE5` | Habillages et placards (existant) |
| Accent | Marbre vert | `#2E3F2A` | Panneau de tête (existant) |
| Bois | Chêne miel | `#AC8350` | Colonnes, chevets, parquet (existant) |
| Textile | Bouclé sable | `#D2C3AD` | Tête de lit, cadre de lit, assise du banc |
| Textile | Lin ivoire | `#EDE6DA` | Linge de lit |
| Textile | Lin moka | `#6B5240` | Plaid, coussin |
| Accent textile | Velours forêt | `#2F3E2C` | Coussin, rappel du marbre |
| Métal | Bronze brossé | `#8C6A43` | Chapeau de tête de lit, suspensions |

## 4. Matériaux ajoutés

| Élément | Matériau | Finition | Notes |
|---|---|---|---|
| Tête de lit | Bouclé laine sable, 10 canaux verticaux de 224 mm | Mousse HR 35 kg/m³ + ouate | Martindale ≥ 40 000 ; chapeau en laiton bronze brossé 8 mm |
| Cadre de lit | Même bouclé, arêtes rayonnées R35 | — | Socle en retrait de 12 cm, LED 2 700 K : le lit flotte |
| Banc | Chêne massif (même teinte que les colonnes) + coussin bouclé | Huile-cire mate | Pieds pleins 80 mm, plateau 40 mm |
| Linge | Lin lavé ivoire, plaid lin moka, coussin velours forêt | — | |
| Tapis | Laine bouclée greige | Poils ras | Bords surjetés ton sur ton |
| Plafond | Plaque de plâtre, peinture mate blanc chaud | Mat absolu | Joints creux 10 mm |

## 5. Plafond architectural
- **Faux-plafond périphérique** à 2,62 m.
- **Caisson central rehaussé** à 2,85 m au-dessus du lit (2,90 × 3,20 m), cadré sur la largeur entre les colonnes.
- **Gorge lumineuse** sur les quatre côtés du caisson : lèvre de 10 cm, ruban LED 2 700 K, diffuseur opale, sans points visibles.
- **Fente de 18 cm le long du mur de tête** : le marbre et les colonnes montent jusqu'à la dalle ; un lécheur linéaire 3 000 K y est logé pour faire vibrer les veines du marbre.
- **3 encastrés orientables** basse luminance (UGR < 19) devant les placards.

> ⚠ À valider : hauteur de plénum disponible (VMC, sprinklage éventuel), position des réseaux, accès d'entretien aux drivers LED.

## 6. Éclairage — couches et scènes

| Couche | Source | Temp. | IRC |
|---|---|---|---|
| Ambiante | Gorge du caisson | 2 700 K | ≥ 90 |
| Accent | Lécheur dans la fente (marbre + colonnes) | 3 000 K | ≥ 95 |
| Existant | LED latérales du marbre, LED des colonnes | 2 700 K | — |
| Lecture | Suspensions albâtre Ø 170 × H 300, bas à 1,18 m | 2 400–2 700 K, dim-to-warm | ≥ 90 |
| Veilleuse | LED du socle de lit | 2 700 K | — |
| Fonctionnel | Encastrés devant placards | 3 000 K | ≥ 90 |

**Scènes** : Jour (gorge 30 %, lécheur 40 %) · Ambiance (gorge 60 %, lécheur 70 %, suspensions 40 %) · Lecture (suspensions 80 %, gorge 30 %) · Nuit (socle de lit 10 %, détection de présence).

## 7. Détails signature
1. **Le marbre libéré** — tête de lit volontairement basse ; le marbre se lit du dessus du chapeau en bronze jusqu'à la dalle.
2. **Canaux et cannelures** — les canaux de la tête de lit répondent au rythme vertical des cannelures en chêne.
3. **Le lit en lévitation** — socle en retrait de 12 cm, LED rasante au sol.
4. **La fente lumineuse** — le mur de tête monte au-delà du faux-plafond, éclairé en lumière rasante.
5. **Le vert en écho** — un seul coussin en velours forêt relie le linge au marbre.

## 8. Intégration dans ton fichier Blender
Script : `blender/kaira_chambre.py` (Blender 5.2).

1. Ouvre `PROJET SOCIAM.blend`, onglet **Scripting** → **Open** → `kaira_chambre.py`.
2. En haut du script, ajuste `ROOM_W`, `ROOM_D`, `CEIL_H`, `MARBLE_W`, `COL_X` à tes cotes.
3. **Run Script** (sans l'option `--shell`, ton architecture n'est pas touchée). Une collection `KAIRA_Amenagement` est créée avec un Empty `KAIRA_Origine`.
4. Place `KAIRA_Origine` au sol, au centre du panneau en marbre, sur sa face avant (Snap to Face), l'axe Y orienté vers la chambre. Tout l'aménagement suit.
5. Matériaux créés avec le préfixe `KAIRA_` : remplace-les par tes propres matériaux si tu préfères (ex. ton « bois maron » sur le banc).
6. Rendu : Cycles, AgX, débruitage OpenImageDenoise, 256 à 512 échantillons. Caméras de référence dans le script (section 4).

## 9. Prochaines étapes
- Recaler les cotes sur ton modèle et valider la hauteur du plénum.
- Choix des échantillons : bouclé, lin, bronze.
- Plans : plan de plafond coté, coupe sur gorge 1:5, élévation de la tête de lit 1:20, carnet de luminaires.
