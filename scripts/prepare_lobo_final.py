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

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "lobo_expulsado_cielo_infierno"
dest_dir.mkdir(parents=True, exist_ok=True)

# 1. Lobo cosmic violent combat
im1 = Image.open('lobo_01_08.jpg').convert('RGB')
f1 = create_full_panel_frame(im1, 1080, 1920)
f1.save(dest_dir / 'scene_01.jpg', quality=95)

# 2. Lobo in Hell slaughtering demons
im2 = Image.open('lobo_hell_01.jpg').convert('RGB')
f2 = create_full_panel_frame(im2, 1080, 1920)
f2.save(dest_dir / 'scene_02.jpg', quality=95)

# 3. Lobo in Heaven causing total chaos
im3 = Image.open('lobo_heaven_02.jpg').convert('RGB')
f3 = create_full_panel_frame(im3, 1080, 1920)
f3.save(dest_dir / 'scene_03.jpg', quality=95)

# 4. Lobo rampage after expulsion
im4 = Image.open('lobo_back_04.jpg').convert('RGB')
f4 = create_full_panel_frame(im4, 1080, 1920)
f4.save(dest_dir / 'scene_04.jpg', quality=95)

print("All 4 frames saved for Lobo. Computing RMS differences...", flush=True)

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

print("\nVerifying with Gemini Vision:", flush=True)
texts = [
    "Tras desatar un combate salvaje en el cosmos, el alma de Lobo, el cazarrecompensas más violento del universo, cayó directamente a las puertas del Más Allá.",
    "Al llegar al Infierno, Lobo comenzó una sangrienta carnicería contra hordas de demonios, convirtiendo el averno en un caos absoluto hasta que el Diablo exigió su expulsión.",
    "Enviado de inmediato al Paraíso, Lobo profanó el santuario celestial, aterrorizando a los serafines y convirtiendo las nubes benditas en un campo de batalla.",
    "Desesperados por deshacerse de él, los líderes del Cielo y del Infierno le prohibieron la muerte para siempre, regresándolo a la vida como un inmortal indestructible."
]

for i, txt in enumerate(texts, 1):
    fpath = dest_dir / f"scene_{i:02d}.jpg"
    res = verify_visual_alignment_with_gemini(str(fpath), txt)
    print(f"Scene {i}: Score={res.get('score')}/10, Action={res.get('depicts_action')}", flush=True)
    print(f"  Reason: {res.get('reason')}", flush=True)
