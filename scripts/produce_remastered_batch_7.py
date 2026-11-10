"""
Master Production Engine: Batch 7 Remastered Mega Hits (>10k Views: Slots 67 al 76)
===================================================================================
1. Slot 67: Invincible Iron Man - El Gran Robo del Mysterium (Fall of X)
2. Slot 68: Thor: God of Thunder - Gorr el Carnicero de Dioses
3. Slot 69: All-Star Superman - El Sacrificio Supremo del Hombre del Mañana
4. Slot 70: Identity Crisis - Deathstroke Humilla a la Liga de la Justicia
5. Slot 71: Thor Vol 6 - Thor Ejecuta a Galactus y Corona Asgard
6. Slot 72: Green Lantern - Crepúsculo Esmeralda: La Caída de Hal Jordan y Parallax
7. Slot 73: Deadpool Kills Marvel - Deadpool Mata a Thor con Mjolnir Gigante
8. Slot 74: The Immortal Hulk #8 - Descuartizado en Frascos de Vidrio
9. Slot 75: Marvel Ruins - El Universo Donde Todo lo que Podía Salir Mal, Salió Mal
10. Slot 76: Ultimatum - Magneto Ahogó Nueva York con un Tsunami Colosal

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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_7_remasters"
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

REMASTER_PROJECTS_BATCH_7 = [
    {
        "slot": 67,
        "queue_folder": "67_iron_man_mysterium_gran_robo",
        "id": "iron_man_mysterium_gran_robo",
        "title": "¡El Metal Mutante Indestructible! El Gran Robo de Tony Stark y Emma Frost 🤖💎",
        "character": "Iron Man & Emma Frost",
        "folder": "67_iron_man_mysterium_gran_robo",
        "theme_signature": "iron_man:mysterium_heist:mark_72_armor",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/67_iron_man_mysterium_gran_robo/scene_03.jpg",
            "text": "¡EL ROBO MUTANTE!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 110
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El robo más audaz y desesperado en la historia de Marvel donde Tony Stark desafió las leyes de la física y la magia! Tras el ataque genocida de la organización anti-mutante Orchis en la Hellfire Gala, Krakoa cayó y los mutantes fueron cazados al borde de la extinción en todo el globo terráqueo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Despojado de su propia compañía y perseguido por Centinelas Stark fabricados con sus diseños robados, Tony forjó una alianza secreta con Emma Frost. Fingiendo un matrimonio público de alta sociedad para infiltrarse en el Club Hellfire, ambos planearon el golpe definitivo en las sombras contra sus enemigos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "El objetivo era el Mysterium, un metal milagroso refinado por mutantes en el mismísimo White Hot Room: un elemento diez veces más resistente que el adamantium, cien por ciento conductor y completamente inmune a cualquier hechicería, magia oscura o ataque psíquico del cosmos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Burlando los escáneres de Orchis en una incursión submarina suicida, Tony extrajo los lingotes sagrados y forjó en secreto la legendaria Armadura Mark setenta y dos, la armadura Mysterium con la que prometió destruir a Orchis. ¿Crees que este metal supera al vibranium y al adamantium? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La audaz infiltración de Tony Stark y Emma Frost en Invincible Iron Man #10. El robo del Mysterium para forjar la Mark 72.",
        "hashtags": "#IronMan #EmmaFrost #Mysterium #XMen #FallOfX #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 68,
        "queue_folder": "68_thor_gorr_carnicero_dioses",
        "id": "thor_gorr_carnicero_dioses",
        "title": "¡Gorr el Carnicero de Dioses! El Mortal que Juró Asesinar a Todas las Deidades ⚔️⚡🩸",
        "character": "Thor & Gorr",
        "folder": "68_thor_gorr_carnicero_dioses",
        "theme_signature": "thor:gorr_god_butcher:all_black_necrosword",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/68_thor_gorr_carnicero_dioses/scene_01.jpg",
            "text": "¡EL CARNICERO DE DIOSES!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 98
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La cruzada de venganza más sangrienta del cosmos de Marvel que puso a temblar a todo el panteón divino! En un planeta desolado y azotado por hambrunas infernales, un simple mortal llamado Gorr vio morir a su esposa e hijos rezándole inútilmente a dioses sordos que jamás respondieron a sus súplicas."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Exiliado por su pueblo, Gorr presenció la caída de dos deidades en combate. Al ver que los dioses sí existían pero ignoraban el sufrimiento de los inocentes, reclamó la Necroespada All-Black, la espada primigenia nacida de la sombra de Knull, jurando exterminar hasta el último dios del universo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Durante tres milenios, Gorr cazó y desolló divinidades a través de las galaxias enteras, construyendo en secreto la Bomba de Dioses para borrarlos a todos de la existencia en cada línea temporal. La amenaza fue tan monstruosa que tres versiones temporales de Thor debieron unirse para confrontarlo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El Thor joven y salvaje del pasado, el vengador del presente y el anciano Rey Thor del fin del tiempo libraron una guerra estelar sin tregua para detener al Carnicero. ¿Es Gorr el villano con la motivación más justificada de Marvel? ¡Comenta abajo tu opinión!"
            }
        ],
        "description": "La épica saga de Jason Aaron y Esad Ribic en Thor: God of Thunder #1-11. Gorr el Carnicero de Dioses y la Necroespada.",
        "hashtags": "#Thor #Gorr #GodButcher #AllBlackNecrosword #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 69,
        "queue_folder": "69_superman_all_star_sacrificio",
        "id": "superman_all_star_sacrificio",
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
            "font_size": 102
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La obra maestra indiscutible de Grant Morrison y Frank Quitely que captura la verdadera esencia del héroe más grande de la historia! Todo comenzó con una trampa orquestada por Lex Luthor: Superman rescató a una tripulación científica en la atmósfera del Sol, recibiendo una sobredosis masiva de radiación que saturó sus células a niveles letales."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con solo un año de vida por delante, Clark Kent no cayó en la desesperación ni en la ira; decidió regalarle a la humanidad sus últimos días cumpliendo los legendarios doce trabajos de Superman y asegurando el futuro del planeta antes de su partida final."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Le reveló su identidad a Lois Lane, compartió sus poderes con ella en un beso en la Luna, salvó vidas en los rincones más oscuros de Metrópolis e inspiró a una joven al borde del suicidio recordándole que siempre era mucho más fuerte de lo que creía en su interior."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Cuando la estrella solar fue envenenada por el tirano cósmico Solaris, Superman se despidió de Lois con un beso eterno y voló directo al núcleo ardiente del Sol para reparar su corazón, transformándose para siempre en el Dios Dorado que vigila a la Tierra. ¿Es este el cómic definitivo de Superman? ¡Dinos en los comentarios!"
            }
        ],
        "description": "La cumbre de Grant Morrison: All-Star Superman #1-12. El sacrificio solar del Hombre del Mañana.",
        "hashtags": "#Superman #AllStarSuperman #GrantMorrison #LexLuthor #DCComics #Comics #Shorts #Reels"
    },
    {
        "slot": 70,
        "queue_folder": "70_deathstroke_identity_crisis_liga",
        "id": "deathstroke_identity_crisis_liga",
        "title": "¡Un Solo Mercenario Humilló a la Liga de la Justicia! La Hazaña de Deathstroke ⚔️🔥💥",
        "character": "Deathstroke",
        "folder": "70_deathstroke_identity_crisis_liga",
        "theme_signature": "deathstroke:identity_crisis_3:solo_defeats_jla",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/70_deathstroke_identity_crisis_liga/scene_02.jpg",
            "text": "¡HUMILLÓ A LA LIGA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 108
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La mayor cátedra de táctica militar y brutalidad humana jamás vista en las páginas de DC Comics! Durante los eventos de Crisis de Identidad, la Liga de la Justicia acorraló al villano Doctor Luz en un almacén abandonado. Pero lo que no sabían era que Slade Wilson, Deathstroke, había sido contratado como su guardaespaldas privado."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin superpoderes cósmicos, utilizando únicamente el noventa por ciento de su capacidad cerebral y pura preparación letal, Deathstroke anticipó la velocidad infinita de Wally West colocando explosivos en el suelo para hacerlo volar y empalarse contra su propia espada de combate."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En menos de cuatro segundos, golpeó con precisión quirúrgica a Zatanna en el plexo solar haciéndola vomitar e impidiéndole pronunciar sus conjuros mágicos, le cortó las correas del arnés de vuelo a Hawkman dejándolo indefenso y rompió los dedos de Kyle Rayner para impedirle cerrar el puño."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Slade sujetó el anillo de poder de Green Lantern y comenzó a sobrecargarlo con su propia fuerza de voluntad inquebrantable, hasta que Green Arrow le clavó una flecha en la cuenca del ojo vacío. ¿Ha existido alguna hazaña más humillante para la Liga? ¡Comenta tu opinión!"
            }
        ],
        "description": "La legendaria batalla de Brad Meltzer en Identity Crisis #3. Slade Wilson vs la Liga de la Justicia.",
        "hashtags": "#Deathstroke #JusticeLeague #IdentityCrisis #Flash #DCComics #SladeWilson #Comics #Shorts #Reels"
    },
    {
        "slot": 71,
        "queue_folder": "71_thor_mata_galactus_ejecucion",
        "id": "thor_mata_galactus_ejecucion",
        "title": "¡Thor Asesinó a Galactus! La Brutal Ejecución del Devorador de Mundos ⚡👑💀",
        "character": "Thor & Galactus",
        "folder": "71_thor_mata_galactus_ejecucion",
        "theme_signature": "thor:donny_cates_6:kills_galactus_herald",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/71_thor_mata_galactus_ejecucion/scene_03.jpg",
            "text": "¡EJECUTÓ A GALACTUS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La ejecución cósmica más imponente y despiadada en la historia moderna de Marvel Comics! Cuando una catástrofe conocida como el Black Winter amenazó con devorar todo el multiverso, Galactus acudió a Asgard desesperado buscando la ayuda de Thor, transformándolo en su Heraldo del Trueno con el Poder Cósmico."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Juntos lucharon a través del espacio profundo hasta derrotar a la plaga estelar. Pero justo antes de morir, el Black Winter le mostró a Thor una visión aterradora: el verdadero causante de la destrucción total del universo siempre había sido el propio Galactus."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Comprendiendo que el Devorador de Mundos era una plaga insaciable que jamás se detendría por las buenas, Thor no dudó. Invocando el martillo Mjolnir, el Dios del Trueno drenó toda la energía del Poder Cósmico del cuerpo del gigante, dejándolo completamente desvalido y aterrado en el vacío sideral."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con una descarga de relámpagos cataclísmicos que iluminó galaxias enteras, Thor fulminó a Galactus hasta reducir su colosal cuerpo a cenizas y huesos, convirtiendo su gigantesco casco cornudo en las puertas de entrada de Asgard como advertencia al universo. ¿Hizo lo correcto Thor al ejecutarlo? ¡Comenta abajo!"
            }
        ],
        "description": "El momento apoteósico de Donny Cates y Nic Klein en Thor Vol. 6 #6. Thor ejecuta a Galactus con Mjolnir.",
        "hashtags": "#Thor #Galactus #Mjolnir #HeraldOfThunder #Marvel #MarvelComics #Avengers #Comics #Shorts #Reels"
    },
    {
        "slot": 72,
        "queue_folder": "72_green_lantern_parallax_crepusculo",
        "id": "green_lantern_parallax_crepusculo",
        "title": "¡El Mayor Linterna Verde se Volvió Villano! La Caída de Hal Jordan y Parallax 🟢💀⚡",
        "character": "Hal Jordan / Parallax",
        "folder": "72_green_lantern_parallax_crepusculo",
        "theme_signature": "green_lantern:emerald_twilight:hal_jordan_parallax",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/72_green_lantern_parallax_crepusculo/scene_04.jpg",
            "text": "¡PARALLAX NACIÓ!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 118
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La tragedia más desgarradora y oscura del universo cósmico de DC Comics! Todo comenzó cuando el tirano Mongul y Cyborg Superman detonaron setenta y siete mil ojivas nucleares sobre Coast City, borrando a siete millones de habitantes de la faz de la Tierra y dejando a Hal Jordan frente a un cráter humeante."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Consumido por un dolor incontrolable, Hal utilizó su anillo de voluntad para reconstruir la ciudad entera con sus recuerdos. Pero los Guardianes del Universo de Oa interrumpieron su creación, acusándolo de romper la ley cósmica y amenazándolo con quitarle el anillo por conducta egoísta."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Enloquecido de ira ante la frialdad de sus amos, Hal viajó a Oa desatando una auténtica masacre. Derrotó y despojó de sus anillos a decenas de Linternas Verdes, asesinó brutalmente a su mejor amigo Kilowog y le partió el cuello a su némesis Sinestro en un duelo a muerte."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Sin nada que perder, Jordan se arrojó al interior de la Gran Batería Central de Poder, absorbiendo toda la energía esmeralda y la entidad cósmica del miedo, renaciendo como Parallax, el destructor del cosmos. ¿Fue justificada la furia de Hal Jordan? ¡Dinos en los comentarios!"
            }
        ],
        "description": "La legendaria caída de Hal Jordan en Emerald Twilight (Green Lantern #48-50). El nacimiento de Parallax.",
        "hashtags": "#GreenLantern #HalJordan #Parallax #EmeraldTwilight #Sinestro #DCComics #Comics #Shorts #Reels"
    },
    {
        "slot": 73,
        "queue_folder": "73_deadpool_mata_thor_mjolnir",
        "id": "deadpool_mata_thor_mjolnir",
        "title": "¡La Muerte Más Humillante de Thor a Manos de Deadpool! 🔨💀💥",
        "character": "Deadpool vs Thor",
        "folder": "73_deadpool_mata_thor_mjolnir",
        "theme_signature": "deadpool:kills_marvel_universe_4:thor_crushed_mjolnir",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/73_deadpool_mata_thor_mjolnir/scene_04.jpg",
            "text": "¡THOR APLASTADO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 115
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La muerte más censurada, grotesca e ingeniosa de un dios en las páginas de Marvel Comics! En la célebre historia Deadpool Kills the Marvel Universe, una terapia psiquiátrica manipulada provocó que Wade Wilson comprendiera la verdad del cómic: todos eran marionetas sufriendo para el entretenimiento del lector."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Decidido a liberar a sus amigos a través de la muerte, Deadpool emprendió una cacería metódica y despiadada contra todos los héroes del planeta. Pero cuando se enfrentó cara a cara con Thor, el Dios del Trueno creyó que un simple mortal con espadas no sería rival para su poder divino."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Con furia tempestuosa, Thor arrojó el Mjolnir a velocidad hipersónica para pulverizar la cabeza de Wade. Pero Deadpool no intentó esquivarlo; en su lugar, arrojó un frasco entero de Partículas Pym directamente en la trayectoria del martillo encantado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al cruzar la nube cuántica y regresar volando hacia la mano de su amo por el llamado místico, el Mjolnir creció al tamaño de un rascacielos gigantesco, aplastando y pulverizando a Thor contra el pavimento en una fracción de segundo. ¿Ha tenido algún Vengador una muerte más humillante? ¡Comenta abajo!"
            }
        ],
        "description": "La retorcida muerte de Thor en Deadpool Kills the Marvel Universe #4. El martillo gigante con partículas Pym.",
        "hashtags": "#Deadpool #Thor #Mjolnir #PymParticles #DeadpoolKillsTheMarvelUniverse #Marvel #Comics #Shorts #Reels"
    },
    {
        "slot": 74,
        "queue_folder": "74_immortal_hulk_descuartizado_frascos",
        "id": "immortal_hulk_descuartizado_frascos",
        "title": "¡Descuartizaron a Hulk en Frascos de Vidrio! La Resurrección Más Aterradora 🟢💀🧪",
        "character": "The Immortal Hulk",
        "folder": "74_immortal_hulk_descuartizado_frascos",
        "theme_signature": "immortal_hulk:al_ewing_8:dissected_in_jars_resurrection",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/74_immortal_hulk_descuartizado_frascos/scene_02.jpg",
            "text": "¡HULK EN FRASCOS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 110
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El experimento científico más macabro y espeluznante jamás realizado en la historia de Marvel Comics! La siniestra organización militar Shadow Base logró capturar a Bruce Banner. Para evitar que el monstruo volviera a transformarse, un equipo de cirujanos desmembró metódicamente cada centímetro de su cuerpo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su corazón, sus pulmones, sus ojos y sus extremidades fueron seccionados vivos y colocados en recipientes herméticos de vidrio con soluciones químicas. El científico a cargo, el doctor Clive, se regocijó creyendo que por fin la ciencia humana había conquistado y neutralizado la amenaza de Hulk."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero en The Immortal Hulk, la biología de la radiación gamma no responde a las leyes mortales. Cuando el sol se ocultó y la oscuridad cubrió el laboratorio, la cabeza cercenada de Hulk dentro del frasco abrió sus ojos brillantes y le dedicó una sonrisa demoníaca que heló la sangre de Clive."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Desde otro frasco, la mano cortada de Hulk chasqueó los dedos con fuerza titánica rompiendo los recipientes en mil pedazos, mientras los órganos y la carne verde se fusionaron devorando y absorbiendo vivo al doctor en una masa viviente. ¿Es Immortal Hulk la etapa más terrorífica del gigante? ¡Comenta!"
            }
        ],
        "description": "El escalofriante número de Al Ewing y Joe Bennett en The Immortal Hulk #8. Hulk descuartizado en frascos.",
        "hashtags": "#ImmortalHulk #Hulk #BruceBanner #MarvelHorror #AlEwing #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 75,
        "queue_folder": "75_marvel_ruins_universo_maldito",
        "id": "marvel_ruins_universo_maldito",
        "title": "Marvel Ruins: El Universo Donde Todo lo que Podía Salir Mal, Salió Mal ☣️💀🌑",
        "character": "Marvel Ruins",
        "folder": "75_marvel_ruins_universo_maldito",
        "theme_signature": "marvel_ruins:warren_ellis:dystopia_biological_horror",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/75_marvel_ruins_universo_maldito/scene_02.jpg",
            "text": "¡EL UNIVERSO MALDITO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 102
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La distopía más perturbadora, enfermiza y deprimente de todo el multiverso de Marvel! Creada por el legendario guionista Warren Ellis, la miniserie Ruins presenta una realidad alternativa terrorífica donde las leyes de la física y la biología no otorgaron milagros: cada accidente radioactivo provocó una tragedia biológica abominable."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El periodista Phil Sheldon recorre las ruinas podridas de Estados Unidos documentando el destino atroz de los seres que en otro mundo fueron héroes. Peter Parker no se convirtió en Spider-Man; la picadura de la araña irradiada le provocó una erupción masiva y gangrenosa que carcomió su cuerpo hasta asfixiarlo en agonía."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Bruce Banner no es un titán de músculos, sino una masa monstruosa de tumores y quistes cancerígenos palpitantes que apenas puede respirar en una celda de plomo, mientras Silver Surfer enloqueció en el espacio arrancándose su propia piel metálica a jirones sangrientos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En este mundo sin esperanza, los Vengadores fueron ejecutados como presos comunes y el gobierno militarizado oculta los cadáveres de los mutantes desfigurados. ¿Podrías vivir en un universo tan despiadado como Marvel Ruins? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La desgarradora pesadilla distópica de Warren Ellis en Marvel Ruins #1-2. El universo donde ningún héroe triunfó.",
        "hashtags": "#MarvelRuins #Ruins #WarrenEllis #SpiderMan #Hulk #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 76,
        "queue_folder": "76_magneto_ultimatum_tsunami_manhattan",
        "id": "magneto_ultimatum_tsunami_manhattan",
        "title": "Magneto: El Día que Ahogó al Mundo en Ultimatum 🌊💀🗽",
        "character": "Magneto",
        "folder": "76_magneto_ultimatum_tsunami_manhattan",
        "theme_signature": "magneto:ultimatum_1:manhattan_tidal_wave",
        "voice": "Puck",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/76_magneto_ultimatum_tsunami_manhattan/scene_01.jpg",
            "text": "¡MAGNETO AHOGÓ NY!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 108
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El cataclismo más sangriento y devastador en la historia del Universo Ultimate de Marvel! Tras el brutal asesinato de sus hijos Wanda y Pietro Maximoff, un Magneto completamente desquiciado por el luto y el odio decidió que la humanidad ya no merecía existir ni un solo segundo más sobre la faz de la Tierra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Utilizando el martillo robado de Thor y combinando su poder magnético con las líneas de fuerza polar del planeta, Magneto invirtió los polos magnéticos terrestres, desatando una perturbación gravitatoria colosal sobre las aguas del océano Atlántico."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Una gigantesca muralla de agua de cientos de metros de altura se levantó sobre la bahía de Nueva York y se estrelló a velocidad supersónica contra la isla de Manhattan, pulverizando rascacielos y arrastrando a millones de civiles y superhéroes bajo toneladas de escombros y fango."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Spider-Man, Daredevil, Avispa y Bestia se ahogaron en cuestión de minutos entre las ruinas inundadas, mientras Magneto contemplaba la masacre flotando impasible en el ojo de la tormenta. ¿Fue Ultimatum el evento más brutal y polémico de Marvel? ¡Comenta abajo!"
            }
        ],
        "description": "El evento cataclísmico de Jeph Loeb y David Finch en Ultimatum #1. Magneto inunda Manhattan con una ola titánica.",
        "hashtags": "#Magneto #Ultimatum #UltimateMarvel #SpiderMan #XMen #Avengers #Comics #Shorts #Reels"
    }
]

def produce_project(proj: dict):
    slot = proj["slot"]
    queue_name = proj["queue_folder"]
    proj_id = proj["id"]
    print("\n" + "=" * 80)
    print(f"🎬 [PRODUCIENDO SLOT {slot}]: {proj['title']}")
    print("=" * 80)

    curated_folder = CURATED_BASE / proj["folder"]
    scene_art_urls = []
    scenes_text = []
    for s in proj["scenes"]:
        p_path = curated_folder / s["file"]
        if not p_path.exists():
            print(f"❌ [ERROR] Panel faltante: {p_path}")
            return None
        scene_art_urls.append(str(p_path))
        scenes_text.append(s["text"])

    story_payload = dict(proj)
    story_payload["scenes"] = scenes_text
    story_payload["scene_art_urls"] = scene_art_urls

    proj_out_dir = PACK_OUTPUT_DIR / proj_id
    if proj_out_dir.exists():
        shutil.rmtree(proj_out_dir, ignore_errors=True)

    work_dir = PROJECT_ROOT / "work" / f"batch7_{proj_id}"
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
    for proj in REMASTER_PROJECTS_BATCH_7:
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
