import os
import sys
import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

pid = os.environ.get('FB_PAGE_ID', '1289410784257454')
tok = os.environ.get('FB_PAGE_TOKEN')

url = f"https://graph.facebook.com/v20.0/{pid}/scheduled_posts?access_token={tok}&fields=id,scheduled_publish_time,message&limit=50"
res = requests.get(url).json()
data = sorted(res.get('data', []), key=lambda x: x.get('scheduled_publish_time', 0))

print(f"\n=======================================================")
print(f" TOTAL PROGRAMADOS EN COLA OFICIAL DE FACEBOOK: {len(data)}")
print(f"=======================================================")

tz_local = datetime.timezone(datetime.timedelta(hours=-5))

for idx, p in enumerate(data, 1):
    ts = p.get('scheduled_publish_time', 0)
    dt_local = datetime.datetime.fromtimestamp(ts, tz=tz_local)
    first_line = (p.get('message') or '').splitlines()[0] if p.get('message') else '(Sin texto)'
    print(f"[{idx:02d}] {dt_local.strftime('%A %d-%b %I:%M %p')} | ID: {p['id']} | {first_line}")
