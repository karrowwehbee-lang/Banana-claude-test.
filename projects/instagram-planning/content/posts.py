"""KAÏRA — Instagram content queue (specs). One entry = one daily feed publication, in publishing order.

Each spec: id (3 digits), slug, pillar, kind ('carousel' | 'image' | 'reel'), renders used, build() → slides or reel,
caption (English), hashtags. make_post.py renders a spec into queue/<id>_<slug>/.
Captions never name clients, locations or dates that Karen has not given.
"""
CORE = ["#kairainteriordesign", "#interiorarchitecture", "#interiordesign", "#luxuryinteriors", "#interiordesigner"]
TAGS = {
    "residential": ["#luxuryhomes", "#contemporaryinterior", "#modernluxury", "#residentialdesign", "#livingroomdesign"],
    "bedroom": ["#bedroomdesign", "#masterbedroom", "#luxurybedroom", "#calminteriors"],
    "lighting": ["#lightingdesign", "#indirectlighting", "#architecturallighting", "#ledlighting"],
    "materials": ["#materialpalette", "#interiordetails", "#walnut", "#marble", "#naturalmaterials"],
    "joinery": ["#bespokefurniture", "#customfurniture", "#joinerydesign", "#madetomeasure"],
    "hospitality": ["#hospitalitydesign", "#bardesign", "#rooftopbar", "#loungedesign"],
    "process": ["#designprocess", "#technicaldrawing", "#interiorelevation", "#3dvisualization"],
    "viz": ["#3dvisualization", "#interiorrender", "#archviz"],
    "quiet": ["#quietluxury", "#minimalluxury", "#timelessdesign"],
}


def tags(*groups):
    out = list(CORE)
    for g in groups:
        for t in TAGS[g]:
            if t not in out:
                out.append(t)
    return " ".join(out[:16])


def P(**kw):
    POSTS.append(kw)


POSTS = []

