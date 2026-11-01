import sys
import requests
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}
url = "https://www.reddit.com/r/comicbooks/comments/1nvec3b/daredevil_50_alex_maleev.json"
r = requests.get(url, headers=headers, timeout=10)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    post = data[0]['data']['children'][0]['data']
    print("Title:", post.get('title'))
    print("URL:", post.get('url'))
    print("Gallery data:", post.get('gallery_data'))
    print("Media metadata keys:", list(post.get('media_metadata', {}).keys()))
    for k, v in post.get('media_metadata', {}).items():
        print(f"  {k} -> {v.get('s')}")
