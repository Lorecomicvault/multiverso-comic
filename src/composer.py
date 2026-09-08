import subprocess
import json
import random
from pathlib import Path


def get_duration(file_path: str) -> float:
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'json',
        file_path,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(json.loads(r.stdout)['format']['duration'])


def compose_scene(video_path: str, audio_path: str, duration: float, output: str, width: int = 1080, height: int = 1920) -> str:
    """Denoise, smooth motion, mux audio (video is trimmed to match audio length)."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-filter_complex', (
            '[0:v]hqdn3d=luma_spatial=2:chroma_spatial=1:luma_tmp=0:chroma_tmp=0,'
            'minterpolate=mi_mode=mci:mc_mode=obmc:vsbmc=1:fps=60,'
            'fps=30,'
            'setpts=1.5*PTS,'
            f'scale={width}:{height}:force_original_aspect_ratio=decrease,'
            f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=white,'
            'unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.5,'
            'setsar=1[v];'
            '[1:a]dynaudnorm=p=0.95:m=100[a]'
        ),
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '20',
        '-r', '30',
        '-t', str(duration),
        '-c:a', 'aac',
        '-b:a', '192k',
        output,
    ], check=True, capture_output=True, text=True)
    return output


def _build_zoompan_exprs(pattern: str, total_frames: int, nf: int, duration: float, width: int, height: int) -> tuple[str, str, str, float, float]:
    """
    Movimiento de cámara dinámico y cinematográfico para viñetas y cómics.
    Mayor profundidad de zoom (20%-30%) y paneos para crear energía y retención visual.
    """
    t_norm = f'on/{nf}' if nf > 0 else '0'
    zoom_depth = 0.25
    rotation = 0.0

    if pattern == 'zoom-out':
        # Acercamiento inicial que se abre para revelar el plano completo
        z = f'1.25 - {zoom_depth} * {t_norm}'
        x = '(iw - iw/zoom)/2'
        y = '(ih - ih/zoom)/2'
    elif pattern == 'pan-up':
        # Paneo ascendente hacia el rostro del personaje con zoom activo
        z = '1.20'
        x = '(iw - iw/zoom)/2'
        y = f'(ih - ih/zoom) * (1 - {t_norm} * 0.8)'
    elif pattern == 'pan-down':
        # Paneo descendente
        z = '1.20'
        x = '(iw - iw/zoom)/2'
        y = f'(ih - ih/zoom) * ({t_norm} * 0.8)'
    elif pattern == 'pan-left-to-right':
        # Barrido horizontal suave
        z = '1.22'
        x = f'(iw - iw/zoom) * ({t_norm} * 0.8)'
        y = '(ih - ih/zoom)/2'
    elif pattern == 'pan-right-to-left':
        # Barrido horizontal inverso
        z = '1.22'
        x = f'(iw - iw/zoom) * (1 - {t_norm} * 0.8)'
        y = '(ih - ih/zoom)/2'
    else:
        # zoom-in dinámico
        z = f'1.0 + {zoom_depth} * {t_norm}'
        x = '(iw - iw/zoom)/2'
        y = '(ih - ih/zoom)/2'

    return z, x, y, zoom_depth, rotation


def compose_scene_from_image(image_path: str, audio_path: str, duration: float, output: str, pattern_idx: int = 0, width: int = 1080, height: int = 1920, audio_codec: str = 'aac') -> str:
    """Create a dynamic animated comic scene from an image with lively camera motion."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    fps = 30
    total_frames = max(2, int(duration * fps))
    nf = total_frames - 1

    patterns = ['zoom-in', 'zoom-out', 'pan-up', 'pan-down', 'pan-left-to-right', 'pan-right-to-left']
    pattern = patterns[pattern_idx % len(patterns)]

    z_expr, x_expr, y_expr, _, _ = _build_zoompan_exprs(
        pattern, total_frames, nf, duration, width, height
    )

    # Native 1080x1920 fast rendering without 4K CPU bottleneck
    video_chain = (
        f'[0:v]scale=\'max({width},iw)\':\'max({height},ih)\':force_original_aspect_ratio=increase,'
        f'zoompan=z=\'{z_expr}\':x=\'{x_expr}\':y=\'{y_expr}\':d={total_frames}:s={width}x{height}:fps={fps},'
        f'setsar=1[v]'
    )

    filter_complex = f'{video_chain};[1:a]dynaudnorm=p=0.95:m=100[a]'

    subprocess.run([
        'ffmpeg', '-y',
        '-t', f'{duration:.3f}',
        '-loop', '1',
        '-i', image_path,
        '-t', f'{duration:.3f}',
        '-i', audio_path,
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '18',
        '-r', str(fps),
        '-t', f'{duration:.3f}',
        '-c:a', audio_codec,
        '-b:a', '192k',
        output,
    ], check=True, capture_output=True, text=True)
    return output


