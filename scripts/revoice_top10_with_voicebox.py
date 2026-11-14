import os, sys, json, time, shutil, subprocess, requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.composer import compose_scene_from_image, get_duration
from src.transcribe import extract_scene_word_timings
from src.comic_pipeline import assemble_reel
from src.social_overlay import get_or_create_vertical_cta_mov
from scripts.produce_top10_viral_25s import TOP10_VIRAL_PROJECTS

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2" # Narrador Referencia Cómic

FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
if not Path(FONT_IMPACT).exists():
    FONT_IMPACT = r"C:\Users\Vanes\comics en espanol\fonts\impact.ttf"

def synthesize_voicebox_scene(text: str, out_wav: Path) -> Path:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    payload = {'profile_id': PROFILE_ID, 'text': text}
    
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
        raise RuntimeError(f"No se pudo iniciar generación en Voicebox para: {text[:30]}")

    for _ in range(80):
        time.sleep(1.0)
        try:
            st = requests.get(f"{VOICEBOX_URL}/generate/{gen_id}/status", timeout=10)
            for line in st.text.splitlines():
                if line.startswith('data:'):
                    j = json.loads(line[5:].strip())
                    status = j.get('status')
                    if status == 'completed':
                        audio_res = requests.get(f"{VOICEBOX_URL}/audio/{gen_id}", timeout=25)
                        raw_tmp = str(out_wav) + '.raw.wav'
                        with open(raw_tmp, 'wb') as f:
                            f.write(audio_res.content)
                        subprocess.run([
                            'ffmpeg', '-y', '-i', raw_tmp,
                            '-af', 'aresample=48000,apad=pad_dur=0.25',
                            '-acodec', 'pcm_s16le', str(out_wav)
                        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if Path(raw_tmp).exists():
                            Path(raw_tmp).unlink()
                        return out_wav
                    elif status == 'failed':
                        raise RuntimeError(f"Voicebox falló: {j.get('error')}")
        except Exception as e:
            if "Voicebox falló" in str(e):
                raise e
    raise TimeoutError(f"Voicebox timeout para: {text[:30]}")

def apply_cinematic_grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.22)
    im = ImageEnhance.Color(im).enhance(1.20)
    return im

def fit_to_vertical(im: Image.Image, target_w=1080, target_h=1920) -> Image.Image:
    w, h = im.size
    aspect = w / h
    target_aspect = target_w / target_h

    if aspect > target_aspect:
        bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(35))
        bg = ImageEnhance.Brightness(bg).enhance(0.40)

        new_w = target_w
        new_h = int(target_w / aspect)
        fg = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

        pos_y = (target_h - new_h) // 2
        bg.paste(fg, (0, pos_y))
        return bg
    else:
        scale = max(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)
        scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - target_w) // 2
        top = (nh - target_h) // 2
        return scaled.crop((left, top, left + target_w, top + target_h))

def render_minimal_text_thumb(image_path: Path, text: str, output_path: Path,
                              text_y=240, text_color=(255, 235, 0), font_size=95):
    raw_img = Image.open(image_path).convert("RGB")
    graded = apply_cinematic_grade(raw_img)
    canvas = fit_to_vertical(graded, 1080, 1920)

    font = ImageFont.truetype(FONT_IMPACT, font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    if tw > 960:
        adjusted_size = int(font_size * (940 / tw))
        font = ImageFont.truetype(FONT_IMPACT, adjusted_size)
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

    tx = (1080 - tw) // 2 - bbox[0]
    ty = text_y

    canvas_rgba = canvas.convert("RGBA")
    shadow_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((tx, ty + 7), text, font=font, fill=(0, 0, 0, 240), stroke_width=20, stroke_fill=(0, 0, 0, 240))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))

    canvas_rgba = Image.alpha_composite(canvas_rgba, shadow_layer)

    text_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    t_draw.text((tx, ty), text, font=font, fill=text_color, stroke_width=11, stroke_fill=(0, 0, 0))

    final_im = Image.alpha_composite(canvas_rgba, text_layer).convert("RGB")
    final_im.save(output_path, "JPEG", quality=95, optimize=True)
    return output_path

def inject_thumbnail_into_video(video_path: Path, thumb_path: Path):
    temp_out = video_path.parent / f"{video_path.stem}_frame0.mp4"
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-loop', '1', '-t', '0.40', '-i', str(thumb_path),
        '-filter_complex',
        '[1:v]fps=30,scale=1080:1920,setsar=1[vthumb];[0:v]trim=start=0.40,setpts=PTS-STARTPTS[vmain];[vthumb][vmain]concat=n=2:v=1:a=0[v]',
        '-map', '[v]',
        '-map', '0:a',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        '-c:a', 'copy',
        str(temp_out)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and temp_out.exists():
        video_path.unlink()
        shutil.move(temp_out, video_path)
        return True
    return False

