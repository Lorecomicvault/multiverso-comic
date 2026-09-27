import csv
import os
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
    extract_thumbnail,
    get_duration,
)
from .transcribe import transcribe_scenes_to_ass, transcribe_to_ass_word, extract_scene_word_timings
from .voiceover import DEFAULT_VOICE, generate_voiceover_scenes
from .social_overlay import get_or_create_vertical_cta_mov
from .comic_pipeline import assemble_reel

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
    generate_thumbnail: bool = True,
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

    # Concatenar todos los audios individuales en uno general
    full_audio_path = output_dir / 'voiceover' / 'narration_full.wav'
    if has_voiceover and voice_results:
        audio_inputs = []
        filter_inputs = []
        for idx, sn in enumerate(sorted(voice_results.keys())):
            audio_inputs.extend(['-i', voice_results[sn]['audio']])
            filter_inputs.append(f'[{idx}:a]')
        n_a = len(filter_inputs)
        a_filter = f"{''.join(filter_inputs)}concat=n={n_a}:v=0:a=1[aout]"
        cmd_cat = ['ffmpeg', '-y', *audio_inputs, '-filter_complex', a_filter, '-map', '[aout]', str(full_audio_path)]
        subprocess.run(cmd_cat, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    # Preparar ruta del video final
    if final_video_dir is not None:
        final_dir = Path(final_video_dir)
    else:
        env_dir = os.environ.get('FINAL_VIDEO_DIR')
        final_dir = Path(env_dir) if env_dir else (Path.home() / 'Downloads' / 'comics en espanol')
    final_dir.mkdir(parents=True, exist_ok=True)

    meta = script.get('metadata') or {}
    title = meta.get('title', '') or output_name
    safe_name = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')[:80]
    final_video = str(final_dir / f'{safe_name}.mp4')

    # Si es video vertical y tenemos locución, ejecutamos el Motor Cinematográfico Maestro
    if height == 1920 and has_voiceover and len(composed_scenes) > 1:
        log("Ejecutando Motor Maestro: Papel Rasgado 3D (0.65s), Foley sincronizado y Caja de Narrador Bangers...")
        word_json = str(output_dir / 'word_timings.json')
        words_data = extract_scene_word_timings(voice_results, word_json, language='es', model_name='base')
        words_timing = [{"word": w['text'], "start": w['start'], "end": w['end']} for w in words_data.get('words', [])]

        # Extraer palabras clave de alto impacto
        keywords = []
        title_words = re.findall(r'\b[A-Za-zÁÉÍÓÚáéíóúÑñ]{4,}\b', title)
        keywords.extend([w.upper() for w in title_words])
        for s in script.get('scenes', []):
            nar = s.get('voiceover_text') or s.get('narration') or ''
            caps = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}\b', nar)
            keywords.extend([c.upper() for c in caps])
        keywords = list(set(keywords))

        social_mov = None
        if os.environ.get('NO_SOCIAL_CTA', '0') != '1':
            cta_style = os.environ.get('SOCIAL_CTA_STYLE', 'dual_line')
            try:
                social_mov = get_or_create_vertical_cta_mov(cta_style)
                log(f"  OK -> Social CTA Overlay activado ({cta_style})")
            except Exception as e:
                log(f"  Warning: No se pudo preparar el overlay social: {e}")

        total_dur = words_data.get('total_duration', 30.0)
        cta_start = max(8.0, min(total_dur - 6.0, total_dur * 0.58))

        assemble_reel(
            panel_clips=composed_scenes,
            words_timing=words_timing,
            narration_audio=str(full_audio_path),
            output_mp4=final_video,
            work_dir=str(output_dir / 'master_reel'),
            keywords=keywords,
            social_cta_mov=social_mov,
            cta_start_time=cta_start,
            alignment=5,
            margin_v=20,
            font_size=58,
        )
    else:
        # Fallback estándar para videos 16:9 o sin locución
        log("Concatenando escenas con sincronización estándar...")
        concat_path = str(output_dir / 'concatenated.mp4')
        concat_videos_audio(composed_scenes, concat_path, transition_duration=0)
        ass_path = None
        if has_voiceover:
            ass_path = str(output_dir / 'subtitles.ass')
            transcribe_scenes_to_ass(voice_results, ass_path, language='es', width=width, height=height)
        if ass_path and Path(ass_path).exists():
            compose_final(concat_path, ass_path, final_video, width=width, height=height)
        else:
            compose_final_pure(concat_path, final_video)

    log(f"  OK -> Video final generado: {final_video}")

    # Generate high-impact thumbnail (if enabled)
    if generate_thumbnail and os.environ.get('NO_THUMB', '0') != '1':
        thumb_path = str(final_dir / f'{safe_name}_thumb.jpg')
        try:
            extract_thumbnail(final_video, thumb_path, timestamp=2.5)
            log(f"  OK -> Miniatura oficial generada: {thumb_path}")
        except Exception as e:
            log(f"  Warning: No se pudo generar archivo de miniatura: {e}")

    scene_guides = {s['scene_number']: s.get('visual_guide', '') for s in scenes_sorted}
    description = _generate_description(script, scene_guides)
    hashtags = _generate_hashtags(script, scene_guides)
    social_title = _generate_social_title(script)
    _append_video_log(str(final_dir), title, f'{safe_name}.mp4', description, hashtags, social_title)
    log(f"  OK -> {VIDEO_LOG_FILE} actualizado")

    return final_video
