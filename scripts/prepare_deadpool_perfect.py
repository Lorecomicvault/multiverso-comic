import sys
from PIL import Image
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.cloud_runner import create_full_panel_frame

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "deadpool_wolverine_corea_del_norte"
dest_dir.mkdir(parents=True, exist_ok=True)

# Scene 3: Frame dp_p07.jpg
im3 = Image.open('dp_p07.jpg').convert('RGB')
f3 = create_full_panel_frame(im3, 1080, 1920)
f3.save(dest_dir / 'scene_03.jpg', quality=95)

def get_rms(p1, p2):
    i1 = np.array(Image.open(p1).convert('RGB').resize((128, 128)), dtype=float)
    i2 = np.array(Image.open(p2).convert('RGB').resize((128, 128)), dtype=float)
    return np.sqrt(np.mean((i1 - i2) ** 2))

for i in range(1, 5):
    for j in range(i + 1, 5):
        p1 = dest_dir / f"scene_{i:02d}.jpg"
        p2 = dest_dir / f"scene_{j:02d}.jpg"
        rms = get_rms(p1, p2)
        print(f"RMS Scene {i} vs Scene {j}: {rms:.2f}", flush=True)

print("Deadpool 4 panels fully prepared!", flush=True)
