import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'dc.fandom.com'
for cat in ["Batman Vol 2 13/Images", "Batman Vol 2 14/Images", "Batman Vol 2 17/Images", "Detective Comics Vol 2 1/Images"]:
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
    members = [m.get("title") for m in r.get("query", {}).get("categorymembers", [])]
    print(f"=== {cat} ({len(members)}) ===")
    for m in members:
        print(" ", m)
