import sys
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://databasecomics.com/?s=justice+league+25', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all('a', href=True):
    if 'justice-league-25' in a['href']:
        print(a['href'])
