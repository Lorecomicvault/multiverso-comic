import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH4-T5_7Ozr7ArckeyjC3gN5418RRTf-Ti_Ac_kU7BsT8P-atKW4z_izhpqxJbG0-hJ01AY20NSV8U1psaqdUbrWEFMuJAlfgdu5GKBqh_0JMavQI5RnO1B1jj1o-Ol0BwLsRBMd32TBhk-8P_pFkyooQfqiZztMw=="
r = requests.get(url, allow_redirects=False, timeout=10)
target = r.headers.get('Location', '')
print("Target:", target)

if target:
    r2 = requests.get(target, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', r2.text)
    for img in imgs:
        if any(ext in img.lower() for ext in ['.jpg', '.png', '.jpeg']):
            print("Found:", img)
