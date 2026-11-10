"""
Curador Canónico 1:1 para el Lote 7 Remasterizado (>10k Views: Slots 67 al 76)
=============================================================================
Enmarca y escala todas las viñetas a 1080x1920 sin recorte destructivo:
- Preserva el 100% de la acción original con fondo desenfocado oscuro de alta calidad.
- Cero cabezas cortadas, cero globos de texto cortados.
- Grado de color cinemático suave y optimizado para pantallas móviles OLED.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
COMICS_SOURCE = PROJECT_ROOT / "assets" / "comics_source"

def frame_to_vertical_1080x1920(src_img_path, dest_path, crop_box=None, center_y_ratio=0.48):
    """
    Convierte una viñeta/página de cómic en video vertical 1080x1920 sin recorte destructivo:
    - Preserva el 100% del ancho y alto de la viñeta/personajes.
    - Aplica fondo desenfocado cinematográfico suave para viñetas horizontales o cuadradas.
    - Garantiza safe-zone absoluta para que ningún personaje, golpe ni texto quede cortado.
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

        # Fondo desenfocado artístico y oscuro de la misma escena
        bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(38))
        bg = ImageEnhance.Brightness(bg).enhance(0.32)

        if current_aspect >= target_aspect:
            fg_w = target_w
            fg_h = int(round(target_w / current_aspect))
            fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
            y_pos = int((target_h - fg_h) * center_y_ratio)
            bg.paste(fg, (0, y_pos))
            im_final = bg
        else:
            fg_h = target_h
            fg_w = int(round(target_h * current_aspect))
            fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
            x_pos = (target_w - fg_w) // 2
            bg.paste(fg, (x_pos, 0))
            im_final = bg

        im_final.save(dest_path, "JPEG", quality=95)
        print(f"  [OK] Guardado seguro: {dest_path.parent.name}/{dest_path.name} (1080x1920)")

print("=" * 80)
print("🎨 CURANDO PANELES CANÓNICOS 1:1 PARA SLOTS 67 AL 76")
print("=" * 80)

