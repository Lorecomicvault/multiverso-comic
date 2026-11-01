import requests
from bs4 import BeautifulSoup

url = 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGgLaeoFiCezwAdc0nPHWMHW16GTq_fYW-nYT_KuKQtr9zpOzM_MA2tMZj7k9yB4lyx7EaLTTL2FjVWAKmSq367gPLsRkag81ldCXghKnUYs8aLMBnlsKUFiGBmSQqyHmsnmymMMOlIkb13GMxjDRRr6g9P4mX49_I='

headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
print("Blog URL:", r.url)
soup = BeautifulSoup(r.text, 'html.parser')
imgs = [img.get('src') for img in soup.find_all('img') if img.get('src') and any(ext in img.get('src').lower() for ext in ['.jpg', '.png', '.jpeg', '.webp'])]
print(f"Found {len(imgs)} images:")
for im in imgs:
    print("  ", im)
