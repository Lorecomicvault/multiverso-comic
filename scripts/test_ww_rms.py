import sys
from PIL import Image
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.cloud_runner import create_full_panel_frame

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "wonderwoman_hiketeia_bota_batman"

# 1. Erinyes
im1 = Image.open('test_ 001.jpg').convert('RGB')
f1 = create_full_panel_frame(im1, 1080, 1920)
f1.save(dest_dir / 'scene_01.jpg', quality=95)

# 2. Wonder Woman standing guard
im2 = Image.open('test_0046.jpg').convert('RGB')
f2 = create_full_panel_frame(im2, 1080, 1920)
f2.save(dest_dir / 'scene_02.jpg', quality=95)

# 3. Wonder Woman overpowering Batman on the ground (ww_hik_1430.jpg)
im3 = Image.open('ww_hik_1430.jpg').convert('RGB')
f3 = create_full_panel_frame(im3, 1080, 1920)
f3.save(dest_dir / 'scene_03.jpg', quality=95)

# 4. Boot on Batman's face (ww_hik_1424.jpg)
im4 = Image.open('ww_hik_1424.jpg').convert('RGB')
f4 = create_full_panel_frame(im4, 1080, 1920)
f4.save(dest_dir / 'scene_04.jpg', quality=95)

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
