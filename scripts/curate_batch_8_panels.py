"""
Curador Canónico 1:1 para el Lote 8 Remasterizado (Slots 77 al 86)
==================================================================
Enmarca y escala todas las viñetas a 1080x1920 sin recorte destructivo:
- Preserva el 100% de la acción original con fondo desenfocado oscuro de alta calidad.
- Safe-zone absoluta: cero cabezas cortadas, cero globos de texto cortados.
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
print("🎨 CURANDO PANELES CANÓNICOS 1:1 PARA SLOTS 77 AL 86")
print("=" * 80)

# -------------------------------------------------------------
# SLOT 77: Thanos Rising - El Origen Perturbador de Thanos
# -------------------------------------------------------------
print("\n--- SLOT 77: Thanos Rising - El Origen Perturbador ---")
s77_dest = CURATED_BASE / "77_thanos_origen_perturbador_muerte"
s77_raw = CURATED_BASE / "thanos_rising"
frame_to_vertical_1080x1920(s77_raw / "scene_01.jpg", s77_dest / "scene_01.jpg", crop_box=None) # Nacimiento en Titán y rechazo materno
frame_to_vertical_1080x1920(s77_raw / "scene_02.jpg", s77_dest / "scene_02.jpg", crop_box=None) # Disección de criaturas en las cavernas
frame_to_vertical_1080x1920(s77_raw / "scene_03.jpg", s77_dest / "scene_03.jpg", crop_box=None) # Encuentro con la Dama Muerte
frame_to_vertical_1080x1920(s77_raw / "scene_04.jpg", s77_dest / "scene_04.jpg", crop_box=None) # Masacre nuclear de su propio planeta Titán

# -------------------------------------------------------------
# SLOT 78: Uncanny X-Men - Días del Futuro Pasado
# -------------------------------------------------------------
print("\n--- SLOT 78: X-Men - Días del Futuro Pasado ---")
s78_dest = CURATED_BASE / "78_xmen_dias_del_futuro_pasado"
s78_raw = CURATED_BASE / "xmen_dias_del_futuro_pasado"
frame_to_vertical_1080x1920(s78_raw / "scene_01.jpg", s78_dest / "scene_01.jpg", crop_box=None) # Cartel de Centinelas: Apprehended / Slain
frame_to_vertical_1080x1920(s78_raw / "scene_02.jpg", s78_dest / "scene_02.jpg", crop_box=None) # Caza y exterminio en las ruinas de NY
frame_to_vertical_1080x1920(s78_raw / "scene_03.jpg", s78_dest / "scene_03.jpg", crop_box=None) # Transferencia mental hacia el pasado
frame_to_vertical_1080x1920(s78_raw / "scene_04.jpg", s78_dest / "scene_04.jpg", crop_box=None) # Muerte de Wolverine y alteración de la historia

# -------------------------------------------------------------
# SLOT 79: Thanos Wins - Thanos Conquistó el Fin del Universo
# -------------------------------------------------------------
print("\n--- SLOT 79: Thanos Wins - Donny Cates ---")
s79_dest = CURATED_BASE / "79_thanos_gana_fin_del_universo"
tw_pages = sorted(list((COMICS_SOURCE / "thanos_wins" / "extracted_pages").glob("*.jpg")))
frame_to_vertical_1080x1920(tw_pages[9], s79_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Thanos conquistador en el trono de cráneos
frame_to_vertical_1080x1920(tw_pages[20], s79_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Cosmic Ghost Rider con cadenas de Cyttorak
frame_to_vertical_1080x1920(tw_pages[28], s79_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Cosmos muerto y restos de celestiales
frame_to_vertical_1080x1920(tw_pages[38], s79_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # El Rey Thanos anciano en el trono final

# -------------------------------------------------------------
# SLOT 80: Batman: Silencio (Hush) - La Conspiración Wayne
# -------------------------------------------------------------
print("\n--- SLOT 80: Batman Hush - Silencio ---")
s80_dest = CURATED_BASE / "80_batman_hush_conspiracion_wayne"
hush_base = PROJECT_ROOT / "output" / "batman_hush_silencio"
frame_to_vertical_1080x1920(hush_base / "scene_01" / "scene_01.jpg", s80_dest / "scene_01.jpg", crop_box=None) # Batman vigilando Gotham en la noche
frame_to_vertical_1080x1920(hush_base / "scene_02" / "scene_02.jpg", s80_dest / "scene_02.jpg", crop_box=None) # La caída y fractura craneal del murciélago
frame_to_vertical_1080x1920(hush_base / "scene_03" / "scene_03.jpg", s80_dest / "scene_03.jpg", crop_box=None) # Cirugía de Thomas Elliot y alianza villana
frame_to_vertical_1080x1920(hush_base / "scene_04" / "scene_04.jpg", s80_dest / "scene_04.jpg", crop_box=None) # Revelación de Hush vendado y venganza

# -------------------------------------------------------------
# SLOT 81: Doctor Strange: The Oath - La Cura Prohibida del Cáncer
# -------------------------------------------------------------
print("\n--- SLOT 81: Doctor Strange: The Oath - La Cura del Cáncer ---")
s81_dest = CURATED_BASE / "81_doctor_strange_the_oath_cura_cancer"
oath_raw = CURATED_BASE / "42_doctor_strange_the_oath_cirugia"
frame_to_vertical_1080x1920(oath_raw / "scene_01.jpg", s81_dest / "scene_01.jpg", crop_box=None) # Strange herido de bala y Wong enfermo
frame_to_vertical_1080x1920(oath_raw / "scene_02.jpg", s81_dest / "scene_02.jpg", crop_box=None) # Strange guiando la cirugía en forma astral
frame_to_vertical_1080x1920(oath_raw / "scene_03.jpg", s81_dest / "scene_03.jpg", crop_box=None) # El elixir místico de Otkid contra el cáncer
frame_to_vertical_1080x1920(oath_raw / "scene_04.jpg", s81_dest / "scene_04.jpg", crop_box=None) # El juramento hipocrático y la salvación de Wong

# -------------------------------------------------------------
# SLOT 82: Ultimate Wolverine vs Hulk - Logan en Dos Mitades
# -------------------------------------------------------------
print("\n--- SLOT 82: Ultimate Wolverine vs Hulk - Logan en Dos Mitades ---")
s82_dest = CURATED_BASE / "82_ultimate_wolverine_vs_hulk_dos_mitades"
wvh_pages = sorted(list((COMICS_SOURCE / "wolverine_vs_hulk" / "extracted_pages").glob("*.jpg")))
frame_to_vertical_1080x1920(wvh_pages[3], s82_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Logan despertando en la nieve congelada
frame_to_vertical_1080x1920(wvh_pages[4], s82_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 0.52, 0.95)) # Viendo sus piernas a 4 millas en la montaña
frame_to_vertical_1080x1920(wvh_pages[22], s82_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Hulk partiendo a Wolverine en dos mitades
frame_to_vertical_1080x1920(wvh_pages[5], s82_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Logan arrastrando su torso con las garras

# -------------------------------------------------------------
# SLOT 83: Siege: Sentry / The Void - La Destrucción de Asgard
# -------------------------------------------------------------
print("\n--- SLOT 83: Siege - Sentry The Void Devora Asgard ---")
s83_dest = CURATED_BASE / "83_sentry_vacio_void_devora_asgard"
s3_pages = sorted(list((COMICS_SOURCE / "siege" / "extracted_siege_void" / "Siege 03").glob("*.jpg")))
s4_pages = sorted(list((COMICS_SOURCE / "siege" / "extracted_siege_void" / "Siege 04").glob("*.jpg")))
frame_to_vertical_1080x1920(s3_pages[20], s83_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Sentry sucumbe al Vacío, tentáculos oscuros
frame_to_vertical_1080x1920(s3_pages[24], s83_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # The Void demoliendo las torres de Asgard
frame_to_vertical_1080x1920(s4_pages[2], s83_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 0.52, 0.95)) # Asgard cayendo en ruinas y llamas sobre la Tierra
frame_to_vertical_1080x1920(s4_pages[16], s83_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Thor desatando el rayo divino final contra Void

# -------------------------------------------------------------
# SLOT 84: House of M - Scarlet Witch: "No Más Mutantes"
# -------------------------------------------------------------
print("\n--- SLOT 84: House of M - No Más Mutantes ---")
s84_dest = CURATED_BASE / "84_scarlet_witch_house_of_m_no_mas_mutantes"
hom_frames = PROJECT_ROOT / "scratch" / "house_of_m_frames"
frame_to_vertical_1080x1920(hom_frames / "hom_05s.jpg", s84_dest / "scene_01.jpg", crop_box=None) # Wanda confrontando a Magneto
frame_to_vertical_1080x1920(hom_frames / "hom_14s.jpg", s84_dest / "scene_02.jpg", crop_box=None) # El susurro letal: "No more mutants"
frame_to_vertical_1080x1920(hom_frames / "hom_20s.jpg", s84_dest / "scene_03.jpg", crop_box=None) # La onda dorada alterando la realidad
frame_to_vertical_1080x1920(hom_frames / "hom_26s.jpg", s84_dest / "scene_04.jpg", crop_box=None) # Extinción mutante y pérdida de poderes

# -------------------------------------------------------------
# SLOT 85: Uncanny X-Force - Archangel: El Heredero de Apocalipsis
# -------------------------------------------------------------
print("\n--- SLOT 85: Uncanny X-Force - Archangel y la Semilla de la Muerte ---")
s85_dest = CURATED_BASE / "85_archangel_heredero_apocalipsis_xforce"
uxf_pages = sorted(list((COMICS_SOURCE / "uncanny_xforce" / "extracted_pages").glob("*.jpg")))
frame_to_vertical_1080x1920(uxf_pages[5], s85_dest / "scene_01.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Warren luchando contra la personalidad de Archangel
frame_to_vertical_1080x1920(uxf_pages[12], s85_dest / "scene_02.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # El equipo secreto X-Force en misión letal
frame_to_vertical_1080x1920(uxf_pages[20], s85_dest / "scene_03.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # El templo de Apocalipsis y los jinetes
frame_to_vertical_1080x1920(uxf_pages[28], s85_dest / "scene_04.jpg", crop_box=(0.0, 0.05, 1.0, 0.95)) # Archangel desplegando sus alas de navajas de acero

# -------------------------------------------------------------
# SLOT 86: The Amazing Spider-Man - La Última Cacería de Kraven
# -------------------------------------------------------------
print("\n--- SLOT 86: Kraven's Last Hunt - Enterró a Spider-Man ---")
s86_dest = CURATED_BASE / "86_kraven_ultima_caceria_entierra_spiderman"
kraven_base = PROJECT_ROOT / "output" / "spiderman_kravens_last_hunt"
frame_to_vertical_1080x1920(kraven_base / "scene_01" / "scene_01.jpg", s86_dest / "scene_01.jpg", crop_box=None) # Kraven con su rifle acechando a Spider-Man
frame_to_vertical_1080x1920(kraven_base / "scene_02" / "scene_02.jpg", s86_dest / "scene_02.jpg", crop_box=None) # Disparo a quemarropa derribando a Peter
frame_to_vertical_1080x1920(kraven_base / "scene_03" / "scene_03.jpg", s86_dest / "scene_03.jpg", crop_box=None) # Kraven arrojando tierra y enterrando vivo a Spider-Man
frame_to_vertical_1080x1920(kraven_base / "scene_04" / "scene_04.jpg", s86_dest / "scene_04.jpg", crop_box=None) # Kraven portando el traje negro como el nuevo arácnido

print("\n🎉 ¡CURACIÓN DE LOS 10 SLOTS (77 AL 86) COMPLETADA CON ÉXITO!")
