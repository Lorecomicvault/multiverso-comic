import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'marvel.fandom.com'
for issue in [46, 47, 48, 49, 50, 56, 57]:
    cat = f"Daredevil Vol 2 {issue}/Images"
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{cat}",
        "cmnamespace": 6,
        "cmlimit": 20,
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    members = [m.get("title") for m in r.get("query", {}).get("categorymembers", [])]
    print(f"Daredevil Vol 2 {issue} -> {len(members)} images:")
    for m in members[:5]:
        print("  ", m)
