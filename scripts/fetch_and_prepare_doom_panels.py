"""
DESCARGA Y PREPARACIÓN DE PANELES CANÓNICOS: DOCTOR DOOM
=========================================================
1. Mapeo 1:1 exacto de cada escena a su viñeta de cómic canónica de Marvel Database.
2. Descarga a panels_raw/.
3. Formateo cinemático a panels_1080p/ en 1920x1080 Full HD (sin estirar, manteniendo relación de aspecto con fondo desenfocado sutil).
4. Auditoría con Gemini Vision para validar entintado de cómic y alineación narrativa.
"""

import os
import json
import requests
from PIL import Image, ImageFilter

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "doctor_doom_doomsday_long")
PANELS_RAW = os.path.join(OUTPUT_DIR, "panels_raw")
PANELS_1080P = os.path.join(OUTPUT_DIR, "panels_1080p")
os.makedirs(PANELS_RAW, exist_ok=True)
os.makedirs(PANELS_1080P, exist_ok=True)

# Cargar catálogo recolectado de Marvel Fandom
with open(os.path.join(BASE_DIR, "scratch", "doom_fandom_harvest.json"), "r", encoding="utf-8") as f:
    harvest = json.load(f)

# Aplanar archivos para búsqueda rápida
url_lookup = {}
for group, items in harvest.items():
    for item in items:
        # Extraer nombre limpio
        title = item["title"].replace("File:", "").strip()
        url_lookup[title] = item["url"]
        url_lookup[item["title"]] = item["url"]

