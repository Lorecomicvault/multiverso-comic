import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "lobo_expulsado_cielo_infierno"

txt1 = "En un duelo sangriento e implacable a través del cosmos, Lobo, el cazarrecompensas más brutal de la galaxia, arrasó con sus enemigos en un combate cuerpo a cuerpo feroz."
res1 = verify_visual_alignment_with_gemini(str(dest_dir / "scene_01.jpg"), txt1)
print("Scene 1 audit:", res1)

txt4 = "Expulsado para siempre del Más Allá y devuelto a la vida, Lobo desató una masacre salvaje aplastando a sus enemigos con una furia indestructible."
res4 = verify_visual_alignment_with_gemini(str(dest_dir / "scene_04.jpg"), txt4)
print("Scene 4 audit:", res4)
