import asyncio
import base64
import json
import os
import random
import re
import subprocess
from pathlib import Path
import requests
import edge_tts

# Google Cloud Text-to-Speech API Key
GOOGLE_TTS_API_KEY = os.environ.get('GOOGLE_TTS_API_KEY', 'AIzaSyDpdDhoXt8GDwJ_sEj-vjtd6HqVflN_vSY')
GOOGLE_TTS_URL = 'https://texttospeech.googleapis.com/v1/text:synthesize'

# ============================================================================
# SANITIZACIÓN PARA MONETIZACIÓN
# ============================================================================

_HARD_REPLACEMENTS = {
    'hijo de puta': 'desgraciado',
    'hijos de puta': 'desgraciados',
    'hija de puta': 'desgraciada',
    'hijas de puta': 'desgraciadas',
    'putamadre': 'porquería',
    'puta': 'maldita',
    'putas': 'malditas',
    'puto': 'maldito',
    'putos': 'malditos',
    'pendejo': 'idiota',
    'pendeja': 'idiota',
    'pendejos': 'idiotas',
    'cabrón': 'tonto',
    'cabron': 'tonto',
    'carajo': 'demonios',
    'verga': 'diablos',
    'chingada': 'maldita',
    'chingar': 'estafar',
    'chingaste': 'perdiste',
    'maricón': 'necio',
    'maricon': 'necio',
    # English replacements for monetization safety
    'motherfucker': 'monster',
    'motherfuckers': 'monsters',
    'fucking': 'brutal',
    'fuck': 'ruin',
    'fucked': 'ruined',
    'asshole': 'coward',
    'assholes': 'cowards',
    'bastard': 'fiend',
    'bastards': 'fiends',
    'bitch': 'villain',
    'bitches': 'villains',
}

_SOFT_REPLACEMENTS = {
    'mierda': 'porquería',
    'mierdas': 'porquerías',
    'joder': 'fastidiar',
    'jodiendo': 'fastidiando',
    'jodido': 'complicado',
    'jodida': 'complicada',
    'jodidos': 'complicados',
    'coño': 'demonios',
    'cojones': 'narices',
    'cagaste': 'perdiste',
    'cagar': 'meter la pata',
    'cagada': 'porquería',
    'hostia': 'vaya',
    'hostias': 'vaya',
    'gilipollas': 'imbécil',
    # English soft replacements
    'bullshit': 'nonsense',
    'shit': 'crap',
    'shitty': 'awful',
    'pissed': 'enraged',
    'piss': 'anger',
    'dammit': 'blast it',
}

SOFT_PROFANITY_BUDGET = 3

# ============================================================================
# PERFILES DE VOZ (Google Cloud TTS y Edge-TTS)
# ============================================================================

VOICE_PROFILES = {
    # --- Google Cloud TTS (Voces Principales de Alta Calidad) ---
    'es-US-Studio-B': {
        'provider': 'google',
        'lang': 'es-US',
        'gender': 'MALE',
        'rate': 1.05,
        'pitch': 0.0,
        'label': 'Google Studio B (US/Latam, narración cómic/documental)',
    },
    'es-US-Neural2-B': {
        'provider': 'google',
        'lang': 'es-US',
        'gender': 'MALE',
        'rate': 1.05,
        'pitch': 0.0,
        'label': 'Google Neural2 B (US/Latam, masculina dinámica)',
    },
    'es-US-News-D': {
        'provider': 'google',
        'lang': 'es-US',
        'gender': 'MALE',
        'rate': 1.05,
        'pitch': 0.0,
        'label': 'Google News D (US/Latam, narrador reportaje)',
    },
    'es-US-Chirp3-HD-Fenrir': {
        'provider': 'google',
        'lang': 'es-US',
        'gender': 'MALE',
        'rate': 1.05,
        'pitch': 0.0,
        'label': 'Google Chirp3 Fenrir (US/Latam, moderna)',
    },
    'es-ES-Studio-F': {
        'provider': 'google',
        'lang': 'es-ES',
        'gender': 'MALE',
        'rate': 1.02,
        'pitch': 0.0,
        'label': 'Google Studio F (ES, masculina)',
    },

    
    # --- English Voices (Google Cloud Journey & Studio) ---
    'en-US-Studio-Q': {
        'provider': 'google',
        'lang': 'en-US',
        'gender': 'MALE',
        'rate': 1.02,
        'pitch': 0.0,
        'label': 'Google Studio Q (US, deep epic male narrator)',
    },
    'en-US-Journey-D': {
        'provider': 'google',
        'lang': 'en-US',
        'gender': 'MALE',
        'rate': 1.04,
        'pitch': 0.0,
        'label': 'Google Journey D (US, storytelling male narrator)',
    },
    'en-US-Journey-F': {
        'provider': 'google',
        'lang': 'en-US',
        'gender': 'FEMALE',
        'rate': 1.04,
        'pitch': 0.0,
        'label': 'Google Journey F (US, storytelling female)',
    },
    'en-US-Studio-O': {
        'provider': 'google',
        'lang': 'en-US',
        'gender': 'FEMALE',
        'rate': 1.02,
        'pitch': 0.0,
        'label': 'Google Studio O (US, female narrator)',
    },
    'en-US-ChristopherNeural': {
        'provider': 'edge',
        'rate': 1.02,
        'pitch': '+0Hz',
        'label': 'Christopher (Edge-TTS US, male narrator)',
    },

    # --- Edge-TTS (Respaldo) ---
    'es-MX-JorgeNeural': {
        'provider': 'edge',
        'rate': 1.05,
        'pitch': '+2Hz',
        'label': 'Jorge (Edge-TTS MX, masculina)',
    },
    'es-CO-GonzaloNeural': {
        'provider': 'edge',
        'rate': 1.0,
        'pitch': '+0Hz',
        'label': 'Gonzalo (Edge-TTS CO, masculina)',
    },
    'es-US-AlonsoNeural': {
        'provider': 'edge',
        'rate': 1.02,
        'pitch': '+0Hz',
        'label': 'Alonso (Edge-TTS US, masculina)',
    },
}

