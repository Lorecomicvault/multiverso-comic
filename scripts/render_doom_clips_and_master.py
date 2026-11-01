"""
RENDERIZADO MAESTRO COMPLETO: DOCTOR DOOM (AVENGERS: DOOMSDAY)
==============================================================
- 44 Escenas en Full HD 1080p con movimiento cinemático (Ken Burns)
- Subtítulos estilo Cómic ZaZooM (Arial Black, blanco con contorno negro)
- Logo animado de Multiverso Cómic en esquina superior derecha
- Banda sonora cinemática sutil (-32 dB)
- Exportación del video maestro y generación de Launch Kit
"""

import os
import sys
import json
import time
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageFont, ImageDraw

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "doctor_doom_doomsday_long")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
PANELS_1080P = os.path.join(OUTPUT_DIR, "panels_1080p")
CLIPS_DIR = os.path.join(OUTPUT_DIR, "clips")
THUMBNAILS_DIR = os.path.join(OUTPUT_DIR, "thumbnails")
MUSIC_BED = os.path.join(BASE_DIR, "music_bed.mp3")
CORNER_BUG_MOV = os.path.join(BASE_DIR, "scratch", "multiverso_corner_bug.mov")
FINAL_MASTER_VIDEO = os.path.join(OUTPUT_DIR, "doctor_doom_historia_completa_1080p.mp4")

FFMPEG = r"C:\Users\Vanes\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.EXE"
if not os.path.exists(FFMPEG):
    FFMPEG = "ffmpeg"

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(THUMBNAILS_DIR, exist_ok=True)

MOTION_PATTERNS = [
    "zoom-in",
    "pan-left-to-right",
    "zoom-out",
    "pan-up",
    "pan-right-to-left",
    "pan-down"
]

def format_ts(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    cs = int((s - int(s)) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

def generate_scene_ass(sid, text, duration):
    ass_path = os.path.join(CLIPS_DIR, f"sub_{sid:03d}.ass")
    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Narration,Arial,48,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.8,2.0,2,60,60,70,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    words = text.split()
    chunk_size = 6
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    if not chunks:
        chunks = [text]

    time_per_chunk = duration / len(chunks)
    for idx, chunk in enumerate(chunks):
        t_start = idx * time_per_chunk
        t_end = (idx + 1) * time_per_chunk
        start_str = format_ts(t_start)
        end_str = format_ts(t_end)
        ass_content += f"Dialogue: 0,{start_str},{end_str},Narration,,0,0,0,,{chunk}\n"

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
    return ass_path

def get_motion_exprs(pattern, nf):
    if pattern == "zoom-out":
        z = f"1.12-0.10*(on/{nf})"
        x = "(iw-iw/zoom)/2"
        y = "(ih-ih/zoom)/2"
    elif pattern == "pan-left-to-right":
        z = "1.10"
        x = f"(iw-iw/zoom)*(on/{nf})"
        y = "(ih-ih/zoom)/2"
    elif pattern == "pan-right-to-left":
        z = "1.10"
        x = f"(iw-iw/zoom)*(1-on/{nf})"
        y = "(ih-ih/zoom)/2"
    elif pattern == "pan-up":
        z = "1.10"
        x = "(iw-iw/zoom)/2"
        y = f"(ih-ih/zoom)*(1-on/{nf})"
    elif pattern == "pan-down":
        z = "1.10"
        x = "(iw-iw/zoom)/2"
        y = f"(ih-ih/zoom)*(on/{nf})"
    else:  # zoom-in
        z = f"1.02+0.10*(on/{nf})"
        x = "(iw-iw/zoom)/2"
        y = "(ih-ih/zoom)/2"
    return z, x, y

def render_scene(sid):
    meta_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.json")
    wav_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.wav")
    panel_path = os.path.join(PANELS_1080P, f"panel_{sid:03d}.jpg")
    out_mp4 = os.path.join(CLIPS_DIR, f"clip_{sid:03d}.mp4")

    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 100000:
        return sid, out_mp4, True

    if not os.path.exists(meta_path) or not os.path.exists(wav_path) or not os.path.exists(panel_path):
        return sid, None, False

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    duration = meta["duration"]
    text = meta["text"]

    ass_path = generate_scene_ass(sid, text, duration)
    escaped_ass = ass_path.replace("\\", "/").replace(":", "\\:")

    fps = 30
    total_frames = max(2, int(duration * fps))
    nf = total_frames - 1

    pattern = MOTION_PATTERNS[(sid - 1) % len(MOTION_PATTERNS)]
    z, x, y = get_motion_exprs(pattern, nf)

    vf_filter = (
        f"scale=2880:1620:flags=bicubic,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={total_frames}:s=1920x1080:fps={fps},"
        f"ass='{escaped_ass}',format=yuv420p"
    )

    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", panel_path,
        "-i", wav_path,
        "-vf", vf_filter,
        "-c:v", "libx264", "-preset", "veryfast", "-b:v", "4000k",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.3f}",
        "-shortest",
        out_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sid, out_mp4, True

def render_all_clips():
    print("=== [Paso 3] Renderizado Paralelo de Clips en 1080p con Ken Burns ===")
    sids_to_render = []
    for sid in range(1, 45):
        out_mp4 = os.path.join(CLIPS_DIR, f"clip_{sid:03d}.mp4")
        if not os.path.exists(out_mp4) or os.path.getsize(out_mp4) < 100000:
            sids_to_render.append(sid)

    if not sids_to_render:
        print("-> Todos los 44 clips ya están renderizados!")
        return

    print(f"-> Renderizando {len(sids_to_render)} clips restantes...")
    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(render_scene, sid): sid for sid in sids_to_render}
        for future in as_completed(futures):
            sid = futures[future]
            try:
                sid, out_mp4, success = future.result()
                if success:
                    print(f"   [Clip {sid:02d}/44] Listo: {os.path.basename(out_mp4)}")
                else:
                    print(f"   [Clip {sid:02d}/44] Pendiente de insumos (audio/panel)")
            except Exception as e:
                print(f"   [Clip {sid:02d}/44] Error: {e}")

