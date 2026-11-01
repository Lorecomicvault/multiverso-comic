import sys
from pathlib import Path
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "05_daredevil_nuevo_rey_del_crimen_hells_kitchen"

for p in sorted(OUT_DIR.glob("*.jpg")):
    if p.name.startswith("scene_"):
        continue
    im = Image.open(p)
    print(f"{p.name}: size={im.size}, aspect={im.width/im.height:.2f}")
