import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "wonderwoman_hiketeia_bota_batman"

texts = [
    "Bajo la mirada silenciosa de las temibles Erinias, los espíritus vengadores de la tragedia griega, una fugitiva desesperada acudió a Themyscira para invocar el antiguo ritual sagrado de Hiketeia.",
    "Al aceptar la súplica sagrada, Diana de Themyscira quedó atada por las leyes divinas del Olimpo a protegerla con su vida, empuñando su guardia amazona.",
    "Batman irrumpió en la noche exigiendo la custodia de la fugitiva, desatando un combate frontal implacable donde Wonder Woman sometió al murciélago contra el pavimento.",
    "Demostrando la superioridad absoluta de su fuerza divina, Diana derribó al Caballero de la Noche y colocó su bota firmemente sobre su rostro, sellando su juramento."
]

for i, txt in enumerate(texts, 1):
    fpath = dest_dir / f"scene_{i:02d}.jpg"
    res = verify_visual_alignment_with_gemini(str(fpath), txt)
    print(f"Scene {i}: Score={res.get('score')}/10, Action={res.get('depicts_action')}", flush=True)
    print(f"  Reason: {res.get('reason')}", flush=True)
