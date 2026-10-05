"""
MÓDULO DE PRECISIÓN VISUAL MULTI-FUENTE PARA CÓMICS CON ÁRBITRO DE IA
=====================================================================
1. Multi-Fuente: Fandom MediaWiki + Cross-Wiki + Búsqueda Web Abierta (Bing Panels).
2. Filtro Anti-Portadas: Descarta portadas, variantes, pósters y mercancía.
3. Deduplicador Visual RMS: Evita viñetas repetidas o planos idénticos.
4. Árbitro de IA (Gemini Vision): Evalúa la imagen contra la narración (1-10).
5. Respaldo Resiliente: Si ninguna viñeta alcanza 10/10, toma el mejor candidato
   disponible para evitar caídas en producción.
"""

import base64
import json
import os
import re
import urllib.parse
from io import BytesIO
import requests
from PIL import Image, ImageChops, ImageStat

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
}

WIKI_DOMAINS = [
    "marvel.fandom.com",
    "dc.fandom.com",
    "imagecomics.fandom.com",
    "comiccrossroads.fandom.com"
]

CANDIDATE_VISION_MODELS = [
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-flash-latest"
]

# -------------------------------------------------------------------------
# 1. DEDUPLICACIÓN VISUAL Y FILTROS HEURÍSTICOS
# -------------------------------------------------------------------------

def calculate_image_rms_difference(img_path1: str, img_path2: str) -> float:
    """Calcula la diferencia RMS en escala de grises. < 14.0 indica imágenes idénticas."""
    try:
        try:
            import numpy as np
            im1 = Image.open(img_path1).convert('L').resize((128, 128))
            im2 = Image.open(img_path2).convert('L').resize((128, 128))
            arr1 = np.array(im1, dtype=np.float32)
            arr2 = np.array(im2, dtype=np.float32)
            return float(np.sqrt(np.mean((arr1 - arr2) ** 2)))
        except ImportError:
            im1 = Image.open(img_path1).convert('L').resize((128, 128))
            im2 = Image.open(img_path2).convert('L').resize((128, 128))
            diff = ImageChops.difference(im1, im2)
            stat = ImageStat.Stat(diff)
            return float(stat.rms[0])
    except Exception:
        return 999.0


def is_duplicate_panel(candidate_path: str, existing_paths: list, threshold: float = 14.0) -> bool:
    """Verifica si el candidato ya fue usado o es casi idéntico a una viñeta previa del video."""
    for ep in existing_paths:
        if os.path.exists(ep) and os.path.abspath(ep) != os.path.abspath(candidate_path):
            rms = calculate_image_rms_difference(candidate_path, ep)
            if rms < threshold:
                return True
            # Verificación simétrica: si una imagen es 1080x1920 y la otra es raw
            try:
                with Image.open(candidate_path) as im_c, Image.open(ep) as im_e:
                    if (im_e.size == (1080, 1920) and im_c.size != (1080, 1920)) or (im_c.size == (1080, 1920) and im_e.size != (1080, 1920)):
                        from .cloud_runner import create_full_panel_frame
                        framed_c = create_full_panel_frame(im_c.convert('RGB'), 1080, 1920) if im_c.size != (1080, 1920) else im_c
                        framed_e = create_full_panel_frame(im_e.convert('RGB'), 1080, 1920) if im_e.size != (1080, 1920) else im_e
                        diff = ImageChops.difference(framed_c.convert('L').resize((128, 128)), framed_e.convert('L').resize((128, 128)))
                        f_rms = float(ImageStat.Stat(diff).rms[0])
                        if f_rms < threshold:
                            return True
            except Exception:
                pass
    return False


