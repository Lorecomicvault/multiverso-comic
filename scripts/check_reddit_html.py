import sys
import requests
from bs4 import BeautifulSoup
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.reddit.com/r/Thor/comments/1rw32md/thor_vs_jormungandr_full_fight_thor_1966_380/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all(['a', 'img']):
    href = a.get('href') or a.get('src')
    if href and any(ext in href.lower() for ext in ['.jpg', '.png', '.jpeg', '.webp']):
        print('IMG:', href)
