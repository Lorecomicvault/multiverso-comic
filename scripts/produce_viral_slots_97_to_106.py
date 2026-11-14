"""
Master Production Engine: Lote 10 Videos Virales (Slots 97 al 106)
Formato de Alta Retención Viral: 25 a 30 Segundos
=============================================================================
Historias de Máximo Impacto y Audiencia Masiva:
  - Slot 97: Lobo: Expulsado del Cielo y el Infierno (61_lobo_expulsado_cielo_infierno)
  - Slot 98: World War Hulk: La Venganza de Sakaar (62_hulk_world_war_venganza_illuminati)
  - Slot 99: Azrael Batman destroza a Bane con cuchillas y fuego (63_azrael_batman_destroza_bane)
  - Slot 100: Plastic Man: El Terror Oculto de Batman (64_plastic_man_pesadilla_batman)
  - Slot 101: Venom Dios de la Luz vs Knull (65_venom_dios_de_la_luz_knull)
  - Slot 102: Invincible vs Conquest: Asalto Brutal Sangre (invincible_conquest_asalto_brutal_sangre)
  - Slot 103: Old Man Logan desgarra el estómago de Hulk (old_man_logan_estomago_hulk)
  - Slot 104: Doomsday humilla a Darkseid en Apokolips (doomsday_humilla_darkseid_apokolips)
  - Slot 105: Under the Red Hood: El Ultimátum de Jason Todd (batman_under_red_hood)
  - Slot 106: Batman: Bane quiebra la espalda de Bruce Wayne (26_batman_quiebra_espalda_bane_arkham)

- Duración estricta: 25.0s a 30.0s (narraciones calibradas a 58-61 palabras, rate=0.97).
- Sincronización visual 1:1 viñeta-narración con viñetas canónicas curadas en HD.
- Safe zone vertical 1080x1920 con fondo desenfocado protector sin recorte destructivo.
- Miniatura minimalista (2 a 4 palabras) inyectada en fotograma exacto t=0.000s.
- Encolado directo en scheduled_queue/{slot}_{name}/.
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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch10_viral_25s"
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


SLOTS_97_TO_106_PROJECTS = [
    # -------------------------------------------------------------
    # SLOT 97: Lobo - Expulsado del Cielo y el Infierno
    # -------------------------------------------------------------
    {
        "slot": 97,
        "queue_folder": "97_lobo_expulsado_cielo_infierno",
        "id": "lobo_expulsado_cielo_infierno_25s",
        "title": "¡Expulsado del Cielo y el Infierno! El Hombre que Rompió la Muerte 💀🚀🍺",
        "character": "Lobo",
        "folder": "61_lobo_expulsado_cielo_infierno",
        "theme_signature": "lobo:the_last_czarnian:banned_from_death_immortal",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/61_lobo_expulsado_cielo_infierno/scene_03.jpg",
            "text": "¡EXPULSADO DE LA MUERTE!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En el planeta Czarnia nació Lobo, un asesino despiadado que exterminó a toda su civilización."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Como el cazarrecompensas más temido del cosmos, recorrió el universo destrozando a cuanto rival encontró."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al morir, su alma llegó al Cielo, donde masacró a los ángeles en una fiesta caótica."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Aterrados, Dios y el Diablo firmaron un pacto expulsándolo del más allá para volverlo inmortal."
            }
        ],
        "description": "La legendaria mitología de Alan Grant, Keith Giffen y Simon Bisley en The Last Czarnian y Lobo's Back. La inmortalidad eterna de Lobo.",
        "hashtags": "#Lobo #TheMainMan #Czarnia #SimonBisley #DCComics #Inmortal #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 98: World War Hulk - La Venganza de Sakaar
    # -------------------------------------------------------------
    {
        "slot": 98,
        "queue_folder": "98_hulk_world_war_venganza_illuminati",
        "id": "hulk_world_war_venganza_illuminati_25s",
        "title": "¡Hulk Aplasta a los Illuminati! La Implacable Venganza de Sakaar 🟢⚔️💥",
        "character": "Hulk",
        "folder": "62_hulk_world_war_venganza_illuminati",
        "theme_signature": "hulk:world_war_hulk:green_scar_revenge",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/62_hulk_world_war_venganza_illuminati/scene_02.jpg",
            "text": "¡HULK APLASTA A TODOS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Los Illuminati engañaron a Hulk, exiliándolo en una nave espacial rumbo a un planeta desolado."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras forjar su reinado en Sakaar, una explosión asesinó a su esposa, desatando su ira."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Hulk regresó a la Tierra con armadura de gladiador, destrozando a cada héroe que encontró."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Obligó a sus antiguos amigos a pelear como esclavos en un coliseo en Manhattan."
            }
        ],
        "description": "La aclamada saga de Greg Pak y John Romita Jr en World War Hulk. La venganza del Green Scar contra los Illuminati.",
        "hashtags": "#WorldWarHulk #Hulk #Illuminati #IronMan #DoctorStrange #Marvel #MarvelComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 99: Azrael Batman destroza a Bane
    # -------------------------------------------------------------
    {
        "slot": 99,
        "queue_folder": "99_azrael_batman_destroza_bane",
        "id": "azrael_batman_destroza_bane_25s",
        "title": "¡El Batman Dorado de Azrael! Destrozó a Bane con Cuchillas y Fuego 🦇🩸⚙️",
        "character": "Azrael",
        "folder": "63_azrael_batman_destroza_bane",
        "theme_signature": "azrael:knightfall_19:destroys_bane_venom",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/63_azrael_batman_destroza_bane/scene_03.jpg",
            "text": "¡DESTROZÓ A BANE!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras quebrar la columna a Bruce Wayne, Bane se proclamó el dueño absoluto de todo Gotham."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero Jean-Paul Valley asumió el manto de Batman, construyendo una armadura letal con cuchillas de acero."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Azrael emboscó al villano en una fábrica, rebanando con precisión sus conductos de Venom."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Sin su droga, Bane colapsó destrozado en el asfalto, rogando piedad ante el murciélago."
            }
        ],
        "description": "El brutal enfrentamiento en Knightfall #19 de Chuck Dixon y Graham Nolan. Azrael pulveriza a Bane.",
        "hashtags": "#Azrael #Batman #Bane #Knightfall #JeanPaulValley #DCComics #Gotham #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 100: Plastic Man - El Terror Oculto de Batman
    # -------------------------------------------------------------
    {
        "slot": 100,
        "queue_folder": "100_plastic_man_pesadilla_batman",
        "id": "plastic_man_pesadilla_batman_25s",
        "title": "Plastic Man: El Arma Secreta y el Verdadero Terror de Batman 🔴⚡🧬",
        "character": "Plastic Man",
        "folder": "64_plastic_man_pesadilla_batman",
        "theme_signature": "plastic_man:tower_of_babel:batman_secret_fear",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/64_plastic_man_pesadilla_batman/scene_04.jpg",
            "text": "¡EL TERROR DE BATMAN!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Todos los héroes creían que Plastic Man era un simple bromista inofensivo de la Liga."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin embargo, en los archivos secretos de Batman, fue catalogado como la mayor amenaza biológica."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sus moléculas fluidas son inmortales; sobrevivió miles de años congelado y fragmentado en el fondo marino."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Batman confesó que Plastic Man podría introducirse en los órganos de cualquiera y destruirlo."
            }
        ],
        "description": "La revelación de Mark Waid y Howard Porter en JLA: Tower of Babel. El poder ilimitado e inmortal de Plastic Man.",
        "hashtags": "#PlasticMan #Batman #JusticeLeague #TowerOfBabel #DCComics #JLA #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 101: Venom Dios de la Luz vs Knull
    # -------------------------------------------------------------
    {
        "slot": 101,
        "queue_folder": "101_venom_dios_de_la_luz_knull",
        "id": "venom_dios_de_la_luz_knull_25s",
        "title": "¡El Hacha de Luz Cósmica! Eddie Brock Aniquila a Knull en el Sol ⚡🪓🌌",
        "character": "Venom",
        "folder": "65_venom_dios_de_la_luz_knull",
        "theme_signature": "venom:king_in_black_5:god_of_light_kills_knull",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/65_venom_dios_de_la_luz_knull/scene_04.jpg",
            "text": "¡VENOM DIOS DE LA LUZ!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Knull, el Dios de la Oscuridad, invadió la Tierra cubriendo el cielo de sombras tenebrosas."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con los Vengadores derrotados y Eddie Brock muerto, el abismo parecía haber ganado todo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero la Fuerza Enigma cósmica despertó, resucitando a Eddie Brock como el Dios de la Luz."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Forjando un hacha estelar, Eddie arrastró a Knull al Sol, desintegrándolo para siempre en llamas."
            }
        ],
        "description": "La apoteósica batalla final en King in Black #5 de Donny Cates y Ryan Stegman. Venom Dios de la Luz aniquila a Knull.",
        "hashtags": "#Venom #KingInBlack #EddieBrock #Knull #Marvel #MarvelComics #Symbiote #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 102: Invincible vs Conquest - Asalto Brutal
    # -------------------------------------------------------------
    {
        "slot": 102,
        "queue_folder": "102_invincible_conquest_asalto_brutal_sangre",
        "id": "invincible_conquest_asalto_brutal_sangre_25s",
        "title": "¡La Masacre de Conquest! La Pelea Más Despiadada de Invincible 💥🩸👊",
        "character": "Invincible",
        "folder": "invincible_conquest_asalto_brutal_sangre",
        "theme_signature": "invincible:conquest:pelea_viltrumita_craneo_sangre_atomo_eve",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/invincible_conquest_asalto_brutal_sangre/scene_04.jpg",
            "text": "¡DESTROZÓ SU CRÁNEO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "El despiadado guerrero viltrumita Conquest llegó a la Tierra exigiendo la rendición total del planeta."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Mark Grayson se negó rotundamente a arrodillarse, desatando una batalla colosal en el cielo terrestre."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cuando Conquest hirió de muerte a Atom Eve, Mark perdió por completo el control."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con una furia ciega, Invincible molió a Conquest a cabezazos demoledores hasta destrozarle el cráneo."
            }
        ],
        "description": "El choque más sangriento en Invincible #61-64 de Robert Kirkman y Ryan Ottley. Mark Grayson destroza a Conquest.",
        "hashtags": "#Invincible #Conquest #Viltrumite #MarkGrayson #ImageComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 103: Old Man Logan desgarra el estómago de Hulk
    # -------------------------------------------------------------
    {
        "slot": 103,
        "queue_folder": "103_old_man_logan_estomago_hulk",
        "id": "old_man_logan_estomago_hulk_25s",
        "title": "¡Logan Desgarró a Hulk desde Adentro! El Fin del Tirano Caníbal 🥩🩸🐺",
        "character": "Wolverine",
        "folder": "old_man_logan_estomago_hulk",
        "theme_signature": "logan_anciano:coloso_canibal:regeneracion_tripas:caida_tirano_california",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/old_man_logan_estomago_hulk/scene_04.jpg",
            "text": "¡DESGARRÓ SU ESTÓMAGO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 90
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En un futuro desolado, un envejecido Logan desenfundó sus garras para vengar a su familia."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al llegar a la fortaleza, un Bruce Banner caníbal desató la furia de su bestia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Confiado en su poder descomunal, Hulk devoró a Wolverine de un solo bocado sangriento."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Pero Logan se regeneró en sus entrañas, desgarrando el vientre del monstruo desde adentro."
            }
        ],
        "description": "El sangriento clímax de Mark Millar y Steve McNiven en Wolverine: Old Man Logan. Logan mata a Bruce Banner.",
        "hashtags": "#Wolverine #OldManLogan #Hulk #Marvel #MarvelComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 104: Doomsday humilla a Darkseid en Apokolips
    # -------------------------------------------------------------
    {
        "slot": 104,
        "queue_folder": "104_doomsday_humilla_darkseid_apokolips",
        "id": "doomsday_humilla_darkseid_apokolips_25s",
        "title": "¡Doomsday Destrozó a Darkseid en Apokolips! La Humillación del Tirano 💀🔥💥",
        "character": "Doomsday",
        "folder": "doomsday_humilla_darkseid_apokolips",
        "theme_signature": "doomsday:destrozo_darkseid:apokolips_invasion:rayos_omega_inutiles",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/doomsday_humilla_darkseid_apokolips/scene_03.jpg",
            "text": "¡HUMILLÓ A DARKSEID!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Al escapar al espacio, el monstruo Doomsday aterrizó en el ardiente planeta de Apokolips."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Confiado en su divinidad suprema, Darkseid le disparó sus infalibles Rayos Omega para desintegrarlo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero Doomsday resistió el impacto sin rasguños, quebrando los brazos del tirano a golpes."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Dejó al gobernante del mal ensangrentado e impotente, demostrando que nada en el cosmos puede frenarlo."
            }
        ],
        "description": "La brutal humillación de Dan Jurgens y Brett Breeding en Superman/Doomsday: Hunter/Prey. Doomsday quiebra a Darkseid.",
        "hashtags": "#Doomsday #Darkseid #Superman #Apokolips #DCComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 105: Under the Red Hood - El Ultimátum de Jason Todd
    # -------------------------------------------------------------
    {
        "slot": 105,
        "queue_folder": "105_batman_under_red_hood",
        "id": "batman_under_red_hood_25s",
        "title": "¡El Ultimátum de Red Hood! Jason Todd Confronta a Batman y al Joker 🔴🔫🦇",
        "character": "Red Hood",
        "folder": "batman_under_red_hood",
        "theme_signature": "red_hood:under_the_red_hood:jason_ultimatum_joker_batman",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/batman_under_red_hood/scene_03.jpg",
            "text": "¡EL ULTIMÁTUM DE RED HOOD!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 84
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Resucitado de entre los muertos por el Pozo de Lázaro, Jason Todd regresó a Gotham como Red Hood."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Recordando cómo el Joker le arrebató la vida a golpes de palanca, confrontó a Batman furioso."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Ató al payaso en una silla y le apuntó con una pistola cargada frente a su antiguo mentor."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Jason le dio un ultimátum definitivo a Bruce Wayne: matarlo a él o permitir ejecutar al Joker."
            }
        ],
        "description": "El doloroso desenlace de Judd Winick y Doug Mahnke en Batman: Under the Red Hood. El ultimátum de Jason Todd.",
        "hashtags": "#RedHood #JasonTodd #Batman #Joker #UnderTheRedHood #DCComics #Gotham #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # SLOT 106: Batman - Bane quiebra la espalda de Bruce Wayne
    # -------------------------------------------------------------
    {
        "slot": 106,
        "queue_folder": "106_batman_quiebra_espalda_bane_arkham",
        "id": "batman_quiebra_espalda_bane_arkham_25s",
        "title": "¡La Caída del Murciélago! El Día que Bane Quebró la Espalda de Batman 🦇🦴💥",
        "character": "Batman",
        "folder": "26_batman_quiebra_espalda_bane_arkham",
        "theme_signature": "batman:knightfall:bane_breaks_batman_spine",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/26_batman_quiebra_espalda_bane_arkham/scene_04.jpg",
            "text": "¡LE QUEBRÓ LA ESPALDA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Para destruir a Batman, Bane liberó a todos los psicópatas del Manicomio de Arkham."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras semanas de lucha incesante, un Bruce Wayne agotado regresó a solas a su mansión."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Bane lo esperaba en las sombras, emboscándolo y levantándolo en vilo con fuerza sobrehumana."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El coloso estrelló la columna de Batman contra su rodilla, quebrando el símbolo de Gotham."
            }
        ],
        "description": "El momento más icónico de Chuck Dixon, Jim Aparo y Norm Breyfogle en Batman #497 (Knightfall). Bane rompe a Batman.",
        "hashtags": "#Batman #Bane #Knightfall #BruceWayne #DCComics #Gotham #Comics #Shorts #Reels"
    }
]

def produce_project(proj: dict):
    proj_id = proj["id"]
    slot = proj["slot"]
    queue_name = proj["queue_folder"]

    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_video = dest_dir / "video.mp4"
    if dest_video.exists():
        try:
            dur = get_duration(str(dest_video))
            if 25.0 <= dur <= 30.0:
                print(f"⏩ [SALTAR] Slot {slot} ({queue_name}) ya existe y es perfecto: {dur:.2f}s")
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

    work_dir = PROJECT_ROOT / "work" / f"batch10_viral_{proj_id}"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    generation = build_cloud_generation(story_payload, work_dir)

    # Formatear cada escena a vertical 1080x1920 con fondo desenfocado
    gen_dir = work_dir / proj_id
    for idx in range(1, len(scenes_text) + 1):
        sc_img = gen_dir / f"scene_{idx:02d}" / f"scene_{idx:02d}.jpg"
        if sc_img.exists():
            raw_im = Image.open(sc_img).convert("RGB")
            if raw_im.size != (1080, 1920):
                formatted_im = fit_to_vertical(raw_im, 1080, 1920)
                formatted_im.save(sc_img, "JPEG", quality=95)
                print(f"  [CANVAS 1080x1920 OK] scene_{idx:02d}.jpg")

    voice_choice = proj.get("voice", "es-MX-JorgeNeural")
    final_output_dir = PACK_OUTPUT_DIR / "finals"
    final_output_dir.mkdir(parents=True, exist_ok=True)

    final_video_path = run_pipeline(
        generation=generation,
        output_name=proj_id,
        voice=voice_choice,
        rate=0.97,
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
    if dur < 24.5 or dur > 30.5:
        print(f"⚠️ AVISO: Duración {dur:.2f}s fuera del rango óptimo 25-30s!")

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
    if dest_video.exists():
        dest_video.unlink()
    shutil.copy2(final_video_path, dest_video)

    # 3. Inyectar miniatura en frame 0
    inject_thumbnail_into_video(dest_video, thumb_path, queue_name)

    final_dur = get_duration(str(dest_video))
    print(f"✅ Video viral encolado: {dest_video} (Duración: {final_dur:.2f}s)")

    # 4. Guardar metadata.json para YouTube Shorts / Reels / TikTok
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
    for proj in SLOTS_97_TO_106_PROJECTS:
        if target_slot is not None and proj["slot"] != target_slot:
            continue
        v = produce_project(proj)
        if v:
            produced.append(v)
        else:
            print(f"❌ Error produciendo slot {proj['slot']}")

    print("\n" + "=" * 80)
    print(f"🎉 RESUMEN FINAL: {len(produced)} VIDEOS VIRALES (SLOTS 97 AL 106) PRODUCIDOS")
    print("=" * 80)

if __name__ == "__main__":
    main()
