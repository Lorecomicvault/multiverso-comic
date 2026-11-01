import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.reddit.com/r/Thor/comments/1rw32md/thor_vs_jormungandr_full_fight_thor_1966_380/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get(url, headers=headers)
print("Status:", r.status_code)
# Find all preview.redd.it or i.redd.it
matches = set(re.findall(r'https?://(?:i\.redd\.it|preview\.redd\.it)/[^\s"\'<>&]+', r.text))
print(f"Found {len(matches)} matches:")
for m in sorted(matches):
    print(" ", m)
