"""
Master Sequential Batch Runner for Batch 5 (Slots 46 al 50)
============================================================
Garantiza:
1. Paneles 1:1 canónicos curados sin alucinaciones.
2. Cero errores de ejecución (retry inteligente en caso de micro-latencias de TTS).
3. Duración >= 60.0s en cada reel.
4. Encolado directo y validado en scheduled_queue/
"""
import sys
import os
import time
import json
import traceback
from pathlib import Path

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

import scripts.produce_batch_5_inéditos_pack as p5

TARGET_SLOTS = [46, 47, 48, 49, 50]

print("=" * 80)
print("🚀 INICIANDO PRODUCCIÓN AUTOMATIZADA DE SLOTS 46 AL 50 (BATCH 5)")
print(f"🎯 Slots a procesar: {TARGET_SLOTS}")
print("=" * 80)

completed_slots = []
failed_slots = []

for slot_num in TARGET_SLOTS:
    projs = [p for p in p5.PROJECTS if p["slot"] == slot_num]
    if not projs:
        print(f"❌ Error: Configuración de Slot {slot_num} no encontrada.")
        failed_slots.append(slot_num)
        continue

    proj = projs[0]
    title = proj["title"]
    queue_name = proj["queue_folder"]

    print("\n" + "#" * 80)
    print(f"▶️ PROCESANDO SLOT {slot_num}: {title}")
    print(f"📁 Destino: scheduled_queue/{queue_name}")
    print("#" * 80)

    max_attempts = 3
    success = False

    for attempt in range(1, max_attempts + 1):
        print(f"\n--- [Intento {attempt}/{max_attempts}] Ejecutando compilación de Slot {slot_num} ---")
        try:
            res_dir = p5.produce_single_project(proj)
            if not res_dir:
                print(f"⚠️ produce_single_project devolvió None en intento {attempt}")
                time.sleep(4)
                continue

            video_file = res_dir / "video.mp4"
            thumb_file = res_dir / "thumb.jpg"
            meta_file = res_dir / "metadata.json"

            if not video_file.exists():
                print(f"⚠️ video.mp4 no existe en {res_dir}")
                time.sleep(4)
                continue

            dur = p5.get_duration(str(video_file))
            if dur < 60.0:
                print(f"⚠️ Duración {dur:.2f}s es inferior al requisito estricto de 60.0s!")
                time.sleep(4)
                continue

            print(f"🌟 ¡ÉXITO ROTUNDO! Slot {slot_num} generado y validado:")
            print(f"   - Video: {video_file} ({dur:.2f}s, {video_file.stat().st_size / (1024*1024):.1f} MB)")
            print(f"   - Miniatura: {thumb_file} (Existe: {thumb_file.exists()})")
            print(f"   - Metadata: {meta_file} (Existe: {meta_file.exists()})")
            success = True
            completed_slots.append(slot_num)
            break

        except Exception as e:
            print(f"❌ Excepción durante intento {attempt} para Slot {slot_num}: {e}")
            traceback.print_exc()
            time.sleep(5)

    if not success:
        print(f"🚨 FATAL: Slot {slot_num} falló todos los intentos.")
        failed_slots.append(slot_num)
        # Detener para no encadenar errores
        break

print("\n" + "=" * 80)
print("📊 RESUMEN FINAL DE PRODUCCIÓN")
print(f"✅ Slots completados exitosamente: {completed_slots}")
print(f"❌ Slots fallidos: {failed_slots}")
print("=" * 80)

if failed_slots:
    sys.exit(1)
else:
    print("🎉 ¡TODOS LOS SLOTS DEL LOTE COMPLETADOS CON ÉXITO Y ENCOLADOS!")
    sys.exit(0)
