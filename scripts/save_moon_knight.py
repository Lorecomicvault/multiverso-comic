import os
import sys
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "moonknight_mr_knight_edificio_rescate"
dest_dir.mkdir(parents=True, exist_ok=True)

# Scene 1: Mr Knight suit 1 (10/10)
create_full_panel_frame(Image.open('mk_suit1.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_01.jpg', quality=95)

# Scene 2: Mr Knight issue 5 (10/10)
create_full_panel_frame(Image.open('test_mk_01.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_02.jpg', quality=95)

# Scene 3: Mr Knight combat action (10/10)
create_full_panel_frame(Image.open('mk_suit2.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_03.jpg', quality=95)

# Scene 4: Scarlet rescued girl (10/10)
create_full_panel_frame(Image.open('mk_girl.jpg').convert('RGB'), 1080, 1920).save(dest_dir / 'scene_04.jpg', quality=95)

print("Moon Knight 4 Curated 10/10 Panels saved successfully!", flush=True)