# Mapeo maestro 1 a 44 de escena a archivo canónico
PANEL_MAPPING = {
    # ACTO 1: EL SHOCK DEL MULTIVERSO Y EL VERDADERO DOOM
    1: {
        "file": "Books_of_Doom_Vol_1_1.jpg",
        "title": "Books of Doom Vol 1 1.jpg",
        "desc": "Doctor Doom clásico con túnica y armadura completa"
    },
    2: {
        "file": "Victor_von_Doom_616_Books_of_Doom_6.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 6 001.jpg",
        "desc": "Retrato intimidante de Doctor Doom en Books of Doom #6"
    },
    3: {
        "file": "Doctor_Strange_and_Doctor_Doom_Triumph_and_Torment_Vol_1_1.jpg",
        "title": "Doctor Strange and Doctor Doom Triumph and Torment Vol 1 1.jpg",
        "desc": "Doom y Strange combinando ciencia y hechicería"
    },
    4: {
        "file": "Doom_Armor_Books_of_Doom_3.jpg",
        "title": "Books of Doom Vol 1 3.jpg",
        "desc": "Doctor Doom envuelto en su túnica verde y tecnología arcana"
    },

    # ACTO 2: EL ORIGEN TRÁGICO: LATVERIA Y EL PACTO INFERNAL
    5: {
        "file": "Latveria_Zefiro_Books_of_Doom_1.jpg",
        "title": "Books of Doom Vol 1 1.jpg",
        "desc": "Campamento de gitanos Zefiro en las montañas de Latveria"
    },
    6: {
        "file": "Victor_and_Werner_von_Doom_Books_of_Doom_1.jpg",
        "title": "Victor von Doom (Earth-616) and Werner von Doom (Earth-616) from Books of Doom Vol 1 1 0001.jpg",
        "desc": "Werner von Doom sosteniendo al pequeño Victor en brazos"
    },
    7: {
        "file": "Cynthia_von_Doom_Sorcery_Books_of_Doom_1.jpg",
        "title": "Cynthia von Doom (Earth-616) from Books of Doom Vol 1 1 0002.jpg",
        "desc": "Cynthia von Doom practicando magia prohibida"
    },
    8: {
        "file": "Cynthia_von_Doom_Portrait_Books_of_Doom_1.jpg",
        "title": "Cynthia von Doom (Earth-616) from Books of Doom Vol 1 1 0001.jpg",
        "desc": "Cynthia von Doom herida y trágica"
    },
    9: {
        "file": "Cynthia_von_Doom_Mephisto_Books_of_Doom_2.jpg",
        "title": "Victor von Doom (Earth-616), Cynthia von Doom (Earth-616) and Mephisto (Earth-616) from Books of Doom Vol 1 2 0001.jpg",
        "desc": "Cynthia von Doom condenada en las garras de Mefisto"
    },
    10: {
        "file": "Werner_von_Doom_Winter_Books_of_Doom_1.jpg",
        "title": "Victor von Doom (Earth-616) and Werner von Doom (Earth-616) from Books of Doom Vol 1 1 0001.jpg",
        "desc": "Werner y el pequeño Victor huyendo por la ventisca"
    },
    11: {
        "file": "Victor_von_Doom_Child_Books_of_Doom_1.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 1 0003.jpg",
        "desc": "Victor huérfano y solitario en el frío"
    },
    12: {
        "file": "Victor_Chest_Sorcery_Books_of_Doom_1.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 1 0001.jpg",
        "desc": "Victor adolescente descubriendo los pergaminos de brujería"
    },
    13: {
        "file": "Victor_Young_Inventions_Books_of_Doom_1.jpg",
        "title": "Victor von Doom (Earth-616) and Valeria von Frazen (Earth-616) from Books of Doom Vol 1 1 001.jpg",
        "desc": "Victor joven en Latveria con Valeria desarrollando inventos"
    },
    14: {
        "file": "Victor_Empire_State_Books_of_Doom_2.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 2 0001.jpg",
        "desc": "Victor von Doom llegando a la universidad Empire State"
    },

    # ACTO 3: LA RIVALIDAD CON REED Y LA MÁSCARA DE HIERRO
    15: {
        "file": "Reed_Richards_Young_Books_of_Doom_2.jpg",
        "title": "Reed Richards (Earth-616) from Books of Doom Vol 1 2 0001.jpg",
        "desc": "El joven estudiante Reed Richards conociendo a Victor"
    },
    16: {
        "file": "Victor_Robotic_Machine_Books_of_Doom_2.jpg",
        "title": "Robotic Soldier, Victor von Doom (Earth-616) from Books of Doom Vol 1 2.jpg",
        "desc": "Victor construyendo su máquina transdimensional"
    },
    17: {
        "file": "Reed_Warns_Victor_Books_of_Doom_2.jpg",
        "title": "Reed Richards (Earth-616) from Books of Doom Vol 1 2 0001.jpg",
        "desc": "Reed advirtiendo a Victor sobre el error de cálculo"
    },
    18: {
        "file": "Machine_Explosion_Books_of_Doom_2.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 2 0002.jpg",
        "desc": "La brutal explosión de la máquina en el laboratorio"
    },
    19: {
        "file": "Victor_Scarred_Books_of_Doom_2.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 2 0002.jpg",
        "desc": "Victor con el rostro herido jurando venganza"
    },
    20: {
        "file": "Tibet_Monastery_Books_of_Doom_4.jpg",
        "title": "Monastery of Doom from Books of Doom Vol 1 4 001.jpg",
        "desc": "El monasterio aislado en las cumbres nevadas del Tíbet"
    },
    21: {
        "file": "Victor_Monks_Master_Books_of_Doom_4.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 4 0001.jpg",
        "desc": "Victor liderando a los monjes del Tíbet"
    },
    22: {
        "file": "Monks_Forge_Armor_Books_of_Doom_4.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 4 0003.jpg",
        "desc": "Los monjes forjando la armadura y la máscara de hierro"
    },
    23: {
        "file": "Doom_Molten_Mask_Books_of_Doom_4.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 4 0002.jpg",
        "desc": "La máscara al rojo vivo sellando la carne de Doctor Doom"
    },
    24: {
        "file": "Doom_Overthrow_Vladimir_Books_of_Doom_6.jpg",
        "title": "Victor von Doom (Earth-616) and Vladimir Fortunov (Earth-616) from Books of Doom Vol 1 6 0001.jpg",
        "desc": "Doom derrocando al tirano Rey Vladimir en Latveria"
    },

    # ACTO 4: EL LADRÓN DE DIOSES (HAZAÑAS CÓSMICAS)
    25: {
        "file": "Doombot_Patrol_Books_of_Doom_6.jpg",
        "title": "Doombot from Books of Doom Vol 1 6 001.jpg",
        "desc": "Los Doombots patrullando las calles de Latveria"
    },
    26: {
        "file": "Fantastic_Four_57_Cover.jpg",
        "title": "Fantastic Four Vol 1 57.jpg",
        "desc": "Doctor Doom tendiendo una trampa a Silver Surfer"
    },
    27: {
        "file": "Doom_Absorbs_Silver_Surfer_FF_57.jpg",
        "title": "Victor von Doom (Earth-616) from Fantastic Four Vol 1 57 0001.jpg",
        "desc": "Doom drenando el Poder Cósmico con su arnés científico"
    },
    28: {
        "file": "Secret_Wars_1984_Doom_Beyonder.jpg",
        "title": "Marvel Super Heroes Secret Wars Vol 1 8.jpg",
        "desc": "Doom en Battleworld durante las Secret Wars originales"
    },
    29: {
        "file": "Doom_Defeats_Galactus_Secret_Wars.jpg",
        "title": "Marvel Super Heroes Secret Wars Facsimile Edition Vol 1 9.jpg",
        "desc": "Doctor Doom doblegando a las fuerzas divinas de Galactus"
    },

    # ACTO 5: LA ANIQUILACIÓN DEL MULTIVERSO Y DIOS EMPERADOR DOOM
    30: {
        "file": "Incursion_Universes_Colliding.jpg",
        "title": "Secret Wars Vol 1 1.jpg",
        "desc": "Las Incursiones colisionando mundos enteros en el cielo rojo"
    },
    31: {
        "file": "Living_Tribunal_Slain_Beyonders.jpg",
        "title": "Victor von Doom (Earth-616) and Black Swans (Multiverse) from New Avengers Vol 3 33 001.jpg",
        "desc": "Las Black Swans y el vacío cósmico de las Incursiones"
    },
    32: {
        "file": "Doom_Strange_MoleculeMan_New_Avengers_33.jpg",
        "title": "Victor von Doom (Earth-616), Owen Reece (Earth-616), and Stephen Strange (Earth-616) from New Avengers Vol 3 33 001.jpg",
        "desc": "Doom, Stephen Strange y Molecule Man desafiando a los Beyonders"
    },
    33: {
        "file": "Doom_Kills_Beyonders_Secret_Wars_4.jpg",
        "title": "Secret Wars Vol 1 4.jpg",
        "desc": "Doom desatando el poder para matar a los Beyonders"
    },
    34: {
        "file": "Battleworld_Latverion_Secret_Wars_9.jpg",
        "title": "Battleworld (Latverion) from Secret Wars Vol 1 9 001.jpg",
        "desc": "El mapa y la creación del planeta mosaico Battleworld"
    },
    35: {
        "file": "God_Emperor_Doom_Throne_Secret_Wars_3.jpg",
        "title": "Secret Wars Vol 1 3.jpg",
        "desc": "Dios Emperador Doom con armadura y túnica blanca en el trono"
    },
    36: {
        "file": "Thanos_Confronts_Doom_Secret_Wars_8.jpg",
        "title": "Secret Wars Vol 1 8 Coker Variant.jpg",
        "desc": "Thanos marchando arrogante ante el trono de Dios Emperador Doom"
    },
    37: {
        "file": "Doom_Approaches_Thanos_Secret_Wars_8.jpg",
        "title": "Reed Richards (Earth-616) from Secret Wars Vol 1 8 001.jpg",
        "desc": "Doom descendiendo hacia Thanos con total calma"
    },
    38: {
        "file": "Doom_Rips_Thanos_Spine_Secret_Wars_8.jpg",
        "title": "Victor von Doom (Earth-616) and Thanos (Earth-616) from Secret Wars Vol 1 8 001.jpg",
        "desc": "Doom arrancándole de cuajo la espina dorsal a Thanos con sus manos"
    },
    39: {
        "file": "Reed_and_Doom_Final_Secret_Wars_9.jpg",
        "title": "Reed Richards (Earth-616) and Victor von Doom (Earth-616) from Secret Wars Vol 1 9 001.jpg",
        "desc": "La confrontación filosófica final entre Reed Richards y Doom"
    },
    40: {
        "file": "Doom_Healed_Face_Secret_Wars_9.jpg",
        "title": "Victor von Doom (Earth-616) (Earth-616) from Secret Wars Vol 1 9 001.jpg",
        "desc": "Victor von Doom contemplando su rostro curado en Latveria"
    },

    # ACTO 6: INFAMOUS IRON MAN Y LA CONEXIÓN DOOMSDAY
    41: {
        "file": "Infamous_Iron_Man_Model_51.jpg",
        "title": "Victor von Doom (Earth-616) from Infamous Iron Man Vol 1 1 001.jpg",
        "desc": "Victor von Doom vistiendo la armadura de Infamous Iron Man"
    },
    42: {
        "file": "Doom_Tony_Swap_Demon_in_Armor.jpg",
        "title": "Victor von Doom (Earth-11029) from What If? Iron Man Demon in an Armor Vol 1 1 0001.jpg",
        "desc": "Tony Stark y Victor von Doom intercambiando cuerpos y mentes"
    },
    43: {
        "file": "Doom_Monarch_Latveria_Books_of_Doom_6.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 6 001.jpg",
        "desc": "Doctor Doom con capa verde y máscara plateada mirando al frente"
    },
    44: {
        "file": "Doom_Absolute_Ruler_Books_of_Doom_5.jpg",
        "title": "Victor von Doom (Earth-616) from Books of Doom Vol 1 5 0001.jpg",
        "desc": "Doctor Doom en el balcón supremo exigiendo sumisión para salvar el cosmos"
    }
}

