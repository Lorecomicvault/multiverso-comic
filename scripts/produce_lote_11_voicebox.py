"""
Production & Scheduling Engine: Lote 11 (Slots 107 al 116)
===========================================================
- Duración objetivo estricta: 25 a 30 segundos
- Locución: Voicebox CUDA 'Narrador Referencia Cómic' (28078056-1a1d-43d4-9d57-d616275f13c2)
- Precisión quirúrgica 1:1 entre narrativa y viñeta mostrada en pantalla
- Miniatura minimalista de alto impacto estampada en frame 0 (t=0.000s)
- Transiciones 3D de papel rasgado + Foley + subtítulos Bangers activos
- Destino: 'scheduled_queue/107_...' a 'scheduled_queue/116_...'
"""

import os
import sys
import json
import time
import shutil
import requests
import subprocess
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageFont, ImageDraw

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.composer import compose_scene_from_image, get_duration
from src.transcribe import extract_scene_word_timings
from src.comic_pipeline import assemble_reel
from src.social_overlay import get_or_create_vertical_cta_mov

CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2" # Narrador Referencia Cómic

FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
if not Path(FONT_IMPACT).exists():
    FONT_IMPACT = r"C:\Users\Vanes\comics en espanol\fonts\impact.ttf"

LOTE_11_PROJECTS = [
    {
        "slot": 107,
        "id": "107_morlun_devora_ojo_spiderman",
        "queue_folder": "107_morlun_devora_ojo_spiderman",
        "title": "Spider-Man: ¡La Pesadilla de Morlun y la Maldición Totémica! 🕷️👁️",
        "character": "Spider-Man",
        "folder": "morlun_devora_ojo_spiderman",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Morlun camina entre el fuego infernal, un cazador implacable que no siente dolor ni cansancio."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Peter Parker y Ezekiel lo golpean con todo lo que tienen en un combate frenético."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Spider-Man intenta emboscarlo desde las alturas de la ciudad mientras el vampiro lo acecha."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Pero la maldición totémica despierta, haciendo que aterradores ojos rojos broten de las manos de Morlun."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/morlun_devora_ojo_spiderman/scene_04.jpg",
            "text": "OJOS EN MANOS",
            "text_y": 240,
            "font_size": 110,
            "color": (255, 235, 0)
        },
        "description": "El terrorífico enfrentamiento de Spider-Man contra el depredador totémico Morlun, donde la pesadilla cobra vida.",
        "hashtags": "#SpiderMan #Morlun #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 108,
        "id": "108_magneto_fatal_attractions",
        "queue_folder": "108_magneto_fatal_attractions",
        "title": "Magneto: ¡El Desgarro de Adamantium a Wolverine! 🧲🩸",
        "character": "Magneto",
        "folder": "magneto_fatal_attractions",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Los X-Men irrumpen en la estación espacial Avalon equipados con armaduras tácticas para detener a Magneto."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero el amo del magnetismo desata su furia y arranca el adamantium líquido de Wolverine."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Logan grita en agonía pura mientras el metal incandescente brota despedazando cada poro de su cuerpo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Horrorizado por la masacre, Charles Xavier utiliza todo su poder psiónico para apagar la mente de Magneto."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/magneto_fatal_attractions/scene_03.jpg",
            "text": "DOLOR ABSOLUTO",
            "text_y": 240,
            "font_size": 110,
            "color": (255, 235, 0)
        },
        "description": "Magneto arranca el adamantium líquido de los huesos de Wolverine y Charles Xavier cruza el límite final.",
        "hashtags": "#Wolverine #Magneto #XMen #FatalAttractions #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 109,
        "id": "109_superman_vs_the_elite",
        "queue_folder": "109_superman_vs_the_elite",
        "title": "Superman: ¡La Lección Definitiva a The Elite! 🦸‍♂️💥",
        "character": "Superman",
        "folder": "superman_vs_the_elite",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Una ciudad en ruinas arde tras la masacre despiadada de una criatura biomecánica colosal."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aparece The Elite, un sangriento grupo de antihéroes liderado por el arrogante Manchester Black."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero Superman no tolera su barbarie asesina y se alza imponente con sus ojos en llamas."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Manchester Black enciende su encendedor con burla, sin sospechar el terrible castigo que está por recibir."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/superman_vs_the_elite/scene_03.jpg",
            "text": "SUPERMAN SIN LÍMITES",
            "text_y": 240,
            "font_size": 98,
            "color": (255, 235, 0)
        },
        "description": "Superman demuestra por qué la justicia jamás debe ceder ante la barbarie asesina de The Elite.",
        "hashtags": "#Superman #TheElite #ManchesterBlack #DCComics #ActionComics775 #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 110,
        "id": "110_darth_vader_down",
        "queue_folder": "110_darth_vader_down",
        "title": "Darth Vader: ¡Solo Rodeado de Miedo y Hombres Muertos! ⚔️🌌",
        "character": "Darth Vader",
        "folder": "darth_vader_down",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras un devastador combate aéreo, Darth Vader camina solitario entre las áridas dunas del planeta."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su nave TIE colisionó en pleno vuelo contra el Ala-X de Luke en una explosión gigantesca."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cientos de soldados rebeldes y tanques pesados lo rodean apuntándole con rifles desde cada colina."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Han Solo y Luke abren fuego, pero el Lord Sith frena cada disparo láser con la Fuerza."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/darth_vader_down/scene_03.jpg",
            "text": "SOLO Y RODEADO",
            "text_y": 240,
            "font_size": 110,
            "color": (255, 235, 0)
        },
        "description": "Darth Vader derribado en Vrogas Vas demuestra por qué un ejército entero no es suficiente para vencerlo.",
        "hashtags": "#DarthVader #StarWars #VaderDown #Sith #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 111,
        "id": "111_joker_death_of_the_family",
        "queue_folder": "111_joker_death_of_the_family",
        "title": "Joker: ¡El Rostro Engrapado de Death of the Family! 🃏🩸",
        "character": "Joker",
        "folder": "06_joker_mascara_cara_rebanada_death_of_family",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En una celda de Arkham, el Joker permitió que Dollmaker le rebanara la piel del rostro."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Un año después, regresa con su propio rostro podrido y deforme engrapado macabramente a su cráneo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Oculto en las sombras, vigila a toda la batifamilia en un siniestro altar de monitores."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El payaso del crimen emerge arrastrándose entre enjambres de moscas, listo para torturar a Gotham."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/06_joker_mascara_cara_rebanada_death_of_family/scene_02.jpg",
            "text": "ROSTRO ENGRAPADO",
            "text_y": 240,
            "font_size": 105,
            "color": (255, 235, 0)
        },
        "description": "La siniestra reaparición del Joker con su rostro amputado y engrapado en Death of the Family.",
        "hashtags": "#Joker #Batman #DeathOfTheFamily #DCComics #Gotham #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 112,
        "id": "112_nova_annihilus_desgarro",
        "queue_folder": "112_nova_annihilus_desgarro",
        "title": "Nova Prime: ¡El Desgarro Cósmico de Annihilus! 💫💥",
        "character": "Nova",
        "folder": "nova_annihilus_desgarro",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Annihilus y su implacable enjambre insectoide barren galaxias enteras, dejando mundos convertidos en cenizas."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Richard Rider contempla la devastación de su hogar y promete vengar a todo su pueblo caído."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "El héroe absorbe la totalidad del poder cósmico Nova, haciendo que su armadura resplandezca intensamente."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En el duelo definitivo, Nova hunde su puño en la garganta de Annihilus y desgarra sus entrañas."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/nova_annihilus_desgarro/scene_04.jpg",
            "text": "DESGARRO CÓSMICO",
            "text_y": 240,
            "font_size": 105,
            "color": (255, 235, 0)
        },
        "description": "Richard Rider absorbe la Fuerza Nova completa y ejecuta la venganza más salvaje contra Annihilus en Annihilation.",
        "hashtags": "#Nova #Annihilus #Annihilation #MarvelComics #CosmicMarvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 113,
        "id": "113_wonderwoman_hiketeia_bota_batman",
        "queue_folder": "113_wonderwoman_hiketeia_bota_batman",
        "title": "Wonder Woman: ¡La Bota Amazona que Humilló a Batman! ⚔️👑",
        "character": "Wonder Woman",
        "folder": "wonderwoman_hiketeia_bota_batman",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Las Furias exigen sangre y castigo invocando el antiguo y sagrado ritual griego de la Hiketeia."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Wonder Woman jura proteger a una joven fugitiva, desatando una violenta batalla para defender su honor."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Batman llega decidido a arrestar a la criminal, pero bajo la lluvia torrencial es derribado al suelo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "La amazona aplasta con su bota la cabeza del Murciélago, demostrándole que el honor divino es inquebrantable."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/wonderwoman_hiketeia_bota_batman/scene_04.jpg",
            "text": "LA BOTA DE DIANA",
            "text_y": 240,
            "font_size": 105,
            "color": (255, 235, 0)
        },
        "description": "El juramento sagrado de la Hiketeia enfrenta a Wonder Woman y Batman en una humillación inolvidable.",
        "hashtags": "#WonderWoman #Batman #TheHiketeia #DCComics #JusticeLeague #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 114,
        "id": "114_zombies_consumen_galactus_poder_infinito",
        "queue_folder": "114_zombies_consumen_galactus_poder_infinito",
        "title": "Marvel Zombies: ¡El Festín que Devoró a Galactus! 🧟‍♂️🌌",
        "character": "Marvel Zombies",
        "folder": "zombies_consumen_galactus_poder_infinito",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "El hambre insaciable consume la Tierra mientras un zombificado Spider-Man y Hulk pierden toda su humanidad."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Galactus aterriza entre los rascacielos derruidos proclamando que el planeta entero será destruido y consumido."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero los Vengadores infectados no temen al devorador cósmico y se lanzan a despedazar su carne viva."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En los confines del espacio, seres alienígenas descubren horrorizados que los zombis ahora tienen poder cósmico."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/zombies_consumen_galactus_poder_infinito/scene_03.jpg",
            "text": "DEVORANDO A GALACTUS",
            "text_y": 240,
            "font_size": 95,
            "color": (255, 235, 0)
        },
        "description": "Los Vengadores Zombis despedazan y consumen vivo al devorador de mundos Galactus para apoderarse del poder cósmico.",
        "hashtags": "#MarvelZombies #Galactus #SpiderMan #Hulk #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 115,
        "id": "115_captain_america_asesinato_civil_war",
        "queue_folder": "115_captain_america_asesinato_civil_war",
        "title": "Capitán América: ¡El Asesinato en los Tribunales! 🇺🇸🩸",
        "character": "Capitán América",
        "folder": "captain_america_asesinato_civil_war",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Una multitud conmocionada rodea los tribunales mientras el Capitán América es trasladado bajo una densa custodia."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "En los callejones cercanos, criminales y francotiradores ejecutan un complot despiadado coordinado por Cráneo Rojo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Steve Rogers recibe disparos a quemarropa, desplomándose gravemente herido en las frías escaleras del palacio judicial."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Falcon contempla desconsolado la caída de su hermano de armas, recordando las batallas libradas por la justicia."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/captain_america_asesinato_civil_war/scene_03.jpg",
            "text": "LA MUERTE DE CAP",
            "text_y": 240,
            "font_size": 105,
            "color": (255, 235, 0)
        },
        "description": "El trágico final de Civil War: Steve Rogers asesinado a sangre fría en las escaleras del tribunal de Nueva York.",
        "hashtags": "#CaptainAmerica #CivilWar #DeathOfCaptainAmerica #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 116,
        "id": "116_wolverine_muerte_adamantium",
        "queue_folder": "116_wolverine_muerte_adamantium",
        "title": "Wolverine: ¡La Muerte Definitiva Bañado en Adamantium! 🐺⚔️",
        "character": "Wolverine",
        "folder": "wolverine_muerte_adamantium",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Sin factor curativo y con el cuerpo agotado, Wolverine empuña sus armas para su misión definitiva."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "En los laboratorios de Arma X, el doctor Cornelius descubre aterrado que Logan viene a detenerlo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Para salvar a sujetos inocentes, Wolverine revienta los tanques y queda bañado completamente en adamantium líquido."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Bajo el sol del atardecer, Logan se arrodilla convertido en una estatua sólida de metal, descansando en paz."
            }
        ],
        "minimal_thumb": {
            "source_art": "assets/curated_panels/wolverine_muerte_adamantium/scene_04.jpg",
            "text": "ESTATUA DE ADAMANTIUM",
            "text_y": 240,
            "font_size": 92,
            "color": (255, 235, 0)
        },
        "description": "El épico y conmovedor sacrificio de Logan en La Muerte de Wolverine, convertido en una estatua eterna de adamantium.",
        "hashtags": "#Wolverine #DeathOfWolverine #Logan #WeaponX #MarvelComics #Comics #Shorts #Reels #TikTok"
    }
]

