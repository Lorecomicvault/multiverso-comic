import json
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('published_ledger.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

test_candidates = [
    ("Superman Vuela Seis Soles World Forger", ["world forger", "forjador", "seis soles"]),
    ("Carnage Mind Bomb Psiquiatra", ["mind bomb", "psiquiatra", "kurtz", "kasady"]),
    ("Ghost Rider Posee Celestial Gigante", ["robbie reyes", "celestial gigante", "poseyo celestial"]),
    ("Aquaman Geoff Johns Nadie se Burla", ["habla con los peces", "rey de los mares", "aquaman geoff johns"]),
    ("Thor vs Serpiente de Midgard Muerte 9 Pasos", ["jormungandr", "serpiente de midgard", "nueve pasos", "simonson"]),
    ("Batman Zur-En-Arrh Respaldo", ["zur-en-arrh"]),
    ("Venom Arranca las Alas de Knull", ["alas de knull", "dios de la luz", "fuerza enigma"])
]

for name, keywords in test_candidates:
    matches = []
    for item in ledger:
        text = (item.get('id', '') + " " + item.get('title', '') + " " + item.get('description', '')).lower()
        matched_kw = [kw for kw in keywords if kw in text]
        if matched_kw:
            matches.append((item.get('id'), item.get('title'), matched_kw))
    if matches:
        print(f"⚠️ {name} -> COINCIDENCIA: {matches[0][0]} ({matches[0][2]})")
    else:
        print(f"✅ {name} -> 100% INÉDITO")
