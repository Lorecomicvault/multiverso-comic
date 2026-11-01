import requests
from PIL import Image
from io import BytesIO

url = 'https://deaconsden.wordpress.com/wp-content/uploads/2018/09/4d85819f-9012-469e-96c3-7a7e8e256477-6873-000005793f0431ff1.jpg'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
im = Image.open(BytesIO(r.content)).convert('RGB')
im.save('ww_hik_danielle.jpg', quality=95)
print("Saved ww_hik_danielle.jpg, size:", im.size)

import sys
sys.path.insert(0, r"C:\Users\Vanes\comics en espanol")
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

res = verify_visual_alignment_with_gemini('ww_hik_danielle.jpg', 'Danielle o una mujer suplicando ante Wonder Woman o Diana en The Hiketeia')
print("Gemini audit:", res)