def restart_voicebox_cuda():
    print("  [Auto-Heal] Reiniciando Voicebox CUDA Server para limpiar VRAM...")
    subprocess.run(["powershell", "-Command", "Stop-Process -Name voicebox-server-cuda -Force -ErrorAction SilentlyContinue"], capture_output=True)
    time.sleep(2)
    exe_path = r"C:\Users\Vanes\AppData\Roaming\sh.voicebox.app\backends\cuda\voicebox-server-cuda.exe"
    work_dir = r"C:\Users\Vanes\AppData\Roaming\sh.voicebox.app\backends\cuda"
    subprocess.Popen([exe_path], cwd=work_dir, creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0)
    for i in range(25):
        time.sleep(1.0)
        try:
            r = requests.get(f"{VOICEBOX_URL}/profiles", timeout=2)
            if r.status_code == 200:
                print(f"  [Auto-Heal] Voicebox CUDA listo y operativo ({i+1}s).")
                return True
        except Exception:
            pass
    print("  [Auto-Heal Warning] No se pudo verificar respuesta inmediata.")
    return False

def synthesize_voicebox_scene(text: str, out_wav: Path) -> Path:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    payload = {'profile_id': PROFILE_ID, 'text': text}
    
    for outer_retry in range(1, 4):
        gen_id = None
        for attempt in range(1, 4):
            try:
                res = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=20)
                if res.status_code == 200:
                    gen_id = res.json().get('id')
                    break
            except Exception:
                time.sleep(2)
                
        if not gen_id:
            print("  [Voicebox] No se pudo conectar al endpoint, intentando reiniciar CUDA...")
            restart_voicebox_cuda()
            continue

        oom_detected = False
        for _ in range(80):
            time.sleep(1.0)
            try:
                st = requests.get(f"{VOICEBOX_URL}/generate/{gen_id}/status", timeout=10)
                for line in st.text.splitlines():
                    if line.startswith('data:'):
                        j = json.loads(line[5:].strip())
                        status = j.get('status')
                        if status == 'completed':
                            audio_res = requests.get(f"{VOICEBOX_URL}/audio/{gen_id}", timeout=25)
                            raw_tmp = str(out_wav) + '.raw.wav'
                            with open(raw_tmp, 'wb') as f:
                                f.write(audio_res.content)
                            subprocess.run([
                                'ffmpeg', '-y', '-i', raw_tmp,
                                '-af', 'aresample=48000,apad=pad_dur=0.25',
                                '-acodec', 'pcm_s16le', str(out_wav)
                            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            if Path(raw_tmp).exists():
                                Path(raw_tmp).unlink()
                            return out_wav
                        elif status == 'failed':
                            err = j.get('error', '')
                            if 'CUDA' in err or 'memory' in err.lower():
                                print(f"  [Voicebox OOM detectado]: {err}")
                                restart_voicebox_cuda()
                                oom_detected = True
                                break
                            else:
                                raise RuntimeError(f"Voicebox falló: {err}")
            except Exception as e:
                if "CUDA" in str(e) or "memory" in str(e).lower():
                    restart_voicebox_cuda()
                    oom_detected = True
                    break
                elif "Voicebox falló" in str(e):
                    raise e
            if oom_detected:
                break
        if not oom_detected and gen_id:
            break
            
    raise TimeoutError(f"Voicebox timeout para: {text[:30]}")

def apply_cinematic_grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.22)
    im = ImageEnhance.Color(im).enhance(1.20)
    return im

def fit_to_vertical(im: Image.Image, target_w=1080, target_h=1920) -> Image.Image:
    w, h = im.size
    aspect = w / h
    target_aspect = target_w / target_h

    if aspect > target_aspect:
        bg_scale = target_h / h
        bg = im.resize((int(w * bg_scale), target_h), Image.Resampling.LANCZOS)
        left = (bg.width - target_w) // 2
        bg = bg.crop((left, 0, left + target_w, target_h))
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
                              text_y=240, text_color=(255, 235, 0), font_size=95):
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
    if res.returncode == 0 and temp_out.exists():
        video_path.unlink()
        shutil.move(temp_out, video_path)
        return True
    return False

