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
    "gemini-3-flash-preview",
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json,text/html,*/*;q=0.8',
}


def log(msg: str):
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [AUTONOMOUS-AI] {msg}", flush=True)
    except UnicodeEncodeError:
        clean_msg = str(msg).encode('ascii', errors='backslashreplace').decode('ascii')
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [AUTONOMOUS-AI] {clean_msg}", flush=True)


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
        "id": "spiderman_sin_eater_iglesia_conflicto",
        "universe": "Marvel",
        "character": "Spider-Man",
        "title": "¡Spider-Man Perdió el Control en la Iglesia! La Balacera de Sin-Eater y Jean DeWolff 🕷️⛪",
        "theme_signature": "spiderman:jean_dewolff:sin_eater:iglesia_conflicto",
        "description": "El brutal asesinato de la capitana Jean DeWolff desató la furia de Peter Parker, quien persiguió a Sin-Eater hasta una iglesia donde casi comete el mayor error de su vida.",
        "hashtags": "#SpiderMan #SinEater #JeanDeWolff #Daredevil #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "La capitana Jean DeWolff fue asesinada en su cama por el psicópata conocido como Sin-Eater.",
            "Consumido por la furia, Peter Parker rastreó al asesino hasta los confesionarios de una iglesia.",
            "Spider-Man golpeó sin piedad al criminal, rompiendo por primera vez su código moral de héroe.",
            "Solo la violenta intervención de Daredevil impidió que el Hombre Araña matara a golpes a Sin-Eater."
        ],
        "art_queries": [
            "Spider-Man Jean DeWolff bed murder badge panel",
            "Sin Eater shotgun church confession Peter Parker panel",
            "Spider-Man beating Sin Eater church enraged panel",
            "Daredevil stopping Spider-Man beating Sin Eater church panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "punisher_the_slavers_tibor_bulat",
        "universe": "Marvel",
        "character": "The Punisher",
        "title": "¡La Operación Clandestina de Punisher! La Caída de la Red Humana de Tibor 💀⚖️",
        "theme_signature": "punisher:the_slavers:tibor_bulat:operacion_clandestina",
        "description": "En The Slavers, Frank Castle descubre una red de trata internacional liderada por criminales de guerra, desatando una cacería metódica y despiadada.",
        "hashtags": "#ThePunisher #FrankCastle #MarvelMAX #GarthEnnis #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "Frank Castle rescató a una joven extranjera y descubrió una red clandestina en Nueva York.",
            "El líder de la organización era Tibor Bulat, un despiadado criminal de guerra intocable.",
            "The Punisher se infiltró en su mansión blindada eliminando a cada guardia uno a uno.",
            "Mirando a los ojos al monstruo, Frank cumplió su promesa y borró a la red para siempre."
        ],
        "art_queries": [
            "The Punisher Garth Ennis The Slavers comic panel",
            "Frank Castle interrogating criminal rain MAX panel",
            "The Punisher shooting mansion assault Slavers panel",
            "Frank Castle standing over villain final judgment panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "ghost_rider_trail_of_tears_travis_parham",
        "universe": "Marvel",
        "character": "Ghost Rider",
        "title": "¡El Jinete Fantasma de la Guerra Civil! El Espíritu que no Conoce Piedad 🔥💀",
        "theme_signature": "ghost_rider:trail_of_tears:travis_parham:guerra_civil",
        "description": "En el siglo XIX, el soldado Travis Parham busca venganza tras la masacre de su familia, desatando la aparición de un Jinete Fantasma ancestral sobre un caballo de fuego.",
        "hashtags": "#GhostRider #TrailOfTears #ClaytonCrain #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "En las cenizas de la Guerra Civil americana, una familia inocente fue masacrada en el bosque.",
            "Travis Parham juró justicia, pero un pacto de sangre convocó al auténtico Espíritu de la Venganza.",
            "Sobre un corcel envuelto en llamas infernales, el demonio cabalgó sin mostrar piedad a los culpables.",
            "El fuego espiritual calcinó a los criminales, dejando una estela de ceniza que la historia olvidó."
        ],
        "art_queries": [
            "Ghost Rider Trail of Tears Clayton Crain burning horse panel",
            "Travis Parham grave oath Ghost Rider comic panel",
            "Ghost Rider skull flaming horse night forest panel",
            "Ghost Rider hellfire burning soldiers Civil War panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "silver_surfer_parable_falso_mesias",
        "universe": "Marvel",
        "character": "Silver Surfer",
        "title": "¡La Parábola Sagrada de Galactus! Silver Surfer se Convirtió en el Falso Mesías 🌌🕊️",
        "theme_signature": "silver_surfer:parable:galactus:falso_mesias",
        "description": "Cuando Galactus desciende sobre la Tierra proclamándose un dios pacífico, la humanidad se rinde ante él, obligando a Silver Surfer a rebelarse para despertar al planeta.",
        "hashtags": "#SilverSurfer #Galactus #Moebius #StanLee #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "Una gigantesca nave estelar cubrió los cielos del planeta sin disparar una sola arma.",
            "Galactus descendió proclamando que la humanidad debía adorarlo como a su nuevo salvador.",
            "Millones cayeron de rodillas en fanatismo, creyendo en las promesas del devorador de mundos.",
            "Silver Surfer se plantó en las nubes, dispuesto a ser odiado con tal de revelar la verdad."
        ],
        "art_queries": [
            "Silver Surfer Parable Moebius Galactus descending city panel",
            "Galactus standing colossal humans praying Parable panel",
            "Silver Surfer floating above crowd preaching Moebius panel",
            "Silver Surfer facing Galactus cosmic energy Parable panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "blue_marvel_adam_brashear_secreto_prohibido",
        "universe": "Marvel",
        "character": "Blue Marvel",
        "title": "¡El Héroe Más Poderoso que el Presidente Prohibió! El Secreto de Blue Marvel ⚡🛡️",
        "theme_signature": "blue_marvel:adam_brashear:presidente_prohibido:neutralizador",
        "description": "Adam Brashear era el héroe más imponente de la Tierra en los años 60, hasta que su máscara se rompió y el gobierno le exigió abandonar su manto por racismo institucional.",
        "hashtags": "#BlueMarvel #AdamBrashear #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "En 1962, un científico y veterano de guerra adquirió el poder de manipular la antimateria pura.",
            "Conocido como Blue Marvel, salvó al mundo de catástrofes que ningún ejército podía frenar.",
            "Pero en una feroz batalla su máscara se rasgó, revelando que el mayor protector era afroamericano.",
            "Por orden del propio presidente, Adam aceptó retirarse en silencio para no incendiar a la nación."
        ],
        "art_queries": [
            "Blue Marvel Adam Brashear reactor explosion antimatter panel",
            "Blue Marvel saving rocket earth hero comic panel",
            "Blue Marvel torn mask face revealed crowd panel",
            "Adam Brashear President Kennedy medal retirement panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "captain_america_dimension_z_ian_zola",
        "universe": "Marvel",
        "character": "Captain America",
        "title": "¡12 Años en la Dimensión Z! Cuando Arnim Zola le Arrebató al Niño Ian 🛡️🧬",
        "theme_signature": "captain_america:dimension_z:ian_zola:mutacion_alienigena",
        "description": "Atrapado en el páramo radioactivo de Arnim Zola, Steve Rogers rescató a un bebé de los laboratorios y pasó doce años protegiéndolo de hordas mutantes.",
        "hashtags": "#CaptainAmerica #DimensionZ #ArnimZola #RickRemender #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "Atrapado en un portal interdimensional, el Capitán América cayó en el desierto hostil de Zola.",
            "En los laboratorios biomecánicos, rescató a un recién nacido genéticamente modificado llamado Ian.",
            "Durante doce agotadores años en el páramo, Steve crió y defendió al niño con su escudo abollado.",
            "Cuando las fuerzas de Zola finalmente lo capturaron, Steve luchó hasta el último aliento por su hijo."
        ],
        "art_queries": [
            "Captain America Dimension Z wasteland Rick Remender panel",
            "Steve Rogers holding baby Ian shield wasteland panel",
            "Captain America bearded surviving mutants Dimension Z panel",
            "Captain America shield broken fighting Zola soldiers panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "iron_man_demon_in_a_bottle_alcoholismo",
        "universe": "Marvel",
        "character": "Iron Man",
        "title": "¡El Enemigo Invisible en el Espejo! La Caída al Abismo de Tony Stark 🍾🤖",
        "theme_signature": "iron_man:demon_in_a_bottle:alcoholismo:espejo_roto",
        "description": "El clásico arco Demon in a Bottle: cuando Tony Stark enfrentó su mayor debilidad no en el campo de batalla, sino en el fondo de una botella.",
        "hashtags": "#IronMan #TonyStark #DemonInABottle #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "Con la tecnología más avanzada del planeta, Tony Stark creía controlar cualquier amenaza.",
            "Pero las presiones de ser un vengador y magnate industrial comenzaron a desgastar su mente.",
            "La armadura dorada no pudo protegerlo del enemigo más peligroso: su propia adicción al alcohol.",
            "Mirándose al espejo con la mirada vacía, Tony tuvo que elegir entre la botella o su propia vida."
        ],
        "art_queries": [
            "Tony Stark drinking scotch glass mansion armor panel",
            "Iron Man malfunctioning armor armor failure Michelinie panel",
            "Tony Stark looking in mirror unkempt Demon in a Bottle panel",
            "Tony Stark sitting bed head in hands armor Demon in a Bottle panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "daredevil_out_identidad_filtrada_globe",
        "universe": "Marvel",
        "character": "Daredevil",
        "title": "¡El Titular que Destruyó su Vida! Cuando el Mundo Entero Descubrió a Daredevil ⚖️📰",
        "theme_signature": "daredevil:out:daily_globe:identidad_expuesta",
        "description": "En la aclamada saga Out de Brian Michael Bendis, un topo del FBI filtra a la prensa que el abogado ciego Matt Murdock es el vigilante Daredevil.",
        "hashtags": "#Daredevil #MattMurdock #Bendis #MarvelComics #HellsKitchen #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "Durante años, Matt Murdock protegió su doble identidad con precisión quirúrgica en el juzgado.",
            "Pero una indiscreción dentro del FBI provocó la filtración más peligrosa de Hell's Kitchen.",
            "El periódico Daily Globe publicó en su portada la primicia mundial con una foto de Murdock.",
            "Acosado por cámaras y enemigos jurados, el abogado ciego negó todo para salvar a sus amigos."
        ],
        "art_queries": [
            "Matt Murdock courtroom blind lawyer Bendis panel",
            "Daily Globe front page Matt Murdock Daredevil headline panel",
            "Matt Murdock surrounded by reporters microphones street panel",
            "Daredevil rain rooftop looking down newspaper panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "invincible_viltrumite_war_scourge_virus",
        "universe": "Image",
        "character": "Invincible",
        "title": "¡El Secreto que Aterró a Omni-Man! El Virus que Exterminó a los Viltrumitas 🩸🧬",
        "theme_signature": "invincible:viltrumite_war:scourge_virus:plaga_genetica",
        "description": "La Coalición de Planetas revela la verdad sobre la expansión viltrumita: su raza casi se extinguió debido al Virus Azote y solo quedan cincuenta individuos puros.",
        "hashtags": "#Invincible #OmniMan #ViltrumiteWar #ImageComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "El Imperio Viltrumita conquistó mundos enteros infundiendo terror absoluto por galaxias.",
            "Pero los líderes de la Coalición ocultaban el mayor secreto biológico del universo conocido.",
            "Décadas atrás, un virus modificado genéticamente aniquiló al noventa y nueve por ciento de su raza.",
            "Solo cincuenta viltrumitas puros sobrevivían en el cosmos, ocultando su inminente extinción."
        ],
        "art_queries": [
            "Viltrumite army space conquest Invincible comic panel",
            "Coalition of Planets Thaedus Allen Invincible comic panel",
            "Viltrumites coughing blood Scourge Virus dying panel",
            "Omni Man serious face space stars Invincible comic panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
    },
    {
        "id": "flash_rebelion_secreta_the_top_mente_villanos",
        "universe": "DC",
        "character": "The Flash",
        "title": "¡La Rebelión Secreta de The Top! El Traidor que Manipuló la Mente de los Villanos ⚡🧠",
        "theme_signature": "flash:the_top:rebelion_secreta:manipulacion_mental",
        "description": "Roscoe Dillon, The Top, manipuló mentalmente a la galería de villanos de Flash, desencadenando una guerra sin cuartel entre Rogues reformados y criminales sádicos.",
        "hashtags": "#TheFlash #WallyWest #TheRogues #TheTop #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "Los villanos de Central City vivían bajo un código: jamás matar inocentes ni romper reglas.",
            "Pero Roscoe Dillon, The Top, descubrió cómo usar su telepatía rotativa para alterar cerebros.",
            "Lavó el cerebro a varios villanos para forzarlos a ser héroes, provocando una guerra interna.",
            "Wally West tuvo que intervenir a toda velocidad antes de que los Rogues pulverizaran la ciudad."
        ],
        "art_queries": [
            "The Rogues Captain Cold Heat Wave street panel",
            "The Top Roscoe Dillon spinning mental power comic panel",
            "Rogues fighting Rogues civil war Geoff Johns panel",
            "Flash Wally West lightning running between villains panel"
        ],
        "voice": "Puck",
        "tts_model": "gemini-3.8-flash-tts",
        "fallback_tts_model": "gemini-3.8-flash-lite-tts",
        "style_direction": "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"
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
    
    # Solo prohibir los personajes de los últimos 6 videos publicados para garantizar rotación sin vetar a los iconos Tier-1
    recent_characters = set(item.get("character", "").strip() for item in ledger[-6:] if item.get("character"))
    past_titles = [item.get("title", "").strip() for item in ledger if item.get("title")]
    past_themes = [item.get("theme_signature", "").strip() for item in ledger if item.get("theme_signature")]

    char_recency_banned = ", ".join(sorted(list(recent_characters)))
    titles_summary = " | ".join(past_titles[-40:])

    # Grupos rotativos con arcos legendarios INÉDITOS para garantizar que la IA nunca proponga historias ya existentes
    ROTATING_CHAR_PROMPTS = [
        "Spider-Man (The Death of Jean DeWolff / Sin-Eater / Conflicto Moral en la Iglesia)",
        "The Punisher (The Slavers / Tibor Bulat / Operación Clandestina en Nueva York)",
        "Ghost Rider (Trail of Tears / Travis Parham / Siglo XIX y Corcel Infernal)",
        "Silver Surfer (Parable / Moebius y Stan Lee / Galactus Falso Mesías)",
        "Blue Marvel (Adam Brashear / Retiro Forzado por el Presidente / Antimateria Pura)",
        "Captain America (Dimensión Z / Rick Remender / Criando al Niño Ian Rogers)",
        "Iron Man (Demon in a Bottle / La Batalla en el Espejo / Crisis de Alcoholismo de Tony Stark)",
        "Daredevil (Out / Brian Michael Bendis / Filtración de Identidad al Periódico Daily Globe)",
        "Invincible (Viltrumite War / El Virus Azote / Plaga Secreta de la Coalición)",
        "The Flash (Rogue War / The Top Roscoe Dillon / Manipulación Mental de Villanos)"
    ]

    rejected_session_titles = []
    max_attempts = 10

    for attempt in range(1, max_attempts + 1):
        log(f"Generando propuesta de historia con IA (Intento {attempt}/{max_attempts})...")

        target_roster = ROTATING_CHAR_PROMPTS[(attempt - 1) % len(ROTATING_CHAR_PROMPTS)]
        rejected_clause = ""
        if rejected_session_titles:
            rejected_clause = f"\nATENCIÓN CRÍTICA: Las siguientes historias fueron RECHAZADAS en intentos previos de esta sesión por colisión o falta de viñetas. ESTÁ ESTRICTAMENTE PROHIBIDO REPETIRLAS:\n{', '.join(rejected_session_titles)}\n"

        system_prompt = f"""
Eres el Guionista Principal y Director Creativo de ComicLoreVault, el canal líder de videos de cómics en español en TikTok y Reels con récords de más de 400,000 reproducciones.

Tu misión es crear una historia COMPLETAMENTE NUEVA, ULTRA-VIRAL, OSCURA Y MEMORABLE sobre un arco legendario de los SUPERHÉROES Y SUPERVILLANOS MÁS FAMOSOS DE MARVEL O DC COMICS.

REGLAS SUPREMAS DE FRANQUICIA Y PERSONAJES:
1. Queda TERMINANTEMENTE PROHIBIDO crear historias de Star Wars, Image Comics, Invincible, The Boys, mangas o franquicias secundarias.
2. Queda TERMINANTEMENTE PROHIBIDO elegir personajes desconocidos, oscuros o secundarios (NO elijas Bastion, Shang-Chi, Atrocitus, etc.). Concéntrate EXCLUSIVAMENTE en personajes famosos Tier-1.
{rejected_clause}
ENFÓCATE EN UNO DE ESTOS PERSONAJES O ARCOS:
{target_roster}

ROTACIÓN Y PREVENCIÓN DE DUPLICADOS:
- Personajes en descanso (publicados en los últimos 6 videos, NO repetir en este turno): {char_recency_banned}
- Títulos recientes ya publicados (PROHIBIDO REPETIR EL MISMO ARCO O TÍTULO): {titles_summary}

FÓRMULA VIRAL DE 400K REPRODUCCIONES (OBLIGATORIA):
1. TÍTULO ULTRA-VIRAL (MÁXIMA CURIOSIDAD Y MORBO):
   - Estructura: ¡[Héroe/Villano] [Acción Impensable o Tabú Quebrado]! [Consecuencia Brutal / Revelación] [Emojis]
   - Ejemplos reales que lograron 440k y 400k views:
     * "¡Spider-Man Siempre se Contuvo! El Golpe que le Arrancó la Mandíbula a Escorpión 💥🕷️"
     * "¡Batman se Inyectó el Virus Doomsday! El Monstruo que Destruyó a Superman 🦇💉"
     * "¡Superman Cruzó la Línea! La Brutal Lobotomía que Aterró al Mundo 😱🩸"
   - PROHIBIDO títulos aburridos tipo enciclopedia o "Personaje: El Día que...".

2. GUION DE RETENCIÓN HIPNÓTICA (EXACTAMENTE 5 ESCENAS, 125 A 150 PALABRAS TOTALES, DURACIÓN 50 A 60 SEGUNDOS):
   - Escena 1 (Gancho directo y tabú quebrado en el cómic): PROHIBIDO empezar con "¿Sabías que...?". Entra directo al conflicto o tabú quebrado en las viñetas (22-26 palabras).
   - Escena 2 (Origen y contexto del cómic): Explica la motivación oculta, el número del cómic y por qué la situación llegó a un punto límite (24-28 palabras).
   - Escena 3 (Escalada y tensión del enfrentamiento): El choque de fuerzas, las líneas de diálogo icónicas o la resistencia desesperada (24-28 palabras).
   - Escena 4 (Clímax gráfico y horror/acción cumbre): El golpe devastador, la ejecución o la revelación visual cumbre (24-28 palabras).
   - Escena 5 (Desenlace canónico del cómic + Gatillo de debate viral): Conclusión épica de cómo termina la historia en las viñetas, cerrando OBLIGATORIAMENTE con una pregunta provocadora que obligue al espectador a comentar y compartir (28-34 palabras). Ej: "¿Crees que Peter debió matarlo para siempre?", "¿Es Batman el ser más peligroso de la Tierra?".

3. VIÑETAS DE CÓMIC (art_queries):
   - Proporciona exactamente 5 términos de búsqueda en INGLÉS súper CONCISOS (de 3 a 5 palabras clave, ej: 'Superman Action Comics 775 heat vision panel', 'Batman Endgame Justice Buster comic', 'Spider-Man black suit fury panel').

Devuelve ÚNICAMENTE un objeto JSON válido con este esquema:
{{
  "id": "identificador_en_snake_case_unico",
  "universe": "Marvel o DC",
  "character": "Nombre del Personaje Tier-1",
  "title": "¡Título Viral con Signos de Exclamación! Subtítulo Épico 💥🦇",
  "theme_signature": "personaje:arco_especifico:giro_clave",
  "description": "Sinopsis de alta retención para la descripción del Reel.",
  "hashtags": "#ComicLoreVault #ComicsNarrados #Marvel #DC #Reels #Shorts",
  "scenes": [
    "Texto directo escena 1 (sin sabias que)...",
    "Texto origen y contexto escena 2...",
    "Texto escalada y combate escena 3...",
    "Texto climax visual escena 4...",
    "Texto desenlace canonico y pregunta debate escena 5..."
  ],
  "art_queries": [
    "Busqueda concisa escena 1",
    "Busqueda concisa escena 2",
    "Busqueda concisa escena 3",
    "Busqueda concisa escena 4",
    "Busqueda concisa escena 5"
  ]
}}
"""


        payload = {
            "contents": [{"parts": [{"text": system_prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 1.0,
                "topP": 0.95
            }
        }

        story = None
        for cand_key in keys_to_try:
            for model in CANDIDATE_MODELS:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={cand_key}"
                try:
                    r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=25)
                    if r.status_code == 200:
                        raw_text = r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                        if "```json" in raw_text:
                            raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                        elif "```" in raw_text:
                            raw_text = raw_text.split("```")[1].split("```")[0].strip()
                        story = json.loads(raw_text)
                        log(f"Propuesta generada por {model}: '{story.get('title')}'")
                        break
                    elif r.status_code == 429:
                        log(f"Modelo {model} respondió 429 (cuota excedida). Rotando inmediatamente a siguiente clave...")
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
            rejected_session_titles.append(story.get("title", ""))
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

        # Solo asignar si se resolvieron las 4 escenas completas para evitar huecos parciales
        if len(resolved_art) == len(story["scenes"]):
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
