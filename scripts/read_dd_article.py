import sys
import requests, re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://atomicjunkshop.com/your-bendis-maleev-daredevil-timeline/"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
text = r.text
idx = text.find('daredevil11')
if idx != -1:
    print(re.sub(r'<[^>]+>', ' ', text[idx-800:idx+2500]))
