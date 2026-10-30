"""
Voicebox Production & Scheduling Engine: Lote 2 de Videos Virales (9 Videos de 60s)
===================================================================================
Voz: 'Narrador Referencia Cómic' (Voicebox CUDA Local, Profile ID: 28078056-1a1d-43d4-9d57-d616275f13c2)
Formato: 1080x1920 (Vertical 9:16 para Shorts, Reels y TikTok)
Optimización Viral: Ganchos de curiosidad "¿Sabías que...?" en los primeros 3 segundos + tempo acelerado a 1.08 + volumen boosting.
Destino: Staging completo en 'scheduled_queue/' para publicación automática vía GitHub Actions Cronjobs.
"""

import os
import sys
import json
import time
import shutil
import hashlib
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
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
OUTPUT_BASE = PROJECT_ROOT / "output" / "batch_2_voicebox_60s"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2"  # Narrador Referencia Cómic

PROJECTS = [
    {
        "id": "24_moira_mactaggert_house_of_x",
        "queue_folder": "24_dia6_10h_moira_mactaggert_house_of_x",
        "title": "¡Los X-Men Murieron 9 Veces! El Secreto de Moira MacTaggert 🧬⏳",
        "character": "Moira MacTaggert",
        "folder": "moira_mactaggert_diez_vidas_house_of_x",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías que los X-Men murieron 9 veces y una simple científica humana vivió mil años para salvarlos del exterminio total? Durante décadas, el mundo creyó que Moira MacTaggert era una simple aliada, pero ocultaba el poder mutante más asombroso del multiverso."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su habilidad secreta era la reencarnación temporal: cada vez que moría, su mente regresaba intacta al vientre materno, habiendo vivido vidas completas como maestra, madre y líder rebelde de la resistencia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "A lo largo de nueve existencias consecutivas, Moira luchó al lado de cada generación mutante, presenciando una y otra vez cómo los Centinelas exterminaban a toda su especie sin piedad alguna."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En su décima y definitiva vida, con la mirada endurecida por mil años de derrotas inevitables, Moira reunió en secreto a Charles Xavier y Magneto para romper el ciclo y levantar Krakoa, la nación inmortal de los mutantes."
            }
        ],
        "description": "¿Sabías que los X-Men fueron exterminados 9 veces? La revelación de Moira MacTaggert en House of X y la fundación de Krakoa.",
        "hashtags": "#MoiraMacTaggert #HouseOfX #PowersOfX #XMen #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "25_doctor_strange_empirikul",
        "queue_folder": "25_dia6_13h_doctor_strange_empirikul",
        "title": "¿Qué Hace Doctor Strange Sin Magia? ¡El Hacha Ancestral de Sangre! 🔮⚔️",
        "character": "Doctor Strange",
        "folder": "doctor_strange_ultimos_dias_magia_empirikul",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Qué hace el Doctor Strange cuando unos robots aniquilan toda la magia del multiverso? ¡Tomar un hacha de batalla ancestral y destrozarlos a sangre fría! Una inquisición científica implacable purgó cada dimensión arcana exterminando hechiceros con armas tecno-orgánicas."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Lideradas por el fanático Imperator, estas máquinas invadieron la Tierra y desataron toxinas que devoraron la energía mágica del planeta, neutralizando al instante todos los conjuros y encantamientos del Hechicero Supremo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al ver su Santuario en cenizas y los reinos mágicos desmoronándose, del sufrimiento acumulado de la hechicería surgió la criatura del sótano, una abominación esquelética alimentada por los sacrificios arcanos del propio Strange."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Despojado de su Capa de Levitación y sin una sola gota de magia en sus venas, Stephen Strange se negó a rendirse: empuñó el hacha de guerra de Angarruumus para enfrentar a la inquisición a golpe de puro acero."
            }
        ],
        "description": "¿Qué hace Doctor Strange cuando la magia deja de existir? Empuñar un hacha de batalla ancestral para defender la Tierra a sangre y fuego.",
        "hashtags": "#DoctorStrange #Empirikul #MarvelComics #SorcererSupreme #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "26_green_arrow_longbow_hunters",
        "queue_folder": "26_dia6_17h_green_arrow_longbow_hunters",
        "title": "¡Por Qué Flecha Verde Empezó a Matar! The Longbow Hunters 🏹🌧️",
        "character": "Green Arrow",
        "folder": "green_arrow_longbow_hunters_seattle",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías por qué Flecha Verde tiró sus flechas con guante de boxeo a la basura y empezó a atravesar corazones con flechas de caza reales? Cansado de batallas cómicas, Oliver Queen se internó en los bosques fríos de Seattle con su arco tradicional para redescubrir su verdadera esencia."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Reflexionando sobre su pasado como millonario caprichoso que jugaba a ser Robin Hood, el arquero esmeralda tomó una decisión radical: desechó sus trucos infantiles para cargar exclusivamente puntas de caza de acero afilado."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Junto a su gran amor Dinah Lance, Canario Negro, abrió una florería buscando paz, pero las calles de Seattle pronto se infectaron de narcotráfico, secuestros y crímenes despiadados que amenazaron con arrebatarle lo más preciado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Lanzándose desde una camioneta en marcha y encapuchado bajo la lluvia, Flecha Verde se convirtió en un cazador urbano letal, cruzando por primera vez la línea moral de matar para salvar a Dinah de sus torturadores."
            }
        ],
        "description": "El día que Green Arrow cruzó la línea: Oliver Queen abandona los trucos en Seattle y mata para salvar a Canario Negro. The Longbow Hunters.",
        "hashtags": "#GreenArrow #LongbowHunters #BlackCanary #DCComics #OliverQueen #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "27_nightcrawler_espadachin_fe",
        "queue_folder": "27_dia6_20h_nightcrawler_espadachin_fe",
        "title": "Nightcrawler: ¡El Espadachín que los Demonios Temen en X-Men! ⚔️💙",
        "character": "Nightcrawler",
        "folder": "nightcrawler_kurt_wagner_fe_espadachin",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías por qué Nightcrawler es el único héroe al que los demonios le temen a pesar de tener cuerpo de bestia infernal? Pese a su apariencia de piel azul y cola prensil, Kurt Wagner siempre conservó el espíritu más bondadoso de los X-Men, gozando de la amistad y el humor caballeresco."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aceptando con madurez espiritual el peso de su condición física mientras inspecciona los motores del Blackbird, Nightcrawler aprendió que la fe y la nobleza no se miden por la silueta exterior, sino por la pureza de los actos cotidianos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero cuando el peligro acecha a los inocentes, el elfo azul salta al combate materializándose entre nubes de humo sulfuroso, coordinando tácticas de teletransportación junto a genios como Forge para proteger a sus hermanos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Blandiendo floretes con la destreza incomparable de un mosquetero clásico, Kurt danza entre autómatas en la sala de peligro, esquivando cada estocada con una sonrisa pícara y el corazón noble de un auténtico héroe de leyenda."
            }
        ],
        "description": "Cuerpo de demonio, alma de mosquetero: Kurt Wagner es el mutante más noble de los X-Men y el espadachín más ágil del multiverso.",
        "hashtags": "#Nightcrawler #KurtWagner #XMen #MarvelComics #Marvel #Excalibur #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "28_jessica_jones_purple_man",
        "queue_folder": "28_dia7_07h_jessica_jones_purple_man",
        "title": "¡La Orden Más Perturbadora de Killgrave a Jessica Jones! 🥃🕵️",
        "character": "Jessica Jones",
        "folder": "jessica_jones_alias_investigacion_killgrave",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías cuál fue la orden más perturbadora y sádica que el Hombre Púrpura le obligó a cumplir a Jessica Jones antes de que rompiera su control mental? Oculta tras las persianas de su oficina en Hell's Kitchen, Jessica fuma en silencio intentando olvidar su pasado como superheroína."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "En su mente aún resuenan los ecos traumáticos de Zebediah Killgrave, cuyas feromonas psíquicas anularon su voluntad durante meses de cautiverio, obligándola a obedecer sus órdenes más retorcidas y crueles sin poder resistirse."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Años atrás, soñaba con la gloria usando el traje de Jewel y volando libre sobre Manhattan, pero la pesadilla vivida bajo el control mental de Killgrave destrozó para siempre su inocencia y su fe en el heroísmo tradicional."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Ahora, caminando en vaqueros y zapatillas por los tejados de Nueva York, Jessica Jones utiliza su superfuerza para defender a los indefensos, jurando que jamás volverá a ser víctima de ningún titán mental."
            }
        ],
        "description": "¿Cuál fue el mayor trauma de Jessica Jones? El aterrador control mental de Zebediah Killgrave y su renacimiento como detective privada.",
        "hashtags": "#JessicaJones #Killgrave #Alias #MarvelComics #Marvel #HellsKitchen #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "29_ms_marvel_niebla_terrigena",
        "queue_folder": "29_dia7_10h_ms_marvel_niebla_terrigena",
        "title": "¡El Impactante Origen Inhumano de Ms. Marvel! Kamala Khan ⚡🧣",
        "character": "Ms. Marvel",
        "folder": "ms_marvel_kamala_khan_niebla_terrigena",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Qué harías si una extraña niebla alienígena te envolviera de noche y despertara de golpe el poder genético más elástico del planeta? Sintiéndose excluida entre los jóvenes de Jersey City, la soñadora Kamala Khan se refugió sola en la costa, deseando ser tan audaz como Capitana Marvel."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Cabizbaja y en silencio sobre los escalones, la joven paquistaní meditaba sobre su identidad y su lugar en el mundo, sin sospechar que una densa y luminosa nube química se aproximaba flotando sobre las aguas oscuras de la bahía."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "De repente, la sagrada Niebla Terrígena de los Inhumanos envolvió su cuerpo despertando sus genes alienígenas, otorgándole una visión cósmica que transmutó su apariencia física en la mismísima Ms. Marvel de traje negro y relámpago dorado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al escuchar los gritos de auxilio de su compañera Zoe Zimmer ahogándose en las profundidades del mar, Kamala estiró su brazo elástico decenas de metros bajo el agua, rescatándola y comprendiendo que su deber es salvar vidas."
            }
        ],
        "description": "¿Cómo despertaron los poderes de Kamala Khan? La Niebla Terrígena y el nacimiento de la nueva Ms. Marvel en Jersey City.",
        "hashtags": "#MsMarvel #KamalaKhan #Inhumans #MarvelComics #Marvel #CaptainMarvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "30_thor_indigno_susurro_luna",
        "queue_folder": "30_dia7_13h_thor_indigno_susurro_luna",
        "title": "¡Las 3 Palabras que Destruyeron a Thor! El Susurro en la Luna ⚡🌑",
        "character": "Thor",
        "folder": "thor_unworthy_susurro",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías cuáles fueron las 3 palabras exactas que Nick Fury le susurró a Thor en la Luna para hacer que jamás pudiera volver a levantar el Mjolnir? Sobre la superficie agrietada del Área Azul, el martillo milenario yace inmóvil, convertido en metal inerte que rechaza con frialdad al Dios del Trueno."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Encadenado a las rocas lunares y despojado de sus ojos mortales, Nick Fury deambula como El Que No Es Visto, condenado a vigilar la Tierra tras haber alterado para siempre el destino de los dioses nórdicos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Durante la batalla de Original Sin, Fury se aproximó al oído de Thor y pronunció apenas tres palabras demoledoras: Gorr tenía razón; un susurro mortal que quebró la fe divina del Dios del Trueno en el valor de los inmortales."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Condenado a vagar en las sombras del espacio entre cadenas místicas, el viejo soldado vigila cómo el peso de esa verdad irrevocable arrastra al guerrero asgardiano hacia un abismo de vergüenza y redención solitaria."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "De rodillas en el polvo lunar y tirando con desesperación ciega del martillo, Thor es incapaz de moverlo un solo milímetro ante la mirada atónita de Iron Man, iniciando su trágico camino como el Dios Indigno."
            }
        ],
        "description": "'Gorr tenía razón': Las 3 demoledoras palabras que Nick Fury susurró en la Luna para arrebatarle el Mjolnir a Thor. Original Sin.",
        "hashtags": "#Thor #UnworthyThor #Mjolnir #NickFury #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "31_miles_morales_legado_aracnido",
        "queue_folder": "31_dia7_17h_miles_morales_legado_aracnido",
        "title": "¡El Desgarrador Secreto de Miles Morales! The Prowler Desenmascarado 🕷️⚡",
        "character": "Miles Morales",
        "folder": "miles_morales_legado_prodigio",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías qué descubrió Miles Morales al romperle la máscara a su peor enemigo? ¡Que el villano al que estaba cazando era su propio y querido tío! Abrumado por el pánico tras ser picado por una araña genéticamente alterada, el joven Miles temía que ponerse el manto fuera una falta de respeto a Peter Parker."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero aceptando la pesada carga de la responsabilidad y confeccionando su traje en negro y carmesí, Miles saltó sobre los tejados de Brooklyn, desatando su habilidad de invisibilidad y su letal Picadura Venenosa."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su mayor prueba de fuego llegó al enfrentarse en combate aéreo contra el peligroso ladrón de alta tecnología The Prowler, descubriendo con el corazón destrozado que el villano era en realidad su tío, Aaron Davis."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con la máscara rasgada por la violencia del enfrentamiento y el rostro ensangrentado ante las sirenas policiales, Miles contempló la tragedia familiar de su destino, asumiendo con valentía que el verdadero Spider-Man jamás retrocede."
            }
        ],
        "description": "La mayor tragedia de Miles Morales: descubrir que el despiadado villano The Prowler es su propio tío Aaron Davis en las calles de Brooklyn.",
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
                        
                        # Resample to 48kHz, speed up by 8% (atempo=1.08) for viral urgency, boost volume and tight 0.20s pause
                        subprocess.run([
                            'ffmpeg', '-y', '-i', raw_tmp,
                            '-af', 'atempo=1.08,aresample=48000,volume=1.8dB,apad=pad_dur=0.20',
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

    work_dir = OUTPUT_BASE / proj_id
    work_dir.mkdir(parents=True, exist_ok=True)
    curated_folder = CURATED_BASE / folder_name

    print(f"\n=======================================================")
    print(f"[RE-INGENIERÍA VIRAL VOICEBOX]: {title}")
    print(f"Gancho: {scenes[0]['text'][:70]}...")
    print(f"Destino: {queue_name}")
    print(f"=======================================================")

    # 1. Generar audios con Voicebox (sintetizar o usar cache si el texto coincide)
    print("1/5 Sintetizando locución de alta retención...")
    vo_dir = work_dir / "voicebox_audio"
    vo_dir.mkdir(parents=True, exist_ok=True)
    
    voice_results = {}
    for sc in scenes:
        sn = sc["scene_number"]
        txt = sc["text"]
        out_wav = str(vo_dir / f"scene_{sn:02d}.wav")
        txt_hash_file = str(vo_dir / f"scene_{sn:02d}.hash")
        cur_hash = hashlib.md5(txt.encode('utf-8')).hexdigest()
        
        need_synth = True
        if Path(out_wav).exists() and Path(txt_hash_file).exists():
            with open(txt_hash_file, "r") as hf:
                if hf.read().strip() == cur_hash:
                    need_synth = False
                    
        if need_synth:
            print(f"   -> Sintetizando escena {sn}/{len(scenes)} (texto nuevo)...")
            synthesize_voicebox_scene(txt, out_wav)
            with open(txt_hash_file, "w") as hf:
                hf.write(cur_hash)
            time.sleep(0.5)
        else:
            print(f"   -> Escena {sn} en caché válido.")
            
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
    print(f"   OK -> Audio completo optimizado: {total_audio_dur:.2f} segundos")

    # 2.0 ESCUDO DE CALIDAD VISUAL: Validar con IA que el 100% de las imágenes sean viñetas reales de cómic
    print("2/5 Validando autenticidad visual de paneles con IA...")
    for sc in scenes:
        sn = sc["scene_number"]
        src_img = str(curated_folder / sc["file"])
        val = verify_visual_alignment_with_gemini(src_img, f"{proj['character']} comic book narrative art panel")
        if not val.get("is_comic_panel", False) or val.get("score", 0) <= 2:
            raise RuntimeError(
                f"BLOQUEO DE SEGURIDAD CRÍTICO: La imagen '{sc['file']}' en '{folder_name}' NO es una viñeta de cómic válida. "
                f"Motivo detectado: {val.get('reason')}. ¡Render abortado inmediatamente para evitar publicar imágenes ajenas al cómic!"
            )
        print(f"   OK -> Viñeta {sn} verificada auténtica por IA (Score: {val.get('score')}/10).")

    # 2. Componer escenas visuales con Ken Burns
    print("2/5 Componiendo escenas visuales...")
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
    print("3/5 Extrayendo timings de palabras con Whisper...")
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
    print("4/5 Ensamblando Reel vertical maestro con Hook Banner...")
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

    # 5. Generar miniatura y actualizar scheduled_queue
    print("5/5 Actualizando scheduled_queue...")
    target_queue_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(temp_master_mp4, final_queue_video)
    
    thumb_path = str(target_queue_dir / "thumb.jpg")
    try:
        extract_thumbnail(temp_master_mp4, thumb_path, timestamp=1.5)
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
        "voice_profile": "Narrador Referencia Cómic (Voicebox Optimizado 1.08x)",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(final_queue_meta, "w", encoding="utf-8") as f:
        json.dump(meta_payload, f, indent=2, ensure_ascii=False)

    print(f"✅ ¡Video repotenciado con éxito en: {target_queue_dir}!")
    return str(final_queue_video)

def main():
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    completed = []
    
    print(f"Iniciando Re-Ingeniería Viral de {len(PROJECTS)} Videos Pendientes:")
    start_time = time.time()
    
    for idx, proj in enumerate(PROJECTS, 1):
        print(f"\n>>> MEJORANDO VIDEO {idx}/{len(PROJECTS)}: {proj['id']} <<<")
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
    print(f"RESUMEN FINAL: {len(completed)}/{len(PROJECTS)} Videos Optimizados")
    print(f"Tiempo Total: {total_time/60:.2f} minutos")
    print(f"=======================================================")
    for proj, v_path, dur in completed:
        print(f" - [{dur:.1f}s] {proj['queue_folder']}: {proj['title']}")

if __name__ == "__main__":
    main()
