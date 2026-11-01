import sys
from pathlib import Path
from PIL import Image
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "05_daredevil_nuevo_rey_del_crimen_hells_kitchen"

TARGET_W, TARGET_H = 1080, 1920

def create_vertical_panel(img_path, focus='center'):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    target_ratio = TARGET_W / TARGET_H
    current_ratio = w / h

    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        cropped = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = 0 if focus == 'top' else ((h - new_h) // 2)
        cropped = img.crop((0, top, w, top + new_h))
    return cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

scenes_spec = [
    ("scene_01.jpg", OUT_DIR / "dd50_cover.jpg", 'top'),
    ("scene_02.jpg", OUT_DIR / "daredevil14.jpg", 'center'),
    ("scene_03.jpg", OUT_DIR / "daredevil15.jpg", 'center'),
    ("scene_04.jpg", OUT_DIR / "daredevil16.jpg", 'center')
]

scenes = []
for out_name, src_path, focus in scenes_spec:
    panel = create_vertical_panel(src_path, focus)
    out_file = OUT_DIR / out_name
    panel.save(out_file, quality=95)
    scenes.append(panel)
    print(f"Generated {out_name}: {panel.size}")

print("\n--- Verifying Pairwise RMS Difference Quality Gate (Must all be > 12.0) ---")
passed = True
for i in range(len(scenes)):
    for j in range(i + 1, len(scenes)):
        arr1 = np.array(scenes[i], dtype=np.float32)
        arr2 = np.array(scenes[j], dtype=np.float32)
        rms = np.sqrt(np.mean((arr1 - arr2) ** 2))
        print(f"RMS diff Scene {i+1} vs Scene {j+1}: {rms:.2f}")
        if rms < 12.0:
            print(f"FATAL ERROR: Scene {i+1} and Scene {j+1} are too similar (RMS < 12.0)!")
            passed = False

if passed:
    print("\nSUCCESS: All 4 scenes for Daredevil #50 verified and passed Quality Gate!")
else:
    sys.exit(1)
