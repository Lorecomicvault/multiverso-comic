import requests, re
from PIL import Image
from io import BytesIO

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
q = 'Wonder Woman The Hiketeia Batman rain panel'
url = f'https://www.bing.com/images/search?q={requests.utils.quote(q)}&FORM=HDRSC2'
r = requests.get(url, headers=headers)
m = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', r.text)
print(f"Found {len(m)} candidate images:")
for u in m[:10]:
    print(u)
