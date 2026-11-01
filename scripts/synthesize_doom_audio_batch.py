"""
SÍNTESIS POR LOTES DE AUDIO NEURONAL CON VOICEBOX
=================================================
- Perfil: Narrador Referencia Cómic (28078056-1a1d-43d4-9d57-d616275f13c2)
- Engine: Qwen-TTS neuronal
- Genera y descarga los audios para las 44 escenas del video de Doctor Doom
"""

import os
import sys
import json
import time
import requests

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "doctor_doom_doomsday_long")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2" # Narrador Referencia Cómic

# Importar las escenas del script de producción
sys.path.append(os.path.join(BASE_DIR, "scripts"))
from produce_doctor_doom_doomsday_long import SCENES

def run_audio_synthesis():
    print(f"=== Síntesis Neuronal con Voicebox: {len(SCENES)} escenas ===")
    total = len(SCENES)
    
    for s in SCENES:
        sid = s["id"]
        wav_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.wav")
        meta_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.json")
        
        if os.path.exists(wav_path) and os.path.exists(meta_path) and os.path.getsize(wav_path) > 10000:
            with open(meta_path, "r", encoding="utf-8") as f:
                d = json.load(f)
            print(f"[{sid:02d}/{total}] En caché: {d.get('duration', 0):.2f}s - {s['text'][:50]}...")
            continue
            
        print(f"[{sid:02d}/{total}] Generando ({len(s['text'])} chars): {s['text'][:60]}...")
        payload = {
            'profile_id': PROFILE_ID,
            'text': s['text'],
            'language': 'es',
            'engine': 'qwen',
            'max_chunk_chars': 1500,
            'crossfade_ms': 80,
            'normalize': True
        }
        
        try:
            r = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=60)
            if r.status_code != 200:
                print(f"   Error HTTP {r.status_code}: {r.text}")
                continue
            gen_id = r.json()['id']
            
            # Polling hasta completar
            for attempt in range(60):
                time.sleep(2)
                sr = requests.get(f"{VOICEBOX_URL}/history/{gen_id}")
                if sr.status_code == 200:
                    sdata = sr.json()
                    status = sdata.get('status')
                    if status == 'completed':
                        dur = float(sdata.get('duration', 5.0))
                        ar = requests.get(f"{VOICEBOX_URL}/audio/{gen_id}")
                        with open(wav_path, 'wb') as f:
                            f.write(ar.content)
                        with open(meta_path, 'w', encoding='utf-8') as f:
                            json.dump({"id": sid, "duration": dur, "text": s['text']}, f, indent=2)
                        print(f"   -> Escena {sid:02d} completada! Duración: {dur:.2f}s ({os.path.getsize(wav_path)//1024} KB)")
                        break
                    elif status == 'failed':
                        print(f"   -> Fallo en escena {sid:02d}: {sdata.get('error')}")
                        break
        except Exception as e:
            print(f"   Excepción en escena {sid:02d}: {e}")

if __name__ == "__main__":
    run_audio_synthesis()
