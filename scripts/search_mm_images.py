import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://marvel.fandom.com/api.php"
params = {
    'action': 'query',
    'titles': 'Matthew Murdock (Earth-616)',
    'prop': 'images',
    'imlimit': 200,
    'format': 'json'
}
r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
pages = r.get('query', {}).get('pages', {})
for pid, pdata in pages.items():
    for img in pdata.get('images', []):
        t = img['title']
        if any(k in t.lower() for k in ['50', 'fisk', 'kingpin', 'maleev', 'hardcore']):
            print(t)
