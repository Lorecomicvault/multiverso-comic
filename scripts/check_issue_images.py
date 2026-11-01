import sys
import requests
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

ISSUES = [
    ("marvel.fandom.com", "Hulk_Vol_2_4"),
    ("marvel.fandom.com", "Hulk_Vol_2_5"),
    ("marvel.fandom.com", "Wolverine_Vol_3_72"),
    ("dc.fandom.com", "Green_Lantern_Vol_3_48"),
    ("dc.fandom.com", "Green_Lantern_Vol_3_49"),
    ("dc.fandom.com", "Green_Lantern_Vol_3_50"),
    ("marvel.fandom.com", "Amazing_Spider-Man_Vol_1_269"),
    ("marvel.fandom.com", "Amazing_Spider-Man_Vol_1_270"),
    ("marvel.fandom.com", "Daredevil_Vol_2_50"),
    ("dc.fandom.com", "Batman_Vol_2_13"),
    ("dc.fandom.com", "Batman_Vol_2_17"),
    ("marvel.fandom.com", "The_Punisher_Vol_5_1"),
    ("dc.fandom.com", "Justice_League_Vol_4_25"),
    ("marvel.fandom.com", "Thor_Vol_1_380"),
    ("dc.fandom.com", "Crisis_on_Infinite_Earths_Vol_1_8")
]

all_images = {}
for wiki, page in ISSUES:
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": page,
        "prop": "images",
        "imlimit": 50,
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
    for im in images[:8]:
        print(f"   {im}", flush=True)

with open("issue_embedded_images.json", "w", encoding="utf-8") as f:
    json.dump(all_images, f, indent=2, ensure_ascii=False)
