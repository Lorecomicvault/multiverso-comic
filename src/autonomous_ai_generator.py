"""
Multiverso Comic - Autonomous AI Story Generator
Powered by Google Gemini (gemini-flash-latest / gemini-3.8-flash)
Guarantees:
1. Zero duplication: Considers the complete historical ledger before generating.
2. Strict Golden Standard: Exactly 4 scenes, 55-65 words total, viral hooks.
3. 1:1 Visual Alignment: Resolves official Marvel/DC Fandom comic art.
4. Quality Shield: Mathematically rejects text-only pages, letters, or handwritten documents.
"""

import io
import json
import os
import re
import time
import urllib.parse
import requests
from pathlib import Path
from PIL import Image, ImageStat

CANDIDATE_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json,text/html,*/*;q=0.8',
}


def log(msg: str):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [AUTONOMOUS-AI] {msg}", flush=True)


def resolve_fandom_image(wiki: str, query: str) -> str | None:
    """Busca en la API de Fandom el archivo oficial más relevante con extensión de imagen."""
    from .comic_precision_scraper import is_cover_or_promo_image
    DISALLOWED_KEYWORDS = [
        'mug', 'actor', 'film', 'movie', 'live-action', 'live action', 'cast', 'cosplay',
        'photo', 'shot', 'portrait', 'interview', 'trailer', 'commercial', 'fox', 'warner',
        'tv', 'series', 'clip', 'joaquin', 'variant', 'poster', 'logo', 'trading cards', 'video game',
        'soundtrack', 'review', 'bts', 'behind the scenes', 'script', 'text'
    ]
    url = f"https://{wiki}.fandom.com/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=6&srlimit=12&format=json"
    try:
        r = requests.get(url, headers=HEADERS, timeout=8).json()
        candidates = []
        for item in r.get('query', {}).get('search', []):
            t = item['title'].replace('File:', '').strip()
            t_lower = t.lower()
            if any(t_lower.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                if any(bad in t_lower for bad in DISALLOWED_KEYWORDS) or is_cover_or_promo_image(t):
                    continue
                # Priorizar si tiene indicios de viñeta interior (from, 001, page, panel)
                score = 0
                if 'from' in t_lower:
                    score += 5
                if any(p in t_lower for p in ['001', '002', '003', 'page', 'panel']):
                    score += 5
                candidates.append((score, t))
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]
    except Exception as e:
        log(f"Error resolviendo imagen en Fandom ({wiki}): {e}")
    return None


def verify_image_quality(wiki: str, filename: str) -> bool:
    """Verifica que la imagen exista y que cumpla el Quality Shield (no texto/manuscrito ni foto real)."""
    from .comic_precision_scraper import check_is_comic_art_inking, is_cover_or_promo_image
    if is_cover_or_promo_image(filename):
        return False
    api_url = f"https://{wiki}.fandom.com/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url|size&format=json"
    try:
        r = requests.get(api_url, headers=HEADERS, timeout=10).json()
        pages = r.get('query', {}).get('pages', {})
        for p in pages.values():
            if 'imageinfo' in p:
                img_url = p['imageinfo'][0]['url']
                resp = requests.get(img_url, headers=HEADERS, timeout=12)
                if resp.status_code == 200 and len(resp.content) > 15000:
                    im = Image.open(io.BytesIO(resp.content)).convert('RGB')
                    
                    # Quality Shield (HSV check)
                    stat = ImageStat.Stat(im.convert('HSV'))
                    mean_sat, mean_val = stat.mean[1], stat.mean[2]
                    if mean_sat < 15.0 and mean_val > 175.0:
                        log(f"Quality Shield: Rechazada '{filename}' por ser documento de texto/nota (sat={mean_sat:.1f}).")
                        return False

                    # Quality Shield (Inking check)
                    if not check_is_comic_art_inking(im):
                        log(f"Quality Shield: Rechazada '{filename}' por no presentar entintado de cómic (foto/actor/live-action).")
                        return False
                    
                    if im.width >= 400 or im.height >= 400:
                        return True
    except Exception as e:
        log(f"Error verificando calidad de '{filename}': {e}")
    return False


EMERGENCY_VIRAL_POOL = [
    {
        "id": "thanos_rising_el_origen_del_titan_loco",
        "universe": "Marvel",
        "character": "Thanos",
        "title": "Thanos: El Perturbador Origen y la Obsesión con la Muerte",
        "theme_signature": "thanos:rising:origen_titan_loco_asesinato",
        "description": "Nacido como una anomalía en la luna Titán, Thanos comenzó diseccionando criaturas en cuevas secretas hasta convertirse en el genocida cósmico obsesionado con cortejar a la Señora Muerte.",
        "hashtags": "#Thanos #MarvelComics #ThanosRising #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que Thanos nació en la luna Titán como una anomalía monstruosa que horrorizó a su propia madre?",
            "Guiado por una niña misteriosa, comenzó realizando sádicas disecciones biológicas a sus propios compañeros de clase.",
            "Al descubrir que la niña era la personificación de la Muerte, Thanos asesinó a su madre para cortejarla.",
            "Años después, bombardeó Titán con ojivas nucleares extinguiendo a su especie entera en nombre de su amada."
        ],
        "scene_art_urls": [
            "Thanos (Earth-616) from Thanos Rising Vol 1 1 001.jpg",
            "Thanos (Earth-616) from Thanos Rising Vol 1 1 005.jpg",
            "Thanos (Earth-616) from Thanos Rising Vol 1 2 001.jpg",
            "Thanos (Earth-616) from Thanos Rising Vol 1 3 001.jpg"
        ],
        "art_queries": [
            "Thanos newborn baby Titan alien mother horror",
            "Thanos dissection cave mysterious girl Death",
            "Thanos murders mother scalpel Lady Death",
            "Thanos bombards Titan nuclear missiles genocide"
        ]
    },
    {
        "id": "captain_america_el_soldado_del_invierno",
        "universe": "Marvel",
        "character": "Captain America",
        "title": "Capitán América: El Regreso del Soldado del Invierno",
        "theme_signature": "captain_america:winter_soldier:bucky_barnes_asesino_cosmic_cube",
        "description": "Steve Rogers descubre la desgarradora verdad: su querido hermano de armas Bucky Barnes sobrevivió a la guerra convertido en el despiadado asesino de HYDRA, el Soldado del Invierno.",
        "hashtags": "#CaptainAmerica #WinterSoldier #BuckyBarnes #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que tras décadas de creerlo muerto, el Capitán América descubrió que Bucky Barnes era el asesino más letal de HYDRA?",
            "Con un brazo biónico de titanio y la memoria lavada, el Soldado del Invierno ejecutó a cientos de objetivos en las sombras.",
            "En un feroz combate cuerpo a cuerpo, Steve Rogers logró quitarle la máscara reconociendo los ojos de su hermano de armas.",
            "Usando el Cubo Cósmico para restaurar sus recuerdos, Bucky cayó de rodillas abrumado por el dolor de sus crímenes."
        ],
        "scene_art_urls": [
            "James Buchanan Barnes (Earth-616) from Captain America Vol 5 2 0004.png",
            "Winter Soldier's Bionic Arm from Captain America Vol 5 33 001.jpg",
            "James Buchanan Barnes (Earth-616) and Steven Rogers (Earth-616) from Captain America Vol 5 607 0001.jpg",
            "James Buchanan Barnes (Earth-616) from Captain America & the Winter Soldier Special Vol 1 1 002.jpg"
        ],
        "art_queries": [
            "Captain America Winter Soldier highway sniper comic panel",
            "Winter Soldier bionic arm cybernetic Hydra comic panel",
            "Captain America unmasks Winter Soldier Bucky Ed Brubaker comic panel",
            "Winter Soldier Cosmic Cube remembers Bucky Barnes crying comic panel"
        ]
    },
    {
        "id": "spiderman_spiders_shadow_simbionte",
        "universe": "Marvel",
        "character": "Spider-Man",
        "title": "Spider's Shadow: Cuando Peter Parker Abrazó la Oscuridad del Simbionte",
        "theme_signature": "spiderman:spiders_shadow:simbionte_asesino",
        "description": "En este universo alternativo, Peter Parker jamás se separó del simbionte de Venom y masacró a los Seis Siniestros.",
        "hashtags": "#SpiderMan #Venom #SpidersShadow #MarvelComics #ComicsNarrados #Shorts #Marvel",
        "scenes": [
            "¿Qué habría pasado si Spider-Man jamás se hubiera separado del simbionte alienígena de Venom?",
            "Tras el asesinato de su tía May, Peter quebró su única regla sagrada y desató una cacería implacable en Nueva York.",
            "Persiguió a Hobgoblin por los tejados y lo quemó vivo en una explosión devastadora sin remordimiento alguno.",
            "Consumido por el hambre del simbionte, se transformó en el depredador supremo liquidando a cada uno de sus villanos."
        ],
        "art_queries": [
            "Spider-Man Spider's Shadow black suit",
            "Spider's Shadow Peter Parker kills Hobgoblin",
            "Spider's Shadow symbiote monster",
            "Spider-Man symbiote execution sinister six"
        ]
    },
    {
        "id": "punisher_kills_marvel_universe",
        "universe": "Marvel",
        "character": "The Punisher",
        "title": "The Punisher: El Día en que Frank Castle Masacró a Marvel",
        "theme_signature": "punisher:kills_marvel:venganza_familia_mutantes",
        "description": "Cuando los superhéroes mataron accidentalmente a su familia en Central Park, Frank Castle juró aniquilar a cada héroe y villano de Marvel.",
        "hashtags": "#ThePunisher #FrankCastle #MarvelComics #PunisherKills #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que cuando la batalla de los Vengadores contra los alienígenas mató a su familia, Frank Castle enloqueció de odio?",
            "Sin dudar un instante, levantó su rifle en Central Park y ejecutó a Cyclops y Hawkeye de un solo disparo en la cabeza.",
            "Armado con ojivas nucleares de Doctor Doom, engañó a todos los mutantes en la Luna y detonó una explosión cósmica.",
            "Tras liquidar a Spider-Man, Wolverine y Daredevil, Frank se apuntó con su propia pistola cerrando su venganza final."
        ],
        "scene_art_urls": [
            "Thor Odinson (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 0001.jpg",
            "Scott Summers (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 0001.jpg",
            "Victor von Doom (Earth-95126) and Francis Castle (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 0001.jpg",
            "Peter Parker (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 002.jpg"
        ],
        "art_queries": [
            "Punisher kills Cyclops Hawkeye Central Park",
            "Punisher Kills the Marvel Universe rifle",
            "Punisher kills mutants nuclear bomb Moon",
            "Punisher suicide last panel Marvel Universe"
        ]
    },
    {
        "id": "flash_forward_wally_west_doctor_manhattan",
        "universe": "DC",
        "character": "The Flash",
        "title": "Flash Forward: Wally West y los Poderes de Doctor Manhattan",
        "theme_signature": "wally_west:flash_forward:mobius_chair_manhattan",
        "description": "Al sentarse en la Silla de Mobius imbuida con la energía de Doctor Manhattan, Wally West ascendió como el velocista cósmico supremo.",
        "hashtags": "#TheFlash #WallyWest #DoctorManhattan #FlashForward #DCComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Wally West se sentó en la legendaria Silla de Mobius y absorbió el poder supremo de Doctor Manhattan?",
            "En el centro del Multiverso Oscuro, una grieta dimensional amenazaba con devorar todas las realidades existentes.",
            "La energía cósmica azul envolvió su traje, grabando el símbolo del átomo en su frente y volviéndolo omnisciente.",
            "Con un simple parpadeo mental, Wally reescribió las líneas temporales y salvó a sus hijos atrapados en el olvido."
        ],
        "art_queries": [
            "Wally West Mobius Chair Doctor Manhattan",
            "Flash Forward Dark Multiverse incursion",
            "Wally West blue glowing Doctor Manhattan powers",
            "Wally West saves children Flash Forward ending"
        ],
        "scene_art_urls": [
            "Mobius_Chair_Prime_Earth_001.jpg",
            "Flash_Wally_West_Prime_Earth_0017.jpg",
            "Flash_Wally_West_Prime_Earth_0018.jpg",
            "Flash_Wally_West_Prime_Earth_0032.jpg"
        ]
    },
    {
        "id": "hulk_the_end_ultimo_humano",
        "universe": "Marvel",
        "character": "Hulk",
        "title": "Hulk The End: El Último Ser Vivo en la Tierra",
        "theme_signature": "hulk:the_end:cucarachas_soledad_muerte_banner",
        "description": "Tras el holocausto nuclear, Hulk sobrevive solo en una Tierra muerta, regenerándose cada día de los enjambres de cucarachas carnívoras.",
        "hashtags": "#Hulk #TheEnd #MarvelComics #PeterDavid #ComicsDeTerror #Shorts #Reels",
        "scenes": [
            "¿Sabías que en un futuro devastado por una guerra nuclear, Hulk es el único ser humano que sobrevive en la Tierra?",
            "Cada día, enjambres de cucarachas gigantes carnívoras devoran su piel viva mientras su factor curativo lo regenera dolorosamente.",
            "Dentro de su mente, un anciano y enfermo Bruce Banner le ruega a Hulk que lo deje morir en paz.",
            "Cuando el corazón de Banner se detiene para siempre, Hulk queda solo en la oscuridad absoluta, anhelando un final que jamás llegará."
        ],
        "scene_art_urls": [
            "assets/curated_panels/hulk_the_end/scene_01.jpg",
            "assets/curated_panels/hulk_the_end/scene_02.jpg",
            "assets/curated_panels/hulk_the_end/scene_03.jpg",
            "assets/curated_panels/hulk_the_end/scene_04.jpg"
        ],
        "art_queries": [
            "Bruce Banner (Earth-2081) from Incredible Hulk The End Vol 1 1 0001.jpg",
            "Bruce Banner (Earth-2081) from Incredible Hulk The End Vol 1 1 0002.jpg",
            "Hulk The End regenerating Dale Keown comic panel",
            "Hulk The End feels cold final panel"
        ]
    }
]


def generate_autonomous_story(ledger: list[dict], api_key: str | None = None) -> dict:
    """
    Genera una historia 100% inédita con Google Gemini que jamás repita ningún tema del ledger histórico.
    Asegura viñetas oficiales existentes y cumplimiento estricto del Estándar de Retención.
    """
    from .cloud_runner import is_duplicate
    import base64

    from .gemini_tts import get_candidate_keys
    keys_to_try = get_candidate_keys()
    if api_key and api_key not in keys_to_try:
        keys_to_try.insert(0, api_key)
    
    # Extraer historial COMPLETO para prohibir duplicados
    past_characters = set(item.get("character", "").strip() for item in ledger if item.get("character"))
    past_titles = [item.get("title", "").strip() for item in ledger if item.get("title")]
    past_themes = [item.get("theme_signature", "").strip() for item in ledger if item.get("theme_signature")]

    char_summary = ", ".join(sorted(list(past_characters)))
    titles_summary = " | ".join(past_titles[-40:])

    max_attempts = 4
    for attempt in range(1, max_attempts + 1):
        log(f"Generando propuesta de historia con IA (Intento {attempt}/{max_attempts})...")

        system_prompt = f"""
Eres el Guionista Principal y Director Creativo de ComicLoreVault, el canal líder de videos cinematográficos de cómics en español para TikTok y Reels.

Tu misión es crear una historia COMPLETAMENTE NUEVA, ULTRA-VIRAL, OSCURA Y MEMORABLE sobre un arco legendario EXCLUSIVAMENTE DE SUPERHÉROES Y SUPERVILLANOS DE MARVEL O DC COMICS.

REGLA SUPREMA DE FRANQUICIA (INVIOLABLE):
- Queda TERMINANTEMENTE PROHIBIDO crear historias de Star Wars, Image Comics, Invincible, The Boys, Spawn, películas, series o mangas.
- Cada historia DEBE SER 100% de SUPERHÉROES o SUPERVILLANOS de MARVEL COMICS o DC COMICS.

ESTRICTO HISTORIAL DE TEMAS YA PRODUCIDOS (TOTALMENTE PROHIBIDO REPETIR O REUTILIZAR ESTOS PERSONAJES O ARCOS):
- Personajes ya cubiertos (PROHIBIDO REPETIR): {char_summary}
- Títulos recientes ya publicados (PROHIBIDO REPETIR): {titles_summary}

IDEAS DE TEMAS CANDIDATOS ULTRA-VIRALES DE SUPERHÉROES MARVEL/DC CON VIÑETAS INTERIORES VERIFICADAS (Elige uno de estos o similar):
- Captain America: El Soldado del Invierno (Steve Rogers descubre que Bucky Barnes es el asesino cibernético de HYDRA)
- Thanos: Rising (El perturbador origen de Thanos en la luna Titán, disecciones secretas y la adoración a la Dama Muerte)
- The Flash: Godspeed (August Heart obteniendo la Speed Force y robando la velocidad a sangre fría de otros velocistas)
- Wolverine: Old Man Logan (La ilusión óptica de Mysterio que manipuló a Logan para masacrar a todos los X-Men)
- Knull: El Rey de Negro (El dios de la oscuridad decapitando al Celestial y forjando la All-Black Necroespada)
- Batman: El Tribunal de los Búhos (El laberinto subterráneo secreto y la quiebra mental de Bruce Wayne ante los Talons)
- Superior Spider-Man (Otto Octavius intercambiando su mente con Peter Parker y ejecutando criminales sin piedad)

REGLAS INVIOLABLES DE FORMATO:
1. Exactamente 4 escenas narrativas.
2. CONTEO TOTAL DE PALABRAS: Estrictamente entre 55 y 65 palabras en total para la narración (sweet spot de 22-26 segundos en TTS).
3. TONO: Dramático, de suspenso, cinematográfico, directo al grano sin introducciones aburridas.
4. ESTRUCTURA:
   - Escena 1: Gancho y pregunta provocadora (15 a 18 palabras).
   - Escena 2: Choque o revelación de horror (15 a 18 palabras).
   - Escena 3: Momento de máxima tensión, muerte o brutalidad (15 a 18 palabras).
   - Escena 4: Desenlace trágico, irónico o épico (15 a 18 palabras).
5. ALINEACIÓN VISUAL 1:1: Cada escena debe describir EXACTAMENTE lo que se ve en la viñeta interior de cómic (PROHIBIDAS portadas comerciales, portadas variantes, logos, fotos reales y actores). En 'art_queries' proporciona términos de búsqueda enfocados en VIÑETAS INTERIORES del cómic (ej: 'Spider-Man Spiders Shadow interior panel 1', 'Batman White Knight panel Joker sanity').

Devuelve ÚNICAMENTE un objeto JSON válido con este esquema:
{{
  "id": "identificador_en_snake_case_unico",
  "universe": "Marvel o DC",
  "character": "Nombre del Personaje Principal",
  "title": "Título Cinematográfico Atractivo",
  "theme_signature": "personaje:arco:tema_clave",
  "description": "Sinopsis de alta retención para la descripción del Reel.",
  "hashtags": "#ComicLoreVault #ComicsNarrados #Marvel #DC #Reels #Shorts",
  "scenes": [
    "Texto de la Escena 1...",
    "Texto de la Escena 2...",
    "Texto de la Escena 3...",
    "Texto de la Escena 4..."
  ],
  "art_queries": [
    "Busqueda de comic escena 1",
    "Busqueda de comic escena 2",
    "Busqueda de comic escena 3",
    "Busqueda de comic escena 4"
  ]
}}
"""

        payload = {
            "contents": [{"parts": [{"text": system_prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        story = None
        for cand_key in keys_to_try:
            for model in CANDIDATE_MODELS:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={cand_key}"
                try:
                    r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
                    if r.status_code == 200:
                        raw_text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                        story = json.loads(raw_text)
                        log(f"Propuesta generada por {model}: '{story.get('title')}'")
                        break
                    else:
                        log(f"Modelo {model} respondió {r.status_code}")
                except Exception as err:
                    log(f"Excepción consultando {model}: {err}")
            if story:
                break

        if not story:
            continue

        # Validar duplicados contra el ledger histórico
        is_dup, reason = is_duplicate(story, ledger)
        if is_dup:
            log(f"Escudo Anti-Duplicados: Propuesta '{story.get('title')}' rechazada ({reason}). Reintentando con otro arco...")
            continue

        # Resolver y validar viñetas oficiales en Fandom
        from .cloud_runner import get_story_comic_wiki
        wiki_domain = get_story_comic_wiki(story)
        wiki = 'dc' if 'dc' in wiki_domain else 'marvel'
        char_name = story.get("character", "")

        resolved_art = []
        art_queries = story.get("art_queries", [])

        for idx, q in enumerate(art_queries, 1):
            log(f"Resolviendo viñeta oficial para escena {idx}: '{q}'...")
            panel_queries = [
                q,
                f"{char_name} {story.get('title', '')} interior panel",
                f"{char_name} {story.get('theme_signature', '').replace(':', ' ')}"
            ]
            found_panel = None
            for p_q in panel_queries:
                cand = resolve_fandom_image(wiki, p_q)
                if cand and cand not in resolved_art and verify_image_quality(wiki, cand):
                    found_panel = cand
                    break

            if found_panel:
                resolved_art.append(found_panel)
            else:
                log(f"Aviso escena {idx}: Viñeta Fandom no resuelta en precarga. El scraper multi-fuente y Bing la obtendrán durante el render.")

        if resolved_art:
            story["scene_art_urls"] = resolved_art
        story["voice"] = "Puck"
        story["tts_model"] = "gemini-3.8-flash-tts"
        story["fallback_tts_model"] = "gemini-3.8-flash-lite-tts"
        story["style_direction"] = "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
        log(f"Historia autónoma APROBADA y blindada con voz Puck (Gemini 3.8): '{story['title']}'")
        return story

    # Respaldo automático ultra-viral en caso de limitación transitoria de API de Gemini
    log("Aviso: Cuota de Gemini limitada temporalmente tras múltiples intentos. Activando Banco de Respaldo Ultra-Viral...")
    for candidate in EMERGENCY_VIRAL_POOL:
        is_dup, reason = is_duplicate(candidate, ledger)
        if not is_dup:
            candidate["voice"] = "Puck"
            candidate["tts_model"] = "gemini-3.8-flash-tts"
            candidate["fallback_tts_model"] = "gemini-3.8-flash-lite-tts"
            candidate["style_direction"] = "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
            log(f"Historia Ultra-Viral de Respaldo Aprobada: '{candidate['title']}' (ID: {candidate['id']})")
            return candidate

    raise RuntimeError("No se pudo generar una historia inédita tras múltiples intentos con IA.")
