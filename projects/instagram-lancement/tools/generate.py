"""KAÏRA — génère les visuels du feed avec Gemini (génération d'images).

Usage :
  python3 tools/generate.py --models            liste les modèles d'image disponibles sur la clé
  python3 tools/generate.py 02-salon            génère un visuel (prompts/02-salon.txt)
  python3 tools/generate.py all                 génère tous les visuels manquants

La clé est ajoutée par le proxy réseau de l'environnement cloud (en-tête x-goog-api-key) ;
en local, définir GEMINI_API_KEY. Le modèle se choisit avec GEMINI_IMAGE_MODEL, sinon le meilleur
modèle d'image disponible est pris automatiquement (Pro avant Flash).
"""
import base64, json, os, pathlib, sys, time, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS, RAW = ROOT / "prompts", ROOT / "build/raw"
API = "https://generativelanguage.googleapis.com/v1beta"
KEY = os.environ.get("GEMINI_API_KEY", "proxy-injected")
PREFERENCE = ["gemini-3-pro-image", "gemini-3.1-pro-image", "gemini-3.1-flash-image", "gemini-3-flash-image",
              "gemini-2.5-flash-image"]


def call(url, body=None, timeout=300):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Gemini HTTP {e.code} : {e.read().decode()[:600]}")


def image_models():
    data = json.loads(call(f"{API}/models?pageSize=200"))
    return [m["name"].split("/")[-1] for m in data.get("models", [])
            if "image" in m["name"] and "generateContent" in m.get("supportedGenerationMethods", [])]


def pick_model():
    if os.environ.get("GEMINI_IMAGE_MODEL"):
        return os.environ["GEMINI_IMAGE_MODEL"]
    avail = image_models()
    for pref in PREFERENCE:
        hits = [m for m in avail if m.startswith(pref)]
        if hits:
            return sorted(hits, key=lambda m: ("preview" in m, m))[0]   # version stable de préférence
    if avail:
        return avail[0]
    raise SystemExit("Aucun modèle d'image Gemini disponible sur cette clé.")


def generate(name, model):
    style = (PROMPTS / "_style.txt").read_text().strip()
    prompt = (PROMPTS / f"{name}.txt").read_text().strip() + "\n\n" + style
    cfg = {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "1:1"}}
    if "pro" in model:
        cfg["imageConfig"]["imageSize"] = "2K"
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": cfg}
    for attempt in range(3):
        raw = call(f"{API}/models/{model}:streamGenerateContent?alt=sse", body)
        for line in raw.splitlines():
            if not line.startswith("data: "):
                continue
            d = json.loads(line[6:])
            if "error" in d:
                raise SystemExit("Gemini : " + d["error"].get("message", ""))
            for c in d.get("candidates", []):
                for p in c.get("content", {}).get("parts", []):
                    img = p.get("inlineData")
                    if img:
                        ext = {"image/jpeg": ".jpg", "image/webp": ".webp"}.get(img.get("mimeType"), ".png")
                        RAW.mkdir(parents=True, exist_ok=True)
                        out = RAW / f"{name}{ext}"
                        out.write_bytes(base64.b64decode(img["data"]))
                        (RAW / f"{name}.model.txt").write_text(model)
                        return out
        print(f"  pas d'image (essai {attempt + 1}) : {raw[:300]}")
        time.sleep(5)
    raise SystemExit(f"Échec de génération pour {name}")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg == "--models":
        print("\n".join(image_models()))
        sys.exit()
    model = pick_model()
    names = [p.stem for p in sorted(PROMPTS.glob("[0-9]*.txt"))] if arg == "all" else [arg]
    for n in names:
        if arg == "all" and any(RAW.glob(f"{n}.*g")):
            continue
        print(f"{n} — {model} …")
        print("  ->", generate(n, model))
