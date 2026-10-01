"""
Limpieza de Artefactos Antiguos en GitHub Actions (Lorecomicvault/multiverso-comic)
Libera espacio de almacenamiento de Actions borrando videos y logs de pruebas antiguas.
"""

import json
import urllib.request
import subprocess

import os

TOKEN = os.environ.get("GITHUB_TOKEN") or subprocess.check_output(["gh", "auth", "token"], text=True).strip()
REPO = "Lorecomicvault/multiverso-comic"

def get_artifacts():
    url = f"https://api.github.com/repos/{REPO}/actions/artifacts?per_page=100"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Lorecomicvault-Cleaner"
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data.get('artifacts', [])

def delete_artifact(artifact_id, name):
    url = f"https://api.github.com/repos/{REPO}/actions/artifacts/{artifact_id}"
    req = urllib.request.Request(url, method="DELETE", headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Lorecomicvault-Cleaner"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 204:
                return True
    except Exception as e:
        print(f"Error borrando {artifact_id} ({name}): {e}")
        return False
    return False

def main():
    artifacts = get_artifacts()
    print(f"Artefactos totales encontrados: {len(artifacts)}")

    # Filtrar artefactos viejos (del 8 y 9 de septiembre)
    old_artifacts = [a for a in artifacts if a['created_at'].startswith('2026-09-08') or a['created_at'].startswith('2026-09-09')]
    print(f"Artefactos antiguos (Sep 8-9) a eliminar: {len(old_artifacts)}")

    freed_bytes = 0
    deleted_count = 0
    for a in old_artifacts:
        aid = a['id']
        name = a['name']
        size_mb = a['size_in_bytes'] / (1024 * 1024)
        print(f"Borrando artefacto {aid}: {name} ({size_mb:.2f} MB)...", end=" ")
        if delete_artifact(aid, name):
            print("OK")
            freed_bytes += a['size_in_bytes']
            deleted_count += 1
        else:
            print("FALLO")

    print("\n" + "=" * 60)
    print(f"Eliminados con exito: {deleted_count}/{len(old_artifacts)}")
    print(f"Espacio liberado: {freed_bytes / (1024 * 1024):.2f} MB ({freed_bytes / (1024 * 1024 * 1024):.3f} GB)")
    print("=" * 60)

if __name__ == '__main__':
    main()
