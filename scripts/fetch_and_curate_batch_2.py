import sys
import os
import json
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
CURATED_DIR = PROJECT_ROOT / "assets" / "curated_panels"

HEADERS_FANDOM_MARVEL = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://marvel.fandom.com/'
}
HEADERS_FANDOM_DC = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://dc.fandom.com/'
}
HEADERS_GENERIC = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def get_fandom_image_url(wiki, file_title):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8).json()
        for p in r.get("query", {}).get("pages", {}).values():
            info = p.get("imageinfo", [{}])[0]
            return info.get("url")
    except Exception as e:
        print(f"Error fetching url for {file_title}: {e}")
    return None

def download_image(url, referer_wiki=None):
    headers = HEADERS_GENERIC.copy()
    if referer_wiki:
        headers['Referer'] = f"https://{referer_wiki}/"
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200 and len(r.content) > 1000:
            return Image.open(BytesIO(r.content)).convert("RGB")
        else:
            print(f"Download failed for {url}: status {r.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

print("=== SCRIPT DE CURACIÓN Y DESCARGA PARA LOTE 2 ===", flush=True)
