"""
Curador Canónico 1:1 para los 5 Mega Hits Remasterizados (Slots 51 al 55)
========================================================================
Extrae y enmarca viñetas 1080x1920 directamente de los cómics fuente:
- Slot 51: Superior Spider-Man #1 (Puñetazo a Escorpión)
- Slot 52: Batman: The Devastator #1 (Virus Doomsday)
- Slot 53: Amazing Spider-Man #542 (Spider-Man humilla a Kingpin en Ryker's)
- Slot 54: Siege #2 (Sentry parte en dos a Ares)
- Slot 55: Dark Nights: The Batman Who Laughs #1 (Nacimiento del Batman que Ríe)
"""

import os
import sys
import math
from pathlib import Path
from PIL import Image, ImageStat, ImageChops

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
COMICS_SOURCE = PROJECT_ROOT / "assets" / "comics_source"

def frame_to_vertical_1080x1920(src_img_path, dest_path, crop_box=None):
    """
    Convierte una viñeta/página de cómic en video vertical 1080x1920:
    - Si se especifica crop_box (left, top, right, bottom en fracciones 0.0-1.0), recorta la viñeta exacta.
    - Aplica fill/crop proporcional preservando el arte del cómic sin distorsión.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src_img_path) as im:
        im = im.convert("RGB")
        w, h = im.size
        
        if crop_box:
            l = int(crop_box[0] * w)
            t = int(crop_box[1] * h)
            r = int(crop_box[2] * w)
            b = int(crop_box[3] * h)
            im = im.crop((l, t, r, b))
            w, h = im.size
            
        target_w, target_h = 1080, 1920
        target_aspect = target_w / target_h # 0.5625
        current_aspect = w / h
        
        if current_aspect > target_aspect:
            # Más ancha -> ajustar altura y recortar laterales
            new_h = target_h
            new_w = int(round(w * (target_h / h)))
            im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
            left = (new_w - target_w) // 2
            im_final = im_resized.crop((left, 0, left + target_w, target_h))
        else:
            # Más alta -> ajustar ancho y recortar arriba/abajo centrado
            new_w = target_w
            new_h = int(round(h * (target_w / w)))
            im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
            top = (new_h - target_h) // 2
            im_final = im_resized.crop((0, top, target_w, top + target_h))
            
        im_final.save(dest_path, "JPEG", quality=95)
        print(f"  [OK] Guardado: {dest_path.name} (1080x1920)")

def calc_rms(p1, p2):
    with Image.open(p1) as im1, Image.open(p2) as im2:
        im1_gray = im1.convert('L').resize((256, 256))
        im2_gray = im2.convert('L').resize((256, 256))
        stat = ImageStat.Stat(ImageChops.difference(im1_gray, im2_gray))
        return stat.rms[0]

print("=" * 80)
print("🎨 CURANDO PANELES CANÓNICOS 1:1 PARA SLOTS 51 AL 55")
print("=" * 80)

# -------------------------------------------------------------
# SLOT 51: Superior Spider-Man vs Escorpión (Mandíbula)
# Fuente: output/superior_spiderman_long/panels_1080p/
# -------------------------------------------------------------
print("\n--- SLOT 51: Superior Spider-Man (Mandíbula de Escorpión) ---")
s51_dest = CURATED_BASE / "51_spiderman_escorpion_mandibula_superior"
p_dir_51 = PROJECT_ROOT / "output" / "superior_spiderman_long" / "panels_1080p"

frame_to_vertical_1080x1920(p_dir_51 / "panel_031.jpg", s51_dest / "scene_01.jpg") # Escorpión amenazando en hospital
frame_to_vertical_1080x1920(p_dir_51 / "panel_033.jpg", s51_dest / "scene_02.jpg") # Superior Spider-Man confrontándolo
frame_to_vertical_1080x1920(p_dir_51 / "panel_036.jpg", s51_dest / "scene_03.jpg") # El derechazo que arranca la mandíbula
frame_to_vertical_1080x1920(p_dir_51 / "panel_039.jpg", s51_dest / "scene_04.jpg") # Otto mirando su puño en shock

# -------------------------------------------------------------
# SLOT 52: Batman: The Devastator #1 (Virus Doomsday)
# Fuente: assets/comics_source/batman_devastator/extracted/
# -------------------------------------------------------------
print("\n--- SLOT 52: Batman se inyecta el Virus Doomsday ---")
s52_dest = CURATED_BASE / "52_batman_virus_doomsday_devastator"
p_dir_52 = COMICS_SOURCE / "batman_devastator" / "extracted"

# Page 006: Superman rogue heat vision / Lois dying
frame_to_vertical_1080x1920(p_dir_52 / "Batman - The Devastator (2017-) 001-006.jpg", s52_dest / "scene_01.jpg", crop_box=(0.0, 0.25, 1.0, 0.85))
# Page 010: Flashback Superman confronting Bruce / spear broken
frame_to_vertical_1080x1920(p_dir_52 / "Batman - The Devastator (2017-) 001-010.jpg", s52_dest / "scene_02.jpg", crop_box=(0.0, 0.35, 1.0, 0.95))
# Page 011: Bruce pulling syringe and injecting Doomsday virus
frame_to_vertical_1080x1920(p_dir_52 / "Batman - The Devastator (2017-) 001-011.jpg", s52_dest / "scene_03.jpg", crop_box=(0.0, 0.15, 1.0, 0.75))
# Page 013: Full Devastator bone monster roaring over defeated Superman
frame_to_vertical_1080x1920(p_dir_52 / "Batman - The Devastator (2017-) 001-013.jpg", s52_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.85))

# -------------------------------------------------------------
# SLOT 53: Amazing Spider-Man #542 (Back in Black / Kingpin)
# Fuente: assets/comics_source/spiderman_back_in_black/extracted_asm_542/.../
# -------------------------------------------------------------
print("\n--- SLOT 53: Spider-Man humilla a Kingpin en prisión ---")
s53_dest = CURATED_BASE / "53_spiderman_back_in_black_kingpin"
p_dir_53 = list((COMICS_SOURCE / "spiderman_back_in_black" / "extracted_asm_542").glob("*"))[0]

# Page 002: Peter in black suit entering Ryker's Island
frame_to_vertical_1080x1920(p_dir_53 / "The Amazing Spider-Man 542-002.jpg", s53_dest / "scene_01.jpg", crop_box=(0.0, 0.10, 1.0, 0.75))
# Page 006: Peter taking off the mask in front of Kingpin
frame_to_vertical_1080x1920(p_dir_53 / "The Amazing Spider-Man 542-006.jpg", s53_dest / "scene_02.jpg", crop_box=(0.0, 0.20, 1.0, 0.85))
# Page 014: Slapping Kingpin bloody across the cell block
frame_to_vertical_1080x1920(p_dir_53 / "The Amazing Spider-Man 542-014.jpg", s53_dest / "scene_03.jpg", crop_box=(0.0, 0.15, 1.0, 0.80))
# Page 015: Grabbing Fisk's throat and threatening to fill lungs with web
frame_to_vertical_1080x1920(p_dir_53 / "The Amazing Spider-Man 542-015.jpg", s53_dest / "scene_04.jpg", crop_box=(0.0, 0.25, 1.0, 0.90))

# -------------------------------------------------------------
# SLOT 54: Siege #2 (Sentry descuartiza a Ares)
# Fuente: assets/comics_source/siege/extracted_siege_02/
# -------------------------------------------------------------
print("\n--- SLOT 54: Sentry descuartiza a Ares en Asedio ---")
s54_dest = CURATED_BASE / "54_sentry_descuartiza_ares_siege"
p_dir_54 = COMICS_SOURCE / "siege" / "extracted_siege_02"

# Page 004: Norman Osborn and Dark Avengers attacking Asgard
frame_to_vertical_1080x1920(p_dir_54 / "Siege 02-004.jpg", s54_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.70))
# Page 010: Ares confronting Sentry in the skies
frame_to_vertical_1080x1920(p_dir_54 / "Siege 02-010.jpg", s54_dest / "scene_02.jpg", crop_box=(0.0, 0.30, 1.0, 0.95))
# Page 013: Sentry grabbing Ares by the chest with black Void eyes
frame_to_vertical_1080x1920(p_dir_54 / "Siege 02-013.jpg", s54_dest / "scene_03.jpg", crop_box=(0.0, 0.20, 1.0, 0.80))
# Page 014: Sentry ripping Ares in two halves down the middle
frame_to_vertical_1080x1920(p_dir_54 / "Siege 02-014.jpg", s54_dest / "scene_04.jpg", crop_box=(0.0, 0.10, 1.0, 0.85))

# -------------------------------------------------------------
# SLOT 55: Dark Nights: The Batman Who Laughs #1
# Fuente: assets/comics_source/batman_who_laughs/extracted/
# -------------------------------------------------------------
print("\n--- SLOT 55: El Batman Que Ríe (Origen en Crime Alley) ---")
s55_dest = CURATED_BASE / "55_batman_que_rie_dark_multiverse"
p_dir_55 = COMICS_SOURCE / "batman_who_laughs" / "extracted"

# Page 006: Joker holding hostages and laughing
frame_to_vertical_1080x1920(p_dir_55 / "Dark Nights - The Batman Who Laughs - c001 (web) - p006-007 [Digital-HD] [danke-Empire].jpg", s55_dest / "scene_01.jpg", crop_box=(0.0, 0.10, 0.55, 0.85))
# Page 008: Batman breaking Joker's neck on the ground
frame_to_vertical_1080x1920(p_dir_55 / "Dark Nights - The Batman Who Laughs - c001 (web) - p008 [Digital-HD] [danke-Empire].jpg", s55_dest / "scene_02.jpg", crop_box=(0.0, 0.25, 1.0, 0.90))
# Page 009: Green toxin puffing from Joker's heart infecting Bruce
frame_to_vertical_1080x1920(p_dir_55 / "Dark Nights - The Batman Who Laughs - c001 (web) - p009 [Digital-HD] [danke-Empire].jpg", s55_dest / "scene_03.jpg", crop_box=(0.0, 0.15, 1.0, 0.75))
# Page 018: The Batman Who Laughs laughing with guns over fallen Bat-family
frame_to_vertical_1080x1920(p_dir_55 / "Dark Nights - The Batman Who Laughs - c001 (web) - p018-019 [Digital-HD] [danke-Empire].jpg", s55_dest / "scene_04.jpg", crop_box=(0.05, 0.15, 0.65, 0.85))

print("\n" + "=" * 80)
print("📊 AUDITORÍA DE DIVERSIDAD INTER-ESCENA (RMS > 50.0):")
slots = [
    ("Slot 51 (Superior Spider-Man)", s51_dest),
    ("Slot 52 (Batman Devastator)", s52_dest),
    ("Slot 53 (Spider-Man Back in Black)", s53_dest),
    ("Slot 54 (Sentry Ares)", s54_dest),
    ("Slot 55 (Batman Who Laughs)", s55_dest),
]

all_passed = True
for name, folder in slots:
    print(f"\nAuditando {name}:")
    scenes = [folder / f"scene_0{i}.jpg" for i in range(1, 5)]
    min_rms = 999.0
    for i in range(4):
        for j in range(i + 1, 4):
            rms_val = calc_rms(scenes[i], scenes[j])
            min_rms = min(min_rms, rms_val)
            print(f"  - Escena {i+1} vs Escena {j+1}: RMS = {rms_val:.2f}")
    if min_rms < 50.0:
        print(f"  ❌ FALLÓ RMS MÍNIMO: {min_rms:.2f} < 50.0")
        all_passed = False
    else:
        print(f"  ✅ PASÓ AUDITORÍA: RMS Mínimo = {min_rms:.2f} >= 50.0")

if all_passed:
    print("\n🎉 TODOS LOS 5 SLOTS SUPERARON EL QUALITY GATE RMS Y ESTÁN LISTOS AL 100%!")
else:
    print("\n⚠️ ALGUNOS SLOTS REQUIEREN AJUSTE DE ENCUADRE.")
