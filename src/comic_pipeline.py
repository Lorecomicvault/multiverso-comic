import os
import math
import subprocess
from pathlib import Path

try:
    from .comic_transitions import build_torn_paper_clip
    from .comic_subtitles import generate_comic_ass
except ImportError:
    from comic_transitions import build_torn_paper_clip
    from comic_subtitles import generate_comic_ass

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

def assemble_reel(
    panel_clips: list[str],
    words_timing: list[dict],
    narration_audio: str,
    output_mp4: str,
    work_dir: str,
    fonts_dir: str = None,
    sfx_rip: str = None,
    keywords: list[str] = None,
    social_cta_mov: str = None,
    cta_start_time: float = 18.0,
    cta_duration: float = 5.0,
    alignment: int = 5,
    margin_v: int = 20,
    font_size: int = 58
) -> str:
    """
    Motor Cinematográfico Maestro para Video Vertical (1080x1920):
    1. Trimming inteligente y transiciones orgánicas de papel rasgado lento (0.65s).
    2. Mezcla de audio Foley sincronizada con 'paper_rip.mp3' en cada corte.
    3. Subtítulos dinámicos estilo 'Caja de Narrador Comic Noir' (Bangers, #181818, resaltado #00F0FF).
    4. Overlay elegante de tarjeta de redes sociales (@MultiversoComic) en Safe Zone.
    5. Normalización de audio profesional con EBU R128 (loudnorm).
    """
    if fonts_dir is None:
        fonts_dir = str(ASSETS_DIR / "fonts")
    if sfx_rip is None:
        sfx_rip = str(ASSETS_DIR / "audio" / "paper_rip.mp3")
    if social_cta_mov is None:
        default_cta = ASSETS_DIR / "vertical_cta_multiversocomic_dual_line.mov"
        if default_cta.exists():
            social_cta_mov = str(default_cta)

    os.makedirs(work_dir, exist_ok=True)
    num_panels = len(panel_clips)
    trans_duration = 0.65
    half_trans = trans_duration / 2.0
    sequence = []
    trans_times = []
    cum_time = 0.0

    print(f"[Master Assembler] Procesando {num_panels} viñetas dinámicas...")

    # 1. Trimming de clips y renderizado de transiciones de papel rasgado
    for i in range(num_panels):
        raw_c = panel_clips[i]
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", raw_c],
            stdout=subprocess.PIPE, text=True, check=True
        )
        dur = float(res.stdout.strip())

        t_start = 0.0 if i == 0 else half_trans
        t_dur = max(0.4, dur - half_trans) if (i == 0 or i == num_panels - 1) else max(0.4, dur - trans_duration)
        trimmed = os.path.join(work_dir, f"trim_{i:02d}.mp4")
        
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", f"{t_start:.3f}",
            "-i", raw_c,
            "-t", f"{t_dur:.3f}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "veryfast",
            trimmed
        ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        sequence.append(trimmed)

        if i < num_panels - 1:
            trans_c = os.path.join(work_dir, f"trans_{i:02d}.mp4")
            temp_trans_dir = os.path.join(work_dir, f"temp_torn_{i:02d}")
            # Alternar dirección de rasgado para un efecto hiperrealista
            direction = "left_to_right" if (i % 2 == 0) else "right_to_left"
            print(f"  -> Generando transición de papel rasgado {i+1}/{num_panels-1} ({direction})...")
            build_torn_paper_clip(
                raw_c, panel_clips[i+1], trans_c, temp_trans_dir,
                duration=trans_duration, direction=direction
            )
            sequence.append(trans_c)
            cum_time += dur
            trans_times.append(max(0.0, cum_time - half_trans))

    # 2. Concat list
    concat_txt = os.path.join(work_dir, "concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in sequence:
            f.write(f"file '{os.path.abspath(c).replace(os.sep, '/')}'\n")

    # 3. Mezcla de audio Foley (sonidos de rasgado en cada corte de papel)
    mixed_audio = os.path.join(work_dir, "audio_mixed.mp3")
    if os.path.exists(sfx_rip) and trans_times:
        print(f"[Master Assembler] Mezclando {len(trans_times)} efectos Foley de rasgado de papel...")
        cmd_a = ["ffmpeg", "-y", "-i", narration_audio]
        f_parts = []
        for idx, t in enumerate(trans_times):
            cmd_a.extend(["-i", sfx_rip])
            delay = int(round(t * 1000))
            f_parts.append(f"[{idx+1}:a]adelay={delay}|{delay},volume=0.85[s{idx}]")
        f_str = ";".join(f_parts) + f";[0:a]" + "".join(f"[s{k}]" for k in range(len(trans_times))) + f"amix=inputs={1+len(trans_times)}:duration=first:normalize=0[aout]"
        cmd_a.extend(["-filter_complex", f_str, "-map", "[aout]", "-c:a", "libmp3lame", "-b:a", "192k", mixed_audio])
        subprocess.run(cmd_a, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        final_audio = mixed_audio
    else:
        final_audio = narration_audio

    # 4. Generar subtítulos .ass estilo Caja de Narrador (Comic Noir)
    ass_path = os.path.join(work_dir, "subs.ass")
    print(f"[Master Assembler] Creando subtítulos ASS con estética Comic Noir y tipografía Bangers...")
    generate_comic_ass(
        words_timing, ass_path, font_name="Bangers",
        box_bgr="&H00181818", text_bgr="&H00FFFFFF", highlight_bgr="&H0000F0FF",
        keywords=keywords, alignment=alignment, margin_v=margin_v, font_size=font_size
    )

    # 5. Renderizado final quemando subtítulos y compositando overlay social
    escaped_ass = os.path.abspath(ass_path).replace(os.sep, "/").replace(":", r"\:")
    escaped_fonts = os.path.abspath(fonts_dir).replace(os.sep, "/").replace(":", r"\:")

    has_cta = social_cta_mov and os.path.exists(social_cta_mov)
    print(f"[Master Assembler] Ensamblando video final con FFmpeg (CTA activo: {has_cta})...")

    Path(output_mp4).parent.mkdir(parents=True, exist_ok=True)

    if has_cta:
        cmd_final = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", final_audio,
            "-itsoffset", f"{cta_start_time:.3f}", "-i", social_cta_mov,
            "-filter_complex", (
                f"[0:v][2:v]overlay=0:0:eof_action=pass[vcta];"
                f"[vcta]subtitles=f='{escaped_ass}':fontsdir='{escaped_fonts}'[vout]"
            ),
            "-map", "[vout]",
            "-map", "1:a",
            "-af", "loudnorm=I=-14:LRA=7:TP=-2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", output_mp4
        ]
    else:
        vf_sub = f"subtitles=f='{escaped_ass}':fontsdir='{escaped_fonts}'"
        cmd_final = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt,
            "-i", final_audio,
            "-vf", vf_sub,
            "-af", "loudnorm=I=-14:LRA=7:TP=-2",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", output_mp4
        ]

    subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    print(f"[Master Assembler] ¡Video vertical cinematográfico exportado exitosamente! -> {output_mp4}")
    return output_mp4
