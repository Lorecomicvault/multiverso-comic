import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = Path(r"C:\Users\Vanes\comics en espanol\assets\curated_panels\08_superman_vuela_seis_soles_noquea_world_forger")
OUT_DIR.mkdir(parents=True, exist_ok=True)

u1 = "https://i0.wp.com/databasecomics.com/wp-content/uploads/justiceleague201925str2.png"
r = requests.get(u1, headers={'User-Agent': 'Mozilla/5.0'})
im = Image.open(BytesIO(r.content))
im.save(OUT_DIR / "punch_panel.png")
print("Saved punch_panel.png:", im.size)
