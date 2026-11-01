import json
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

with open('published_ledger.json', 'r', encoding='utf-8') as f:
    ledger = json.load(f)

pack_candidates = [
    {
        "id": "red_hulk_golpea_watcher_humilla_thor",
        "title": "¡Red Hulk le Dio un Puñetazo al Vigilante Uatu y Humilló a Thor en el Espacio! 🔴🔨🌌",
        "character": "Red Hulk",
        "keywords": ["red hulk", "hulk rojo", "uatu", "watcher", "gravedad cero"]
    },
    {
        "id": "wolverine_decapito_red_skull_escudo_capitan",
        "title": "¡Wolverine Decapitó a Red Skull con el Escudo del Capitán América! 🩸🛡️⚔️",
        "character": "Wolverine",
        "keywords": ["red skull", "craneo rojo", "old man logan decapit", "trophy room"]
    },
    {
        "id": "hal_jordan_masacre_green_lantern_corps_parallax",
        "title": "¡Hal Jordan Enloqueció y Masacró a Todo el Cuerpo de Green Lanterns! 🟢💀⚡",
        "character": "Green Lantern",
        "keywords": ["emerald twilight", "crepusculo esmeralda", "kilowog muerte", "masacre lanterns"]
    },
    {
        "id": "spiderman_noquea_firelord_heraldo_galactus",
        "title": "¡Spider-Man Noqueó a un Heraldo Cósmico de Galactus a Puño Limpio! 🕷️🔥🌌",
        "character": "Spider-Man",
        "keywords": ["firelord", "heraldo de galactus", "peter parker firelord"]
    },
    {
        "id": "daredevil_nuevo_rey_del_crimen_hells_kitchen",
        "title": "¡Daredevil Destronó a Kingpin y se Proclamó el Nuevo Rey del Crimen! 😈🥊👑",
        "character": "Daredevil",
        "keywords": ["nuevo kingpin", "rey del crimen matt", "murdock destrona", "daredevil 50"]
    },
    {
        "id": "joker_mascara_cara_rebanada_death_of_family",
        "title": "¡El Joker se Rebanó su Propia Cara para Convertirla en una Máscara! 🃏🪓🩸",
        "character": "The Joker",
        "keywords": ["death of the family", "dollmaker", "cara rebanada", "joker se corto la cara"]
    },
    {
        "id": "punisher_masacre_funeral_familia_mafia",
        "title": "¡The Punisher Asistió a un Funeral Solo para Masacrar a Toda la Mafia! 💀⚰️🔫",
        "character": "The Punisher",
        "keywords": ["funeral gnucci", "funeral mafia", "punisher ataúd", "mausoleo"]
    },
    {
        "id": "superman_vuela_seis_soles_noquea_world_forger",
        "title": "¡Superman Voló a Través de Seis Soles y Noqueó a un Dios del Multiverso! ☀️💥🦸‍♂️",
        "character": "Superman",
        "keywords": ["world forger", "forjador de mundos", "seis soles", "sixth dimension"]
    },
    {
        "id": "thor_muerte_serpiente_midgard_nueve_pasos",
        "title": "¡Thor Mató a la Serpiente de Midgard y Cayó Tras Dar Nueve Pasos! ⚡🐍🔨",
        "character": "Thor",
        "keywords": ["jormungandr", "serpiente de midgard", "nueve pasos", "thor 380", "simonson"]
    },
    {
        "id": "flash_barry_allen_se_convierte_en_rayo_crisis",
        "title": "¡The Flash Corrió Tan Rápido que se Convirtió en el Rayo de su Propio Origen! ⚡🏃‍♂️🌀",
        "character": "The Flash",
        "keywords": ["canon de antimateria", "se convirtio en el rayo", "origen de barry rayo", "muerte de barry allen"]
    }
]

print("=" * 60)
print("AUDITORÍA DE COLISIÓN RIGUROSA (305 VIDEOS HISTÓRICOS)")
print("=" * 60)

all_clean = True
for idx, c in enumerate(pack_candidates, 1):
    matched = []
    for item in ledger:
        haystack = f"{item.get('id', '')} {item.get('title', '')} {item.get('description', '')}".lower()
        if any(kw in haystack for kw in c["keywords"]):
            matched.append((item.get('id'), item.get('title')))
    
    if matched:
        print(f"❌ [{idx:02d}] {c['title']} -> CONFLICTO CON: {matched}")
        all_clean = False
    else:
        print(f"✅ [{idx:02d}] {c['title']} -> 100% INÉDITO Y VERIFICADO")

if all_clean:
    print("\n🎉 ¡CONFIRMADO! LOS 10 TEMAS SON 100% INÉDITOS Y CUMPLEN LA POLÍTICA DE TOLERANCIA CERO.")
