import requests
from io import BytesIO
from PIL import Image
import sys

PROJECT_ROOT = r"C:\Users\Vanes\comics en espanol"
sys.path.insert(0, PROJECT_ROOT)
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

url = 'https://static.wikia.nocookie.net/marvel_dc/images/3/33/Batman_0641.jpg'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://dc.fandom.com/'
}
r = requests.get(url, headers=headers)
im = Image.open(BytesIO(r.content)).convert('RGB')
im.save('test_batman_hiketeia_clean.jpg', quality=95)
print("Saved test_batman_hiketeia_clean.jpg, dimensions:", im.size)

audit = verify_visual_alignment_with_gemini('test_batman_hiketeia_clean.jpg', 'Batman irrumpe en la noche en Gotham o se enfrenta a Wonder Woman en The Hiketeia')
print("Gemini audit:")
print(audit)