def compose_scene_from_images(image_paths: list[str], audio_path: str, duration: float, output: str, pattern_start: int = 0, width: int = 1080, height: int = 1920) -> str:
    """Create a video from multiple images with dynamic Ken Burns zoom, splitting audio equally and concatenating."""
    n = len(image_paths)
    if n == 1:
        return compose_scene_from_image(image_paths[0], audio_path, duration, output, pattern_idx=pattern_start, width=width, height=height)

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    fps = 30
    seg_duration = duration / n
    segments = []
    stem = Path(output).stem

    for i, img_path in enumerate(image_paths):
        seg_video = str(Path(output).parent / f'{stem}_seg{i}.mp4')
        seg_audio = str(Path(output).parent / f'{stem}_aud{i}.wav')

        subprocess.run([
            'ffmpeg', '-y',
            '-i', audio_path,
            '-ss', str(i * seg_duration),
            '-t', str(seg_duration),
            seg_audio,
        ], check=True, capture_output=True, text=True)

        compose_scene_from_image(img_path, seg_audio, seg_duration, seg_video, pattern_idx=pattern_start + i, width=width, height=height, audio_codec='pcm_s16le')
        segments.append(seg_video)

    return concat_videos_audio(segments, output, transition_duration=0.45)


TRANSITION_TYPES = [
    'fade', 'dissolve', 'zoomin', 'slideleft', 'slideright', 'slideup', 'smoothleft', 'smoothright', 'circlecrop', 'wipeleft', 'wiperight'
]

MUSIC_BED_PATH = Path(__file__).resolve().parent.parent / 'music_bed.mp3'


