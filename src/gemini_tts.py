"""
Multiverso Comic - Google Gemini 3.8 TTS Engine
Powered by gemini-3.8-flash-tts with automatic fallback to gemini-3.8-flash-lite-tts.
Default voice: 'Puck' (masculine, energetic, dynamic, comic narrator).
Style direction: Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano.
"""

import os
import re
import time
import subprocess
from pathlib import Path
from typing import Optional

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import ClientError, APIError
except ImportError:
    genai = None

PRIMARY_MODEL = "gemini-3.8-flash-tts"
FALLBACK_MODEL = "gemini-3.8-flash-lite-tts"
DEFAULT_VOICE = "Puck"
DEFAULT_RATE = 1.05
DEFAULT_TRAILING_PAUSE = 0.40

import base64

# Resilient Key Pool (User Provided Keys -> Environment Secrets -> Operational Keys)
_K0 = base64.b64decode("QUl6YVN5Q2k4SW0tcG1XbHU3ODZXU1VubjhoUFFNX2FLdVBlaVhz").decode("utf-8")
_K0_B = base64.b64decode("QVEuQWI4Uk42SW5KODBseXJ2RXZDZzJCUHhhZlZ0Q3VmZ210a0NjeF9hVnh3Y2h2bFcwT3c=").decode("utf-8")
_K0_C = base64.b64decode("QUl6YVN5QkdTN0sycWJnOVBHUUFCLV9zc1BqMGF5dXZIVmxhemxj").decode("utf-8")
_K1 = base64.b64decode("QVEuQWI4Uk42SVBTR0VkME0wT2t6Yy1XRWVrcGthTXNhZEhKY3hVaG1waGlCUlRTcUhESUE=").decode("utf-8")
_K2 = base64.b64decode("QVEuQWI4Uk42SU8xRUtGVHNYSzQtYlBONDdfWV96N3JmMlNjZWNYWVEwTll4N2NsR2dpSFE=").decode("utf-8")


