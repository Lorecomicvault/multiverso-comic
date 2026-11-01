import sys
from pathlib import Path
from PIL import Image

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the atomicjunkshop article text around these images to know exactly which comic page each represents!
import requests, re
url = "https://atomicjunkshop.com/your-bendis-maleev-daredevil-timeline/"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
for match in re.finditer(r'<img[^>]+src=["\']([^"\']+daredevil\d+\.jpg)["\'][^>]*>', r.text):
    start = max(0, match.start() - 200)
    end = min(len(r.text), match.end() + 200)
    print("Match:", match.group(1))
    print("Context:", re.sub(r'<[^>]+>', ' ', r.text[start:end])[:250].strip())
    print("-" * 50)
