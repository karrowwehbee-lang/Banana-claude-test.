"""Douche principale — Étage 1 : géométrie relevée (cm). X depuis le mur ouest, Y depuis le mur sud, Z depuis le sol fini.

Statuts : 'v' vérifiée (écrite sur le plan coté IMG_7771), 'd' ≈ déduite (relevé), 'c' à confirmer.

Sources et méthode
- Plan coté IMG_7771 (sources/05.png), partie gauche en L = la salle d'eau, confirmée par Karen sur le plan annoté
  (sources/05-annote.png : « Salle d'eau », flèche sur la porte de 74). Échelle 0,577 cm/px, contrôlée sur ses
  cotes écrites. Cotes écrites reprises : 374,80 · 234,10 · 137,00 · 164,80 · 66,00 · 74,00 · 70,00 · 116,00 · 40,00.
  Partie droite (chambre) : exclue. Sa cote « 478.00 » (≈ 386 à l'échelle) : À VÉRIFIER, non corrigée.
- Vue de dessus IMG_7773 (sources/03.png) : caméra en perspective au-dessus de la pièce, recalée sur le plan coté
  (contour au niveau du plafond 0,2566 cm/px, au sol 0,398 cm/px) → positions des équipements au sol.
- Rendus de face (perspective à un point, horizon au centre de l'image) calibrés sur un mur de largeur vérifiée :
  02 → mur sud (fenêtres sur le plan coté, 4,45 px/cm, caméra à 132 cm) ; 06 → mur est 234,10 (5,04 px/cm, 128 cm) ;
  08 → fond de douche 164,80 (3,82 px/cm, 129 cm). Profondeurs : 02 D ≈ 255 cm, 06 D ≈ 256 cm, 08 D ≈ 317 cm.
  Contrôles : hauteur sous plafond 289 / 289 / 288 ; porte 202 / 203 (06 et 08) ; bord de la porte X 236 relevé sur 08
  contre 230,8 écrit ; coffrage 119 relevé contre 116 écrit ; paroi de douche : 5 rangs de 40,1 cm.
"""

# ---------------------------------------------------------------- room (verified)
W_TOT = 374.8      # largeur partie large (v)
D_LARGE = 234.1    # profondeur partie large (v)
D_RET = 137.0      # profondeur du retour douche (v)
W_RET = 164.8      # largeur du retour douche (v)
D_TOT = D_LARGE + D_RET   # 371,1 (somme de cotes écrites)
NORD = [66.0, 74.0, 70.0]   # mur nord de la partie large : trumeau, porte, trumeau (v)
DOOR_X = (W_RET + 66.0, W_RET + 66.0 + 74.0)   # 230,8 → 304,8
WALL_T = 20.0      # épaisseur des murs (d, mesurée sur le plan coté)
H_PLAF = 289       # hauteur sous plafond (d) — 289 (02), 289 (06), 288 (08)
H_DOOR = 202       # hauteur de la porte (d) — 202 (06), 203 (08)

# windows on the south wall (positions d from the plan drawing, confirmed on render 02)
W1 = dict(x0=56.0, x1=110.8, z0=157, z1=226)   # petite fenêtre, au-dessus du coffrage
W2 = dict(x0=256.1, x1=311.5, z0=13, z1=226)   # fenêtre haute

# ---------------------------------------------------------------- fixtures (d unless noted)
BOXING = dict(x0=0, x1=116.0, y0=0, y1=40.0, h=145)          # coffrage WC : 116 × 40 (v), hauteur ≈ 145
WC = dict(ax=78, w=38, y1=97, seat_h=None)                   # axe ≈ 78, saillie jusqu'à Y ≈ 97 ; largeur à conf.
FLUSH = dict(ax=78, z0=85, z1=97, w=19)                      # plaque de commande sur le coffrage
COMMODE = dict(x0=140, x1=224, y0=0, y1=50, z0=9, z1=87)     # commode en noyer
GLASS_SHELVES = dict(x0=140, x1=240, depth=22, levels=(110, 144, 179))
WALNUT_SHELVES = dict(x0=0, x1=51, depth=20, levels=(179, 216))
VANITY = dict(y0=16, y1=172, depth=52, z0=34, z1=83, split=80)   # niches Y 16–80, tiroirs Y 80–172
BASIN = dict(ay=137, w=45, d=35, z1=97)
SPLASH = dict(y0=2, y1=177, z1=99)                           # crédence terrazzo, de 83 à 99
MIRROR = dict(y0=2, y1=177, z0=99, z1=199)
TOWEL_BAR = dict(y0=179, y1=232, z=78, depth=12)
PENDANTS = [dict(y=29, z=125), dict(y=29, z=144), dict(y=43, z=123), dict(y=43, z=142)]
PEND_X = W_TOT - 52                                          # à l'aplomb du bord du plan vasque
SHOWER = dict(x0=0, x1=122.5, y0=281, y1=D_TOT, curb=8.5, glass_top=208.8, mullion=70,
              rows=(8.5, 48.5, 88, 128, 168, 208.8))
SHOWER_COL = dict(y=339, head_z=220, mixer_z=100, mixer2_z=88)
SHOWER_NICHE = dict(x0=86, x1=112, z0=105, z1=175)           # rangement sur le fond de douche (type à conf.)
HOOKS = [dict(y=274, z=197), dict(y=255, z=180)]             # patères sur le mur X = 164,8 (2e : à conf.)
LADDER = dict(y0=128, y1=204, depth=35)                      # échelle porte-serviettes (mur ouest)
LED_SET = dict(s=28, e=9)                                    # retrait de la ligne LED : 28 (02) / 9 (06) → à conf.
