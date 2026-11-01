import os
import sys
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "deadpool_wolverine_corea_del_norte"
dest_dir.mkdir(parents=True, exist_ok=True)

def get_fandom_image(wiki, title):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    pages = r.get("query", {}).get("pages", {})
    for k, v in pages.items():
        if "imageinfo" in v:
            img_url = v["imageinfo"][0]["url"]
            print(f"Fetching {title} -> {img_url}")
            res = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': f'https://{wiki}/'})
            return Image.open(BytesIO(res.content)).convert('RGB')
    raise ValueError(f"Could not fetch {title}")

# 1. Butler harvesting organs / dark lab
im1 = get_fandom_image("marvel.fandom.com", "File:Bartol Utler (Earth-616) from Deadpool Vol 4 16 001.jpg")
create_full_panel_frame(im1, 1080, 1920).save(dest_dir / "scene_01.jpg", quality=95)

# 2. North Korean mutant camp
im2 = get_fandom_image("marvel.fandom.com", "File:North Korean Deadpool X-Men Mutates (Earth-616) from Deadpool Vol 4 16 001.png")
create_full_panel_frame(im2, 1080, 1920).save(dest_dir / "scene_02.jpg", quality=95)

# 3. Assault on compound (KPA base)
im3 = get_fandom_image("marvel.fandom.com", "File:Korean People's Army (Earth-616) from Deadpool Vol 4 17 001.jpg")
create_full_panel_frame(im3, 1080, 1920).save(dest_dir / "scene_03.jpg", quality=95)

# 4. Rescued captives / aftermath
im4 = get_fandom_image("marvel.fandom.com", "File:North Korean Deadpool X-Men Mutates (Earth-616) from Deadpool Vol 4 18 001.png")
create_full_panel_frame(im4, 1080, 1920).save(dest_dir / "scene_04.jpg", quality=95)

print("All 4 Deadpool frames saved. Checking RMS differences:", flush=True)

def get_rms(p1, p2):
    i1 = np.array(Image.open(p1).convert('RGB').resize((128, 128)), dtype=float)
    i2 = np.array(Image.open(p2).convert('RGB').resize((128, 128)), dtype=float)
    return np.sqrt(np.mean((i1 - i2) ** 2))

for i in range(1, 5):
    for j in range(i + 1, 5):
        p1 = dest_dir / f"scene_{i:02d}.jpg"
        p2 = dest_dir / f"scene_{j:02d}.jpg"
        rms = get_rms(p1, p2)
        print(f"RMS Scene {i} vs Scene {j}: {rms:.2f}", flush=True)
