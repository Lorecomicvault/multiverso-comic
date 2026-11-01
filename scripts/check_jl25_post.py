import sys
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://databasecomics.com/2022/09/28/feat-superman-justice-league-25-superman-day-1/', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
for img in soup.find_all('img'):
    print(img.get('src'))