def concatenate_and_master():
    print("\n=== [Paso 4] Ensamble Maestro, Mezcla Sonora y Marca de Agua ===")
    concat_list = os.path.join(OUTPUT_DIR, "concat_clips_list.txt")
    with open(concat_list, "w", encoding="utf-8") as f:
        for sid in range(1, 45):
            clip_path = os.path.join(CLIPS_DIR, f"clip_{sid:03d}.mp4").replace("\\", "/")
            f.write(f"file '{clip_path}'\n")

    temp_concat = os.path.join(OUTPUT_DIR, "temp_concatenated.mp4")
    print("-> Concatenando clips de video...")
    cmd_concat = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        temp_concat
    ]
    subprocess.run(cmd_concat, check=True)

    print("-> Obteniendo duracion exacta de video concatenado...")
    probe_cmd = [
        FFMPEG.replace("ffmpeg.EXE", "ffprobe.exe").replace("ffmpeg.exe", "ffprobe.exe"),
        "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", temp_concat
    ]
    dur_res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
    exact_duration = float(dur_res.stdout.strip())
    print(f"-> Duracion exacta: {exact_duration:.2f} segundos")

    print("-> Aplicando banda sonora orquestal a -32 dB y marca de agua Multiverso Cómic...")
    filter_complex = (
        "[0:v][2:v]overlay=W-w-30:30:shortest=1[v];"
        "[1:a]volume=0.035,aloop=loop=-1:size=2e+09[bgm];"
        "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
    )

    cmd_master = [
        FFMPEG, "-y",
        "-i", temp_concat,
        "-i", MUSIC_BED,
        "-stream_loop", "-1", "-i", CORNER_BUG_MOV,
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[a]",
        "-t", f"{exact_duration:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
        "-c:a", "aac", "-b:a", "256k",
        "-movflags", "+faststart",
        FINAL_MASTER_VIDEO
    ]
    subprocess.run(cmd_master, check=True)
    if os.path.exists(temp_concat):
        os.remove(temp_concat)
    print(f"-> VIDEO MAESTRO GENERADO EXITOSAMENTE:\n   {FINAL_MASTER_VIDEO}")

if __name__ == "__main__":
    render_all_clips()
    concatenate_and_master()
