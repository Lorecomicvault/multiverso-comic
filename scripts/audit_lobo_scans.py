import sys
PROJECT_ROOT = r"C:\Users\Vanes\comics en espanol"
sys.path.insert(0, PROJECT_ROOT)
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

for f in ['lobo_hell_01.jpg', 'lobo_heaven_02.jpg', 'lobo_back_03.jpg', 'lobo_back_04.jpg', 'lobo_heaven_song.jpg']:
    audit = verify_visual_alignment_with_gemini(f, "Lobo en el Infierno o Cielo o combatiendo o resucitando")
    print(f, "->", audit)
