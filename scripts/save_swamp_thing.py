import os
import sys
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "swampthing_leccion_anatomia_vegetal"
dest_dir.mkdir(parents=True, exist_ok=True)

# 1. test_st_1.jpg -> scene_01.jpg (10/10)
create_full_panel_frame(Image.open('test_st_1.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_01.jpg', quality=95)

# 2. test_st_2.jpg -> scene_02.jpg (10/10)
create_full_panel_frame(Image.open('test_st_2.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_02.jpg', quality=95)

# 3. test_st_3.jpg -> scene_03.jpg (10/10)
create_full_panel_frame(Image.open('test_st_3.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_03.jpg', quality=95)

# 4. test_st_14.jpg -> scene_04.jpg (10/10)
create_full_panel_frame(Image.open('test_st_14.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_04.jpg', quality=95)

print("Swamp Thing 4 Curated 10/10 Panels successfully saved!", flush=True)
