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

# 1. Iron Man Wedding
im_out = COMICS_SOURCE / "iron_man_mysterium" / "extracted_pages"
print(f"Iron Man pages extracted: {len(list(im_out.glob('*.jpg')))} files")

# 2. Extract Immortal Hulk 8 using bsdtar
hulk_8_cbr = COMICS_SOURCE / "immortal_hulk_8" / "extracted" / "Immortal Hulk 008 (2018).cbr"
hulk_8_pages = COMICS_SOURCE / "immortal_hulk_8" / "extracted_pages_08"
hulk_8_pages.mkdir(parents=True, exist_ok=True)
if not list(hulk_8_pages.glob("*.jpg")):
    print("Extracting Immortal Hulk 008 with tar...")
    subprocess.run(['tar', '-xf', str(hulk_8_cbr), '-C', str(hulk_8_pages)], check=True)
    # Flatten if inside subfolder
    for sub in hulk_8_pages.iterdir():
        if sub.is_dir():
            for f in sub.glob("*.jpg"):
                shutil.move(f, hulk_8_pages / f.name)
print(f"Immortal Hulk 008 pages: {len(list(hulk_8_pages.glob('*.jpg')))} files")

# 3. Extract Marvel Ruins
ruins_zip = COMICS_SOURCE / "marvel_ruins" / "marvel_ruins_01_02.zip"
ruins_out = COMICS_SOURCE / "marvel_ruins" / "extracted_cbz"
safe_extract_zip(ruins_zip, ruins_out)

ruins_pages = COMICS_SOURCE / "marvel_ruins" / "extracted_pages"
ruins_pages.mkdir(parents=True, exist_ok=True)
for cbz in ruins_out.glob("*.cbz"):
    print(f"  Extracting {cbz.name}...")
    safe_extract_zip(cbz, ruins_pages / cbz.stem)
print(f"Marvel Ruins pages extracted: {len(list(ruins_pages.rglob('*.jpg')))} files")

# 4. Extract Ultimatum Complete
ult_cbz = COMICS_SOURCE / "ultimatum" / "ultimatum_complete.cbz"
ult_pages = COMICS_SOURCE / "ultimatum" / "extracted_pages"
safe_extract_zip(ult_cbz, ult_pages)
print(f"Ultimatum pages extracted: {len(list(ult_pages.glob('*.jpg')))} files")

print("\n🎉 ALL 4 COMICS FULLY EXTRACTED!")
