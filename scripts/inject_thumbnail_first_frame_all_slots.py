import os
import sys
import shutil
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

QUEUE_DIR = Path("scheduled_queue")
BRAIN_DIR = Path(r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb")

SLOTS = [
    49, 50, 51, 52, 53, 54, 55
]

def inject_thumbnail_into_video(slot_dir: Path, thumb_path: Path):
    video_path = slot_dir / "video.mp4"
    if not video_path.exists():
        print(f"  [ERROR] No existe video.mp4 en {slot_dir}")
        return False
    if not thumb_path.exists():
        print(f"  [ERROR] No existe thumb.jpg en {thumb_path}")
        return False

    temp_out = slot_dir / "video_with_thumb_frame0.mp4"

    # Inyección de 0.40 segundos de miniatura como primer frame exacto
    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-loop', '1', '-t', '0.40', '-i', str(thumb_path),
        '-filter_complex',
        '[1:v]fps=30,scale=1080:1920,setsar=1[vthumb];[0:v]trim=start=0.40,setpts=PTS-STARTPTS[vmain];[vthumb][vmain]concat=n=2:v=1:a=0[v]',
        '-map', '[v]',
        '-map', '0:a',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        '-c:a', 'copy',
        str(temp_out)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR FFMPEG]: {res.stderr[-300:]}")
        if temp_out.exists():
            temp_out.unlink()
        return False

    # Verificar que el video resultante es válido y tiene tamaño adecuado
    if temp_out.stat().st_size < 1000000:
        print(f"  [ERROR] Video resultante sospechosamente pequeño: {temp_out.stat().st_size} bytes")
        temp_out.unlink()
        return False

    # Extraer frame 0 para auditoría estricta
    audit_f0 = BRAIN_DIR / f"audit_frame0_{slot_dir.name}.jpg"
    sub_res = subprocess.run([
        'ffmpeg', '-y',
        '-ss', '00:00:00.000',
        '-i', str(temp_out),
        '-vframes', '1',
        '-q:v', '2',
        str(audit_f0)
    ], capture_output=True)

    if not audit_f0.exists() or audit_f0.stat().st_size < 10000:
        print(f"  [ERROR] Falló extracción de frame 0 de auditoría")
        temp_out.unlink()
        return False

    # Reemplazar video original
    shutil.move(temp_out, video_path)
    print(f"  [OK] Video actualizado exitosamente: {video_path.name} ({video_path.stat().st_size / (1024*1024):.2f} MB)")
    print(f"  [OK] Frame 0 verificado en brain: {audit_f0.name} ({audit_f0.stat().st_size / 1024:.1f} KB)")
    return True

def main():
    print("=====================================================================")
    print("INYECCIÓN DE MINIATURA IMPACTANTE COMO PRIMER FRAME (SLOTS 49 AL 55)")
    print("=====================================================================")

    success_count = 0
    for sid in SLOTS:
        matching = list(QUEUE_DIR.glob(f"{sid}_*"))
        if not matching:
            print(f"[SKIP] No se encontró carpeta para Slot {sid}")
            continue

        slot_dir = matching[0]
        thumb_file = slot_dir / "thumb.jpg"
        print(f"\nProcesando Slot {sid}: {slot_dir.name}...")

        ok = inject_thumbnail_into_video(slot_dir, thumb_file)
        if ok:
            success_count += 1

    print(f"\n=====================================================================")
    print(f"RESULTADO FINAL: {success_count} de {len(SLOTS)} videos actualizados con éxito")
    print("=====================================================================")

if __name__ == "__main__":
    main()
