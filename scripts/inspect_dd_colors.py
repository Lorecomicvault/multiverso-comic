import sys
from pathlib import Path
from PIL import Image
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "05_daredevil_nuevo_rey_del_crimen_hells_kitchen"

for p in sorted(OUT_DIR.glob("*.jpg")):
    if p.name.startswith("scene_"):
        continue
    im = Image.open(p).convert('RGB')
    arr = np.array(im)
    r_mean = arr[:, :, 0].mean()
    g_mean = arr[:, :, 1].mean()
    b_mean = arr[:, :, 2].mean()
    print(f"{p.name}: size={im.size}, R={r_mean:.1f}, G={g_mean:.1f}, B={b_mean:.1f}")