# 001 — Residential — carousel
P(id="001", slug="sculptural-calm", pillar="Project", kind="carousel", renders=["n03", "n02"],
  build=lambda S: [
      S.cover("n03", "white", "Residential Interiors", "Sculptural<br>calm", "Living room"),
      S.render_slide("n02", "white", "The dining room — a gallery of portraits", "02 / 03"),
      S.numbered("olive", "Design notes", "The details", [
          ("Curved bouclé seating", "A sofa and arched armchairs in soft white bouclé."),
          ("Walnut fluted strips", "A vertical rhythm framing taupe wall panels."),
          ("Track lighting", "Black rails that light the art, not the room."),
          ("Glass globe pendants", "A floating cluster above the marble table.")], size_t=80, pg="03 / 03")],
  caption="Sculptural calm.\n\nA living room shaped by soft curves — a bouclé sofa and arched armchairs set against taupe "
          "panels and walnut fluted strips — opening onto a dining room conceived as a gallery of portraits.\n\n"
          "Swipe for the dining room and the design notes.\n\nInterior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=tags("residential", "quiet", "viz"))

# 002 — Villa — single image
P(id="002", slug="oak-and-shadow", pillar="Detail", kind="image", renders=["rdc-salon-08"],
  build=lambda S: [S.cover("rdc-salon-08", "white", "Villa — Living room", "Oak &amp; shadow", "Detail")],
  caption="Oak & shadow.\n\nLight oak columns rise from fluted, backlit bases, set between cream panels with fine shadow "
          "joints. At the end of the room, a double door in dark wood closes the composition.\n\n"
          "Villa — living room. Interior design by KAÏRA Interior Design.",
  hashtags=tags("materials", "lighting", "residential").replace("#walnut #marble", "#oakwood #woodpanelling"))

# 003 — Villa — Reel
P(id="003", slug="quiet-bedrooms-reel", pillar="Reel", kind="reel",
  renders=["chambre-principale-05", "chambre-principale-01", "chambre-principale-03", "chambre-amis-01", "chambre-amis-03"],
  reel=dict(kick="Villa", title="Quiet<br>bedrooms", scenes=[
      ("chambre-principale-05", "Master bedroom — backlit marble"), ("chambre-principale-01", "Upholstered headboard wall"),
      ("chambre-principale-03", "Bay window and mirrored panels"), ("chambre-amis-01", "Guest bedroom — oak slats"),
      ("chambre-amis-03", "Soft light, layered curtains")]),
  caption="Quiet bedrooms.\n\nA dark veined marble band, backlit between oak columns. A wall-to-wall upholstered headboard. "
          "In the guest room, vertical oak slats and opal pendants. Two bedrooms of the same villa, written in the same "
          "calm language.\n\nInterior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=tags("bedroom", "quiet", "viz"))

# 004 — Design notes — lighting
P(id="004", slug="light-that-disappears", pillar="Design notes", kind="carousel",
  renders=["rdc-salon-10", "chambre-principale-03", "n01"],
  build=lambda S: [
      S.solid("burgundy", "Design notes", "Light that<br>disappears", "Four principles we apply to every project.",
              foot="Swipe"),
      S.render_slide("rdc-salon-10", "white", "Two lit ceiling coffers, separated by a black profile", "01"),
      S.render_slide("chambre-principale-03", "white", "A perimeter cove draws the volume of the room", "02"),
      S.render_slide("n01", "white", "LED lines under shelves and wall units", "03"),
      S.numbered("white", "Design notes", "The principles", [
          ("Coves, not spots", "Light the ceiling, and the ceiling lights the room."),
          ("Backlit, not bright", "Niches, panels and marble glow from behind."),
          ("Lines, not fixtures", "Light is built into the architecture."),
          ("Warm white", "A warm colour temperature for evening calm.")], size_t=80, pg="05 / 05")],
  caption="Light that disappears.\n\nIn our interiors, you see the light — rarely the fixture. Coves wash the ceilings, "
          "LED lines hide under shelves, panels and marble glow from behind. The result is a soft, even light that "
          "shapes the architecture.\n\nSave this post for your next project.",
  hashtags=tags("lighting", "quiet", "residential"))

# 005 — Hospitality — carousel
P(id="005", slug="rooftop-bar", pillar="Project", kind="carousel", renders=["n05", "n08"],
  build=lambda S: [
      S.cover("n05", "white", "Rooftop Bar &amp; Lounge", "Above<br>the city", "Hospitality"),
      S.render_slide("n08", "white", "The lounge — woven armchairs facing the bar", "02 / 03"),
      S.numbered("choc", "Design notes", "The bar", [
          ("Walnut battens", "Vertical rhythm on every face of the counter."),
          ("Green marble top", "A deep, veined stone against the skyline."),
          ("Recessed LED line", "A band of light that cuts the walnut."),
          ("White marble floor", "Bright, continuous, open to the view.")], size_t=80, pg="03 / 03")],
  caption="Above the city.\n\nA rooftop bar and lounge: a counter clad in vertical walnut battens, topped with green "
          "marble and cut by a line of light; woven armchairs and brass stools facing the skyline.\n\n"
          "Interior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=tags("hospitality", "materials", "viz"))

# 006 — Materials — carousel
P(id="006", slug="walnut-and-black-marble", pillar="Materials", kind="carousel", renders=["n01", "n09", "n04"],
  build=lambda S: [
      S.palette_slide("white", "Material study", "Walnut &amp;<br>black marble", [
          ("Walnut", S.sample("n09", (330, 200, 420, 560))), ("Black marble", S.sample("n01", (390, 470, 470, 600))),
          ("Greige lacquer", S.sample("n01", (1360, 520, 1500, 760))), ("Light oak", S.sample("n04", (640, 735, 1000, 760))),
          ("Green marble", S.sample("n05", (450, 895, 800, 925)))],
          "Tints sampled from our renders."),
      S.render_slide("n01", "white", "Kitchen — greige lacquer and black veined marble", "02 / 04"),
      S.render_slide("n09", "white", "Living room — walnut cabinetry and a lit black niche", "03 / 04"),
      S.render_slide("n04", "white", "Office — light oak and black fluting", "04 / 04")],
  caption="Material study — walnut & black marble.\n\nDeep woods and dark stones, balanced by greige lacquer and light oak. "
          "A palette we return to for kitchens, living rooms and workspaces: warm, quiet and made to last.\n\n"
          "Which one would you choose for your home?",
  hashtags=tags("materials", "joinery", "quiet"))

# 007 — Process — carousel with a concept elevation (no client drawings on Instagram)
P(id="007", slug="from-render-to-drawing", pillar="Process", kind="carousel", renders=["k07"],
  build=lambda S: [
      S.solid("olive", "Our process", "From render<br>to drawing", "Every wall we design is drawn, dimensioned and "
              "detailed — ready for the workshop.", foot="Swipe"),
      S.render_slide("k07", "white", "Nuage Olive — children's room concept, 3D visualization", "02 / 04"),
      S.drawing_slide(S.concept_elevation_svg("nuageolive"), "Design drawing", "The same wall, drawn",
                      "Concept elevation: wardrobe, olive storage column, fluted wall with a backlit cloud, upholstered "
                      "headboard, trundle bed and floating desk."),
      S.numbered("white", "Our process", "Four steps", [
          ("Survey", "Measurements, photographs and existing plans."),
          ("Concept", "Atmosphere, materials and layout."),
          ("3D visualization", "Realistic renders of each key space."),
          ("Technical drawings", "Elevations, sections and joinery details.")], size_t=80, pg="04 / 04")],
  caption="From render to drawing.\n\nA 3D view shows the atmosphere; the drawing makes it buildable. For each project we "
          "draw elevations, sections and bespoke joinery so that workshops build exactly what was designed.\n\n"
          "Swipe to see the Nuage Olive children's room concept, rendered and drawn.",
  hashtags=tags("process", "joinery", "viz"))

# 008 — Villa — Reel (first-floor living room; etage1-sejour-02 is held back by the 30-day launch-feed rule)
P(id="008", slug="upstairs-living-reel", pillar="Reel", kind="reel",
  renders=["etage1-sejour-03", "etage1-sejour-04", "etage1-sejour-06", "etage1-sejour-09"],
  reel=dict(kick="Villa", title="Upstairs,<br>softly lit", scenes=[
      ("etage1-sejour-03", "First-floor living room — sheer curtains"), ("etage1-sejour-04", "Lit oak shelving and red artwork"),
      ("etage1-sejour-06", "Oak double door and a quiet corner"), ("etage1-sejour-09", "A cove of light around the room")]),
  caption="Upstairs, softly lit.\n\nThe villa's first-floor living room, seen from every side: sheer curtains along tall "
          "windows, a ceiling cove that traces the room, oak shelving lit shelf by shelf, and a red-and-white artwork "
          "beside an oak double door. A green-grey corner sofa, an oval marble coffee table and a cognac leather pouf "
          "keep it warm and relaxed.\n\nSave it for your next living-room project. Interior design & 3D visualization "
          "by KAÏRA Interior Design.",
  hashtags=tags("residential", "viz") + " #villadesign #indirectlighting")

# 009 — Design notes — zoning open spaces (Residential + Workspaces; not Villa, which is 008)
P(id="009", slug="one-room-several-zones", pillar="Design notes", kind="carousel", renders=["r19", "n06", "r14"],
  build=lambda S: [
      S.solid("choc", "Design notes", "One room,<br>several zones", "How we organise open spaces without walls.",
              foot="Swipe"),
      S.render_slide("r19", "white", "A rug and two low sofas draw the lounge", "01"),
      S.render_slide("n06", "white", "The dining zone, under a recessed line of light", "02"),
      S.render_slide("r14", "white", "Office — lounge, meeting table and desk in one room", "03"),
      S.numbered("white", "Design notes", "The principles", [
          ("Rugs draw the plan", "Each zone stands on its own ground."),
          ("The ceiling follows", "Coves and light lines echo the zones below."),
          ("Furniture as walls", "A sofa back or a table edge marks the limit."),
          ("One continuous floor", "A single finish keeps the space whole.")], size_t=80, pg="05 / 05")],
  caption="One room, several zones.\n\nOpen spaces need structure, not walls. A rug and two low sofas draw the lounge, a "
          "recessed line of light marks the dining table, oak-clad columns frame the view, and in an office the lounge, "
          "the meeting table and the desk each find their own place, all on one continuous floor.\n\n"
          "Save this post for your next open-plan project.",
  hashtags=" ".join(CORE + ["#openplanliving", "#spaceplanning", "#livingroomdesign", "#diningroomdesign", "#officedesign",
                            "#workspacedesign", "#residentialdesign", "#contemporaryinterior", "#3dvisualization",
                            "#interiorrender"]))

# 010 — Children's Rooms — Reel (Friday project spotlight as a Reel: two-Reels-a-week test from the 15 Nov review)
P(id="010", slug="little-worlds-reel", pillar="Reel", kind="reel", renders=["k01", "k04", "k05", "k06"],
  reel=dict(kick="Children's Rooms", title="Little<br>worlds", scenes=[
      ("k01", "Douceur Lapin — blush pink arches"), ("k04", "Nuages — backlit clouds, sage bed"),
      ("k05", "Ourson Caramel — the teddy-bear arch"), ("k06", "Jungle Douce — sage arches, painted leaves")]),
  caption="Little worlds.\n\nFour children's rooms from our collection, each built around one idea: soft pink arches for "
          "Douceur Lapin, backlit clouds above a sage bed for Nuages, a caramel teddy-bear arch for Ourson Caramel and "
          "painted leaves for Jungle Douce. Rounded shapes, warm light and low open shelves within reach.\n\n"
          "Interior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#kidsroomdesign", "#childrensroom", "#nurserydesign", "#kidsinterior", "#playfulinteriors",
                            "#bespokefurniture", "#customfurniture", "#3dvisualization", "#interiorrender", "#archviz"]))

# 011 — Villa — Materials & palette
P(id="011", slug="oak-marble-and-burgundy", pillar="Materials", kind="carousel",
  renders=["rdc-salon-02", "rdc-salon-01", "rdc-salon-09"],
  build=lambda S: [
      S.palette_slide("white", "Material study", "Oak, marble<br>&amp; burgundy", [
          ("Light oak", S.sample("rdc-salon-01", (1340, 650, 1520, 1000))),
          ("Veined marble", S.sample("rdc-salon-01", (600, 1250, 680, 1500))),
          ("Greige panel", S.sample("rdc-salon-02", (1340, 750, 1420, 1000))),
          ("Charcoal leather", S.sample("rdc-salon-02", (330, 1080, 520, 1180))),
          ("Burgundy", S.sample("rdc-salon-09", (1450, 850, 1560, 950)))],
          "Tints sampled from our renders."),
      S.render_slide("rdc-salon-02", "white", "Villa living room — oak fins, greige panels, charcoal sofa", "02 / 04"),
      S.render_slide("rdc-salon-01", "white", "Oak shelving and a veined marble column", "03 / 04"),
      S.render_slide("rdc-salon-09", "white", "Dining — pale stone table and a burgundy artwork", "04 / 04")],
  caption="Material study — oak, marble & burgundy.\n\nIn the villa's living and dining room, light oak shelving and fins "
          "meet a veined marble column, greige wall panels and charcoal leather, with one deep burgundy artwork as the "
          "accent. Warm, restrained and made to age well.\n\nSave it as a reference for your own palette.",
  hashtags=" ".join(CORE + ["#materialpalette", "#interiordetails", "#oakwood", "#marble", "#naturalmaterials",
                            "#villadesign", "#livingroomdesign", "#diningroomdesign", "#quietluxury", "#timelessdesign"]))

# ---- Coverage plan (16 Nov 2026): every render Karen sent appears in at least one post — see COVERAGE.md ----

# 012 — Retail Showroom I — carousel (Retail at most once every two weeks: part II not before 6 Dec)
P(id="012", slug="a-showroom-in-zones", pillar="Project", kind="carousel", renders=["n13", "n11", "n10", "n12"],
  build=lambda S: [
      S.cover("n13", "white", "Retail Showroom", "A showroom<br>in zones", "Retail"),
      S.render_slide("n11", "white", "Overview — one zone per brand, one material language", "02 / 05"),
      S.render_slide("n10", "white", "TV and air-conditioning islands on wood-topped plinths", "03 / 05"),
      S.render_slide("n12", "white", "Audio island — stepped wood shelves", "04 / 05"),
      S.numbered("choc", "Design notes", "The showroom", [
          ("One language", "Charcoal, wood and white for every brand."),
          ("Islands", "Products at hand height, with room to walk around."),
          ("Wall bays", "Framed niches that read from across the hall."),
          ("Light lines", "LED profiles that guide the eye.")], size_t=80, pg="05 / 05")],
  caption="A showroom in zones.\n\nAn electronics and appliance showroom organised brand by brand: framed wall bays in "
          "charcoal and white, islands on wood-topped plinths, and lines of light that lead visitors through the hall.\n\n"
          "Retail interior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#retaildesign", "#showroomdesign", "#retailinterior", "#storedesign", "#visualmerchandising",
                            "#commercialdesign", "#retailspace", "#3dvisualization", "#interiorrender", "#archviz"]))

