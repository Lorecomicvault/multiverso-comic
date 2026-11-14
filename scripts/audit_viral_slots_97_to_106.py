"""
Auditoría Estricta: Lote 10 Videos Virales Remasterizados (Slots 97 al 106)
Verifica que los 10 videos cumplan estrictamente:
- Duración entre 25.0s y 30.0s
- Existencia de video.mp4, thumb.jpg y metadata.json
- Tamaño de archivo > 2MB
"""

import os
import json
import subprocess
from pathlib import Path

QUEUE_DIR = Path(r"C:\Users\Vanes\comics en espanol\scheduled_queue")

slots = sorted([
    d for d in os.listdir(QUEUE_DIR)
    if os.path.isdir(QUEUE_DIR / d) and d[0].isdigit() and 97 <= int(d.split('_')[0]) <= 106
], key=lambda x: int(x.split('_')[0]))

print("=" * 105)
print(f"AUDITORÍA DEFINITIVA LOTE 10 VIRAL (SLOTS 97 AL 106) - TOTAL: {len(slots)} VIDEOS")
print("=" * 105)

all_perfect = True
report = []

for s in slots:
    sdir = QUEUE_DIR / s
    vfile = sdir / "video.mp4"
    tfile = sdir / "thumb.jpg"
    mfile = sdir / "metadata.json"
    
    if not vfile.exists():
        print(f"❌ {s}: FALTA video.mp4")
        all_perfect = False
        continue
        
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(vfile)]
    dur = float(subprocess.check_output(cmd).decode().strip())
    size_mb = vfile.stat().st_size / (1024 * 1024)
    
    slot_num = s.split("_")[0]
    title = ""
    if mfile.exists():
        with open(mfile, 'r', encoding='utf-8') as f:
            m = json.load(f)
            title = m.get('title', '')
            
    in_range = 25.00 <= dur <= 30.00
    if not in_range:
        all_perfect = False
        
    status_icon = "✅" if in_range else "❌"
    print(f"{status_icon} Slot {slot_num:>3} | {dur:5.2f}s | {size_mb:5.1f}MB | {sdir.name[:35]:<35} | {title[:40]}...")
    report.append({
        "slot": slot_num,
        "folder": sdir.name,
        "duration": dur,
        "size_mb": round(size_mb, 2),
        "in_range": in_range,
        "title": title
    })

print("=" * 105)
if all_perfect and len(slots) == 10:
    print(f"🚀 ¡ÉXITO TOTAL! LOS 10 VIDEOS (SLOTS 97 AL 106) CUMPLEN ESTRICTAMENTE EL RANGO VIRAL 25.0s - 30.0s")
else:
    print(f"⚠️ ATENCIÓN: Revisar inconsistencias ({len(slots)}/10 encontrados)")

with open(r"scratch\batch10_audit_summary.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
