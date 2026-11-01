import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGiuLQClP1LPN6bK6w6A4uyKj91Tom4PpIMVS2leOHwjTBxAORyo4zMJz61HaNVWZqA8TWcexUOCT8zu9z4izkyTfMJ9dFRqMEQyCX7QLRbiLfdf-PS7SW8E_eVw4qG6HvL-tuPduX3hkIuVZsp3SmN9IF8FDwjyM1b8k_x6SBwKZ0fTd7JpqtFYHy5vM__ZjEFTZlV"
r = requests.get(url, allow_redirects=False, timeout=10)
target = r.headers.get('Location', '')
print("Target:", target)

if target:
    r2 = requests.get(target, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    imgs = re.findall(r'src=["\']([^"\']+)["\']', r2.text)
    for img in imgs:
        if any(ext in img.lower() for ext in ['.jpg', '.png', '.jpeg']):
            print("Img:", img)
