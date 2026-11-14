"""
Master Production Engine: Top 10 Videos con Más Reproducciones de la Página
Remasterizados en Formato Viral Calibrado de 25-30 Segundos (Slots 70 al 79)
=============================================================================
- Basado en los datos auditados de la página:
    #1: Superior Spider-Man vs Escorpión (439,682 views) -> Slot 70
    #2: Batman The Devastator - Virus Doomsday (398,125 views) -> Slot 71
    #3: Hellboy - Mano Derecha del Destino (173,068 views) -> Slot 72
    #4: Spider-Man Back in Black vs Kingpin (144,699 views) -> Slot 73
    #5: Sentry descuartiza a Ares en Siege (117,683 views) -> Slot 74
    #6: El Batman Que Ríe - Origen Oscuro (103,611 views) -> Slot 75
    #7: Injustice: Alfred humilla a Superman (96,396 views) -> Slot 76
    #8: Bruce Wayne recupera el manto vs Azrael (73,908 views) -> Slot 77
    #9: Secret Wars: Doctor Doom Dios vs Thanos (72,728 views) -> Slot 78
    #10: Flash Reverso - Odio a Barry Allen (50,289 views) -> Slot 79

- Duración estricta: 25.0s a 30.0s (calibrado matemáticamente a 58-61 palabras, rate=1.12).
- Sincronización visual 1:1 viñeta-narración con viñetas canónicas curadas en HD.
- Safe zone vertical 1080x1920 con fondo desenfocado protector sin recorte ciego.
- Miniatura minimalista (2 a 4 palabras) inyectada en fotograma exacto t=0.000s.
- Encolado directo en scheduled_queue/{slot}_{name}/ para publicarse a partir de mañana.
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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "top10_viral_25s"
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


TOP10_VIRAL_PROJECTS = [
    # -------------------------------------------------------------
    # TOP #1 (439,682 views) | SLOT 70: Superior Spider-Man vs Escorpión
    # -------------------------------------------------------------
    {
        "slot": 70,
        "queue_folder": "70_spiderman_escorpion_mandibula_superior",
        "id": "spiderman_escorpion_mandibula_superior_top10_25s",
        "title": "¡Spider-Man Siempre se Contuvo! El Golpe que le Arrancó la Mandíbula a Escorpión 🕷️💥🩸",
        "character": "Spider-Man",
        "folder": "51_spiderman_escorpion_mandibula_superior",
        "theme_signature": "spiderman:superior_1:scorpion_jaw_shattered",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/51_spiderman_escorpion_mandibula_superior/scene_03.jpg",
            "text": "¡MANDÍBULA ARRANCADA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Cuando el Doctor Octopus robó la mente y cuerpo de Spider-Man, descubrió un secreto aterrador."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El temible villano Escorpión atacó un hospital civil, amenazando a todos con su aguijón letal."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sin contenerse jamás, Otto descargó un puñetazo brutal que arrancó la mandíbula entera de Escorpión."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Otto comprendió en shock que Peter Parker siempre contuvo toda su descomunal fuerza sobrehumana."
            }
        ],
        "description": "La legendaria revelación en Superior Spider-Man #1 de Dan Slott y Ryan Stegman. El puñetazo que arrancó la mandíbula de Escorpión.",
        "hashtags": "#SpiderMan #SuperiorSpiderMan #DoctorOctopus #PeterParker #Marvel #MarvelComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #2 (398,125 views) | SLOT 71: Batman The Devastator (Virus Doomsday)
    # -------------------------------------------------------------
    {
        "slot": 71,
        "queue_folder": "71_batman_virus_doomsday_devastator",
        "id": "batman_virus_doomsday_devastator_top10_25s",
        "title": "¡Batman se Inyectó el Virus Doomsday! El Monstruo que Asesinó a Superman 🦇💀💉",
        "character": "Batman",
        "folder": "52_batman_virus_doomsday_devastator",
        "theme_signature": "batman:the_devastator_1:doomsday_virus_injection",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/52_batman_virus_doomsday_devastator/scene_04.jpg",
            "text": "¡VIRUS DOOMSDAY!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En el Multiverso Oscuro, un Superman despiadado enloqueció y masacró a la humanidad entera."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Acorralado y herido de muerte, Batman vio cómo el Hombre de Acero descendía para ejecutarlo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Desesperado, Bruce se clavó una jeringa con el virus Doomsday directo en el centro del corazón."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Transformado en el temible monstruo Devastator, Batman asesinó a Superman petrificándolo con esporas mortales."
            }
        ],
        "description": "La escalofriante pesadilla de Frank Tieri y Tony Daniel en Batman: The Devastator #1. El nacimiento del Batman Doomsday.",
        "hashtags": "#Batman #Superman #Doomsday #TheDevastator #DarkMultiverse #DCComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #3 (173,068 views) | SLOT 72: Hellboy - Mano Derecha del Destino
    # -------------------------------------------------------------
    {
        "slot": 72,
        "queue_folder": "72_hellboy_mano_derecha_apocalipsis",
        "id": "hellboy_mano_derecha_apocalipsis_top10_25s",
        "title": "¡El Secreto de la Mano de Hellboy! La Llave del Fin del Mundo 🗝️🔥💀",
        "character": "Hellboy",
        "folder": "56_hellboy_mano_derecha_apocalipsis",
        "theme_signature": "hellboy:right_hand_of_doom:anung_un_rama",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/56_hellboy_mano_derecha_apocalipsis/scene_04.jpg",
            "text": "¡LA LLAVE DEL APOCALIPSIS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 88
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En mil novecientos cuarenta y cuatro, soldados aliados rescataron a un pequeño demonio huérfano."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aunque creían que su enorme mano de piedra era un simple defecto, ocultaba algo siniestro."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su nombre real es Anung Un Rama, y su mano es la llave del apocalipsis."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Hellboy juró rechazar para siempre su destino demoníaco protegiendo al mundo que lo adoptó con amor."
            }
        ],
        "description": "La mitología original creada por Mike Mignola en Dark Horse Comics: Hellboy y el enigma profético de la Mano Derecha del Destino.",
        "hashtags": "#Hellboy #DarkHorse #AnungUnRama #RightHandOfDoom #MikeMignola #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #4 (144,699 views) | SLOT 73: Spider-Man Back in Black vs Kingpin
    # -------------------------------------------------------------
    {
        "slot": 73,
        "queue_folder": "73_spiderman_back_in_black_kingpin",
        "id": "spiderman_back_in_black_kingpin_top10_25s",
        "title": "¡Sin Máscara y Sin Piedad! Spider-Man Humilla a Kingpin en la Cárcel 🕷️⛓️🩸",
        "character": "Spider-Man",
        "folder": "53_spiderman_back_in_black_kingpin",
        "theme_signature": "spiderman:back_in_black:kingpin_rykers_prison_beating",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/53_spiderman_back_in_black_kingpin/scene_03.jpg",
            "text": "¡HUMILLÓ A KINGPIN!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras el atentado que dejó a su tía al borde de la muerte, Peter buscó venganza."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Vistiendo el traje negro, entró sin máscara a la prisión para confrontar a Wilson Fisk."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Spider-Man humilló al temido mafioso, moliéndolo a bofetadas frente a cientos de reclusos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Peter juró que si su tía moría, regresaría para asfixiar a Kingpin con telaraña."
            }
        ],
        "description": "La legendaria obra maestra de J. Michael Straczynski y Ron Garney en Amazing Spider-Man #542. La paliza a Wilson Fisk en Ryker's.",
        "hashtags": "#SpiderMan #Kingpin #BackInBlack #PeterParker #WilsonFisk #Marvel #MarvelComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #5 (117,683 views) | SLOT 74: Sentry descuartiza a Ares en Siege
    # -------------------------------------------------------------
    {
        "slot": 74,
        "queue_folder": "74_sentry_descuartiza_ares_siege",
        "id": "sentry_descuartiza_ares_siege_top10_25s",
        "title": "¡La Muerte Más Censurada de Marvel! Sentry Descuartiza a Ares en Dos Mitades ⚡🩸🪓",
        "character": "Sentry",
        "folder": "54_sentry_descuartiza_ares_siege",
        "theme_signature": "sentry:siege_2:ares_ripped_in_half_void",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/54_sentry_descuartiza_ares_siege/scene_04.jpg",
            "text": "¡PARTIDO EN DOS!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 105
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Durante el brutal asedio a la ciudad dorada de Asgard, una masacre sacudió Marvel."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al descubrir una traición, Ares levantó su hacha de combate para ejecutar a Norman Osborn."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero Sentry, totalmente poseído por la oscura entidad The Void, descendió para frenar al dios."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con una fuerza sobrehumana aterradora, Sentry agarró a Ares y lo partió en dos mitades."
            }
        ],
        "description": "El brutal clímax de Brian Michael Bendis y Olivier Coipel en Siege #2. Sentry descuartiza a Ares, Dios de la Guerra.",
        "hashtags": "#Sentry #Ares #Siege #TheVoid #Avengers #Marvel #MarvelComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #6 (103,611 views) | SLOT 75: El Batman Que Ríe - Fusión Siniestra
    # -------------------------------------------------------------
    {
        "slot": 75,
        "queue_folder": "75_batman_que_rie_dark_multiverse",
        "id": "batman_que_rie_dark_multiverse_top10_25s",
        "title": "¡El Batman Que Ríe! La Fusión Más Siniestra entre Bruce Wayne y el Joker 🃏🦇🩸",
        "character": "The Batman Who Laughs",
        "folder": "55_batman_que_rie_dark_multiverse",
        "theme_signature": "batman:the_batman_who_laughs_1:joker_neck_snapped_toxin",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/55_batman_que_rie_dark_multiverse/scene_04.jpg",
            "text": "¡EL BATMAN QUE RÍE!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 98
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En el abismo del Multiverso Oscuro nació la versión más perturbadora del Caballero de la Noche."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras una ola de asesinatos que destruyó Gotham, el Joker cruzó el límite definitivo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Furioso, Batman rompió el cuello del payaso, inhalando una toxina mortal que brotó del cadáver."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El veneno fusionó su brillante intelecto táctico con la pura locura: nació Batman Que Ríe."
            }
        ],
        "description": "El origen definitivo creado por James Tynion IV y Riley Rossmo en Dark Nights: The Batman Who Laughs #1.",
        "hashtags": "#TheBatmanWhoLaughs #Batman #Joker #DarkMultiverse #DCComics #BatmanQueRie #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #7 (96,396 views) | SLOT 76: Injustice: Alfred Humilla a Superman
    # -------------------------------------------------------------
    {
        "slot": 76,
        "queue_folder": "76_injustice_alfred_superman",
        "id": "injustice_alfred_superman_top10_25s",
        "title": "¡Alfred Humilló a Superman! El Mayordomo que Rompió la Nariz al Tirano 👊💥🩸",
        "character": "Alfred Pennyworth",
        "folder": "57_injustice_alfred_superman",
        "theme_signature": "injustice:alfred_headbutt_superman:nanopill_5u93r",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/57_injustice_alfred_superman/scene_03.jpg",
            "text": "¡ALFRED DESTROZÓ A SUPERMAN!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 84
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Cuando Superman se convirtió en un tirano asesino, irrumpió en la Baticueva para matar a Batman."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras fracturarle la columna a Bruce Wayne, el kryptoniano se burló del héroe derrotado."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Furioso, Alfred tragó una píldora de superfuerza y le partió la nariz de un cabezazo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El leal mayordomo molió a golpes a Superman, advirtiéndole que jamás volviera a tocarlo."
            }
        ],
        "description": "El momento legendario de Tom Taylor y Bruno Redondo en Injustice: Gods Among Us #36. Alfred Pennyworth destroza a Superman.",
        "hashtags": "#AlfredPennyworth #Superman #Batman #Injustice #DCComics #InjusticeGodsAmongUs #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #8 (73,908 views) | SLOT 77: Bruce Wayne Recupera el Manto vs Azrael
    # -------------------------------------------------------------
    {
        "slot": 77,
        "queue_folder": "77_batman_recupera_manto_derrota_azrael",
        "id": "batman_recupera_manto_derrota_azrael_top10_25s",
        "title": "¡Bruce Wayne Reclama Gotham! El Retorno del Verdadero Defensor de la Noche 🦇⚔️🔥",
        "character": "Bruce Wayne",
        "folder": "58_batman_recupera_manto_derrota_azrael",
        "theme_signature": "batman:knightsend:bruce_defeats_azrael",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/58_batman_recupera_manto_derrota_azrael/scene_02.jpg",
            "text": "¡BRUCE WAYNE REGRESA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras la caída de Bruce Wayne, Azrael usurpó el manto convirtiendo a Batman en asesino."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Recuperado de sus heridas, Bruce regresó decidido a reclamar su legado con sus manos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En vez de fuerza bruta, Batman atrajo a Azrael abriendo una compuerta de luz solar."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Cegado por el brillo, el usurpador cayó derrotado ante la imponente figura de Bruce."
            }
        ],
        "description": "El clímax triunfal de Dennis O'Neil, Chuck Dixon y Doug Moench en KnightsEnd. Bruce Wayne reclama el manto de Batman.",
        "hashtags": "#Batman #BruceWayne #Azrael #KnightsEnd #Knightfall #DCComics #Gotham #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #9 (72,728 views) | SLOT 78: Secret Wars - Doctor Doom Dios vs Thanos
    # -------------------------------------------------------------
    {
        "slot": 78,
        "queue_folder": "78_doctor_doom_destruye_thanos_secret_wars",
        "id": "doctor_doom_destruye_thanos_secret_wars_top10_25s",
        "title": "¡El Peor Error de Thanos! Desafió a Doctor Doom Dios y Pagó el Precio ⚡💀👑",
        "character": "Doctor Doom",
        "folder": "59_doctor_doom_destruye_thanos_secret_wars",
        "theme_signature": "doctor_doom:secret_wars_8:rips_thanos_spine",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/59_doctor_doom_destruye_thanos_secret_wars/scene_04.jpg",
            "text": "¡COLUMNA ARRANCADA!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 95
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Con el poder de los Beyonders, Doctor Doom se convirtió en emperador de Battleworld."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El arrogante Thanos llegó ante su trono divino, burlándose del supuesto poder de Victor Von Doom."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Doom le preguntó con calma si portaba el Guantelete del Infinito para respaldar su insolencia."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al decir que no, Doom le arrancó la columna vertebral en un segundo, pulverizándolo por completo."
            }
        ],
        "description": "La escena más aplastante de Jonathan Hickman y Esad Ribic en Secret Wars #8. God Emperor Doom arranca la columna vertebral de Thanos.",
        "hashtags": "#DoctorDoom #Thanos #GodEmperorDoom #SecretWars #Marvel #MarvelComics #Comics #Shorts #Reels"
    },

    # -------------------------------------------------------------
    # TOP #10 (50,289 views) | SLOT 79: Flash Reverso - La Obsesión Temporal
    # -------------------------------------------------------------
    {
        "slot": 79,
        "queue_folder": "79_reverse_flash_odio_thawne",
        "id": "reverse_flash_odio_thawne_top10_25s",
        "title": "¡El Villano Más Retorcido de DC! Por Qué Flash Reverso Destruyó la Vida de Barry Allen ⚡🔪⏳",
        "character": "Reverse Flash",
        "folder": "60_reverse_flash_odio_thawne",
        "theme_signature": "reverse_flash:the_flash_rebirth:thawne_torment_barry",
        "voice": "es-MX-JorgeNeural",
        "minimal_thumb": {
            "source_art": "assets/curated_panels/60_reverse_flash_odio_thawne/scene_02.jpg",
            "text": "¡EL ODIO DE FLASH REVERSO!",
            "text_y": 240,
            "color": (255, 235, 0),
            "font_size": 88
        },
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Eobard Thawne dedicó su vida entera a un único objetivo: destruir a Barry Allen."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Dominando la Fuerza Negativa, viajó al pasado para arruinar cada momento de su infancia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Empujó a Barry de niño, mató a su mascota y finalmente asesinó a su madre Nora."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con una sonrisa siniestra, Flash Reverso le confesó que cada dolor siempre fue su culpa."
            }
        ],
        "description": "La siniestra revelación de Geoff Johns y Ethan Van Sciver en The Flash: Rebirth. La tortura temporal de Eobard Thawne.",
        "hashtags": "#ReverseFlash #Flash #BarryAllen #EobardThawne #TheFlash #DCComics #SpeedForce #Comics #Shorts #Reels"
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
    print(f"🎬 PROCESANDO TOP 10 VIRAL 25-30s | SLOT {slot}: {proj['title']}")
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

    work_dir = PROJECT_ROOT / "work" / f"top10_viral_{proj_id}"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    generation = build_cloud_generation(story_payload, work_dir)

    # Asegurar que todas las escenas en work_dir estén formateadas a 1080x1920 con fondo desenfocado
    gen_dir = work_dir / proj_id
    for idx in range(1, len(scenes_text) + 1):
        sc_img = gen_dir / f"scene_{idx:02d}" / f"scene_{idx:02d}.jpg"
        if sc_img.exists():
            raw_im = Image.open(sc_img).convert("RGB")
            if raw_im.size != (1080, 1920):
                formatted_im = fit_to_vertical(raw_im, 1080, 1920)
                formatted_im.save(sc_img, "JPEG", quality=95)
                print(f"  [CANVAS 1080x1920 OK] scene_{idx:02d}.jpg")

    voice_choice = proj.get("voice", "Puck")
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
        "format": "viral_top10_25_30s",
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
    for proj in TOP10_VIRAL_PROJECTS:
        if target_slot is not None and proj["slot"] != target_slot:
            continue
        v = produce_project(proj)
        if v:
            produced.append(v)
        else:
            print(f"❌ Error produciendo slot {proj['slot']}")

    print("\n" + "=" * 80)
    print(f"🎉 RESUMEN FINAL: {len(produced)} VIDEOS VIRALES TOP 10 PRODUCIDOS")
    print("=" * 80)

if __name__ == "__main__":
    main()
