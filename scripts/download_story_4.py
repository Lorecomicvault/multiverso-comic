import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "04_spiderman_noquea_firelord_heraldo_galactus"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pics = [
    ("raw_s1.jpg", "https://pics.livejournal.com/starwolf_oakley/pic/005pxt2y"),
    ("raw_s2.jpg", "https://pics.livejournal.com/starwolf_oakley/pic/005pzg27"),
    ("raw_s3.jpg", "https://pics.livejournal.com/starwolf_oakley/pic/005py7d2"),
    ("raw_s4.jpg", "https://pics.livejournal.com/starwolf_oakley/pic/005q0ff7")
]

for filename, url in pics:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content)).convert('RGB')
        im.save(OUT_DIR / filename, quality=95)
        print(f"Saved {filename}: {im.size} from {url}")
    else:
        print(f"Failed {url}: status {r.status_code}")

print("Done Story 4 downloads.")
