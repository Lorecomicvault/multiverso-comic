import sys
import requests
from bs4 import BeautifulSoup

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://www.destroythebrain.com/comics/the-joker-gets-a-face-lift-in-new-batman-story-death-of-the-family', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')
for img in soup.find_all('img'):
    print(img.get('src'))
