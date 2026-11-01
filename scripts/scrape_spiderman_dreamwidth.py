import sys
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://scans-daily.dreamwidth.org/3742358.html"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
entry = soup.find('div', class_='entry-content')
if entry:
    for img in entry.find_all('img'):
        print(img.get('src'))
else:
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and ('imgur' in src or 'photobucket' in src or 'abload' in src):
            print(src)
