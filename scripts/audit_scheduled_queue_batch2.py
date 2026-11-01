import sys
import json
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))

from src.composer import get_duration

QUEUE_DIR = PROJECT_ROOT / "scheduled_queue"

slots = [
    "11_red_hulk_golpea_watcher_humilla_thor",
    "12_wolverine_decapito_red_skull_escudo_capitan",
    "13_hal_jordan_masacre_green_lantern_corps_parallax",
    "14_spiderman_noquea_firelord_heraldo_galactus",
    "15_daredevil_nuevo_rey_del_crimen_hells_kitchen",
    "16_joker_mascara_cara_rebanada_death_of_family",
    "17_punisher_masacre_funeral_familia_mafia",
    "18_superman_vuela_seis_soles_noquea_world_forger",
    "19_thor_muerte_serpiente_midgard_nueve_pasos",
    "20_flash_barry_allen_se_convierte_en_rayo_crisis"
]

all_ok = True
print("================ MASTER AUDIT: SCHEDULED QUEUE SLOTS 11 AL 20 ================\n")

for s in slots:
    s_dir = QUEUE_DIR / s
    if not s_dir.exists():
        print(f"❌ Missing directory: {s}")
        all_ok = False
        continue

    v_file = s_dir / "video.mp4"
    t_file = s_dir / "thumb.jpg"
    m_file = s_dir / "metadata.json"

    if not v_file.exists() or v_file.stat().st_size < 1000000:
        print(f"❌ {s}: Invalid or missing video.mp4")
        all_ok = False
        continue

    if not t_file.exists() or t_file.stat().st_size < 5000:
        print(f"❌ {s}: Invalid or missing thumb.jpg")
        all_ok = False
        continue

    if not m_file.exists():
        print(f"❌ {s}: Missing metadata.json")
        all_ok = False
        continue

    dur = get_duration(str(v_file))
    meta = json.loads(m_file.read_text(encoding='utf-8'))
    title = meta.get("title", "")
    v_size_mb = v_file.stat().st_size / (1024 * 1024)

    dur_ok = "✅" if dur >= 60.0 else "⚠️ (<60s)"
    if dur < 60.0:
        all_ok = False

    print(f"{dur_ok} {s[:25]}... | {dur:.2f}s | {v_size_mb:.1f}MB | {title}")

print("\n" + "="*80)
if all_ok:
    print("🎯 TODOS LOS 10 VIDEOS CUMPLEN ESTRICTAMENTE DURATION >= 60.0s Y ESTÁN 100% LISTOS!")
else:
    print("❌ AL MENOS UN VIDEO NO CUMPLE CON LOS REQUISITOS.")
