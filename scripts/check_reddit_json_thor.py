import sys
import requests
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.reddit.com/r/Thor/comments/1rw32md/thor_vs_jormungandr_full_fight_thor_1966_380.json"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
}
r = requests.get(url, headers=headers)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    post = data[0]['data']['children'][0]['data']
    print("Title:", post.get('title'))
    gallery = post.get('gallery_data')
    media_metadata = post.get('media_metadata', {})
    if gallery:
        for item in gallery.get('items', []):
            media_id = item.get('media_id')
            m = media_metadata.get(media_id, {})
            # get full url
            s = m.get('s', {})
            u = s.get('u')
            if u:
                print(" Gallery img:", u.replace('&amp;', '&'))
    else:
        print("URL:", post.get('url'))
