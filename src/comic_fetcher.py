import io
import json
import os
import re
import urllib.parse
from pathlib import Path
from PIL import Image, ImageStat
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json,text/html,*/*;q=0.8',
}

# Lista de palabras clave para distinguir universos y evitar contaminación cruzada
DC_CHARACTERS = {
    'batman', 'bruce wayne', 'joker', 'superman', 'clark kent', 'wonder woman', 'flash', 'barry allen',
    'reverse flash', 'eobard thawne', 'darkseid', 'doomsday', 'batman who laughs', 'superboy prime',
    'spectre', 'lucifer morningstar', 'doctor manhattan', 'watchmen', 'deathstroke', 'blackest night',
    'green lantern', 'hal jordan', 'red hood', 'jason todd', 'aquaman', 'dark multiverse', 'shazam',
    'black adam', 'teth-adam', 'bialya', 'constantine', 'john constantine', 'swamp thing', 'bane',
    'robin', 'nightwing', 'dick grayson', 'cyborg', 'martian manhunter', 'lex luthor', 'brainiac',
    'zatanna', 'harley quinn', 'sinestro', 'riddler', 'penguin', 'two-face', 'scarecrow', 'catwoman',
    'grim knight', 'the grim knight', 'justice league', 'justice society', 'teen titans', 'arkham', 'gotham'
}

DISALLOWED_KEYWORDS = [
    'mug', 'actor', 'film', 'movie', 'live-action', 'live action', 'cast', 'cosplay',
    'photo', 'shot', 'portrait', 'interview', 'trailer', 'commercial', 'fox', 'warner',
    'tv', 'series', 'clip', 'joaquin', 'variant', 'poster', 'logo', 'cover', 'tpb',
    'omnibus', 'action figure', 'toy', 'statue', 'cosplayer', 'trading cards', 'video game',
    'soundtrack', 'review', 'bts', 'behind the scenes'
]


def _detect_primary_wiki(character_name: str) -> list[str]:
    """Determina si el personaje pertenece a DC o Marvel para buscar en la wiki correcta."""
    norm = character_name.lower().strip()
    is_dc = any(dc_name in norm for dc_name in DC_CHARACTERS)
    if is_dc:
        return ['dc']
    return ['marvel']


def get_fandom_comic_art(character_name: str, count: int = 10) -> list[str]:
    """Obtiene arte e ilustraciones oficiales de cómics reales desde Marvel y DC Fandom con validación estricta."""
    from .comic_precision_scraper import is_cover_or_promo_image, check_is_comic_art_inking

    wikis = _detect_primary_wiki(character_name)
    found_urls = []
    char_terms = set(re.findall(r'\w+', character_name.lower()))

    for wiki in wikis:
        search_api = f"https://{wiki}.fandom.com/api.php?action=query&list=search&srsearch={urllib.parse.quote(character_name)}&srlimit=10&format=json"
        try:
            res = requests.get(search_api, headers=HEADERS, timeout=8)
            if res.status_code != 200:
                continue

            search_data = res.json()
            raw_results = search_data.get('query', {}).get('search', [])

            valid_titles = []
            for item in raw_results:
                title = item.get('title', '')
                title_lower = title.lower()
                # Descartar páginas de películas, actores o series
                if any(bad in title_lower for bad in DISALLOWED_KEYWORDS):
                    continue
                title_words = set(re.findall(r'\w+', title_lower))

                if char_terms.intersection(title_words) or any(k in title_lower for k in ['earth', 'prime', 'vol', 'metal', 'wars', 'secret']):
                    valid_titles.append(title)

            valid_titles = sorted(valid_titles, key=lambda t: 0 if any(k in t for k in ['Earth', 'Prime', '616', 'Gallery']) else 1)

            for title in valid_titles[:5]:
                for page_name in [f"{title}/Gallery", title]:
                    img_api = f"https://{wiki}.fandom.com/api.php?action=query&titles={urllib.parse.quote(page_name)}&generator=images&gimlimit=40&prop=imageinfo&iiprop=url|size&format=json"
                    r_img = requests.get(img_api, headers=HEADERS, timeout=8)
                    if r_img.status_code == 200:
                        pages = r_img.json().get('query', {}).get('pages', {})
                        for p in pages.values():
                            img_title = p.get('title', '').lower()

                            # Descartar imágenes de películas, actores, fotos, portadas
                            if any(bad in img_title for bad in DISALLOWED_KEYWORDS) or is_cover_or_promo_image(img_title):
                                continue

                            # Descartar imágenes de personajes ajenos
                            if wiki == 'dc' and any(m in img_title for m in ['deadpool', 'spiderman', 'spider-man', 'avengers', 'marvel', 'x-men']):
                                continue
                            if wiki == 'marvel' and any(d in img_title for d in ['batman', 'superman', 'joker', 'justice league', 'dc_']):
                                continue

                            for info in p.get('imageinfo', []):
                                u = info.get('url', '')
                                w = info.get('width', 0)
                                h = info.get('height', 0)
                                if any(bad in u.lower() for bad in DISALLOWED_KEYWORDS) or is_cover_or_promo_image(u):
                                    continue
                                # Solo arte de cómics en alta resolución
                                if w >= 450 and h >= 450:
                                    clean_u = u.split('/revision/')[0]
                                    if clean_u not in found_urls and any(clean_u.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                                        found_urls.append(clean_u)
                                        if len(found_urls) >= count:
                                            return found_urls
        except Exception as e:
            print(f"[COMIC FETCHER] Error consultando Fandom {wiki}: {e}")
            continue

    return found_urls


def download_comic_art_image(url: str, output_path: str) -> bool:
    """Descarga y guarda una imagen oficial de cómic en formato JPEG de alta calidad."""
    from .comic_precision_scraper import check_is_comic_art_inking, is_cover_or_promo_image
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    if is_cover_or_promo_image(url):
        return False
    try:
        r = requests.get(url, headers=HEADERS, timeout=12)
        if r.status_code == 200 and len(r.content) > 20000:
            img = Image.open(io.BytesIO(r.content))
            img = img.convert('RGB')
            # Quality Shield: Reject text documents / handwritten notes
            stat = ImageStat.Stat(img.convert('HSV'))
            mean_sat, mean_val = stat.mean[1], stat.mean[2]
            if mean_sat < 15.0 and mean_val > 175.0:
                print(f"  [QUALITY SHIELD] Rechazada imagen con texto/nota manuscrita: {Path(output_path).name} (sat={mean_sat:.1f})")
                return False
            # Quality Shield: Reject live-action photos, actors, or objects
            if not check_is_comic_art_inking(img):
                print(f"  [QUALITY SHIELD] Rechazada imagen por entintado (posible foto real/actor): {Path(output_path).name}")
                return False
            img.save(output_path, "JPEG", quality=95)
            print(f"  [OK] Guardado arte oficial de cómic: {Path(output_path).name} ({img.width}x{img.height})")
            return True
    except Exception as err:
        print(f"  [ERR] No se pudo descargar {url}: {err}")
    return False


def fetch_images_for_script(script_data: dict, generation_dir: str) -> dict:
    """Descarga imágenes reales de cómics para cada escena del script."""
    gen_path = Path(generation_dir)
    gen_path.mkdir(parents=True, exist_ok=True)

    meta = script_data.get('metadata', {})
    character_topic = meta.get('tema', '') or meta.get('title', 'Franklin Richards')
    # Limpiar palabras genéricas para buscar el personaje exacto
    clean_character = re.sub(r'(el ser más poderoso|historia|cómic|lore|poderes|marvel|dc|origen|oscuro|pesadilla|del|multiverso)', '', character_topic, flags=re.IGNORECASE).strip()
    if not clean_character or len(clean_character) < 3:
        clean_character = character_topic

    print(f"[COMIC FETCHER] Buscando arte oficial de cómic para: '{clean_character}'...")
    scenes = script_data.get('scenes', [])
    needed_count = len(scenes)

    comic_urls = get_fandom_comic_art(clean_character, count=max(needed_count + 4, 8))

    results = {}

    for idx, s in enumerate(scenes):
        sn = s.get('scene_number', idx + 1)
        scene_dir = gen_path / f"Escena_{sn:02d}"
        scene_dir.mkdir(parents=True, exist_ok=True)

        img_dest = str(scene_dir / "imagen_1.jpg")

        # Seleccionar la URL correspondiente a la escena
        selected_url = comic_urls[idx % len(comic_urls)] if comic_urls else None

        success = False
        if selected_url:
            success = download_comic_art_image(selected_url, img_dest)

        results[sn] = {
            'success': success,
            'path': img_dest if success else None,
        }

    # Guardar script.json en la carpeta de la generación
    with open(gen_path / "script.json", "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    return results
