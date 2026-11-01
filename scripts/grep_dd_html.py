import sys
import requests, re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://atomicjunkshop.com/your-bendis-maleev-daredevil-timeline/"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
for line in r.text.splitlines():
    if 'daredevil1' in line:
        print(line[:150])
