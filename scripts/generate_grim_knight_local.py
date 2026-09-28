"""
Multiverso Comic - Generador Local de Alta Precisión
Proyecto: The Grim Knight: El Batman que Disparó a Matar en Crime Alley
Fórmula Estándar de Oro (1080x1920, Papel Rasgado 0.65s, Bangers Noir, Voice Studio-B)
"""

import os
import sys
import shutil
from pathlib import Path
from PIL import Image

# Configurar rutas del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

# Cargar variables de entorno locales
from src.cloud_runner import load_env_file, create_full_panel_frame, record_production
load_env_file()

from src.comic_precision_scraper import get_file_url_cross_wiki, download_image
from src.pipeline import run_pipeline

STORY = {
    "id": "batman_grim_knight_crime_alley",
    "universe": "DC",
    "character": "The Grim Knight",
    "title": "The Grim Knight: El Batman que Disparó a Matar en Crime Alley",
    "theme_signature": "batman:grim_knight:crime_alley_arsenal_militar",
    "description": "En este oscuro universo alternativo, Bruce Wayne no lloró la muerte de sus padres: recogió el arma de Joe Chill y lo ejecutó en el acto convirtiéndose en el despiadado Grim Knight.",
    "hashtags": "#TheGrimKnight #Batman #DCComics #DarkMultiverse #BatmanWhoLaughs #ComicsNarrados #Shorts #Reels",
    "scenes": [
        {
            "scene_number": 1,
            "text": "¿Sabías que en el Multiverso Oscuro, la noche en que asesinaron a sus padres, Bruce Wayne no derramó lágrimas?",
            "file": "File:Wayne Murder Grim Knight 0001.jpg"
        },
        {
            "scene_number": 2,
            "text": "Viendo el revólver de Joe Chill sobre el asfalto, el niño lo recogió y le disparó en el pecho sin piedad.",
            "file": "File:Joe Chill Grim Knight 0001.PNG"
        },
        {
            "scene_number": 3,
            "text": "Sin código moral, convirtió a Gotham en una zona de guerra ejecutando a cada villano con tácticas militares letales.",
            "file": "File:Batman Villains Grim Knight 0001.PNG"
        },
        {
            "scene_number": 4,
            "text": "Armado hasta los dientes y aliado con el Batman que Ríe, se consagró como el implacable Grim Knight.",
            "file": "File:The Batman Who Laughs The Grim Knight Vol 1 1 Textless.jpg"
        }
    ]
}

FINAL_DEST_DIR = Path(r"C:\Users\Vanes\Downloads\video\Comics")
OUTPUT_ROOT = Path("output")

def main():
    print("==================================================================")
    print(f"INICIANDO PRODUCCIÓN LOCAL: {STORY['title']}")
    print("Estándar de Oro: 4 Escenas | Bangers Noir | Papel Rasgado 0.65s | Foley")
    print("==================================================================")

    proj_dir = OUTPUT_ROOT / STORY["id"]
    proj_dir.mkdir(parents=True, exist_ok=True)

    # Limpiar renders anteriores para garantizar compilación fresca
    for sub in ["composed", "master_reel"]:
        d = proj_dir / sub
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)

    scenes_data = []
    scene_videos = []

    for sc in STORY["scenes"]:
        sn = sc["scene_number"]
        txt = sc["text"]
        target_f = sc["file"]
        sc_folder = proj_dir / f"scene_{sn:02d}"
        sc_folder.mkdir(parents=True, exist_ok=True)
        img_path = sc_folder / f"scene_{sn:02d}.jpg"

        print(f"\n[Escena {sn}] Procesando imagen...")
        # Descargar viñeta canónica oficial si no existe
        if not img_path.exists() or img_path.stat().st_size < 10000:
            temp_raw = sc_folder / f"raw_{sn:02d}.jpg"
            url, wiki = get_file_url_cross_wiki("dc.fandom.com", target_f)
            if not url:
                raise RuntimeError(f"No se pudo resolver URL de {target_f}")
            
            ok = download_image(url, wiki, str(temp_raw))
            if not ok or not temp_raw.exists():
                raise RuntimeError(f"Error descargando {target_f} desde {url}")

            # Aplicar enmarcado vertical 1080x1920 con fondo desenfocado y safe zone
            with Image.open(temp_raw) as raw_im:
                framed_im = create_full_panel_frame(raw_im.convert("RGB"), target_w=1080, target_h=1920)
                framed_im.save(img_path, "JPEG", quality=95)
            
            if temp_raw.exists():
                temp_raw.unlink()
            print(f"  OK -> Viñeta encuadrada en 1080x1920 con fondo desenfocado.")
        else:
            print(f"  OK -> Imagen existente {img_path.name}")

        scenes_data.append({
            "scene_number": sn,
            "voiceover_text": txt,
            "narration": txt
        })

        scene_videos.append({
            "folder": f"scene_{sn:02d}",
            "video": str(img_path),
            "images": [str(img_path)],
            "scene_number": sn,
            "is_image": True,
            "image_count": 1
        })

    generation = {
        "path": str(proj_dir),
        "name": STORY["id"],
        "script": {
            "metadata": {
                "title": STORY["title"],
                "character": STORY["character"],
                "description": STORY["description"],
                "hashtags": STORY["hashtags"],
                "voice": "es-US-Studio-B"
            },
            "scenes": scenes_data
        },
        "scene_videos": scene_videos,
        "scene_count": len(scene_videos)
    }

    # Guardar script.json
    with open(proj_dir / "script.json", "w", encoding="utf-8") as f:
        import json
        json.dump(generation["script"], f, indent=2, ensure_ascii=False)

    FINAL_DEST_DIR.mkdir(parents=True, exist_ok=True)
    voice_choice = os.environ.get("VOICE", "es-US-Studio-B")
    print(f"\n[Master Engine] Compilando Reel con voz: {voice_choice}...")

    out_video = run_pipeline(
        generation=generation,
        output_name=STORY["id"],
        voice=voice_choice,
        output_root=str(OUTPUT_ROOT),
        width=1080,
        height=1920,
        final_video_dir=str(FINAL_DEST_DIR),
        generate_thumbnail=True
    )

    print("\n==================================================================")
    print("¡PRODUCCIÓN COMPLETADA CON ÉXITO!")
    print(f"Video exportado a: {out_video}")
    print("==================================================================")

    # Registrar en el ledger
    record_production(STORY, "local_production", out_video)
    print(f"Historia registrada en published_ledger.json para prevenir duplicados.")

if __name__ == "__main__":
    main()
