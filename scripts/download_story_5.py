import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "05_daredevil_nuevo_rey_del_crimen_hells_kitchen"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pics = [
    ("raw_p10.jpg", "https://abload.de/img/daredevilv2050-010vdqqh.jpg"),
    ("raw_p14.jpg", "https://abload.de/img/daredevilv2050-014aopvt.jpg"),
    ("raw_p21.jpg", "https://abload.de/img/daredevilv2050-0211cqna.jpg"),
    ("raw_p23.jpg", "https://abload.de/img/daredevilv2050-023ykoje.jpg"),
    ("raw_p24.jpg", "https://abload.de/img/daredevilv2050-024sfq3w.jpg")
]

for filename, url in pics:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content)).convert('RGB')
        im.save(OUT_DIR / filename, quality=95)
        print(f"Saved {filename}: {im.size} from {url}")
    else:
        print(f"Failed {url}: status {r.status_code}")

print("Done Story 5 downloads.")
