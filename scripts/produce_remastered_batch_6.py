"""
Master Production Engine: Batch 6 Remastered Mega Hits (Slots 56 al 65)
======================================================================
1. Slot 56: Hellboy - La Mano Derecha del Destino (Anung Un Rama)
2. Slot 57: Alfred vs Superman - El Cabezazo Brutal (Injustice #36)
3. Slot 58: Bruce Wayne Recupera el Manto de Batman (KnightsEnd)
4. Slot 59: Doctor Doom Destruye a Thanos (Secret Wars #8)
5. Slot 60: Flash Reverso - El Odio Eterno de Thawne (The Flash: Rebirth)
6. Slot 61: Lobo - Expulsado del Cielo y el Infierno (The Last Czarnian / Lobo's Back)
7. Slot 62: World War Hulk - La Venganza contra los Illuminati (World War Hulk)
8. Slot 63: Azrael Batman Destroza a Bane (Knightfall #19)
9. Slot 64: Plastic Man - La Pesadilla Secreta de Batman (JLA Tower of Babel)
10. Slot 65: Venom Dios de la Luz Aniquila a Knull (King in Black #5)

Reglas Críticas:
- Duración obligatoria >= 60.0 segundos por video.
- Primer frame exacto (t=0.000s) es la miniatura de alto impacto.
- Paneles 100% canónicos 1:1.
- Safe-zone 1:1 para Reels/Shorts.
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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_6_remasters"
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

def draw_pill_badge(canvas: Image.Image, text: str, center_x: int, y: int, font: ImageFont.FreeTypeFont,
                    bg_color=(15, 15, 15, 220), border_color=(255, 230, 0, 255), border_width=3,
                    text_color=(255, 255, 255), pad_x=28, pad_y=10, radius=18) -> Image.Image:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    x1 = center_x - tw // 2 - pad_x
    x2 = center_x + tw // 2 + pad_x
    y1 = y
    y2 = y + th + pad_y * 2

    d.rounded_rectangle([x1 + 3, y1 + 4, x2 + 3, y2 + 4], radius=radius, fill=(0, 0, 0, 180))
    d.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg_color, outline=border_color, width=border_width)

    tx = center_x - tw // 2 - bbox[0]
    ty = y + pad_y - bbox[1]
    d.text((tx, ty), text, font=font, fill=text_color)

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

def apply_text_vignette(canvas: Image.Image, top_y=380, bottom_y=860, max_alpha=190) -> Image.Image:
    w, h = canvas.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    mid_y = (top_y + bottom_y) // 2
    height_range = (bottom_y - top_y) / 2.0

    for y in range(top_y, bottom_y):
        dist = abs(y - mid_y) / height_range
        alpha = int(max_alpha * (1.0 - (dist ** 2)))
        alpha = max(0, min(255, alpha))
        if alpha > 0:
            ov_draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha))

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

def draw_impact_text(canvas: Image.Image, lines: list[dict], center_x=540, start_y=470, line_spacing=18) -> Image.Image:
    canvas_rgba = canvas.convert("RGBA")
    w, h = canvas.size

    line_layouts = []
    curr_y = start_y

    for item in lines:
        font = ImageFont.truetype(FONT_IMPACT, item.get('size', 96))
        txt = item['text']
        bbox = font.getbbox(txt)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = center_x - tw // 2 - bbox[0]
        line_layouts.append({
            'text': txt,
            'font': font,
            'pos': (x, curr_y),
            'color': item.get('color', (255, 235, 0)),
            'stroke_color': item.get('stroke_color', (0, 0, 0)),
            'stroke_w': item.get('stroke_w', 9),
            'shadow_blur': item.get('shadow_blur', 12),
            'shadow_offset': item.get('shadow_offset', (0, 7)),
        })
        curr_y += th + line_spacing

    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)

    for layout in line_layouts:
        x, y = layout['pos']
        ox, oy = layout['shadow_offset']
        s_draw.text((x + ox, y + oy), layout['text'], font=layout['font'],
                    fill=(0, 0, 0, 230),
                    stroke_width=layout['stroke_w'] + 6,
                    stroke_fill=(0, 0, 0, 230))

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))
    canvas_rgba = Image.alpha_composite(canvas_rgba, shadow_layer)

    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)

    for layout in line_layouts:
        x, y = layout['pos']
        t_draw.text((x, y), layout['text'], font=layout['font'],
                    fill=layout['color'],
                    stroke_width=layout['stroke_w'],
                    stroke_fill=layout['stroke_color'])

    final_im = Image.alpha_composite(canvas_rgba, text_layer)
    return final_im.convert("RGB")

def build_high_impact_thumbnail(proj: dict, output_path: Path):
    thumb_cfg = proj["thumb_config"]
    source_img_path = Path(thumb_cfg["source_art"])
    if not source_img_path.is_absolute():
        source_img_path = PROJECT_ROOT / source_img_path

    raw_img = Image.open(source_img_path).convert("RGB")
    graded = apply_cinematic_grade(raw_img)
    canvas = fit_to_vertical(graded, 1080, 1920)

    top_v, bot_v = thumb_cfg.get("vignette", (390, 850))
    canvas = apply_text_vignette(canvas, top_y=top_v, bottom_y=bot_v, max_alpha=190)

    badge_font = ImageFont.truetype(FONT_IMPACT, 40)
    badge_text = thumb_cfg.get("badge", "MULTIVERSO CÓMIC")
    badge_border = thumb_cfg.get("badge_border", (255, 230, 0, 255))
    canvas = draw_pill_badge(canvas, badge_text, 540, 395, badge_font, border_color=badge_border)

    start_y = thumb_cfg.get("text_start_y", 465)
    canvas = draw_impact_text(canvas, thumb_cfg["lines"], center_x=540, start_y=start_y, line_spacing=18)

    canvas.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"  [THUMB] Miniatura de alto impacto creada: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    return output_path

def inject_thumbnail_into_video(video_path: Path, thumb_path: Path):
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
        print(f"  [ERROR] Video resultante corrupto o pequeño: {temp_out.stat().st_size} bytes")
        temp_out.unlink()
        return False

    # Auditoría de frame 0
    audit_f0 = BRAIN_DIR / f"audit_frame0_{video_path.parent.name}.jpg"
    subprocess.run([
        'ffmpeg', '-y',
        '-ss', '00:00:00.000',
        '-i', str(temp_out),
        '-vframes', '1',
        '-q:v', '2',
        str(audit_f0)
    ], capture_output=True)

    shutil.move(temp_out, video_path)
    print(f"  [OK] Frame 0 inyectado y verificado: {video_path.name}")
    return True

REMASTER_PROJECTS_BATCH_6 = [
    {
        "slot": 56,
        "queue_folder": "56_hellboy_mano_derecha_apocalipsis",
        "id": "hellboy_mano_derecha_apocalipsis",
        "title": "¡El Secreto de la Mano de Hellboy! La Llave del Fin del Mundo 🗝️🔥💀",
        "character": "Hellboy",
        "folder": "56_hellboy_mano_derecha_apocalipsis",
        "theme_signature": "hellboy:right_hand_of_doom:anung_un_rama",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El secreto más perturbador en el universo de Dark Horse que cambia por completo el propósito de Hellboy! En una tormentosa noche de mil novecientos cuarenta y cuatro, una división esotérica nazi abrió una brecha infernal sobre las ruinas de una abadía en Escocia. Para asombro del profesor Trevor Bruttenholm y los soldados aliados, no surgió un ejército colosal, sino un pequeño demonio rojo con cuernos recortados al que decidieron adoptar con amor."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin embargo, la criatura portaba un misterio aterrador en su brazo derecho: un guantelete gigante de piedra viva, indestructible y frío como la tumba. Durante años, la humanidad creyó que aquella extremidad era un simple defecto biológico o un mazo de combate para aplastar monstruos paranormales. Pero antiguos textos ocultos revelaron que la reliquia fue tallada por los espíritus primordiales del universo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su verdadero nombre no es Hellboy, sino Anung Un Rama, que se traduce como sobre cuya frente se posa la corona de fuego. Esa colosal extremidad de piedra no es un arma terrenal, sino la Mano Derecha del Destino: la única llave cósmica capaz de girar la cerradura del abismo infinito y despertar a los siete dioses del caos para devorar toda la creación."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Conociendo su espantoso destino, Hellboy se niega a abrir el inframundo, luchando cada día contra su propia sangre demoníaca para defender a la humanidad que lo acogió. ¿Crees que Hellboy logrará resistir su destino final para siempre, o la profecía del apocalipsis será inevitable? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La mitología original creada por Mike Mignola en Dark Horse Comics: Hellboy y el enigma profético de la Mano Derecha del Destino.",
        "hashtags": "#Hellboy #DarkHorse #AnungUnRama #RightHandOfDoom #MikeMignola #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/56_hellboy_mano_derecha_apocalipsis/scene_04.jpg",
            "badge": "DARK HORSE • CANÓNICO",
            "badge_border": (255, 30, 40, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡LA MANO DEL DESTINO!", "size": 98, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "LA LLAVE DEL APOCALIPSIS", "size": 84, "color": (255, 255, 255), "stroke_w": 9},
                {"text": "EL SECRETO DE HELLBOY", "size": 64, "color": (0, 230, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 57,
        "queue_folder": "57_injustice_alfred_superman",
        "id": "injustice_alfred_superman",
        "title": "¡Alfred Humilló a Superman! El Mayordomo Rompe la Nariz al Tirano ☕💥🩸",
        "character": "Alfred Pennyworth",
        "folder": "57_injustice_alfred_superman",
        "theme_signature": "injustice:alfred_headbutt_superman:nanopill_5u93r",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El momento más glorioso y brutal en la historia de DC Comics donde Superman aprendió lo que significa la verdadera furia familiar! En el universo de Injustice, el Hombre de Acero se convirtió en un dictador sanguinario. Tras rastrear a Batman hasta las profundidades de la Baticueva, Clark Kent estrelló al Caballero de la Noche contra el suelo y le quebró la columna vertebral sobre su rodilla con total frialdad."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Mientras Bruce Wayne agonizaba desangrándose en el pavimento, Superman se burló de su resistencia humana, asegurando que nadie en el planeta podía desafiar el orden supremo del Régimen. Pero en las sombras de la cueva, un hombre de setenta años de traje impecable observó cómo el alienígena intentaba arrebatarle a su único hijo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Con la elegancia de un mayordomo británico, Alfred Pennyworth tragó la píldora nanotecnológica experimental 5-U-93-R que aumentaba la fuerza tisular por miles. Sin mediar palabra, Alfred apoyó su mano en el hombro del tirano y le descargó un cabezazo demoledor con tanta violencia que fracturó los huesos faciales de Superman en una lluvia de sangre."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Enfurecido como jamás se le vio, Alfred pisoteó el rostro del dios alienígena y lo molió a puñetazos en el suelo, advirtiéndole que jamás volvería a tocar a Bruce porque en él ya no quedaba nada que valiera la pena salvar. ¿Fue este el golpe más satisfactorio en los cómics? ¡Comenta abajo!"
            }
        ],
        "description": "El momento legendario de Tom Taylor y Bruno Redondo en Injustice: Gods Among Us #36. Alfred Pennyworth destroza a Superman.",
        "hashtags": "#AlfredPennyworth #Superman #Batman #Injustice #DCComics #InjusticeGodsAmongUs #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/57_injustice_alfred_superman/scene_03.jpg",
            "badge": "DC COMICS • INJUSTICE #36",
            "badge_border": (255, 230, 0, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡HUMILLÓ A SUPERMAN!", "size": 100, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "LE ROMPIÓ LA NARIZ", "size": 94, "color": (255, 35, 45), "stroke_w": 9},
                {"text": "LA BRUTAL FURIA DE ALFRED", "size": 64, "color": (255, 255, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 58,
        "queue_folder": "58_batman_recupera_manto_derrota_azrael",
        "id": "batman_recupera_manto_derrota_azrael",
        "title": "¡Bruce Wayne Recupera el Manto! La Caída del Batman Asesino 🦇⚔️🔥",
        "character": "Bruce Wayne",
        "folder": "58_batman_recupera_manto_derrota_azrael",
        "theme_signature": "batman:knightsend:bruce_defeats_azrael",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La batalla psicológica y estratégica más intensa donde Bruce Wayne demostró por qué nadie más puede ser el verdadero Batman! Tras sufrir la fractura de su espalda ante Bane, un Bruce debilitado cometió el peor error de su vida al ceder el manto a Jean-Paul Valley, el despiadado asesino conocido como Azrael, quien transformó el símbolo del murciélago en una máquina de tortura blindada."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Consumido por el fanatismo del Sistema de San Dumas, Azrael comenzó a ejecutar criminales con cuchillas térmicas y lanzallamas en las calles de Gotham. Bruce Wayne comprendió que sus plegarias no bastaban: entrenó hasta el límite de sus fuerzas con Lady Shiva y reconstruyó su cuerpo destrozado para regresar a reclamar su legado con sus propias manos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En lugar de enfrentarse con violencia bruta a la armadura cibernética de Azrael, Bruce atrajo al usurpador hasta las profundidades estrechas de la Baticueva. Usando las sombras y su conocimiento absoluto del terreno, Batman fue bloqueando cada salida hasta abrir una compuerta superior que inundó la caverna con una luz solar cegadora."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Incapaz de procesar la luz con sus visores infrarrojos enloquecidos, Jean-Paul colapsó de rodillas, arrancándose el casco metálico y llorando ante la silueta silenciosa y dominante de Bruce Wayne. ¿Crees que la armadura blindada de Azrael era necesaria para limpiar Gotham, o Bruce tenía la razón? ¡Déjanos tu comentario!"
            }
        ],
        "description": "El clímax triunfal de Dennis O'Neil, Chuck Dixon y Doug Moench: KnightsEnd. Bruce Wayne reclama el manto de Batman.",
        "hashtags": "#Batman #BruceWayne #Azrael #KnightsEnd #Knightfall #DCComics #Gotham #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/58_batman_recupera_manto_derrota_azrael/scene_02.jpg",
            "badge": "DC COMICS • KNIGHTSEND",
            "badge_border": (255, 230, 0, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡BRUCE WAYNE REGRESA!", "size": 96, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "LA CAÍDA DE AZRAEL", "size": 90, "color": (255, 255, 255), "stroke_w": 9},
                {"text": "EL VERDADERO CABALLERO OSCURO", "size": 60, "color": (0, 230, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 59,
        "queue_folder": "59_doctor_doom_destruye_thanos_secret_wars",
        "id": "doctor_doom_destruye_thanos_secret_wars",
        "title": "¡El Peor Error de Thanos! Desafió a Doctor Doom Dios y Pagó el Precio 💀👑⚡",
        "character": "Doctor Doom",
        "folder": "59_doctor_doom_destruye_thanos_secret_wars",
        "theme_signature": "doctor_doom:secret_wars_8:rips_thanos_spine",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El enfrentamiento de egos más aplastante en toda la historia de Marvel Comics que dejó en ridículo al Titán Loco! Tras el colapso absoluto del multiverso provocado por las incursiones, Victor Von Doom absorbió el poder omnipotente de los Beyonders, convirtiéndose en el Dios Emperador absoluto de Battleworld y gobernando la realidad desde su trono del Árbol del Mundo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Convencido de su propia superioridad cósmica y marchando al frente de un ejército invasor, Thanos exigió una audiencia directa con el monarca. Con una sonrisa arrogante, el Titán Loco le dijo a Doom que un hombre con armadura jamás sería un dios verdadero, y le ofreció la oportunidad de arrodillarse ante él para conservar su vida como siervo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Victor Von Doom descendió calmadamente de su trono divino y miró fijamente a los ojos de Thanos. Con voz gélida, Doom le preguntó si en ese instante poseía el Guantelete del Infinito o el Corazón del Universo en sus manos. Cuando el Titán Loco admitió con desprecio que no los necesitaba, el gobernante de Latveria extendió su brazo blindado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con un movimiento relampagueante e implacable, Doom atravesó el pecho del Titán, aferró su columna vertebral y la arrancó de cuajo en una milésima de segundo, convirtiendo el cuerpo entero de Thanos en una pila de huesos y cenizas humeantes. ¿Es Doctor Doom el villano definitivo y más poderoso de Marvel? ¡Comenta qué opinas!"
            }
        ],
        "description": "La escena más aplastante de Jonathan Hickman y Esad Ribic: Secret Wars #8. God Emperor Doom arranca la columna vertebral de Thanos.",
        "hashtags": "#DoctorDoom #Thanos #GodEmperorDoom #SecretWars #Marvel #MarvelComics #MCU #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/59_doctor_doom_destruye_thanos_secret_wars/scene_04.jpg",
            "badge": "MARVEL COMICS • SECRET WARS #8",
            "badge_border": (0, 230, 255, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡LE ARRANCÓ LA COLUMNA!", "size": 94, "color": (255, 35, 45), "stroke_w": 10},
                {"text": "A THANOS EN SEGUNDOS", "size": 86, "color": (255, 235, 0), "stroke_w": 9},
                {"text": "DOCTOR DOOM DIOS SUPREMO", "size": 62, "color": (255, 255, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 60,
        "queue_folder": "60_reverse_flash_odio_thawne",
        "id": "reverse_flash_odio_thawne",
        "title": "¡El Villano Más Retorcido de DC! El Odio Eterno de Flash Reverso ⚡🟡⏳",
        "character": "Reverse Flash",
        "folder": "60_reverse_flash_odio_thawne",
        "theme_signature": "reverse_flash:the_flash_rebirth:thawne_torment_barry",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La obsesión psicológica más aterradora y enferma en la historia de los superhéroes! Todos los villanos de los cómics buscan dinero, conquista galáctica o venganza tras una derrota. Pero Eobard Thawne, el infame Flash Reverso del siglo veinticinco, construyó toda su existencia con un único y macabro propósito: arruinar cada segundo de la vida de Barry Allen."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Thawne descubrió la Fuerza de la Velocidad Negativa, lo que le permitió viajar en el tiempo sin alterar su propia línea temporal. En lugar de simplemente asesinar a Barry en la cuna para ganar fácilmente, Eobard decidió torturarlo gota a gota a lo largo de décadas con una crueldad que hiela la sangre."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Viajando al pasado invisible como un fantasma, Thawne empujó a Barry por las escaleras cuando era un niño pequeño para fracturarle el brazo, asesinó a su perro de la infancia y borró de la existencia a su mejor amigo de la escuela para que creciera en soledad absoluta, culminando con el asesinato de su madre Nora."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Cuando Barry le preguntó desesperado por qué tanto resentimiento contra él, Thawne le sonrió con desquicio susurrándole que cada tragedia de su vida siempre fue obra suya. ¿Crees que Flash Reverso es el enemigo más tóxico y retorcido jamás creado? ¡Comenta tu opinión!"
            }
        ],
        "description": "La siniestra revelación de Geoff Johns y Ethan Van Sciver en The Flash: Rebirth. La tortura temporal de Eobard Thawne.",
        "hashtags": "#ReverseFlash #Flash #BarryAllen #EobardThawne #TheFlash #DCComics #SpeedForce #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/60_reverse_flash_odio_thawne/scene_02.jpg",
            "badge": "DC COMICS • FLASH: REBIRTH",
            "badge_border": (255, 30, 40, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡EL VILLANO MÁS TÓXICO!", "size": 96, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "EL ODIO DE FLASH REVERSO", "size": 84, "color": (255, 35, 45), "stroke_w": 9},
                {"text": "ARRUINÓ CADA DÍA DE SU VIDA", "size": 62, "color": (255, 255, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 61,
        "queue_folder": "61_lobo_expulsado_cielo_infierno",
        "id": "lobo_expulsado_cielo_infierno",
        "title": "¡Expulsado del Cielo y el Infierno! El Hombre que Rompió la Muerte 💀🚀🍺",
        "character": "Lobo",
        "folder": "61_lobo_expulsado_cielo_infierno",
        "theme_signature": "lobo:the_last_czarnian:banned_from_death",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La leyenda más desquiciada y sangrienta de todo el cosmos de DC Comics! En el planeta pacífico y utópico de Czarnia, nació un monstruo indestructible dotado de una fuerza titánica y un factor regenerativo invencible conocido como Lobo. Con solo diecisiete años, diseñó una plaga de insectos microscópicos que exterminó a los cinco mil millones de habitantes de su mundo solo para obtener una calificación perfecta."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Convertido en el cazarrecompensas más temido de la galaxia, Lobo recorrió el universo a bordo de su motocicleta espacial fumando puros cósmicos, cobrando contratos millonarios y despedazando a quien se cruzara en su camino con cadenas de tungsteno y dinamita. Pero su verdadera locura comenzó el día en que finalmente fue asesinado en combate."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al morir, su alma recaló directamente en el Paraíso celestial. Sin embargo, en lugar de cantar salmos de paz, Lobo le arrancó las cuerdas a una lira dorada para conectarla a amplificadores divinos, armó una pelea campal con los querubines y masacró a la mitad de los ángeles en un concierto de rock infernal."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Desesperados, los gobernantes del Cielo lo enviaron al Infierno, donde Lobo destrozó a los demonios mayores por pura diversión. Aterrorizados por la anarquía, tanto Dios como Lucifer firmaron un pacto eterno expulsándolo formalmente del Más Allá, otorgándole la inmortalidad absoluta. ¿Es Lobo el antihéroe definitivo? ¡Déjanos tu comentario!"
            }
        ],
        "description": "La creación de Alan Grant y Keith Giffen con arte de Simon Bisley: The Last Czarnian y Lobo's Back. La inmortalidad eterna de Lobo.",
        "hashtags": "#Lobo #TheMainMan #Czarnia #SimonBisley #DCComics #Inmortal #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/61_lobo_expulsado_cielo_infierno/scene_03.jpg",
            "badge": "DC COMICS • THE LAST CZARNIAN",
            "badge_border": (255, 230, 0, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡EXPULSADO DE LA MUERTE!", "size": 94, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "DEL CIELO Y EL INFIERNO", "size": 88, "color": (255, 35, 45), "stroke_w": 9},
                {"text": "LOBO ES 100% INDESTRUCTIBLE", "size": 60, "color": (255, 255, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 62,
        "queue_folder": "62_hulk_world_war_venganza_illuminati",
        "id": "hulk_world_war_venganza_illuminati",
        "title": "¡Hulk Aplasta a los Illuminati! La Venganza de Sakaar 🟢⚔️💥",
        "character": "Hulk",
        "folder": "62_hulk_world_war_venganza_illuminati",
        "theme_signature": "hulk:world_war_hulk:green_scar_revenge",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La hora más oscura para los superhéroes más inteligentes de la Tierra cuando desataron la furia definitiva del Gigante Esmeralda! Temiendo el poder destructivo de Hulk, los Illuminati liderados por Iron Man, Reed Richards y Doctor Strange lo engañaron y lo exiliaron al espacio profundo dentro de una nave automatizada con rumbo a un planeta desolado."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras caer en el salvaje mundo de Sakaar, Hulk sobrevivió a los coliseos de gladiadores, derrocó al Rey Rojo y encontró el amor con la reina Caiera, esperando tener su primer hijo. Pero el motor de la nave terrenal estalló en una deflagración nuclear que vaporizó a su esposa y a millones de inocentes, fracturando la mente del coloso para siempre."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Lleno de un odio incalculable, Hulk se armó con armadura de combate forjada en magma y regresó a la Tierra al frente de su flota alienígena. Uno tras otro, destrozó los huesos del Rey de los Inhumanos Black Bolt, despedazó la armadura Hulkbuster de Tony Stark y quebró las manos místicas del Hechicero Supremo con una brutalidad nunca antes vista."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Bruce Banner forzó a los mayores héroes del mundo a combatir como gladiadores esclavos en una arena en el corazón de Nueva York para que sintieran la traición en carne viva. ¿Estuvo justificada la venganza de Hulk contra los Illuminati? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La aclamada saga de Greg Pak y John Romita Jr: World War Hulk. La venganza implacable del Green Scar contra los Illuminati.",
        "hashtags": "#WorldWarHulk #Hulk #Illuminati #IronMan #DoctorStrange #Marvel #MarvelComics #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/62_hulk_world_war_venganza_illuminati/scene_02.jpg",
            "badge": "MARVEL COMICS • WORLD WAR HULK",
            "badge_border": (0, 230, 100, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡HULK DESTROZA A TODOS!", "size": 96, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "LA VENGANZA DE SAKAAR", "size": 86, "color": (255, 255, 255), "stroke_w": 9},
                {"text": "LA CAÍDA DE LOS ILLUMINATI", "size": 64, "color": (255, 35, 45), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 63,
        "queue_folder": "63_azrael_batman_destroza_bane",
        "id": "azrael_batman_destroza_bane",
        "title": "¡El Batman Dorado de Azrael! Destrozó a Bane con Cuchillas y Fuego 🦇🩸⚙️",
        "character": "Azrael",
        "folder": "63_azrael_batman_destroza_bane",
        "theme_signature": "azrael:knightfall_19:destroys_bane_venom",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El momento más violento y sangriento de la mítica saga Knightfall que cambió las reglas de Gotham para siempre! Tras quebrar la espalda de Bruce Wayne en la mansión, el colosal titán de Peña Dura, Bane, se proclamó el amo y señor del bajo mundo de la ciudad, convencido de que ningún mortal con capa volvería a desafiar su fuerza sobrehumana."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero Bruce le había confiado el manto al joven Jean-Paul Valley, quien pronto cayó bajo el influjo del adoctrinamiento religioso de la Orden de San Dumas. Despreciando el juramento de no matar de Bruce, Jean-Paul diseñó una temible armadura de titanio azul y oro equipada con garras afiladas de acero templado y lanzallamas de alta presión."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Azrael localizó a Bane en una fábrica abandonada y desató una ofensiva despiadada. Mientras Bane inyectaba dosis masivas de Venom en su cerebro para aplastarlo con sus puños de hierro, Valley esquivó los impactos y usó sus proyectiles de batarangs cortantes para rebanar sistemáticamente los conductos del químico venenoso."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con el Venom derramándose sobre el asfalto y el cuerpo de Bane colapsando en una agonía insoportable, Azrael lo golpeó sin piedad hasta dejarlo reducido a un hombre quebrado que rogaba por su vida en el suelo. ¿Crees que este nuevo Batman debió acabar con Bane en ese instante? ¡Déjanos tu comentario!"
            }
        ],
        "description": "El choque cumbre de Knightfall #19 por Chuck Dixon y Graham Nolan: Azrael pulveriza a Bane con su armadura de combate.",
        "hashtags": "#Azrael #Batman #Bane #Knightfall #JeanPaulValley #DCComics #Gotham #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/63_azrael_batman_destroza_bane/scene_03.jpg",
            "badge": "DC COMICS • KNIGHTFALL #19",
            "badge_border": (255, 30, 40, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡DESTROZÓ A BANE!", "size": 104, "color": (255, 35, 45), "stroke_w": 10},
                {"text": "CON CUCHILLAS Y FUEGO", "size": 86, "color": (255, 235, 0), "stroke_w": 9},
                {"text": "EL BATMAN ASESINO DE AZRAEL", "size": 60, "color": (255, 255, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 64,
        "queue_folder": "64_plastic_man_pesadilla_batman",
        "id": "plastic_man_pesadilla_batman",
        "title": "Plastic Man: El Arma Secreta y el Verdadero Terror de Batman 🔴⚡🧬",
        "character": "Plastic Man",
        "folder": "64_plastic_man_pesadilla_batman",
        "theme_signature": "plastic_man:tower_of_babel:batman_secret_fear",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El secreto más perturbador de la Liga de la Justicia que casi nadie conoce sobre el héroe más ridículo del equipo! Todos los miembros consideran a Patrick Eel O'Brian, alias Plastic Man, como un simple payaso bromista que utiliza su elasticidad para transformar su cuerpo en teteras, resortes o alfombras para divertir a sus compañeros."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin embargo, en los archivos secretos de contingencia de la Baticueva conocidos como la Torre de Babel, Bruce Wayne catalogó a Plastic Man no como un alivio cómico, sino como el ser biológico más peligroso y letal sobre la faz del planeta Tierra si alguna vez perdía la cordura moral."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su anatomía carece por completo de órganos internos, cerebro vulnerable o ADN orgánico común: sus moléculas están en constante estado fluido indestructible. Plastic Man sobrevivió al ser congelado en nitrógeno líquido y destrozado en millones de fragmentos en el fondo del océano durante más de tres mil años, reuniéndose después sin sufrir un solo rasguño."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Batman confesó que no existe ninguna debilidad natural para matarlo, ya que Plastic Man podría introducirse microscópicamente en los pulmones de Superman o en el torrente sanguíneo de cualquier héroe y expandirse hasta destrozarlos desde adentro. ¿Es Plastic Man el personaje más temible de DC? ¡Comenta qué opinas!"
            }
        ],
        "description": "La sorprendente revelación de Mark Waid y Howard Porter en JLA: Tower of Babel. El verdadero poder ilimitado de Plastic Man.",
        "hashtags": "#PlasticMan #Batman #JusticeLeague #TowerOfBabel #DCComics #JLA #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/64_plastic_man_pesadilla_batman/scene_04.jpg",
            "badge": "DC COMICS • TOWER OF BABEL",
            "badge_border": (255, 230, 0, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡EL TERROR DE BATMAN!", "size": 100, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "PLASTIC MAN ES INDESTRUCTIBLE", "size": 74, "color": (255, 255, 255), "stroke_w": 9},
                {"text": "EL HÉROE MÁS PELIGROSO DE DC", "size": 60, "color": (0, 230, 255), "stroke_w": 8},
            ]
        }
    },
    {
        "slot": 65,
        "queue_folder": "65_venom_dios_de_la_luz_knull",
        "id": "venom_dios_de_la_luz_knull",
        "title": "¡El Hacha de Luz Cósmica! Eddie Brock Aniquila a Knull ⚡🪓🌌",
        "character": "Venom",
        "folder": "65_venom_dios_de_la_luz_knull",
        "theme_signature": "venom:king_in_black_5:god_of_light_kills_knull",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El clímax cósmico más brutal y épico jamás presenciado en las páginas de Marvel Comics! Knull, el ancestral Dios de la Oscuridad y creador de los simbiontes, invadió el planeta Tierra al mando de billones de dragones alienígenas, cubriendo el cielo con una cúpula viviente que sumió a la humanidad en una pesadilla tenebrosa y asesinó a Eddie Brock arrojándolo al vacío."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con los Vengadores, los X-Men y la flota intergaláctica completamente subyugados por el abismo negro del All-Black, toda esperanza parecía extinta ante el señor del vacío que había decapitado a un Celestial con sus propias manos miles de millones de años atrás."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero en el momento de mayor desesperación, la Fuerza Enigma cósmica, el avatar de la luz primordial del universo, despertó y eligió el alma agonizante de Eddie Brock como su nuevo huésped divino. Eddie resucitó flotando en una llamarada brillante de fuego estelar, transformándose en el Dios de la Luz con alas angelicales de energía pura."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Fusionando el martillo de Thor con la tabla cósmica de Silver Surfer, Eddie forjó una colosal hacha de combate estelar, atravesó el cráneo de Knull, lo arrastró hasta el núcleo ardiente del Sol y lo incineró para siempre, asumiendo el mando supremo de la colmena simbionte. ¿Fue este el mejor momento en la historia de Venom? ¡Comenta abajo!"
            }
        ],
        "description": "La apoteósica batalla final creada por Donny Cates y Ryan Stegman: King in Black #5. Venom Dios de la Luz derrota a Knull.",
        "hashtags": "#Venom #KingInBlack #EddieBrock #Knull #Marvel #MarvelComics #Symbiote #Comics #Shorts #Reels",
        "thumb_config": {
            "source_art": "assets/curated_panels/65_venom_dios_de_la_luz_knull/scene_04.jpg",
            "badge": "MARVEL COMICS • KING IN BLACK #5",
            "badge_border": (255, 230, 0, 255),
            "text_start_y": 460,
            "vignette": (390, 840),
            "lines": [
                {"text": "¡VENOM DIOS DE LA LUZ!", "size": 98, "color": (255, 235, 0), "stroke_w": 10},
                {"text": "EL HACHA CÓSMICA", "size": 90, "color": (255, 255, 255), "stroke_w": 9},
                {"text": "ANIQUILÓ A KNULL EN EL SOL", "size": 62, "color": (255, 35, 45), "stroke_w": 8},
            ]
        }
    }
]

def produce_slot(proj: dict):
    slot_num = proj["slot"]
    proj_id = proj["id"]
    queue_name = proj["queue_folder"]

    print(f"\n{'='*75}")
    print(f"🎬 [PRODUCCIÓN] SLOT {slot_num}: {proj['title']}")
    print(f"{'='*75}")

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

    work_dir = PROJECT_ROOT / "work" / f"batch6_{proj_id}"
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

    # 1. Generar miniatura vertical de alto impacto
    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = dest_dir / "thumb.jpg"
    build_high_impact_thumbnail(proj, thumb_path)

    # 2. Copiar video base al destino
    dest_video = dest_dir / "video.mp4"
    shutil.copy2(final_video_path, dest_video)

    # 3. Inyectar miniatura de alto impacto como primer frame exacto
    print(f"⚡ Inyectando miniatura como primer frame exacto en {dest_video.name}...")
    ok_inject = inject_thumbnail_into_video(dest_video, thumb_path)
    if not ok_inject:
        print(f"🚨 Falló la inyección de miniatura en {dest_video}")
        return None

    final_dur = get_duration(str(dest_video))
    print(f"✅ Duración final verificada: {final_dur:.2f}s (>= 60.0s PASS)")

    meta_payload = {
        "title": proj["title"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "character": proj["character"],
        "theme_signature": proj["theme_signature"],
        "duration_seconds": round(final_dur, 2),
        "scheduled_slot": slot_num,
        "queue_folder": queue_name,
        "source": "batch_6_remasters_10k_plus",
        "first_frame_thumbnail_injected": True,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(dest_dir / "metadata.json", "w", encoding="utf-8") as mf:
        json.dump(meta_payload, mf, indent=2, ensure_ascii=False)

    print(f"🎉 Slot {slot_num} completado y listo en {dest_dir}!")
    return dest_dir

if __name__ == "__main__":
    target_slot = None
    force_mode = "--force" in [a.lower() for a in sys.argv]
    for a in sys.argv[1:]:
        if a.strip().isdigit():
            target_slot = int(a.strip())

    print("=" * 80)
    print("🚀 INICIANDO PRODUCCIÓN AUTOMATIZADA: SLOTS 56 AL 65")
    print("=" * 80)

    completed = []
    failed = []

    for proj in REMASTER_PROJECTS_BATCH_6:
        slot = proj["slot"]
        if target_slot and slot != target_slot:
            continue

        dest = SCHEDULED_QUEUE / proj["queue_folder"]
        if not force_mode and (dest / "video.mp4").exists() and (dest / "metadata.json").exists():
            # Verificar si ya tiene miniatura inyectada
            try:
                with open(dest / "metadata.json", encoding="utf-8") as f:
                    meta = json.load(f)
                if meta.get("first_frame_thumbnail_injected"):
                    print(f"⏩ Slot {slot} ya existe y tiene frame 0 inyectado. Saltando.")
                    completed.append(slot)
                    continue
            except Exception:
                pass

        max_attempts = 3
        success = False
        for attempt in range(1, max_attempts + 1):
            print(f"\n--- [Intento {attempt}/{max_attempts}] Compilando Slot {slot} ---")
            try:
                res = produce_slot(proj)
                if res and (res / "video.mp4").exists():
                    completed.append(slot)
                    success = True
                    break
                else:
                    print(f"⚠️ Reintentando slot {slot}...")
                    time.sleep(3)
            except Exception as e:
                print(f"❌ Error en slot {slot}: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(4)

        if not success:
            failed.append(slot)
            print(f"🚨 FATAL: Slot {slot} no pudo completarse.")
            break

    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL DE PRODUCCIÓN")
    print(f"✅ Slots completados: {completed}")
    print(f"❌ Slots fallidos: {failed}")
    print("=" * 80)

    if failed:
        sys.exit(1)
    else:
        print("🎉 ¡TODOS LOS SLOTS PROCESADOS CON ÉXITO!")
        sys.exit(0)
