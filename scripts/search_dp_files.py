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
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    results = r.get("query", {}).get("search", [])
    print(f"Search '{query}' -> {len(results)} files:")
    for res in results:
        print("  ", res.get("title"))
    return results

search_files("marvel.fandom.com", "The Good, the Bad and the Ugly")
search_files("marvel.fandom.com", "Butler Earth-616")
search_files("marvel.fandom.com", "Bartol Utler")
search_files("marvel.fandom.com", "Deadpool Vol 3 17")
search_files("marvel.fandom.com", "Deadpool Vol 3 18")
search_files("marvel.fandom.com", "Deadpool Vol 3 19")
