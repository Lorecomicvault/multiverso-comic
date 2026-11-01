import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'marvel.fandom.com'
url = f"https://{wiki}/api.php"
params = {
    "action": "query",
    "list": "search",
    "srsearch": "Daredevil Vol 2 Maleev Kingpin",
    "srnamespace": 6,
    "srlimit": 30,
    "format": "json"
}
r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
for res in r.get("query", {}).get("search", []):
    print("  ", res.get("title"))
