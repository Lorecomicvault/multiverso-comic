import sys
import requests
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

SEARCHES = [
    {
        "id": "01_red_hulk",
        "wiki": "marvel.fandom.com",
        "queries": [
            "Hulk Vol 2 4",
            "Hulk Vol 2 5",
            "Thaddeus Ross Uatu",
            "Red Hulk Thor",
            "Red Hulk Watcher",
            "Mjolnir Red Hulk"
        ],
        "categories": [
            "Hulk Vol 2 4/Images",
            "Hulk Vol 2 5/Images"
        ]
    },
    {
        "id": "02_wolverine",
        "wiki": "marvel.fandom.com",
        "queries": [
            "Wolverine Vol 3 72",
            "Giant-Size Old Man Logan",
            "Johann Shmidt Earth-807128",
            "James Howlett Earth-807128",
            "Red Skull Old Man Logan"
        ],
        "categories": [
            "Wolverine Vol 3 72/Images",
            "Giant-Size Old Man Logan Vol 1 1/Images"
        ]
    },
    {
        "id": "03_hal_jordan",
        "wiki": "dc.fandom.com",
        "queries": [
            "Green Lantern Vol 3 48",
            "Green Lantern Vol 3 49",
            "Green Lantern Vol 3 50",
            "Emerald Twilight",
            "Hal Jordan Parallax",
            "Sinestro Green Lantern Vol 3 50"
        ],
        "categories": [
            "Green Lantern Vol 3 48/Images",
            "Green Lantern Vol 3 49/Images",
            "Green Lantern Vol 3 50/Images"
        ]
    },
    {
        "id": "04_spiderman",
        "wiki": "marvel.fandom.com",
        "queries": [
            "Amazing Spider-Man Vol 1 269",
            "Amazing Spider-Man Vol 1 270",
            "Pyreus Kril Amazing Spider-Man",
            "Firelord Spider-Man"
        ],
        "categories": [
            "Amazing Spider-Man Vol 1 269/Images",
            "Amazing Spider-Man Vol 1 270/Images"
        ]
    },
    {
        "id": "05_daredevil",
        "wiki": "marvel.fandom.com",
        "queries": [
            "Daredevil Vol 2 50",
            "King of Hell's Kitchen",
            "Wilson Fisk Daredevil Vol 2 50"
        ],
        "categories": [
            "Daredevil Vol 2 50/Images"
        ]
    },
    {
        "id": "06_joker",
        "wiki": "dc.fandom.com",
        "queries": [
            "Batman Vol 2 13",
            "Batman Vol 2 14",
            "Batman Vol 2 15",
            "Batman Vol 2 16",
            "Batman Vol 2 17"
        ],
        "categories": [
            "Batman Vol 2 13/Images",
            "Batman Vol 2 14/Images",
            "Batman Vol 2 15/Images",
            "Batman Vol 2 16/Images",
            "Batman Vol 2 17/Images"
        ]
    },
    {
        "id": "07_punisher",
        "wiki": "marvel.fandom.com",
        "queries": [
            "The Punisher Vol 5 1",
            "Welcome Back Frank 1"
        ],
        "categories": [
            "The Punisher Vol 5 1/Images"
        ]
    },
    {
        "id": "08_superman",
        "wiki": "dc.fandom.com",
        "queries": [
            "Justice League Vol 4 25",
            "World Forger Prime Earth",
            "Superman World Forger"
        ],
        "categories": [
            "Justice League Vol 4 25/Images"
        ]
    },
    {
        "id": "09_thor",
        "wiki": "marvel.fandom.com",
        "queries": [
            "Thor Vol 1 380",
            "Midgard Serpent Thor",
            "Jormungand Earth-616"
        ],
        "categories": [
            "Thor Vol 1 380/Images"
        ]
    },
    {
        "id": "10_flash",
        "wiki": "dc.fandom.com",
        "queries": [
            "Crisis on Infinite Earths Vol 1 8",
            "Barry Allen Earth-One Crisis"
        ],
        "categories": [
            "Crisis on Infinite Earths Vol 1 8/Images"
        ]
    }
]

def search_files(wiki, query, limit=10):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 6,
        "srlimit": limit,
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        return [res.get("title") for res in r.get("query", {}).get("search", [])]
    except Exception as e:
        return []

def search_cat(wiki, cat, limit=25):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{cat}",
        "cmnamespace": 6,
        "cmlimit": limit,
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5).json()
        return [m.get("title") for m in r.get("query", {}).get("categorymembers", [])]
    except Exception as e:
        return []

results_all = {}
for item in SEARCHES:
    sid = item["id"]
    wiki = item["wiki"]
    print(f"Searching {sid}...", flush=True)
    found = set()
    for cat in item["categories"]:
        found.update(search_cat(wiki, cat))
    for q in item["queries"]:
        found.update(search_files(wiki, q))
    results_all[sid] = list(found)
    print(f"[{sid}] Found {len(found)} candidate images from {wiki}", flush=True)
    for title in sorted(found)[:5]:
        print(f"   {title}", flush=True)

with open("batch_2_discovered_files.json", "w", encoding="utf-8") as f:
    json.dump(results_all, f, indent=2, ensure_ascii=False)
print("\nSaved batch_2_discovered_files.json", flush=True)
