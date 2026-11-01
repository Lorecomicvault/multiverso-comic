import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "09_thor_muerte_serpiente_midgard_nueve_pasos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pics = [
    ("raw_1.jpg", "https://p2.dreamwidth.org/bb5a8a1dfe0d/172314-1945775/i49.tinypic.com/dwrkgi.jpg"),
    ("raw_2.jpg", "https://p2.dreamwidth.org/47d0c47539d1/172314-1945775/i50.tinypic.com/5vatz6.jpg"),
    ("raw_3.jpg", "https://p2.dreamwidth.org/c23a81b6d2a4/172314-1945775/i49.tinypic.com/292l8gz.jpg"),
    ("raw_4.jpg", "https://p2.dreamwidth.org/f8f942f311b1/172314-1945775/i47.tinypic.com/2qlfl3s.jpg"),
    ("raw_5.jpg", "https://p2.dreamwidth.org/a6ca65c3c8fa/172314-1945775/i50.tinypic.com/30rp26g.jpg"),
    ("raw_6.jpg", "https://p2.dreamwidth.org/b3cd29a3ec10/172314-1945775/i50.tinypic.com/s41eah.jpg"),
    ("raw_7.jpg", "https://p2.dreamwidth.org/effabf5cc150/172314-1945775/i50.tinypic.com/wjj7s7.jpg"),
    ("raw_8.jpg", "https://p2.dreamwidth.org/e0037be11308/172314-1945775/i46.tinypic.com/9h3vd4.jpg")
]

for filename, url in pics:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content)).convert('RGB')
        im.save(OUT_DIR / filename, quality=95)
        print(f"Saved {filename}: {im.size}")
    else:
        print(f"Failed {url}: status {r.status_code}")

print("Done Story 9 downloads.")
