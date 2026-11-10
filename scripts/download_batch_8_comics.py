import os
import sys
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
        "name": "thanos_wins",
        "url": "https://ten.comicfiles.ru/Others/Collection/008/Thanos%20by%20Donny%20Cates%20%282019%29%20%28Digital%29%20%28Kileko-Empire%29.cbz",
        "file": "thanos_by_donny_cates.cbz"
    },
    {
        "name": "wolverine_vs_hulk",
        "url": "https://elv.comicfiles.ru/Marvel/U%20-%20Z/Wolverine/Ultimate%20Comics%20Wolverine%20vs.%20Hulk%20%282010%29%20%28Digital%29%20%28F%29%20%28Kileko-Empire%29.cbz",
        "file": "ultimate_wolverine_vs_hulk.cbz"
    },
    {
        "name": "uncanny_xforce",
        "url": "https://elv.comicfiles.ru/Weekly/2019.08.14/Uncanny%20X-Force%20v01%20-%20Apocalypse%20Solution%20%282011%29%20%28Digital%29%20%28F%29%20%28Zone-Empire%29.cbr",
        "file": "uncanny_xforce_apocalypse_solution.cbr"
    }
]

print("=" * 80)
print("📥 DESCARGANDO CÓMICS FUENTE PARA EL LOTE 8 (SLOTS 79, 82, 85)")
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