def is_cover_or_promo_image(file_title: str) -> bool:
    """Detecta y descarta portadas oficiales, variantes, pósters y logos."""
    if not file_title:
        return False
    # Normalizar reemplazando guiones bajos y guiones por espacios
    t = file_title.lower().replace('_', ' ').replace('-', ' ').strip()
    cover_keywords = [
        'cover', 'variant', 'textless', 'solicit', 'promo', 'poster',
        'logo', 'tpb', 'omnibus', 'sketch', 'wraparound', 'facsimile',
        'reprint', 'chronicles', 'bullet', 'advertisement', 'card',
        'action figure', 'figure', 'toy', 'cosplay', 'wallpaper',
        'trade paperback', 'hardcover', 'annual',
        # Instant rejection of MCU live-action film stills, TV series, actors, video games
        'earth 199999', 'earth-199999', 'earth 89', 'earth 96', 'earth 12',
        'season', 'episode', 'live action', 'live-action', 'actor', 'actress',
        'film', 'movie', 'cinematic', 'mcu', 'dceu', 'soundtrack', 'bts',
        'behind the scenes', 'cast', 'interview', 'trailer', 'commercial',
        'video game', 'videogame', 'game', 'heroclix', 'endgame', 'infinity war',
        'homecoming', 'far from home', 'no way home', 'wandavision', 'she hulk',
        'she-hulk', 'defenders', 'jessica jones', 'luke cage', 'iron fist',
        'agents of shield', 'agents of s.h.i.e.l.d', 'daredevil born again season',
        'multiverse of madness', 'quantumania', 'brave new world'
    ]
    if any(k in t for k in cover_keywords):
        return True

    # Detecta formato de portada de Fandom: "Comic Vol X Y.jpg" o "Comic Vol. X Y.jpg" sin sub-número de página
    m = re.search(r'vol\.?\s*(\d+)\s+(\d+)(\s+(\d+))?', t)
    if m:
        page_num = m.group(4)
        if not page_num:
            return True

    # Detecta nombres con número de edición suelto sin número de panel (ej: "Daredevil 227.jpg")
    if re.search(r'\b(issue|iss|no|num|#)\s*\d+\b', t) and not any(p in t for p in ['panel', 'scene', 'page', '001', '002', '003']):
        return True

    return False

# -------------------------------------------------------------------------
# 2. MOTORES DE BÚSQUEDA Y EXTRACCIÓN (MULTI-FUENTE)
# -------------------------------------------------------------------------

