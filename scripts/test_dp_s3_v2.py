import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "deadpool_wolverine_corea_del_norte"

txt3 = "Decidido a irrumpir en el campamento, Deadpool empuñó sus armas y preparó su ofensiva armada listo para la acción."
res3 = verify_visual_alignment_with_gemini(str(dest_dir / "scene_03.jpg"), txt3)
print("Scene 3 audit:", res3)