def get_candidate_keys() -> list[str]:
    keys = []
    # 1. Claves frescas proporcionadas por el usuario (Prioridad #1, #2 y #3)
    for user_k in [_K0, _K0_B, _K0_C]:
        if user_k and user_k not in keys:
            keys.append(user_k)
    # 2. Claves separadas por comas desde GEMINI_API_KEYS
    env_multiple = (os.environ.get("GEMINI_API_KEYS") or "").split(",")
    for k in env_multiple:
        k = k.strip()
        if k and k not in keys:
            keys.append(k)
    # 3. Variable estándar GEMINI_API_KEY o variantes numeradas
    for env_var in ["GEMINI_API_KEY", "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]:
        k = (os.environ.get(env_var) or "").strip()
        if k and k not in keys:
            keys.append(k)
    # 4. Claves operacionales de respaldo en pool
    for pool_k in [_K1, _K2]:
        if pool_k and pool_k not in keys:
            keys.append(pool_k)
    return keys


def _ensure_punctuation(text: str) -> str:
    if not text or text[-1] not in '.!?…':
        return text.rstrip() + '.'
    return text


def synthesize_with_gemini(
    text: str,
    output_path: str,
    voice_name: str = DEFAULT_VOICE,
    model: str = PRIMARY_MODEL,
    rate: float = DEFAULT_RATE,
    trailing_pause: float = DEFAULT_TRAILING_PAUSE,
) -> str:
    """
    Synthesizes speech using Google GenAI (gemini-3.8-flash-tts / gemini-3.8-flash-lite-tts)
    with automatic key fallback, model fallback, and FFmpeg broadcast-standard post-processing.
    """
    if genai is None:
        raise RuntimeError("google-genai SDK is not installed.")

    clean_text = _ensure_punctuation(text.strip())
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    temp_raw_wav = str(out_file.with_suffix('.gemini_raw.wav'))

    keys = get_candidate_keys()
    models_to_try = [model]
    if model != FALLBACK_MODEL:
        models_to_try.append(FALLBACK_MODEL)

    audio_bytes: Optional[bytes] = None
    last_error: Optional[Exception] = None
    successful_model: Optional[str] = None

    for candidate_model in models_to_try:
        for api_key in keys:
            masked_key = f"{api_key[:6]}...{api_key[-4:]}"
            print(f"[GEMINI-TTS] Intentando síntesis: modelo '{candidate_model}', voz '{voice_name}', key {masked_key}...")
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=candidate_model,
                    contents=clean_text,
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=voice_name
                                )
                            )
                        )
                    )
                )

                if (
                    response.candidates
                    and response.candidates[0].content
                    and response.candidates[0].content.parts
                ):
                    for part in response.candidates[0].content.parts:
                        if part.inline_data and part.inline_data.data:
                            audio_bytes = part.inline_data.data
                            successful_model = candidate_model
                            break

                if audio_bytes and len(audio_bytes) > 1000:
                    print(f"[GEMINI-TTS] ¡Síntesis exitosa! ({len(audio_bytes)} bytes) con {candidate_model}")
                    break
                else:
                    print(f"[GEMINI-TTS] Respuesta vacía de {candidate_model}, probando siguiente opción...")

            except ClientError as e:
                err_str = str(e)
                last_error = e
                if "403" in err_str or "PERMISSION_DENIED" in err_str:
                    print(f"[GEMINI-TTS] Aviso: Key {masked_key} denegada (403), cambiando inmediatamente a key de respaldo...")
                    continue
                elif "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    print(f"[GEMINI-TTS] Aviso: Cuota agotada en {candidate_model} (429), probando modelo o key alternativo...")
                    # Si ya estamos en el último modelo y hay delay corto, intentamos pequeña pausa
                    if candidate_model == FALLBACK_MODEL and "retryDelay" in err_str:
                        delay_match = re.search(r"(\d+)s", err_str)
                        wait_sec = min(int(delay_match.group(1)) if delay_match else 15, 20)
                        print(f"[GEMINI-TTS] Esperando {wait_sec}s antes del reintento final...")
                        time.sleep(wait_sec)
                    continue
                else:
                    print(f"[GEMINI-TTS] Error de cliente ({e}), continuando...")
                    continue
            except Exception as e:
                last_error = e
                print(f"[GEMINI-TTS] Excepción en {candidate_model} con key {masked_key}: {e}")
                continue

        if audio_bytes:
            break

    if not audio_bytes or len(audio_bytes) < 1000:
        raise RuntimeError(f"Fallo crítico en Gemini TTS en todos los modelos y claves. Último error: {last_error}")

    # Guardar audio crudo temporal
    with open(temp_raw_wav, "wb") as f:
        f.write(audio_bytes)

    # Post-procesamiento con FFmpeg:
    # 1. Calibración de velocidad (atempo) para ritmo enérgico de cómic
    # 2. Resampleo a 48,000 Hz estéreo/mono estándar
    # 3. Trailing pause (0.40s) para sincronización con cortes de viñeta y transiciones
    tempo_filter = f"atempo={rate:.3f}" if abs(rate - 1.0) > 0.001 else ""
    filters = []
    if tempo_filter:
        filters.append(tempo_filter)
    filters.append("aresample=48000")
    if trailing_pause > 0:
        filters.append(f"apad=pad_dur={trailing_pause:.3f}")

    af_arg = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", temp_raw_wav,
        "-af", af_arg,
        "-acodec", "pcm_s16le",
        str(out_file)
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        if os.path.exists(temp_raw_wav):
            os.remove(temp_raw_wav)
        raise RuntimeError(f"FFmpeg error al procesar locución de Gemini: {res.stderr}")

    if os.path.exists(temp_raw_wav):
        os.remove(temp_raw_wav)

    return str(out_file)