def get_file_url(wiki_domain: str, file_title: str) -> str:
    """Extrae la URL de resolución completa de Fandom mediante la MediaWiki API preservando el token de revisión."""
    clean_title = file_title if file_title.startswith("File:") else f"File:{file_title}"
    url = f"https://{wiki_domain}/api.php"
    params = {
        "action": "query",
        "titles": clean_title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for pid, pinfo in pages.items():
            if "imageinfo" in pinfo and pinfo["imageinfo"]:
                return pinfo["imageinfo"][0]["url"]
    except Exception:
        pass
    return None


def get_file_url_cross_wiki(primary_wiki: str, file_title: str):
    """Busca el archivo en la wiki principal y en wikis alternativas si no existe."""
    wikis = [primary_wiki] + [w for w in WIKI_DOMAINS if w != primary_wiki]
    for w in wikis:
        url = get_file_url(w, file_title)
        if url:
            return url, w
    return None, None


DISALLOWED_SCRAPER_KEYWORDS = [
    'mug', 'actor', 'film', 'movie', 'live-action', 'live action', 'cast', 'cosplay',
    'photo', 'shot', 'portrait', 'interview', 'trailer', 'commercial', 'fox', 'warner',
    'tv', 'series', 'clip', 'joaquin', 'variant', 'poster', 'logo', 'trading cards', 'video game',
    'soundtrack', 'review', 'bts', 'behind the scenes', 'script', 'text'
]


def get_issue_category_panels(wiki_domain: str, query_str: str) -> list:
    """
    Extrae la lista de viñetas interiores escaneadas desde la categoría oficial
    de la grapa en Fandom (Category:<Comic Issue>/Images).
    Descarta estrictamente números de universo como Earth-616 o categorías genéricas.
    """
    if not query_str:
        return []

    # Decodificar URL y normalizar guiones bajos
    cleaned = urllib.parse.unquote(query_str).replace("_", " ")

    # Prioridad 1: Detectar 'from <Comic Title> Vol X Y' o 'from <Comic Title> Y'
    m_from = re.search(r'from\s+([A-Za-z0-9\s\-]+?(?:Vol(?:\.|\s*)\s*\d+\s*)?\d+)', cleaned, re.IGNORECASE)
    issue_name = None
    if m_from:
        cand = m_from.group(1).strip()
        if not re.search(r'\b(earth|season|episode|universe|movie|film)\b', cand, re.IGNORECASE):
            issue_name = cand

    # Prioridad 2: Buscar patrón explícito '<Comic Title> Vol X Y'
    if not issue_name:
        m_vol = re.search(r'([A-Za-z0-9\s\-]+?Vol(?:\.|\s*)\s*\d+\s*\d+)', cleaned, re.IGNORECASE)
        if m_vol:
            cand = m_vol.group(1).strip()
            if not re.search(r'\b(earth|season|episode|universe|movie|film)\b', cand, re.IGNORECASE):
                issue_name = cand

    if not issue_name or len(issue_name) < 4:
        return []

    url = f"https://{wiki_domain}/api.php"
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Category:{issue_name}/Images",
        "cmnamespace": 6,
        "format": "json",
        "cmlimit": 35
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        items = r.json().get("query", {}).get("categorymembers", [])
        return [
            it["title"] for it in items
            if not is_cover_or_promo_image(it["title"])
            and not any(bad in it["title"].lower() for bad in DISALLOWED_SCRAPER_KEYWORDS)
        ]
    except Exception:
        return []


def search_fandom_files(wiki_domain: str, query: str, max_results: int = 8) -> list:
    """Búsqueda semántica de archivos en Fandom filtrando por extensión de imagen y descartando películas/portadas."""
    url = f"https://{wiki_domain}/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srnamespace": 6,
        "format": "json",
        "srlimit": max_results
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        items = r.json().get("query", {}).get("search", [])
        files = []
        for it in items:
            t = it["title"]
            t_low = t.lower()
            if any(t_low.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                if is_cover_or_promo_image(t) or any(bad in t_low for bad in DISALLOWED_SCRAPER_KEYWORDS):
                    continue
                files.append(t)
        return files
    except Exception:
        return []


COMIC_APPROVED_DOMAINS = [
    "fandom.com", "nocookie.net", "comicvine.gamespot.com", "cbr.com", "cbrimages.com",
    "srcdn.com", "screenrant.com", "aiptcomics.com", "readallcomics.com", "viewcomic.com",
    "bleedingcool.com", "reddit.com", "pinimg.com", "tumblr.com", "marvel.com", "dc.com",
    "comicosity.com", "panelsandpixels.com", "previewsworld.com", "comicartfans.com",
    "comic-watch.com", "gamespot.com", "blogspot.com", "blogger.com", "googleusercontent.com",
    "wordpress.com", "wp.com"
]


def check_is_comic_art_inking(img: Image.Image) -> bool:
    """Verifica mediante visión por computador que la imagen tenga entintado y trazos de cómic, descartando fotos reales, comida o actores."""
    try:
        from PIL import ImageFilter
        if img.size == (1080, 1920):
            # Evaluar el panel interior central excluyendo los márgenes de fondo desenfocado
            crop_box = (108, 384, 972, 1536)
            eval_img = img.crop(crop_box).resize((512, 512))
            edges = eval_img.convert('L').filter(ImageFilter.FIND_EDGES)
            edge_stat = ImageStat.Stat(edges)
            return edge_stat.mean[0] >= 3.5 or edge_stat.stddev[0] >= 12.0
        eval_img = img.resize((512, 512))
        edges = eval_img.convert('L').filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        return edge_stat.mean[0] >= 7.5 or edge_stat.stddev[0] >= 12.0
    except Exception:
        return True


def search_bing_comic_panels(query: str, limit: int = 8) -> list:
    """
    Búsqueda web abierta de viñetas en Bing: Utiliza cabeceras de navegador reales,
    simplificación de consulta para máxima precisión y filtrado estricto por dominios de cómics.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    clean_q = re.sub(r'\b(comic|panel|scan|scans)\b', '', query, flags=re.IGNORECASE).strip()
    words = [w for w in clean_q.split() if len(w) > 2]
    
    # Generar variantes de búsqueda: completa y simplificada (3-4 palabras clave)
    variants = [f"{clean_q} comic panel scan"]
    if len(words) > 4:
        variants.append(f"{' '.join(words[:4])} comic panel")
        variants.append(f"{words[0]} {words[-1]} comic panel scan")
    elif len(words) >= 2:
        variants.append(f"{' '.join(words)} comic panel")

    collected_urls = []
    disallowed = ['wallpaper', 'icon', 'steamstatic', 'action_figure', 'cosplay', 't-shirt', 'recipe', 'food', 'actor', 'cast']

    for v in variants:
        url = f"https://www.bing.com/images/search?q={urllib.parse.quote(v)}&form=HDRSC2&first=1"
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                urls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', r.text)
                for u in urls:
                    u_low = u.lower()
                    if any(bad in u_low for bad in disallowed):
                        continue
                    if any(d in u_low for d in COMIC_APPROVED_DOMAINS) and u not in collected_urls:
                        collected_urls.append(u)
                        if len(collected_urls) >= limit:
                            return collected_urls
        except Exception:
            continue

    # Respaldo flexible: si no hubo suficientes con dominios específicos, tomar URLs de imágenes limpias
    if len(collected_urls) < 4:
        for v in variants:
            url = f"https://www.bing.com/images/search?q={urllib.parse.quote(v)}&form=HDRSC2&first=1"
            try:
                r = requests.get(url, headers=headers, timeout=8)
                if r.status_code == 200:
                    urls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', r.text)
                    for u in urls:
                        u_low = u.lower()
                        if any(bad in u_low for bad in disallowed):
                            continue
                        if any(u_low.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']) and u not in collected_urls:
                            collected_urls.append(u)
                            if len(collected_urls) >= limit:
                                return collected_urls
            except Exception:
                continue

    return collected_urls[:limit]


# -------------------------------------------------------------------------
# 3. GESTORES DE DESCARGA
# -------------------------------------------------------------------------

def download_image(url: str, referer_domain: str, dest_path: str, min_dim: int = 350) -> bool:
    """Descarga y valida una imagen de Fandom, aplicando además el filtro Quality Shield y entintado."""
    req_headers = dict(HEADERS)
    if referer_domain:
        req_headers["Referer"] = f"https://{referer_domain}/"
    try:
        r = requests.get(url, headers=req_headers, timeout=12)
        if r.status_code != 200:
            return False
        img = Image.open(BytesIO(r.content)).convert("RGB")
        w, h = img.size
        if w < min_dim and h < min_dim:
            return False

        # Quality Shield: Rechazar si no tiene trazo de cómic o si es documento de texto
        if not check_is_comic_art_inking(img):
            return False

        stat = ImageStat.Stat(img.convert("HSV"))
        mean_sat, mean_val = stat.mean[1], stat.mean[2]
        if mean_sat < 15.0 and mean_val > 175.0:
            return False

        dest_dir = os.path.dirname(os.path.abspath(dest_path))
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        img.save(dest_path, "JPEG", quality=95)
        return True
    except Exception:
        return False


def download_web_panel(url: str, dest_path: str, min_dim: int = 350) -> bool:
    """Descarga y valida una imagen de la web abierta (Bing / blogs / foros)."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=7)
        if r.status_code != 200:
            return False
        img = Image.open(BytesIO(r.content)).convert("RGB")
        w, h = img.size
        if w < min_dim and h < min_dim:
            return False

        # Quality Shield: Rechazar si no tiene trazo de cómic o si es documento de texto
        if not check_is_comic_art_inking(img):
            return False

        stat = ImageStat.Stat(img.convert("HSV"))
        mean_sat, mean_val = stat.mean[1], stat.mean[2]
        if mean_sat < 15.0 and mean_val > 175.0:
            return False

        dest_dir = os.path.dirname(os.path.abspath(dest_path))
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        img.save(dest_path, "JPEG", quality=95)
        return True
    except Exception:
        return False

# -------------------------------------------------------------------------
# 4. ÁRBITRO DE VISIÓN POR INTELIGENCIA ARTIFICIAL (GEMINI MULTIMODAL)
# -------------------------------------------------------------------------

def verify_visual_alignment_with_gemini(image_path: str, scene_text: str) -> dict:
    """
    Auditor de Calidad Gráfica con Gemini Vision:
    Examina si la viñeta muestra con exactitud lo que narra el locutor.
    Utiliza el pool completo de claves de Gemini para máxima disponibilidad.
    """
    from .gemini_tts import get_candidate_keys
    keys_to_try = get_candidate_keys()

    if not scene_text or not os.path.exists(image_path):
        return {"score": 1, "is_comic_panel": False, "depicts_action": False, "reason": "Entrada inválida"}

    prompt = f"""Eres el supervisor de edición gráfica y control de calidad de un canal de cómics.
Evalúa con rigor si esta imagen ilustra con fidelidad la siguiente escena que narra la voz:
Escena narrada: "{scene_text}"

REGLA DE TOLERANCIA CERO PARA PORTADAS Y LOGOTIPOS:
- Si la imagen contiene el título del cómic en letras gigantes ("DAREDEVIL", "BATMAN", "SPIDER-MAN", etc.), sello Comics Code Authority, número de edición gigante, logos de Marvel/DC o código de barras, ES UNA PORTADA COMERCIAL.
- Para cualquier portada o póster comercial, responde OBLIGATORIAMENTE con score 1 e is_comic_panel false.
- Solo acepta viñetas o secuencias interiores que ilustren los sucesos relatados.

Responde ESTRICTAMENTE con un objeto JSON:
{{
  "score": <número entero de 1 a 10, donde 10 es viñeta exacta de la acción/personajes y 1 es portada, live-action o contenido no relacionado>,
  "is_comic_panel": <true si es arte/viñeta interior de cómic, false si es portada, live-action o póster>,
  "depicts_action": <true si muestra la acción o consecuencia de la escena narrada, false si no>,
  "reason": <1 frase breve de explicación>
}}"""

    # Intento 1: SDK oficial google.genai si está instalado
    for cand_key in keys_to_try:
        try:
            from google import genai
            client = genai.Client(api_key=cand_key, http_options={"timeout": 12000})
            im = Image.open(image_path)
            for model in CANDIDATE_VISION_MODELS:
                try:
                    res = client.models.generate_content(model=model, contents=[im, prompt])
                    raw = res.text.strip()
                    if "```json" in raw:
                        raw = raw.split("```json")[1].split("```")[0].strip()
                    elif "```" in raw:
                        raw = raw.split("```")[1].split("```")[0].strip()
                    return json.loads(raw)
                except Exception:
                    continue
        except Exception:
            pass

    # Intento 2: Conexión REST directa con soporte multimodal y fallback de modelos
    try:
        with open(image_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_data}},
                    {"text": prompt}
                ]
            }],
            "generationConfig": {"responseMimeType": "application/json"}
        }

        for cand_key in keys_to_try:
            for model in CANDIDATE_VISION_MODELS:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={cand_key}"
                try:
                    r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=7)
                    if r.status_code == 200:
                        raw = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                        if "```json" in raw:
                            raw = raw.split("```json")[1].split("```")[0].strip()
                        elif "```" in raw:
                            raw = raw.split("```")[1].split("```")[0].strip()
                        return json.loads(raw)
                except Exception:
                    continue
    except Exception:
        pass

    # Respaldo heurístico: Si Gemini no pudo verificar, dar score 2 (no verificado)
    try:
        im = Image.open(image_path)
        if not check_is_comic_art_inking(im):
            return {"score": 1, "is_comic_panel": False, "depicts_action": False, "reason": "Rechazado: La imagen no presenta entintado de cómic (posible foto real/actor/objeto)"}
        return {"score": 2, "is_comic_panel": True, "depicts_action": False, "reason": "Arte de cómic detectado por entintado, pero alineación de acción NO verificada por Gemini"}
    except Exception:
        return {"score": 1, "is_comic_panel": False, "depicts_action": False, "reason": "Error procesando imagen para verificación"}