def process_top10_slot(proj: dict):
    slot = proj["slot"]
    slot_str = f"{slot:03d}"
    title = proj["title"]
    print(f"\n=======================================================")
    print(f"🎬 PROCESANDO CON VOICEBOX (CUDA): SLOT {slot} - {title}")
    print(f"=======================================================")

    work_dir = PROJECT_ROOT / "work" / f"voicebox_top10_{slot:02d}"
    work_dir.mkdir(parents=True, exist_ok=True)
    curated_dir = PROJECT_ROOT / proj["folder"] if Path(proj["folder"]).is_absolute() else PROJECT_ROOT / "assets" / "curated_panels" / proj["folder"]
    
    # 1. Synthesize 4 scenes in Voicebox
    raw_audios = {}
    for sc in proj["scenes"]:
        sn = sc["scene_number"]
        txt = sc["text"]
        out_wav = work_dir / f"raw_scene_{sn:02d}.wav"
        if not out_wav.exists() or out_wav.stat().st_size < 5000:
            print(f"  [Voicebox] Sintetizando Escena {sn}/4: {txt[:40]}...")
            synthesize_voicebox_scene(txt, out_wav)
        raw_audios[sn] = out_wav

    # Measure raw audio duration
    raw_durs = [get_duration(str(raw_audios[sn])) for sn in sorted(raw_audios.keys())]
    sum_raw = sum(raw_durs)
    print(f"  [Voicebox Raw Durations]: {[f'{d:.2f}s' for d in raw_durs]} | Total: {sum_raw:.2f}s")

    # Target total audio: ~27.0s to 28.5s (so after -1.95s transitions + frame 0, video is 26.0s - 28.0s)
    target_audio = 27.5
    calibrated_speed = sum_raw / target_audio
    # Clamp speed between 0.82 and 0.95
    calibrated_speed = max(0.82, min(0.95, calibrated_speed))
    print(f"  [Calibration] Factor de velocidad atempo: {calibrated_speed:.3f}")

    calibrated_dir = work_dir / "calibrated"
    calibrated_dir.mkdir(parents=True, exist_ok=True)
    voice_results = {}
    for sn, raw_w in raw_audios.items():
        cal_w = calibrated_dir / f"scene_{sn:02d}.wav"
        txt = proj["scenes"][sn-1]["text"]
        subprocess.run([
            'ffmpeg', '-y', '-i', str(raw_w),
            '-af', f'atempo={calibrated_speed:.3f},apad=pad_dur=0.35',
            '-c:a', 'pcm_s16le', str(cal_w)
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        voice_results[sn] = {'audio': str(cal_w), 'text': txt}

    full_audio = str(work_dir / "narration_full.wav")
    audio_inputs = []
    filter_inputs = []
    for idx, sn in enumerate(sorted(voice_results.keys())):
        audio_inputs.extend(['-i', voice_results[sn]['audio']])
        filter_inputs.append(f'[{idx}:a]')
    a_filter = f"{''.join(filter_inputs)}concat=n={len(filter_inputs)}:v=0:a=1[aout]"
    subprocess.run(['ffmpeg', '-y', *audio_inputs, '-filter_complex', a_filter, '-map', '[aout]', full_audio],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_audio_dur = get_duration(full_audio)
    print(f"  [Audio Total Calibrado]: {total_audio_dur:.2f}s")

    # 2. Componer escenas con Ken Burns y canvas 1080x1920
    composed_dir = work_dir / "composed"
    composed_dir.mkdir(parents=True, exist_ok=True)
    composed_scenes = []
    motion_map = {1: 0, 2: 1, 3: 2, 4: 3}

    for sc in proj["scenes"]:
        sn = sc["scene_number"]
        src_img = str(curated_dir / sc["file"])
        audio_path = voice_results[sn]['audio']
        dur = get_duration(audio_path)
        out_clip = str(composed_dir / f"scene_{sn:02d}.mp4")
        compose_scene_from_image(src_img, audio_path, dur, out_clip, pattern_idx=motion_map.get(sn, 0), width=1080, height=1920)
        composed_scenes.append(out_clip)

    # 3. Extraer timestamps de palabras con Whisper
    word_json = str(work_dir / "word_timings.json")
    words_data = extract_scene_word_timings(voice_results, word_json, language='es', model_name='base')
    words_timing = [{"word": w['text'], "start": w['start'], "end": w['end']} for w in words_data.get('words', [])]

    # Palabras clave
    keywords = [proj["character"].upper()]
    for sc in proj["scenes"]:
        for w in sc["text"].split():
            clean_w = ''.join(c for c in w if c.isalnum()).upper()
            if len(clean_w) > 4:
                keywords.append(clean_w)
    keywords = list(set(keywords))[:20]

    # 4. Ensamblar Reel
    master_mp4 = str(work_dir / "master.mp4")
    social_mov = get_or_create_vertical_cta_mov("motion")
    hook_short = title.split('!')[0] + '!' if '!' in title else title[:35]

    assemble_reel(
        panel_clips=composed_scenes,
        words_timing=words_timing,
        narration_audio=full_audio,
        output_mp4=master_mp4,
        work_dir=str(work_dir / "assemble_work"),
        keywords=keywords,
        social_cta_mov=social_mov,
        cta_start_time=max(8.0, min(total_audio_dur - 7.0, total_audio_dur * 0.58)),
        alignment=5,
        margin_v=20,
        font_size=58,
        hook_title=hook_short
    )

    assembled_dur = get_duration(master_mp4)
    print(f"  [Video Maestro]: {assembled_dur:.2f}s")

    # 5. Renderizar miniatura minimalista e inyectar en frame 0
    min_cfg = proj["minimal_thumb"]
    art_path = PROJECT_ROOT / min_cfg["source_art"]
    thumb_path = work_dir / "thumb.jpg"
    render_minimal_text_thumb(
        image_path=art_path,
        text=min_cfg["text"],
        output_path=thumb_path,
        text_y=min_cfg.get("text_y", 240),
        text_color=min_cfg.get("color", (255, 235, 0)),
        font_size=min_cfg.get("font_size", 95)
    )
    inject_thumbnail_into_video(Path(master_mp4), thumb_path)
    final_dur = get_duration(master_mp4)
    print(f"  [FINAL CON FRAME 0]: {final_dur:.2f}s")

    # 6. Actualizar scheduled_queue
    # Detect queue directory (check both 07X and 7X)
    target_dir = None
    for cand in [f"{slot:03d}_{proj['queue_folder'].split('_', 1)[-1]}", proj["queue_folder"]]:
        qpath = PROJECT_ROOT / "scheduled_queue" / cand
        if qpath.exists():
            target_dir = qpath
            break
    if not target_dir:
        target_dir = PROJECT_ROOT / "scheduled_queue" / f"{slot:03d}_{proj['queue_folder'].split('_', 1)[-1]}"
        target_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(master_mp4, target_dir / "video.mp4")
    shutil.copy2(thumb_path, target_dir / "thumb.jpg")

    meta_path = target_dir / "metadata.json"
    meta = {}
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    meta["slot"] = slot
    meta["queue_folder"] = target_dir.name
    meta["id"] = proj["id"]
    meta["title"] = proj["title"]
    meta["character"] = proj["character"]
    meta["description"] = proj.get("description", "")
    meta["hashtags"] = proj.get("hashtags", "")
    meta["duration"] = round(final_dur, 2)
    meta["video_file"] = "video.mp4"
    meta["thumbnail_file"] = "thumb.jpg"
    meta["format"] = "viral_top10_25_30s"
    meta["voice_profile"] = "Narrador Referencia Cómic (Voicebox Profile 28078056-1a1d-43d4-9d57-d616275f13c2)"
    meta["voice_engine"] = "Voicebox Local CUDA"
    meta["produced_at"] = time.strftime('%Y-%m-%d %H:%M:%S')

    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"✅ SLOT {slot} ({target_dir.name}) ACTUALIZADO CON ÉXITO: {final_dur:.2f}s")
    return target_dir, final_dur

def main():
    # Slots 71 to 79 (Slot 70 was already verified and updated)
    slots_to_process = [p for p in TOP10_VIRAL_PROJECTS if p["slot"] in range(71, 80)]
    print(f"Iniciando re-voceo de {len(slots_to_process)} proyectos Top 10 con Voicebox...")

    results = []
    for proj in slots_to_process:
        try:
            tdir, dur = process_top10_slot(proj)
            results.append((proj["slot"], tdir.name, dur, "OK"))
        except Exception as e:
            print(f"❌ ERROR en Slot {proj['slot']}: {e}")
            results.append((proj["slot"], proj.get("title", ""), 0, f"ERROR: {e}"))

    print("\n" + "=" * 80)
    print("RESUMEN DE PROCESAMIENTO TOP 10 (VOICEBOX):")
    for r in results:
        print(f"Slot {r[0]}: {r[1]} -> {r[2]}s [{r[3]}]")
    print("=" * 80)

if __name__ == "__main__":
    main()
