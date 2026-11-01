import sys
import requests, re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://atomicjunkshop.com/your-bendis-maleev-daredevil-timeline/"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
text = r.text

for i in range(1, 20):
    tag = f"daredevil{i}"
    idx = text.find(tag)
    if idx != -1:
        # find the preceding heading or text
        prev = text[max(0, idx-200):idx]
        print(f"daredevil{i}: {re.sub(r'<[^>]+>', ' ', prev).strip()}")
