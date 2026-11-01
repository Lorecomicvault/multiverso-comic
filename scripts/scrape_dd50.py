import sys
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://scans-daily.dreamwidth.org/7585232.html"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
entry = soup.find('div', class_='entry-content')
if entry:
    for img in entry.find_all('img'):
        print(img.get('src'))
