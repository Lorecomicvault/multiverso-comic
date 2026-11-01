import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "02_wolverine_decapito_red_skull_escudo_capitan"
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

def download_and_save(wiki, title, filename):
    u = get_fandom_url(wiki, title)
    if not u:
        print(f"URL not found for {title}")
        return None
    r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': f'https://{wiki}/'})
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content)).convert('RGB')
        im.save(OUT_DIR / filename, quality=95)
        print(f"Saved {filename}: {im.size} from {title}")
        return im
    else:
        print(f"Failed download {u}: {r.status_code}")
        return None

download_and_save("marvel.fandom.com", "File:Red Skull's Trophy Case from Wolverine Vol 3 72 001.jpg", "raw_s1.jpg")
download_and_save("marvel.fandom.com", "File:Johann Shmidt (Earth-807128) from Wolverine Vol 3 72 001.jpg", "raw_s2.jpg")
download_and_save("marvel.fandom.com", "File:James Howlett (Earth-807128) from Wolverine Vol 3 72 001.jpg", "raw_s3.jpg")
download_and_save("marvel.fandom.com", "File:James Howlett (Earth-807128) from Wolverine Vol 3 72 002.jpg", "raw_s4.jpg")
print("Done Story 2 raw downloads.")
