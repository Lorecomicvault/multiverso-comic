import sys
from pathlib import Path
from PIL import Image
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

dd_dir = Path(r"C:\Users\Vanes\comics en espanol\assets\curated_panels\05_daredevil_nuevo_rey_del_crimen_hells_kitchen")
for p in sorted(dd_dir.glob("*.jpg")):
    im = Image.open(p).convert('RGB')
    arr = np.array(im)
    print(f"{p.name}: mean {arr.mean():.1f}, std {arr.std():.1f}, min {arr.min()}, max {arr.max()}")
