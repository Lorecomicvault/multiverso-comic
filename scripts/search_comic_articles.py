import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def search_ddg(query):
    url = 'https://html.duckduckgo.com/html/'
    try:
        r = requests.post(url, data={'q': query}, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for a in soup.find_all('a', class_='result__snippet'):
            href = a.get('href', '')
            # duckduckgo redirects via uddg=
            m = re.search(r'uddg=([^&]+)', href)
            if m:
                links.append(urllib.parse.unquote(m.group(1)))
        if not links:
            for a in soup.find_all('a', class_='result__url'):
                href = a.get('href', '').strip()
                m = re.search(r'uddg=([^&]+)', href)
                if m:
                    links.append(urllib.parse.unquote(m.group(1)))
                elif href.startswith('http'):
                    links.append(href)
        return links
    except Exception as e:
        print(f"Error DDG: {e}")
        return []

def get_page_images(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                if not any(bad in src.lower() for bad in ['avatar', 'icon', 'logo', 'button', 'tracker', 'ad-']):
                    imgs.append(src)
        return imgs
    except Exception as e:
        return []

print("=== TESTING SEARCH FOR COMIC SCANS ===")
links = search_ddg('site:scans-daily.dreamwidth.org "Wolverine #72" "Red Skull"')
print(f"Found {len(links)} links for Wolverine:")
for l in links[:3]:
    print(" ", l)
    imgs = get_page_images(l)
    print(f"   -> {len(imgs)} images found")
    for im in imgs[:4]:
        print("     ", im)
