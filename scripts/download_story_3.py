import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "03_hal_jordan_masacre_green_lantern_corps_parallax"
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

download_and_save("dc.fandom.com", "File:Destruction of Coast City 01.jpg", "raw_s1.jpg")
download_and_save("dc.fandom.com", "File:Emerald Twilight 01.jpg", "raw_s2.jpg")
download_and_save("dc.fandom.com", "File:Becoming Parallax.jpg", "raw_s4.jpg")

# Search for Sinestro neck or Kilowog in GL 50
url = "https://dc.fandom.com/api.php"
params = {
    "action": "query",
    "list": "search",
    "srsearch": "Sinestro neck Green Lantern Vol 3 50",
    "srnamespace": 6,
    "srlimit": 10,
    "format": "json"
}
r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
print("Search results for Sinestro/GL 50:")
for res in r.get("query", {}).get("search", []):
    print("  ", res.get("title"))
