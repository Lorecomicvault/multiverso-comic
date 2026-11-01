import requests
from bs4 import BeautifulSoup
import re

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnrwd3Sitfhf1XHiGXPPrrQF0mSPUdTlxAN78oa1M0ECwCdUJTuWrVFao6e3r8QN_FL4HCt63LY_IarjfJHyCpidX1ITkTTR4l7bCvKOMYCiT6hu8gSg8QkGQYEp4DlS0PfMvseA==',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSqNOiAkJVf2P3IbleQOud5zy_obZ2Z0hHv3nnNsBlk8PF0ZwXzcV7UPFfL-JVPUS2JGY9IB7R1TLzj63fNSRXTJWrCq4rMyYYm38Vs1UPYFgKIRCfxQn_1KTXVZKkXpXFtgKKNg=='
]

headers = {'User-Agent': 'Mozilla/5.0'}
for idx, u in enumerate(urls, 1):
    try:
        r = requests.get(u, headers=headers, allow_redirects=True, timeout=10)
        print(f"Article {idx}: {r.url}")
        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = [img.get('src') for img in soup.find_all('img') if img.get('src') and any(ext in img.get('src').lower() for ext in ['.jpg', '.png', '.jpeg'])]
        print(f"  Found {len(imgs)} images:")
        for im in imgs:
            print("   ", im)
    except Exception as e:
        print(f"Article {idx} failed: {e}")
