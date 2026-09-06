from pathlib import Path
import json
import re


def get_downloads_folder() -> Path:
    return Path.home() / 'Downloads'


def _scan_single_dir(entry: Path) -> dict | None:
    script_path = entry / 'script.json'
    if not script_path.exists():
        return None

    scenes = sorted(
        [d for d in entry.iterdir() if d.is_dir() and re.match(r'^Escena_\d{2}$', d.name)],
        key=lambda d: int(re.search(r'\d+', d.name).group()),
    )

    scene_videos = []
    for sc in scenes:
        videos = sorted(list(sc.glob('video_*.mp4')) + list(sc.glob('animacion.mp4')) + list(sc.glob('scene_*.mp4')))
        images = sorted(list(sc.glob('imagen_*.png')) + list(sc.glob('imagen_*.jpg')))

        if videos:
            scene_videos.append({
                'folder': sc.name,
                'video': str(videos[0]),
                'videos': [str(v) for v in videos],
                'scene_number': int(re.search(r'\d+', sc.name).group()),
                'is_image': False,
            })
        elif images:
            scene_videos.append({
                'folder': sc.name,
                'video': str(images[0]),
                'images': [str(img) for img in images],
                'scene_number': int(re.search(r'\d+', sc.name).group()),
                'is_image': True,
                'image_count': len(images),
            })


    if not scene_videos:
        return None

    with open(script_path, encoding='utf-8') as f:
        script_data = json.load(f)

    return {
        'path': str(entry),
        'name': entry.name,
        'script': script_data,
        'scene_videos': scene_videos,
        'scene_count': len(scene_videos),
    }


def find_generations(base: Path | str | None = None) -> list[dict]:
    results = []
    if base is not None:
        base = Path(base)
        if (base / 'script.json').exists():
            result = _scan_single_dir(base)
            return [result] if result else []
        candidates = [base]
    else:
        downloads = get_downloads_folder()
        candidates = [
            downloads / 'Flow_Generations',
        ]

    seen = set()
    for c_dir in candidates:
        if not c_dir.exists():
            continue
        for entry in sorted(c_dir.iterdir()):
            if not entry.is_dir() or str(entry) in seen:
                continue
            result = _scan_single_dir(entry)
            if result:
                seen.add(str(entry))
                results.append(result)

    return results

