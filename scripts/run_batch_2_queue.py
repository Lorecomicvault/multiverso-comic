import sys
import time
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.produce_batch_2_inéditos_pack import PROJECTS, produce_single_project

print("======================================================================")
print("🚀 INICIANDO PRODUCCIÓN AUTOMATIZADA: SLOTS 12 AL 20 (9 VIDEOS DE 60s+)")
print("======================================================================\n")

results = []

for idx in range(1, len(PROJECTS)):
    proj = PROJECTS[idx]
    slot = proj["slot"]
    title = proj["title"]
    print(f"\n[{idx+1}/10] >>> PROCESANDO SLOT {slot}: {title} <<<")
    start_t = time.time()
    try:
        dest_dir = produce_single_project(proj)
        elapsed = time.time() - start_t
        if dest_dir:
            print(f"[{idx+1}/10] ✅ SLOT {slot} COMPLETADO EN {elapsed:.1f}s -> {dest_dir.name}")
            results.append((slot, title, "SUCCESS", elapsed))
        else:
            print(f"[{idx+1}/10] ❌ ERROR EN SLOT {slot}")
            results.append((slot, title, "FAILED", elapsed))
    except Exception as e:
        elapsed = time.time() - start_t
        print(f"[{idx+1}/10] ❌ EXCEPCIÓN EN SLOT {slot}: {e}")
        import traceback
        traceback.print_exc()
        results.append((slot, title, f"ERROR: {e}", elapsed))

print("\n" + "="*70)
print("🏁 RESUMEN FINAL DE PRODUCCIÓN SLOTS 12 AL 20:")
print("="*70)
for slot, title, status, elapsed in results:
    print(f"Slot {slot:02d}: [{status}] ({elapsed:.1f}s) - {title}")