DEFAULT_VOICE = 'en-US-Studio-Q'
SCENE_TRAILING_PAUSE = 0.4


def _match_case(original: str, replacement: str) -> str:
    if original[:1].isupper():
        return replacement.capitalize()
    return replacement


def sanitize_narration(text: str, soft_used: list[int] | None = None, force_clean: bool = False) -> str:
    if soft_used is None:
        soft_used = [0]

    result = text
    for word, replacement in sorted(_HARD_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True):
        result = re.sub(
            rf'\b{re.escape(word)}\b',
            lambda m, _r=replacement: _match_case(m.group(0), _r),
            result,
            flags=re.IGNORECASE,
        )

    for word, replacement in sorted(_SOFT_REPLACEMENTS.items(), key=lambda kv: len(kv[0]), reverse=True):
        def _repl(match, _word=word, _repl=replacement):
            if not force_clean and soft_used[0] < SOFT_PROFANITY_BUDGET:
                soft_used[0] += 1
                return match.group(0)
            return _match_case(match.group(0), _repl)

        result = re.sub(rf'\b{re.escape(word)}\b', _repl, result, flags=re.IGNORECASE)

    return result


def _ensure_punctuation(text: str) -> str:
    if not text or text[-1] not in '.!?…':
        return text.rstrip() + '.'
    return text


def _scene_pitch(base_pitch: str, text: str) -> str:
    match = re.match(r'([+-])(\d+(?:\.\d+)?)Hz', str(base_pitch))
    sign, value = (1.0, 0.0) if not match else (1.0 if match.group(1) == '+' else -1.0, float(match.group(2)))
    base = sign * value

    pitch = base + random.randint(-2, 2)
    stripped = text.strip()
    if stripped.endswith('?'):
        pitch += 4
    elif stripped.endswith('!'):
        pitch += 2

    pitch = max(-12, min(12, round(pitch)))
    return f'{pitch:+d}Hz'


# ============================================================================
# GENERADORES DE AUDIO
# ============================================================================

