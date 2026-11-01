import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'marvel.fandom.com'
queries = [
    'Daredevil Kingpin pool table',
    'Hardcore Daredevil',
    'King of Hell\'s Kitchen',
    'Daredevil 50',
    'Wilson Fisk Daredevil Vol 2 50',
    'Matthew Murdock Daredevil Vol 2 50'
]

for q in queries:
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": q,
        "srnamespace": 6,
        "srlimit": 10,
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    print(f"=== Query: {q} ===")
    for res in r.get("query", {}).get("search", []):
        print("  ", res.get("title"))
