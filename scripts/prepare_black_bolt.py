import os
import sys
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "blackbolt_bomba_t_falla_espacio"
dest_dir.mkdir(parents=True, exist_ok=True)

# Scene 1: Emperor Vulcan (10/10)
im1 = Image.open('test_vulcan_01.jpg').convert('RGB')
framed1 = create_full_panel_frame(im1, 1080, 1920)
framed1.save(dest_dir / 'scene_01.jpg', quality=95)

# Scene 2: Terrigen Bomb (10/10)
im2 = Image.open('test_wok_1.jpg').convert('RGB')
framed2 = create_full_panel_frame(im2, 1080, 1920)
framed2.save(dest_dir / 'scene_02.jpg', quality=95)

# Scene 3: Detonation / battle (10/10)
im3 = Image.open('test_wok_2.jpg').convert('RGB')
framed3 = create_full_panel_frame(im3, 1080, 1920)
framed3.save(dest_dir / 'scene_03.jpg', quality=95)

# Scene 4: The Fault cosmic tear (10/10)
im4 = Image.open('test_wok_3.jpg').convert('RGB')
framed4 = create_full_panel_frame(im4, 1080, 1920)
framed4.save(dest_dir / 'scene_04.jpg', quality=95)

print("Black Bolt 4 Curated 10/10 Panels saved successfully!", flush=True)
