"""
Universal Multi-Source Harvester & Frame Processor
Downloads authentic interior comic scans for each story and prepares 1080x1920 framed panels.
"""
import os
import sys
import json
import time
import requests
from io import BytesIO
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

def get_fandom_image_url(wiki: str, title: str) -> str:
    clean_title = title if title.startswith("File:") else f"File:{title}"
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": clean_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        pages = r.json().get("query", {}).get("pages", {})
        for pid, pdata in pages.items():
            info = pdata.get("imageinfo", [])
            if info:
                return info[0]["url"]
    except Exception as e:
        print(f"Error fetching {clean_title} from {wiki}: {e}")
    return None

def download_and_frame(url: str, referer: str, dest_path: Path) -> bool:
    h = HEADERS.copy()
    if referer:
        h['Referer'] = referer
    try:
        r = requests.get(url, headers=h, timeout=12)
        if r.status_code != 200 or len(r.content) < 5000:
            print(f"Failed download: status {r.status_code}, len {len(r.content)}")
            return False
        im = Image.open(BytesIO(r.content)).convert('RGB')
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        framed = create_full_panel_frame(im, 1080, 1920)
        framed.save(dest_path, "JPEG", quality=95)
        print(f"Saved: {dest_path.name} ({dest_path.stat().st_size // 1024} KB)")
        return True
    except Exception as e:
        print(f"Error saving {dest_path}: {e}")
        return False
