"""
Pilot Producer: FilmCraft 75s Master Video (Spider-Man Back in Black vs Kingpin)
==============================================================================
Produces a ~75-second (1m 15s) high-retention 1080x1920 @ 60fps video using:
- Voicebox Local CUDA (qwen 0.6B, language='es', Narrador Referencia Cómic)
- Whisper word-level alignment locked 1:1 to Spanish narration
- Native FilmCraft MCP video assembly, Ken Burns motion, page_turn/cross_zoom
  transitions, Master White + Pastel Pink karaoke subtitles, and 3-track audio mix.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

import requests
from src.filmcraft_engine import assemble_filmcraft_reel, get_media_duration
from src.transcribe import extract_scene_word_timings
from scripts.produce_lote_common import (
    PROFILE_REFERENCIA,
    PROFILE_ZAZOOM,
    render_minimal_text_thumb,
)

VOICEBOX_URL = "http://127.0.0.1:17493"


def synthesize_voicebox_es(text: str, out_wav: Path, profile_id: str = PROFILE_REFERENCIA) -> Path:
    """Synthesizes Spanish narration via local Voicebox using fast 0.6B model."""
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "profile_id": profile_id,
        "text": text,
        "language": "es",
        "model_size": "0.6B",
        "normalize": True,
    }

    for attempt in range(1, 5):
        # Wait politely if another generation is running
        for _ in range(60):
            try:
                act = requests.get(f"{VOICEBOX_URL}/tasks/active", timeout=5)
                if act.status_code == 200 and not act.json().get("generations"):
                    break
            except Exception:
                pass
            time.sleep(1.5)

        r = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=25)
        if r.status_code != 200:
            time.sleep(3)
            continue
        gid = r.json()["id"]

        for poll_i in range(300):
            time.sleep(1.0)
            h = requests.get(f"{VOICEBOX_URL}/history/{gid}", timeout=10).json()
            status = h.get("status")
            if status == "completed":
                aud = requests.get(f"{VOICEBOX_URL}/audio/{gid}", timeout=30)
                raw_tmp = str(out_wav) + ".raw.wav"
                with open(raw_tmp, "wb") as f:
                    f.write(aud.content)
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        raw_tmp,
                        "-af",
                        "silenceremove=start_periods=1:start_silence=0.12:start_threshold=-45dB,aresample=48000,apad=pad_dur=0.22",
                        "-acodec",
                        "pcm_s16le",
                        str(out_wav),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if Path(raw_tmp).exists():
                    Path(raw_tmp).unlink()
                return out_wav
            elif status == "failed":
                print(f"  [Voicebox Error] {h.get('error')} (attempt {attempt})")
                time.sleep(3)
                break
    raise TimeoutError(f"Voicebox timeout for: {text[:40]}")


def run_pilot():
    curated_dir = PROJECT_ROOT / "assets" / "curated_panels" / "fc_01_spiderman_back_in_black_kingpin"
    curated_dir.mkdir(parents=True, exist_ok=True)

    asm542_dir = (
        PROJECT_ROOT
        / "assets"
        / "comics_source"
        / "spiderman_back_in_black"
        / "extracted_asm_542"
        / "The Amazing Spider-Man 542 (2007) (digital) (Minutemen-InnerDemons)"
    )
    bib248_dir = PROJECT_ROOT / "assets" / "curated_panels" / "248_spiderman_back_in_black_disparo_tia_may"

    panel_sources = {
        "scene_1.jpg": asm542_dir / "The Amazing Spider-Man 542-008.jpg",  # Sin máscara en prisión
        "scene_2.jpg": bib248_dir / "scene_1.jpg",                         # Disparo a Tía May
        "scene_3.jpg": bib248_dir / "scene_2.jpg",                         # Cargándola al hospital
        "scene_4.jpg": bib248_dir / "scene_4.jpg",                         # Traje negro bajo la lluvia
        "scene_5.jpg": asm542_dir / "The Amazing Spider-Man 542-014.jpg",  # Golpiza/bofetadas a Kingpin
        "scene_6.jpg": asm542_dir / "The Amazing Spider-Man 542-015.jpg",  # Agarra por la garganta a Kingpin
        "scene_7.jpg": asm542_dir / "The Amazing Spider-Man 542-018.jpg",  # Kingpin humillado sangrando en el suelo
        "scene_8.jpg": asm542_dir / "The Amazing Spider-Man 542-019.jpg",  # Spider-Man se balancea dejando la cárcel en silencio
    }

    for dst_name, src_path in panel_sources.items():
        if not src_path.exists():
            raise FileNotFoundError(f"Falta panel fuente: {src_path}")
        shutil.copy2(src_path, curated_dir / dst_name)

    scenes = [
        {
            "scene_number": 1,
            "file": "scene_1.jpg",
            "text": "Frente a cientos de reclusos en máxima seguridad, Peter Parker se quita lentamente la máscara. Hoy no viene como Spider-Man, viene como un hombre dispuesto a matar.",
        },
        {
            "scene_number": 2,
            "file": "scene_2.jpg",
            "text": "Días atrás, tras revelar su identidad en la Guerra Civil, un francotirador ejecutó la orden de Wilson Fisk. La bala destrozó el pecho de la tía May frente a Mary Jane.",
        },
        {
            "scene_number": 3,
            "file": "scene_3.jpg",
            "text": "Desesperado y sin llamar a los Vengadores, Peter recorrió la ciudad cargándola entre sus brazos, rompiendo cada ventana de su pasado con tal de mantenerla con vida.",
        },
        {
            "scene_number": 4,
            "file": "scene_4.jpg",
            "text": "Esa noche desenterró su traje negro bajo la tormenta. Juró ante el cielo que cuando encontrara al verdadero culpable, abandonaría para siempre su regla de no asesinar.",
        },
        {
            "scene_number": 5,
            "file": "scene_5.jpg",
            "text": "Al llegar a prisión, Kingpin creyó poder aplastarlo con su enorme fuerza bruta. Pero Peter no esquivó ni hizo chistes: lo tomó de la piel y lo abofeteó sin piedad.",
        },
        {
            "scene_number": 6,
            "file": "scene_6.jpg",
            "text": "Frente a toda la cárcel paralizada por el miedo, lo levantó del cuello como a un muñeco de trapo, destruyendo en segundos el imperio de terror que Fisk construyó.",
        },
        {
            "scene_number": 7,
            "file": "scene_7.jpg",
            "text": "Con Kingpin sangrando en el suelo, Peter sentenció que si May muere, regresará y llenará sus pulmones de telaraña para ahogarlo en tres segundos.",
        },
        {
            "scene_number": 8,
            "file": "scene_8.jpg",
            "text": "Dejando a toda la prisión muda de pánico, Peter desapareció entre las sombras. Y tú, ¿cruzarías esa línea definitiva si tocaran a tu familia?",
        },
    ]

    work_dir = PROJECT_ROOT / "work" / "filmcraft_pilot_01"
    work_dir.mkdir(parents=True, exist_ok=True)

    # 1. Voicebox Narration
    raw_audios = {}
    for sc in scenes:
        sn = sc["scene_number"]
        out_wav = work_dir / f"raw_scene_{sn:02d}.wav"
        if not out_wav.exists() or out_wav.stat().st_size < 5000:
            print(f"[Pilot Voicebox] Sintetizando Escena {sn}/{len(scenes)}...")
            synthesize_voicebox_es(sc["text"], out_wav, profile_id=PROFILE_REFERENCIA)
        raw_audios[sn] = out_wav

    raw_durs = [get_media_duration(raw_audios[sn]) for sn in sorted(raw_audios.keys())]
    sum_raw = sum(raw_durs)
    print(f"[Pilot] Duraciones crudas Voicebox: {[round(d, 2) for d in raw_durs]} -> Total: {sum_raw:.2f}s")

    # Calibrate subtly towards 75.0s target (clamp between 0.94 and 1.08 for natural cadence)
    target_dur = 75.0
    speed = max(0.94, min(1.08, sum_raw / target_dur))
    print(f"[Pilot] Factor atempo calibrado: {speed:.3f}")

    cal_dir = work_dir / "calibrated"
    cal_dir.mkdir(parents=True, exist_ok=True)
    voice_results = {}
    scene_items = []

    for sc in scenes:
        sn = sc["scene_number"]
        cal_w = cal_dir / f"scene_{sn:02d}.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_audios[sn]),
                "-af",
                f"atempo={speed:.3f}",
                "-c:a",
                "pcm_s16le",
                str(cal_w),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        dur = get_media_duration(cal_w)
        voice_results[sn] = {"audio": str(cal_w), "text": sc["text"]}
        scene_items.append({"image": curated_dir / sc["file"], "duration": dur})

    # Concatenate full narration
    full_audio = work_dir / "narration_full.wav"
    cmd_cat = ["ffmpeg", "-y"]
    f_parts = []
    for i, sn in enumerate(sorted(voice_results.keys())):
        cmd_cat.extend(["-i", voice_results[sn]["audio"]])
        f_parts.append(f"[{i}:a]")
    cmd_cat.extend(
        [
            "-filter_complex",
            "".join(f_parts) + f"concat=n={len(voice_results)}:v=0:a=1[outa]",
            "-map",
            "[outa]",
            str(full_audio),
        ]
    )
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_audio_dur = get_media_duration(full_audio)
    print(f"[Pilot] Narración total concatenada: {total_audio_dur:.2f}s")

    # 2. Whisper Word Timings
    word_json = work_dir / "word_timings.json"
    words_data = extract_scene_word_timings(voice_results, str(word_json), language="es", model_name="base")
    words_timing = [{"word": w["text"], "start": w["start"], "end": w["end"]} for w in words_data.get("words", [])]

    # 3. Assemble and Render with FilmCraft Engine
    out_mp4 = PROJECT_ROOT / "output" / "pilot_filmcraft_75s_spiderman_kingpin.mp4"
    final_dur = assemble_filmcraft_reel(
        scene_items=scene_items,
        words_timing=words_timing,
        narration_audio=full_audio,
        output_mp4=out_mp4,
        work_dir=work_dir / "fc_work",
        hook_text="¿POR QUÉ SPIDER-MAN JURÓ MATAR A KINGPIN?",
        hook_duration=7.0,
        seq_name="Pilot_SpiderMan_BackInBlack_75s",
        bitrate_kbps=14000,
    )

    # 4. Generate matching high-contrast thumbnail
    thumb_path = PROJECT_ROOT / "output" / "pilot_filmcraft_75s_thumb.jpg"
    render_minimal_text_thumb(
        image_path=curated_dir / "scene_1.jpg",
        text="SIN MÁSCARA Y SIN PIEDAD",
        output_path=thumb_path,
        text_y=240,
        text_color=(255, 235, 0),
        font_size=82,
    )

    print(f"\n✅ PILOTO FILMCRAFT COMPLETADO: {out_mp4} ({final_dur:.2f}s)")


if __name__ == "__main__":
    run_pilot()
