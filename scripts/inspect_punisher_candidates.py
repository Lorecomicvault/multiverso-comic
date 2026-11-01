import sys
from pathlib import Path
import requests
from PIL import Image
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "07_punisher_masacre_funeral_familia_mafia"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

def get_fandom_url(wiki, title):
    params = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json'}
    r = requests.get(f'https://{wiki}/api.php', params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    for p in r.get('query', {}).get('pages', {}).values():
        return p.get('imageinfo', [{}])[0].get('url')

additional_files = [
    ('frank_castle_sniper.jpg', 'File:Francis Castle (Earth-616) from Punisher Vol 5 1 0001.jpg'),
    ('carlo_gnucci.jpg', 'File:Carlo Gnucci (Earth-616) from Punisher Vol 5 1 001.jpg')
]

for fname, title in additional_files:
    u = get_fandom_url('marvel.fandom.com', title)
    if u:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://marvel.fandom.com/'})
        (OUT_DIR / fname).write_bytes(r.content)
        print(f"Downloaded {fname}: {len(r.content)} bytes")

# Let's inspect all candidate images in the directory
print("\nInspecting candidates in folder:")
candidates = list(OUT_DIR.glob("*.*"))
for c in candidates:
    if c.name.startswith("scene_"):
        continue
    try:
        im = Image.open(c)
        print(f"  {c.name}: {im.size}, mode {im.mode}")
    except Exception as e:
        print(f"  {c.name}: error {e}")