# 013 — Villa — art (the two Villa renders without a screen that were not yet planned)
P(id="013", slug="art-first", pillar="Detail", kind="carousel", renders=["rdc-salon-06", "etage1-sejour-08"],
  build=lambda S: [
      S.cover("rdc-salon-06", "white", "Villa — Living &amp; dining", "Art first", "Detail"),
      S.render_slide("etage1-sejour-08", "white", "First-floor lounge — a red-and-white work beside the oak door", "02 / 03"),
      S.numbered("olive", "Design notes", "Placing art", [
          ("A wall of its own", "No shelves or fixtures competing with it."),
          ("Scale", "A large work for a large wall, never the reverse."),
          ("Quiet around it", "Neutral panels and furniture let it lead."),
          ("Light", "Soft, even light from the ceiling cove.")], size_t=80, pg="03 / 03")],
  caption="Art first.\n\nA large painted portrait, a figure under a wide straw hat in red, ochre and stripes, is given a "
          "whole white wall beside the dining table. Upstairs, a red-and-white work answers the oak door. Everything "
          "around them stays quiet so that they can lead.\n\nVilla — living and dining room, first-floor lounge.",
  hashtags=" ".join(CORE + ["#artininteriors", "#interiorart", "#statementart", "#villadesign", "#diningroomdesign",
                            "#contemporaryinterior", "#quietluxury", "#timelessdesign", "#interiordetails"]))

