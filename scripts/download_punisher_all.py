import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "07_punisher_masacre_funeral_familia_mafia"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def get_fandom_url(wiki, title):
    params = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url', 'format': 'json'}
    r = requests.get(f'https://{wiki}/api.php', params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    for p in r.get('query', {}).get('pages', {}).values():
        return p.get('imageinfo', [{}])[0].get('url')

files = [
    ('gnucci_family.png', 'File:Gnucci Crime Family (Earth-616) from Punisher Vol 5 1 001.png'),
    ('bruno_gnucci.jpg', 'File:Bruno (Gnucci Family) (Earth-616) from Punisher Vol 5 1 001.jpg'),
    ('edward_gnucci.jpg', 'File:Edward Gnucci in The Punisher Vol 5 1.jpg'),
    ('punisher_cover_textless.jpg', 'File:Punisher Vol 5 1 Textless.jpg')
]

for fname, title in files:
    u = get_fandom_url('marvel.fandom.com', title)
    if u:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://marvel.fandom.com/'})
        (OUT_DIR / fname).write_bytes(r.content)
        print(f"Saved {fname}, size: {len(r.content)}")
    else:
        print(f"URL not found for {title}")

print("Done Punisher downloads.")
