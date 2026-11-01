import sys
import requests
from io import BytesIO
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

for name in ['daredevil11', 'daredevil12', 'daredevil13', 'daredevil14', 'daredevil15', 'daredevil16']:
    url = f"https://atomicjunkshop.com/wp-content/uploads/2020/05/{name}.jpg"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    if r.status_code == 200:
        im = Image.open(BytesIO(r.content))
        print(f"Success: {name}.jpg -> size {im.size}, bytes {len(r.content)}")
    else:
        print(f"Failed {name}.jpg: {r.status_code}")
