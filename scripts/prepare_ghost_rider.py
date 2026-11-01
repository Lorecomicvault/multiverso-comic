import os
import sys
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "ghostrider_asedio_cielo_zadkiel"
dest_dir.mkdir(parents=True, exist_ok=True)

# 1. Zadkiel on throne (10/10)
im1 = Image.open('test_l 6 30 0001.jpg').convert('RGB')
create_full_panel_frame(im1, 1080, 1920).save(dest_dir / 'scene_01.jpg', quality=95)

# 2. Army of Spirits of Vengeance (10/10)
im2 = Image.open('test_Vol 1 6 001.jpg').convert('RGB')
create_full_panel_frame(im2, 1080, 1920).save(dest_dir / 'scene_02.jpg', quality=95)

# 3. Hell-Driver Ghost Rider charging (10/10)
im3 = Image.open('test_l 6 33 0001.jpg').convert('RGB')
create_full_panel_frame(im3, 1080, 1920).save(dest_dir / 'scene_03.jpg', quality=95)

# 4. Celestial battle (10/10)
im4 = Image.open('test_ol 6 30 001.jpg').convert('RGB')
create_full_panel_frame(im4, 1080, 1920).save(dest_dir / 'scene_04.jpg', quality=95)

print("Ghost Rider 4 Curated 10/10 Panels saved successfully!", flush=True)
