import sys
from pathlib import Path
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
OUT_DIR = PROJECT_ROOT / "assets" / "curated_panels" / "05_daredevil_nuevo_rey_del_crimen_hells_kitchen"

for name in ['daredevil11', 'daredevil12', 'daredevil13', 'daredevil14', 'daredevil15', 'daredevil16']:
    url = f"https://atomicjunkshop.com/wp-content/uploads/2020/05/{name}.jpg"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
    if r.status_code == 200:
        (OUT_DIR / f"{name}.jpg").write_bytes(r.content)
        print(f"Saved {name}.jpg: {len(r.content)} bytes")

print("Done saving Daredevil candidate panels.")
