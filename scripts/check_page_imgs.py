import sys
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

url = "https://scans-daily.dreamwidth.org/7585232.html"
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
for img in soup.find_all('img'):
    src = img.get('src')
    print('IMG:', src)
