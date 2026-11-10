import json
import subprocess
from pathlib import Path
import sys

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.composer import get_duration

brain = Path(r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb")
queue_base = PROJECT_ROOT / "scheduled_queue"

slots = range(77, 87)
print("=" * 80)
print("AUDITORÍA DE LOS 10 VIDEOS DEL LOTE 8 (SLOTS 77 AL 86)")
print("=" * 80)

results = []

for s in slots:
    folder = list(queue_base.glob(f"{s}_*"))[0]
    video = folder / "video.mp4"
    thumb = folder / "thumb.jpg"
    meta = folder / "metadata.json"
    
    with open(meta, "r", encoding="utf-8") as f:
        meta_data = json.load(f)
        
    dur = get_duration(str(video))
    v_size = video.stat().st_size / (1024 * 1024)
    t_size = thumb.stat().st_size / 1024
    
    title = meta_data.get("title")
    print(f"Slot {s}: {folder.name}")
    print(f"  Título: {title}")
    print(f"  Duración: {dur:.2f}s | Tamaño: {v_size:.1f} MB | Thumb: {t_size:.1f} KB")
    
    for t in [15, 45]:
        out_img = brain / f"audit_sample_slot_{s}_at_{t}s.jpg"
        subprocess.run([
            "ffmpeg", "-y",
            "-ss", f"00:00:{t:02d}.000",
            "-i", str(video),
            "-vframes", "1",
            "-q:v", "2",
            str(out_img)
        ], capture_output=True)
    
    results.append({
        "slot": s,
        "folder": folder.name,
        "title": title,
        "duration": dur,
        "size_mb": v_size,
        "valid_duration": dur >= 60.0
    })

print("\n" + "=" * 80)
print("RESUMEN DE CUMPLIMIENTO:")
all_valid = all(r["valid_duration"] for r in results)
print(f"Todos >= 60.0s: {all_valid}")
for r in results:
    status = "✅ OK" if r["valid_duration"] else "❌ ERROR"
    slot_num = r["slot"]
    slot_dur = r["duration"]
    print(f"  Slot {slot_num}: {slot_dur:.2f}s -> {status}")
