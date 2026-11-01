import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = 'https://old.reddit.com/r/Marvel/comments/1vcbbq/the_hulk_lifts_thors_hammer/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers)
print('Status:', r.status_code)
matches = set(re.findall(r'https?://[^\s"\'<>]+(?:imgur\.com|i\.redd\.it)[^\s"\'<>]+', r.text))
for m in matches:
    print(' ', m)
