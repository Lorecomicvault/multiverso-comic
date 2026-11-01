import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = Path(r"C:\Users\Vanes\comics en espanol\assets\curated_panels\08_superman_vuela_seis_soles_noquea_world_forger")
OUT_DIR.mkdir(parents=True, exist_ok=True)

urls = [
    ("str1.jpeg", "https://i0.wp.com/databasecomics.com/wp-content/uploads/2021/06/justiceleague201925str1.jpeg"),
    ("str2.jpeg", "https://i0.wp.com/databasecomics.com/wp-content/uploads/2021/06/justiceleague201925str2.jpeg"),
    ("chi.jpg", "https://i0.wp.com/databasecomics.com/wp-content/uploads/2021/06/supermanprimeearthchi.jpg")
]

for fname, u in urls:
    r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'})
    im = Image.open(BytesIO(r.content))
    im.save(OUT_DIR / fname)
    print(f"Saved {fname}: {im.size}")
