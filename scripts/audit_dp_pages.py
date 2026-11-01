import sys
PROJECT_ROOT = r"C:\Users\Vanes\comics en espanol"
sys.path.insert(0, PROJECT_ROOT)
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

for f in ['dp_p07.jpg', 'dp_p12.jpg']:
    audit = verify_visual_alignment_with_gemini(f, "Deadpool en combate, acción armada o asalto")
    print(f, "->", audit)
