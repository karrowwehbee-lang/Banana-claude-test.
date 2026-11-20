# KAÏRA — Portfolio « Chambres d'enfants »

PDF : `livrables/KAIRA-Portfolio-Chambres-enfants.pdf` — 46 pages, 360 × 240 mm (ratio 3:2 des rendus, qui occupent
la page entière sans recadrage).

## Projets

| N° | Nom | Rendu | Type |
|---|---|---|---|
| 01 | Douceur Lapin | sources/recus/01.png | Nurserie |
| 02 | Jungle Douce | sources/recus/06.png | Nurserie évolutive |
| 03 | Nuages | sources/recus/04.png | Chambre petite enfance |
| 04 | Ourson Caramel | sources/recus/05.png | Chambre petite enfance |
| 05 | Nuage Olive | sources/recus/07.png | Chambre d'enfant avec bureau |

Les images 02 et 03 (inspirations d'autres studios : livres en cyrillique, composition reprise par l'image 04) ne sont
pas présentées comme projets KAÏRA.

Par projet : rendu pleine page · concept, ambiance, lumière, palette · matériaux et textures · mobilier sur mesure
(vue de face + profil cotés) · architecture et décor · plan d'aménagement coté · élévation du mur décoratif ·
coupe (+ seconde élévation ou détail au 1:10).

## Règles

- Rendus insérés entiers et sans modification ; vérification pixel par pixel dans le PDF.
- Teintes relevées directement sur les rendus (`tools/teintes.json`).
- Toutes les cotes sont des **dimensions proposées pour le concept**, cohérentes avec le mobilier visible et les
  dimensions courantes (lit bébé 60 × 120, couchage 90 × 200, armoires P 60…). Elles sont signalées comme telles et
  seront adaptées aux mesures réelles après relevé.

## Reconstruire

```
python3 tools/pbuild.py --previews
```

`tools/pdata.py` (contenu, dimensions), `tools/pviews.py` (plans, élévations, coupes, profils, textures),
`tools/pbuild.py` (mise en page).
