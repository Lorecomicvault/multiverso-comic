"""
Voicebox Production & Scheduling Engine: 10 Videos Virales (Voz Clonada)
=======================================================================
Voz: 'Narrador Referencia Cómic' (Voicebox CUDA Local, Profile ID: 28078056-1a1d-43d4-9d57-d616275f13c2)
Formato: 1080x1920 (Vertical 9:16 para Shorts, Reels y TikTok)
Duración: 50 a 65 segundos por video
Destino: Staging completo en 'scheduled_queue/' para publicación automática vía GitHub Actions Cronjobs.
"""

import os
import sys
import json
import time
import shutil
import requests
import subprocess
from pathlib import Path

# Force UTF-8 stdout
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

from src.composer import (
    compose_scene_from_image,
    get_duration,
    extract_thumbnail
)
from src.transcribe import extract_scene_word_timings
from src.comic_pipeline import assemble_reel
from src.social_overlay import get_or_create_vertical_cta_mov

CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
OUTPUT_BASE = PROJECT_ROOT / "output" / "batch_10_nuevos_virales_60s"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2" # Narrador Referencia Cómic

PROJECTS = [
    {
        "id": "01_wonder_woman_ceguera_medusa",
        "queue_folder": "13_dia4_07h_wonder_woman_ceguera_medusa",
        "title": "Wonder Woman: ¡El Sacrificio Ciego que Destruyó a Medusa! ⚔️🐍",
        "character": "Wonder Woman",
        "folder": "wonder_woman_ceguera_medusa",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Resucitada por la hechicera Circe en medio de un coliseo moderno abarrotado, la temible Gorgona Medusa desafió a Wonder Woman a un duelo a muerte transmitido en vivo ante la mirada aterrada de todo el planeta."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con miles de inocentes como rehenes, Diana de Themyscira descendió a la arena sabiendo que el más mínimo reflejo en los ojos de Medusa convertiría su carne amazona en estatua de piedra sólida para siempre."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sabiendo que no podría vencer con la mirada descubierta, Diana tomó una decisión desgarradora: agarró una serpiente venenosa viva y frotó su letal fluido directamente sobre sus pupilas, quemando su vista en una agonía indescriptible."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Completamente ciega y guiándose únicamente por las vibraciones del aire y su instinto guerrero milenario, la princesa amazona esquivó las garras de la Gorgona y cercenó su cabeza de un solo tajo de espada."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Alzando el trofeo sangriento en alto, Wonder Woman demostró que el verdadero poder de un héroe no reside en sus ojos, sino en la inquebrantable pureza de su alma. ¿Fue este su sacrificio más glorioso?"
            }
        ],
        "description": "El día en que Wonder Woman se arrancó la vista con veneno de serpiente para decapitar a Medusa y salvar a miles de inocentes. La hazaña más heroica de DC Comics.",
        "hashtags": "#WonderWoman #Medusa #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "02_constantine_triunvirato_infierno",
        "queue_folder": "14_dia4_10h_constantine_triunvirato_infierno",
        "title": "John Constantine: ¡La Gran Estafa a los Reyes del Infierno! 🚬🔥",
        "character": "John Constantine",
        "folder": "constantine_triunvirato_infierno",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Desahuciado por los médicos y tosiendo sangre por un cáncer de pulmón terminal incurable, el detective de lo oculto John Constantine descubrió que solo le quedaban escasos días de vida antes de ser arrastrado al averno."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Consciente de que su alma era la más codiciada por las tinieblas, visitó en secreto a los tres gobernantes absolutos del inframundo: el Primer Caído, Azazel y Beelzebub, ofreciéndole su alma a cada uno por separado."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sin que ninguno supiera del otro, los tres reyes infernales firmaron el pacto prohibido, creyendo que por fin poseían el alma del mago más escurridizo de la Tierra, sellando sin saberlo su propia trampa legal."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al llegar la hora fatal, Constantine aceleró su muerte y los tres señores se manifestaron en su habitación. Al verse cara a cara, descubrieron la triple estafa que desataría una guerra civil cósmica por su alma."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Para evitar que el Infierno entero se autodestruyera, Lucifer no tuvo más opción que extirparle el cáncer milagrosamente y devolverle la vida. Constantine encendió un cigarro, burlándose en la cara de los señores del abismo."
            }
        ],
        "description": "John Constantine engañó a Lucifer, Azazel y Beelzebub vendiendo su alma tres veces para obligarlos a curarle el cáncer terminal. La mayor estafa al Infierno.",
        "hashtags": "#JohnConstantine #Hellblazer #DCComics #Vertigo #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "03_spiderman_vs_juggernaut",
        "queue_folder": "15_dia4_13h_spiderman_vs_juggernaut",
        "title": "Spider-Man vs Juggernaut: ¡La Trampa de Cemento Líquido! 🕷️🧱",
        "character": "Spider-Man",
        "folder": "spiderman_vs_juggernaut",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Un coloso imparable de fuerza ilimitada caminó en línea recta por las calles de Manhattan, demoliendo rascacielos, tanques policiales y edificios enteros sin que ninguna fuerza del planeta fuera capaz de frenar su avance."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Enviado por Black Tom Cassidy para capturar los poderes psíquicos de la clarividente Madame Web, Juggernaut atravesó los muros blindados de su apartamento ignorando con desprecio cada golpe de Spider-Man."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Desesperado por proteger a la anciana, Peter Parker desató todo su ingenio: le arrojó encima grúas de construcción enteras y lo electrocutó con cables de alto voltaje, pero el monstruo ni siquiera pestañeó."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al borde de la asfixia, Spider-Man saltó sobre la gigantesca espalda del titán y disparó telarañas directas a las ranuras de su casco blindado, cegándolo por completo para obligarlo a caminar hacia una zona de obras."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Juggernaut dio un paso en falso y cayó en un foso de cemento líquido de doce metros de profundidad que se solidificó al instante, sepultando a la bestia bajo toneladas de roca. ¿Fue esta la hazaña más épica de Spidey?"
            }
        ],
        "description": "¡Nada puede detener al Juggernaut! Excepto el ingenio de Spider-Man enterrándolo en doce metros de cemento líquido para salvar a Madame Web.",
        "hashtags": "#SpiderMan #Juggernaut #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "04_nova_annihilus_desgarro",
        "queue_folder": "16_dia4_17h_nova_annihilus_desgarro",
        "title": "Nova vs Annihilus: ¡El Despiadado Desgarro Cósmico! 🌌⚡",
        "character": "Nova",
        "folder": "nova_annihilus_desgarro",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Surgiendo desde las profundidades oscuras de la Zona Negativa, la Ola de Aniquilación arrasó galaxias completas, devorando civilizaciones y masacrando a billones de seres vivos sin que nada pudiera detenerla."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El despiadado señor insectoide Annihilus destruyó la capital dorada de Xandar y exterminó al legendario Cuerpo Nova, dejando al joven terrestre Richard Rider como el último guardián superviviente de la galaxia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cargando con la totalidad de la mente colectiva del Worldmind y toda la Nova Force cósmica fluyendo por sus venas, Richard Rider lideró el Frente Unido lanzándose en una misión suicida final."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En una colisión salvaje cuerpo a cuerpo en el vacío espacial, Nova clavó su puño directo por las fauces de Annihilus y tiró con toda su fuerza, arrancándole las entrañas de adentro hacia afuera en un acto sangriento definitivo."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Sosteniendo el cadáver despedazado del tirano cósmico y despojándolo de la Barra de Control, Nova salvó al universo entero demostrando hasta dónde llega la voluntad de un verdadero protector de las estrellas."
            }
        ],
        "description": "Richard Rider le arrancó las entrañas a Annihilus desde adentro para vengar al Cuerpo Nova y salvar al universo entero. El momento más salvaje de Annihilation.",
        "hashtags": "#Nova #Annihilus #Annihilation #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "05_red_goblin_osborn_carnage",
        "queue_folder": "17_dia4_20h_red_goblin_osborn_carnage",
        "title": "¡Nació el Duende Rojo! La Fusión de Norman Osborn y Carnage 🩸🎃",
        "character": "Norman Osborn",
        "folder": "red_goblin_osborn_carnage",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Desesperado tras perder los poderes del suero del Duende Verde y obsesionado con destruir a Peter Parker, Norman Osborn asaltó las instalaciones secretas para apoderarse del simbionte más sanguinario: Carnage."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al fusionar su mente psicópata con el simbionte alienígena, nació el Duende Rojo: un monstruo imparable con la astucia mortal de Osborn y la ferocidad sádica de Carnage, completamente inmune al fuego y al sonido."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Desatando el pánico absoluto en Manhattan, infectó a su propio nieto con microduendes simbióticos para obligarlo a matar y atacó a los seres queridos de Spider-Man en una noche de pesadilla sin escape."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Viendo a sus aliados caer, Spider-Man tomó una medida desesperada: se unió al simbionte Venom para igualar el poder de la bestia, provocando el orgullo de Osborn para forzarlo a luchar sin la criatura."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Tras un brutal combate final, el Duende Rojo fue despojado, pero el trauma neuronal destruyó la mente de Norman para siempre, dejándolo encerrado en Ravencroft creyendo que él es el verdadero Cletus Kasady."
            }
        ],
        "description": "La pesadilla carmesí: Norman Osborn fusionado con Carnage para crear al Duende Rojo, inmune al fuego y las ondas sonoras. El clímax de Dan Slott.",
        "hashtags": "#RedGoblin #Carnage #SpiderMan #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "06_flash_human_race",
        "queue_folder": "18_dia5_07h_flash_human_race",
        "title": "The Flash: ¡Más Rápido que la Teletransportación Instantánea! ⚡🌌",
        "character": "The Flash",
        "folder": "flash_human_race",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Unos colosales seres interdimensionales conocidos como los Apostadores Cósmicos llegaron a nuestro sector amenazando con desintegrar la Tierra si su campeón, The Flash, perdía una carrera a través del universo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El desafío era una trampa matemática mortal: el contrincante alienígena no corría, sino que poseía teletransportación instantánea, haciendo inútil cualquier velocidad física conocida en las leyes del espacio y tiempo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Wally West contactó a cada ser humano de la Tierra mediante Krakkl y les pidió que corrieran todos a la vez. Absorbiendo la energía cinética de seis mil millones de personas, Flash superó la velocidad trans-temporal."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Quebrando el tiempo de Planck, Flash cruzó la línea de meta en un tiempo negativo, llegando a su destino una fracción de segundo antes de que la teletransportación instantánea se materializara, salvando al planeta entero."
            }
        ],
        "description": "Wally West rompió la física: corrió más rápido que la teletransportación instantánea absorbiendo la energía cinética de toda la humanidad. The Human Race.",
        "hashtags": "#TheFlash #WallyWest #DCComics #SpeedForce #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "07_saint_walker_linterna_azul",
        "queue_folder": "19_dia5_10h_saint_walker_linterna_azul",
        "title": "Saint Walker: ¡La Esperanza que Salvó a Hal Jordan! 💙✨",
        "character": "Saint Walker",
        "folder": "saint_walker_linterna_azul",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Bajo el sol moribundo de su mundo natal Astonia, un pacífico habitante llamado Bro'Dee Walker perdió a toda su familia en un trágico cataclismo, pero se negó a rendirse ante la desesperación cósmica."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Guiado por una fe inquebrantable, escaló la montaña sagrada donde los Guardianes Ganthet y Sayd lo consagraron como el Primer Linterna Azul del cosmos, empuñando la luz pura de la Esperanza."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cuando Hal Jordan fue capturado en el planeta de fuego Ysmault y consumido por la sangre rabiosa de los Red Lanterns, Saint Walker descendió en medio del combate para realizar un milagro divino."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Colocando un anillo azul en la mano de Jordan y susurrando con amor ¡Todo estará bien!, la luz de la esperanza neutralizó el veneno de la ira, arrancando el anillo rojo sin detener su corazón."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Demostró ante el cosmos que la esperanza es el motor que enciende la voluntad, supercargando las baterías verdes al doscientos por ciento para salvar a los héroes de la oscuridad absoluta."
            }
        ],
        "description": "¡Todo estará bien! Bro'Dee Walker se convirtió en el primer Linterna Azul y salvó el corazón de Hal Jordan de la ira roja. La luz de la esperanza.",
        "hashtags": "#SaintWalker #GreenLantern #BlueLantern #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "08_shazam_billy_batson_relampago_dioses",
        "queue_folder": "20_dia5_13h_shazam_billy_batson_relampago_dioses",
        "title": "¡El Místico Origen de Shazam! El Relámpago de los Seis Dioses ⚡🏛️",
        "character": "Shazam",
        "folder": "shazam_billy_batson_relampago_dioses",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Vagando solo y abandonado por las frías calles de la ciudad, el pequeño huérfano Billy Batson sobrevivía en las estaciones del metro, manteniendo su bondad intacta pese a la crueldad del mundo moderno."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Una noche misteriosa, un tren subterráneo desprovisto de conductor abrió sus puertas mágicas y lo transportó a través de dimensiones ocultas hasta la milenaria y cavernosa Roca de la Eternidad."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Frente al trono de piedra de los siete pecados capitales, el anciano Mago Shazam examinó el corazón del niño y decidió heredarle el poder absoluto de Salomón, Hércules, Atlas, Zeus, Aquiles y Mercurio."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al pronunciar con valentía la palabra sagrada ¡SHAZAM!, un relámpago divino descendió de los cielos transformando al indefenso niño en el Campeón Supremo de la magia, protector eterno de la Tierra."
            }
        ],
        "description": "El origen místico del Campeón de la Magia: Billy Batson en la Roca de la Eternidad y el relámpago sagrado de los seis dioses inmortales. ¡SHAZAM!",
        "hashtags": "#Shazam #BillyBatson #DCComics #CaptainMarvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "09_zatanna_magia_inversa_conjuro_sombras",
        "queue_folder": "21_dia5_17h_zatanna_magia_inversa_conjuro_sombras",
        "title": "Zatanna: ¡El Secreto de la Magia Inversa que Dobla la Realidad! 🎩✨",
        "character": "Zatanna",
        "folder": "zatanna_magia_inversa_conjuro_sombras",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Heredera del legendario linaje de los Homo Magi y de su padre Giovanni Zatara, Zatanna creció deslumbrando a multitudes en los teatros de Gotham como la ilusionista más elegante y aclamada del mundo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero cuando entidades oscuras y demonios de pesadilla intentan romper la frontera dimensional para devorar a los inocentes, Zatanna abandona el truco teatral para desatar la verdadera magia primordial de la creación."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pronunciando cada conjuro en orden inverso, las palabras mágicas doblan las leyes de la física, congelando el tiempo, encadenando sombras infernales y transmutando la realidad misma con una sola orden hablada."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Ajustando su sombrero de copa y empuñando su varita de plata, Zatanna destierra a los monstruos al abismo con una sonrisa confiada, protegiendo el multiverso con el poder de su voz."
            }
        ],
        "description": "Zatanna y el misterio del lenguaje inverso: cuando hablar al revés dobla las leyes de la física y expulsa a los demonios del multiverso.",
        "hashtags": "#Zatanna #JusticeLeagueDark #DCComics #Magic #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "10_moon_knight_manicomio_khonshu_lemire",
        "queue_folder": "22_dia5_20h_moon_knight_manicomio_khonshu_lemire",
        "title": "Moon Knight: ¡El Manicomio de Khonshu y las Mentes de Marc Spector! 🌙🏥",
        "character": "Moon Knight",
        "folder": "moon_knight_manicomio_khonshu_lemire",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Marc Spector despertó atado con una camisa de fuerza en las celdas asépticas del hospital psiquiátrico New Bain, golpeado por enfermeros brutales y rodeado de pacientes que parecían antiguos aliados de guerra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "La directora del asilo, la doctora Emmet, intentó convencerlo con terapias de shock de que su vida como vigilante enmascarado y sus dioses egipcios eran solo delirios provocados por su grave trastorno de identidad disociativo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero al mirar fijamente a través de las ventanas bajo la luna llena, Marc descubrió la aterradora verdad: todo el hospital era una ilusión mágica y el personal médico eran sirvientes momificados de la deidad Ammit."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Desgarrando sus ataduras con furia mística y unificando sus mentes fracturadas, Marc abrazó el poder del Dios Khonshu para recuperar su armadura blanca y escapar del manicomio de dioses."
            }
        ],
        "description": "Marc Spector encerrado en un psiquiátrico donde los doctores son demonios egipcios de Ammit. La obra maestra psicológica de Moon Knight por Jeff Lemire.",
        "hashtags": "#MoonKnight #MarcSpector #Khonshu #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    }
]

