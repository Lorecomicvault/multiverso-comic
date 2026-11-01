import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFUgCEWLTl41hDRlt7AXV2_-iFkmbJSmrGFOSejkMcz91Qp4ESLnNFmQTwVv1GEJwcWCTG9P2PiblEMdnwOk1Y8XrHulZf3JvI2WbqPdwPIFV3yimMPIOgMBgp6TiAstVXQWg==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH8KuO_GsXFtx191YKGWSckQtucs84F4MoKbXddjQeeAU5eLK5iYqJeWP37BPkeQyhlHc1RKMgCg691EW6bylF5UG_XJb8wx04MS8F0k_OLS6FNIdnT6CJ_r5B-yZWH8fJqz2x6nUcmSLfYTrsb6IwyEv5kpwwXQSZSkhB5"
]

for u in urls:
    try:
        r = requests.get(u, allow_redirects=False, timeout=10)
        target = r.headers.get('Location', '')
        print("Target:", target)
        if target:
            r2 = requests.get(target, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            imgs = re.findall(r'src=["\']([^"\']+)["\']', r2.text)
            for img in imgs:
                if any(k in img.lower() for k in ['daredevil', 'kingpin', 'fisk', 'maleev', 'hardcore', '50']):
                    print("  Img:", img)
    except Exception as e:
        print("Error:", e)
