import requests

def search_cat(cat):
    url = "https://marvel.fandom.com/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{cat}",
        "cmnamespace": 6,
        "cmlimit": 50,
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    members = r.get("query", {}).get("categorymembers", [])
    print(f"Category:{cat} -> {len(members)} files:")
    for m in members:
        print("  ", m.get("title"))
    return members

for issue in [15, 16, 17, 18, 19]:
    search_cat(f"Deadpool Vol 4 {issue}/Images")
