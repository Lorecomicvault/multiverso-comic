import sys
from PIL import Image

sys.path.insert(0, r"C:\Users\Vanes\comics en espanol")
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

for fname in ['ww_hik_1424.jpg', 'ww_hik_1430.jpg', 'ww_hik_1444.jpg']:
    audit = verify_visual_alignment_with_gemini(fname, "Wonder Woman combate con Batman o protege a Danielle o juramento")
    print(f"{fname}: Score={audit.get('score')}/10, Action={audit.get('depicts_action')}")
    print(f"  Reason: {audit.get('reason')}")
