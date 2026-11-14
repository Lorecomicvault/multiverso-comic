import os
import json
import subprocess
from pathlib import Path

queue_dir = Path(r"C:\Users\Vanes\comics en espanol\scheduled_queue")
slots = sorted([
    d for d in os.listdir(queue_dir)
    if os.path.isdir(queue_dir / d) and d[0].isdigit() and int(d.split('_')[0]) >= 69
], key=lambda x: int(x.split('_')[0]))

all_perfect = True
report = []

print("=" * 95)
print(f"AUDITORÍA DEFINITIVA FORMATO VIRAL 25-30s (SLOTS 69 AL 86) - TOTAL: {len(slots)} VIDEOS")
print("=" * 95)

for s in slots:
    sdir = queue_dir / s
    vfile = sdir / "video.mp4"
    tfile = sdir / "thumb.jpg"
    mfile = sdir / "metadata.json"
    
    if not vfile.exists():
        print(f"❌ {s}: FALTA video.mp4")
        all_perfect = False
        continue
    
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(vfile)]
    dur = float(subprocess.check_output(cmd).decode().strip())
    
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
    print(f"{status_icon} Slot {slot_num:>2} ({sdir.name[:35]:<35}): {dur:5.2f}s | {title[:45]}...")
    report.append((slot_num, sdir.name, dur, in_range, title))

print("=" * 95)
if all_perfect:
    print(f"🚀 ¡ÉXITO ROTUNDO! LOS {len(slots)} VIDEOS CUMPLEN ESTRICTAMENTE EL FORMATO VIRAL 25.0s - 30.0s")
else:
    print("⚠️ ALGUNOS VIDEOS ESTÁN FUERA DEL RANGO!")
