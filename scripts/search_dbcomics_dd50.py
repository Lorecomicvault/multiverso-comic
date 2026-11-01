import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://databasecomics.com/?s=daredevil+50', headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
hrefs = re.findall(r'href=["\'](https://databasecomics\.com/[^"\']+)["\']', r.text)
for h in set(hrefs):
    print("Found link:", h)
