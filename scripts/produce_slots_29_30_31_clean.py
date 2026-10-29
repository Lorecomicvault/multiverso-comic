"""
Production Script for Slots 29, 30, and 31 (100% Clean, Fresh & Unprecedented Stories)
========================================================================================
- Slot 29: Daredevil - El Asombroso Sentido Radar (Mark Waid / Paolo Rivera)
- Slot 30: Hellboy - El Secreto de la Mano Derecha del Destino (Anung Un Rama)
- Slot 31: Swamp Thing - La Perturbadora Autopsia (The Anatomy Lesson / Alan Moore)

Voicebox: CUDA local port 17493, Profile ID: 28078056-1a1d-43d4-9d57-d616275f13c2 (Narrador Referencia Cómic)
Retention: 1.08x tempo, +1.8dB volume boost, curiosity hook in Scene 1, Top Hook Header in ASS Bangers.
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

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

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

NEW_PROJECTS = [
    {
        "id": "29_daredevil_sentido_radar",
        "queue_folder": "29_dia7_10h_daredevil_sentido_radar",
        "title": "¡El Sentido Radar de Daredevil! La Visión que Superó la Ceguera 📡🦯",
        "character": "Daredevil",
        "folder": "daredevil_sentido_radar_mark_waid",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Alguna vez te has preguntado cómo percibe el mundo Daredevil sin usar los ojos? No es simple oscuridad ni un vacío negro; ¡su cerebro traduce cada mínima vibración sonora, cada eco y cada impacto del entorno en un mapa tridimensional perfecto!"
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "A través de una ecolocalización hipersensible que avergonzaría a los murciélagos, Matt Murdock puede oír el latido acelerado de un corazón culpable a dos manzanas de distancia, sintiendo cómo el flujo de la sangre revela las mentiras de sus enemigos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cuando la lluvia cae torrencialmente sobre Hell's Kitchen, millones de gotas impactando en las calles le otorgan una visión nítida y cristalina, delineando cada rascacielos, cada bala en el aire y cada silueta con una precisión visual asombrosa."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Aunque sus ojos fueron quemados por químicos radiactivos en su infancia, Daredevil demostró al mundo que la verdadera visión nace del espíritu, convirtiendo la tragedia de su ceguera en el radar más letal y elegante de todo Marvel."
            }
        ],
        "description": "¿Cómo ve el mundo Daredevil? La asombrosa representación visual del sentido radar de Matt Murdock creada por Mark Waid y Paolo Rivera.",
        "hashtags": "#Daredevil #MattMurdock #MarkWaid #MarvelComics #Marvel #HellsKitchen #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "30_hellboy_mano_derecha_destino",
        "queue_folder": "30_dia7_13h_hellboy_mano_derecha_destino",
        "title": "¡El Secreto de la Mano de Hellboy! La Llave del Apocalipsis 🔴🔑",
        "character": "Hellboy",
        "folder": "hellboy_mano_derecha_del_destino_anung",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías por qué la mano derecha de Hellboy es de gigantesca piedra roja indestructible y jamás puede empuñar una espada normal? ¡Porque no es un arma terrenal, sino la llave cósmica diseñada para despertar a los monstruos del Apocalipsis!"
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Conocida como la Mano Derecha del Destino, esta reliquia ancestral perteneció originalmente al espíritu Anum, quien la utilizó para encerrar al temible Dragón Ogdru Jahad en el abismo del espacio exterior antes del inicio del tiempo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Los hechiceros oscuros invocaron al demonio en 1944 esperando coronar a Anung Un Rama, la Bestia profetizada para abrir las puertas del infierno y hacer arder la Tierra en cenizas con el fuego de su corona maldita."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Pero criado por el bondadoso profesor Trevor Bruttenholm, Hellboy se limó sus enormes cuernos con una amoladora y juró proteger a la humanidad, demostrando que tu verdadero destino lo forjan tus decisiones y jamás tu sangre."
            }
        ],
        "description": "¿Por qué la mano de Hellboy es de piedra roja? El secreto de la Mano Derecha del Destino, Anung Un Rama y la llave del Apocalipsis.",
        "hashtags": "#Hellboy #MikeMignola #DarkHorseComics #AnungUnRama #RightHandOfDoom #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "31_swamp_thing_leccion_anatomia",
        "queue_folder": "31_dia7_17h_swamp_thing_leccion_anatomia",
        "title": "¡La Perturbadora Autopsia de Swamp Thing! El Gran Engaño del Pantano 🌿🫀",
        "character": "Swamp Thing",
        "folder": "swamp_thing_leccion_anatomia",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Sabías cuál fue la autopsia más escalofriante en la historia de los cómics? Cuando el Dr. Jason Woodrue abrió el pecho congelado de Swamp Thing en una mesa de acero, no encontró un solo hueso ni órgano humano... ¡Descubrió una verdad aterradora!"
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Bajo el microscopio, los pulmones y el corazón eran pura vegetación podrida mimetizando formas humanas. El científico comprendió el engaño biológico: la criatura nunca necesitó respirar ni bombear sangre para mantenerse con vida."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "El científico dictó su demoledora conclusión: Alec Holland murió quemado en la explosión original. La flora del pantano absorbió su mente y su conciencia creyendo erróneamente durante años que era un hombre transformado en monstruo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al despertar y escuchar que su humanidad entera era una fantasía botánica, Swamp Thing desató una furia vegetal titánica, rompiendo sus cadenas criogénicas para renacer como el dios absoluto del reino verde."
            }
        ],
        "description": "La Lección de Anatomía (Alan Moore): La escalofriante autopsia que reveló que Alec Holland nunca sobrevivió al pantano.",
        "hashtags": "#SwampThing #AlanMoore #TheAnatomyLesson #DCComics #Vertigo #AlecHolland #Comics #Shorts #Reels #TikTok"
    }
]

def synthesize_voicebox_scene(text: str, out_wav: str, profile_id: str = PROFILE_ID) -> str:
    Path(out_wav).parent.mkdir(parents=True, exist_ok=True)
    payload = {'profile_id': profile_id, 'text': text}
    
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
        raise RuntimeError(f"No se pudo iniciar generación en Voicebox para: {text[:40]}")

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

    # 1. Generar audios con Voicebox
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

    # 4. Ensamblar Reel con transiciones y Hook Banner
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
        "duration_seconds": round(final_dur, 2),
        "voice_profile": "Narrador Referencia Cómic (Voicebox Optimizado 1.08x)",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(final_queue_meta, "w", encoding="utf-8") as f:
        json.dump(meta_payload, f, indent=2, ensure_ascii=False)

    print(f"✅ ¡Video repotenciado con éxito en: {target_queue_dir}!")
    return str(final_queue_video)

def main():
    print("Iniciando reemplazo de slots duplicados 29, 30 y 31...")
    
    old_duplicates = [
        "29_dia7_10h_ms_marvel_niebla_terrigena",
        "30_dia7_13h_thor_indigno_susurro_luna",
        "31_dia7_17h_miles_morales_legado_aracnido"
    ]
    for old_d in old_duplicates:
        target_p = SCHEDULED_QUEUE / old_d
        if target_p.exists():
            print(f"Eliminando carpeta duplicada previa: {old_d}")
            shutil.rmtree(target_p)

    completed = []
    start_time = time.time()
    
    for idx, proj in enumerate(NEW_PROJECTS, 1):
        print(f"\n>>> PRODUCIENDO VIDEO {idx}/{len(NEW_PROJECTS)}: {proj['id']} <<<")
        v_path = produce_and_schedule_single(proj)
        dur = get_duration(v_path)
        completed.append((proj, v_path, dur))

    total_time = time.time() - start_time
    print(f"\n=======================================================")
    print(f"RESUMEN FINAL: {len(completed)}/{len(NEW_PROJECTS)} Videos Inéditos Producidos")
    print(f"Tiempo Total: {total_time/60:.2f} minutos")
    print(f"=======================================================")
    for proj, v_path, dur in completed:
        print(f" - [{dur:.1f}s] {proj['queue_folder']}: {proj['title']}")

if __name__ == "__main__":
    main()