# 014 — Residential — design notes: media walls (renders with a screen on: inner slides only, never the cover)
P(id="014", slug="the-media-wall", pillar="Design notes", kind="carousel", renders=["r15", "r16", "n07"],
  build=lambda S: [
      S.solid("burgundy", "Design notes", "The media<br>wall", "How we make room for the screen.", foot="Swipe"),
      S.render_slide("r15", "white", "Walnut cabinetry around a dark panel, with a lit low unit", "01"),
      S.render_slide("r16", "white", "Walnut and black around the screen, marble underfoot", "02"),
      S.render_slide("n07", "white", "Oak slats, black lines and a floating bench", "03"),
      S.numbered("white", "Design notes", "The principles", [
          ("Frame the screen", "A panel or a niche gives it a place."),
          ("Hide the cables", "Everything runs inside the wall."),
          ("Storage below", "A low, floating unit keeps the floor clear."),
          ("Calm when off", "Wood and stone carry the wall, not the screen.")], size_t=80, pg="05 / 05")],
  caption="The media wall.\n\nThe screen is part of the room, so we design around it: walnut cabinetry and a lit low "
          "unit, a dark frame between wood panels, oak slats with black lines and a floating bench. Cables disappear "
          "and the wall stays calm when the screen is off.\n\nSave this post for your living-room project.",
  hashtags=" ".join(CORE + ["#tvwall", "#mediawall", "#tvunit", "#livingroomdesign", "#joinerydesign", "#bespokefurniture",
                            "#walnut", "#woodpanelling", "#contemporaryinterior", "#residentialdesign"]))

