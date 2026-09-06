import json
import subprocess
import shutil
from pathlib import Path


REMOTION_DIR = Path(__file__).resolve().parent.parent / 'remotion'


def export_word_timings(audio_path: str, output_json: str):
    from .transcribe import transcribe_with_words
    data = transcribe_with_words(audio_path)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return output_json


def render_with_remotion(
    concat_video: str,
    full_audio: str,
    word_timings_json: str,
    output_video: str,
    width: int = 720,
    height: int = 1280,
    title: str = '',
):
    public_dir = REMOTION_DIR / 'public'
    public_dir.mkdir(exist_ok=True)

    shutil.copy2(concat_video, public_dir / 'concatenated.mp4')
    shutil.copy2(full_audio, public_dir / 'voiceover_full.mp3')

    with open(word_timings_json, encoding='utf-8') as f:
        subtitle_data = json.load(f)

    props = {
        'subtitleData': subtitle_data,
        'width': width,
        'height': height,
        'title': title,
    }
    props_path = public_dir / 'input_props.json'
    with open(props_path, 'w', encoding='utf-8') as f:
        json.dump(props, f, ensure_ascii=False)

    Path(output_video).parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        'npx.cmd', 'remotion', 'render',
        'src/Root.tsx',
        'VideoComposition',
        str(Path(output_video).resolve()),
        '--props', str(props_path),
        '--log', 'error',
    ]

    result = subprocess.run(
        cmd,
        cwd=str(REMOTION_DIR),
        capture_output=True,
        text=True,
        timeout=3600,
    )

    if result.returncode != 0:
        raise RuntimeError(f'Remotion render failed:\n{result.stderr}')

    return output_video
