import requests
from bs4 import BeautifulSoup

url = 'https://comicritico.blogspot.com/2012/03/el-retorno-de-lobo-lobos-back.html'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')
for img in soup.find_all('img'):
    src = img.get('src', '')
    if 'lobo' in src.lower() or 'lb' in src.lower() or 'back' in src.lower():
        print(src)