# ---- Images received 16 Nov 2026 (sources/2026-11-16): the unfurnished office w08–w15 ----

# 015 — Workspaces — Reel (renders w08, w13, w10, w09; the other four go to 017 so no render repeats within 21 days)
P(id="015", slug="before-the-furniture-reel", pillar="Reel", kind="reel", renders=["w08", "w13", "w10", "w09"],
  reel=dict(kick="Workspaces", title="Before the<br>furniture", scenes=[
      ("w08", "Walnut, stone and a line of light"), ("w13", "A corner of glass and walnut"),
      ("w10", "Storage wall — green marble niches"), ("w09", "Green marble columns, walnut below")]),
  caption="Before the furniture.\n\nAn office floor shown bare, so the architecture speaks first: walnut walls, a beige "
          "veined stone panel, niches backed in green marble, marble-clad columns between tall windows and a line of "
          "light that runs around the ceiling.\n\nInterior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#officedesign", "#workspacedesign", "#officeinterior", "#corporateinterior", "#walnut",
                            "#marble", "#architecturallighting", "#3dvisualization", "#interiorrender", "#archviz"]))

# 016 — Villa — design notes: every screen wall of the villa (the 8 Villa renders with a screen on; solid cover)
P(id="016", slug="the-screen-framed", pillar="Design notes", kind="carousel",
  renders=["rdc-salon-04", "rdc-salon-03", "rdc-salon-07", "etage1-sejour-01", "etage1-sejour-05", "chambre-amis-02",
           "chambre-amis-04", "chambre-principale-04"],
  build=lambda S: [
      S.solid("olive", "Design notes · Villa", "The screen,<br>framed", "Every screen in the villa has its own wall.",
              foot="Swipe"),
      S.render_slide("rdc-salon-04", "white", "Ground floor — a backlit oak panel beside the garden doors", "02 / 10"),
      S.render_slide("rdc-salon-03", "white", "The same wall: lit niches and a low white unit", "03 / 10"),
      S.render_slide("rdc-salon-07", "white", "Seen from the sofa", "04 / 10"),
      S.render_slide("etage1-sejour-01", "white", "First-floor lounge — a long oak unit, lit shelving beside it", "05 / 10"),
      S.render_slide("etage1-sejour-05", "white", "The same wall, from the coffee table", "06 / 10"),
      S.render_slide("chambre-amis-02", "white", "Guest bedroom — veined marble behind the screen, oak fins", "07 / 10"),
      S.render_slide("chambre-amis-04", "white", "A dressing table built into the same wall", "08 / 10"),
      S.render_slide("chambre-principale-04", "white", "Master bedroom — a walnut wall and a low media unit", "09 / 10"),
      S.numbered("white", "Design notes", "In every room", [
          ("One wall, one gesture", "The screen sits inside a panel, never alone."),
          ("Light behind", "A soft halo instead of a bright box."),
          ("Low and light", "Long low units keep the wall calm."),
          ("The room's materials", "Oak, marble and walnut, as everywhere else.")], size_t=80, pg="10 / 10")],
  caption="The screen, framed.\n\nIn the villa, every screen has its wall: a backlit oak panel beside the garden doors, a "
          "long oak unit upstairs, veined marble and oak fins in the guest bedroom, walnut in the master suite. The "
          "screen sits inside the architecture instead of on it.\n\nSwipe through the four rooms.",
  hashtags=" ".join(CORE + ["#mediawall", "#tvwalldesign", "#villadesign", "#villainterior", "#bedroomdesign",
                            "#guestbedroom", "#oakwood", "#marble", "#indirectlighting", "#timelessdesign"]))

# 017 — Workspaces — materials: two finishes for the same office (w14, w15, w11, w12)
P(id="017", slug="choosing-the-stone", pillar="Materials", kind="carousel", renders=["w14", "w15", "w11", "w12"],
  build=lambda S: [
      S.solid("choc", "Material study", "Choosing<br>the stone", "One office, two finishes, before the furniture.",
              foot="Swipe"),
      S.render_slide("w14", "white", "Option A — the feature wall in beige stone", "02 / 06"),
      S.render_slide("w15", "white", "Option B — the same wall in dark green marble", "03 / 06"),
      S.render_slide("w11", "white", "Option A — beige stone columns", "04 / 06"),
      S.render_slide("w12", "white", "Option B — green marble columns", "05 / 06"),
      S.palette_slide("white", "Material study", "The palette", [
          ("Walnut", S.sample("w14", (230, 600, 330, 840))), ("Beige stone", S.sample("w14", (340, 620, 480, 900))),
          ("Green marble", S.sample("w15", (390, 620, 520, 900))), ("Black panel", S.sample("w14", (530, 700, 610, 920))),
          ("White marble", S.sample("w14", (600, 1250, 900, 1450)))], "Tints sampled from our renders.")],
  caption="Choosing the stone.\n\nThe same office, before the furniture, in two finishes: a beige veined stone or a dark "
          "green marble for the feature wall, and the same choice for the columns between the windows. Walnut, black "
          "panels and a white marble floor stay the same.\n\nWhich would you choose, A or B?",
  hashtags=" ".join(CORE + ["#materialpalette", "#materialselection", "#interiordetails", "#marble", "#naturalstone",
                            "#stoneinteriors", "#walnut", "#officedesign", "#workspacedesign", "#timelessdesign"]))

