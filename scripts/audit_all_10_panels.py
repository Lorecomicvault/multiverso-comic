import sys
from pathlib import Path
from PIL import Image
import numpy as np

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
PANELS_DIR = PROJECT_ROOT / "assets" / "curated_panels"

stories = [
    "01_red_hulk_golpea_watcher_humilla_thor",
    "02_wolverine_decapito_red_skull_escudo_capitan",
    "03_hal_jordan_masacre_green_lantern_corps_parallax",
    "04_spiderman_noquea_firelord_heraldo_galactus",
    "05_daredevil_nuevo_rey_del_crimen_hells_kitchen",
    "06_joker_mascara_cara_rebanada_death_of_family",
    "07_punisher_masacre_funeral_familia_mafia",
    "08_superman_vuela_seis_soles_noquea_world_forger",
    "09_thor_muerte_serpiente_midgard_nueve_pasos",
    "10_flash_barry_allen_se_convierte_en_rayo_crisis"
]

all_passed = True
print("================ MASTER AUDIT: 10 STORIES CURATED PANELS ================\n")

for idx, story in enumerate(stories, 1):
    story_dir = PANELS_DIR / story
    if not story_dir.exists():
        print(f"[{idx}/10] ❌ MISSING DIRECTORY: {story}")
        all_passed = False
        continue
        
    scenes = []
    missing_scenes = []
    for s_idx in range(1, 5):
        s_file = story_dir / f"scene_{s_idx:02d}.jpg"
        if not s_file.exists():
            missing_scenes.append(f"scene_{s_idx:02d}.jpg")
        else:
            im = Image.open(s_file)
            if im.size != (1080, 1920):
                print(f"  ❌ Invalid size for {s_file.name}: {im.size} (expected 1080x1920)")
                all_passed = False
            scenes.append(im.convert('RGB'))
            
    if missing_scenes:
        print(f"[{idx}/10] ❌ {story}: Missing scenes {missing_scenes}")
        all_passed = False
        continue
        
    # Check RMS differences
    min_rms = 999.0
    for i in range(len(scenes)):
        for j in range(i + 1, len(scenes)):
            arr1 = np.array(scenes[i], dtype=np.float32)
            arr2 = np.array(scenes[j], dtype=np.float32)
            rms = np.sqrt(np.mean((arr1 - arr2) ** 2))
            if rms < min_rms:
                min_rms = rms
                
    if min_rms < 12.0:
        print(f"[{idx}/10] ❌ {story}: FAILED RMS check! Min RMS = {min_rms:.2f} < 12.0")
        all_passed = False
    else:
        print(f"[{idx}/10] ✅ {story}: ALL 4 SCENES OK (1080x1920, Min RMS = {min_rms:.2f})")

print("\n" + "=" * 70)
if all_passed:
    print("🎯 MASTER QUALITY GATE PASSED: 10/10 STORIES READY FOR VIDEO PRODUCTION!")
else:
    print("❌ QUALITY GATE FAILED! Please fix the errors above.")
    sys.exit(1)
