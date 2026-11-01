import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def search_titles(query):
    url = "https://marvel.fandom.com/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'srnamespace': '6', # File namespace
        'srlimit': 30,
        'format': 'json'
    }
    r = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'}).json()
    items = r.get('query', {}).get('search', [])
    print(f"Results for '{query}': {len(items)}")
    for item in items:
        print(" ", item['title'])

search_titles('Daredevil Vol 2 50')
search_titles('Daredevil Kingpin Hardcore')
search_titles('Daredevil beats Kingpin')
search_titles('Daredevil Kingpin Josie')