# ---- Images received 16 Nov 2026, second batch (sources/2026-11-16b): boardroom b01–b06, green kitchen g07–g12, kitchen c14 ----

# 018 — Residential — materials: the green kitchen (all six views)
P(id="018", slug="forest-green-and-brass", pillar="Materials", kind="carousel",
  renders=["g09", "g07", "g12", "g08", "g11", "g10"],
  build=lambda S: [
      S.palette_slide("white", "Material study", "Forest green<br>&amp; brass", [
          ("Forest green", S.sample("g09", (990, 300, 1100, 520))), ("Brushed brass", S.sample("g09", (1358, 530, 1360, 550))),
          ("White stone", S.sample("g09", (1290, 590, 1480, 680))), ("Black steel", S.sample("g09", (190, 450, 300, 700))),
          ("Pale floor", S.sample("g09", (600, 1000, 900, 1150)))], "Tints sampled from our renders."),
      S.render_slide("g09", "white", "Kitchen — tall units, glazed cabinets lit from within", "02 / 07"),
      S.render_slide("g07", "white", "Built-in ovens beside a full-height glazed cabinet", "03 / 07"),
      S.render_slide("g12", "white", "The range wall under a slim hood", "04 / 07"),
      S.render_slide("g08", "white", "The whole run, from the fridge to the sink", "05 / 07"),
      S.render_slide("g11", "white", "Sink corner — white veined splashback", "06 / 07"),
      S.render_slide("g10", "white", "The island — green fronts wrapped in white stone", "07 / 07")],
  caption="Forest green & brass.\n\nA kitchen in deep green with brushed brass handles, white veined worktops and "
          "splashback, glazed upper cabinets lit from within and an island wrapped in white stone. One colour, carried "
          "from the floor to the ceiling.\n\nWould you dare a green kitchen?",
  hashtags=" ".join(CORE + ["#kitchendesign", "#greenkitchen", "#luxurykitchen", "#kitchencabinets", "#brasshardware",
                            "#kitchenisland", "#materialpalette", "#interiordetails", "#residentialdesign", "#modernkitchen"]))

# 019 — Workspaces — project: the boardroom (all six views; b01 shows flags: inner slide only)
P(id="019", slug="around-the-table", pillar="Project", kind="carousel", renders=["b03", "b01", "b06", "b02", "b04", "b05"],
  build=lambda S: [
      S.cover("b03", "white", "Workspaces", "Around<br>the table", "Boardroom"),
      S.render_slide("b01", "white", "One long table, a planted centre line, green marble behind", "02 / 07"),
      S.render_slide("b06", "white", "Walnut-tone slats and lines of light overhead", "03 / 07"),
      S.render_slide("b02", "white", "Walnut walls all around", "04 / 07"),
      S.render_slide("b04", "white", "Storage wall — lit shelving backed in green marble", "05 / 07"),
      S.render_slide("b05", "white", "Low cabinets under the windows, the city beyond", "06 / 07"),
      S.numbered("choc", "Design notes", "The boardroom", [
          ("One long table", "Microphones and power built in, plants down the centre."),
          ("Slatted ceiling", "Linear lights between the slats, even and glare-free."),
          ("Walnut and green marble", "Warm walls and one strong stone."),
          ("Storage built in", "Cabinets under the windows, lit shelving between.")], size_t=80, pg="07 / 07")],
  caption="Around the table.\n\nA boardroom designed for long sessions: one long table with built-in microphones and a "
          "planted centre line, a slatted ceiling with linear lights, walnut walls and a wall of green marble that "
          "anchors the room. Storage is built in under the windows and into lit shelving.\n\n"
          "Interior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#boardroom", "#meetingroom", "#conferenceroom", "#officedesign", "#workspacedesign",
                            "#corporateinterior", "#walnut", "#marble", "#lightingdesign", "#3dvisualization"]))

# 020 — Residential — detail: the wood kitchen (single image)
P(id="020", slug="a-bar-for-six", pillar="Detail", kind="image", renders=["c14"],
  build=lambda S: [S.cover("c14", "white", "Residential — Kitchen", "A bar for six", "Detail")],
  caption="A bar for six.\n\nWarm wood cabinetry with built-in ovens, a long wooden bar on a fluted cream base, six white "
          "stools and a square cove of light above. The window brings the garden into the kitchen.\n\n"
          "Residential interiors — kitchen.",
  hashtags=" ".join(CORE + ["#kitchendesign", "#kitchenbar", "#breakfastbar", "#woodkitchen", "#fluteddetails",
                            "#indirectlighting", "#contemporaryinterior", "#modernkitchen", "#residentialdesign"]))

