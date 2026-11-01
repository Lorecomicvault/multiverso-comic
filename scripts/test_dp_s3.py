import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "deadpool_wolverine_corea_del_norte"

txt3 = "Lleno de una furia implacable, Deadpool tomó las armas y se lanzó a la batalla al frente del combate para arrasar el complejo militar."
res3 = verify_visual_alignment_with_gemini(str(dest_dir / "scene_03.jpg"), txt3)
print("Scene 3 audit:", res3)
