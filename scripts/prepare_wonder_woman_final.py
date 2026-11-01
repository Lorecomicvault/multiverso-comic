import os
import sys
from io import BytesIO
from PIL import Image
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "wonderwoman_hiketeia_bota_batman"
dest_dir.mkdir(parents=True, exist_ok=True)

# 1. Erinyes
im1 = Image.open('test_ 001.jpg').convert('RGB')
create_full_panel_frame(im1, 1080, 1920).save(dest_dir / 'scene_01.jpg', quality=95)

# 2. Wonder Woman standing guard
im2 = Image.open('test_0046.jpg').convert('RGB')
create_full_panel_frame(im2, 1080, 1920).save(dest_dir / 'scene_02.jpg', quality=95)

# 3. Batman confronting in the rain / Gotham shadows (Batman 0641)
im3 = Image.open('test_batman_hiketeia_clean.jpg').convert('RGB')
create_full_panel_frame(im3, 1080, 1920).save(dest_dir / 'scene_03.jpg', quality=95)

# 4. Wonder Woman boot on Batman's face
im4 = Image.open('test_ww_04.jpg').convert('RGB')
create_full_panel_frame(im4, 1080, 1920).save(dest_dir / 'scene_04.jpg', quality=95)

print("All 4 frames created. Computing RMS differences...", flush=True)

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

print("RMS checks complete!", flush=True)
