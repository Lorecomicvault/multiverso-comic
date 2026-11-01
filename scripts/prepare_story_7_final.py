import sys
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "07_punisher_masacre_funeral_familia_mafia"

TARGET_W, TARGET_H = 1080, 1920

def create_vertical_panel(img_path, focus='center'):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    target_ratio = TARGET_W / TARGET_H
    current_ratio = w / h

    # If the image is already portrait and reasonably close to 9:16
    if current_ratio <= target_ratio * 1.3:
        # Standard crop/fill
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            cropped = img.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = 0 if focus == 'top' else ((h - new_h) // 2)
            cropped = img.crop((0, top, w, top + new_h))
        return cropped.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    else:
        # Very wide panel (e.g. panoramic cemetery shot):
        # Create a cinematic blurred background + crisp centered sharp foreground
        bg = img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(radius=25))
        # Darken bg slightly
        bg_arr = np.array(bg, dtype=np.float32) * 0.45
        bg = Image.fromarray(bg_arr.astype(np.uint8))
        
        # Scale foreground to fit width
        fg_w = TARGET_W
        fg_h = int(h * (TARGET_W / w))
        fg = img.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
        
        # Paste centered
        y_offset = (TARGET_H - fg_h) // 2
        bg.paste(fg, (0, y_offset))
        return bg

scenes_spec = [
    ("scene_01.jpg", OUT_DIR / "punisher_cover_textless.jpg", 'top'),
    ("scene_02.jpg", OUT_DIR / "gnucci_family.png", 'center'),
    ("scene_03.jpg", OUT_DIR / "frank_castle_sniper.jpg", 'top'),
    ("scene_04.jpg", OUT_DIR / "carlo_gnucci.jpg", 'center')
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
    print("\nSUCCESS: All 4 scenes for Punisher #1 verified and passed Quality Gate!")
else:
    sys.exit(1)