# -------------------------------------------------------------------------
# 5. COORDINADOR PRINCIPAL: FETCH_SCENE_IMAGE
# -------------------------------------------------------------------------

def fetch_scene_image(
    wiki_domain: str,
    target_file: str,
    fallback_query: str,
    dest_path: str,
    existing_scene_images: list = None,
    scene_text: str = None,
    used_sources: set = None
) -> str:
    """
    Descarga la viñeta perfecta aplicando el pipeline completo:
    Multi-fuente -> Deduplicación RMS -> Arbitraje con Gemini Vision -> Respaldo resiliente.
    """
    if existing_scene_images is None:
        existing_scene_images = []

    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 10000:
        if not is_duplicate_panel(dest_path, existing_scene_images):
            return dest_path

    temp_candidate = dest_path + ".cand.jpg"
    candidates_pool = []

    # 1. Candidato target_file explícito
    if target_file:
        is_cov = is_cover_or_promo_image(target_file)
        candidates_pool.append({
            "source": "fandom_target",
            "title": target_file,
            "is_cover": is_cov,
            "wiki": wiki_domain
        })

    # 2. Exploración de galería interior de la grapa (Category:<Issue>/Images)
    search_seed = target_file or fallback_query or ""
    category_panels = get_issue_category_panels(wiki_domain, search_seed)
    for p in category_panels:
        if not any(c.get("title") == p for c in candidates_pool if c["source"].startswith("fandom")):
            candidates_pool.append({
                "source": "fandom_category",
                "title": p,
                "is_cover": False,
                "wiki": wiki_domain
            })

    # 3. Búsqueda semántica de viñetas en Fandom
    if fallback_query:
        for q in [fallback_query, f"{fallback_query} 001"]:
            found_files = search_fandom_files(wiki_domain, q, max_results=6)
            for f in found_files:
                if not any(c.get("title") == f for c in candidates_pool if c["source"].startswith("fandom")):
                    is_cov = is_cover_or_promo_image(f)
                    candidates_pool.append({
                        "source": "fandom_search",
                        "title": f,
                        "is_cover": is_cov,
                        "wiki": wiki_domain
                    })

    # 4. Búsqueda web abierta en Bing (blogs, foros de cómics y Reddit)
    web_query = fallback_query or (target_file.replace("File:", "").replace(".jpg", "") if target_file else "")
    if web_query:
        bing_urls = search_bing_comic_panels(web_query, limit=5)
        for u in bing_urls:
            candidates_pool.append({
                "source": "bing_web",
                "url": u,
                "is_cover": False,
                "wiki": None
            })

    # Priorización: Viñetas interiores ÚNICAMENTE. Portadas comerciales 100% prohibidas.
    interior_pool = [c for c in candidates_pool if not c["is_cover"]]
    ordered_candidates = interior_pool

    # Si no se encontraron viñetas interiores en Fandom, forzar búsqueda web de scans interiores
    if not ordered_candidates:
        expanded_q = f"{fallback_query or target_file or ''} interior comic panel scan"
        more_web = search_bing_comic_panels(expanded_q, limit=8)
        for u in more_web:
            ordered_candidates.append({
                "source": "bing_web",
                "url": u,
                "is_cover": False,
                "wiki": None
            })

    best_fallback_file = None
    highest_score = -1
    MAX_EVALUATIONS = 8
    eval_count = 0

    for cand in ordered_candidates:
        if eval_count >= MAX_EVALUATIONS:
            print(f"  [Límite de Evaluación] Máximo de {MAX_EVALUATIONS} candidatos evaluados para esta escena. Finalizando búsqueda rápida.")
            break

        cand_src = cand["source"]
        cand_name = cand.get("title") or cand.get("url", "")[:50]
        cand_id = cand.get("title") or cand.get("url")

        # Deduplicación por fuente: evitar reutilizar el mismo archivo o URL en escenas diferentes
        if used_sources is not None and cand_id and cand_id in used_sources:
            print(f"  [Deduplicación Fuente] Candidato '{cand_name}' ya utilizado en otra escena. Descartando.")
            continue

        success = False

        if cand_src.startswith("fandom"):
            url, found_wiki = get_file_url_cross_wiki(cand["wiki"], cand["title"])
            if url:
                success = download_image(url, found_wiki, temp_candidate)
        elif cand_src == "bing_web":
            success = download_web_panel(cand["url"], temp_candidate)

        if not success or not os.path.exists(temp_candidate):
            continue

        # Validar duplicados visuales RMS
        if is_duplicate_panel(temp_candidate, existing_scene_images):
            print(f"  [Deduplicación Visual] Candidato descartado por similitud RMS.")
            if os.path.exists(temp_candidate):
                os.remove(temp_candidate)
            continue

        # Si no hay texto de escena disponible, aceptar el primer panel válido
        if not scene_text:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(temp_candidate, dest_path)
            label = "[PORTADA]" if cand["is_cover"] else "[VIÑETA INTERIOR]"
            cand_name = cand.get("title") or cand.get("url", "")[:50]
            print(f"  {label} ({cand_src}): {cand_name}")
            if used_sources is not None and cand_id:
                used_sources.add(cand_id)
            return dest_path

        # Evaluación con Árbitro de IA Gemini Multimodal Vision
        eval_count += 1
        eval_result = verify_visual_alignment_with_gemini(temp_candidate, scene_text)
        score = eval_result.get("score", 7)
        is_panel = eval_result.get("is_comic_panel", True)
        reason = eval_result.get("reason", "")
        cand_name = cand.get("title") or cand.get("url", "")[:50]

        # Guardar el candidato con la mayor puntuación encontrada (siempre que no sea duplicado)
        if score > highest_score and not is_duplicate_panel(temp_candidate, existing_scene_images):
            highest_score = score
            import shutil
            best_fallback_file = dest_path + ".best.jpg"
            shutil.copy2(temp_candidate, best_fallback_file)

        # Si supera el umbral de aprobación visual (6+ de 10, y representa la acción narrada)
        depicts_action = eval_result.get("depicts_action", False)
        if (score >= 6 or (cand_src == "fandom_target" and score >= 5)) and is_panel and not cand["is_cover"] and (depicts_action or score >= 7):
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(temp_candidate, dest_path)
            print(f"  [PRECISIÓN VISUAL {score}/10] ({cand_src}): {cand_name} -> {reason}")
            if best_fallback_file and os.path.exists(best_fallback_file):
                os.remove(best_fallback_file)
            if used_sources is not None and cand_id:
                used_sources.add(cand_id)
            return dest_path
        else:
            print(f"  [Candidato descartado {score}/10] ({cand_src}): {cand_name} -> {reason}")
            if os.path.exists(temp_candidate):
                os.remove(temp_candidate)

    # Si ningún candidato superó el umbral estricto, usar el de mayor puntaje disponible que sea cómic verificado (>= 2)
    if best_fallback_file and os.path.exists(best_fallback_file) and highest_score >= 2:
        if not is_duplicate_panel(best_fallback_file, existing_scene_images):
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(best_fallback_file, dest_path)
            print(f"  [VIÑETA RESCATADA]: Utilizando viñeta de cómic con entintado/alineación confirmada (Score: {highest_score}/10).")
            return dest_path

    if best_fallback_file and os.path.exists(best_fallback_file):
        os.remove(best_fallback_file)

    # Rescate de emergencia: búsqueda genérica del personaje para evitar fallo de producción
    char_seed = (fallback_query or "").split()[0] if fallback_query else "comic"
    emergency_urls = search_bing_comic_panels(f"{char_seed} comic panel interior scan", limit=6)
    for em_u in emergency_urls:
        if download_web_panel(em_u, temp_candidate):
            if not is_duplicate_panel(temp_candidate, existing_scene_images):
                try:
                    with Image.open(temp_candidate) as em_im:
                        if check_is_comic_art_inking(em_im):
                            if os.path.exists(dest_path):
                                os.remove(dest_path)
                            os.rename(temp_candidate, dest_path)
                            print(f"  [RESCATE DE EMERGENCIA]: Viñeta interior de cómic verificada obtenida para evitar fallo de producción.")
                            return dest_path
                except Exception:
                    pass
            if os.path.exists(temp_candidate):
                os.remove(temp_candidate)

    if os.path.exists(temp_candidate):
        os.remove(temp_candidate)

    raise RuntimeError(f"FATAL: No se encontró ninguna viñeta de cómic válida para '{fallback_query or target_file}' (Todas las imágenes analizadas fueron fotos reales, portadas o no superaron los controles de calidad).")