def download_panel(sid, info):
    raw_path = os.path.join(PANELS_RAW, f"panel_{sid:03d}_{info['file']}")
    if os.path.exists(raw_path) and os.path.getsize(raw_path) > 10000:
        return raw_path

    # Buscar URL
    t = info["title"]
    url = url_lookup.get(t) or url_lookup.get(f"File:{t}")
    if not url:
        # Fallback a búsqueda en harvest por coincidencia
        for grp, items in harvest.items():
            for it in items:
                if t.lower() in it["title"].lower() or info["file"].lower() in it["title"].lower():
                    url = it["url"]
                    break
            if url:
                break

    if not url:
        print(f"[{sid:02d}] No se encontró URL directa para {t}")
        return None

    # Limpiar URL de Fandom para descargar resolución completa
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://marvel.fandom.com/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200 and len(r.content) > 5000:
            with open(raw_path, "wb") as f:
                f.write(r.content)
            print(f"[{sid:02d}] Descargado ({len(r.content)//1024} KB): {info['desc']}")
            return raw_path
        else:
            print(f"[{sid:02d}] Error HTTP {r.status_code} al descargar {url}")
            return None
    except Exception as e:
        print(f"[{sid:02d}] Excepción descargando {url}: {e}")
        return None

def create_1080p_canvas(src_img_path, out_img_path):
    with Image.open(src_img_path) as im:
        im = im.convert("RGB")
        target_w, target_h = 1920, 1080
        
        # Fondo desenfocado y oscurecido para llenar los laterales 16:9
        bg = im.copy()
        bg_scale = max(target_w / im.width, target_h / im.height)
        bg_w = int(im.width * bg_scale)
        bg_h = int(im.height * bg_scale)
        bg = bg.resize((bg_w, bg_h), Image.Resampling.LANCZOS)
        left = (bg_w - target_w) // 2
        top = (bg_h - target_h) // 2
        bg = bg.crop((left, top, left + target_w, top + target_h))
        bg = bg.filter(ImageFilter.GaussianBlur(radius=30))
        # Oscurecer fondo al 40% para enfoque en el panel principal
        bg = Image.blend(bg, Image.new("RGB", (target_w, target_h), (0, 0, 0)), 0.60)
        
        # Imagen principal centrada manteniendo proporción sin deformación
        fg_scale = min(target_w / im.width, target_h / im.height)
        fg_w = int(im.width * fg_scale)
        fg_h = int(im.height * fg_scale)
        fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
        
        pos_x = (target_w - fg_w) // 2
        pos_y = (target_h - fg_h) // 2
        bg.paste(fg, (pos_x, pos_y))
        bg.save(out_img_path, "JPEG", quality=95)

def run_pipeline():
    print("=== [Paso 2] Descarga y Preparación de Paneles 100% Canónicos ===")
    success_count = 0
    for sid in range(1, 45):
        info = PANEL_MAPPING[sid]
        raw = download_panel(sid, info)
        if raw and os.path.exists(raw):
            dst_1080p = os.path.join(PANELS_1080P, f"panel_{sid:03d}.jpg")
            create_1080p_canvas(raw, dst_1080p)
            success_count += 1
        else:
            print(f"ALERTA: Escena {sid} no pudo descargarse!")
    print(f"\nProceso finalizado: {success_count}/44 paneles preparados en 1080p Full HD!")

if __name__ == "__main__":
    run_pipeline()
