import requests

def search_files(wiki, query):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 6,
        "srlimit": 20,
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    data = r.json()
    results = data.get("query", {}).get("search", [])
    print(f"[{wiki}] Search '{query}' -> {len(results)} results:")
    for res in results:
        print("  ", res.get("title"))
    return results

search_files("dc.fandom.com", "Hiketeia")
search_files("dc.fandom.com", "Danielle Wellys")
search_files("dc.fandom.com", "Lobo's Back")
search_files("dc.fandom.com", "Lobo Hell")
search_files("dc.fandom.com", "Lobo Heaven")
