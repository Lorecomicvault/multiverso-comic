import os
import sys
import json
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))

def search_fandom(wiki, query, limit=15):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 6, # File namespace
        "srlimit": limit,
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
        results = r.get("query", {}).get("search", [])
        return [res.get("title") for res in results]
    except Exception as e:
        print(f"Error searching {wiki} for {query}: {e}")
        return []

def search_category(wiki, cat, limit=20):
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
        r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
        members = r.get("query", {}).get("categorymembers", [])
        return [m.get("title") for m in members]
    except Exception as e:
        print(f"Error category {wiki} {cat}: {e}")
        return []

print("=== BUSCANDO VIÑETAS PARA EL NUEVO LOTE 2 ===\n")

# 1. Red Hulk (Hulk Vol 2 4 & 5)
print("1. Red Hulk vs Watcher & Thor:")
for title in search_category("marvel.fandom.com", "Hulk Vol 2 4/Images"):
    print("  ", title)
for title in search_category("marvel.fandom.com", "Hulk Vol 2 5/Images"):
    print("  ", title)

# 2. Wolverine Old Man Logan (Wolverine Vol 3 72 / Giant-Size Old Man Logan)
print("\n2. Old Man Logan vs Red Skull:")
for title in search_category("marvel.fandom.com", "Wolverine Vol 3 72/Images"):
    print("  ", title)
for title in search_fandom("marvel.fandom.com", "Old Man Logan Red Skull"):
    print("  ", title)

# 3. Hal Jordan Emerald Twilight (Green Lantern Vol 3 48, 49, 50)
print("\n3. Hal Jordan Emerald Twilight:")
for title in search_category("dc.fandom.com", "Green Lantern Vol 3 48/Images"):
    print("  ", title)
for title in search_category("dc.fandom.com", "Green Lantern Vol 3 49/Images"):
    print("  ", title)
for title in search_category("dc.fandom.com", "Green Lantern Vol 3 50/Images"):
    print("  ", title)

# 4. Spider-Man vs Firelord (Amazing Spider-Man Vol 1 269 & 270)
print("\n4. Spider-Man vs Firelord:")
for title in search_category("marvel.fandom.com", "Amazing Spider-Man Vol 1 269/Images"):
    print("  ", title)
for title in search_category("marvel.fandom.com", "Amazing Spider-Man Vol 1 270/Images"):
    print("  ", title)

# 5. Daredevil King of Hell's Kitchen (Daredevil Vol 2 50)
print("\n5. Daredevil Vol 2 50:")
for title in search_category("marvel.fandom.com", "Daredevil Vol 2 50/Images"):
    print("  ", title)

# 6. Joker Death of the Family (Batman Vol 2 13, 14, 15, 16, 17)
print("\n6. Joker Death of the Family:")
for title in search_fandom("dc.fandom.com", "Joker face Batman Vol 2 13"):
    print("  ", title)
for title in search_category("dc.fandom.com", "Batman Vol 2 13/Images"):
    print("  ", title)

# 7. Punisher Welcome Back Frank #1
print("\n7. Punisher Vol 5 1:")
for title in search_category("marvel.fandom.com", "The Punisher Vol 5 1/Images"):
    print("  ", title)

# 8. Superman Justice League Vol 4 25 (World Forger)
print("\n8. Superman World Forger (Justice League Vol 4 25):")
for title in search_category("dc.fandom.com", "Justice League Vol 4 25/Images"):
    print("  ", title)

# 9. Thor #380 (Midgard Serpent)
print("\n9. Thor #380:")
for title in search_category("marvel.fandom.com", "Thor Vol 1 380/Images"):
    print("  ", title)

# 10. Flash Crisis on Infinite Earths #8
print("\n10. Flash Crisis on Infinite Earths #8:")
for title in search_category("dc.fandom.com", "Crisis on Infinite Earths Vol 1 8/Images"):
    print("  ", title)
