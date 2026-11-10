"""
Master Production Engine: Batch 8 Remastered Viral Hits (Slots 77 al 86)
========================================================================
1. Slot 77: Thanos Rising - El Origen Perturbador de Thanos
2. Slot 78: Uncanny X-Men - Días del Futuro Pasado
3. Slot 79: Thanos Wins - Thanos Conquistó el Fin del Universo
4. Slot 80: Batman: Silencio (Hush) - La Conspiración Wayne
5. Slot 81: Doctor Strange: The Oath - La Cura Prohibida del Cáncer
6. Slot 82: Ultimate Wolverine vs Hulk - Logan en Dos Mitades
7. Slot 83: Siege: Sentry / The Void - La Destrucción de Asgard
8. Slot 84: House of M - Scarlet Witch: "No Más Mutantes"
9. Slot 85: Uncanny X-Force - Archangel: El Heredero de Apocalipsis
10. Slot 86: The Amazing Spider-Man - La Última Cacería de Kraven

Reglas Críticas:
- Duración obligatoria >= 60.0 segundos por video (estricta monetización).
- Viñetas canónicas 1:1 enmarcadas con safe-zone no destructiva y fondo desenfocado (frame_to_vertical_1080x1920).
- Miniatura minimalista (2 a 4 palabras, sin párrafos amontonados) inyectada en fotograma exacto t=0.000s.
- Salida automática en scheduled_queue/{slot}_{name}/ con video.mp4 y metadata.json.
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.pipeline import run_pipeline
from src.cloud_runner import build_cloud_generation
from src.composer import get_duration

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_8_remasters"
PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
BRAIN_DIR = Path(r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb")

FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
if not Path(FONT_IMPACT).exists():
    FONT_IMPACT = r"C:\Users\Vanes\comics en espanol\fonts\impact.ttf"

def apply_cinematic_grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.22)
    im = ImageEnhance.Color(im).enhance(1.20)
    im = ImageEnhance.Sharpness(im).enhance(1.15)
    return im

def fit_to_vertical(im: Image.Image, target_w=1080, target_h=1920) -> Image.Image:
    w, h = im.size
    aspect = w / h
    if w == target_w and h == target_h:
        return im.copy()

    if aspect > 1.1:
        bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(35))
        bg = ImageEnhance.Brightness(bg).enhance(0.40)

        new_w = target_w
        new_h = int(target_w / aspect)
        fg = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

        pos_y = (target_h - new_h) // 2
        bg.paste(fg, (0, pos_y))
        return bg
    else:
        scale = max(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)
        scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - target_w) // 2
        top = (nh - target_h) // 2
        return scaled.crop((left, top, left + target_w, top + target_h))

def render_minimal_text_thumb(image_path: Path, text: str, output_path: Path,
                              text_y=240, text_color=(255, 235, 0), font_size=108):
    raw_img = Image.open(image_path).convert("RGB")
    graded = apply_cinematic_grade(raw_img)
    canvas = fit_to_vertical(graded, 1080, 1920)

    font = ImageFont.truetype(FONT_IMPACT, font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    if tw > 960:
        adjusted_size = int(font_size * (940 / tw))
        font = ImageFont.truetype(FONT_IMPACT, adjusted_size)
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

    tx = (1080 - tw) // 2 - bbox[0]
    ty = text_y

    canvas_rgba = canvas.convert("RGBA")
    shadow_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((tx, ty + 7), text, font=font, fill=(0, 0, 0, 240), stroke_width=20, stroke_fill=(0, 0, 0, 240))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))

    canvas_rgba = Image.alpha_composite(canvas_rgba, shadow_layer)

    text_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    t_draw.text((tx, ty), text, font=font, fill=text_color, stroke_width=11, stroke_fill=(0, 0, 0))

    final_im = Image.alpha_composite(canvas_rgba, text_layer).convert("RGB")
    final_im.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"  [THUMB MINIMAL] {output_path.name}: '{text}'")
    return output_path

def inject_thumbnail_into_video(video_path: Path, thumb_path: Path, slot_name: str):
    temp_out = video_path.parent / f"{video_path.stem}_frame0.mp4"

    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-loop', '1', '-t', '0.40', '-i', str(thumb_path),
        '-filter_complex',
        '[1:v]fps=30,scale=1080:1920,setsar=1[vthumb];[0:v]trim=start=0.40,setpts=PTS-STARTPTS[vmain];[vthumb][vmain]concat=n=2:v=1:a=0[v]',
        '-map', '[v]',
        '-map', '0:a',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        '-c:a', 'copy',
        str(temp_out)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR FFMPEG INJECTION]: {res.stderr[-300:]}")
        if temp_out.exists():
            temp_out.unlink()
        return False

    if temp_out.stat().st_size < 1000000:
        print(f"  [ERROR] Video resultante corrupto: {temp_out.stat().st_size} bytes")
        temp_out.unlink()
        return False

    audit_f0 = BRAIN_DIR / f"audit_minimal_frame0_{slot_name}.jpg"
    subprocess.run([
        'ffmpeg', '-y',
        '-ss', '00:00:00.000',
        '-i', str(temp_out),
        '-vframes', '1',
        '-q:v', '2',
        str(audit_f0)
    ], capture_output=True)

    if video_path.exists():
        video_path.unlink()
    shutil.move(temp_out, video_path)
    print(f"  [OK] Frame 0 inyectado y auditado: {video_path.name}")
    return True

REMASTER_PROJECTS_BATCH_8 = [
    {
        "slot": 77,
        "queue_folder": "77_thanos_origen_perturbador_muerte",
        "id": "thanos_origen_perturbador_muerte",
        "title": "¡El Origen Perturbador de Thanos! El Monstruo que Asesinó a su Propia Madre 💀🌌🩸",
        "character": "Thanos & Lady Death",
        "folder": "77_thanos_origen_perturbador_muerte",
        "theme_signature": "thanos:thanos_rising:origin_lady_death_slaughter",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/77_thanos_origen_perturbador_muerte/scene_03.jpg",
            "text": "¡EL ORIGEN DE THANOS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El origen más retorcido y aterrador en todo el universo de Marvel que definió el destino de la galaxia! En las lunas de Titán, una sociedad utópica y pacífica fue testigo del nacimiento de un bebé con el gen Deviant: piel púrpura y ojos oscuros. Su propia madre, Sui-San, al mirarlo a los ojos enloqueció y trató de asesinarlo con un bisturí, profetizando la destrucción cósmica."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aislado y rechazado por su aspecto monstruoso, el joven Thanos era tímido y pacifista. Pero todo cambió al descender a las cavernas prohibidas junto a sus compañeros de escuela, quienes fueron devorados por monstruos subterráneos. Guiado por una misteriosa niña que lo incitaba a explorar los límites del dolor, Thanos comenzó a diseccionar criaturas vivas para entender la muerte."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "A medida que su obsesión científica se convertía en una sed insaciable de sangre, la misteriosa niña se reveló como la mismísima personificación de la Muerte. Enamorado ciegamente de la entidad, Thanos cometió atrocidades impensables a través de las estrellas, regresando a Titán no para reconciliarse con su gente, sino para desatar un holocausto."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Thanos bombardeó su propio planeta con armas nucleares, masacrando a millones de inocentes, y capturó a su madre para abrirla viva en su mesa de operaciones, buscando inútilmente dónde residía el amor que ella nunca le dio. ¿Crees que Thanos nació siendo un monstruo o la Dama Muerte lo corrompió? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "El origen psicológico y aterrador de Thanos en Thanos Rising #1-5 de Jason Aaron y Simone Bianchi.",
        "hashtags": "#Thanos #LadyDeath #ThanosRising #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 78,
        "queue_folder": "78_xmen_dias_del_futuro_pasado",
        "id": "xmen_dias_del_futuro_pasado",
        "title": "¡Días del Futuro Pasado! El Apocalipsis de los Centinelas que Exterminó a los Mutantes 🤖🔥⏳",
        "character": "X-Men & Sentinels",
        "folder": "78_xmen_dias_del_futuro_pasado",
        "theme_signature": "xmen:days_of_future_past:sentinel_genocide_timeline",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/78_xmen_dias_del_futuro_pasado/scene_01.jpg",
            "text": "¡EXTERMINIO MUTANTE!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La historia más trágica y desesperada de los Hombres X que revolucionó la ciencia ficción en los cómics! En un sombrío y distópico año dos mil trece, los Centinelas han tomado el control absoluto de Norteamérica, recluyendo a los pocos mutantes sobrevivientes en campos de concentración y cazando despiadadamente a todo superhumano."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "La mayoría de los X-Men han sido masacrados: el legendario cartel de Se Busca muestra los rostros tachados de Cíclope, Tormenta y Coloso con la temida palabra Asesinado. Los Centinelas no solo barrieron con los portadores del gen X, sino que redujeron a cenizas las grandes ciudades de la humanidad para imponer su orden robótico."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En un último y desesperado intento por evitar el apocalipsis, los últimos guerreros restantes, liderados por un envejecido y amargado Wolverine, orquestan un plan suicida. Usando los poderes telepáticos de Rachel Summers, transfieren la consciencia de Kate Pryde décadas hacia el pasado para advertir a sus compañeros antes de la catástrofe."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "La misión en el presente consiste en impedir el magnicidio del senador Robert Kelly a manos de la Hermandad de Mutantes, el detonante de la ley anti-mutante. Mientras en el futuro los Centinelas vaporizan a Wolverine hasta dejar solo su esqueleto de adamantium, ¿habrá valido la pena su sacrificio? ¡Comenta si este es el mejor cómic de los X-Men!"
            }
        ],
        "description": "La legendaria obra maestra Uncanny X-Men #141-142 de Chris Claremont y John Byrne: Days of Future Past.",
        "hashtags": "#XMen #DaysOfFuturePast #Wolverine #Sentinels #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 79,
        "queue_folder": "79_thanos_gana_fin_del_universo",
        "id": "thanos_gana_fin_del_universo",
        "title": "¡Thanos Conquistó Todo el Universo! La Masacre al Fin de los Tiempos 💀👑🔥",
        "character": "King Thanos & Cosmic Ghost Rider",
        "folder": "79_thanos_gana_fin_del_universo",
        "theme_signature": "thanos:thanos_wins:old_king_cosmic_ghost_rider",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/79_thanos_gana_fin_del_universo/scene_01.jpg",
            "text": "¡THANOS CONQUISTÓ TODO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La historia definitiva donde el Titán Loco finalmente logra lo impensable y aniquila toda la vida del cosmos! En la aclamada saga de Donny Cates, vemos que sin importar cuántas veces los héroes de la Tierra o los dioses galácticos resistieron, la profecía universal se cumplió: al final de todos los tiempos, Thanos siempre gana."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Thanos exterminó a los Vengadores, asesinó a los Celestiales, derribó a Galactus y redujo a polvo el multiverso entero. Sentado sobre una pirámide colosal hecha con los cráneos de miles de billones de seres vivientes, gobierna en absoluta soledad como el Rey Thanos, el ser supremo de una existencia moribunda y vacía."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Para cumplir su último anhelo, envía a su sirviente enloquecido, el Cósmico Ghost Rider, con las cadenas de Cyttorak a través del tiempo para secuestrar a su versión joven. El Thanos del presente es arrastrado al futuro no para una alianza gloriosa, sino para contemplar el horror de una victoria cósmica totalmente desolada."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El anciano Rey Thanos solo necesita una última cosa para reunirse con su amada Muerte: que su yo del pasado lo mate en combate a muerte con la Espada del Crepúsculo. ¿Es Thanos el villano definitivo y más temible en la historia de Marvel? ¡Suscríbete y déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La magistral saga Thanos Wins (Thanos Vol. 2 #13-18) de Donny Cates y Geoff Shaw. El fin de todos los tiempos.",
        "hashtags": "#Thanos #KingThanos #ThanosWins #CosmicGhostRider #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 80,
        "queue_folder": "80_batman_hush_conspiracion_wayne",
        "id": "batman_hush_conspiracion_wayne",
        "title": "¡La Conspiración Definitiva Contra Bruce Wayne! La Venganza de Batman Hush 🦇🩹🤫",
        "character": "Batman & Hush (Thomas Elliot)",
        "folder": "80_batman_hush_conspiracion_wayne",
        "theme_signature": "batman:hush:thomas_elliot_revenge_gotham",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/80_batman_hush_conspiracion_wayne/scene_04.jpg",
            "text": "¡LA TRAMPA DE HUSH!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La conspiración psicológica más siniestra y letal que casi destruye por completo al Caballero de la Noche! En la obra maestra de Jeph Loeb y Jim Lee, una misteriosa figura vendada en la penumbra orquesta un ataque masivo sincronizando a toda la galería de villanos de Gotham con una precisión milimétrica jamás antes vista."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Durante una persecución nocturna sobre los rascacielos, la cuerda del batarang de Batman es saboteada, provocando una caída libre devastadora que le fractura el cráneo. Al borde de la muerte, Alfred recurre al doctor Thomas Elliot, el brillante neurocirujano y amigo de la infancia de Bruce, quien realiza una milagrosa operación cerebral."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero la pesadilla apenas comenzaba: Killer Croc, Poison Ivy manipulando a Superman con kriptonita, el Joker y el Acertijo atacan en una danza macabra sin descanso. Pronto se revela que el titiritero vendado, que se hace llamar Hush, conoce íntimamente el pasado, la identidad y cada secreto oscuro de la familia Wayne."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Detrás de las vendas se ocultaba el rencor putrefacto de Elliot, quien odiaba a los Wayne porque Thomas Wayne salvó la vida de su madre, arruinando su plan de heredar una fortuna. ¿Es Hush el villano con el plan más perfecto para destrozar a Batman? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La conspiración definitiva en Batman: Hush (Batman #608-619) de Jeph Loeb y Jim Lee. El complot de Thomas Elliot.",
        "hashtags": "#Batman #Hush #ThomasElliot #DCComics #BatmanHush #Gotham #Comics #Shorts #Reels"
    },
    {
        "slot": 81,
        "queue_folder": "81_doctor_strange_the_oath_cura_cancer",
        "id": "doctor_strange_the_oath_cura_cancer",
        "title": "¡Doctor Strange Descubrió la Cura del Cáncer! El Dilema Moral del Hechicero Supremo 🔮💊✨",
        "character": "Doctor Strange & Wong",
        "folder": "81_doctor_strange_the_oath_cura_cancer",
        "theme_signature": "doctor_strange:the_oath:cancer_cure_elixir_otkid",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/81_doctor_strange_the_oath_cura_cancer/scene_03.jpg",
            "text": "¡LA CURA PROHIBIDA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El dilema moral más desgarrador y humano que jamás enfrentó el Hechicero Supremo de Marvel! En la brillante obra The Oath de Brian K. Vaughan, Stephen Strange descubre que su compañero y mejor amigo Wong padece un tumor cerebral terminal e inoperable que ningún hechizo médico terrenal puede revertir."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Desesperado por salvar a su hermano de vida, Strange viaja a dimensiones prohibidas y supera pruebas mortales para conseguir el legendario Elixir de Otkid, una poción mística milagrosa capaz de erradicar cualquier tipo de cáncer en el cuerpo humano con una sola gota bendita."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero la codicia humana interviene brutalmente: un ex-compañero cirujano y una corporación farmacéutica corrupta le disparan a quemarropa a Strange en el Sanctum Sanctorum para robar la fórmula y lucrar con la enfermedad. Gravemente herido, Stephen guía en forma astral a Night Nurse durante una cirugía a corazón abierto."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al recuperar la única dosis intacta del elixir, Strange afronta la decisión más dura de su existencia: guardarla para salvar al hombre que siempre lo cuidó o arriesgarse a clonarla para el resto del mundo. ¿Habrías hecho lo mismo que Strange para salvar a tu mejor amigo? ¡Comenta abajo tu respuesta!"
            }
        ],
        "description": "Doctor Strange: The Oath de Brian K. Vaughan y Marcos Martin. El juramento hipocrático del Hechicero Supremo.",
        "hashtags": "#DoctorStrange #Wong #TheOath #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 82,
        "queue_folder": "82_ultimate_wolverine_vs_hulk_dos_mitades",
        "id": "ultimate_wolverine_vs_hulk_dos_mitades",
        "title": "¡Hulk Partió a Wolverine en Dos Mitades! La Pelea Más Brutal y Salvaje de Marvel 🩸🏔️🦵",
        "character": "Ultimate Wolverine vs Hulk",
        "folder": "82_ultimate_wolverine_vs_hulk_dos_mitades",
        "theme_signature": "wolverine:vs_hulk:ultimate_ripped_in_half_snow",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/82_ultimate_wolverine_vs_hulk_dos_mitades/scene_03.jpg",
            "text": "¡WOLVERINE EN DOS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La batalla más sangrienta, salvaje y despiadada en toda la historia de los cómics de Marvel! En el universo Ultimate, Nick Fury y la organización S.H.I.E.L.D. envían a Wolverine al Tíbet con una misión aparentemente suicida: cazar y ejecutar al monstruo esmeralda, quien ha desaparecido tras arrasar Manhattan."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El cómic inicia con una de las escenas más impactantes jamás dibujadas: Logan despierta desorientado en medio de una tormenta de nieve brutal en el Himalaya, olfateando el rastro de su propia sangre congelada. Al mirar hacia la montaña, descubre que sus piernas están arrancadas a más de cuatro millas de distancia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En un violento choque cuerpo a cuerpo, un Hulk colosal e imparable había agarrado a Wolverine con ambas manos monstruosas y, usando su rodilla con fuerza descomunal, partió la columna de adamantium de Logan en dos mitades como si fuera una simple rama seca de madera."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Sin rendirse jamás y gracias a su salvaje factor de curación mutante, Wolverine clava sus garras metálicas en el hielo, arrastrando su torso moribundo para recuperar la parte inferior de su cuerpo y terminar la cacería. ¿Podría el Hulk del cine hacerle esto a Wolverine? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La sangrienta confrontación en Ultimate Wolverine vs. Hulk #1 de Damon Lindelof y Leinil Francis Yu.",
        "hashtags": "#Wolverine #Hulk #UltimateWolverine #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 83,
        "queue_folder": "83_sentry_vacio_void_devora_asgard",
        "id": "sentry_vacio_void_devora_asgard",
        "title": "¡The Void Desatado! La Entidad Oscura que Destruyó Asgard y Asombró a los Vengadores 🌑⚡🏛️",
        "character": "Sentry / The Void",
        "folder": "83_sentry_vacio_void_devora_asgard",
        "theme_signature": "sentry:the_void:siege_asgard_destruction_apocalypse",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/83_sentry_vacio_void_devora_asgard/scene_02.jpg",
            "text": "¡THE VOID DESATADO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El colapso más aterrador de Marvel donde el héroe más poderoso se convirtió en la pesadilla de los dioses! Durante el brutal asedio a la ciudad dorada de Asgard en la saga Siege, Norman Osborn perdió el control total sobre Robert Reynolds, desatando a la bestia eldritch que dormía en su mente."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras destrozar horriblemente a Ares con sus propias manos, la psique fracturada de Sentry cedió por completo: el héroe dorado desapareció para dar paso a The Void, una entidad primordial cósmica hecha de sombras vivientes, ojos carmesí y tentáculos colosales que cubrieron el cielo entero."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Bajo la orden de arrasarlo todo, The Void canalizó una fuerza destructiva inimaginable, derribando las columnas celestiales y haciendo que Asgard colapsara en un impacto titánico sobre los campos de Oklahoma, reduciendo el reino de los dioses nórdicos a un cementerio en llamas."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Ni los Vengadores reunidos, ni los rayos de Thor, ni el impacto directo de un Helicarrier podían frenar a la monstruosidad oscura, obligando a los héroes a tomar la decisión más dolorosa para erradicarlo. ¿Es Sentry con el Vacío el personaje más peligroso de Marvel? ¡Comenta tu opinión abajo!"
            }
        ],
        "description": "La caída de Asgard y el despertar de The Void en Siege #3-4 de Brian Michael Bendis y Olivier Coipel.",
        "hashtags": "#Sentry #TheVoid #Siege #Asgard #Thor #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 84,
        "queue_folder": "84_scarlet_witch_house_of_m_no_mas_mutantes",
        "id": "scarlet_witch_house_of_m_no_mas_mutantes",
        "title": "¡Tres Palabras que Extinguieron a los Mutantes! El Colapso Mental de Bruja Escarlata 🔴🗣️🧬",
        "character": "Scarlet Witch",
        "folder": "84_scarlet_witch_house_of_m_no_mas_mutantes",
        "theme_signature": "scarlet_witch:house_of_m:no_more_mutants_extinction",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/84_scarlet_witch_house_of_m_no_mas_mutantes/scene_02.jpg",
            "text": "¡NO MÁS MUTANTES!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 110
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El momento más catastrófico e impactante en los sesenta años de historia de los X-Men! Al descubrir que su padre Magneto y su hermano Quicksilver manipularon la realidad para crear un imperio gobernado por la Casa de M, el dolor y la locura de Wanda Maximoff alcanzaron su punto de quiebre absoluto."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Furiosa al ver que Magneto antepuso su fanatismo supremacista por encima del amor a sus propios hijos, Bruja Escarlata se manifestó en una figura divina de energía caótica frente a los héroes de la Tierra, decidida a borrar la causa de todo el sufrimiento que azotaba a su familia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Con un frío susurro que resonó a través de cada rincón de la realidad, Wanda pronunció tres simples palabras: No más mutantes. En ese instante, un destello dorado y cegador envolvió el planeta entero, reescribiendo la estructura genética de la población humana en una fracción de segundo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En el trágico Día M, más del noventa y nueve por ciento de los mutantes perdieron sus poderes instantáneamente, reduciendo a una especie de millones a menos de doscientos sobrevivientes al borde del olvido. ¿Fue este el mayor acto de poder jamás visto en Marvel? ¡Suscríbete y déjanos tu opinión!"
            }
        ],
        "description": "El evento definitorio House of M #7 de Brian Michael Bendis y Olivier Coipel. Las tres palabras de Bruja Escarlata.",
        "hashtags": "#ScarletWitch #HouseOfM #NoMoreMutants #XMen #Magneto #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 85,
        "queue_folder": "85_archangel_heredero_apocalipsis_xforce",
        "id": "archangel_heredero_apocalipsis_xforce",
        "title": "¡La Caída de Archangel! El Heredero Definitivo de Apocalipsis y la Misión Suicida de X-Force 🪽☠️⚔️",
        "character": "Archangel & X-Force",
        "folder": "85_archangel_heredero_apocalipsis_xforce",
        "theme_signature": "archangel:uncanny_xforce:dark_angel_saga_death_seed",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/85_archangel_heredero_apocalipsis_xforce/scene_04.jpg",
            "text": "¡EL NUEVO APOCALIPSIS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 98
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La saga más oscura, violenta y trágica que consagró a Uncanny X-Force como una leyenda de Marvel! Warren Worthington Tercero, el ángel original de los X-Men, libraba una guerra interna agónica y silenciosa contra la personalidad psicópata de Archangel, implantada años atrás por el tirano Apocalipsis."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Para evitar que la Semilla de la Muerte celeste despertara en su mente, Wolverine y Psylocke formaron un escuadrón clandestino de operaciones negras para cazar al clan Akkaba, descubriendo que un niño clon de En Sabah Nur estaba a punto de asumir el trono del exterminio evolutivo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "A pesar de que el escuadrón ejecutó al infante en una de las decisiones morales más crueles de los cómics, el destino fue inexorable: la semilla latente en Warren eclosionó por completo, transformándolo en el nuevo y temible Apocalipsis, un dios de la muerte dispuesto a reiniciar la Tierra."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Armado con alas metálicas afiladas como navajas capaces de disparar plumas envenenadas, Archangel lideró a sus nuevos Jinetes en una guerra sin tregua contra sus antiguos compañeros de equipo. ¿Crees que Archangel es el mutante con el destino más trágico? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La aclamada saga The Dark Angel Saga en Uncanny X-Force de Rick Remender y Jerome Opeña.",
        "hashtags": "#Archangel #XForce #Wolverine #Apocalypse #Psylocke #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 86,
        "queue_folder": "86_kraven_ultima_caceria_entierra_spiderman",
        "id": "kraven_ultima_caceria_entierra_spiderman",
        "title": "¡Kraven Disparó y Enterró Vivo a Spider-Man! La Obra Maestra Más Oscura de Marvel 🕷️🪦🌧️",
        "character": "Spider-Man & Kraven el Cazador",
        "folder": "86_kraven_ultima_caceria_entierra_spiderman",
        "theme_signature": "spiderman:kravens_last_hunt:buried_alive_graveyard_rain",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/86_kraven_ultima_caceria_entierra_spiderman/scene_03.jpg",
            "text": "¡ENTERRÓ A SPIDERMAN!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 100
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La historia más madura, oscura y aclamada en los sesenta años de cómics del Hombre Araña! En La Última Cacería de Kraven de J.M. DeMatteis, un Sergei Kravinoff anciano y acosado por la locura decide que su vida no tendrá honor hasta vencer definitivamente a su más grande y escurridiza presa."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con un sigilo escalofriante en una noche de tormenta torrencial, Kraven embosca a Peter Parker en los tejados de Nueva York y le dispara un dardo con un potentísimo tranquilizante médico que paraliza el sistema nervioso del héroe, dejándolo en un estado de coma idéntico a la muerte."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En lugar de asesinarlo con un cuchillo, Kraven introduce el cuerpo inerte de Spider-Man en un ataúd de madera y lo entierra bajo seis pies de tierra húmeda en un cementerio abandonado, celebrando un sombrío funeral mientras el barro sella para siempre la tumba de su enemigo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Kraven roba el traje negro arácnido para demostrar que él puede ser un Spider-Man superior y más letal, mientras Peter despierta en la asfixia total y lucha desesperadamente por cavar hacia la superficie. ¿Es esta la mejor novela gráfica de Spider-Man jamás escrita? ¡Comenta abajo tu opinión!"
            }
        ],
        "description": "La magistral novela gráfica Spider-Man: Kraven's Last Hunt (The Amazing Spider-Man #293-294).",
        "hashtags": "#SpiderMan #Kraven #KravensLastHunt #PeterParker #Marvel #MarvelComics #Comics #Shorts #Reels"
    }
]

def produce_project(proj: dict):
    slot = proj["slot"]
    queue_name = proj["queue_folder"]
    proj_id = proj["id"]

    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_video = dest_dir / "video.mp4"
    if dest_video.exists() and dest_video.stat().st_size > 5000000:
        existing_dur = get_duration(str(dest_video))
        if existing_dur >= 60.0:
            print(f"⏩ Slot {slot} ya completado en {queue_name} ({existing_dur:.2f}s). Omitiendo.")
            return dest_video

    print("\n" + "=" * 80)
    print(f"🎬 PROCESANDO SLOT {slot}: {proj['title']}")
    print("=" * 80)

    curated_dir = CURATED_BASE / proj["folder"]
    if not curated_dir.exists():
        print(f"❌ Error: Directorio curado no existe: {curated_dir}")
        return None

    scenes_text = []
    scene_art_urls = []
    for s in proj["scenes"]:
        sc_file = curated_dir / s["file"]
        if not sc_file.exists():
            print(f"❌ Falta archivo de escena: {sc_file}")
            return None
        scene_art_urls.append(str(sc_file.resolve()))
        scenes_text.append(s["text"])

    story_payload = dict(proj)
    story_payload["scenes"] = scenes_text
    story_payload["scene_art_urls"] = scene_art_urls

    proj_out_dir = PACK_OUTPUT_DIR / proj_id
    if proj_out_dir.exists():
        shutil.rmtree(proj_out_dir, ignore_errors=True)

    work_dir = PROJECT_ROOT / "work" / f"batch8_{proj_id}"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    generation = build_cloud_generation(story_payload, work_dir)
    voice_choice = proj.get("voice", "Puck")
    final_output_dir = PACK_OUTPUT_DIR / "finals"
    final_output_dir.mkdir(parents=True, exist_ok=True)

    final_video_path = run_pipeline(
        generation=generation,
        output_name=proj_id,
        voice=voice_choice,
        output_root=str(PACK_OUTPUT_DIR),
        width=1080,
        height=1920,
        final_video_dir=str(final_output_dir),
        generate_thumbnail=True
    )

    if not final_video_path or not Path(final_video_path).exists():
        print(f"❌ [ERROR] Falló la generación del video para {proj_id}")
        return None

    dur = get_duration(str(final_video_path))
    print(f"⏱️ Duración inicial: {dur:.2f}s")
    if dur < 60.0:
        print(f"🚨 FATAL: Duración {dur:.2f}s es menor a 60.0s!")
        return None

    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = dest_dir / "thumb.jpg"

    # 1. Renderizar miniatura minimalista (2 a 4 palabras, arte protagonista)
    min_cfg = proj["minimal_thumb"]
    art_path = PROJECT_ROOT / min_cfg["source_art"]
    render_minimal_text_thumb(
        image_path=art_path,
        text=min_cfg["text"],
        output_path=thumb_path,
        text_y=min_cfg.get("text_y", 240),
        text_color=min_cfg.get("color", (255, 235, 0)),
        font_size=min_cfg.get("font_size", 108)
    )

    # 2. Copiar video base al destino
    dest_video = dest_dir / "video.mp4"
    if dest_video.exists():
        dest_video.unlink()
    shutil.copy2(final_video_path, dest_video)

    # 3. Inyectar miniatura en frame 0
    inject_thumbnail_into_video(dest_video, thumb_path, queue_name)

    final_dur = get_duration(str(dest_video))
    print(f"✅ Video encolado: {dest_video} (Duración: {final_dur:.2f}s)")

    # 4. Guardar metadata.json para YouTube Shorts
    meta = {
        "slot": slot,
        "queue_folder": queue_name,
        "id": proj_id,
        "title": proj["title"],
        "character": proj["character"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "duration": final_dur,
        "video_file": "video.mp4",
        "thumbnail_file": "thumb.jpg",
        "produced_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(dest_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    return dest_video

def main():
    target_slot = None
    if len(sys.argv) > 1:
        target_slot = int(sys.argv[1])

    produced = []
    for proj in REMASTER_PROJECTS_BATCH_8:
        if target_slot is not None and proj["slot"] != target_slot:
            continue
        v = produce_project(proj)
        if v:
            produced.append(v)
        else:
            print(f"❌ Error en slot {proj['slot']}")

    print("\n" + "=" * 80)
    print(f"🎉 RESUMEN FINAL: {len(produced)} VIDEOS PRODUCIDOS CON ÉXITO")
    print("=" * 80)

if __name__ == "__main__":
    main()
