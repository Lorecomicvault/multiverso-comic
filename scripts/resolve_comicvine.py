import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE7mvh4JYCd0fb9WMj6Z0gS6mAbyQThTVrcLEP5ZAMco2VZ-lznavxO55Vbd8NYZYweA0u4M0W2u2J4M4N_DOy83k2wyF1VDBhCnw0UO_nkWsWB1Uf7L7xa5AEbIT6IFc0vAXGYy_5CyrU=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFLFlk5crJuEF-N7nAHS4atrNTRg0id6FapXRMtfcWpke9Rm87i2twlk3FY533VOz54hQ4vZ2F9nQ1bsX-M5ZEgJ7jblWHzG1KVbuQGF5GTAZS1VY-7MpXik8xeP9Dh3hNhwdtOrosT4SMCFj3mCK2eYMaOrzw-ZKHhFoMW4BLE-6XaVPGKGQ=="
]

for u in urls:
    r = requests.get(u, allow_redirects=False, timeout=10)
    target = r.headers.get('Location', '')
    print("Target:", target)
    if target:
        r2 = requests.get(target, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        imgs = re.findall(r'src=["\']([^"\']+)["\']', r2.text)
        for img in imgs:
            if any(k in img.lower() for k in ['comicvine', 'gamespot', 'uploads']):
                print("  Img:", img)