# ---- Images received 16 Nov 2026, third batch (sources/2026-11-16c): private office o01–o08, dressing room d09–d16 ----

# 021 — Workspaces — project: the private office (all eight views)
P(id="021", slug="the-private-office", pillar="Project", kind="carousel",
  renders=["o04", "o08", "o06", "o05", "o03", "o07", "o01", "o02"],
  build=lambda S: [
      S.cover("o04", "white", "Workspaces", "The private<br>office", "Office"),
      S.render_slide("o08", "white", "The desk in front of the window, two visitor chairs", "02 / 09"),
      S.render_slide("o06", "white", "A walnut desk and a wall of four screens", "03 / 09"),
      S.render_slide("o05", "white", "Four screens over a floating unit with stone fronts", "04 / 09"),
      S.render_slide("o03", "white", "Fluted walnut and cream panels, before the furniture", "05 / 09"),
      S.render_slide("o07", "white", "The lounge corner — a walnut return and stone-backed shelving", "06 / 09"),
      S.render_slide("o01", "white", "Two armchairs and a round stone table", "07 / 09"),
      S.render_slide("o02", "white", "The same corner with the shelving lit", "08 / 09"),
      S.numbered("choc", "Design notes", "The office", [
          ("Walnut that wraps", "Wall panels, returns and desk in one wood."),
          ("Cream panels", "Fine joints that keep the walls calm."),
          ("A place to pause", "Two armchairs away from the desk."),
          ("Light in lines", "A ceiling cove and lit shelving.")], size_t=80, pg="09 / 09")],
  caption="The private office.\n\nWalnut panels that wrap the room, cream walls with fine joints, a walnut and black desk "
          "in front of the window, a wall of four screens above a floating unit, and a lounge corner with two armchairs "
          "and stone-backed shelving that can be lit.\n\nInterior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#officedesign", "#privateoffice", "#executiveoffice", "#workspacedesign", "#officeinterior",
                            "#walnut", "#woodpanelling", "#indirectlighting", "#3dvisualization", "#interiorrender"]))

# 022 — Residential — Reel: the dressing room, closed then open (all eight views)
P(id="022", slug="behind-the-doors-reel", pillar="Reel", kind="reel",
  renders=["d13", "d16", "d09", "d12", "d10", "d11", "d15", "d14"],
  reel=dict(kick="Residential", title="Behind<br>the doors", scenes=[
      ("d13", "Closed — cream doors, smoked glass at the centre"), ("d16", "Open — walnut shelving and hanging rails"),
      ("d09", "Cream doors and a lit glass tower"), ("d12", "The same wall, opened"),
      ("d10", "Closed, from the corner"), ("d11", "Open, from the same corner"),
      ("d15", "Glass doors at the heart of the wardrobe"), ("d14", "A walk-in, both sides")]),
  caption="Behind the doors.\n\nOne dressing room, shown closed and then open: tall cream doors with smoked glass at the "
          "centre, a lit glass tower for display, and behind them walnut shelving, hanging rails and drawers planned "
          "piece by piece.\n\nSave it for your own dressing room.",
  hashtags=" ".join(CORE + ["#dressingroom", "#walkincloset", "#wardrobedesign", "#closetdesign", "#bespokefurniture",
                            "#customfurniture", "#joinerydesign", "#walnut", "#storagedesign", "#bedroomdesign"]))

# ---- Images received 16 Nov 2026, fourth batch (sources/2026-11-16d): executive floor e01, light oak office l02–l06,
#      barbershop x10–x13 + x16. Held for Karen: 07–09 (kitchens, edited with Apple Photos Clean Up), 14–15 (top views = plans) ----

# 023 — Barbershop — design notes (x12, x16, x13; x10 and x11 go to 025)
P(id="023", slug="arches-and-leather", pillar="Design notes", kind="carousel", renders=["x12", "x16", "x13"],
  build=lambda S: [
      S.cover("x12", "white", "Barbershop", "Arches &amp; leather", "Barbershop"),
      S.render_slide("x16", "white", "The waiting area — a curved sofa, nested marble tables", "02 / 04"),
      S.render_slide("x13", "white", "Arched mirrors along one wall, light from the street", "03 / 04"),
      S.numbered("choc", "Design notes", "The barbershop", [
          ("Arched mirrors", "One arch per chair, lit along its edge."),
          ("Cognac leather", "Classic chairs against olive-taupe walls."),
          ("A quiet wait", "A curved sofa and brass-legged tables."),
          ("Display in light", "Backlit shelving above a stone counter.")], size_t=80, pg="04 / 04")],
  caption="Arches & leather.\n\nA barbershop drawn around a row of arched mirrors, each lit along its edge, with cognac "
          "leather chairs against olive-taupe walls. At the back, a curved sofa and nested marble tables make the wait part "
          "of the visit, under backlit display shelving.\n\nInterior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#barbershop", "#barbershopdesign", "#salondesign", "#saloninterior", "#commercialdesign",
                            "#archedmirror", "#brassdetails", "#3dvisualization", "#interiorrender", "#archviz"]))

