import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Search comicvine for issue 50
url = "https://comicvine.gamespot.com/api/search/?api_key=... " # We don't have api key, but we can scrape the HTML page:
# Let's check google search for comicvine issue url:
url2 = "https://comicvine.gamespot.com/daredevil-50-hardcore-part-5/4000-92892/"
r = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=10)
print("Status:", r.status_code)
imgs = re.findall(r'https://comicvine\.gamespot\.com/a/uploads/[^"\']+', r.text)
for img in set(imgs):
    print("CV img:", img)
