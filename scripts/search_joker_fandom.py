import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

wiki = 'dc.fandom.com'
queries = [
    'Joker face',
    'Death of the Family',
    'Batman Vol 2 13',
    'Batman Vol 2 17',
    'Dollmaker Detective Comics Vol 2 1',
    'Joker strapped'
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
