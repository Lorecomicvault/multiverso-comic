import os
import sys
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "wonderwoman_hiketeia_bota_batman"
dest_dir.mkdir(parents=True, exist_ok=True)

# 1. Erinyes (10/10) - Scene 1 / 2
im1 = Image.open('test_ 001.jpg').convert('RGB')
create_full_panel_frame(im1, 1080, 1920).save(dest_dir / 'scene_01.jpg', quality=95)

# 2. Wonder Woman accepting / standing guard
im2 = Image.open('test_0046.jpg').convert('RGB')
create_full_panel_frame(im2, 1080, 1920).save(dest_dir / 'scene_02.jpg', quality=95)

# 3. Wonder Woman combat action
create_full_panel_frame(im2, 1080, 1920).save(dest_dir / 'scene_03.jpg', quality=95)

# 4. Boot on face (10/10)
im4 = Image.open('test_ww_04.jpg').convert('RGB')
create_full_panel_frame(im4, 1080, 1920).save(dest_dir / 'scene_04.jpg', quality=95)

scenes_texts = [
    "Bajo la mirada silenciosa de las temibles Erinias, los espíritus vengadores de la tragedia griega, una fugitiva desesperada acudió a Themyscira para invocar el antiguo ritual sagrado de Hiketeia.",
    "Al aceptar la súplica, Diana de Themyscira quedó atada por las leyes divinas del Olimpo a protegerla con su vida, sin importar quién viniera a reclamarla.",
    "Batman irrumpió en la noche exigiendo la custodia de la fugitiva para llevarla a Gotham, desatando un combate frontal implacable entre el intelecto y la fuerza divina.",
    "Demostrando la superioridad de su estirpe amazona, Diana esquivó sus ataques, derribó al Caballero de la Noche y colocó su bota firmemente sobre su rostro contra el pavimento."
]

print("AUDITING WONDER WOMAN SCENES:")
for i, txt in enumerate(scenes_texts, 1):
    fpath = dest_dir / f"scene_{i:02d}.jpg"
    res = verify_visual_alignment_with_gemini(str(fpath), txt)
    print(f"Scene {i}: Score={res.get('score')}/10, Action={res.get('depicts_action')}")
    print(f"  Reason: {res.get('reason')}")
