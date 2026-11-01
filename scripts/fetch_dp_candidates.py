import requests
from io import BytesIO
from PIL import Image

def fetch_fandom(wiki, title, out_name):
    url = f"https://{wiki}/api.php"
    params = {
        "action": "query",
        "titles": title,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    pages = r.get("query", {}).get("pages", {})
    for k, v in pages.items():
        if "imageinfo" in v:
            img_url = v["imageinfo"][0]["url"]
            print(f"Fetching {title} -> {img_url}")
            res = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': f'https://{wiki}/'})
            im = Image.open(BytesIO(res.content)).convert('RGB')
            im.save(out_name, quality=95)
            print(f"Saved {out_name}, size: {im.size}")
            return True
    return False

fetch_fandom("marvel.fandom.com", "File:Wade Wilson (Earth-616) from Deadpool Vol 3 17 page 07.jpg", "dp_p07.jpg")
fetch_fandom("marvel.fandom.com", "File:Wade Wilson (Earth-616) from Deadpool Vol 3 17 page 12.jpg", "dp_p12.jpg")
fetch_fandom("marvel.fandom.com", "File:Wade Wilson (Earth-616) from Deadpool Vol 3 18 0001.jpg", "dp_18_01.jpg")
