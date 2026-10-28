"""
Voicebox Production & Scheduling Engine: Lote 2 de Videos Virales (9 Videos de 60s)
===================================================================================
Voz: 'Narrador Referencia Cómic' (Voicebox CUDA Local, Profile ID: 28078056-1a1d-43d4-9d57-d616275f13c2)
Formato: 1080x1920 (Vertical 9:16 para Shorts, Reels y TikTok)
Duración: 58 a 62 segundos por video
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

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
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
OUTPUT_BASE = PROJECT_ROOT / "output" / "batch_2_voicebox_60s"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2"  # Narrador Referencia Cómic

PROJECTS = [
    {
        "id": "23_ash_williams_marvel_zombies",
        "queue_folder": "23_dia6_07h_ash_williams_marvel_zombies",
        "title": "¡Ash Williams vs Marvel Zombies! La Motosierra en el Fin del Mundo 🪚💀",
        "character": "Ash Williams",
        "folder": "ash_williams_ejercito_tinieblas_invasion_muertos",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "El cielo de Manhattan se desgarró sobre los rascacielos abriendo una brecha dimensional. Ash Williams cayó gritando al vacío con su escopeta recortada en mano, estrellándose en un contenedor de basura mientras la silueta de un infectado susurraba con hambre."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aturdido entre los desperdicios y con una cáscara de plátano en la cabeza, Ashley J. Williams intentó incorporarse confundido, cuando una mano humana mutilada y ensangrentada trepó por el borde del contenedor gimiendo desesperadamente por carne viva."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al levantarse, una anciana zombi con ojos lechosos y piel podrida se lanzó sobre él intentando morderlo; Ash la empujó con absoluto desprecio creyendo que era una simple mendiga o un demonio solitario, ignorando el apocalipsis caníbal del planeta."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Encendiendo su fiel motosierra con un rugido ensordecedor y amartillando su escopeta, Ash se dispuso a despedazar a la muerta viviente, justo cuando Daredevil y Luke Cage emergieron atónitos creyendo que atacaba a una pobre anciana indefensa."
            }
        ],
        "description": "El mítico guerrero Ash Williams aterriza en la dimensión de Marvel Zombies y enciende su motosierra para enfrentar la plaga de carne viva.",
        "hashtags": "#AshWilliams #ArmyOfDarkness #MarvelZombies #EvilDead #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "24_moira_mactaggert_house_of_x",
        "queue_folder": "24_dia6_10h_moira_mactaggert_house_of_x",
        "title": "¡El Gran Secreto de Moira MacTaggert! Las 10 Vidas de House of X 🧬⏳",
        "character": "Moira MacTaggert",
        "folder": "moira_mactaggert_diez_vidas_house_of_x",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Durante décadas, el mundo entero creyó que Moira MacTaggert era únicamente una científica humana y aliada leal de los Hombres X, pero tras esa mirada serena se ocultaba el poder mutante más trascendental y revolucionario de la historia cósmica."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su habilidad oculta consistía en la reencarnación temporal: cada vez que fallecía, su conciencia regresaba al vientre materno con todos sus recuerdos intactos, habiendo vivido vidas completas como maestra, madre de familia y líder rebelde de la resistencia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "A lo largo de nueve existencias consecutivas, Moira luchó al lado de cada generación mutante, desde los cinco héroes originales hasta los jinetes apocalípticos, presenciando una y otra vez cómo los Centinelas mecánicos exterminaban a su especie sin piedad alguna."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En su décima y definitiva vida, con la mirada endurecida por mil años de derrotas inevitables, Moira reunió en secreto a Charles Xavier y Magneto para romper el fatídico ciclo y levantar Krakoa, la primera nación inmortal de mutantes."
            }
        ],
        "description": "La gran revelación de House of X: Moira MacTaggert es una mutante inmortal que reencarnó 10 veces para romper la extinción mutante y fundar Krakoa.",
        "hashtags": "#MoiraMacTaggert #HouseOfX #PowersOfX #XMen #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "25_doctor_strange_empirikul",
        "queue_folder": "25_dia6_13h_doctor_strange_empirikul",
        "title": "¡Los Últimos Días de la Magia! Doctor Strange vs La Inquisición Empirikul 🔮⚔️",
        "character": "Doctor Strange",
        "folder": "doctor_strange_ultimos_dias_magia_empirikul",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "A través de las infinitas dimensiones del multiverso, un implacable ejército cibernético conocido como el Empirikul inició una purga sistemática, cazando y ejecutando a los hechiceros arcanos con lanzas tecno-orgánicas y bestias rastreadoras de energía mística ancestral."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Liderados por el fanático Imperator, estas máquinas de ciencia dogmática invadieron la Tierra y desataron toxinas microscópicas que devoraron la energía mágica del planeta, neutralizando al instante todos los conjuros, sellos y encantamientos del Doctor Strange."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al ver su Santuario profanado y los reinos mágicos desmoronándose en cenizas, del sufrimiento acumulado de la hechicería surgió la criatura del sótano, una abominación esquelética y oscura alimentada por los sacrificios arcanos secretos del Hechicero Supremo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Despojado de su Capa de Levitación y sin una sola gota de magia en sus venas, Stephen Strange se negó a doblar la rodilla: empuñó el hacha de guerra de Angarruumus para enfrentar a la inquisición a golpe de puro acero y sangre."
            }
        ],
        "description": "Cuando el Empirikul extinguió toda la magia del multiverso, Doctor Strange tomó un hacha de batalla ancestral para defender la Tierra con sus propias manos.",
        "hashtags": "#DoctorStrange #Empirikul #MarvelComics #SorcererSupreme #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "26_green_arrow_longbow_hunters",
        "queue_folder": "26_dia6_17h_green_arrow_longbow_hunters",
        "title": "¡Flecha Verde: The Longbow Hunters! El Cazador Implacable de Seattle 🏹🌧️",
        "character": "Green Arrow",
        "folder": "green_arrow_longbow_hunters_seattle",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Cansado de las batallas cósmicas y los villanos teatrales, Oliver Queen empacó sus pertenencias y viajó al noroeste del Pacífico, internándose en los bosques densos y lluviosos de Seattle con su arco de madera tradicional para redescubrir su verdadera esencia."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Reflexionando sobre su juventud arrogante como millonario caprichoso que jugaba a ser Robin Hood, el arquero esmeralda tomó una decisión radical: desechó sus flechas trucadas de red y guante de boxeo para cargar exclusivamente puntas de caza de acero afilado."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Junto a su gran amor Dinah Lance, Canario Negro, abrió una florería en la ciudad buscando una vida apacible, pero las calles de Seattle pronto se infectaron de narcotráfico, secuestros brutales y crímenes despiadados que amenazaron con arrebatarle lo más preciado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Lanzándose desde una camioneta en marcha y encapuchado bajo el frío implacable, Flecha Verde se transformó en un cazador urbano silencioso y letal, cruzando por primera vez la línea moral de matar para salvar a Dinah de sus torturadores."
            }
        ],
        "description": "La obra maestra de Mike Grell: Oliver Queen abandona las flechas trucadas en Seattle y se convierte en un cazador urbano letal para salvar a Canario Negro.",
        "hashtags": "#GreenArrow #LongbowHunters #BlackCanary #DCComics #OliverQueen #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "27_nightcrawler_espadachin_fe",
        "queue_folder": "27_dia6_20h_nightcrawler_espadachin_fe",
        "title": "Nightcrawler: ¡El Espadachín Celestial y el Alma Más Noble de X-Men! ⚔️💙",
        "character": "Nightcrawler",
        "folder": "nightcrawler_kurt_wagner_fe_espadachin",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Pese a su apariencia demoníaca de piel azul y cola prensil, Kurt Wagner siempre conservó el espíritu más cálido y bondadoso entre los mutantes, disfrutando de los placeres sencillos como un baño caliente y el humor caballeresco junto a sus camaradas de Excalibur."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aceptando con madurez espiritual el peso de su condición física mientras inspecciona los motores del avión Blackbird, Nightcrawler aprendió que la fe cristiana y la nobleza no se miden por la silueta exterior, sino por la pureza inquebrantable de los actos cotidianos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero cuando el peligro acecha a los inocentes, el elfo azul salta al combate materializándose entre nubes de humo sulfuroso y olor a azufre, coordinando tácticas de teletransportación junto a genios tecnológicos como Forge para proteger la vida de sus hermanos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Blandiendo floretes con la destreza incomparable de un mosquetero clásico, Kurt danza ágilmente entre autómatas mecánicos en la sala de entrenamiento, esquivando cada estocada con una sonrisa pícara y el corazón noble de un auténtico héroe de leyenda."
            }
        ],
        "description": "Kurt Wagner, el héroe incomprendido: un mutante con cuerpo de demonio y alma de mosquetero que defiende a la humanidad con espadas y fe absoluta.",
        "hashtags": "#Nightcrawler #KurtWagner #XMen #MarvelComics #Marvel #Excalibur #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "28_jessica_jones_purple_man",
        "queue_folder": "28_dia7_07h_jessica_jones_purple_man",
        "title": "Jessica Jones: ¡La Pesadilla de Killgrave y el Resurgir de Alias! 🥃🕵️",
        "character": "Jessica Jones",
        "folder": "jessica_jones_alias_investigacion_killgrave",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Oculta tras las persianas metálicas de su modesta oficina en Hell's Kitchen, Jessica Jones fuma en silencio y anota pistas en su libreta, intentando ganarse la vida como detective privada tras abandonar definitivamente el mundo de los superhéroes."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "En su mente aún resuenan los ecos traumáticos de Zebediah Killgrave, el Hombre Púrpura, cuyas feromonas psíquicas de sumisión absoluta anularon su voluntad durante meses de cautiverio psicológico, obligándola a obedecer sus órdenes más retorcidas y crueles."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Años atrás, soñaba con la gloria usando el traje blanco de Jewel y volando libre sobre los rascacielos de Manhattan, pero la pesadilla vivida bajo el control mental de Killgrave destrozó para siempre su inocencia y su fe en el heroísmo tradicional."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Ahora, caminando en vaqueros y zapatillas por los tejados y callejones oscuros de Nueva York, Jessica Jones utiliza su superfuerza y su dura determinación para defender a los indefensos, jurando que jamás volverá a ser víctima de ningún titán mental."
            }
        ],
        "description": "De la pesadilla de sumisión psíquica con Killgrave a detective privada en Hell's Kitchen. La historia de resistencia inquebrantable de Jessica Jones.",
        "hashtags": "#JessicaJones #Killgrave #Alias #MarvelComics #Marvel #HellsKitchen #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "29_ms_marvel_niebla_terrigena",
        "queue_folder": "29_dia7_10h_ms_marvel_niebla_terrigena",
        "title": "¡El Despertar de Kamala Khan! La Niebla Terrígena y Ms. Marvel ⚡🧣",
        "character": "Ms. Marvel",
        "folder": "ms_marvel_kamala_khan_niebla_terrigena",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Sintiéndose excluida y pequeña entre los adolescentes populares de Jersey City, la joven Kamala Khan se refugió sola en las escaleras de la costa, soñando con ser tan fuerte, audaz y admirada como su gran heroína de los Vengadores, Capitana Marvel."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Cabizbaja y en silencio sobre los escalones, la soñadora paquistaní meditaba sobre su identidad y su lugar en el mundo, sin sospechar que una espesa y luminosa nube química se aproximaba flotando sobre las aguas oscuras de la bahía urbana."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "De repente, la sagrada Niebla Terrígena de los Inhumanos envolvió su cuerpo despertando sus genes alienígenas latentes, otorgándole una impactante visión cósmica que transmutó su apariencia física en la mismísima Ms. Marvel de traje negro y relámpago dorado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al escuchar los gritos de auxilio de su compañera Zoe Zimmer ahogándose en las profundidades del mar, Kamala estiró su brazo elástico decenas de metros bajo el agua, rescatándola y comprendiendo que el verdadero heroísmo es proteger a los demás."
            }
        ],
        "description": "El origen de Kamala Khan: cuando la Niebla Terrígena de los Inhumanos descendió sobre Jersey City despertando los poderes de la nueva Ms. Marvel.",
        "hashtags": "#MsMarvel #KamalaKhan #Inhumans #MarvelComics #Marvel #CaptainMarvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "30_thor_indigno_susurro_luna",
        "queue_folder": "30_dia7_13h_thor_indigno_susurro_luna",
        "title": "¡Thor Indigno! El Devastador Susurro en la Luna que Destruyó al Dios ⚡🌑",
        "character": "Thor",
        "folder": "thor_unworthy_susurro",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Sobre la superficie yerma y agrietada del Área Azul de la Luna, el martillo milenario Mjolnir yace completamente inmóvil, convertido en un bloque de metal inerte que rechaza con frialdad al Príncipe Heredero de Asgard."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Encadenado a las rocas lunares y despojado de sus ojos mortales, Nick Fury deambula en silencio como El Que No Es Visto, condenado eternamente a vigilar la Tierra tras haber alterado para siempre el destino de los dioses nórdicos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Durante la cruenta batalla de Original Sin, Fury se aproximó al oído de Thor y pronunció apenas tres palabras demoledoras: Gorr tenía razón; un susurro mortal que quebró la fe divina del Dios del Trueno en el valor de los inmortales."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Condenado a vagar en las sombras del espacio entre cadenas místicas, el viejo soldado vigila cómo el peso de esa verdad irrevocable arrastra al guerrero asgardiano hacia un abismo de vergüenza y redención solitaria."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "De rodillas en el polvo lunar y tirando con desesperación ciega del mango del martillo, Thor es incapaz de moverlo un solo milímetro ante la mirada atónita de Iron Man, iniciando su doloroso y trágico camino como el Dios Indigno."
            }
        ],
        "description": "'Gorr tenía razón': las tres palabras que Nick Fury susurró en la Luna para hacer a Thor indigno de levantar el Mjolnir. El clímax de Original Sin.",
        "hashtags": "#Thor #UnworthyThor #Mjolnir #NickFury #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "31_miles_morales_legado_aracnido",
        "queue_folder": "31_dia7_17h_miles_morales_legado_aracnido",
        "title": "¡Miles Morales: El Salto de Fe! El Heredero del Manto Arácnido 🕷️⚡",
        "character": "Miles Morales",
        "folder": "miles_morales_legado_prodigio",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Abrumado por el pánico y el sudor tras ser picado por una araña genéticamente alterada de Oscorp, el joven estudiante Miles Morales se levantó la máscara en un callejón oscuro, temiendo que ponerse el manto arácnido fuera una falta de respeto a Peter Parker."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero aceptando la pesada carga de la responsabilidad y confeccionando su propio traje en elegante negro y carmesí, Miles saltó con acrobacias espectaculares sobre los tejados de Brooklyn, desatando su habilidad de invisibilidad y su letal Picadura Venenosa."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su mayor prueba de madurez llegó al enfrentarse en combate aéreo contra el peligroso ladrón de alta tecnología The Prowler, descubriendo con el corazón destrozado que el villano era en realidad su propio y querido tío, Aaron Davis."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con la máscara rasgada por la violencia del enfrentamiento y el rostro ensangrentado en medio de las sirenas policiales, Miles contempló la tragedia familiar de su destino, asumiendo con valentía que el verdadero Spider-Man jamás retrocede ante el dolor."
            }
        ],
        "description": "El salto de fe de Miles Morales: superando el miedo a reemplazar a Peter Parker y enfrentando a su propio tío The Prowler en las calles de Brooklyn.",
        "hashtags": "#MilesMorales #SpiderMan #SpiderVerse #MarvelComics #Marvel #Brooklyn #Comics #Shorts #Reels #TikTok"
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
    
    print(f"Iniciando Pipeline de Voz Clonada (Voicebox) y Programación de 9 Videos:")
    print(f"Destino de Cola: {SCHEDULED_QUEUE}")
    start_time = time.time()
    
    for idx, proj in enumerate(PROJECTS, 1):
        print(f"\n=======================================================")
        print(f">>> PROCESANDO VIDEO {idx}/9: {proj['id']} <<<")
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
    print(f"RESUMEN FINAL: {len(completed)}/9 Videos Listos y Programados")
    print(f"Tiempo Total: {total_time/60:.2f} minutos")
    print(f"=======================================================")
    for proj, v_path, dur in completed:
        print(f" - [{dur:.1f}s] {proj['queue_folder']}: {proj['title']}")

if __name__ == "__main__":
    main()
