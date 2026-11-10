import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.produce_remastered_batch_7 import REMASTER_PROJECTS_BATCH_7, produce_project

def main():
    target_slots = range(68, 77)
    success = []
    failed = []

    print("=" * 80)
    print("🚀 INICIANDO PRODUCCIÓN AUTOMATIZADA DE SLOTS 68 AL 76")
    print("=" * 80)

    for proj in REMASTER_PROJECTS_BATCH_7:
        slot = proj["slot"]
        if slot not in target_slots:
            continue
        try:
            v = produce_project(proj)
            if v and v.exists():
                success.append(slot)
                print(f"🎉 Slot {slot} completado con éxito!")
            else:
                failed.append(slot)
                print(f"❌ Slot {slot} falló")
        except Exception as e:
            failed.append(slot)
            print(f"💥 Excepción en slot {slot}: {e}")

    print("\n" + "=" * 80)
    print(f"🏁 RESUMEN: {len(success)} exitosos ({success}), {len(failed)} fallidos ({failed})")
    print("=" * 80)

if __name__ == "__main__":
    main()