def produce_single_lote11_project(proj: dict):
    slot_num = proj["slot"]
    queue_folder_name = proj["queue_folder"]
    title = proj["title"]
    print(f"\n=======================================================")
    print(f"🎬 [LOTE 11 - SLOT {slot_num}] {queue_folder_name}")
    print(f"   Título: {title}")
    print(f"   Perfil de Voz: Narrador Referencia Cómic (Voicebox CUDA)")
    print(f"=======================================================")

    work_dir = PROJECT_ROOT / "work" / f"voicebox_lote11_slot_{slot_num:03d}"
    work_dir.mkdir(parents=True, exist_ok=True)
    curated_dir = PROJECT_ROOT / "assets" / "curated_panels" / proj["folder"]

    # 1. Synthesize 4 scenes with Voicebox
    raw_audios = {}
    for sc in proj["scenes"]:
        sn = sc["scene_number"]
        txt = sc["text"]
        out_wav = work_dir / f"raw_scene_{sn:02d}.wav"
        if not out_wav.exists() or out_wav.stat().st_size < 5000:
            print(f"  [Voicebox] Sintetizando Escena {sn}/4: {txt[:45]}...")
            synthesize_voicebox_scene(txt, out_wav)
            time.sleep(0.3)
        raw_audios[sn] = out_wav

    raw_durs = [get_duration(str(raw_audios[sn])) for sn in sorted(raw_audios.keys())]
    sum_raw = sum(raw_durs)
    print(f"  [Voicebox Raw Durations]: {[f'{d:.2f}s' for d in raw_durs]} | Suma: {sum_raw:.2f}s")

    # Calibrate atempo: target narration audio duration around 27.2 seconds
    # After 3 paper tear overlaps (-1.95s) + frame0 (+0.40s) = ~25.6s - 26.5s
    target_audio = 27.2
    calibrated_speed = sum_raw / target_audio
    calibrated_speed = max(0.82, min(0.96, calibrated_speed))
    print(f"  [Calibration] Factor atempo: {calibrated_speed:.3f}")

    calibrated_dir = work_dir / "calibrated"
    calibrated_dir.mkdir(parents=True, exist_ok=True)
    voice_results = {}
    for sn, raw_w in raw_audios.items():
        cal_w = calibrated_dir / f"scene_{sn:02d}.wav"
        txt = proj["scenes"][sn-1]["text"]
        subprocess.run([
            'ffmpeg', '-y', '-i', str(raw_w),
            '-af', f'atempo={calibrated_speed:.3f},apad=pad_dur=0.35',
            '-c:a', 'pcm_s16le', str(cal_w)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        voice_results[sn] = {'audio': str(cal_w), 'text': txt}

    full_audio = str(work_dir / "narration_full.wav")
    audio_inputs = []
    filter_inputs = []
    for idx, sn in enumerate(sorted(voice_results.keys())):
        audio_inputs.extend(['-i', voice_results[sn]['audio']])
        filter_inputs.append(f'[{idx}:a]')
    a_filter = f"{''.join(filter_inputs)}concat=n={len(filter_inputs)}:v=0:a=1[aout]"
    subprocess.run(['ffmpeg', '-y', *audio_inputs, '-filter_complex', a_filter, '-map', '[aout]', full_audio],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_audio_dur = get_duration(full_audio)
    print(f"  [Audio Total Calibrado]: {total_audio_dur:.2f}s")

    # 2. Ken Burns Panels
    composed_dir = work_dir / "composed"
    composed_dir.mkdir(parents=True, exist_ok=True)
    composed_scenes = []
    motion_map = {1: 0, 2: 1, 3: 2, 4: 3}

    for sc in proj["scenes"]:
        sn = sc["scene_number"]
        src_img = str(curated_dir / sc["file"])
        audio_path = voice_results[sn]['audio']
        dur = get_duration(audio_path)
        out_clip = str(composed_dir / f"scene_{sn:02d}.mp4")
        compose_scene_from_image(src_img, audio_path, dur, out_clip, pattern_idx=motion_map.get(sn, 0), width=1080, height=1920)
        composed_scenes.append(out_clip)

    # 3. Whisper Timestamps
    word_json = str(work_dir / "word_timings.json")
    words_data = extract_scene_word_timings(voice_results, word_json, language='es', model_name='base')
    words_timing = [{"word": w['text'], "start": w['start'], "end": w['end']} for w in words_data.get('words', [])]

    # Resaltado de palabras clave
    keywords = [proj["character"].upper()]
    for sc in proj["scenes"]:
        for w in sc["text"].split():
            clean_w = ''.join(c for c in w if c.isalnum()).upper()
            if len(clean_w) > 4:
                keywords.append(clean_w)
    keywords = list(set(keywords))[:20]

    # 4. Ensamblar Reel
    master_mp4 = str(work_dir / "master.mp4")
    social_mov = get_or_create_vertical_cta_mov("motion")
    hook_short = title.split('!')[0] + '!' if '!' in title else title[:35]

    assemble_reel(
        panel_clips=composed_scenes,
        words_timing=words_timing,
        narration_audio=full_audio,
        output_mp4=master_mp4,
        work_dir=str(work_dir / "assemble_work"),
        keywords=keywords,
        social_cta_mov=social_mov,
        cta_start_time=max(8.0, min(total_audio_dur - 7.0, total_audio_dur * 0.58)),
        alignment=5,
        margin_v=20,
        font_size=58,
        hook_title=hook_short
    )

    assembled_dur = get_duration(master_mp4)
    print(f"  [Video Ensamblado]: {assembled_dur:.2f}s")

    # 5. Renderizar miniatura minimalista e inyectar en frame 0
    min_cfg = proj["minimal_thumb"]
    art_path = PROJECT_ROOT / min_cfg["source_art"]
    thumb_path = work_dir / "thumb.jpg"
    render_minimal_text_thumb(
        image_path=art_path,
        text=min_cfg["text"],
        output_path=thumb_path,
        text_y=min_cfg.get("text_y", 240),
        text_color=min_cfg.get("color", (255, 235, 0)),
        font_size=min_cfg.get("font_size", 95)
    )
    inject_thumbnail_into_video(Path(master_mp4), thumb_path)
    final_dur = get_duration(master_mp4)
    print(f"  [DURACIÓN FINAL CON FRAME 0]: {final_dur:.2f}s")

    # 6. Escribir a scheduled_queue
    target_dir = SCHEDULED_QUEUE / queue_folder_name
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(master_mp4, target_dir / "video.mp4")
    shutil.copy2(thumb_path, target_dir / "thumb.jpg")

    meta = {
        "slot": slot_num,
        "queue_folder": queue_folder_name,
        "id": proj["id"],
        "title": proj["title"],
        "character": proj["character"],
        "description": proj.get("description", ""),
        "hashtags": proj.get("hashtags", ""),
        "duration": round(final_dur, 2),
        "video_file": "video.mp4",
        "thumbnail_file": "thumb.jpg",
        "format": "viral_25_30s",
        "voice_profile": "Narrador Referencia Cómic (Voicebox Profile 28078056-1a1d-43d4-9d57-d616275f13c2)",
        "voice_engine": "Voicebox Local CUDA",
        "produced_at": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    meta_path = target_dir / "metadata.json"
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"✅ Slot {slot_num} programado con éxito en: {target_dir} ({final_dur:.2f}s)")
    return final_dur

def main():
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    results = []
    start_all = time.time()

    print("=================================================================")
    print("INICIANDO PRODUCCIÓN DE LOTE 11 (SLOTS 107 AL 116) CON VOICEBOX")
    print("=================================================================")

    for proj in LOTE_11_PROJECTS:
        slot = proj["slot"]
        q_dir = SCHEDULED_QUEUE / proj["queue_folder"]
        v_file = q_dir / "video.mp4"
        m_file = q_dir / "metadata.json"

        # Check if already completed and within 25.0 - 30.0s
        if v_file.exists() and m_file.exists() and v_file.stat().st_size > 5_000_000:
            dur = get_duration(str(v_file))
            if 25.0 <= dur <= 30.0:
                print(f"[SKIP] Slot {slot} ({proj['queue_folder']}) ya completado con éxito ({dur:.2f}s).")
                results.append((slot, proj["queue_folder"], proj["title"], dur, "OK (Cached)"))
                continue

        try:
            dur = produce_single_lote11_project(proj)
            status = "OK" if 25.0 <= dur <= 30.0 else f"WARNING ({dur:.1f}s)"
            results.append((slot, proj["queue_folder"], proj["title"], dur, status))
        except Exception as e:
            print(f"[ERROR CRÍTICO] en Slot {slot}: {e}")
            import traceback
            traceback.print_exc()
            results.append((slot, proj["queue_folder"], proj["title"], 0.0, f"ERROR: {e}"))

    elapsed = time.time() - start_all
    print("\n=================================================================")
    print(f"REPORTE DE AUDITORÍA FINAL - LOTE 11 (Tiempo: {elapsed/60:.2f} min)")
    print("=================================================================")
    print(f"{'Slot':<6} | {'Duración':<10} | {'Estado':<14} | {'Carpeta':<42} | {'Título'}")
    print("-" * 110)
    for slot, q_f, title, dur, st in results:
        print(f"{slot:<6} | {dur:<10.2f} | {st:<14} | {q_f:<42} | {title}")
    print("=================================================================")

if __name__ == "__main__":
    main()
