import sys
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "deadpool_wolverine_corea_del_norte"

texts = [
    "En una de las historias más crudas de Marvel, el siniestro científico Bartol Utler engañó a Wade Wilson para secuestrar y extirpar sus órganos en un laboratorio secreto.",
    "El rastro condujo a un campo de concentración en Corea del Norte, donde sujetos de prueba eran torturados para replicar los poderes de los X-Men.",
    "Deadpool, Wolverine y el Capitán América lanzaron un asalto implacable contra las tropas del ejército norcoreano en el complejo militar.",
    "Tras demoler las instalaciones y liberar a las familias y mutantes cautivos, Wade contempló las secuelas del rescate jurando proteger a los inocentes."
]

for i, txt in enumerate(texts, 1):
    fpath = dest_dir / f"scene_{i:02d}.jpg"
    res = verify_visual_alignment_with_gemini(str(fpath), txt)
    print(f"Scene {i}: Score={res.get('score')}/10, Action={res.get('depicts_action')}", flush=True)
    print(f"  Reason: {res.get('reason')}", flush=True)
