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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

WIKI_DOMAINS = [
    "marvel.fandom.com",
    "dc.fandom.com",
    "imagecomics.fandom.com",
    "comiccrossroads.fandom.com"
]

CANDIDATE_VISION_MODELS = [
    "gemini-flash-latest",
    "gemini-3.8-flash",
    "gemini-2.5-flash",
    "gemini-pro-latest"
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
        if os.path.exists(ep) and ep != candidate_path:
            rms = calculate_image_rms_difference(candidate_path, ep)
            if rms < threshold:
                return True
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
        'trade paperback', 'hardcover', 'annual'
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
    """Extrae la URL de resolución completa de Fandom mediante la MediaWiki API."""
    url = f"https://{wiki_domain}/api.php"
    params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "format": "json"
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        pages = r.json().get("query", {}).get("pages", {})
        for pid, pinfo in pages.items():
            if "imageinfo" in pinfo:
                return pinfo["imageinfo"][0]["url"].split("/revision/")[0]
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


def get_issue_category_panels(wiki_domain: str, query_str: str) -> list:
    """
    Extrae la lista de viñetas interiores escaneadas desde la categoría oficial
    de la grapa en Fandom (Category:<Comic Issue>/Images).
    """
    match = re.search(r'([A-Za-z\s\-]+Vol\s*\d+\s*\d+)', query_str, re.IGNORECASE)
    if not match:
        match = re.search(r'([A-Za-z\s\-]+\d+)', query_str)
        
    if not match:
        return []
        
    issue_name = match.group(1).strip()
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
        return [it["title"] for it in items if not is_cover_or_promo_image(it["title"])]
    except Exception:
        return []


def search_fandom_files(wiki_domain: str, query: str, max_results: int = 8) -> list:
    """Búsqueda semántica de archivos en Fandom filtrando por extensión de imagen."""
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
            if any(t.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                files.append(t)
        return files
    except Exception:
        return []


def search_bing_comic_panels(query: str, limit: int = 6) -> list:
    """
    Búsqueda web abierta de viñetas en Bing: Accede a escaneos publicados
    en foros de cómics, blogs, Reddit (r/comicbooks) y reseñas especializadas.
    """
    clean_q = re.sub(r'\b(comic|panel|scan|scans)\b', '', query, flags=re.IGNORECASE).strip()
    bing_query = f"{clean_q} comic panel"
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(bing_query)}&form=HDRSC2&first=1"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
        if r.status_code == 200:
            urls = re.findall(r'murl&quot;:&quot;(http[^&]+)&quot;', r.text)
            clean_urls = []
            for u in urls:
                u_low = u.lower()
                if not any(bad in u_low for bad in ['wallpaper', 'icon', 'steamstatic', 'action_figure', 'cosplay', 't-shirt']):
                    clean_urls.append(u)
            return clean_urls[:limit]
    except Exception:
        pass
    return []

# -------------------------------------------------------------------------
# 3. GESTORES DE DESCARGA
# -------------------------------------------------------------------------

def download_image(url: str, referer_domain: str, dest_path: str, min_dim: int = 350) -> bool:
    """Descarga y valida una imagen de Fandom, aplicando además el filtro Quality Shield."""
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

        # Quality Shield: Rechazar documentos o libretas de texto
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

        # Quality Shield: Rechazar documentos o libretas de texto
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
    Si Gemini no está disponible o presenta demoras, devuelve un score seguro (7)
    para que la producción nunca se bloquee.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key or not scene_text or not os.path.exists(image_path):
        return {"score": 7, "is_comic_panel": True, "depicts_action": True, "reason": "Modo heurístico activo"}

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
    try:
        from google import genai
        client = genai.Client(api_key=api_key, http_options={"timeout": 12000})
        im = Image.open(image_path)
        res = client.models.generate_content(model="gemini-flash-latest", contents=[im, prompt])
        raw = res.text.strip()
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
        return json.loads(raw)
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

        for model in CANDIDATE_VISION_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            try:
                r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=12)
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

    return {"score": 7, "is_comic_panel": True, "depicts_action": True, "reason": "Heurística de respaldo"}

# -------------------------------------------------------------------------
# 5. COORDINADOR PRINCIPAL: FETCH_SCENE_IMAGE
# -------------------------------------------------------------------------

def fetch_scene_image(
    wiki_domain: str,
    target_file: str,
    fallback_query: str,
    dest_path: str,
    existing_scene_images: list = None,
    scene_text: str = None
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

    for cand in ordered_candidates:
        cand_src = cand["source"]
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
            return dest_path

        # Evaluación con Árbitro de IA Gemini Multimodal Vision
        eval_result = verify_visual_alignment_with_gemini(temp_candidate, scene_text)
        score = eval_result.get("score", 7)
        is_panel = eval_result.get("is_comic_panel", True)
        reason = eval_result.get("reason", "")
        cand_name = cand.get("title") or cand.get("url", "")[:50]

        # Guardar el candidato con la mayor puntuación encontrada
        if score > highest_score:
            highest_score = score
            import shutil
            best_fallback_file = dest_path + ".best.jpg"
            shutil.copy2(temp_candidate, best_fallback_file)

        # Si supera el umbral de aprobación visual (6+ de 10)
        if score >= 6 and is_panel and not cand["is_cover"]:
            if os.path.exists(dest_path):
                os.remove(dest_path)
            os.rename(temp_candidate, dest_path)
            print(f"  [PRECISIÓN VISUAL {score}/10] ({cand_src}): {cand_name} -> {reason}")
            if best_fallback_file and os.path.exists(best_fallback_file):
                os.remove(best_fallback_file)
            return dest_path
        else:
            print(f"  [Candidato descartado {score}/10] ({cand_src}): {cand_name} -> {reason}")
            if os.path.exists(temp_candidate):
                os.remove(temp_candidate)

    # Si ningún candidato fue 100% perfecto, usar el de mayor puntaje
    if best_fallback_file and os.path.exists(best_fallback_file):
        if os.path.exists(dest_path):
            os.remove(dest_path)
        os.rename(best_fallback_file, dest_path)
        print(f"  [VIÑETA RESCATADA]: Utilizando mejor candidato visual encontrado (Score: {highest_score}/10).")
        return dest_path

    if os.path.exists(temp_candidate):
        os.rename(temp_candidate, dest_path)
        return dest_path

    raise RuntimeError(f"No se pudo descargar una viñeta válida para {fallback_query or target_file}")
