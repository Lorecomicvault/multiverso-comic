import requests, re

url = 'https://www.reddit.com/r/DCcomics/comments/174s0i4/comic_excerpt_should_batman_be_weaker_or_stronger/'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
print("Response status:", r.status_code)
# Search for any jpg or png
all_links = re.findall(r'https?://[^\s\"\'<>]+\.(?:jpg|png|jpeg|webp)', r.text)
print("Total image links:", len(all_links))
for l in list(set(all_links))[:10]:
    print(" ", l)
