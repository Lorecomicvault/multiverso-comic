import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://earthsmightiestblog.com/daredevil-46-50-426-430-2003-hardcore/"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
imgs = re.findall(r'src=["\']([^"\']+)["\']', r.text)
for img in imgs:
    if any(ext in img.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
        print(img)
