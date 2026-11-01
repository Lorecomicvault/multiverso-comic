import os
import sys
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "swampthing_leccion_anatomia_vegetal"
dest_dir.mkdir(parents=True, exist_ok=True)

# Page 1: Scene 1 (Dr. Woodrue examining frozen Swamp Thing)
im1 = Image.open('test_st_1.jpg').convert('RGB')
framed1 = create_full_panel_frame(im1, 1080, 1920)
framed1.save(dest_dir / 'scene_01.jpg', quality=95)

# Page 4: Scene 2 (Autopsy and dissection)
im2 = Image.open('test_st_4.jpg').convert('RGB')
framed2 = create_full_panel_frame(im2, 1080, 1920)
framed2.save(dest_dir / 'scene_02.jpg', quality=95)

# Page 3: Scene 3 (Microscope revelation, not human)
im3 = Image.open('test_st_3.jpg').convert('RGB')
framed3 = create_full_panel_frame(im3, 1080, 1920)
framed3.save(dest_dir / 'scene_03.jpg', quality=95)

# Page 6: Scene 4 (Swamp Thing awakening / elemental rage)
im4 = Image.open('test_st_6.jpg').convert('RGB')
framed4 = create_full_panel_frame(im4, 1080, 1920)
framed4.save(dest_dir / 'scene_04.jpg', quality=95)

print("Swamp Thing 1080x1920 framed panels created successfully!", flush=True)

scenes_texts = [
    "Creyendo haber capturado el cadáver congelado del monstruo del pantano, la corporación Sunderland contrató al brillante biólogo Jason Woodrue para realizar la autopsia definitiva.",
    "Al abrir el torso con el bisturí, Woodrue quedó petrificado de horror: no había corazón, no había pulmones, ni una sola gota de sangre o tejido humano en su interior.",
    "El microscopio confirmó la verdad más aterradora de los cómics: Alec Holland murió quemado en la explosión, y la criatura era una planta vegetal que absorbió su mente y creyó ser un hombre.",
    "Al descongelarse en el laboratorio inundado, Swamp Thing abrió los ojos y comprendió su verdadera naturaleza divina: no era un humano maldito, sino la furia encarnada del Verde elemental."
]

for i, txt in enumerate(scenes_texts, 1):
    fpath = dest_dir / f"scene_{i:02d}.jpg"
    res = verify_visual_alignment_with_gemini(str(fpath), txt)
    print(f"Scene {i}: Score={res.get('score')}/10, Action={res.get('depicts_action')}", flush=True)
    print(f"  Reason: {res.get('reason')}", flush=True)
