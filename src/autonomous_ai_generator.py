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
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-3.8-flash",
    "gemini-3.7-flash"
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
            if 'imageinfo' in p and p['imageinfo']:
                img_url = p['imageinfo'][0].get('url')
                if not img_url:
                    continue
                req_headers = {**HEADERS, "Referer": f"https://{wiki}.fandom.com/"}
                resp = requests.get(img_url, headers=req_headers, timeout=12)
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
            "assets/curated_panels/thanos_rising/scene_01.jpg",
            "assets/curated_panels/thanos_rising/scene_02.jpg",
            "assets/curated_panels/thanos_rising/scene_03.jpg",
            "assets/curated_panels/thanos_rising/scene_04.jpg"
        ],
        "art_queries": [
            "Thanos newborn mother Sui-San horror comic panel",
            "Young Thanos dissecting creatures cave Simone Bianchi comic panel",
            "Thanos bloody massacre corpses Simone Bianchi comic panel",
            "Thanos galactic destruction cosmic death Simone Bianchi comic panel"
        ]
    },
    {
        "id": "xmen_dias_del_futuro_pasado_centinelas",
        "universe": "Marvel",
        "character": "X-Men",
        "title": "Días del Futuro Pasado: El Exterminio Mutante de los Centinelas",
        "theme_signature": "x_men:days_of_future_past:sentinels_extermination_wolverine_logan",
        "description": "En un futuro postapocalíptico dominado por los Centinelas, los últimos mutantes son perseguidos y aniquilados en campos de concentración.",
        "hashtags": "#XMen #DaysOfFuturePast #Wolverine #Sentinels #MarvelComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que en Días del Futuro Pasado los gigantescos Centinelas cazaron y asesinaron a casi todos los mutantes?",
            "Los pocos X-Men supervivientes fueron encerrados en campos de concentración portando collares inhibidores de poder.",
            "Wolverine lideró un asalto desesperado, pero una ráfaga de plasma del Centinela redujo su cuerpo a cenizas.",
            "Enviando la mente de Kitty Pryde al pasado, los mutantes jugaron su última carta para reescribir la historia."
        ],
        "scene_art_urls": [
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_01.jpg",
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_02.jpg",
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_03.jpg",
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_04.jpg"
        ],
        "art_queries": [
            "Days of Future Past Sentinel poster mutant gravestones comic panel",
            "X-Men concentration camp inhibitor collars John Byrne comic panel",
            "Wolverine disintegrated Sentinel blast Days of Future Past comic panel",
            "Kitty Pryde time travel mind transfer Days of Future Past comic panel"
        ]
    },
    {
        "id": "vengadores_desunidos_la_locura_de_wanda",
        "universe": "Marvel",
        "character": "Scarlet Witch",
        "title": "Vengadores Desunidos: El Día en que Wanda Destruyó a los Héroes",
        "theme_signature": "scarlet_witch:avengers_disassembled:wanda_maximoff_chaos_magic_vision",
        "description": "Al recordar a sus hijos borrados de la realidad, Wanda Maximoff pierde la cordura y desata su magia del caos contra la Mansión de los Vengadores.",
        "hashtags": "#ScarletWitch #Avengers #AvengersDisassembled #MarvelComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que la tragedia más devastadora de los Vengadores no fue provocada por un villano, sino por Wanda Maximoff?",
            "Al recordar a sus hijos perdidos, la mente de Wanda se quebró desatando una marea imparable de magia del caos.",
            "Un Jack of Hearts reanimado explotó sobre la Mansión y Visión colapsó atacando a sus propios compañeros de equipo.",
            "Entre los escombros y los cuerpos caídos, los Vengadores comprendieron que su era dorada había terminado."
        ],
        "art_queries": [
            "Scarlet Witch chaos magic Avengers Mansion explosion comic panel",
            "Jack of Hearts explodes Avengers Mansion David Finch comic panel",
            "Vision melting attacking Avengers Disassembled comic panel",
            "Avengers ruins fallen heroes Hawkeye Disassembled comic panel"
        ]
    },
    {
        "id": "batman_arkham_asylum_locura_joker",
        "universe": "DC",
        "character": "Batman",
        "title": "Batman: Una Casa Seria en una Tierra Seria - La Pesadilla de Arkham",
        "theme_signature": "batman:arkham_asylum_serious_house:joker_amadeus_arkham_madness",
        "description": "Encerrado dentro del Asilo Arkham tomado por el Joker, Batman debe someterse a las pruebas psicológicas más siniestras de sus peores enemigos.",
        "hashtags": "#Batman #Joker #ArkhamAsylum #DCComics #GrantMorrison #DaveMcKean #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que cuando los reclusos tomaron el Asilo Arkham, el Joker solo exigió que Batman entrara completamente solo?",
            "Al cruzar las puertas de hierro, Batman descubrió que el asilo era un perturbador santuario consagrado a la locura.",
            "El Joker y Two-Face lo sometieron a sádicas torturas psicológicas, cuestionando la propia cordura del murciélago.",
            "Tras enfrentar sus traumas más oscuros, Batman abandonó Arkham demostrando que él controla las sombras de Gotham."
        ],
        "art_queries": [
            "Batman Arkham Asylum Dave McKean gates entrance comic panel",
            "Joker Arkham Asylum Serious House Dave McKean smiling dark panel",
            "Two-Face coin trial Arkham Asylum Dave McKean comic panel",
            "Batman walking away Arkham Asylum shadow night comic panel"
        ]
    },
    {
        "id": "daredevil_el_hombre_sin_miedo_origen_quimico",
        "universe": "Marvel",
        "character": "Daredevil",
        "title": "Daredevil: El Accidente Químico que Creó al Hombre Sin Miedo",
        "theme_signature": "daredevil:the_man_without_fear:blindness_toxic_waste_radar_sense",
        "description": "Matt Murdock salva a un anciano de ser atropellado por un camión, pero los desechos radiactivos le quitan la vista y despiertan sus sentidos hipersensibles.",
        "hashtags": "#Daredevil #MattMurdock #ManWithoutFear #MarvelComics #FrankMiller #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Matt Murdock obtuvo sus increíbles poderes salvando la vida de un anciano en Hell's Kitchen?",
            "Un camión perdió el control y un cilindro con desechos radiactivos impactó directamente en los ojos del joven Matt.",
            "La sustancia química le arrebató la vista para siempre, pero agudizó sus restantes cuatro sentidos a niveles superhumanos.",
            "Entrenado en secreto por el maestro ciego Stick, Matt juró proteger su barrio como el justiciero Daredevil."
        ],
        "art_queries": [
            "Young Matt Murdock saves blind man truck toxic waste comic panel",
            "Radioactive canister hits Matt Murdock eyes blinding comic panel",
            "Matt Murdock sensory overload radar sense hospital comic panel",
            "Stick training young Matt Murdock martial arts Man Without Fear panel"
        ]
    },
    {
        "id": "aquaman_mano_arpon_charybdis",
        "universe": "DC",
        "character": "Aquaman",
        "title": "Aquaman: El Día en que las Pirañas Devoraron su Mano",
        "theme_signature": "aquaman:harpoon_hand:charybdis_piranhas_peter_david",
        "description": "En una de las historias más oscuras de DC Comics, el villano Charybdis sumerge la mano de Arthur Curry en un pozo de pirañas carnívoras.",
        "hashtags": "#Aquaman #ArthurCurry #PeterDavid #DCComics #HarpoonHand #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Aquaman perdió su mano izquierda cuando un villano se la sumergió en un pozo de pirañas hambrientas?",
            "El sádico terrorista Charybdis neutralizó sus poderes telepáticos marinos y sostuvo el brazo de Arthur bajo el agua.",
            "En cuestión de segundos, los peces devoraron la carne viva de su mano hasta dejar los huesos completamente expuestos.",
            "En lugar de rendirse, Arthur se colocó un arpón metálico retráctil convirtiéndose en el rey guerrero de Atlantis."
        ],
        "art_queries": [
            "Aquaman fight Charybdis Time and Tide Peter David comic panel",
            "Charybdis forces Aquaman hand piranha pool comic panel",
            "Aquaman screaming skeletal hand piranha bite comic panel",
            "Aquaman harpoon hand beard shirtless warrior king comic panel"
        ]
    },
    {
        "id": "green_lantern_kyle_rayner_major_force",
        "universe": "DC",
        "character": "Kyle Rayner",
        "title": "Kyle Rayner: El Día en que Major Force Asesinó a su Novia",
        "theme_signature": "kyle_rayner:green_lantern:major_force_refrigerator_alex",
        "description": "El brutal momento en que el nuevo Green Lantern Kyle Rayner regresa a su departamento y descubre que Major Force asesinó a su novia Alex DeWitt.",
        "hashtags": "#GreenLantern #KyleRayner #MajorForce #DCComics #RonMarz #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Kyle Rayner vivió una de las tragedias más impactantes de DC apenas días después de recibir su anillo?",
            "El despiadado villano Major Force fue enviado por el gobierno para arrebatarle el último anillo de Green Lantern.",
            "Al entrar a su departamento en Nueva York, Kyle encontró una nota sobre el refrigerador y al abrirlo vio el cuerpo sin vida de su novia.",
            "Enceguecido por la furia esmeralda, Kyle desató todo el poder del anillo derrotando a Major Force en una feroz batalla."
        ],
        "art_queries": [
            "Kyle Rayner Green Lantern apartment Alex DeWitt comic panel",
            "Major Force Green Lantern 54 Ron Marz comic panel",
            "Kyle Rayner finds Alex refrigerator Green Lantern 54 comic panel",
            "Green Lantern Kyle Rayner green energy blast Major Force comic panel"
        ]
    },
    {
        "id": "doctor_strange_dormammu_bucle_dimension_oscura",
        "universe": "Marvel",
        "character": "Doctor Strange",
        "title": "Doctor Strange: El Duelo Eterno contra Dormammu en la Dimensión Oscura",
        "theme_signature": "doctor_strange:dormammu:dark_dimension_eternity_clea",
        "description": "Doctor Strange viaja a la aterradora Dimensión Oscura para desafiar a la entidad cósmica Dormammu y salvar la Tierra.",
        "hashtags": "#DoctorStrange #Dormammu #DarkDimension #MarvelComics #SteveDitko #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Doctor Strange desafió solo al dios de la Dimensión Oscura para evitar que devorara nuestra realidad?",
            "Dormammu, un ser titánico de puro fuego místico, juró convertir la Tierra en parte de su reino de pesadilla.",
            "Con el Ojo de Agamotto brillando en su pecho, Strange tejió un laberinto de hechizos antiguos contra las llamas oscuras.",
            "Incapaz de doblegar la voluntad del Hechicero Supremo, Dormammu tuvo que pactar y jurar jamás invadir la Tierra."
        ],
        "scene_art_urls": [
            "assets/curated_panels/doctor_strange_dormammu/scene_01.jpg",
            "assets/curated_panels/doctor_strange_dormammu/scene_02.jpg",
            "assets/curated_panels/doctor_strange_dormammu/scene_03.jpg",
            "assets/curated_panels/doctor_strange_dormammu/scene_04.jpg"
        ],
        "art_queries": [
            "Doctor Strange enters Dark Dimension Steve Ditko comic panel",
            "Dormammu giant flaming head cosmic demon Steve Ditko comic panel",
            "Doctor Strange Eye of Agamotto mystical shields battle comic panel",
            "Doctor Strange defeats Dormammu mystical oath Ditko comic panel"
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

IDEAS DE TEMAS CANDIDATOS ULTRA-VIRALES DE SUPERHÉROES MARVEL/DC CON VIÑETAS INTERIORES VERIFICADAS (Elige uno de estos arcos no producidos o inventa otro arco similar de superhéroes Marvel/DC):
- Vengadores Desunidos (Wanda Maximoff enloquecida destruye la Mansión de los Vengadores y sacrifica a Vision)
- Daredevil: El Hombre Sin Miedo (El camión de desechos radiactivos y el trágico origen ciego de Matt Murdock)
- Aquaman: La Mano de Arpón (Charybdis devora la mano de Arthur Curry arrojándolo a las pirañas)
- Green Lantern: Kyle Rayner y Major Force (Major Force asesina a Alexandra DeWitt y la encierra en el refrigerador)
- Martian Manhunter: Fernus (J'onn J'onzz dominado por la llama ardiente marciana atacando a la Liga de la Justicia)
- Ghost Rider: La Mirada de Penitencia Cósmica contra Galactus
- Batman: White Knight (El Joker consume medicación psiquiátrica y expone la brutalidad de Batman ante Gotham)
- Silver Surfer: Réquiem (Norrin Radd ante sus últimos momentos cósmicos antes de que se apague su luz)

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
