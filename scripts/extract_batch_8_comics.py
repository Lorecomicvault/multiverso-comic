import os
import sys
import zipfile
import shutil
import subprocess
from pathlib import Path

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
COMICS_SOURCE = PROJECT_ROOT / "assets" / "comics_source"

def safe_extract_zip(zip_path, target_dir):
    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            fname = Path(info.filename).name
            if not fname:
                continue
            ext = Path(fname).suffix.lower()
            if ext in ['.jpg', '.jpeg', '.png', '.webp', '.cbr', '.cbz']:
                dest_file = target_dir / fname
                if not dest_file.exists():
                    with z.open(info) as src, open(dest_file, "wb") as dst:
                        shutil.copyfileobj(src, dst)

# 1. Thanos Wins
tw_cbz = COMICS_SOURCE / "thanos_wins" / "thanos_by_donny_cates.cbz"
tw_out = COMICS_SOURCE / "thanos_wins" / "extracted_pages"
print("Extracting Thanos Wins...")
safe_extract_zip(tw_cbz, tw_out)
print(f"  Thanos Wins extracted: {len(list(tw_out.glob('*.*')))} files")

# 2. Wolverine vs Hulk
wvh_cbz = COMICS_SOURCE / "wolverine_vs_hulk" / "ultimate_wolverine_vs_hulk.cbz"
wvh_out = COMICS_SOURCE / "wolverine_vs_hulk" / "extracted_pages"
print("Extracting Wolverine vs Hulk...")
safe_extract_zip(wvh_cbz, wvh_out)
print(f"  Wolverine vs Hulk extracted: {len(list(wvh_out.glob('*.*')))} files")

# 3. Uncanny X-Force (CBR -> tar)
uxf_cbr = COMICS_SOURCE / "uncanny_xforce" / "uncanny_xforce_apocalypse_solution.cbr"
uxf_out = COMICS_SOURCE / "uncanny_xforce" / "extracted_pages"
uxf_out.mkdir(parents=True, exist_ok=True)
print("Extracting Uncanny X-Force...")
try:
    subprocess.run(['tar', '-xf', str(uxf_cbr), '-C', str(uxf_out)], check=True)
    for sub in uxf_out.iterdir():
        if sub.is_dir():
            for f in sub.glob("*.jpg"):
                shutil.move(f, uxf_out / f.name)
except Exception as e:
    print(f"  tar extract failed: {e}")
print(f"  Uncanny X-Force extracted: {len(list(uxf_out.glob('*.*')))} files")

# 4. Siege 03 & 04 (for Sentry Void)
siege_dir = COMICS_SOURCE / "siege" / "extracted" / "Siege 01-04 (2010) (digital) (Minutemen-InnerDemons)"
siege_void_out = COMICS_SOURCE / "siege" / "extracted_siege_void"
siege_void_out.mkdir(parents=True, exist_ok=True)
print("Extracting Siege 03 & 04...")
for s_cbr in siege_dir.glob("Siege 0[34]*.cbr"):
    sub = siege_void_out / s_cbr.stem[:8]
    sub.mkdir(parents=True, exist_ok=True)
    subprocess.run(['tar', '-xf', str(s_cbr), '-C', str(sub)], stdout=subprocess.DEVNULL)
print(f"  Siege Void extracted: {len(list(siege_void_out.rglob('*.jpg')))} files")

print("\n🎉 ALL BATCH 8 COMICS EXTRACTED!")
