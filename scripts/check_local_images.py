from PIL import Image
import os
import sys

# inspect test_batman_074.jpg
im = Image.open('test_batman_074.jpg')
print(f"test_batman_074.jpg size: {im.size}, mode: {im.mode}")

# check if we can verify with Gemini
sys.path.insert(0, r"C:\Users\Vanes\comics en espanol")
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

res = verify_visual_alignment_with_gemini('test_batman_074.jpg', 'Batman llega bajo la lluvia o en la noche para confrontar a Wonder Woman')
print("Gemini response for test_batman_074.jpg:")
print(res)
