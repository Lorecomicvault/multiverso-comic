import requests
import re
from bs4 import BeautifulSoup

def get_images_from_redirect(redirect_url):
    r = requests.get(redirect_url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
    print('Resolved URL:', r.url)
    soup = BeautifulSoup(r.text, 'html.parser')
    imgs = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src and ('jpg' in src.lower() or 'png' in src.lower() or 'webp' in src.lower()):
            imgs.append(src)
    return imgs

url = 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHgQoUfrYDt_fqmbnC6YRCWOEVsqlR8vY6_qGuYf2Z7fQJcJQ5UvpktWljwOweBwaTTdrDb9tOMZk1RsFJNYMkZinSrQqrvrE5iuP3xCeMkj_3G0_NlXH2QhRhjPIBD2NDmKl42CTysm7Wty7boAmpNXXfo79pZfeOETF33cDb0LSZB7n03oaA='
imgs = get_images_from_redirect(url)
print(f'Found {len(imgs)} images:')
for im in imgs:
    print(im)
