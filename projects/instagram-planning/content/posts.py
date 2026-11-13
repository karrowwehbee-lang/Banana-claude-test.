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
