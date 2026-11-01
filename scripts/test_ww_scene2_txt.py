import sys
sys.path.insert(0, r"C:\Users\Vanes\comics en espanol")
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

test_txt = "Con su indumentaria de guerra y lista para el combate en las calles de la ciudad, Wonder Woman montó guardia implacable, decidida a frenar a quien intentara romper el juramento."
res = verify_visual_alignment_with_gemini(r"assets\curated_panels\wonderwoman_hiketeia_bota_batman\scene_02.jpg", test_txt)
print(res)
