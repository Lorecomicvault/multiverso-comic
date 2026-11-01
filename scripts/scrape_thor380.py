import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://scans-daily.dreamwidth.org/1945775.html"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
imgs = re.findall(r'src=["\']([^"\']+)["\']', r.text)
for img in imgs:
    if any(ext in img.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
        if not any(bad in img.lower() for bad in ['silk', 'avatar', 'icon', 'button', 'statcounter', 'banner']):
            print(img)
