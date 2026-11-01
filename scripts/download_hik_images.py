import requests
from PIL import Image
from io import BytesIO

urls = [
    ('ww_hik_1424.jpg', 'https://deaconsden.wordpress.com/wp-content/uploads/2018/09/img_1424.jpg'),
    ('ww_hik_1444.jpg', 'https://deaconsden.wordpress.com/wp-content/uploads/2018/09/img_1444.jpg'),
    ('ww_hik_1430.jpg', 'https://deaconsden.wordpress.com/wp-content/uploads/2018/09/img_1430.jpg'),
]

headers = {'User-Agent': 'Mozilla/5.0'}
for fname, u in urls:
    r = requests.get(u, headers=headers)
    print(f"Downloaded {fname}: status {r.status_code}, {len(r.content)} bytes")
    im = Image.open(BytesIO(r.content)).convert('RGB')
    im.save(fname, quality=95)
    print(f"  Saved {fname}, size: {im.size}")
