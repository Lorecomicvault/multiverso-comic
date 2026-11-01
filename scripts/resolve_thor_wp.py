import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGRvqYkgVwE_O_Man8BxV2lRm06AxXiH9mhhLcBSFi894wxbmncQmbg1valNC4f9bKlyQJi57kOs_vzFqj3Ja5iVAlDdIFKyIHzlsfnlAeDo3_E3r7AfSI_gMNsNppyHBywD4Qd0Ct7GetAxnDoas00Z9d4hn_b5DgtlN4naN_gE84aX5Kzp7NxAZqd62jV4Q4poPbBOaY="
r = requests.get(url, allow_redirects=False, timeout=10)
target = r.headers.get('Location', '')
print("Target URL:", target)

if target:
    r2 = requests.get(target, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    imgs = re.findall(r'src=["\']([^"\']+)["\']', r2.text)
    for img in imgs:
        if any(k in img.lower() for k in ['thor', '380', 'simonson', 'serpent', 'midgard', 'jormungand', 'wp-content']):
            print("Found img:", img)
