import csv
import re
import subprocess
import time
from pathlib import Path

from .composer import (
    compose_final,
    compose_final_pure,
    compose_scene,
    compose_scene_from_image,
    compose_scene_from_image_pure,
    compose_scene_pure,
    concat_videos_audio,
    get_duration,
)
from .transcribe import transcribe_to_ass_word
from .voiceover import DEFAULT_VOICE, generate_voiceover_scenes

VIDEO_LOG_FILE = 'videos_log.csv'


def _motion_pattern(scene_number: int) -> int:
    """Elige el movimiento cinematográfico según el número de escena (cicla entre 6 patrones dinámicos)."""
    return (scene_number - 1) % 6


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def _generate_description(script: dict, scene_texts: dict[int, str]) -> str:
    meta = script.get('metadata') or {}
    title = (meta.get('title', '') or '').strip()
    scene_list = script.get('scenes', [])
    first_narration = ''
    for s in scene_list:
        first_narration = (s.get('voiceover_text') or s.get('narration') or '').strip()
        if first_narration:
            break

    full_text = ' '.join(scene_texts.values())
    hook = f'✨ {title}' if title else '✨ Comic Lore Shorts'
    body = first_narration[:200] if first_narration else full_text[:200]
    cta = '\n\n🎬 Generated with Comic Lore Engine.\n👇 Like & Subscribe for more epic comic book stories!'
    return f'{hook}\n\n{body}{cta}'


def _generate_hashtags(script: dict, scene_texts: dict[int, str]) -> str:
    return '#Comics #Marvel #DC #ComicLore #ComicBooks #Shorts #Reels #TikTok'


def _generate_social_title(script: dict) -> str:
    meta = script.get('metadata') or {}
    title = (meta.get('title', '') or '').strip()
    return title or 'Viral Comic Lore Story'


def _append_video_log(
    final_dir: str,
    title: str,
    filename: str,
    description: str,
    hashtags: str,
    social_title: str,
):
    log_path = Path(final_dir) / VIDEO_LOG_FILE
    file_exists = log_path.exists()
    row = {
        'fecha': time.strftime('%Y-%m-%d %H:%M'),
        'titulo': title,
        'titulo_redes': social_title,
        'archivo': filename,
        'descripcion': description,
        'hashtags': hashtags,
    }
    with open(log_path, 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['fecha', 'titulo', 'titulo_redes', 'archivo', 'descripcion', 'hashtags'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def run_pipeline(
    generation: dict,
    output_name: str | None = None,
    voice: str | None = None,
    rate: float | None = None,
    output_root: str = 'output',
    width: int = 1080,
    height: int = 1920,
    final_video_dir: str | None = None,
):
    gen_path = Path(generation['path'])
    scenes = generation['scene_videos']
    script = generation['script']

    if output_name is None:
        output_name = gen_path.name
    output_dir = Path(output_root) / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    scenes_sorted = sorted(scenes, key=lambda s: s['scene_number'])
    selected_voice = voice or 'en-US-Studio-Q'

    # Extraer textos de locución de cada escena
    scene_texts = {}
    for s in script.get('scenes', []):
        sn = s.get('scene_number', 1)
        text = s.get('voiceover_text') or s.get('narration') or ''
        if text.strip():
            scene_texts[sn] = text.strip()

    has_voiceover = len(scene_texts) > 0

    voice_results = {}
    if has_voiceover:
        log(f"Generando locuciones con {selected_voice} (Google Cloud TTS)...")
        vo_dir = str(output_dir / 'voiceover')
        voice_results = generate_voiceover_scenes(scene_texts, vo_dir, voice=selected_voice, rate=rate)
        log(f"  OK -> {len(voice_results)} locuciones generadas")

    # --- 1. Componer cada escena sincronizada con su audio ---
    log("Componiendo escenas con movimiento y audio sincronizado...")
    composed_scenes = []
    for s in scenes_sorted:
        sn = s['scene_number']
        composed = str(output_dir / 'composed' / f'scene_{sn:02d}.mp4')
        motion = _motion_pattern(sn)
        is_valid = False
        if Path(composed).exists() and Path(composed).stat().st_size > 1000:
            try:
                get_duration(composed)
                is_valid = True
            except Exception:
                is_valid = False
        if is_valid:
            log(f"  Escena {sn:02d} ya existe y es válida, omitiendo render...")
            composed_scenes.append(composed)
            continue

        if has_voiceover and sn in voice_results:
            audio_path = voice_results[sn]['audio']
            dur = get_duration(audio_path)
            if s.get('is_image', False):
                compose_scene_from_image(s['video'], audio_path, dur, composed, pattern_idx=motion, width=width, height=height)
            else:
                compose_scene(s['video'], audio_path, dur, composed, width=width, height=height)
        else:
            if s.get('is_image', False):
                compose_scene_from_image_pure(s['video'], duration=4.5, output=composed, pattern_idx=motion, width=width, height=height)
            else:
                compose_scene_pure(s['video'], composed, width=width, height=height)

        composed_scenes.append(composed)

    log(f"  OK -> {len(composed_scenes)} escenas compuestas")

    # --- 2. Concatenar escenas con transiciones cinemáticas ---
    log("Concatenando escenas con transiciones cinemáticas...")
    concat_path = str(output_dir / 'concatenated.mp4')
    concat_videos_audio(composed_scenes, concat_path, transition_duration=0.4)
    log(f"  OK -> {concat_path}")

    # --- 3. Generar subtítulos estilo cómic (Impact cursiva amarillo/blanco) ---
    ass_path = None
    if has_voiceover:
        log("Generando subtítulos dinámicos estilo cómic con Whisper...")
        concat_audio_path = str(output_dir / 'full_audio.wav')
        subprocess.run([
            'ffmpeg', '-y',
            '-i', concat_path,
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            concat_audio_path,
        ], check=True, capture_output=True, text=True)

        ass_path = str(output_dir / 'subtitles.ass')
        full_text = ' '.join(voice_results[sn]['text'] for sn in sorted(voice_results))
        transcribe_to_ass_word(concat_audio_path, ass_path, language='en', correct_text=full_text)
        log(f"  OK -> Subtítulos generados: {ass_path}")

    # --- 4. Masterización final con música de fondo y subtítulos ---
    log("Masterizando video final...")
    if final_video_dir is not None:
        final_dir = Path(final_video_dir)
    else:
        env_dir = os.environ.get('FINAL_VIDEO_DIR')
        final_dir = Path(env_dir) if env_dir else (Path.home() / 'Downloads' / 'comics en ingles')
    final_dir.mkdir(parents=True, exist_ok=True)

    meta = script.get('metadata') or {}
    title = meta.get('title', '') or output_name
    safe_name = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:80]
    final_video = str(final_dir / f'{safe_name}.mp4')

    if ass_path and Path(ass_path).exists():
        compose_final(concat_path, ass_path, final_video, width=width, height=height)
    else:
        compose_final_pure(concat_path, final_video)

    log(f"  OK -> Video final generado: {final_video}")

    scene_guides = {s['scene_number']: s.get('visual_guide', '') for s in scenes_sorted}
    description = _generate_description(script, scene_guides)
    hashtags = _generate_hashtags(script, scene_guides)
    social_title = _generate_social_title(script)
    _append_video_log(str(final_dir), title, f'{safe_name}.mp4', description, hashtags, social_title)
    log(f"  OK -> {VIDEO_LOG_FILE} actualizado")

    return final_video
