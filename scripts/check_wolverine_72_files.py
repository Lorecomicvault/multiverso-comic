import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'marvel.fandom.com'
cat = "Wolverine Vol 3 72/Images"
url = f"https://{wiki}/api.php"
params = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": f"Category:{cat}",
    "cmnamespace": 6,
    "cmlimit": 50,
    "format": "json"
}
r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
for m in r.get("query", {}).get("categorymembers", []):
    print(" ", m.get("title"))
