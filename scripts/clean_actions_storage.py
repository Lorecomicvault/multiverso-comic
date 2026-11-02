"""
Script para eliminar todos los artefactos de GitHub Actions en Lorecomicvault/multiverso-comic
para liberar espacio de almacenamiento.
"""

import sys
import requests

import os
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = "Lorecomicvault/multiverso-comic"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "Lorecomicvault-Storage-Cleaner"
}

def get_artifacts():
    url = f"https://api.github.com/repos/{REPO}/actions/artifacts?per_page=100"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Error al obtener artefactos: {resp.status_code} - {resp.text}")
        return []
    return resp.json().get("artifacts", [])

def delete_artifact(art_id):
    url = f"https://api.github.com/repos/{REPO}/actions/artifacts/{art_id}"
    resp = requests.delete(url, headers=headers)
    return resp.status_code == 204

def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(f"Consultando artefactos en {REPO}...")
    artifacts = get_artifacts()
    total = len(artifacts)
    total_bytes = sum(a.get("size_in_bytes", 0) for a in artifacts)
    print(f"Total artefactos encontrados: {total}")
    print(f"Espacio total a liberar: {total_bytes / (1024*1024):.2f} MB ({total_bytes / (1024*1024*1024):.3f} GB)\n")

    if total == 0:
        print("No hay artefactos pendientes por eliminar.")
        return

    deleted = 0
    freed = 0
    for a in artifacts:
        aid = a["id"]
        name = a["name"]
        size_mb = a["size_in_bytes"] / (1024 * 1024)
        print(f"Eliminando ID {aid} ({name}, {size_mb:.2f} MB)... ", end="", flush=True)
        if delete_artifact(aid):
            print("OK")
            deleted += 1
            freed += a["size_in_bytes"]
        else:
            print("FALLÓ")

    print("\n" + "="*50)
    print(f"Resumen de limpieza:")
    print(f"Artefactos eliminados: {deleted}/{total}")
    print(f"Espacio liberado: {freed / (1024*1024):.2f} MB")
    print("="*50)

if __name__ == "__main__":
    main()
