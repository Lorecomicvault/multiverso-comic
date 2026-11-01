import requests
from bs4 import BeautifulSoup

url = 'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEASYVc9H42UXT492y7BuowoXC3Zi8rkHr1JJ2jpfwOJ9kf5Pq1aoa5J0kLS4jH__UGp1_opfd8-qWagmi9d0I9IR9A2TMEf5EpnCFp0DrlqJMjhIocYXs2petPouhT_j5-IxfalFcjGK7oEofbT0x2PsJWQQrxECF5dWNMy-m0IZc='
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
print("Blog URL:", r.url)
soup = BeautifulSoup(r.text, 'html.parser')
imgs = [img.get('src') for img in soup.find_all('img') if img.get('src') and any(ext in img.get('src').lower() for ext in ['.jpg', '.png', '.jpeg', '.webp'])]
print(f"Found {len(imgs)} images:")
for im in imgs:
    print("  ", im)