def _generate_google_tts(
    text: str,
    output: str,
    voice_name: str = 'es-US-Studio-B',
    lang_code: str = 'es-US',
    gender: str = 'MALE',
    rate: float = 1.05,
    pitch: float = 0.0,
    trailing_pause: float = SCENE_TRAILING_PAUSE,
) -> str:
    """Genera audio con Google Cloud Text-to-Speech API."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    clean_text = _ensure_punctuation(text)

    payload = {
        'input': {'text': clean_text},
        'voice': {
            'languageCode': lang_code,
            'name': voice_name,
            'ssmlGender': gender,
        },
        'audioConfig': {
            'audioEncoding': 'MP3',
            'speakingRate': rate,
            'pitch': pitch,
        },
    }

    url = f'{GOOGLE_TTS_URL}?key={GOOGLE_TTS_API_KEY}'
    res = requests.post(url, json=payload, timeout=20)
    if res.status_code != 200:
        raise RuntimeError(f'Google TTS API error ({res.status_code}): {res.text}')

    audio_base64 = res.json().get('audioContent', '')
    if not audio_base64:
        raise RuntimeError('Google TTS API returned empty audioContent')

    mp3_path = str(Path(output).with_suffix('.mp3'))
    with open(mp3_path, 'wb') as f:
        f.write(base64.b64decode(audio_base64))

    # Convertir a WAV estándar (pcm_s16le, 48000Hz) con pausa de cierre
    audio_filter = 'aresample=48000'
    if trailing_pause > 0:
        audio_filter += f',apad=pad_dur={trailing_pause:.3f}'

    subprocess.run([
        'ffmpeg', '-y',
        '-i', mp3_path,
        '-af', audio_filter,
        '-acodec', 'pcm_s16le',
        output,
    ], check=True, capture_output=True, text=True)

    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    return output


async def _generate_edge_tts(
    text: str,
    output: str,
    voice: str = 'es-MX-JorgeNeural',
    rate: float = 1.05,
    base_pitch: str = '+0Hz',
    trailing_pause: float = SCENE_TRAILING_PAUSE,
) -> str:
    """Genera audio con Edge-TTS (gratuito/respaldo)."""
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    rate_pct = int((rate - 1) * 100)
    rate_str = f'{rate_pct:+d}%'
    pitch = _scene_pitch(base_pitch, text)
    clean_text = _ensure_punctuation(text)

    mp3_path = str(Path(output).with_suffix('.mp3'))
    communicate = edge_tts.Communicate(clean_text, voice, rate=rate_str, pitch=pitch)
    await communicate.save(mp3_path)

    audio_filter = 'aresample=48000'
    if trailing_pause > 0:
        audio_filter += f',apad=pad_dur={trailing_pause:.3f}'

    subprocess.run([
        'ffmpeg', '-y',
        '-i', mp3_path,
        '-af', audio_filter,
        '-acodec', 'pcm_s16le',
        output,
    ], check=True, capture_output=True, text=True)

    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    return output


def _generate_one(
    text: str,
    output: str,
    voice: str = DEFAULT_VOICE,
    rate: float | None = None,
    pitch: str | float | None = None,
    trailing_pause: float = SCENE_TRAILING_PAUSE,
) -> str:
    """Genera locución seleccionando automáticamente Google TTS o Edge-TTS."""
    profile = VOICE_PROFILES.get(voice, VOICE_PROFILES[DEFAULT_VOICE])
    provider = profile.get('provider', 'google')
    effective_rate = rate if rate is not None else profile.get('rate', 1.05)

    if provider == 'google':
        try:
            lang = profile.get('lang', 'es-US')
            gender = profile.get('gender', 'MALE')
            effective_pitch = float(pitch) if pitch is not None else float(profile.get('pitch', 0.0))
            return _generate_google_tts(
                text=text,
                output=output,
                voice_name=voice,
                lang_code=lang,
                gender=gender,
                rate=effective_rate,
                pitch=effective_pitch,
                trailing_pause=trailing_pause,
            )
        except Exception as err:
            print(f"[VOICEOVER] Error con Google Cloud TTS ({err}), usando Edge-TTS de respaldo...")
            return asyncio.run(_generate_edge_tts(
                text=text,
                output=output,
                voice='es-MX-JorgeNeural',
                rate=effective_rate,
                base_pitch='+2Hz',
                trailing_pause=trailing_pause,
            ))
    else:
        effective_pitch = str(pitch) if pitch is not None else str(profile.get('pitch', '+0Hz'))
        return asyncio.run(_generate_edge_tts(
            text=text,
            output=output,
            voice=voice,
            rate=effective_rate,
            base_pitch=effective_pitch,
            trailing_pause=trailing_pause,
        ))


def generate_voiceover(
    text: str,
    output: str,
    voice: str = DEFAULT_VOICE,
    rate: float | None = None,
    pitch: str | float | None = None,
) -> str:
    clean = sanitize_narration(text)
    return _generate_one(clean, output, voice=voice, rate=rate, pitch=pitch)


def generate_voiceover_scenes(
    scene_texts: dict[int, str],
    output_dir: str,
    voice: str | None = None,
    rate: float | None = None,
) -> dict[int, dict]:
    """Genera una locución de alta calidad por cada escena."""
    selected_voice = voice if (voice and voice in VOICE_PROFILES) else DEFAULT_VOICE
    profile = VOICE_PROFILES[selected_voice]
    effective_rate = rate if rate is not None else profile.get('rate', 1.05)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    soft_used = [0]
    results = {}
    first = True

    for scene_num in sorted(scene_texts):
        text = scene_texts[scene_num]
        if not text.strip():
            continue
        clean = sanitize_narration(text, soft_used, force_clean=first)
        first = False
        audio_path = str(out_dir / f'scene_{scene_num:02d}.wav')
        if not (Path(audio_path).exists() and Path(audio_path).stat().st_size > 1000):
            _generate_one(clean, audio_path, voice=selected_voice, rate=effective_rate)
        results[scene_num] = {'text': clean, 'audio': audio_path}

    return results
