import requests
from bs4 import BeautifulSoup
import re

url = "https://scans-daily.dreamwidth.org/4792932.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

print("Status:", r.status_code)
entries = soup.find_all('div', class_='entry-content')
print("Entries found:", len(entries))

all_imgs = []
for e in entries:
    for img in e.find_all('img'):
        src = img.get('src')
        if src:
            all_imgs.append(src)

print(f"Found {len(all_imgs)} entry images:")
for i in all_imgs:
    print(i)
