import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

test_url = "https://web.archive.org/web/2020/https://abload.de/img/daredevilv2050-023ykoje.jpg"
r = requests.get(test_url, headers={'User-Agent': 'Mozilla/5.0'})
print('Archive status:', r.status_code, 'Length:', len(r.content))
