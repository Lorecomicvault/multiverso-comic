import requests
from bs4 import BeautifulSoup

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEzJgDa7m4EeTjOsyrTy39ZJbZCvMgzh7dLxr68Ue0k7KcXVOyz5JBN7jsYob8fzdlSdklbBN_5yj2p7Rk8lp_7gNAYiWO2SI2dFmawcezFlDG-lnCODA8V-WgawqCg48a76HGgpww3DA9n5jRQIGfoc4qeMqaOQBx1mpDQuScbgDivyNMpbbCjAKDPz73m2dlMZ9SadCdpzV4=',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE0Q_st_mGkUxwBlNMAlYOkP3Jp-e5Vc53EfY7jazpnWze1lPaAQ2YEB7Ff8fIB3r2yO3pm5zBNxgilj7UCzEC8iJwCBqB2KytPzXd7L9I5-vpcKYdwrOR9-3U_Iw3gVbcxXt6WOpeQFajWvw=='
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
for idx, u in enumerate(urls, 1):
    try:
        r = requests.get(u, headers=headers, allow_redirects=True, timeout=8)
        print(f"URL {idx}: {r.url}")
        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = [img.get('src') for img in soup.find_all('img') if img.get('src') and any(ext in img.get('src').lower() for ext in ['.jpg', '.png', '.jpeg', '.webp'])]
        print(f"  Found {len(imgs)} images:")
        for im in imgs[:10]:
            print("   ", im)
    except Exception as e:
        print(f"Error {idx}: {e}")
