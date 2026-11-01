import sys
import os
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "01_red_hulk_golpea_watcher_humilla_thor"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_fandom_url(wiki, title):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    for p in r.get("query", {}).get("pages", {}).values():
        info = p.get("imageinfo", [{}])[0]
        return info.get("url")
    return None

def download_and_save(url, out_path, referer_wiki=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    if referer_wiki:
        headers['Referer'] = f"https://{referer_wiki}/"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content)).convert('RGB')
        im.save(out_path, quality=95)
        print(f"Saved {out_path.name}: size {im.size}")
        return im
    else:
        print(f"Failed {url}: status {r.status_code}")
        return None

# Scene 1: Red Hulk arrives at the Moon facing Uatu
u1 = "https://thecredhulk.wordpress.com/wp-content/uploads/2014/04/uatu1.jpg"
download_and_save(u1, OUT_DIR / "candidate_s1.jpg")

# Scene 2: Red Hulk punches Uatu
u2 = "https://thecredhulk.wordpress.com/wp-content/uploads/2014/04/uatu2.jpg"
download_and_save(u2, OUT_DIR / "candidate_s2.jpg")

# Fandom uatu punch high-res:
f_uatu = get_fandom_url("marvel.fandom.com", "File:Thaddeus Ross (Earth-616) and Uatu (Earth-616) from Hulk Vol 2 4 0001.jpg")
if f_uatu:
    download_and_save(f_uatu, OUT_DIR / "candidate_s2_fandom.jpg", "marvel.fandom.com")

print("Done Story 1 test candidates.")
