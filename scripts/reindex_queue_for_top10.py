"""
Script de Reindexación de la Cola Programada
Mueve los 17 videos existentes (Slots 70-86) a los Slots 80-96
para dar cabida al Top 10 viral que se publicará primero a partir de mañana.
"""

import os
import json
import re
from pathlib import Path

QUEUE_DIR = Path("scheduled_queue")

def reindex_queue():
    folders = sorted(
        [d for d in QUEUE_DIR.iterdir() if d.is_dir() and re.match(r"^\d+_", d.name)],
        key=lambda x: int(x.name.split("_")[0]),
        reverse=True
    )
    
    print(f"Reindexando {len(folders)} carpetas de mayor a menor...")
    for folder in folders:
        old_slot = int(folder.name.split("_")[0])
        rest = "_".join(folder.name.split("_")[1:])
        new_slot = old_slot + 10
        new_name = f"{new_slot}_{rest}"
        new_path = QUEUE_DIR / new_name
        
        # 1. Renombrar carpeta
        folder.rename(new_path)
        print(f"  Renombrado: {folder.name} -> {new_name}")
        
        # 2. Actualizar metadata.json si existe
        meta_file = new_path / "metadata.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                meta["slot"] = new_slot
                meta["queue_folder"] = new_name
                with open(meta_file, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)
                print(f"    metadata.json actualizado con slot {new_slot}")
            except Exception as e:
                print(f"    Error actualizando metadata.json en {new_name}: {e}")

if __name__ == "__main__":
    reindex_queue()
    print("Reindexación completada con éxito.")