def concat_videos_audio(video_paths: list[str], output: str, transition_duration: float = 0.0) -> str:
    """Concatenate videos sequentially with varied cinematic transitions."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    n = len(video_paths)
    if n == 1:
        cmd = [
            'ffmpeg', '-y',
            '-i', video_paths[0],
            '-c:v', 'copy',
            '-c:a', 'copy',
            output,
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output

    inputs = []
    for v in video_paths:
        inputs.extend(['-i', v])

    if transition_duration <= 0:
        video_inputs = ''.join(f'[{i}:v]' for i in range(n))
        audio_inputs = ''.join(f'[{i}:a]' for i in range(n))
        filter_chain = f'{video_inputs}concat=n={n}:v=1:a=0[v];{audio_inputs}concat=n={n}:v=0:a=1[ain];[ain]dynaudnorm=p=0.95:m=100[a]'
        cmd = [
            'ffmpeg', '-y', *inputs,
            '-filter_complex', filter_chain,
            '-map', '[v]',
            '-map', '[a]',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '16',
            '-r', '30',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            output,
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output

    durations = [get_duration(v) for v in video_paths]
    td = transition_duration

    chain = []
    cur_offset = durations[0]
    for i in range(1, n):
        t_type = random.choice(TRANSITION_TYPES)
        pair_td = min(td, durations[i] * 0.25, durations[i - 1] * 0.25)
        offset = max(0.1, cur_offset - pair_td)
        src_v = f'[{i-1}:v]' if i == 1 else f'[v{i-1}]'
        src_a = f'[{i-1}:a]' if i == 1 else f'[a{i-1}]'
        chain.append(
            f'{src_v}[{i}:v]xfade=transition={t_type}:duration={pair_td:.3f}:offset={offset:.3f}[v{i}]'
        )
        chain.append(
            f'{src_a}[{i}:a]acrossfade=d={pair_td:.3f}:c1=tri:c2=tri[a{i}]'
        )
        cur_offset = offset + durations[i]

    chain.append(f'[v{n-1}]format=yuv420p[v]')
    chain.append(f'[a{n-1}]dynaudnorm=p=0.95:m=100, aformat=sample_rates=44100:channel_layouts=stereo[a]')

    filter_chain = ';'.join(chain)

    cmd = [
        'ffmpeg', '-y', *inputs,
        '-filter_complex', filter_chain,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '16',
        '-r', '30',
        '-c:a', 'aac',
        '-b:a', '192k',
        output,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output



def compose_final(
    video_path: str,
    subs_path: str,
    output: str,
    width: int = 1080,
    height: int = 1920,
) -> str:
    """Final pass: fade in/out, loudness -14 LUFS, music bed w/ sidechain,
    color consistency, sharpening, subtitles + CTA, fast-start H.264."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)

    total = get_duration(video_path)
    fade_in = 0.3
    fade_out = 0.6
    fade_out_start = max(0.0, total - fade_out)

    escaped = subs_path.replace('\\', '/').replace(':', '\\:')

    has_music = MUSIC_BED_PATH.exists()

    # --- Video chain: consistent look + end fade + subtitles/CTA (no initial black fade for instant hook & crisp thumbnail) ---
    video_chain = (
        f'[0:v]eq=contrast=1.04:saturation=1.06:brightness=-0.01,'
        f'unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.5,'
        f'fade=t=out:st={fade_out_start}:d={fade_out},'
        f'ass=\'{escaped}\'[v]'
    )

    if has_music:
        audio_chain = (
            f'[0:a]dynaudnorm=p=0.95:m=100[voice];'
            f'[1:a]aloop=loop=-1:size=2e9,atrim=0:{total:.3f},volume=0.18[music];'
            f'[voice]asplit[vo1][vo2];'
            f'[music][vo2]sidechaincompress=threshold=0.02:ratio=8:attack=20:release=300:makeup=1[ducked];'
            f'[vo1][ducked]amix=inputs=2:duration=first,'
            f'loudnorm=I=-14:TP=-1.5:LRA=11,'
            f'afade=t=in:st=0:d={fade_in},'
            f'afade=t=out:st={fade_out_start}:d={fade_out}[a]'
        )
        inputs = ['-i', video_path, '-i', str(MUSIC_BED_PATH)]
    else:
        audio_chain = (
            f'[0:a]dynaudnorm=p=0.95:m=100,'
            f'loudnorm=I=-14:TP=-1.5:LRA=11,'
            f'afade=t=in:st=0:d={fade_in},'
            f'afade=t=out:st={fade_out_start}:d={fade_out}[a]'
        )
        inputs = ['-i', video_path]

    filter_complex = f'{video_chain};{audio_chain}'

    cmd = [
        'ffmpeg', '-y', *inputs,
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '18',
        '-profile:v', 'high',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-movflags', '+faststart',
        output,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output


def has_audio_stream(file_path: str) -> bool:
    cmd = [
        'ffprobe', '-v', 'error',
        '-select_streams', 'a',
        '-show_entries', 'stream=codec_type',
        '-of', 'json',
        file_path,
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(r.stdout)
        return len(data.get('streams', [])) > 0
    except Exception:
        return False


def compose_scene_pure(
    video_path: str,
    output: str,
    width: int = 1080,
    height: int = 1920,
    target_duration: float | None = None,
) -> str:
    """Prepares scene video with full native audio, padding, scaling, and noise reduction."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    has_audio = has_audio_stream(video_path)
    dur = target_duration or get_duration(video_path)

    video_filter = (
        f'scale={width}:{height}:force_original_aspect_ratio=decrease,'
        f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,'
        f'unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.4,'
        f'setsar=1[v]'
    )

    cmd = ['ffmpeg', '-y', '-i', video_path]
    if not has_audio:
        cmd.extend(['-f', 'lavfi', '-t', str(dur), '-i', 'anullsrc=r=44100:cl=stereo'])
        filter_complex = f'[0:v]{video_filter};[1:a]dynaudnorm=p=0.95:m=100[a]'
    else:
        filter_complex = f'[0:v]{video_filter};[0:a]dynaudnorm=p=0.95:m=100[a]'

    cmd.extend([
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '18',
        '-r', '30',
        '-t', str(dur),
        '-c:a', 'aac',
        '-b:a', '192k',
        output,
    ])

    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output



def compose_scene_from_image_pure(
    image_path: str,
    duration: float,
    output: str,
    pattern_idx: int = 0,
    width: int = 1080,
    height: int = 1920,
) -> str:
    """Animates static image with smooth Ken Burns motion and clean room tone audio."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    fps = 30
    total_frames = int(duration * fps)
    patterns = ['zoom-in', 'zoom-out']
    pattern = patterns[pattern_idx % len(patterns)]
    z_expr, x_expr, y_expr, _, _ = _build_zoompan_exprs(pattern, total_frames, total_frames, duration, width, height)

    cmd = [
        'ffmpeg', '-y',
        '-t', f'{duration:.3f}',
        '-loop', '1',
        '-i', image_path,
        '-t', f'{duration:.3f}',
        '-f', 'lavfi',
        '-i', 'anullsrc=r=44100:cl=stereo',
        '-filter_complex', (
            f'[0:v]scale={width}:{height}:force_original_aspect_ratio=increase,'
            f'crop={width}:{height},'
            f'zoompan=z=\'{z_expr}\':x=\'{x_expr}\':y=\'{y_expr}\':d={total_frames}:s={width}x{height}:fps={fps},'
            f'unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.4,'
            f'setsar=1[v];'
            f'[1:a]dynaudnorm=p=0.95:m=100[a]'
        ),
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-crf', '18',
        '-r', str(fps),
        '-t', f'{duration:.3f}',
        '-c:a', 'aac',
        '-b:a', '192k',
        output,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output


def compose_final_pure(
    video_path: str,
    output: str,
) -> str:
    """Final pass for pure ambient/scene audio without voiceover or subtitles."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    total = get_duration(video_path)
    fade_in = 0.3
    fade_out = 0.6
    fade_out_start = max(0.0, total - fade_out)

    has_music = MUSIC_BED_PATH.exists()

    video_chain = (
        f'[0:v]eq=contrast=1.03:saturation=1.05:brightness=-0.01,'
        f'unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.4,'
        f'fade=t=out:st={fade_out_start}:d={fade_out}[v]'
    )

    if has_music:
        audio_chain = (
            f'[0:a]dynaudnorm=p=0.95:m=100[ambient];'
            f'[1:a]aloop=loop=-1:size=2e9,atrim=0:{total:.3f},volume=0.2[music];'
            f'[ambient][music]amix=inputs=2:duration=first,'
            f'loudnorm=I=-14:TP=-1.5:LRA=11,'
            f'afade=t=in:st=0:d={fade_in},'
            f'afade=t=out:st={fade_out_start}:d={fade_out}[a]'
        )
        inputs = ['-i', video_path, '-i', str(MUSIC_BED_PATH)]
    else:
        audio_chain = (
            f'[0:a]dynaudnorm=p=0.95:m=100,'
            f'loudnorm=I=-14:TP=-1.5:LRA=11,'
            f'afade=t=in:st=0:d={fade_in},'
            f'afade=t=out:st={fade_out_start}:d={fade_out}[a]'
        )
        inputs = ['-i', video_path]

    filter_complex = f'{video_chain};{audio_chain}'

    cmd = [
        'ffmpeg', '-y', *inputs,
        '-filter_complex', filter_complex,
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '17',
        '-profile:v', 'high',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-movflags', '+faststart',
        output,
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output


def extract_thumbnail(
    video_path: str | Path,
    output: str | Path,
    timestamp: float = 2.5,
) -> str:
    """Extracts a crisp, full-resolution JPEG thumbnail from the video at a given timestamp."""
    vpath = Path(video_path)
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    dur = get_duration(str(vpath))
    actual_ts = min(timestamp, max(0.5, dur - 1.0)) if dur > 1.0 else 0.5

    cmd = [
        'ffmpeg', '-y',
        '-ss', f'{actual_ts:.3f}',
        '-i', str(vpath),
        '-vframes', '1',
        '-q:v', '2',
        str(out_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return str(out_path)
