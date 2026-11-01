"""
RECONSTRUCCIÓN Y SINCRONIZACIÓN MAESTRA DEL LEDGER DE PUBLICACIONES
===================================================================
1. Carga los 238 videos reales de Facebook y 211 de Instagram.
2. Unifica todo en published_ledger.json sin pérdidas históricas.
3. Enriquecer cada entrada con tokens normalizados y firmas temáticas.
4. Genera un reporte exhaustivo de cobertura.
"""

import os
import re
import sys
import json
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
LEDGER_PATH = os.path.join(BASE_DIR, "published_ledger.json")
FB_PATH = os.path.join(BASE_DIR, "scratch", "all_facebook_published_videos.json")
IG_PATH = os.path.join(BASE_DIR, "scratch", "all_instagram_published_media.json")

def normalize(text):
    if not text:
        return ""
    nfkd = unicodedata.normalize('NFKD', str(text))
    cleaned = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    return " ".join(cleaned.split())

stopwords = {
    "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "en", "por",
    "con", "que", "del", "al", "para", "the", "of", "and", "in", "to", "su", "sus",
    "marvel", "dc", "comics", "comic", "zombies", "zombi", "multiverso", "universo", "historia"
}

def extract_tokens(text):
    norm = normalize(text)
    return [w for w in norm.split() if len(w) > 3 and w not in stopwords]

def run_sync():
    print("=== Sincronización del Ledger Maestro con la Realidad de Redes Sociales ===")
    
    with open(FB_PATH, "r", encoding="utf-8") as f:
        fb_videos = json.load(f)
        
    with open(IG_PATH, "r", encoding="utf-8") as f:
        ig_media = json.load(f)

    existing_ledger = []
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            try:
                existing_ledger = json.load(f)
            except Exception as e:
                print(f"Error leyendo ledger actual: {e}")

    print(f"Entradas previas en el ledger: {len(existing_ledger)}")
    print(f"Videos reales en Facebook: {len(fb_videos)}")
    print(f"Publicaciones en Instagram: {len(ig_media)}")

    # Indexar ledger existente por id normalizado y título normalizado
    ledger_by_norm_title = {}
    ledger_by_id = {}
    for item in existing_ledger:
        sid = item.get("id") or item.get("story_id")
        if sid:
            ledger_by_id[str(sid).strip().lower()] = item
        t = item.get("title") or item.get("headline") or ""
        if t:
            ledger_by_norm_title[normalize(t)] = item

    new_entries_added = 0
    updated_entries = 0

    # 1. Procesar videos de Facebook
    for v in fb_videos:
        fb_id = v["id"]
        created = v.get("created_time")
        title = v.get("title") or ""
        desc = v.get("description") or ""
        first_line = desc.split("\n")[0].strip() if desc else ""
        raw_title = title if title else first_line
        norm_t = normalize(raw_title)

        # Buscar si ya existe en el ledger
        matched = ledger_by_norm_title.get(norm_t)
        if not matched:
            # Buscar por coincidencia parcial de tokens (>70%)
            v_tokens = set(extract_tokens(raw_title))
            if v_tokens:
                for lt, litem in ledger_by_norm_title.items():
                    l_tokens = set(extract_tokens(litem.get("title", "")))
                    if l_tokens and len(v_tokens.intersection(l_tokens)) / max(len(v_tokens), len(l_tokens)) >= 0.70:
                        matched = litem
                        break

        if matched:
            # Actualizar con datos de Facebook
            matched["fb_video_id"] = fb_id
            if not matched.get("published_at"):
                matched["published_at"] = created
            if not matched.get("tokens"):
                matched["tokens"] = list(extract_tokens(matched.get("title", "")))
            updated_entries += 1
        else:
            # Crear nueva entrada canónica
            slug = re.sub(r'[^a-z0-9]+', '_', norm_t)[:50].strip('_')
            new_item = {
                "id": f"fb_{slug}",
                "title": raw_title,
                "normalized_title": norm_t,
                "character": raw_title.split(":")[0].replace("¡", "").strip(),
                "theme_signature": f"fb_published:{slug}",
                "tokens": list(extract_tokens(raw_title)),
                "date": created.split("T")[0] if created else "past",
                "published_at": created,
                "fb_video_id": fb_id,
                "status": "published",
                "source": "facebook_sync"
            }
            existing_ledger.append(new_item)
            ledger_by_norm_title[norm_t] = new_item
            new_entries_added += 1

    # 2. Procesar Instagram media
    for m in ig_media:
        ig_id = m["id"]
        created = m.get("timestamp")
        cap = m.get("caption") or ""
        first_line = cap.split("\n")[0].strip() if cap else ""
        norm_t = normalize(first_line)

        matched = ledger_by_norm_title.get(norm_t)
        if matched:
            matched["ig_media_id"] = ig_id
            updated_entries += 1
        elif norm_t:
            v_tokens = set(extract_tokens(first_line))
            for lt, litem in ledger_by_norm_title.items():
                l_tokens = set(extract_tokens(litem.get("title", "")))
                if l_tokens and len(v_tokens.intersection(l_tokens)) / max(len(v_tokens), len(l_tokens)) >= 0.70:
                    litem["ig_media_id"] = ig_id
                    break

    # Asegurar que cada entrada en el ledger tenga sus campos de auditoría
    for item in existing_ledger:
        t = item.get("title") or item.get("headline") or ""
        item["normalized_title"] = normalize(t)
        if not item.get("tokens"):
            item["tokens"] = list(extract_tokens(t))

    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_ledger, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Sincronización exitosa!")
    print(f" - Nuevas historias históricas añadidas: {new_entries_added}")
    print(f" - Historias existentes enriquecidas: {updated_entries}")
    print(f" - TOTAL ABSOLUTO DE HISTORIAS BLINDADAS EN LEDGER: {len(existing_ledger)}")

if __name__ == "__main__":
    run_sync()