def synthesize_voicebox_scene(text: str, out_wav: str, profile_id: str = PROFILE_ID) -> str:
    Path(out_wav).parent.mkdir(parents=True, exist_ok=True)
    payload = {'profile_id': profile_id, 'text': text}
    
    # Try up to 3 times to submit
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
        raise RuntimeError("No se pudo iniciar generación en Voicebox")

    # Poll status via SSE
    for _ in range(80):
        try:
            st_res = requests.get(f"{VOICEBOX_URL}/generate/{gen_id}/status", timeout=10)
            for line in st_res.text.splitlines():
                if line.startswith('data:'):
                    j = json.loads(line[5:].strip())
                    status = j.get('status')
                    if status == 'completed':
                        audio_res = requests.get(f"{VOICEBOX_URL}/audio/{gen_id}", timeout=25)
                        raw_tmp = out_wav + '.raw.wav'
                        with open(raw_tmp, 'wb') as f:
                            f.write(audio_res.content)
                        
                        # Resample to 48kHz and add 0.35s trailing pause for natural flow
                        subprocess.run([
                            'ffmpeg', '-y', '-i', raw_tmp,
                            '-af', 'aresample=48000,apad=pad_dur=0.35',
                            '-acodec', 'pcm_s16le', out_wav
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        
                        if Path(raw_tmp).exists():
                            Path(raw_tmp).unlink()
                        return out_wav
                    elif status == 'failed':
                        raise RuntimeError(f"Voicebox falló: {j.get('error')}")
        except Exception as e:
            if "Voicebox falló" in str(e):
                raise e
        time.sleep(1.0)
        
    raise TimeoutError(f"Voicebox excedió el tiempo límite para: {text[:40]}...")

def _motion_pattern(scene_number: int) -> int:
    motion_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    return motion_map.get(scene_number, (scene_number - 1) % 5)

def produce_and_schedule_single(proj: dict):
    proj_id = proj["id"]
    queue_name = proj["queue_folder"]
    title = proj["title"]
    folder_name = proj["folder"]
    scenes = proj["scenes"]
    
    target_queue_dir = SCHEDULED_QUEUE / queue_name
    final_queue_video = target_queue_dir / "video.mp4"
    final_queue_meta = target_queue_dir / "metadata.json"
    
    if final_queue_video.exists() and final_queue_meta.exists() and final_queue_video.stat().st_size > 5_000_000:
        dur = get_duration(str(final_queue_video))
        print(f"[SKIP] {queue_name} ya existe en scheduled_queue ({dur:.1f}s)")
        return str(final_queue_video)

    work_dir = OUTPUT_BASE / proj_id
    work_dir.mkdir(parents=True, exist_ok=True)
    curated_folder = CURATED_BASE / folder_name

    print(f"\n=======================================================")
    print(f"[PRODUCIENDO CON VOICEBOX]: {title}")
    print(f"Perfil: Narrador Referencia Cómic | Cola: {queue_name}")
    print(f"=======================================================")

    # 1. Generar audios con Voicebox
    print("1/5 Generando locución clonada con Voicebox (CUDA)...")
    vo_dir = work_dir / "voicebox_audio"
    vo_dir.mkdir(parents=True, exist_ok=True)
    
    voice_results = {}
    for sc in scenes:
        sn = sc["scene_number"]
        txt = sc["text"]
        out_wav = str(vo_dir / f"scene_{sn:02d}.wav")
        # Check if cached
        if not Path(out_wav).exists() or Path(out_wav).stat().st_size < 5000:
            print(f"   -> Sintetizando escena {sn}/{len(scenes)}...")
            synthesize_voicebox_scene(txt, out_wav)
            time.sleep(0.5)
        voice_results[sn] = {'audio': out_wav, 'text': txt}

    # Concatenar audios
    full_audio = str(vo_dir / "narration_full.wav")
    audio_inputs = []
    filter_inputs = []
    for idx, sn in enumerate(sorted(voice_results.keys())):
        audio_inputs.extend(['-i', voice_results[sn]['audio']])
        filter_inputs.append(f'[{idx}:a]')
    a_filter = f"{''.join(filter_inputs)}concat=n={len(filter_inputs)}:v=0:a=1[aout]"
    subprocess.run(['ffmpeg', '-y', *audio_inputs, '-filter_complex', a_filter, '-map', '[aout]', full_audio],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    total_audio_dur = get_duration(full_audio)
    print(f"   OK -> Audio completo Voicebox: {total_audio_dur:.2f} segundos")

    # 2. Componer escenas visuales con Ken Burns
    print("2/5 Componiendo escenas visuales con movimiento sincronizado...")
    composed_dir = work_dir / "composed_voicebox"
    composed_dir.mkdir(parents=True, exist_ok=True)
    composed_scenes = []

    for sc in scenes:
        sn = sc["scene_number"]
        src_img = str(curated_folder / sc["file"])
        audio_path = voice_results[sn]['audio']
        dur = get_duration(audio_path)
        out_clip = str(composed_dir / f"scene_{sn:02d}.mp4")
        motion = _motion_pattern(sn)
        
        compose_scene_from_image(src_img, audio_path, dur, out_clip, pattern_idx=motion, width=1080, height=1920)
        composed_scenes.append(out_clip)
    print(f"   OK -> {len(composed_scenes)} clips visuales compuestos")

    # 3. Transcribir timings exactos de palabras con Whisper
    print("3/5 Extrayendo timings palabra por palabra con Whisper...")
    word_json = str(work_dir / "word_timings_vb.json")
    words_data = extract_scene_word_timings(voice_results, word_json, language='es', model_name='base')
    words_timing = [{"word": w['text'], "start": w['start'], "end": w['end']} for w in words_data.get('words', [])]

    # Palabras clave para resaltado
    keywords = [proj["character"].upper()]
    for sc in scenes:
        for w in sc["text"].split():
            clean_w = ''.join(c for c in w if c.isalnum()).upper()
            if len(clean_w) > 4:
                keywords.append(clean_w)
    keywords = list(set(keywords))[:20]

    # 4. Ensamblar Reel con transiciones de papel rasgado y subtítulos Bangers
    print("4/5 Ensamblando Reel vertical maestro...")
    social_mov = get_or_create_vertical_cta_mov("motion")
    temp_master_mp4 = str(work_dir / "master_voicebox.mp4")
    
    assemble_reel(
        panel_clips=composed_scenes,
        words_timing=words_timing,
        narration_audio=full_audio,
        output_mp4=temp_master_mp4,
        work_dir=str(work_dir / "assemble_vb_work"),
        keywords=keywords,
        social_cta_mov=social_mov,
        cta_start_time=max(8.0, min(total_audio_dur - 7.0, total_audio_dur * 0.58)),
        alignment=5,
        margin_v=20,
        font_size=58,
        hook_title=title
    )
    
    final_dur = get_duration(temp_master_mp4)
    print(f"   OK -> Video maestro renderizado: {final_dur:.2f} segundos")

    # 5. Generar miniatura y stashing en scheduled_queue
    print("5/5 Registrando en scheduled_queue para publicación automática...")
    target_queue_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(temp_master_mp4, final_queue_video)
    
    thumb_path = str(target_queue_dir / "thumb.jpg")
    try:
        extract_thumbnail(temp_master_mp4, thumb_path, timestamp=2.5)
    except Exception as e:
        print(f"   Warning miniatura: {e}")

    meta_payload = {
        "id": proj_id,
        "title": title,
        "character": proj["character"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "video_file": "video.mp4",
        "duration_seconds": final_dur,
        "voice_profile": "Narrador Referencia Cómic (Voicebox)",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(final_queue_meta, "w", encoding="utf-8") as f:
        json.dump(meta_payload, f, indent=2, ensure_ascii=False)

    print(f"✅ ¡Video programado con éxito en: {target_queue_dir}!")
    return str(final_queue_video)

def main():
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    completed = []
    
    print(f"Iniciando Pipeline de Voz Clonada (Voicebox) y Programación de 10 Videos:")
    print(f"Destino de Cola: {SCHEDULED_QUEUE}")
    start_time = time.time()
    
    for idx, proj in enumerate(PROJECTS, 1):
        print(f"\n=======================================================")
        print(f">>> PROCESANDO VIDEO {idx}/10: {proj['id']} <<<")
        print(f"=======================================================")
        try:
            v_path = produce_and_schedule_single(proj)
            dur = get_duration(v_path)
            completed.append((proj, v_path, dur))
        except Exception as e:
            print(f"[ERROR CRÍTICO] en {proj['id']}: {e}")
            import traceback
            traceback.print_exc()

    total_time = time.time() - start_time
    print(f"\n=======================================================")
    print(f"RESUMEN FINAL: {len(completed)}/10 Videos Listos y Programados")
    print(f"Tiempo Total: {total_time/60:.2f} minutos")
    print(f"=======================================================")
    for proj, v_path, dur in completed:
        print(f" - [{dur:.1f}s] {proj['queue_folder']}: {proj['title']}")

if __name__ == "__main__":
    main()
