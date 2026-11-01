import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://api.pullpush.io/reddit/submission/search?ids=l6zv4m,etpry1', timeout=10)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    for item in data.get('data', []):
        print("ID:", item.get('id'), "Title:", item.get('title'))
        print("URL:", item.get('url'))
        if 'media_metadata' in item:
            for k, v in item['media_metadata'].items():
                print("  Media:", k, v.get('s'))
