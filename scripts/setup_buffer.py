"""
Setup and Verification Script for Buffer (TikTok & YouTube Shorts Integration)
Usage: python scripts/setup_buffer.py
"""

import sys
import os
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.buffer_publisher import get_buffer_channels


def main():
    print("=" * 65)
    print("   Comic Lore Vault - Buffer Multi-Platform Setup (TikTok & YouTube)")
    print("=" * 65)

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
        print("Asegúrate de haber conectado tus canales en https://buffer.com/channels")
        sys.exit(1)

    print(f"\nCanales encontrados ({len(channels)}):")
    tiktok_ch = None
    youtube_ch = None
    for ch in channels:
        svc = ch.get("service", "unknown")
        name = ch.get("displayName") or ch.get("name")
        cid = ch.get("id")
        print(f" - [{svc.upper()}] {name} (ID: {cid})")
        if svc.lower() == "tiktok":
            tiktok_ch = ch
        elif svc.lower() == "youtube":
            youtube_ch = ch

    print("\n" + "=" * 65)
    print("RESULTADO DE DETECCIÓN:")
    if tiktok_ch:
        print(f" ✅ Canal TikTok: {tiktok_ch.get('displayName') or tiktok_ch.get('name')} (ID: {tiktok_ch['id']})")
    else:
        print(" ⚠️ TikTok: No conectado en Buffer (puedes conectarlo en buffer.com/channels)")

    if youtube_ch:
        print(f" ✅ Canal YouTube: {youtube_ch.get('displayName') or youtube_ch.get('name')} (ID: {youtube_ch['id']})")
    else:
        print(" ⚠️ YouTube: No conectado en Buffer (conéctalo en buffer.com/channels)")
    print("=" * 65)

    print("\nConfiguración para tu archivo .env y GitHub Secrets:")
    print(f"BUFFER_ACCESS_TOKEN={token}")
    if tiktok_ch:
        print(f"BUFFER_TIKTOK_CHANNEL_ID={tiktok_ch['id']}")
    if youtube_ch:
        print(f"BUFFER_YOUTUBE_CHANNEL_ID={youtube_ch['id']}")


if __name__ == "__main__":
    main()
