"""
HARVEST Y CURACIÓN DE PANELES 1080x1920 PARA BATCH 5 (SLOTS 41 AL 50)
=====================================================================
Descarga los paneles canónicos en alta resolución desde las wikis oficiales
(marvel.fandom.com y dc.fandom.com) para los 10 proyectos de Batch 5 y los
procesa a 1080x1920 Full HD vertical.
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.cloud_runner import create_full_panel_frame

CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
CURATED_BASE.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

SLOTS = [
    {
        "slot": 41,
        "folder": "41_superman_black_mercy_mongul",
        "wiki": "dc.fandom.com",
        "category": "Superman Annual Vol 1 11/Images",
        "search": "Superman Black Mercy Mongul Van-El Annual 11",
        "specific_files": [
            "File:Black Mercy 0001.jpg",
            "File:Superman Annual Vol 1 11.jpg",
            "File:Mongul (New Earth) 0001.jpg",
            "File:Black Mercy (New Earth) 001.jpg"
        ]
    },
    {
        "slot": 42,
        "folder": "doctor_strange_the_oath",
        "wiki": "marvel.fandom.com",
        "category": "Doctor Strange: The Oath Vol 1 1/Images",
        "search": "Doctor Strange The Oath Linda Carter Night Nurse",
        "specific_files": [] # Ya tiene paneles locales listos
    },
    {
        "slot": 43,
        "folder": "43_flashpoint_carta_thomas_wayne",
        "wiki": "dc.fandom.com",
        "category": "Flashpoint Vol 2 5/Images",
        "search": "Thomas Wayne letter Bruce Flashpoint 5",
        "specific_files": [
            "File:Flashpoint Vol 2 5 Textless.jpg",
            "File:Thomas Wayne (Flashpoint Timeline) 0002.jpg",
            "File:Flashpoint Vol 2 5 Textless Variant.jpg",
            "File:Pandora 0001.jpg"
        ]
    },
    {
        "slot": 44,
        "folder": "44_punisher_the_end_bunker",
        "wiki": "marvel.fandom.com",
        "category": "Punisher: The End Vol 1 1/Images",
        "search": "Francis Castle Earth-40616 Punisher The End",
        "specific_files": [
            "File:Francis Castle (Earth-40616) from Punisher The End Vol 1 1.jpg",
            "File:Paris Peters (Earth-40616) from Punisher The End Vol 1 1 001.jpg",
            "File:Punisher The End Vol 1 1 Textless.jpg",
            "File:Punisher The End Vol 1 1.jpg"
        ]
    },
    {
        "slot": 45,
        "folder": "45_annihilation_drax_thanos_corazon",
        "wiki": "marvel.fandom.com",
        "category": "Annihilation Vol 1 4/Images",
        "search": "Arthur Douglas and Thanos Annihilation 4",
        "specific_files": [
            "File:Arthur Douglas and Thanos (Earth-616) from Annihilation Vol 1 4 0001.jpg",
            "File:Annihilation Vol 1 4 Textless.jpg",
            "File:Annihilation Vol 1 4.jpg",
            "File:Caul 7 from Annihilation Vol 1 4 001.png"
        ]
    },
    {
        "slot": 46,
        "folder": "46_daredevil_muerte_karen_page",
        "wiki": "marvel.fandom.com",
        "category": "Daredevil Vol 2 5/Images",
        "search": "Daredevil Bullseye Karen Page Guardian Devil 5",
        "specific_files": [
            "File:Daredevil Vol 2 5 Textless.jpg",
            "File:Daredevil Vol 2 5 Quesada Variant Textless.jpg",
            "File:Daredevil Vol 2 5.jpg",
            "File:Daredevil Vol 2 5 Quesada Variant.jpg"
        ]
    },
    {
        "slot": 47,
        "folder": "47_carnage_usa_dover_oklahoma",
        "wiki": "marvel.fandom.com",
        "category": "Carnage: U.S.A. Vol 1 1/Images",
        "search": "Doverton Carnage U.S.A. Vol 1 1",
        "specific_files": [
            "File:Doverton from Carnage, U.S.A. Vol 1 1 0001.jpg",
            "File:Randolph (Doverton) (Earth-616) from Carnage, U.S.A. Vol 1 1 001.jpg",
            "File:Robbie (Doverton) (Earth-616) from Carnage, U.S.A. Vol 1 1 001.jpg",
            "File:Carnage, U.S.A. Vol 1 1 Textless.jpg"
        ]
    },
    {
        "slot": 48,
        "folder": "48_xmen_schism_cyclops_wolverine",
        "wiki": "marvel.fandom.com",
        "category": "X-Men: Schism Vol 1 5/Images",
        "search": "X-Men Schism Vol 1 5 Cyclops Wolverine",
        "specific_files": [
            "File:X-Men Schism Vol 1 5 Textless.jpg",
            "File:Hellfire Club (Earth-616) from X-Men Schism Vol 1 5 001.jpg",
            "File:X-Men Schism Vol 1 5 Cho Variant Textless.jpg",
            "File:X-Men Schism Vol 1 5.jpg"
        ]
    },
    {
        "slot": 49,
        "folder": "49_green_arrow_cry_for_justice_prometheus",
        "wiki": "dc.fandom.com",
        "category": "Justice League: Cry for Justice Vol 1 7/Images",
        "search": "Green Arrow kills Prometheus Cry for Justice 7",
        "specific_files": [
            "File:Green Arrow kills Prometheus.jpg",
            "File:Death of Lian Harper 01.jpg",
            "File:Justice League Cry for Justice Vol 1 7 Textless.jpg",
            "File:Electrocutioner III 003.jpg"
        ]
    },
    {
        "slot": 50,
        "folder": "50_planet_hulk_muerte_caiera",
        "wiki": "marvel.fandom.com",
        "category": "Incredible Hulk Vol 2 105/Images",
        "search": "Caiera death Incredible Hulk 105",
        "specific_files": [
            "File:Bruce Banner (Earth-616) from Incredible Hulk Vol 2 105 0001.jpeg",
            "File:Incredible Hulk Vol 2 105 Textless.jpg",
            "File:Incredible Hulk Vol 2 105.jpg",
            "File:Caiera (Earth-616) from Incredible Hulk Vol 2 104 0001.jpg"
        ]
    }
]

def get_image_url(wiki, file_title):
    url = f"https://{wiki}/api.php"
    clean = file_title if file_title.startswith("File:") else f"File:{file_title}"
    params = {
        "action": "query",
        "titles": clean,
        "prop": "imageinfo",
        "iiprop": "url",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10).json()
        pages = r.get("query", {}).get("pages", {})
        for pid, pdata in pages.items():
            info = pdata.get("imageinfo", [])
            if info:
                return info[0]["url"]
    except Exception as e:
        print(f"Error fetching url for {file_title}: {e}")
    return None

def download_image(url, wiki=None):
    headers = HEADERS.copy()
    if wiki:
        headers["Referer"] = f"https://{wiki}/"
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return Image.open(BytesIO(r.content)).convert("RGB")
        else:
            print(f"HTTP {r.status_code} on {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def process_slot(slot_data):
    slot_num = slot_data["slot"]
    folder_name = slot_data["folder"]
    wiki = slot_data["wiki"]
    dest_dir = CURATED_BASE / folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n=======================================================")
    print(f"📦 PROCESANDO PANELES SLOT {slot_num}: {folder_name}")
    print(f"=======================================================")
    
    # Si ya existen scene_01 a scene_04 con tamaño adecuado, verificar
    existing = [dest_dir / f"scene_0{i}.jpg" for i in range(1, 5)]
    if all(p.exists() and p.stat().st_size > 10000 for p in existing):
        print(f"✅ Todos los 4 paneles ya existen y están listos en {dest_dir}")
        return True

    # 1. Recolectar lista de archivos
    file_candidates = list(slot_data.get("specific_files", []))
    
    # 2. Agregar archivos de categoría
    cat = slot_data.get("category")
    if cat:
        url = f"https://{wiki}/api.php"
        params = {"action": "query", "list": "categorymembers", "cmtitle": f"Category:{cat}", "cmnamespace": 6, "cmlimit": 15, "format": "json"}
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=8).json()
            for m in r.get("query", {}).get("categorymembers", []):
                t = m.get("title")
                if t and t not in file_candidates:
                    file_candidates.append(t)
        except Exception:
            pass

    # 3. Agregar archivos de búsqueda si faltan
    if len(file_candidates) < 4:
        srch = slot_data.get("search")
        if srch:
            url = f"https://{wiki}/api.php"
            params = {"action": "query", "list": "search", "srsearch": srch, "srnamespace": 6, "srlimit": 10, "format": "json"}
            try:
                r = requests.get(url, params=params, headers=HEADERS, timeout=8).json()
                for m in r.get("query", {}).get("search", []):
                    t = m.get("title")
                    if t and t not in file_candidates:
                        file_candidates.append(t)
            except Exception:
                pass

    print(f"Encontrados {len(file_candidates)} candidatos de archivos en {wiki}")
    
    # 4. Descargar imágenes válidas
    downloaded_images = []
    for ftitle in file_candidates:
        if len(downloaded_images) >= 4:
            break
        iurl = get_image_url(wiki, ftitle)
        if iurl:
            print(f"  Descargando: {ftitle}...")
            img = download_image(iurl, wiki=wiki)
            if img and img.width > 200 and img.height > 200:
                downloaded_images.append(img)
                time.sleep(0.3)

    if len(downloaded_images) == 0:
        print(f"❌ ERROR: No se pudieron descargar imágenes para {folder_name}")
        return False

    if len(downloaded_images) < 4:
        print(f"⚠️ Solo se obtuvieron {len(downloaded_images)} imágenes, duplicando última si es necesario...")
        while len(downloaded_images) < 4:
            downloaded_images.append(downloaded_images[-1].copy())

    # 5. Formatear a 1080x1920 vertical usando create_full_panel_frame
    for i in range(4):
        target_p = dest_dir / f"scene_0{i+1}.jpg"
        formatted_img = create_full_panel_frame(downloaded_images[i], target_w=1080, target_h=1920)
        formatted_img.save(target_p, quality=95)
        print(f"  ✅ Guardado {target_p.name} (1080x1920)")

    return True

if __name__ == "__main__":
    success_count = 0
    for s in SLOTS:
        if process_slot(s):
            success_count += 1
    print(f"\n🎉 ¡Proceso finalizado! {success_count}/{len(SLOTS)} slots tienen paneles 1080x1920 listos.")
