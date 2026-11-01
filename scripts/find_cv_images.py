import requests, re

url = 'https://comicvine.gamespot.com/forums/gen-discussion-1/black-bolt-vs-vulcan-a-great-battle-or-604262/'
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers)
imgs = re.findall(r'https?://[^\s\"\'<>]+\.(?:jpg|png|jpeg)', r.text, re.IGNORECASE)
print(f'Total images: {len(imgs)}')
for i in list(set(imgs))[:15]:
    print(' ', i)
