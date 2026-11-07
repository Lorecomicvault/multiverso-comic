import os
import sys
import time
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
from io import BytesIO
from pathlib import Path
from PIL import Image

sys.path.insert(0, r"C:\Users\Vanes\comics en espanol")
from src.cloud_runner import create_full_panel_frame

CURATED_BASE = Path(r"C:\Users\Vanes\comics en espanol\assets\curated_panels")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_image_url(wiki, file_title):
    url = f"https://{wiki}/api.php"
    params = {"action": "query", "titles": file_title, "prop": "imageinfo", "iiprop": "url", "format": "json"}
    r = requests.get(url, params=params, headers=HEADERS, timeout=10).json()
    pages = r.get("query", {}).get("pages", {})
    for pid, pdata in pages.items():
        info = pdata.get("imageinfo", [])
        if info:
            return info[0]["url"]
    return None

def download_and_format(wiki, file_title, dest_path):
    url = get_image_url(wiki, file_title)
    if not url:
        print(f"❌ No URL for {file_title}")
        return False
    h = HEADERS.copy()
    h["Referer"] = f"https://{wiki}/"
    r = requests.get(url, headers=h, timeout=15)
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content)).convert("RGB")
        formatted = create_full_panel_frame(im, target_w=1080, target_h=1920)
        formatted.save(dest_path, quality=95)
        print(f"✅ Guardado {dest_path.name} desde {file_title}")
        return True
    else:
        print(f"❌ HTTP {r.status_code} for {file_title}")
        return False

# 1. Slot 41: Superman Black Mercy
p41 = CURATED_BASE / "41_superman_black_mercy_mongul"
download_and_format("dc.fandom.com", "File:Superman Annual Vol 1 11.jpg", p41 / "scene_01.jpg")
download_and_format("dc.fandom.com", "File:Black Mercy 0001.jpg", p41 / "scene_02.jpg")
download_and_format("dc.fandom.com", "File:Van-El New Earth 001.jpg", p41 / "scene_03.jpg")
download_and_format("dc.fandom.com", "File:Mongul I 01.jpg", p41 / "scene_04.jpg")

# 2. Slot 47: Carnage USA
p47 = CURATED_BASE / "47_carnage_usa_dover_oklahoma"
download_and_format("marvel.fandom.com", "File:Carnage, U.S.A. Vol 1 1 Textless.jpg", p47 / "scene_01.jpg")
download_and_format("marvel.fandom.com", "File:Doverton from Carnage, U.S.A. Vol 1 1 0001.jpg", p47 / "scene_02.jpg")
download_and_format("marvel.fandom.com", "File:Carnage, U.S.A. Vol 1 2 Textless.jpg", p47 / "scene_03.jpg")
download_and_format("marvel.fandom.com", "File:Carnage, U.S.A. Vol 1 3 Textless.jpg", p47 / "scene_04.jpg")

# 3. Slot 50: Planet Hulk Caiera
p50 = CURATED_BASE / "50_planet_hulk_muerte_caiera"
download_and_format("marvel.fandom.com", "File:Incredible Hulk Vol 2 105 Textless.jpg", p50 / "scene_01.jpg")
download_and_format("marvel.fandom.com", "File:Bruce Banner (Earth-616) and Caiera (Earth-616) from Incredible Hulk Vol 2 102 001.jpg", p50 / "scene_02.jpg")
download_and_format("marvel.fandom.com", "File:Bruce Banner (Earth-616) from Incredible Hulk Vol 2 105 0001.jpeg", p50 / "scene_03.jpg")
download_and_format("marvel.fandom.com", "File:Bruce Banner (Earth-616) and Caiera (Earth-616) from Incredible Hulk Vol 2 98 001.jpg", p50 / "scene_04.jpg")

print("Slots 41, 47, 50 parchados con paneles 100% únicos!")
