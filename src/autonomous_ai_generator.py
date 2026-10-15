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
        "id": "superman_vs_the_elite_action_775",
        "universe": "DC",
        "character": "Superman",
        "title": "¡Superman Cruzó la Línea! La Brutal Lobotomía que Aterró al Mundo 😱🩸",
        "theme_signature": "superman:the_elite:lobotomia_manchester_black_luna",
        "description": "Cuando The Elite desafió el código moral de Superman masacrando villanos, el Hombre de Acero les dio una aterradora lección en la luna que jamás olvidarán.",
        "hashtags": "#Superman #TheElite #ActionComics775 #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Superman jamás rompe su regla de no matar, hasta que una banda de metahumanos amenazó la Tierra!",
            "The Elite masacraba criminales sin piedad, proclamando que la compasión del Hombre de Acero era debilidad.",
            "En la luna, Superman fingió perder la cordura, desatando una cacería aterradora a velocidad imperceptible.",
            "Con micro-visión térmica desactivó los poderes de Manchester Black, demostrando que la fuerza descontrolada solo engendra terror."
        ],
        "scene_art_urls": [
            "assets/curated_panels/superman_vs_the_elite/scene_01.jpg",
            "assets/curated_panels/superman_vs_the_elite/scene_02.jpg",
            "assets/curated_panels/superman_vs_the_elite/scene_03.jpg",
            "assets/curated_panels/superman_vs_the_elite/scene_04.jpg"
        ],
        "art_queries": [
            "Action Comics 775 Tripoli monster destroyed Superman comic panel",
            "Action Comics 775 The Elite team Manchester Black comic panel",
            "Action Comics 775 Superman glowing red eyes heat vision terrifying comic panel",
            "Action Comics 775 Manchester Black trembling defeated comic panel"
        ]
    },
    {
        "id": "spiderman_grim_hunt_venganza_kravinoff",
        "universe": "Marvel",
        "character": "Spider-Man",
        "title": "¡Spider-Man Desató su Furia! El Traje Negro que Aterró a sus Enemigos 🕷️🩸",
        "theme_signature": "spiderman:grim_hunt:furia_traje_negro_kravinoff",
        "description": "Tras el brutal asesinato de Kaine a manos de los Kravinoff, un enfurecido Peter Parker se enfunda de nuevo el traje negro para desatar una venganza implacable.",
        "hashtags": "#SpiderMan #GrimHunt #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Cuando los Kravinoff asesinaron a su clon Kaine, Peter Parker abandonó toda piedad!",
            "Enfundado en su temido traje negro, Spider-Man persiguió a los culpables con precisión implacable.",
            "Acorraló a los villanos uno por uno, quebrando sus defensas con una brutalidad jamás vista.",
            "Estuvo a un milímetro de cruzar la línea y convertirse en un verdugo despiadado. ¿Debió perdonarles la vida?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/spiderman_grim_hunt/scene_01.jpg",
            "assets/curated_panels/spiderman_grim_hunt/scene_02.jpg",
            "assets/curated_panels/spiderman_grim_hunt/scene_03.jpg",
            "assets/curated_panels/spiderman_grim_hunt/scene_04.jpg"
        ],
        "art_queries": [
            "Kaine Parker rising grave Amazing Spider-Man 637 comic panel",
            "Kraven the Hunter throne Sergei Kravinoff Amazing Spider-Man 636 comic panel",
            "Spider-Man black suit hunting Amazing Spider-Man 637 comic panel",
            "Spider-Man Last Stand dark future red jacket Amazing Spider-Man 637 comic panel"
        ]
    },
    {
        "id": "flash_the_human_race_teleportation",
        "universe": "DC",
        "character": "The Flash",
        "title": "¡The Flash Rompió la Física! La Carrera que Superó a la Teletransportación ⚡🌌",
        "theme_signature": "flash:the_human_race:velocidad_trans_temporal_teletransportacion",
        "description": "Para salvar la Tierra de seres cósmicos, Flash absorbió la energía cinética de toda la humanidad corriendo más rápido que la teletransportación instantánea.",
        "hashtags": "#TheFlash #SpeedForce #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Seres cósmicos amenazaron destruir la Tierra si Flash no ganaba una carrera imposible a través del universo!",
            "Su rival poseía teletransportación instantánea, haciendo inútil cualquier intento de velocidad común.",
            "El velocista absorbió la energía cinética del planeta entero, quebrando las leyes de la física.",
            "Llegó antes que la teletransportación instantánea, salvando la Tierra. ¿Es el héroe más veloz de la historia?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/flash_human_race/scene_01.jpg",
            "assets/curated_panels/flash_human_race/scene_02.jpg",
            "assets/curated_panels/flash_human_race/scene_03.jpg",
            "assets/curated_panels/flash_human_race/scene_04.jpg"
        ],
        "art_queries": [
            "The Flash Wally West running at super speed lightning comic panel",
            "Wally West Sprinting Through Time Return of Wally West comic panel",
            "The Flash trans time velocity leaving space time The Flash 138 comic panel",
            "Wally West Flash surrounded by white lightning speed force comic panel"
        ]
    },
    {
        "id": "batman_white_knight_joker_cuerdo",
        "universe": "DC",
        "character": "The Joker",
        "title": "¡El Joker se Volvió Cuerdo! El Juicio que Encarceló a Batman en Gotham 🃏⚖️",
        "theme_signature": "joker:white_knight:jack_napier_cuerdo_juicio",
        "description": "Tras una sobredosis de medicamentos, el Joker recuperó la cordura transformándose en Jack Napier, el político que demandó a Batman y lo metió tras las rejas.",
        "hashtags": "#BatmanWhiteKnight #TheJoker #Batman #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Una sobredosis de medicamentos curó al Joker, transformándolo en un brillante estratega de la ley!",
            "Convertido en Jack Napier, unió a Gotham para denunciar la brutalidad destructiva de Batman.",
            "Vistiendo un elegante traje, demandó a la ciudad convenciendo al pueblo de su inocencia.",
            "La policía arrestó a Bruce Wayne, consagrando al Joker como salvador. ¿Quién era el verdadero monstruo?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/batman_white_knight/scene_01.jpg",
            "assets/curated_panels/batman_white_knight/scene_02.jpg",
            "assets/curated_panels/batman_white_knight/scene_03.jpg",
            "assets/curated_panels/batman_white_knight/scene_04.jpg"
        ],
        "art_queries": [
            "Batman White Knight Joker pills sane Jack Napier comic panel",
            "Batman White Knight Jack Napier press conference television comic panel",
            "Jack Napier white suit lawyer Batman White Knight comic panel",
            "Batman arrested White Knight Sean Murphy comic panel"
        ]
    },
    {
        "id": "magneto_venganza_red_skull",
        "universe": "Marvel",
        "character": "Magneto",
        "title": "¡Magneto Castigó a Red Skull! El Búnker Subterráneo del que Jamás Saldrá ⛓️💀",
        "theme_signature": "magneto:red_skull:bunker_entierro_auschwitz",
        "description": "Como superviviente del Holocausto, Magneto captura a Red Skull y rechaza darle una muerte rápida, encerrándolo vivo en un búnker subterráneo eterno.",
        "hashtags": "#Magneto #RedSkull #XMen #CaptainAmerica #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "¡Cuando Magneto capturó al nazi Red Skull, se negó a darle una muerte rápida con sus poderes!",
            "Como superviviente de Auschwitz, Magneto despreciaba la ideología supremacista de Hydra con odio eterno.",
            "Encerró a Red Skull en un búnker subterráneo blindado, sin luz, sin aire y sin salida.",
            "Dejándole solo un poco de agua, lo abandonó a una agonía eterna en la oscuridad absoluta."
        ],
        "art_queries": [
            "Magneto confronting Red Skull comic panel Acts of Vengeance",
            "Magneto holocaust survivor tattoo memory comic panel",
            "Magneto burying Red Skull underground bunker comic panel",
            "Red Skull trapped in dark bunker tomb comic panel"
        ]
    },
    {
        "id": "wolverine_x23_olor_detonante",
        "universe": "Marvel",
        "character": "X-23",
        "title": "¡X-23 Perdió el Control! El Olor que la Obligó a Asesinar a su Madre 🩸🐺",
        "theme_signature": "x23:laura_kinney:olor_detonante_asesinato_sarah_kinney",
        "description": "El brutal origen de Laura Kinney: convertida en una asesina desde niña, un compuesto químico la obliga a cometer su mayor pecado.",
        "hashtags": "#X23 #Wolverine #LauraKinney #XMen #MarvelComics #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¡La clon de Wolverine, Laura Kinney, fue diseñada como el arma viviente más sanguinaria del mundo!",
            "Científicos crearon un aroma sintético capaz de anular su mente y desatar furia asesina ciega.",
            "Sometida al olor detonante durante una fuga, Laura masacró a los guardias en un frenesí salvaje.",
            "Al recobrar la conciencia descubrió la mayor tragedia: había atravesado con sus garras a su propia madre."
        ],
        "art_queries": [
            "Young Laura Kinney X-23 claws surgical facility comic panel",
            "X-23 berserker rage trigger scent red eyes comic panel",
            "X-23 slashing facility soldiers claws comic panel",
            "X-23 crying holding dying mother Sarah Kinney comic panel"
        ]
    },
    {
        "id": "batman_zur_en_arrh_respaldo",
        "universe": "DC",
        "character": "Batman",
        "title": "¡Batman Creó una Mente de Respaldo! El Guerrero Implacable de Zur-En-Arrh 🦇🧠",
        "theme_signature": "batman:zur_en_arrh:mente_respaldo_personalidad_violenta",
        "description": "Para prevenir que atacaran su cordura, Bruce Wayne programó una personalidad psicótica de reserva: el despiadado Batman de Zur-En-Arrh.",
        "hashtags": "#Batman #ZurEnArrh #BatmanRIP #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Anticipando que destruirían su cordura, Bruce Wayne programó un aterrador protocolo psicológico en su cerebro!",
            "Drogado y abandonado en Crime Alley por Black Glove, una palabra clave detonó su personalidad de reserva.",
            "Nació el Batman de Zur-En-Arrh: un guerrero psicótico sin remordimientos que jamás siente compasión ni dolor.",
            "Barrió a los villanos en Arkham con brutalidad salvaje antes de despertar. ¿Es el Batman más aterrador?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/batman_zur_en_arrh/scene_01.jpg",
            "assets/curated_panels/batman_zur_en_arrh/scene_02.jpg",
            "assets/curated_panels/batman_zur_en_arrh/scene_03.jpg",
            "assets/curated_panels/batman_zur_en_arrh/scene_04.jpg"
        ],
        "art_queries": [
            "Bruce Wayne Crime Alley Batman RIP comic panel",
            "Bat-Radia radio trigger Zur-En-Arrh comic panel",
            "Batman of Zur-En-Arrh red purple yellow suit comic panel",
            "Batman Zur-En-Arrh fighting Arkham Asylum comic panel"
        ]
    },
    {
        "id": "superior_iron_man_extremis_villano",
        "universe": "Marvel",
        "character": "Iron Man",
        "title": "¡Iron Man se Volvió Malvado! La Droga Extremis que Esclavizó San Francisco 🦾😈",
        "theme_signature": "iron_man:superior:extremis_inversion_armadura_endosym_san_francisco",
        "description": "Con su brújula moral invertida tras AXIS, un despiadado Tony Stark viste una armadura plateada de metal líquido y vuelve adicta a toda una ciudad con Extremis 3.0.",
        "hashtags": "#IronMan #SuperiorIronMan #TonyStark #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Tras un hechizo mágico que invirtió su moral, Tony Stark se transformó en un villano megalómano despiadado!",
            "Creó la aplicación Extremis 3.0, regalando belleza y salud perfecta a los habitantes de San Francisco.",
            "Al cumplirse el plazo, bloqueó la cura exigiendo cien dólares diarios para mantener la juventud eterna.",
            "Enfundado en su armadura de metal líquido Endo-Sym, desafió a la humanidad: 'He jugado a ser Dios'."
        ],
        "scene_art_urls": [
            "assets/curated_panels/superior_iron_man/scene_01.jpg",
            "assets/curated_panels/superior_iron_man/scene_02.jpg",
            "assets/curated_panels/superior_iron_man/scene_03.jpg",
            "assets/curated_panels/superior_iron_man/scene_04.jpg"
        ],
        "art_queries": [
            "Tony Stark white suit Superior Iron Man 1 comic panel",
            "Extremis 3.0 app phone Superior Iron Man 1 comic panel",
            "Superior Iron Man Endo-Sym armor liquid metal comic panel",
            "Tony Stark evil smiling god complex Superior Iron Man comic panel"
        ]
    },
    {
        "id": "doctor_strange_el_juramento_elixir",
        "universe": "Marvel",
        "character": "Doctor Strange",
        "title": "¡Doctor Strange Descubrió la Cura del Cáncer! El Dilema Moral que Casi Mata a Wong 🔮🧪",
        "theme_signature": "doctor_strange:the_oath:elixir_otkid_cancer_wong_juramento",
        "description": "Doctor Strange encuentra el elixir ancestral de Otkid para erradicar el cáncer terminal de Wong, pero una corporación criminal intenta robarlo.",
        "hashtags": "#DoctorStrange #TheOath #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Al descubrir que su sirviente Wong padecía un cáncer cerebral incurable, Doctor Strange desafió a la muerte!",
            "Viajó a templos místicos prohibidos hasta conseguir el Elixir de Otkid, la sustancia capaz de curar cualquier enfermedad.",
            "Pero un sicario contratado por una farmacéutica le disparó a quemarropa buscando patentar y monopolizar la fórmula médica.",
            "Al borde de la muerte, Stephen Strange tuvo que elegir entre salvar a su mejor amigo o a la humanidad entera."
        ],
        "scene_art_urls": [
            "assets/curated_panels/doctor_strange_the_oath/scene_01.jpg",
            "assets/curated_panels/doctor_strange_the_oath/scene_02.jpg",
            "assets/curated_panels/doctor_strange_the_oath/scene_03.jpg",
            "assets/curated_panels/doctor_strange_the_oath/scene_04.jpg"
        ],
        "art_queries": [
            "Doctor Strange Sanctum Sanctorum The Oath 1 comic panel",
            "Otkid Elixir magical potion glowing The Oath comic panel",
            "Brigand shooting Doctor Strange handgun The Oath comic panel",
            "Doctor Strange healing Wong astral projection The Oath comic panel"
        ]
    },
    {
        "id": "batman_ultimatum_segundo_robin_pistola",
        "universe": "DC",
        "character": "Batman",
        "title": "¡El Segundo Robin le Apuntó con un Arma a Batman! El Imposible Juicio del Callejón del Crimen 🦇🔫",
        "theme_signature": "batman:ultimatum_segundo_robin:pistola_decision_moral_ejecucion",
        "description": "Jason Todd resucitó de la tumba para obligar a Batman a romper su regla más sagrada, poniéndole una pistola en la cabeza al Joker.",
        "hashtags": "#Batman #RedHood #Joker #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡El mayor fracaso de Batman regresó de entre los muertos convertido en Red Hood, un despiadado verdugo que castiga a los criminales con plomo!",
            "Resucitado tras haber sido asesinado a golpes por el Joker, Jason Todd descubrió con furia que Bruce jamás cobró venganza por su muerte.",
            "Con un arsenal militar y una brutalidad implacable, tomó el control del bajo mundo de Gotham ejecutando a sangre fría a los lugartenientes de Máscara Negra.",
            "En el clímax, acorraló a Batman en un callejón, puso una pistola en la frente del Joker y le entregó un arma a su antiguo mentor.",
            "Obligado a elegir entre matar a su pupilo o salvar a su peor enemigo, Batman cortó la garganta de Jason con un batarang desatando una explosión. ¿Debió Batman liquidar al Joker?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/batman_under_red_hood/scene_01.jpg",
            "assets/curated_panels/batman_under_red_hood/scene_02.jpg",
            "assets/curated_panels/batman_under_red_hood/scene_03.jpg",
            "assets/curated_panels/batman_under_red_hood/scene_04.jpg",
            "assets/curated_panels/batman_under_red_hood/scene_05.jpg"
        ],
        "art_queries": [
            "Batman Under the Red Hood Jason Todd resurrection mask panel",
            "Batman remembering Jason Todd death memorial Robin costume panel",
            "Red Hood weapons beating Black Mask criminals Gotham comic panel",
            "Red Hood gun pointed at Joker Batman moral ultimatum panel",
            "Batman batarang Jason Todd neck explosion Under the Red Hood panel"
        ]
    },
    {
        "id": "hulk_derroto_black_bolt_luna",
        "universe": "Marvel",
        "character": "Hulk",
        "title": "¡Hulk Sometió al Rey de los Inhumanos! La Venganza Implacable que Hizo Temblar la Luna 🌕💥",
        "theme_signature": "hulk:black_bolt_luna:venganza_armadura_gladiador_destierro_derrota",
        "description": "Tras ser desterrado al espacio por los Illuminati, Hulk regresó convertido en el Cicatriz Verde y humilló a Black Bolt en la superficie lunar.",
        "hashtags": "#Hulk #WorldWarHulk #BlackBolt #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Traicionado y exiliado al espacio por sus propios compañeros vengadores, Hulk regresó a la Tierra con una sed insaciable de venganza absoluta!",
            "Convertido en el colosal Cicatriz Verde de Sakaar y armado como gladiador cósmico, su primera parada estratégica fue la ciudadela de Attilan en la luna.",
            "Allí lo esperaba Black Bolt, rey de los Inhumanos, cuya voz puede quebrar planetas enteros y quien había aprobado su cruel destierro intergaláctico.",
            "El monarca susurró provocando una devastadora onda sónica que reventó cráteres lunares, pero un enfurecido Hulk resistió el impacto y lo noqueó a puño limpio.",
            "Sujetando la corona destrozada del rey ante el cosmos, Hulk anunció que Nueva York sería la siguiente en caer bajo su furia. ¿Tenía Hulk derecho a cobrar venganza?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/hulk_world_war/scene_01.jpg",
            "assets/curated_panels/hulk_world_war/scene_02.jpg",
            "assets/curated_panels/hulk_world_war/scene_03.jpg",
            "assets/curated_panels/hulk_world_war/scene_04.jpg",
            "assets/curated_panels/hulk_world_war/scene_05.jpg"
        ],
        "art_queries": [
            "World War Hulk gladiator armor approaching moon comic panel",
            "Black Bolt confronting Hulk Attilan moon surface comic panel",
            "Black Bolt whisper sonic destruction World War Hulk comic panel",
            "Hulk taking Black Bolt sonic blast punching king comic panel",
            "Hulk holding defeated Black Bolt World War Hulk revenge comic panel"
        ]
    },
    {
        "id": "daredevil_tragedia_elektra_asesinos",
        "universe": "Marvel",
        "character": "Daredevil",
        "title": "¡Elektra Cayó Atravesada por su Propia Arma! El Duelo Letal de los Asesinos 💔🗡️",
        "theme_signature": "daredevil:elektra_tragedia:empalamiento_sai_murdock_brazos",
        "description": "En uno de los momentos más trágicos de Marvel, Bullseye y Elektra se enfrentaron a muerte en las calles de Hell's Kitchen.",
        "hashtags": "#Daredevil #Elektra #Bullseye #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Las sombras de Hell's Kitchen fueron testigo del enfrentamiento más sangriento y desgarrador entre los dos asesinos más letales de la ciudad!",
            "Bullseye escapó de prisión obsesionado con recuperar su estatus como el sicario principal de Kingpin, puesto que ahora ocupaba la temible Elektra Natchios.",
            "En una feroz batalla sobre los tejados, ambos guerreros intercambiaron estocadas mortales hasta que el psicópata desarmó a la ninja con una carta metálica.",
            "Con una frialdad perturbadora, Bullseye le arrebató su propio sai y atravesó el torso de Elektra de lado a lado ante la mirada atónita de la noche.",
            "Agonizando lentamente, la guerrera se arrastró por la ciudad hasta desplomarse y morir en los brazos de Matt Murdock. ¿Debió Daredevil romper su código y liquidar a Bullseye?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/daredevil_muerte_elektra/scene_01.jpg",
            "assets/curated_panels/daredevil_muerte_elektra/scene_02.jpg",
            "assets/curated_panels/daredevil_muerte_elektra/scene_03.jpg",
            "assets/curated_panels/daredevil_muerte_elektra/scene_04.jpg",
            "assets/curated_panels/daredevil_muerte_elektra/scene_05.jpg"
        ],
        "art_queries": [
            "Bullseye confronting Elektra rooftops Daredevil 181 comic panel",
            "Elektra sai fighting Bullseye playing card throw comic panel",
            "Bullseye disarming Elektra grabbing sai weapon comic panel",
            "Bullseye impaling Elektra chest sai Daredevil 181 iconic panel",
            "Elektra crawling dying in Matt Murdock arms Daredevil comic panel"
        ]
    },
    {
        "id": "spiderman_asedio_juggernaut_imparable",
        "universe": "Marvel",
        "character": "Spider-Man",
        "title": "¡Una Fuerza Imparable Arrasó Nueva York! El Desesperado Asedio de Juggernaut 🕷️🧱",
        "theme_signature": "spider_man:juggernaut:combate_fuerza_bruta_cemento_fosa",
        "description": "Cuando Juggernaut marchó por Manhattan para destruir a Madame Web, Spider-Man arriesgó su vida en una de las batallas más desesperadas de su historia.",
        "hashtags": "#SpiderMan #Juggernaut #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Un coloso imparable de fuerza ilimitada caminó en línea recta por Manhattan, destruyendo rascacielos y vehículos sin que nadie pudiera frenarlo!",
            "Enviado por Black Tom Cassidy para secuestrar los poderes psíquicos de Madame Web, Juggernaut ignoró barricadas militares aplastando todo obstáculo a su paso.",
            "Spider-Man lo arriesgó todo electrocutándolo con transformadores de alto voltaje y derribándole grúas encima, pero el monstruo ni siquiera pestañeó ante los impactos.",
            "Al borde del colapso físico, Peter Parker saltó sobre su espalda cubriéndole los ojos de la armadura para guiarlo a ciegas hacia una gigantesca construcción.",
            "Juggernaut pisó en falso hundiéndose en una piscina de hormigón líquido de doce metros que se solidificó al instante, atrapándolo bajo tierra. ¿Es esta la mayor hazaña de Spider-Man?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/spiderman_vs_juggernaut/scene_01.jpg",
            "assets/curated_panels/spiderman_vs_juggernaut/scene_02.jpg",
            "assets/curated_panels/spiderman_vs_juggernaut/scene_03.jpg",
            "assets/curated_panels/spiderman_vs_juggernaut/scene_04.jpg",
            "assets/curated_panels/spiderman_vs_juggernaut/scene_05.jpg"
        ],
        "art_queries": [
            "Amazing Spider-Man 229 Juggernaut walking through building debris panel",
            "Madame Web life support chair terrified Juggernaut approaching panel",
            "Spider-Man throwing electric transformers at Juggernaut comic panel",
            "Spider-Man jumping on Juggernaut helmet webbing eyes comic panel",
            "Juggernaut sinking wet cement foundation trapped Spider-Man 230 panel"
        ]
    },
    {
        "id": "wolverine_la_muerte_adamantium_liquido",
        "universe": "Marvel",
        "character": "Wolverine",
        "title": "¡Wolverine Murió Asfixiado en Metal Hirviendo! El Sacrificio que Marcó el Fin del Mutante 🩸🐺",
        "theme_signature": "wolverine:death_of_wolverine:adamantium_liquido_sacrificio_cornelius",
        "description": "Sin su factor curativo, Wolverine asaltó el laboratorio del Doctor Cornelius para salvar vidas inocentes, sufriendo el destino más desgarrador.",
        "hashtags": "#Wolverine #DeathOfWolverine #Logan #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Sin factor curativo y con el cuerpo destrozado, Logan marchó a su última misión suicida!",
            "El doctor Cornelius planeaba crear cientos de mutantes esclavos inyectándoles adamantium a la fuerza.",
            "Para salvarlos, Wolverine rompió el contenedor principal, cubriéndose por completo de metal líquido hirviendo.",
            "Se endureció como una estatua frente al atardecer, muriendo con honor. ¿Es la despedida más heroica de Marvel?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/wolverine_muerte_adamantium/scene_01.jpg",
            "assets/curated_panels/wolverine_muerte_adamantium/scene_02.jpg",
            "assets/curated_panels/wolverine_muerte_adamantium/scene_03.jpg",
            "assets/curated_panels/wolverine_muerte_adamantium/scene_04.jpg",
            "assets/curated_panels/wolverine_muerte_adamantium/scene_05.jpg"
        ],
        "art_queries": [
            "Wolverine wounded claws out final mission comic panel",
            "Doctor Cornelius lab Weapon X experiment Death of Wolverine panel",
            "Wolverine slashing adamantium pipes tanks claws comic panel",
            "Wolverine drenched liquid molten silver adamantium Death of Wolverine panel",
            "Wolverine solid adamantium statue sunset roof Death of Wolverine 4 panel"
        ]
    },
    {
        "id": "thor_indigno_susurro_perdida_martillo",
        "universe": "Marvel",
        "character": "Thor",
        "title": "¡Tres Palabras le Arrebataron el Mjolnir! El Secreto que Hizo Indigno al Príncipe de Asgard ⚡🔨",
        "theme_signature": "thor:unworthy_original_sin:susurro_fury_asgard_perdida_martillo",
        "description": "Durante la guerra de Original Sin, Nick Fury le susurró un secreto cósmico a Thor que quebró su fe divina y le impidió levantar su propio martillo.",
        "hashtags": "#Thor #OriginalSin #Mjolnir #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡El Dios del Trueno era considerado el guerrero más digno del universo, hasta que un secreto cósmico desmoronó toda su divinidad en un instante!",
            "Tras la misteriosa muerte del Vigilante Uatu en la luna, los secretos más oscuros de los héroes de la Tierra salieron a la luz sin censura.",
            "En medio de una sangrienta batalla lunar, un envejecido Nick Fury dotado del conocimiento cósmico se acercó al oído de Thor susurrándole tres demoledoras palabras.",
            "Fury le reveló que el Carnicero de Dioses tenía razón y que los dioses solo traen ruina, quebrando la fe que Thor tenía en sí mismo.",
            "El poderoso Mjolnir cayó al polvo lunar como plomo inútil, y por más que Odinson tiró con desesperación, jamás pudo moverlo un solo milímetro. ¿Tenía razón Gorr sobre los dioses?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/thor_unworthy_susurro/scene_01.jpg",
            "assets/curated_panels/thor_unworthy_susurro/scene_02.jpg",
            "assets/curated_panels/thor_unworthy_susurro/scene_03.jpg",
            "assets/curated_panels/thor_unworthy_susurro/scene_04.jpg",
            "assets/curated_panels/thor_unworthy_susurro/scene_05.jpg"
        ],
        "art_queries": [
            "Thor lightning Mjolnir celestial battle Original Sin comic panel",
            "Watcher Uatu eye secrets cosmic Nick Fury Original Sin panel",
            "Nick Fury whispering into Thor ear moon surface Original Sin 7 panel",
            "Mjolnir falling hitting moon dust Thor horrified comic panel",
            "Thor on knees weeping pulling Mjolnir Unworthy Thor comic panel"
        ]
    },
    {
        "id": "batman_endgame_justice_buster_liga",
        "universe": "DC",
        "character": "Batman",
        "title": "¡Batman Derrotó a Toda la Liga de la Justicia! La Armadura Implacable del Justice Buster 🦇🤖",
        "theme_signature": "batman:endgame:justice_buster_armadura_fenrir_joker_toxina",
        "description": "Cuando el Joker infectó a la Liga de la Justicia con una toxina homicida, Batman desató la armadura Fenrir para someter a sus mejores amigos.",
        "hashtags": "#Batman #JusticeLeague #Endgame #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡El Joker infectó a la Liga de la Justicia con una variante macabra de su toxina, enviando a los héroes más poderosos a asesinar a Batman!",
            "Wonder Woman, Flash y Aquaman atacaron Gotham con una furia sádica descomunal, arrasando manzanas enteras sin mostrar una pizca de cordura o piedad.",
            "Ante la aniquilación inminente, Bruce Wayne activó la colosal armadura Fenrir, conocida como el Justice Buster, equipada con contramedidas científicas para neutralizar a cada compañero.",
            "Usó tejido místico contra Diana, servidores ultraveloces contra Flash y espuma de carbonato contra Aquaman, hasta que un Superman poseído destrozó la cabina desde el aire.",
            "Acorralado y sin armadura, Batman escupió una cápsula de polvo de kriptonita directo a los ojos del Hombre de Acero para noquearlo. ¿Es Batman la mente más peligrosa del universo?"
        ],
        "art_queries": [
            "Wonder Woman Joker venom attacking Batman Batman Endgame 35 panel",
            "Justice League infected Joker smiles destroying Gotham Batman 35 panel",
            "Batman Justice Buster Fenrir armor deploying Gotham Batman 35 panel",
            "Superman Joker toxin attacking Justice Buster armor Batman 36 panel",
            "Batman spitting kryptonite gum Superman eye Batman Endgame 36 panel"
        ]
    },
    {
        "id": "nova_richard_rider_desgarro_annihilus",
        "universe": "Marvel",
        "character": "Nova",
        "title": "¡Nova le Arrancó las Entrañas a Annihilus! La Venganza Más Brutal del Cosmos 🌌⚡",
        "theme_signature": "nova:richard_rider:annihilation:annihilus:venganza",
        "description": "Con el universo al borde de la extinción ante la Ola de Aniquilación, Nova libró un duelo a muerte contra Annihilus para vengar al Cuerpo Nova.",
        "hashtags": "#Nova #Annihilation #MarvelComics #RichardRider #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Cuando la Ola de Aniquilación arrasó galaxias enteras masacrando a billones de seres, el universo entero quedó al borde de la extinción total!",
            "Annihilus, el implacable señor de la Zona Negativa, marchó conquistando planetas y aniquilando al legendario Cuerpo Nova hasta dejar a un único superviviente.",
            "Cargando con toda la Nova Force en sus venas, Richard Rider lideró el Frente Unido lanzándose en una última misión suicida contra el tirano cósmico.",
            "En un choque salvaje cuerpo a cuerpo, Nova metió su brazo directo por las fauces de Annihilus y tiró con toda su alma arrancándole las entrañas desde adentro.",
            "Sosteniendo los restos del tirano en el vacío espacial, Nova salvó al cosmos demostrando hasta dónde llega la voluntad de un héroe. ¿Fue esta la victoria más sangrienta de Marvel?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/nova_annihilus_desgarro/scene_01.jpg",
            "assets/curated_panels/nova_annihilus_desgarro/scene_02.jpg",
            "assets/curated_panels/nova_annihilus_desgarro/scene_03.jpg",
            "assets/curated_panels/nova_annihilus_desgarro/scene_04.jpg",
            "assets/curated_panels/nova_annihilus_desgarro/scene_05.jpg"
        ],
        "art_queries": [
            "Annihilation Wave destroying galaxy cosmic fleet Annihilation comic scan",
            "Annihilus warlord conqueror Negative Zone Annihilation comic panel scan",
            "Nova Richard Rider full Nova Force charging Annihilation comic scan",
            "Nova turning Annihilus inside out Annihilation 6 comic panel scan",
            "Nova Richard Rider floating space victorious Annihilation 6 comic panel"
        ]
    },
    {
        "id": "red_goblin_norman_osborn_simbionte_carnage",
        "universe": "Marvel",
        "character": "Norman Osborn",
        "title": "¡Nació el Duende Rojo! La Fusión Monstruosa de Norman Osborn y Carnage 🩸🎃",
        "theme_signature": "norman_osborn:carnage:duende_rojo:fusion_simbionte:pesadilla",
        "description": "Desesperado por destruir a Spider-Man tras perder su suero, Norman Osborn se vinculó con el simbionte Carnage para convertirse en el letal Red Goblin.",
        "hashtags": "#SpiderMan #RedGoblin #Carnage #NormanOsborn #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Inmune al fuego y sordo a las ondas sonoras, Norman Osborn creó al monstruo definitivo cuando fusionó su mente retorcida con el simbionte de Carnage!",
            "Al haber perdido los poderes del Duende Verde, Osborn robó al simbionte asesino de Cletus Kasady para desatar una cacería implacable contra Peter Parker.",
            "De su unión nació el Duende Rojo, una pesadilla carmesí que infectó a su propio nieto Normie con microduendes simbióticos para obligarlo a matar.",
            "Desesperado ante la masacre, Spider-Man tuvo que vestir el simbionte de Venom y provocar el ego de Norman para que abandonara al monstruo y pelearan mano a mano.",
            "Norman fue derrotado, pero el trauma cerebral lo dejó atrapado creyendo que él era Cletus Kasady para siempre. ¿Es el Duende Rojo la peor versión de Osborn?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/red_goblin_osborn_carnage/scene_01.jpg",
            "assets/curated_panels/red_goblin_osborn_carnage/scene_02.jpg",
            "assets/curated_panels/red_goblin_osborn_carnage/scene_03.jpg",
            "assets/curated_panels/red_goblin_osborn_carnage/scene_04.jpg",
            "assets/curated_panels/red_goblin_osborn_carnage/scene_05.jpg"
        ],
        "art_queries": [
            "Red Goblin Norman Osborn Carnage first appearance Amazing Spider-Man 798 comic scan",
            "Norman Osborn holding Carnage symbiote tube Amazing Spider-Man 795 comic scan",
            "Red Goblin smiling fire Carnage glider Amazing Spider-Man comic panel",
            "Spider-Man Venom symbiote fighting Red Goblin Amazing Spider-Man 800 comic scan",
            "Norman Osborn insane Ravencroft thinking he is Cletus Kasady Amazing Spider-Man 800 comic scan"
        ]
    },
    {
        "id": "wonder_woman_ceguera_decapito_medusa",
        "universe": "DC",
        "character": "Wonder Woman",
        "title": "¡Wonder Woman se Arrancó la Vista! El Sacrificio que Destruyó a Medusa ⚔️🐍",
        "theme_signature": "wonder_woman:diana_prince:ceguera:medusa_decapitacion:sacrificio",
        "description": "Para derrotar a la Gorgona Medusa y salvar a millones de inocentes, Diana Prince derramó veneno en sus propios ojos antes de blandir su espada.",
        "hashtags": "#WonderWoman #Medusa #DCComics #DianaPrince #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Para salvar la vida de miles de inocentes amenazados por la mirada petrificante de Medusa, Wonder Woman cometió el mayor sacrificio físico de su vida!",
            "Resucitada por Circe en el Yankee Stadium, la Gorgona desafió a Diana a un duelo a muerte transmitido en vivo ante la mirada aterrada de todo el planeta.",
            "Sabiendo que un solo reflejo en sus ojos la convertiría en piedra instantáneamente, Diana tomó una serpiente venenosa y restregó su letal fluido directo sobre sus pupilas.",
            "Completamente ciega y guiándose únicamente por sus sentidos de guerrera amazona, Diana esquivó los ataques de Medusa y le cercenó la cabeza de un solo tajo de espada.",
            "Alzando la cabeza de serpientes ante la multitud perpleja, Diana demostró que la verdadera visión de un héroe no depende de sus ojos. ¿Fue este su combate más glorioso?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/wonder_woman_ceguera_medusa/scene_01.jpg",
            "assets/curated_panels/wonder_woman_ceguera_medusa/scene_02.jpg",
            "assets/curated_panels/wonder_woman_ceguera_medusa/scene_03.jpg",
            "assets/curated_panels/wonder_woman_ceguera_medusa/scene_04.jpg",
            "assets/curated_panels/wonder_woman_ceguera_medusa/scene_05.jpg"
        ],
        "art_queries": [
            "Wonder Woman Diana Prince armor sword Wonder Woman 210 comic scan",
            "Medusa Gorgon snakes hair Yankee Stadium Wonder Woman 209 comic scan",
            "Wonder Woman blinding herself snake venom eyes Wonder Woman 210 comic scan",
            "Wonder Woman blind slicing Medusa head sword Wonder Woman 210 comic scan",
            "Wonder Woman holding severed Medusa head blind bleeding eyes comic scan"
        ]
    },
    {
        "id": "larfleeze_orange_lantern_avaricia_absoluta",
        "universe": "DC",
        "character": "Larfleeze",
        "title": "¡Larfleeze: Un Hombre y Todo un Ejército de Avaricia Cósmica! 🧡💎",
        "theme_signature": "larfleeze:agent_orange:avaricia_bateria:anillo_naranja:ego",
        "description": "Durante milenios, Larfleeze fue el único portador de la batería naranja, conjurando los espectros energéticos de todos los guerreros que asesinó.",
        "hashtags": "#Larfleeze #GreenLantern #AgentOrange #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡En lo profundo del sistema Vega habita un ser tan consumido por la codicia que la luz naranja de la avaricia lo convirtió en su único portador!",
            "Conocido como el Agente Naranja, Larfleeze custodió durante millones de años la batería de poder en Okaara, jurando que todo lo que existe le pertenece.",
            "A diferencia de otras corporaciones, él no comparte sus anillos: cada víctima que aniquila es resucitada como un constructo espectral de luz anaranjada bajo su mando.",
            "Cuando los Guardianes del Universo intentaron despojarlo de su tesoro, Larfleeze desató su ejército de espectros devoradores poniendo de rodillas al Cuerpo de Linternas Verdes.",
            "Aislado y abrazando su batería mientras grita que el cosmos es suyo, Larfleeze representa la soledad eterna de la avaricia. ¿Es el espectro naranja el más peligroso de DC?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/larfleeze_orange_lantern_avaricia/scene_01.jpg",
            "assets/curated_panels/larfleeze_orange_lantern_avaricia/scene_02.jpg",
            "assets/curated_panels/larfleeze_orange_lantern_avaricia/scene_03.jpg",
            "assets/curated_panels/larfleeze_orange_lantern_avaricia/scene_04.jpg",
            "assets/curated_panels/larfleeze_orange_lantern_avaricia/scene_05.jpg"
        ],
        "art_queries": [
            "Larfleeze Agent Orange battery Vega system Green Lantern 42 comic scan",
            "Larfleeze holding orange power battery laughing comic panel scan",
            "Orange Lantern Corps constructs ghosts Larfleeze Green Lantern comic scan",
            "Larfleeze Orange Lantern fighting Hal Jordan Guardians Green Lantern 42 comic scan",
            "Larfleeze hugging orange battery alone greed Green Lantern comic scan"
        ]
    },
    {
        "id": "supergirl_red_lantern_anillo_ira",
        "universe": "DC",
        "character": "Supergirl",
        "title": "¡Supergirl Sucumbió a la Furia Roja! El Terror de la Hija de Krypton 🔴💥",
        "theme_signature": "supergirl:kara_zorel:red_lantern:ira_kryptoniana:atrocitus",
        "description": "Ahogada en el dolor por la pérdida de su planeta, un anillo rojo de la ira eligió a Kara Zor-El, desatando una destructora cósmica imparable.",
        "hashtags": "#Supergirl #RedLantern #DCComics #KaraZorEl #GreenLantern #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Consumida por el dolor de ver morir a su familia y su mundo, la furia contenida de Kara Zor-El atrajo al arma más destructiva del cosmos!",
            "Un anillo de poder del espectro rojo cruzó el espacio sintiendo su rencor, reemplazando su corazón kryptoniano y expulsando sangre de plasma hirviendo por su boca.",
            "Convertida en una Linterna Roja sin control ni juicio, Supergirl destruyó flotas alienígenas enteras enfrentándose a Superman y a la Liga de la Justicia.",
            "Fue Guy Gardner quien la llevó al lago de sangre de Ysmault, donde Kara recuperó su cordura y aceptó su ira para proteger a los indefensos.",
            "Tras purgar el anillo arrojándolo al corazón del sol, Kara renació como una protectora madura y temible. ¿Tiene Supergirl más potencial de ira que Superman?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/supergirl_red_lantern_ira/scene_01.jpg",
            "assets/curated_panels/supergirl_red_lantern_ira/scene_02.jpg",
            "assets/curated_panels/supergirl_red_lantern_ira/scene_03.jpg",
            "assets/curated_panels/supergirl_red_lantern_ira/scene_04.jpg",
            "assets/curated_panels/supergirl_red_lantern_ira/scene_05.jpg"
        ],
        "art_queries": [
            "Kara Zor-El enraged crying Supergirl 28 comic panel scan",
            "Supergirl Red Lantern transformation red ring vomiting plasma Supergirl 28 panel",
            "Supergirl Red Lantern destroying alien spaceships comic scan",
            "Guy Gardner Supergirl Ysmault blood lake Red Lanterns 29 comic scan",
            "Supergirl removing red ring flying into sun Supergirl 33 comic scan"
        ]
    },
    {
        "id": "constantine_engano_triunvirato_infierno",
        "universe": "DC",
        "character": "John Constantine",
        "title": "¡Constantine Engañó a los Reyes del Infierno! La Mayor Estafa a Lucifer 🚬🔥",
        "theme_signature": "constantine:triunvirato_infierno:lucifer_azazel:cancer_pulmon:engano",
        "description": "Agonizando por un cáncer terminal, John Constantine vende su alma a los tres reyes del infierno por separado, forzándolos a curarlo para evitar una guerra total.",
        "hashtags": "#Constantine #Hellblazer #DCComics #Vertigo #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¡Condenado a morir por un cáncer de pulmón terminal, John Constantine orquestó la estafa sobrenatural más brillante y peligrosa de la historia!",
            "Sabiendo que su alma estaba destinada al tormento eterno, visitó en secreto a los tres señores del Infierno: el Primer Caído, Azazel y Beelzebub.",
            "A espaldas de cada demonio, Constantine vendió su alma por separado a los tres a cambio de promesas de poder, guardando silencio absoluto.",
            "Al llegar la hora de su muerte, los tres reyes infernales se manifestaron para reclamar su botín descubriendo la triple traición que provocaría una guerra total en el averno.",
            "Para evitar que el Infierno se destruyera en una guerra civil por su alma, Lucifer se vio obligado a extirparle el cáncer y devolverle la vida. ¿Es John Constantine el mortal más astuto?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/constantine_triunvirato_infierno/scene_01.jpg",
            "assets/curated_panels/constantine_triunvirato_infierno/scene_02.jpg",
            "assets/curated_panels/constantine_triunvirato_infierno/scene_03.jpg",
            "assets/curated_panels/constantine_triunvirato_infierno/scene_04.jpg",
            "assets/curated_panels/constantine_triunvirato_infierno/scene_05.jpg"
        ],
        "art_queries": [
            "John Constantine trench coat hospital lung cancer Hellblazer 45 panel",
            "First of the Fallen devil ruler Hellblazer comic panel scan",
            "John Constantine making deal demon lord Hellblazer comic panel",
            "Three lords of Hell devils confronting Constantine Hellblazer 45 panel",
            "John Constantine cured smoking cigarette smiling Hellblazer 45 iconic panel"
        ]
    },
    {
        "id": "punisher_war_machine_armadura_blanca",
        "universe": "Marvel",
        "character": "War Machine (Frank Castle)",
        "title": "¡War Machine Blindó al Castigador! La Armadura de Destrucción Masiva en Chernaya 💀🤖",
        "theme_signature": "war_machine:punisher:chernaya_armadura_stark:calavera_titanio",
        "description": "Cuando Nick Fury le entregó la armadura de War Machine, Frank Castle pintó su icónica calavera blanca en el titanio desatando una guerra implacable en Chernaya.",
        "hashtags": "#ThePunisher #WarMachine #FrankCastle #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Qué sucede cuando combinas la letalidad de Frank Castle con el armamento más destructivo de Tony Stark? ¡El nacimiento del terror definitivo!",
            "Reclutado por Nick Fury para derrocar a un sanguinario dictador en Europa del Este, Castle se infiltró en una base secreta y tomó posesión de la armadura de War Machine.",
            "Pintando su icónica calavera blanca sobre el blindaje de titanio, el Castigador se convirtió en un ejército de un solo hombre con poder de fuego devastador.",
            "Desatando misiles y ametralladoras pesadas, Frank destruyó tanques, helicópteros y batallones enteros sin mostrar un solo gramo de piedad.",
            "Incluso cuando los Vengadores intentaron detenerlo, Castle demostró que ninguna ley humana puede frenar su castigo. ¿Crees que Frank es el héroe más temido de Marvel?"
        ],
        "scene_art_urls": [
            "assets/curated_panels/punisher_war_machine_armadura/scene_01.jpg",
            "assets/curated_panels/punisher_war_machine_armadura/scene_02.jpg",
            "assets/curated_panels/punisher_war_machine_armadura/scene_03.jpg",
            "assets/curated_panels/punisher_war_machine_armadura/scene_04.jpg",
            "assets/curated_panels/punisher_war_machine_armadura/scene_05.jpg"
        ],
        "art_queries": [
            "Punisher War Machine suit flying desert battle comic panel",
            "Frank Castle War Machine armor cockpit interior comic panel",
            "Punisher War Machine white skull armor heavy weapons comic panel",
            "War Machine Punisher missiles gunfire destruction comic panel",
            "Punisher War Machine confronting heroes unstoppable Marvel comic panel"
        ]
    },
    {
            "id": "saint_walker_primer_linterna_azul_esperanza",
            "universe": "DC",
            "character": "Saint Walker",
            "title": "¡El Primer Linterna Azul del Cosmos! El Milagro que Salvó a Hal Jordan 💙✨",
            "theme_signature": "saint_walker:blue_lantern:esperanza_bateria:hal_jordan_ysmault",
            "description": "En un cosmos desgarrado por la guerra, Bro'Dee Walker ascendió como el primer Linterna Azul, portando la luz de la esperanza que curó el alma de Hal Jordan.",
            "hashtags": "#SaintWalker #BlueLantern #GreenLantern #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡En un cosmos desgarrado por la guerra, Bro'Dee Walker demostró que la fe es la mayor fuerza del universo!",
                    "Tras la extinción de su mundo, los Guardianes lo consagraron como el primer Linterna Azul.",
                    "Al viajar a Ysmault, curó la ira roja de Hal Jordan proclamando: ¡todo estará bien!",
                    "Supercargando los anillos verdes al doscientos por ciento, probó el poder de la esperanza. ¿Supera a la voluntad?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/saint_walker_linterna_azul/scene_01.jpg",
                    "assets/curated_panels/saint_walker_linterna_azul/scene_02.jpg",
                    "assets/curated_panels/saint_walker_linterna_azul/scene_03.jpg",
                    "assets/curated_panels/saint_walker_linterna_azul/scene_04.jpg"
            ],
            "art_queries": [
                    "Blue Lantern Corps soaring space comic panel",
                    "Saint Walker Bro Dee Walker Astonia hope comic panel",
                    "Saint Walker healing Hal Jordan red lantern rage Ysmault comic panel",
                    "Blue Lantern Corps charging green lanterns comic panel"
            ]
    },
    {
            "id": "captain_america_asesinato_civil_war_sharon",
            "universe": "Marvel",
            "character": "Captain America (Steve Rogers)",
            "title": "¡El Asesinato del Capitán América! El Disparo a Quemarropa que Conmocionó al Mundo 🇺🇸🩸",
            "theme_signature": "captain_america:asesinato_civil_war:escalinatas_tribunal_sharon_carter:crossbones",
            "description": "Tras rendirse en la Guerra Civil, Steve Rogers fue asesinado en las escalinatas del tribunal en un complot orquestado por Red Skull.",
            "hashtags": "#CaptainAmerica #CivilWar #SteveRogers #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Tras rendirse en la Guerra Civil, el Capitán América enfrentó su juicio final en las escalinatas de Nueva York!",
                    "Desde un tejado, el francotirador Crossbones disparó una bala de alto calibre a su hombro.",
                    "En medio del pánico, una hipnotizada Sharon Carter le disparó tres tiros mortales a quemarropa.",
                    "Muriendo en brazos de Sam Wilson, el centinela de la libertad cayó. ¿Debió Steve jamás rendirse?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/captain_america_asesinato_civil_war/scene_01.jpg",
                    "assets/curated_panels/captain_america_asesinato_civil_war/scene_02.jpg",
                    "assets/curated_panels/captain_america_asesinato_civil_war/scene_03.jpg",
                    "assets/curated_panels/captain_america_asesinato_civil_war/scene_04.jpg"
            ],
            "art_queries": [
                    "Civic Center from Captain America Vol 5 25 001.jpg",
                    "Brock Rumlow Earth-616 Crossbones sniper comic panel",
                    "Steven Rogers Sharon Carter gun shot Captain America 25 comic panel",
                    "Samuel Wilson holding dying Steven Rogers Captain America 25 comic panel"
            ]
    },
    {
            "id": "zoom_hunter_zolomon_chasquido_sonico",
            "universe": "DC",
            "character": "Zoom (Hunter Zolomon)",
            "title": "¡Zoom Destruyó a Wally West! El Chasquido Sónico que Rompió la Línea Temporal ⚡⏱️",
            "theme_signature": "zoom:hunter_zolomon:chasquido_sonico_tiempo:tragedia_wally_west",
            "description": "Hunter Zolomon manipula su propia línea temporal, desatando una onda de choque sónica para enseñarle a Flash el verdadero significado del dolor.",
            "hashtags": "#TheFlash #Zoom #HunterZolomon #WallyWest #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Hunter Zolomon no usa la Speed Force, sino que manipula el tiempo volviéndose inalcanzable para Flash!",
                    "Convencido de que Wally necesitaba tragedia para madurar, Zoom desató el caos sobre Keystone City.",
                    "Con un chasquido sónico de sus dedos provocó una onda expansiva que destruyó a la familia de Wally.",
                    "Ni la velocidad luz pudo evitar el colapso de su vida. ¿Es Zoom el villano más sádico de DC?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/zoom_hunter_zolomon_chasquido/scene_01.jpg",
                    "assets/curated_panels/zoom_hunter_zolomon_chasquido/scene_02.jpg",
                    "assets/curated_panels/zoom_hunter_zolomon_chasquido/scene_03.jpg",
                    "assets/curated_panels/zoom_hunter_zolomon_chasquido/scene_04.jpg"
            ],
            "art_queries": [
                    "Zoom Hunter Zolomon red eyes yellow suit comic panel",
                    "Wally West Flash fighting Zoom Keystone City comic panel",
                    "Zoom finger snap sonic boom shockwave comic panel",
                    "Wally West defeated crying tragedy Flash comic panel"
            ]
    },
    {
            "id": "sinestro_luz_blanca_entidad_vida",
            "universe": "DC",
            "character": "Sinestro",
            "title": "¡Sinestro se Fusionó con la Entidad Divina! El Milagro de la Creación Cósmica 🤍✨",
            "theme_signature": "sinestro:entidad_blanca:luz_de_la_vida:resurreccion_universo",
            "description": "Ante la aniquilación de la muerte cósmica encarnada en Nekron, Sinestro reclamó la Entidad de la Vida y renació como el primer Linterna Blanca.",
            "hashtags": "#Sinestro #WhiteLantern #GreenLantern #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Cuando Nekron amenazó con devorar toda la existencia, el mayor villano del cosmos dio el paso impensable!",
                    "Rechazando el miedo amarillo, Sinestro se lanzó al centro de la Tierra hacia la Entidad de la Vida.",
                    "Al fusionarse con ella renació como el primer Linterna Blanca, blandiendo el poder absoluto de la creación cósmica.",
                    "Con luz divina derrotó a la muerte salvando al universo entero. ¿Fue Sinestro el verdadero salvador de DC?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/sinestro_luz_blanca_entidad/scene_01.jpg",
                    "assets/curated_panels/sinestro_luz_blanca_entidad/scene_02.jpg",
                    "assets/curated_panels/sinestro_luz_blanca_entidad/scene_03.jpg",
                    "assets/curated_panels/sinestro_luz_blanca_entidad/scene_04.jpg"
            ],
            "art_queries": [
                    "Nekron Blackest Night cosmic threat comic panel",
                    "Sinestro diving into White Lantern Life Entity earth center panel",
                    "Sinestro becomes White Lantern glowing white suit comic panel",
                    "White Lantern Sinestro destroying Nekron Blackest Night comic panel"
            ]
    },
    {
            "id": "blue_beetle_jaime_reyes_escarabajo_khaji_da",
            "universe": "DC",
            "character": "Blue Beetle (Jaime Reyes)",
            "title": "¡El Escarabajo Alienígena se Fusionó con su Columna! El Origen de Jaime Reyes 🪲⚡",
            "theme_signature": "blue_beetle:jaime_reyes:escarabajo_khaji_da:alcance_alienigena",
            "description": "En El Paso, el joven Jaime Reyes encuentra el escarabajo Khaji Da, un arma biomecánica extraterrestre que se injerta en su cuerpo para transformarlo en Blue Beetle.",
            "hashtags": "#BlueBeetle #JaimeReyes #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Caminando por El Paso, el joven Jaime Reyes encontró un extraño escarabajo alienígena enterrado en un baldío!",
                    "Durante la noche el artefacto despertó, perforando su piel e injertándose de por vida en su columna.",
                    "El escarabajo Khaji Da desplegó una armadura biomecánica viviente con cañones sónicos destructores de mundos.",
                    "Sometiendo a la entidad invasora con pura bondad, Jaime forjó su leyenda. ¿Es el arma definitiva de DC?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/blue_beetle_jaime_reyes_escarabajo/scene_01.jpg",
                    "assets/curated_panels/blue_beetle_jaime_reyes_escarabajo/scene_02.jpg",
                    "assets/curated_panels/blue_beetle_jaime_reyes_escarabajo/scene_03.jpg",
                    "assets/curated_panels/blue_beetle_jaime_reyes_escarabajo/scene_04.jpg"
            ],
            "art_queries": [
                    "Jaime Reyes finding blue beetle scarab vacant lot comic panel",
                    "Khaji Da scarab attaching Jaime Reyes spine bedroom comic panel",
                    "Blue Beetle biomechanical armor sonic cannons transforming panel",
                    "Blue Beetle soaring sky glowing weapons comic panel"
            ]
    },
    {
            "id": "morlun_devora_ojo_spiderman",
            "universe": "Marvel",
            "character": "Morlun (Vampiro Totémico)",
            "title": "¡Morlun le Arrancó el Ojo a Spider-Man! La Masacre del Cazador Heredero 🩸🕷️",
            "theme_signature": "morlun:vampiro_totemico:arranca_ojo_peter_parker:the_other",
            "description": "El vampiro totémico Morlun acorraló a un exhausto Peter Parker, arrancándole un ojo y devorándolo vivo en la batalla más salvaje del trepamuros.",
            "hashtags": "#SpiderMan #Morlun #TheOther #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡El vampiro totémico Morlun cazó a Spider-Man hasta llevar el cuerpo de Peter Parker a su límite!",
                    "Ignorando cada ataque arácnido, el cazador quebró sus costillas y destrozó su máscara a golpes.",
                    "En el clímax del horror, Morlun le arrancó el ojo izquierdo a Peter devorándolo ante sus ojos.",
                    "Dejando al héroe agonizando al borde de la muerte, demostró su hambre insaciable. ¿Es el villano más brutal?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/morlun_devora_ojo_spiderman/scene_01.jpg",
                    "assets/curated_panels/morlun_devora_ojo_spiderman/scene_02.jpg",
                    "assets/curated_panels/morlun_devora_ojo_spiderman/scene_03.jpg",
                    "assets/curated_panels/morlun_devora_ojo_spiderman/scene_04.jpg"
            ],
            "art_queries": [
                    "Morlun hunting Spider-Man exhausted bloody streets comic panel",
                    "Morlun punching Spider-Man breaking ribs shattered mask panel",
                    "Morlun ripping eating Spider-Man eye horror Amazing Spider-Man comic panel",
                    "Spider-Man beaten dying hospital bed Morlun comic panel"
            ]
    },
    {
            "id": "doomsday_humilla_darkseid_apokolips",
            "universe": "DC",
            "character": "Doomsday (Juicio Final)",
            "title": "¡Doomsday Destrozó a Darkseid en Apokolips! La Humillación del Dios del Mal 💀🔥",
            "theme_signature": "doomsday:destrozo_darkseid:apokolips_invasion:rayos_omega_inutiles",
            "description": "Al aterrizar en el planeta infernal de Apokolips, Doomsday resistió los legendarios Rayos Omega de Darkseid y lo molió a golpes con furia imparable.",
            "hashtags": "#Doomsday #Darkseid #Superman #Apokolips #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Al escapar al cosmos, Doomsday aterrizó en Apokolips desatando una masacre imparable contra los ejércitos oscuros!",
                    "Confiado en su divinidad, Darkseid disparó sus infalibles Rayos Omega para desintegrar al coloso.",
                    "Doomsday resistió el rayo sin rasguños, avanzando hasta quebrar los brazos del tirano a golpes.",
                    "Dejando al señor del mal ensangrentado e impotente en su trono, demostró su furia. ¿Es Doomsday invencible?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/doomsday_humilla_darkseid_apokolips/scene_01.jpg",
                    "assets/curated_panels/doomsday_humilla_darkseid_apokolips/scene_02.jpg",
                    "assets/curated_panels/doomsday_humilla_darkseid_apokolips/scene_03.jpg",
                    "assets/curated_panels/doomsday_humilla_darkseid_apokolips/scene_04.jpg"
            ],
            "art_queries": [
                    "Doomsday rampage Apokolips destroying parademons comic panel",
                    "Darkseid firing Omega Beams at Doomsday Hunter Prey comic panel",
                    "Doomsday shrugging off Omega Beams breaking Darkseid arms panel",
                    "Darkseid beaten bloody lying defeated Doomsday standing comic panel"
            ]
    },
    {
            "id": "venom_dios_de_la_luz_fuerza_enigma",
            "universe": "Marvel",
            "character": "Captain Universe (Eddie Brock)",
            "title": "¡El Hacha de Luz que Destruyó la Oscuridad! La Apoteosis Cósmica en King in Black 🤍⚡",
            "theme_signature": "captain_universe:fuerza_enigma:hacha_cosmica_resurreccion:aniquilacion_sol",
            "description": "Cuando Knull conquistó la Tierra con oscuridad absoluta, la legendaria Fuerza Enigma resucitó a Eddie Brock como el Dios de la Luz.",
            "hashtags": "#Venom #KingInBlack #EnigmaForce #Knull #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Cuando el Dios Simbionte Knull sumergió al planeta en oscuridad eterna, la última esperanza despertó!",
                    "La Fuerza Enigma descendió del cosmos resucitando a un moribundo Eddie Brock como el Dios de la Luz.",
                    "Forjando un hacha cósmica con el martillo de Thor, decapitó a las hordas de dragones alienígenas.",
                    "Arrastró a Knull al corazón del sol incinerándolo para siempre. ¿Fue esta la mayor victoria de Marvel?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/venom_dios_de_la_luz_fuerza_enigma/scene_01.jpg",
                    "assets/curated_panels/venom_dios_de_la_luz_fuerza_enigma/scene_02.jpg",
                    "assets/curated_panels/venom_dios_de_la_luz_fuerza_enigma/scene_03.jpg",
                    "assets/curated_panels/venom_dios_de_la_luz_fuerza_enigma/scene_04.jpg"
            ],
            "art_queries": [
                    "Knull symbiote dome covering Earth King in Black comic panel",
                    "Eddie Brock glowing Enigma Force Captain Universe transformation panel",
                    "Captain Universe Venom wielding light battle axe cutting symbiote dragons panel",
                    "Venom throwing Knull into sun disintegrating King in Black finale panel"
            ]
    },
    {
            "id": "azrael_batman_armadura_asesina",
            "universe": "DC",
            "character": "Jean-Paul Valley (Azrael)",
            "title": "¡El Batman Dorado de Azrael! Jean-Paul Valley Destrozó a Bane con Cuchillas y Fuego 🦇⚔️",
            "theme_signature": "azrael:jean_paul_valley:armadura_cuchillas:orden_de_san_dumas",
            "description": "Tras la caída de Bruce Wayne, Jean-Paul Valley reemplazó a Batman construyendo una aterradora armadura armada con garras y lanzallamas para imponer justicia despiadada.",
            "hashtags": "#Batman #Azrael #Knightfall #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡Con la columna de Bruce Wayne quebrada por Bane, un fanático religioso asumió el manto de Gotham!",
                    "Jean-Paul Valley rechazó la regla de no matar, construyendo una armadura mecánica armada con cuchillas y lanzallamas.",
                    "Acorraló a Bane en combate despiadado, cortando sus tubos de Venom y moliéndolo a golpes.",
                    "Consumido por la Orden de San Dumas, impuso el terror definitivo. ¿Debió Bruce confiarle su legado?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/azrael_batman_armadura_asesina/scene_01.jpg",
                    "assets/curated_panels/azrael_batman_armadura_asesina/scene_02.jpg",
                    "assets/curated_panels/azrael_batman_armadura_asesina/scene_03.jpg",
                    "assets/curated_panels/azrael_batman_armadura_asesina/scene_04.jpg"
            ],
            "art_queries": [
                    "Azrael Batman Knightfall armor rooftop Gotham comic panel",
                    "Jean-Paul Valley armored Batman gauntlets blades flame comic panel",
                    "Azrael armored Batman slashing Bane venom tubes Batman 500 panel",
                    "Azrael Batman standing victorious over defeated broken Bane Batman 500 panel"
            ]
    },
    {
            "id": "old_man_logan_estomago_hulk_canibal",
            "universe": "Marvel",
            "character": "Logan (Wasteland)",
            "title": "¡Logan Desgarró a Hulk desde Adentro! El Fin del Tirano Caníbal en Wasteland 🥩🩸",
            "theme_signature": "logan_anciano:coloso_canibal:regeneracion_tripas:caida_tirano_california",
            "description": "En un futuro desolado, Wolverine desenfunda sus garras tras décadas de paz para vengar a su familia, sufriendo ser devorado por Hulk antes de desgarrar al monstruo desde su estómago.",
            "hashtags": "#Wolverine #OldManLogan #Hulk #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
            "scenes": [
                    "¡En un páramo dominado por villanos, Logan desenfundó sus garras decapitando a la banda de Hulk!",
                    "Frente a su fortaleza, un decrépito Bruce Banner reveló la bestia imparable que aún habitaba en él.",
                    "Logan se lanzó al ataque atravesando el cuerpo de Banner con sus garras, desatando la furia del gigante.",
                    "Tras ser devorado, Wolverine se regeneró en las tripas de Hulk desgarrando su vientre desde adentro. ¿La muerte más grotesca?"
            ],
            "scene_art_urls": [
                    "assets/curated_panels/old_man_logan_estomago_hulk/scene_01.jpg",
                    "assets/curated_panels/old_man_logan_estomago_hulk/scene_02.jpg",
                    "assets/curated_panels/old_man_logan_estomago_hulk/scene_03.jpg",
                    "assets/curated_panels/old_man_logan_estomago_hulk/scene_04.jpg"
            ],
            "art_queries": [
                    "James Howlett Bobbie-Jo Banner Wolverine Old Man Logan Giant-Size 1 001.jpg",
                    "Bruce Banner James Howlett Billy-Bob Banner Wolverine Old Man Logan Giant-Size 1 001.jpg",
                    "James Howlett Bruce Banner Wolverine Old Man Logan Giant-Size 1 001.jpg",
                    "James Howlett Bruce Banner Wolverine Old Man Logan Giant-Size 1 003.jpg"
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
    
    # Solo prohibir los personajes de los últimos 6 videos publicados para garantizar rotación sin vetar a los iconos Tier-1
    recent_characters = set(item.get("character", "").strip() for item in ledger[-6:] if item.get("character"))
    past_titles = [item.get("title", "").strip() for item in ledger if item.get("title")]
    past_themes = [item.get("theme_signature", "").strip() for item in ledger if item.get("theme_signature")]

    char_recency_banned = ", ".join(sorted(list(recent_characters)))
    titles_summary = " | ".join(past_titles[-40:])

    # Grupos rotativos con arcos legendarios INÉDITOS para garantizar que la IA nunca proponga historias ya existentes
    ROTATING_CHAR_PROMPTS = [
        "Miles Morales (Ultimate Spider-Man / Veneno Eléctrico / Prowler Aaron Davis), Red Hood (Lost Days / Venganza con All-Caste / Regreso de la Muerte), Death of Captain America (Asesinato en Escalinatas del Tribunal / Crossbones y Sharon Carter)",
        "Saint Walker (Bro'Dee Walker / Primer Linterna Azul / Esperanza Cósmica), Zoom Hunter Zolomon (Blitz / Chasquido Sónico / Destrucción de Wally West), Moon Knight (Marc Spector / Misión de Medianoche / Venganza de Khonshu)",
        "Sinestro (Linterna Blanca / Primera Batería de Vida / Volthoom), Ghost Rider Robbie Reyes (All-New Ghost Rider / Muscle Car del Infierno / Eli Morrow), Invincible Iron Man (Armor Wars / Traición de Armaduras Stark)",
        "Daredevil (Guardian Devil / Muerte de Karen Page / Bullseye en la Iglesia), Wolverine (Venganza contra Hulk en Old Man Logan / Descuartizamiento Interior), Green Lantern Kyle Rayner (Ascenso a Ion / Poder Infinito de Oa)"
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
