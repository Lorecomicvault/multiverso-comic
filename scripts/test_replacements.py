import json
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('published_ledger.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

test_replacements = [
    ("Red Hulk Golpea al Watcher y a Thor en el Espacio", ["red hulk", "hulk rojo", "watcher", "uatu"]),
    ("Barry Allen Rayo Crisis Tierras Infinitas", ["canon de antimateria", "antimateria barry", "se convirtio en el rayo"]),
    ("Moon Knight Arranca la Cara a Bushman", ["bushman", "cara a bushman", "arranco la cara"]),
    ("Bane Rompe los Brazos a Killer Croc", ["killer croc", "rompe brazos croc"])
]

for name, keywords in test_replacements:
    matched = []
    for item in ledger:
        haystack = f"{item.get('id', '')} {item.get('title', '')} {item.get('description', '')}".lower()
        if any(kw in haystack for kw in keywords):
            matched.append((item.get('id'), item.get('title')))
    if matched:
        print(f"[COINCIDENCIA] {name} -> {matched}")
    else:
        print(f"[100% INEDITO] {name}")
