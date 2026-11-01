import requests
from bs4 import BeautifulSoup

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGDm3sBjDrVsB7J8OBRtCRbNRBeu4jemqa42mDzeAfVBvB5rEcjbcVKfm-FRDuJQlgyk0P473GJIeFUeDEejulSInbVTjZZfcfzVeMLEWUVzETN4pGk2QoMWxrB0zE5UIFX4FsHbQkUFnGdvqrChQ==',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHUzDUZ2NOEwjBkV65xiaH-k6clHzvwioUxExDuRe07BMI8eGNBxSQvLKNzXth_F94cCU2oJS8pSR32ihETfF2MdG6Cuf89yk66-v1bfhn75qpZrdv5lS4PxgzdepWp5dElb6u_NzRQZ4tJLeqpMg1DTE5WqW75R7iygqP0We16JushZVgZx1vs'
]

headers = {'User-Agent': 'Mozilla/5.0'}
for idx, u in enumerate(urls, 1):
    try:
        r = requests.get(u, headers=headers, allow_redirects=True, timeout=8)
        print(f"Article {idx}: {r.url}")
        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = [img.get('src') for img in soup.find_all('img') if img.get('src') and any(ext in img.get('src').lower() for ext in ['.jpg', '.png', '.jpeg'])]
        print(f"  Found {len(imgs)} images:")
        for im in imgs[:8]:
            print("   ", im)
    except Exception as e:
        print(f"Article {idx} failed: {e}")
