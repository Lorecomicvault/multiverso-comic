import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "10_flash_barry_allen_se_convierte_en_rayo_crisis"
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

files = [
    ("barry_crisis.png", "File:Barry Allen Crisis on Infinite Earths 001.png"),
    ("anti_monitor.jpg", "File:Anti-Monitor 0012.jpg"),
    ("flash_0050.jpg", "File:Flash 0050.jpg"),
    ("flash_0065.jpg", "File:Flash 0065.jpg"),
    ("flash_0068.jpg", "File:Flash 0068.jpg"),
    ("flash_0072.jpg", "File:Flash 0072.jpg")
]

for fname, title in files:
    u = get_fandom_url("dc.fandom.com", title)
    if u:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://dc.fandom.com/'})
        if r.status_code == 200:
            im = Image.open(BytesIO(r.content)).convert('RGB')
            im.save(OUT_DIR / fname)
            print(f"Saved {fname}: {im.size} from {title}")
        else:
            print(f"Failed {title}: status {r.status_code}")
    else:
        print(f"URL not found for {title}")

print("Done Story 10 downloads.")