# 024 — Workspaces — Reel (Friday spotlight as a Reel): the light oak office, all five views
P(id="024", slug="light-oak-black-lines-reel", pillar="Reel", kind="reel", renders=["l06", "l04", "l03", "l02", "l05"],
  reel=dict(kick="Workspaces", title="Light oak,<br>black lines", scenes=[
      ("l06", "Light oak and black slats"), ("l04", "A desk with a sculpted return"), ("l03", "Visitor chairs and open shelving"),
      ("l02", "A lounge corner with wooden armchairs"), ("l05", "A coffee wall behind smoked glass")]),
  caption="Light oak, black lines.\n\nA compact office in light oak and black: a desk with a slatted front and a sculpted "
          "return, open shelving in both tones, a lounge corner with wooden armchairs and a glazed wall that hides a "
          "coffee station.\n\nSave it for your next office project.",
  hashtags=" ".join(CORE + ["#officedesign", "#workspacedesign", "#officeinterior", "#oakwood", "#officefurniture",
                            "#deskdesign", "#bespokefurniture", "#minimaloffice", "#3dvisualization", "#interiorrender"]))

# 025 — Barbershop — materials (x11, x10; x10 shows the shop's name: inner slide only)
P(id="025", slug="olive-walnut-and-cognac", pillar="Materials", kind="carousel", renders=["x11", "x10"],
  build=lambda S: [
      S.palette_slide("white", "Material study", "Olive, walnut<br>&amp; cognac", [
          ("Olive taupe", S.sample("x10", (610, 770, 700, 860))), ("Dark walnut", S.sample("x10", (1200, 300, 1330, 650))),
          ("Cognac leather", S.sample("x10", (330, 1250, 420, 1350))), ("White stone", S.sample("x10", (200, 820, 500, 870))),
          ("Brushed brass", S.sample("x10", (763, 1303, 766, 1343)))], "Tints sampled from our renders."),
      S.render_slide("x11", "white", "Barbershop — reception and waiting, the street beyond", "02 / 03"),
      S.render_slide("x10", "white", "The shampoo cabin in olive, the waiting sofa", "03 / 03")],
  caption="Olive, walnut & cognac.\n\nThe palette of our barbershop: olive-taupe walls, dark walnut panels edged with a line "
          "of light, cognac leather chairs, white veined stone and brushed brass on the side tables. Warm, grounded and "
          "calm.\n\nWhich tone would you keep?",
  hashtags=" ".join(CORE + ["#materialpalette", "#colorpalette", "#walnut", "#leatherchairs", "#brassdetails",
                            "#barbershopdesign", "#salondesign", "#interiordetails", "#commercialdesign", "#earthtones"]))

# 026 — Retail Showroom II — carousel (two weeks after 012; the last three showroom renders)
P(id="026", slug="the-appliance-hall", pillar="Project", kind="carousel", renders=["n14", "n15", "n16"],
  build=lambda S: [
      S.cover("n14", "white", "Retail Showroom", "The appliance<br>hall", "Retail"),
      S.render_slide("n15", "white", "TV wall and an island lit from below", "02 / 04"),
      S.render_slide("n16", "white", "Display units outlined in light", "03 / 04"),
      S.numbered("white", "Design notes", "Display", [
          ("Wall bays", "Each brand framed in charcoal and wood."),
          ("Lit plinths", "Islands that float on a line of light."),
          ("A bright floor", "One continuous stone floor for the whole hall."),
          ("Room to walk", "Wide aisles between the islands.")], size_t=80, pg="04 / 04")],
  caption="The appliance hall.\n\nThe second part of our showroom: a long hall of appliances framed in charcoal and wood, a "
          "TV wall facing an island lit from below, and display units outlined in light on a bright stone floor.\n\n"
          "Retail interior design & 3D visualization by KAÏRA Interior Design.",
  hashtags=" ".join(CORE + ["#retaildesign", "#showroomdesign", "#retailinterior", "#storedesign", "#visualmerchandising",
                            "#commercialdesign", "#lightingdesign", "#displaydesign", "#3dvisualization", "#interiorrender"]))

# 027 — Workspaces — detail: the executive floor (single image)
P(id="027", slug="the-executive-floor", pillar="Detail", kind="image", renders=["e01"],
  build=lambda S: [S.cover("e01", "white", "Workspaces", "The executive floor", "Detail")],
  caption="The executive floor.\n\nOne open floor, three uses: a lounge in cream leather around a walnut and black table, a "
          "meeting table by the windows, and a desk in front of stone-backed shelving, with stone-clad columns framing the "
          "city view.\n\nWorkspaces — executive office.",
  hashtags=" ".join(CORE + ["#executiveoffice", "#officedesign", "#workspacedesign", "#officeinterior", "#corporateinterior",
                            "#walnut", "#naturalstone", "#cityview", "#indirectlighting"]))
