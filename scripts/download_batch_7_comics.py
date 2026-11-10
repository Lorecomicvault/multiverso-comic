import os
import sys
import zipfile
import shutil
import requests
from pathlib import Path

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
BASE_DIR = PROJECT_ROOT / "assets" / "comics_source"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

DOWNLOADS = [
    {
        "name": "iron_man_mysterium",
        "url": "https://fs2.comicfiles.ru/2024.02.28/Invincible%20Iron%20Man%20by%20Gerry%20Duggan%20v02%20-%20The%20Wedding%20Of%20Tony%20Stark%20And%20Emma%20Frost%20%282024%29%20%28Digital%29%20%28Shan-Empire%29.cbz",
        "file": "iron_man_wedding_mysterium.cbz"
    },
    {
        "name": "immortal_hulk_8",
        "url": "https://elv.comicfiles.ru/Marvel/F%20-%20J/Hulk/Immortal%20Hulk%20001-011%20%282018-2019%29.zip",
        "file": "immortal_hulk_001_011.zip"
    },
    {
        "name": "marvel_ruins",
        "url": "https://weekly1.comicfiles.ru/2018.11.07/Up2/Ruins%20%28001-002%29%281995%29%28digital%29%28Shadowcat-Empire%29.zip",
        "file": "marvel_ruins_01_02.zip"
    },
    {
        "name": "ultimatum",
        "url": "https://elv.comicfiles.ru/Others/Collection/018/Ultimatum%20%282010%29%20%28Digital%29%20%28F%29%20%28Kileko-Empire%29.cbz",
        "file": "ultimatum_complete.cbz"
    }
]

print("=" * 80)
print("📥 DESCARGANDO CÓMICS FUENTE CANÓNICOS PARA EL LOTE 7 (SLOTS 67, 74, 75, 76)")
print("=" * 80)

for item in DOWNLOADS:
    target_dir = BASE_DIR / item["name"]
    target_dir.mkdir(parents=True, exist_ok=True)
    out_file = target_dir / item["file"]

    if out_file.exists() and out_file.stat().st_size > 1000000:
        print(f"⏩ {item['name']} ya descargado ({out_file.stat().st_size / (1024*1024):.1f} MB). Omitiendo.")
        continue

    print(f"\n⬇️ Descargando {item['name']} desde {item['url']}...")
    try:
        with requests.get(item["url"], headers=HEADERS, stream=True, timeout=120) as r:
            r.raise_for_status()
            with open(out_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 512):
                    if chunk:
                        f.write(chunk)
        print(f"✅ Descargado: {out_file.name} ({out_file.stat().st_size / (1024*1024):.1f} MB)")
    except Exception as e:
        print(f"❌ Error descargando {item['name']}: {e}")

print("\n🎉 Proceso de descarga finalizado.")
