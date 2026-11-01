import sys
import requests
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def get_fandom_url(wiki, title):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    for p in r.get("query", {}).get("pages", {}).values():
        info = p.get("imageinfo", [{}])[0]
        return info.get("url")
    return None

test_cases = [
    # 01 Red Hulk
    ("marvel.fandom.com", "File:Thaddeus Ross (Earth-616) and Bruce Banner (Earth-616) from Hulk Vol 2 4 0001.jpg"),
    ("marvel.fandom.com", "File:Thaddeus Ross (Earth-616) and Uatu (Earth-616) from Hulk Vol 2 4 0001.jpg"),
    ("marvel.fandom.com", "File:Hulk Vol 2 4 page 04 Uatu (Earth-616).jpg"),
    ("marvel.fandom.com", "File:Monument Valley from Hulk Vol 2 5 001.png"),
    # 02 Wolverine
    ("marvel.fandom.com", "File:Johann Shmidt (Earth-807128) from Wolverine Vol 3 72 001.jpg"),
    ("marvel.fandom.com", "File:Red Skull's Trophy Case from Wolverine Vol 3 72 001.jpg"),
    ("marvel.fandom.com", "File:James Howlett (Earth-807128) from Wolverine Vol 3 72 001.jpg"),
    ("marvel.fandom.com", "File:James Howlett (Earth-807128) from Wolverine Vol 3 72 002.jpg"),
    # 03 Hal Jordan
    ("dc.fandom.com", "File:Destruction of Coast City 01.jpg"),
    ("dc.fandom.com", "File:Emerald Twilight 01.jpg"),
    ("dc.fandom.com", "File:Becoming Parallax.jpg"),
    ("dc.fandom.com", "File:Death of Parallax 01.jpg"),
    # 04 Spider-Man
    ("marvel.fandom.com", "File:Pyreus Kril (Earth-616) from Amazing Spider-Man Vol 1 269 001.jpg"),
    ("marvel.fandom.com", "File:Pyreus Kril (Earth-616) from Amazing Spider-Man Vol 1 270 001.jpg"),
    ("marvel.fandom.com", "File:Tony's Pizza from Amazing Spider-Man Vol 1 269 001.png"),
    ("marvel.fandom.com", "File:Bobby Chance (Earth-616) from Amazing Spider-Man Vol 1 270 001.png"),
    # 07 Punisher
    ("marvel.fandom.com", "File:Edward Gnucci in The Punisher Vol 5 1.jpg"),
    # 10 Flash
    ("dc.fandom.com", "File:Barry Allen Crisis on Infinite Earths 001.png"),
    ("dc.fandom.com", "File:Anti-Monitor 0012.jpg")
]

for wiki, title in test_cases:
    u = get_fandom_url(wiki, title)
    print(f"{title} -> {u}")
