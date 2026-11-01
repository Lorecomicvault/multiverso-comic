import sys
import requests
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

CHARACTERS = [
    ("marvel.fandom.com", "Thaddeus_Ross_(Earth-616)"),
    ("marvel.fandom.com", "Uatu_(Earth-616)"),
    ("marvel.fandom.com", "Johann_Shmidt_(Earth-807128)"),
    ("marvel.fandom.com", "James_Howlett_(Earth-807128)"),
    ("dc.fandom.com", "Harold_Jordan_(New_Earth)"),
    ("dc.fandom.com", "Parallax_(Zero_Hour)"),
    ("marvel.fandom.com", "Pyreus_Kril_(Earth-616)"),
    ("marvel.fandom.com", "Wilson_Fisk_(Earth-616)"),
    ("dc.fandom.com", "Joker_(Prime_Earth)"),
    ("marvel.fandom.com", "Ma_Gnucci_(Earth-616)"),
    ("dc.fandom.com", "World_Forger_(Prime_Earth)"),
    ("marvel.fandom.com", "Jormungand_(Earth-616)"),
    ("dc.fandom.com", "Bartholomew_Allen_(Earth-One)")
]

all_images = {}
for wiki, page in CHARACTERS:
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": page,
        "prop": "images",
        "imlimit": 100,
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    pages = r.get("query", {}).get("pages", {})
    images = []
    for p in pages.values():
        for img in p.get("images", []):
            images.append(img.get("title"))
    all_images[f"{wiki}:{page}"] = images
    print(f"[{wiki}] {page} -> {len(images)} images found:", flush=True)
    for im in images[:10]:
        print(f"   {im}", flush=True)

with open("character_embedded_images.json", "w", encoding="utf-8") as f:
    json.dump(all_images, f, indent=2, ensure_ascii=False)
