import requests

def search_category(wiki, cat_title):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{cat_title}",
        "cmnamespace": 6,
        "cmlimit": 50,
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    data = r.json()
    members = data.get("query", {}).get("categorymembers", [])
    print(f"[{wiki}] Category:{cat_title} -> {len(members)} files found:")
    for m in members[:15]:
        print("  ", m.get("title"))
    return members

print("Searching categories:")
search_category("dc.fandom.com", "Wonder Woman: The Hiketeia/Images")
search_category("dc.fandom.com", "Wonder Woman: The Hiketeia")
search_category("marvel.fandom.com", "Deadpool Vol 3 15/Images")
search_category("marvel.fandom.com", "Deadpool Vol 3 16/Images")
search_category("marvel.fandom.com", "Deadpool Vol 3 17/Images")
search_category("marvel.fandom.com", "Deadpool Vol 3 18/Images")
search_category("marvel.fandom.com", "Deadpool Vol 3 19/Images")
search_category("dc.fandom.com", "Lobo's Back Vol 1 1/Images")
search_category("dc.fandom.com", "Lobo's Back Vol 1 2/Images")
search_category("dc.fandom.com", "Lobo's Back Vol 1 3/Images")
search_category("dc.fandom.com", "Lobo's Back Vol 1 4/Images")
