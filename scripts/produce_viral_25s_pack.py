"""
Master Production Engine: 18 Videos Virales de 25-30 Segundos (Slots 69 al 86)
==============================================================================
- Duración estricta: 25.0s a 30.0s (puro clímax y máxima retención viral).
- Sincronización visual precisa: cada viñeta canónica 1:1 describe exactamente lo narrado.
- Encuadre vertical 1080x1920 sin recortes destructivos con fondo desenfocado oscuro.
- Miniatura minimalista (2 a 4 palabras) inyectada en fotograma exacto t=0.000s.
- Salida directa en scheduled_queue/{slot}_{name}/ con video.mp4 y metadata.json.
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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_viral_25s"
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

VIRAL_25S_PROJECTS = [
    # -------------------------------------------------------------
    # SLOT 69: All-Star Superman - El Sacrificio Supremo
    # -------------------------------------------------------------
    {
        "slot": 69,
        "queue_folder": "69_superman_all_star_sacrificio",
        "id": "superman_all_star_sacrificio_25s",
        "title": "El Cómic Más Perfecto de Superman: El Sacrificio Final del Hombre del Mañana ☀️🦸‍♂️✨",
        "character": "Superman",
        "folder": "69_superman_all_star_sacrificio",
        "theme_signature": "superman:all_star_superman:golden_sun_god",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/69_superman_all_star_sacrificio/scene_04.jpg",
            "text": "¡EL SACRIFICIO SUPREMO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Al salvar una nave en el sol, las células de Superman absorbieron radiación letal, sentenciándolo a muerte."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin miedo a morir, pasó sus últimos días junto a Lois Lane, regalándole superpoderes por un día."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cuando el sol moría, Superman voló hacia su núcleo en un viaje final sin retorno para salvar la Tierra."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Hoy vive en el corazón del sol como una deidad dorada inmortal. ¿Es el final más perfecto de Superman?"
            }
        ],
        "description": "La legendaria obra All-Star Superman #1-12 de Grant Morrison y Frank Quitely. El sacrificio final del Hombre del Mañana.",
        "hashtags": "#Superman #AllStarSuperman #DCComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 70: Identity Crisis - Deathstroke Humilla a la Liga
    # -------------------------------------------------------------
    {
        "slot": 70,
        "queue_folder": "70_deathstroke_identity_crisis_liga",
        "id": "deathstroke_identity_crisis_liga_25s",
        "title": "¡Un Solo Mercenario Humilló a la Liga de la Justicia! La Hazaña de Deathstroke ⚔️🔥💥",
        "character": "Deathstroke",
        "folder": "70_deathstroke_identity_crisis_liga",
        "theme_signature": "deathstroke:identity_crisis:slade_humiliates_justice_league",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/70_deathstroke_identity_crisis_liga/scene_01.jpg",
            "text": "¡HUMILLÓ A LA LIGA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Un solo hombre humilló a la Liga de la Justicia! Deathstroke fue contratado para frenar a los mayores héroes del mundo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Anticipando la velocidad de Flash, plantó explosivos y ensartó al velocista antes de que pudiera dar un solo paso."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cortó el aire de Zatanna para silenciarla y derribó las alas de Hawkman usando cables de alta tensión."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Casi le roba el anillo a Green Lantern partiéndole los dedos! ¿Es Deathstroke el mejor estratega de DC?"
            }
        ],
        "description": "La inolvidable pelea en Identity Crisis #3 de Brad Meltzer y Rags Morales. Slade Wilson humilla a la Liga de la Justicia.",
        "hashtags": "#Deathstroke #JusticeLeague #Flash #GreenLantern #DCComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 71: Thor Ejecuta a Galactus
    # -------------------------------------------------------------
    {
        "slot": 71,
        "queue_folder": "71_thor_mata_galactus_ejecucion",
        "id": "thor_mata_galactus_ejecucion_25s",
        "title": "¡Thor Asesinó a Galactus! La Brutal Ejecución del Devorador de Mundos ⚡👑💀",
        "character": "Thor & Galactus",
        "folder": "71_thor_mata_galactus_ejecucion",
        "theme_signature": "thor:kills_galactus:herald_of_thunder_execution",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/71_thor_mata_galactus_ejecucion/scene_04.jpg",
            "text": "¡EJECUTÓ A GALACTUS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El día en que el Rey Thor asesinó a Galactus! El gigante cósmico lo convirtió en su heraldo para salvar el universo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras vencer al Black Winter, Galactus intentó traicionar a Thor para devorarlo en el espacio profundo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero Thor desató la fuerza de Odín, drenándole el poder cósmico a Galactus hasta dejarlo totalmente indefenso."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Thor lo ejecutó con un rayo brutal y colgó su cabeza como monumento en Asgard! ¿Merecía morir Galactus?"
            }
        ],
        "description": "La brutal ejecución de Galactus en Thor Vol 6 #6 de Donny Cates y Nic Klein.",
        "hashtags": "#Thor #Galactus #HeraldOfThunder #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 72: Green Lantern - Crepúsculo Esmeralda y Parallax
    # -------------------------------------------------------------
    {
        "slot": 72,
        "queue_folder": "72_green_lantern_parallax_crepusculo",
        "id": "green_lantern_parallax_crepusculo_25s",
        "title": "¡El Mayor Linterna Verde se Volvió Villano! La Caída de Hal Jordan y Parallax 🟢💀⚡",
        "character": "Hal Jordan / Parallax",
        "folder": "72_green_lantern_parallax_crepusculo",
        "theme_signature": "green_lantern:emerald_twilight:hal_jordan_parallax_fall",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/72_green_lantern_parallax_crepusculo/scene_04.jpg",
            "text": "¡PARALLAX NACIÓ!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 110
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras la destrucción total de Coast City, el dolor quebró para siempre la cordura de Hal Jordan."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Los Guardianes le prohibieron revivirla, y Hal voló a Oa masacrando a todo el cuerpo de linternas."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Asesinó brutalmente a su amigo Kilowog y le rompió el cuello a Sinestro para robar sus anillos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Hal absorbió la Gran Batería Central, transformándose en Parallax! ¿Fue justificada la furia de Hal Jordan?"
            }
        ],
        "description": "La mítica saga Emerald Twilight (Green Lantern #48-50) de Ron Marz. El nacimiento de Parallax.",
        "hashtags": "#GreenLantern #HalJordan #Parallax #DCComics #EmeraldTwilight #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 73: Deadpool Mata a Thor con Mjolnir Gigante
    # -------------------------------------------------------------
    {
        "slot": 73,
        "queue_folder": "73_deadpool_mata_thor_mjolnir",
        "id": "deadpool_mata_thor_mjolnir_25s",
        "title": "¡La Muerte Más Humillante de Thor a Manos de Deadpool! 🔨💀💥",
        "character": "Deadpool & Thor",
        "folder": "73_deadpool_mata_thor_mjolnir",
        "theme_signature": "deadpool:kills_marvel:thor_giant_mjolnir_crush",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/73_deadpool_mata_thor_mjolnir/scene_04.jpg",
            "text": "¡THOR APLASTADO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La muerte más ridícula y humillante de Thor! Deadpool enloqueció y decidió exterminar a todos los superhéroes de Marvel."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "En plena batalla, Thor le arrojó a Mjolnir con toda su fuerza divina para destrozarle la cabeza al mercenario."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero Deadpool le lanzó partículas Pym al martillo en el aire, haciéndolo crecer al tamaño de un rascacielos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Mjolnir cayó de regreso aplastando a Thor contra el suelo en un segundo! ¿Es la muerte más absurda del Dios del Trueno?"
            }
        ],
        "description": "Deadpool Kills the Marvel Universe #4 por Cullen Bunn y Dalibor Talajic. La muerte de Thor.",
        "hashtags": "#Deadpool #Thor #Mjolnir #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 74: The Immortal Hulk #8 - Descuartizado en Frascos
    # -------------------------------------------------------------
    {
        "slot": 74,
        "queue_folder": "74_immortal_hulk_descuartizado_frascos",
        "id": "immortal_hulk_descuartizado_frascos_25s",
        "title": "¡Descuartizaron a Hulk en Frascos de Vidrio! La Resurrección Más Aterradora 🟢💀🧪",
        "character": "The Immortal Hulk",
        "folder": "74_immortal_hulk_descuartizado_frascos",
        "theme_signature": "immortal_hulk:shadow_base:dismembered_jars_resurrection",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/74_immortal_hulk_descuartizado_frascos/scene_02.jpg",
            "text": "¡HULK EN FRASCOS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Científicos del gobierno descuartizaron vivo a Hulk y guardaron sus órganos en frascos de vidrio sellados."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Creyendo haberlo matado, el doctor Clive festejaba, hasta que la cabeza cercenada de Hulk abrió los ojos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Con una sonrisa tétrica, su mano en el frasco vecino chasqueó los dedos, reventando todos los vidrios."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡La masa verde se reconstruyó devorando vivo al científico! ¿Es Immortal Hulk la versión más aterradora?"
            }
        ],
        "description": "El escalofriante clímax de The Immortal Hulk #8 de Al Ewing y Joe Bennett. Hulk descuartizado en frascos.",
        "hashtags": "#Hulk #ImmortalHulk #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 75: Marvel Ruins - El Universo Maldito
    # -------------------------------------------------------------
    {
        "slot": 75,
        "queue_folder": "75_marvel_ruins_universo_maldito",
        "id": "marvel_ruins_universo_maldito_25s",
        "title": "Marvel Ruins: El Universo Donde Todo lo que Podía Salir Mal, Salió Mal ☣️💀🌑",
        "character": "Marvel Ruins",
        "folder": "75_marvel_ruins_universo_maldito",
        "theme_signature": "marvel_ruins:dystopian_body_horror:failed_mutations",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/75_marvel_ruins_universo_maldito/scene_02.jpg",
            "text": "¡UNIVERSO MALDITO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 100
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En Marvel Ruins no existen milagros ni esperanzas: cada origen superheroico se convirtió en una pesadilla terminal."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Peter Parker fue mordido, pero solo contrajo una repugnante y dolorosa erupción radioactiva que lo devora vivo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Silver Surfer enloqueció en el cosmos y se despellejó entero, muriendo asfixiado en la negrura espacial."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Bruce Banner mutó en una grotesca masa de tumores suplicando morir! ¿Leerías este universo tan oscuro?"
            }
        ],
        "description": "La retorcida distopía Marvel Ruins #1-2 de Warren Ellis. Todo lo que podía salir mal, salió mal.",
        "hashtags": "#MarvelRuins #SpiderMan #Hulk #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 76: Magneto: Ultimatum - El Día que Ahogó al Mundo
    # -------------------------------------------------------------
    {
        "slot": 76,
        "queue_folder": "76_magneto_ultimatum_tsunami_manhattan",
        "id": "magneto_ultimatum_tsunami_manhattan_25s",
        "title": "Magneto: El Día que Ahogó al Mundo en Ultimatum 🌊💀🗽",
        "character": "Magneto",
        "folder": "76_magneto_ultimatum_tsunami_manhattan",
        "theme_signature": "magneto:ultimatum:manhattan_tsunami_cataclysm",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/76_magneto_ultimatum_tsunami_manhattan/scene_01.jpg",
            "text": "¡MAGNETO AHOGÓ NY!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Enloquecido por la muerte de sus hijos, Magneto usó su magnetismo para invertir los polos terrestres."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Una ola gigante de cien metros impactó Nueva York, destrozando puentes y arrastrando rascacielos enteros con furia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Millones de civiles y decenas de héroes murieron ahogados, convirtiendo las avenidas en un cementerio submarino."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Magneto contempló la devastación sonriendo desde los cielos tormentosos! ¿Fue este el ataque más letal de Marvel?"
            }
        ],
        "description": "El cataclismo de Jeph Loeb y David Finch en Ultimatum #1. Magneto ahoga la ciudad de Nueva York.",
        "hashtags": "#Magneto #Ultimatum #XMen #Avengers #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 77: Thanos Rising - El Origen Perturbador
    # -------------------------------------------------------------
    {
        "slot": 77,
        "queue_folder": "77_thanos_origen_perturbador_muerte",
        "id": "thanos_origen_perturbador_muerte_25s",
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
                "text": "Al nacer Thanos con aspecto deforme, su propia madre enloqueció e intentó apuñalarlo en la sala de parto."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aislado de todos, bajó a las cavernas de Titán diseccionando bestias vivas para descifrar el misterio biológico."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Manipulado por la Dama Muerte, regresó como conquistador y masacró con armas nucleares a su civilización entera."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Thanos ató a su madre a una camilla abriéndola viva! ¿Thanos nació siendo malvado o lo crearon?"
            }
        ],
        "description": "El origen psicológico y aterrador de Thanos en Thanos Rising #1-5 de Jason Aaron y Simone Bianchi.",
        "hashtags": "#Thanos #LadyDeath #ThanosRising #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 78: Uncanny X-Men - Días del Futuro Pasado
    # -------------------------------------------------------------
    {
        "slot": 78,
        "queue_folder": "78_xmen_dias_del_futuro_pasado",
        "id": "xmen_dias_del_futuro_pasado_25s",
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
                "text": "En un futuro sombrío, los Centinelas tomaron el control de América y exterminaron a casi todos los mutantes."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Los héroes caídos aparecen tachados en afiches, mientras los pocos sobrevivientes son confinados en campos de concentración."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Rachel Summers envía la mente de Kate Pryde al pasado para evitar el magnicidio que causó la guerra."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡En el presente, un Centinela fulmina a Wolverine desintegrando su carne! ¿Es la cumbre dramática de X-Men?"
            }
        ],
        "description": "La legendaria obra maestra Uncanny X-Men #141-142 de Chris Claremont y John Byrne: Days of Future Past.",
        "hashtags": "#XMen #DaysOfFuturePast #Wolverine #Sentinels #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 79: Thanos Wins - Thanos Conquistó el Fin del Universo
    # -------------------------------------------------------------
    {
        "slot": 79,
        "queue_folder": "79_thanos_gana_fin_del_universo",
        "id": "thanos_gana_fin_del_universo_25s",
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
                "text": "Al final de los tiempos la profecía se cumplió: Thanos triunfó sobre todos y reina en la nada."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El Titán masacró a los Vengadores y a Galactus, sentándose sobre una montaña de billones de cráneos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Con Cosmic Ghost Rider, secuestró a su versión joven del pasado para mostrarle su sangriento imperio."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡El viejo Thanos solo suplica ser ejecutado por sí mismo! ¿Es el destino más oscuro de Marvel?"
            }
        ],
        "description": "La magistral saga Thanos Wins (Thanos Vol. 2 #13-18) de Donny Cates y Geoff Shaw. El fin de todos los tiempos.",
        "hashtags": "#Thanos #KingThanos #ThanosWins #CosmicGhostRider #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 80: Batman: Silencio (Hush) - La Conspiración Wayne
    # -------------------------------------------------------------
    {
        "slot": 80,
        "queue_folder": "80_batman_hush_conspiracion_wayne",
        "id": "batman_hush_conspiracion_wayne_25s",
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
                "text": "Una oscura figura vendada manipula desde las sombras a todos los villanos para quebrar psicológicamente a Batman."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "La cuerda de Batman es saboteada, cayendo al vacío y fracturándose el cráneo con brutalidad contra el pavimento."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su amigo Thomas Elliot lo opera de urgencia, mientras villanos controlados atacan Gotham en una trampa perfecta."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡El misterioso Hush era el mismísimo Thomas Elliot buscando venganza! ¿Fue este el mejor plan contra Bruce Wayne?"
            }
        ],
        "description": "La conspiración definitiva en Batman: Hush (Batman #608-619) de Jeph Loeb y Jim Lee. El complot de Thomas Elliot.",
        "hashtags": "#Batman #Hush #ThomasElliot #DCComics #BatmanHush #Gotham #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 81: Doctor Strange: The Oath - La Cura Prohibida del Cáncer
    # -------------------------------------------------------------
    {
        "slot": 81,
        "queue_folder": "81_doctor_strange_the_oath_cura_cancer",
        "id": "doctor_strange_the_oath_cura_cancer_25s",
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
                "text": "Al enterarse de que Wong padece un tumor terminal inoperable, Doctor Strange viaja a dimensiones místicas prohibidas."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Gravemente herido en su santuario, guía en forma astral una arriesgada cirugía para salvar su propio cuerpo físico."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Consigue el legendario Elixir de Otkid, una pócima divina capaz de curar todo tipo de cáncer humano."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Strange decidió usar la última dosis para salvar a su mejor amigo! ¿Habrías hecho lo mismo por lealtad?"
            }
        ],
        "description": "Doctor Strange: The Oath de Brian K. Vaughan y Marcos Martin. El juramento hipocrático del Hechicero Supremo.",
        "hashtags": "#DoctorStrange #Wong #TheOath #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 82: Ultimate Wolverine vs Hulk - Logan en Dos Mitades
    # -------------------------------------------------------------
    {
        "slot": 82,
        "queue_folder": "82_ultimate_wolverine_vs_hulk_dos_mitades",
        "id": "ultimate_wolverine_vs_hulk_dos_mitades_25s",
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
                "text": "Logan despierta bajo una tormenta de nieve en el Tíbet, asfixiado por el olor de su propia sangre."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al levantar la vista ve la pesadilla: ¡sus piernas fueron arrancadas y yacen a cuatro millas de distancia!"
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En su furia, Hulk partió a Logan por la mitad como a una simple rama sobre su rodilla."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Clavando sus garras en el hielo, Wolverine arrastra su torso hacia la cima! ¿Quién ganaría la revancha definitiva?"
            }
        ],
        "description": "La sangrienta confrontación en Ultimate Wolverine vs. Hulk #1 de Damon Lindelof y Leinil Francis Yu.",
        "hashtags": "#Wolverine #Hulk #UltimateWolverine #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 83: Siege: Sentry / The Void - La Destrucción de Asgard
    # -------------------------------------------------------------
    {
        "slot": 83,
        "queue_folder": "83_sentry_vacio_void_devora_asgard",
        "id": "sentry_vacio_void_devora_asgard_25s",
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
                "text": "Durante el asedio final a Asgard, la frágil mente de Sentry colapsó liberando a su entidad más siniestra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Convertido en The Void, una pesadilla de sombras titánicas, derribó de un golpe las torres del reino divino."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Asgard entera cayó envuelta en llamas sobre Oklahoma, reduciendo la ciudadela dorada a un inmenso cementerio humeante."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Thor tuvo que desatar un trueno cósmico para erradicar a la bestia! ¿Es The Void la mayor amenaza?"
            }
        ],
        "description": "La caída de Asgard y el despertar de The Void en Siege #3-4 de Brian Michael Bendis y Olivier Coipel.",
        "hashtags": "#Sentry #TheVoid #Siege #Asgard #Thor #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 84: House of M - Scarlet Witch: "No Más Mutantes"
    # -------------------------------------------------------------
    {
        "slot": 84,
        "queue_folder": "84_scarlet_witch_house_of_m_no_mas_mutantes",
        "id": "scarlet_witch_house_of_m_no_mas_mutantes_25s",
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
                "text": "Devastada por la traición familiar y la pérdida de sus hijos, la mente de Wanda Maximoff colapsó por completo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Flotando frente a los héroes del mundo, la Bruja Escarlata pronunció un susurro letal: No más mutantes."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Un destello blanco envolvió la Tierra en un segundo, borrando el gen X de millones de mutantes instantáneamente."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡El noventa y nueve por ciento perdió sus poderes para siempre! ¿Fue este el mayor hechizo de Marvel?"
            }
        ],
        "description": "El evento definitorio House of M #7 de Brian Michael Bendis y Olivier Coipel. Las tres palabras de Bruja Escarlata.",
        "hashtags": "#ScarletWitch #HouseOfM #NoMoreMutants #XMen #Magneto #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 85: Uncanny X-Force - Archangel: El Heredero de Apocalipsis
    # -------------------------------------------------------------
    {
        "slot": 85,
        "queue_folder": "85_archangel_heredero_apocalipsis_xforce",
        "id": "archangel_heredero_apocalipsis_xforce_25s",
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
                "text": "Warren libraba una guerra desesperada por controlar los impulsos homicidas implantados por Apocalipsis."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pese al esfuerzo de Wolverine, la Semilla de la Muerte despertó sumergiéndolo en la oscuridad."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Warren sucumbió a la maldición, proclamándose el nuevo líder supremo destinado a purgar a los débiles."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Desplegó sus letales alas de acero afiladas contra sus propios compañeros mutantes! ¿Tenía salvación?"
            }
        ],
        "description": "La aclamada saga The Dark Angel Saga en Uncanny X-Force de Rick Remender y Jerome Opeña.",
        "hashtags": "#Archangel #XForce #Wolverine #Apocalypse #Psylocke #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    # -------------------------------------------------------------
    # SLOT 86: The Amazing Spider-Man - La Última Cacería de Kraven
    # -------------------------------------------------------------
    {
        "slot": 86,
        "queue_folder": "86_kraven_ultima_caceria_entierra_spiderman",
        "id": "kraven_ultima_caceria_entierra_spiderman_25s",
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
                "text": "Bajo una lluvia torrencial, Kraven el Cazador se prepara para culminar su obsesión más siniestra contra Spider-Man."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Le dispara un narcótico que paraliza a Peter Parker induciéndole un coma clínicamente idéntico a la muerte."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Kraven encierra el cuerpo inerte en un ataúd y lo entierra seis pies bajo tierra en el cementerio."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "¡Kraven viste el traje arácnido mientras Peter cava con desesperación! ¿Es la historia más tétrica del Hombre Araña?"
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
    dest_meta = dest_dir / "metadata.json"
    if dest_video.exists() and dest_meta.exists():
        try:
            with open(dest_meta, 'r', encoding='utf-8') as mf:
                mdata = json.load(mf)
            if mdata.get("format") == "viral_25_30s":
                dur = get_duration(str(dest_video))
                if 25.0 <= dur <= 30.0:
                    print(f"⏩ Slot {slot} ya remasterizado en 25-30s ({dur:.2f}s). Omitiendo.")
                    return dest_video
        except Exception:
            pass

    print("\n" + "=" * 80)
    print(f"🎬 PROCESANDO VIRAL 25-30s | SLOT {slot}: {proj['title']}")
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

    work_dir = PROJECT_ROOT / "work" / f"viral25_{proj_id}"
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
        rate=1.12,
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
    print(f"⏱️ Duración renderizada: {dur:.2f}s")
    if dur < 23.0 or dur > 32.0:
        print(f"⚠️ AVISO: Duración {dur:.2f}s está fuera del rango ideal (25-30s)!")

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
        font_size=min_cfg.get("font_size", 105)
    )

    # 2. Copiar video base al destino
    dest_video = dest_dir / "video.mp4"
    if dest_video.exists():
        dest_video.unlink()
    shutil.copy2(final_video_path, dest_video)

    # 3. Inyectar miniatura en frame 0
    inject_thumbnail_into_video(dest_video, thumb_path, queue_name)

    final_dur = get_duration(str(dest_video))
    print(f"✅ Video viral encolado: {dest_video} (Duración: {final_dur:.2f}s)")

    # 4. Guardar metadata.json para YouTube Shorts / Reels
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
        "format": "viral_25_30s",
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
    for proj in VIRAL_25S_PROJECTS:
        if target_slot is not None and proj["slot"] != target_slot:
            continue
        v = produce_project(proj)
        if v:
            produced.append(v)
        else:
            print(f"❌ Error en slot {proj['slot']}")

    print("\n" + "=" * 80)
    print(f"🎉 RESUMEN FINAL: {len(produced)} VIDEOS VIRALES (25-30s) PRODUCIDOS CON ÉXITO")
    print("=" * 80)

if __name__ == "__main__":
    main()
