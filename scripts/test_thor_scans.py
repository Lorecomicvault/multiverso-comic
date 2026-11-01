import sys
from pathlib import Path
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand001.jpg",
    "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand005.jpg",
    "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand015.jpg",
    "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand022.jpg",
    "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand024.jpg",
    "https://marswillsendnomore.wordpress.com/wp-content/uploads/2011/08/simonson-thor-jormungand025.jpg",
]

for u in urls:
    r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content))
        print(f"Success: {u.split('/')[-1]} -> size {im.size}, bytes {len(r.content)}")
    else:
        print(f"Failed {u}: status {r.status_code}")
