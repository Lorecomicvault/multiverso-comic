import sys
from pathlib import Path
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

dd_dir = Path(r"C:\Users\Vanes\comics en espanol\assets\curated_panels\05_daredevil_nuevo_rey_del_crimen_hells_kitchen")
for p in sorted(dd_dir.glob("daredevil*.jpg")):
    im = Image.open(p)
    # let's save a smaller preview to inspect or check RMS
    print(f"{p.name}: size {im.size}, mode {im.mode}")
