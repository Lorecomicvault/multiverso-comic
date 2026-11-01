import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'dc.fandom.com'
url = f"https://{wiki}/api.php"
params = {
    "action": "query",
    "titles": "Alpheus_(Sixth_Dimension)",
    "prop": "images",
    "imlimit": 50,
    "format": "json"
}
r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
pages = r.get("query", {}).get("pages", {})
for p in pages.values():
    for img in p.get("images", []):
        print(" ", img.get("title"))
