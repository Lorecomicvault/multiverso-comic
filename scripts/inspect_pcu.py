import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://popcultureuncovered.com/2016/03/11/weekend-coverage-daredevil-50/"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r.text)
for img in imgs:
    print(img)
