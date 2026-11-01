import os
import sys
import json
import time
import requests
import re
from bs4 import BeautifulSoup
from io import BytesIO
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def get_fandom_file_url(wiki: str, file_title: str) -> str:
    clean = file_title if file_title.startswith("File:") else f"File:{file_title}"
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": clean,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=8).json()
        pages = r.get("query", {}).get("pages", {})
        for pid, pdata in pages.items():
            info = pdata.get("imageinfo", [])
            if info:
                return info[0]["url"]
    except Exception as e:
        print(f"Error getting fandom url for {file_title}: {e}")
    return None

def download_and_save(url: str, dest_path: Path, referer: str = None) -> bool:
    h = HEADERS.copy()
    if referer:
        h['Referer'] = referer
    try:
        r = requests.get(url, headers=h, timeout=12)
        if r.status_code == 200 and len(r.content) > 5000:
            im = Image.open(BytesIO(r.content)).convert('RGB')
            framed = create_full_panel_frame(im, 1080, 1920)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            framed.save(dest_path, "JPEG", quality=95)
            print(f"  [OK] Saved {dest_path.name} ({dest_path.stat().st_size // 1024} KB)", flush=True)
            return True
        else:
            print(f"  [FAIL] Download failed: status {r.status_code}, len {len(r.content)}", flush=True)
            return False
    except Exception as e:
        print(f"  [FAIL] Download exception: {e}", flush=True)
        return False

print("Universal Harvester Module Loaded successfully.", flush=True)
