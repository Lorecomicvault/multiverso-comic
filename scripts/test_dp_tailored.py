import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "deadpool_wolverine_corea_del_norte"

txt3 = "Para defender el campamento secreto a cualquier precio, el ejército norcoreano desplegó un batallón de soldados custodiando las instalaciones militares."
res3 = verify_visual_alignment_with_gemini(str(dest_dir / "scene_03.jpg"), txt3)
print("Scene 3 audit:", res3)

txt4 = "En el interior del complejo liberado, el Capitán América y Deadpool contemplaron el desenlace de la misión, confrontando la tragedia de los experimentos mutantes."
res4 = verify_visual_alignment_with_gemini(str(dest_dir / "scene_04.jpg"), txt4)
print("Scene 4 audit:", res4)
