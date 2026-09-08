import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REMOTION_DIR = Path(__file__).resolve().parent.parent / 'remotion'


def get_remotion_cmd() -> list[str]:
    """Resolves the most reliable command to execute Remotion."""
    bin_name = 'remotion.cmd' if sys.platform == 'win32' else 'remotion'
    bin_path = REMOTION_DIR / 'node_modules' / '.bin' / bin_name
    if bin_path.exists():
        return [str(bin_path)]
    
    # Check npm run
    npm_bin = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    return [npm_bin, 'run', 'render', '--']


def check_remotion_available() -> bool:
    """Checks if Node, npm and Remotion are available in the current environment."""
    bin_name = 'remotion.cmd' if sys.platform == 'win32' else 'remotion'
    bin_path = REMOTION_DIR / 'node_modules' / '.bin' / bin_name
    if bin_path.exists():
        return True
    
    npm_bin = 'npm.cmd' if sys.platform == 'win32' else 'npm'
    try:
        r = subprocess.run(
            [npm_bin, 'run', 'compositions'],
            cwd=str(REMOTION_DIR),
            capture_output=True,
            text=True,
            timeout=25
        )
        return r.returncode == 0
    except Exception:
        return False


def export_word_timings(audio_path: str, output_json: str, language: str = 'es'):
    from .transcribe import transcribe_with_words
    data = transcribe_with_words(audio_path, language=language)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_json


def render_with_remotion(
    concat_video: str,
    full_audio: str,
    word_timings_json: str,
    output_video: str,
    width: int = 1080,
    height: int = 1920,
    title: str = '',
) -> str:
    """
    Renders animated kinetic subtitles with Remotion over the composed video.
    """
    public_dir = REMOTION_DIR / 'public'
    public_dir.mkdir(parents=True, exist_ok=True)

    dest_video = public_dir / 'concatenated.mp4'
    dest_audio = public_dir / 'voiceover_full.mp3'

    shutil.copy2(concat_video, dest_video)
    shutil.copy2(full_audio, dest_audio)

    with open(word_timings_json, 'r', encoding='utf-8') as f:
        subtitle_data = json.load(f)

    props = {
        'subtitleData': subtitle_data,
        'width': width,
        'height': height,
        'title': title,
        'videoSrc': 'concatenated.mp4',
        'audioSrc': 'voiceover_full.mp3',
    }
    props_path = public_dir / 'input_props.json'
    with open(props_path, 'w', encoding='utf-8') as f:
        json.dump(props, f, ensure_ascii=False, indent=2)

    target_out = Path(output_video).resolve()
    target_out.parent.mkdir(parents=True, exist_ok=True)

    base_cmd = get_remotion_cmd()
    if 'npm' in base_cmd[0]:
        cmd = [
            *base_cmd,
            str(target_out),
            '--props', str(props_path),
            '--log', 'error',
            '--concurrency=2',
        ]
    else:
        cmd = [
            *base_cmd, 'render',
            'src/Root.tsx',
            'VideoComposition',
            str(target_out),
            '--props', str(props_path),
            '--log', 'error',
            '--concurrency=2',
        ]

    print(f"[Remotion] Invocando renderizado con {' '.join(cmd[:3])} ({width}x{height})...", flush=True)
    result = subprocess.run(
        cmd,
        cwd=str(REMOTION_DIR),
        capture_output=True,
        text=True,
        timeout=1800,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Remotion render error (exit {result.returncode}):\n{result.stderr}\n{result.stdout}")

    print(f"[Remotion] OK -> Video renderizado con subtítulos Remotion: {output_video}", flush=True)
    return str(target_out)

