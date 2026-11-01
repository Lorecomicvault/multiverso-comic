import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'marvel.fandom.com'
queries = [
    'Red Hulk Thor',
    'Thor Odinson Earth-616 Hulk Vol 2 5',
    'Mjolnir Hulk Vol 2 5',
    'Hulk Vol 2 5',
    'Thor Hulk Vol 2 5'
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
