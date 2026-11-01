import json
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('published_ledger.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

print(f"Auditando candidatos contra {len(ledger)} entradas del ledger...\n")

candidates = [
    ("Magneto Submarino Leningrado", ["leningrado", "submarino", "uncanny 150"]),
    ("Sentry Parte a Carnage en el Espacio", ["sentry", "carnage", "espacio"]),
    ("Batman Silla de Mobius / 3 Jokers", ["mobius", "dios del conocimiento", "tres jokers", "three jokers"]),
    ("Wolverine Decapita a Red Skull Escudo", ["decapita", "red skull", "craneo rojo", "old man logan"]),
    ("Hal Jordan Masacre Green Lanterns Emerald Twilight", ["emerald twilight", "crepusculo esmeralda", "kilowog"]),
    ("Doctor Doom Arranca Columna a Thanos", ["columna", "thanos", "secret wars"]),
    ("Spider-Man Noquea a Firelord Heraldo Galactus", ["firelord", "heraldo"]),
    ("Daredevil se Proclama Rey de la Mafia Bendis", ["rey del crimen", "nuevo kingpin", "proclamo"]),
    ("Joker se Rebana su Propia Cara Death of the Family", ["rebano", "dollmaker", "death of the family", "cara"]),
    ("Punisher Mata a Toda la Mafia en un Funeral (Welcome Back Frank)", ["funeral", "mafia", "ataud"])
]

for name, keywords in candidates:
    print(f"--- Verificando: {name} ---")
    matches = []
    for item in ledger:
        text = (item.get('id', '') + " " + item.get('title', '') + " " + item.get('description', '')).lower()
        matched_kw = [kw for kw in keywords if kw in text]
        if len(matched_kw) >= 2 or (len(keywords) == 1 and len(matched_kw) == 1):
            matches.append((item.get('id'), item.get('title'), matched_kw))
    
    if matches:
        print(f"  ⚠️ POSIBLE COINCIDENCIA ({len(matches)}):")
        for m in matches[:3]:
            print(f"     - [{m[0]}] {m[1]} (keywords: {m[2]})")
    else:
        print("  ✅ 100% INÉDITO (0 coincidencias en 305 videos)")
