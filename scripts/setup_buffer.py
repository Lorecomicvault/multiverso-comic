"""
Setup and Verification Script for Buffer (TikTok Integration)
Usage: python scripts/setup_buffer.py
"""

import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.buffer_publisher import get_buffer_channels


def main():
    print("=" * 60)
    print("   Comic Lore Vault - Buffer / TikTok Setup & Verification")
    print("=" * 60)

    token = os.environ.get("BUFFER_ACCESS_TOKEN")
    if not token:
        token = input("Por favor, pega tu Buffer Access Token: ").strip()

    if not token:
        print("Error: No se proporcionó ningún token.")
        sys.exit(1)

    print("\nConsultando canales conectados en Buffer...")
    channels = get_buffer_channels(token)

    if not channels:
        print("\n[!] No se encontraron canales o el token es inválido.")
        print("Asegúrate de haber conectado tu cuenta de TikTok en https://buffer.com")
        sys.exit(1)

    print(f"\nCanales encontrados ({len(channels)}):")
    tiktok_ch = None
    for ch in channels:
        svc = ch.get("service", "unknown")
        name = ch.get("displayName") or ch.get("name")
        cid = ch.get("id")
        print(f" - [{svc.upper()}] {name} (ID: {cid})")
        if svc.lower() == "tiktok":
            tiktok_ch = ch

    if tiktok_ch:
        print("\n" + "=" * 60)
        print("¡CANAL DE TIKTOK DETECTADO CON ÉXITO!")
        print(f"Nombre: {tiktok_ch.get('displayName') or tiktok_ch.get('name')}")
        print(f"Channel ID: {tiktok_ch['id']}")
        print("=" * 60)
        print("\nGuarda estas dos variables en tu archivo .env y en GitHub Secrets:")
        print(f"BUFFER_ACCESS_TOKEN={token}")
        print(f"BUFFER_TIKTOK_CHANNEL_ID={tiktok_ch['id']}")
    else:
        print("\n[!] Tu cuenta de Buffer funciona, pero aún no has conectado TikTok.")
        print("1. Ve a https://buffer.com/channels")
        print("2. Haz clic en 'Connect Channel' y elige TikTok.")
        print("3. Vuelve a ejecutar este script.")


if __name__ == "__main__":
    main()
