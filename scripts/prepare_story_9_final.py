import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image, ImageOps
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "09_thor_muerte_serpiente_midgard_nueve_pasos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 1080, 1920

urls = {
    # Scene 1: La serpiente de Midgard se alza / Thor con armadura dorada
    "raw_scene_01.jpg": "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand001.jpg",
    # Scene 2: La batalla colosal / El choque apocalíptico de Mjolnir y relámpagos
    "raw_scene_02.jpg": "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand015.jpg",
    # Scene 3: El golpe demoledor que pulveriza a la serpiente cósmica
    "raw_scene_03.jpg": "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand022.jpg",
    # Scene 4: Los nueve pasos hacia el destino final / La armadura y el martillo
    "raw_scene_04.jpg": "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand025.jpg",
}

print("Downloading Thor #380 splash pages...")
for fname, u in urls.items():
    r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
    if r.status_code == 200:
        (OUT_DIR / fname).write_bytes(r.content)
        print(f"Saved {fname}: {len(r.content)} bytes")
    else:
        print(f"Failed {fname}: status {r.status_code}")

def format_panel_vertical(img_path):
    img = Image.open(img_path).convert('RGB')
    w, h = img.size
    
    # Target aspect ratio is 9:16 (0.5625)
    # If the image is standard comic page (~0.65), crop slightly from sides or pad top/bottom
    target_ratio = TARGET_W / TARGET_H
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        # Wider than 9:16 -> crop sides to keep center
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Taller than 9:16 -> crop top/bottom
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
        
    return img.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)

scenes = []
for i in range(1, 5):
    raw_path = OUT_DIR / f"raw_scene_{i:02d}.jpg"
    final_img = format_panel_vertical(raw_path)
    out_path = OUT_DIR / f"scene_{i:02d}.jpg"
    final_img.save(out_path, quality=95)
    scenes.append(final_img)
    print(f"Generated {out_path.name}: {final_img.size}")

# Pairwise RMS Difference Quality Gate
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
    print("\nSUCCESS: All 4 scenes for Thor #380 verified and passed Quality Gate!")
else:
    sys.exit(1)