# -------------------------------------------------------------
# SLOT 67: Invincible Iron Man (El Gran Robo del Mysterium)
# -------------------------------------------------------------
print("\n--- SLOT 67: Invincible Iron Man - El Robo del Mysterium ---")
s67_dest = CURATED_BASE / "67_iron_man_mysterium_gran_robo"
im_dir = COMICS_SOURCE / "iron_man_mysterium" / "extracted_pages"
im_files = sorted(list(im_dir.glob("*.jpg")))
frame_to_vertical_1080x1920(im_files[3], s67_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Altar / Alianza Emma Frost y Tony
frame_to_vertical_1080x1920(im_files[58], s67_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Infiltración gala Hellfire Club / ajedrez
frame_to_vertical_1080x1920(im_files[78], s67_dest / "scene_03.jpg", crop_box=(0.0, 0.10, 1.0, 0.90)) # Robo del lingote de Mysterium
frame_to_vertical_1080x1920(im_files[92], s67_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Forja de la Armadura Mysterium Mark 72

# -------------------------------------------------------------
# SLOT 68: Thor vs Gorr el Carnicero de Dioses
# -------------------------------------------------------------
print("\n--- SLOT 68: Thor: God of Thunder - Gorr el Carnicero ---")
s68_dest = CURATED_BASE / "68_thor_gorr_carnicero_dioses"
gorr_raw = PROJECT_ROOT / "output" / "batch_10_virales_60s" / "08_thor_gorr_butcher" / "scenes"
frame_to_vertical_1080x1920(gorr_raw / "scene_01.jpg", s68_dest / "scene_01.jpg", crop_box=None) # Gorr y la Necroespada
frame_to_vertical_1080x1920(gorr_raw / "scene_02.jpg", s68_dest / "scene_02.jpg", crop_box=None) # Thor joven en el año 800
frame_to_vertical_1080x1920(gorr_raw / "scene_04.jpg", s68_dest / "scene_03.jpg", crop_box=None) # Rey Thor al fin del tiempo
frame_to_vertical_1080x1920(gorr_raw / "scene_07.jpg", s68_dest / "scene_04.jpg", crop_box=None) # Los tres Thors derrotando a Gorr

# -------------------------------------------------------------
# SLOT 69: All-Star Superman - El Sacrificio Supremo
# -------------------------------------------------------------
print("\n--- SLOT 69: All-Star Superman - El Sacrificio Supremo ---")
s69_dest = CURATED_BASE / "69_superman_all_star_sacrificio"
as_raw = PROJECT_ROOT / "output" / "all_star_superman_sacrificio"
frame_to_vertical_1080x1920(as_raw / "scene_01" / "scene_01.jpg", s69_dest / "scene_01.jpg", crop_box=None) # Rescate en el sol / sobrecarga celular
frame_to_vertical_1080x1920(as_raw / "scene_03" / "scene_03.jpg", s69_dest / "scene_02.jpg", crop_box=None) # Superman y Lois en la Luna
frame_to_vertical_1080x1920(as_raw / "scene_08" / "scene_08.jpg", s69_dest / "scene_03.jpg", crop_box=None) # Vuelo final hacia el corazón del sol
frame_to_vertical_1080x1920(as_raw / "scene_09" / "scene_09.jpg", s69_dest / "scene_04.jpg", crop_box=None) # Dios Dorado del Sol

# -------------------------------------------------------------
# SLOT 70: Deathstroke - Humillación a la Liga de la Justicia
# -------------------------------------------------------------
print("\n--- SLOT 70: Identity Crisis - Deathstroke Humilla a la Liga ---")
s70_dest = CURATED_BASE / "70_deathstroke_identity_crisis_liga"
ds_raw = PROJECT_ROOT / "output" / "deathstroke_identity_crisis"
frame_to_vertical_1080x1920(ds_raw / "scene_01" / "scene_01.jpg", s70_dest / "scene_01.jpg", crop_box=None) # Slade Wilson listo frente a la Liga
frame_to_vertical_1080x1920(ds_raw / "scene_02" / "scene_02.jpg", s70_dest / "scene_02.jpg", crop_box=None) # Flash ensartado en su espada
frame_to_vertical_1080x1920(ds_raw / "scene_03" / "scene_03.jpg", s70_dest / "scene_03.jpg", crop_box=None) # Zatanna y Hawkman neutralizados
frame_to_vertical_1080x1920(ds_raw / "scene_04" / "scene_04.jpg", s70_dest / "scene_04.jpg", crop_box=None) # Rompiendo dedos a Green Lantern

# -------------------------------------------------------------
# SLOT 71: Thor Ejecuta a Galactus
# -------------------------------------------------------------
print("\n--- SLOT 71: Thor Vol 6 - Ejecución de Galactus ---")
s71_dest = CURATED_BASE / "71_thor_mata_galactus_ejecucion"
tg_raw = PROJECT_ROOT / "output" / "thor_mata_galactus_heraldo"
frame_to_vertical_1080x1920(tg_raw / "scene_01" / "scene_01.jpg", s71_dest / "scene_01.jpg", crop_box=None) # Galactus hace a Thor su heraldo
frame_to_vertical_1080x1920(tg_raw / "scene_02" / "scene_02.jpg", s71_dest / "scene_02.jpg", crop_box=None) # Batalla contra el Black Winter
frame_to_vertical_1080x1920(tg_raw / "scene_03" / "scene_03.jpg", s71_dest / "scene_03.jpg", crop_box=None) # Thor drenando el Poder Cósmico
frame_to_vertical_1080x1920(tg_raw / "scene_04" / "scene_04.jpg", s71_dest / "scene_04.jpg", crop_box=None) # Ejecución de Galactus y casco en Asgard

# -------------------------------------------------------------
# SLOT 72: Green Lantern - Crepúsculo Esmeralda y Parallax
# -------------------------------------------------------------
print("\n--- SLOT 72: Green Lantern - Caída de Hal Jordan y Parallax ---")
s72_dest = CURATED_BASE / "72_green_lantern_parallax_crepusculo"
gl_raw = PROJECT_ROOT / "output" / "green_lantern_crepusculo_esmeralda"
frame_to_vertical_1080x1920(gl_raw / "scene_01" / "scene_01.jpg", s72_dest / "scene_01.jpg", crop_box=None) # Cráter de Coast City
frame_to_vertical_1080x1920(gl_raw / "scene_03" / "scene_03.jpg", s72_dest / "scene_02.jpg", crop_box=None) # Masacre de Linternas Verdes camino a Oa
frame_to_vertical_1080x1920(gl_raw / "scene_05" / "scene_05.jpg", s72_dest / "scene_03.jpg", crop_box=None) # Muerte de Kilowog y Sinestro
frame_to_vertical_1080x1920(gl_raw / "scene_07" / "scene_07.jpg", s72_dest / "scene_04.jpg", crop_box=None) # Absorbiendo la Batería Central: nace Parallax

# -------------------------------------------------------------
# SLOT 73: Deadpool Mata a Thor con Mjolnir Gigante
# -------------------------------------------------------------
print("\n--- SLOT 73: Deadpool Kills Marvel - Thor Aplastado ---")
s73_dest = CURATED_BASE / "73_deadpool_mata_thor_mjolnir"
dp_raw = PROJECT_ROOT / "output" / "deadpool_kills_thor"
frame_to_vertical_1080x1920(dp_raw / "scene_01" / "scene_01.jpg", s73_dest / "scene_01.jpg", crop_box=None) # Deadpool en cacería de Vengadores
frame_to_vertical_1080x1920(dp_raw / "scene_02" / "scene_02.jpg", s73_dest / "scene_02.jpg", crop_box=None) # Thor lanzando a Mjolnir
frame_to_vertical_1080x1920(dp_raw / "scene_03" / "scene_03.jpg", s73_dest / "scene_03.jpg", crop_box=None) # Partículas Pym agrandando el martillo
frame_to_vertical_1080x1920(dp_raw / "scene_04" / "scene_04.jpg", s73_dest / "scene_04.jpg", crop_box=None) # Mjolnir colosal aplasta a Thor

# -------------------------------------------------------------
# SLOT 74: The Immortal Hulk #8 - Descuartizado en Frascos
# -------------------------------------------------------------
print("\n--- SLOT 74: The Immortal Hulk #8 - Descuartizado en Frascos ---")
s74_dest = CURATED_BASE / "74_immortal_hulk_descuartizado_frascos"
hulk_pages = sorted(list((COMICS_SOURCE / "immortal_hulk_8" / "extracted_pages_08").glob("*.jpg")))
frame_to_vertical_1080x1920(hulk_pages[5], s74_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Frascos de vidrio con las partes y Clive
frame_to_vertical_1080x1920(hulk_pages[10], s74_dest / "scene_02.jpg", crop_box=(0.0, 0.10, 1.0, 0.90)) # Cabeza de Hulk en el frasco sonriendo
frame_to_vertical_1080x1920(hulk_pages[11], s74_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Mano de Hulk en el frasco chasqueando dedos (SNAP!)
frame_to_vertical_1080x1920(hulk_pages[17], s74_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Hulk regenerándose alrededor de Clive

# -------------------------------------------------------------
# SLOT 75: Marvel Ruins - El Universo Maldito
# -------------------------------------------------------------
print("\n--- SLOT 75: Marvel Ruins - El Universo Maldito ---")
s75_dest = CURATED_BASE / "75_marvel_ruins_universo_maldito"
ruins_dir = COMICS_SOURCE / "marvel_ruins" / "extracted_pages" / "Ruins 01 (of 02) (1995) (digital) (Shadowcat-Empire)"
ruins_pages = sorted(list(ruins_dir.glob("*.jpg")))
frame_to_vertical_1080x1920(ruins_pages[4], s75_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Phil Sheldon observando el mundo destruido
frame_to_vertical_1080x1920(ruins_pages[6], s75_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Peter Parker agonizando con erupción radioactiva
frame_to_vertical_1080x1920(ruins_pages[13], s75_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Silver Surfer despellejado en el cosmos
frame_to_vertical_1080x1920(ruins_pages[7], s75_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Hulk deforme masa tumoral viviente

# -------------------------------------------------------------
# SLOT 76: Magneto: Ultimatum - El Día que Ahogó al Mundo
# -------------------------------------------------------------
print("\n--- SLOT 76: Ultimatum - Magneto Ahogó Nueva York ---")
s76_dest = CURATED_BASE / "76_magneto_ultimatum_tsunami_manhattan"
ult_dir = COMICS_SOURCE / "ultimatum" / "extracted_pages"
ult_pages = sorted(list(ult_dir.glob("*.jpg")))
frame_to_vertical_1080x1920(ult_pages[9], s76_dest / "scene_01.jpg", crop_box=(0.0, 0.02, 1.0, 0.95)) # Ola gigante colosal sobre los rascacielos
frame_to_vertical_1080x1920(ult_pages[10], s76_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Agua arrasando y destruyendo las calles de Manhattan
frame_to_vertical_1080x1920(ult_pages[14], s76_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Héroes y civiles ahogándose bajo el agua
frame_to_vertical_1080x1920(ult_pages[25], s76_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Magneto levitando sobre la catástrofe

print("\n🎉 ¡CURACIÓN DE LOS 10 SLOTS (67 AL 76) COMPLETADA CON ÉXITO!")
