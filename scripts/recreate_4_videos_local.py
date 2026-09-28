"""
Recrea los 4 videos locales en C:\\Users\\Vanes\\Downloads\\video\\Comics
con el Nuevo Motor Cinematografico Vertical (1080x1920):
- Transiciones 3D de papel rasgado (0.65s) con Foley sfx_rip
- Subtitulos Bangers Comic Noir (Option 6 ASS: #181818 caja, #00F0FF resaltado dinámico)
- Overlay Social CTA
- Sincronizacion visual-narrativa 100% garantizada escena por escena
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.pipeline import run_pipeline

PROJECTS = [
    {
        "dir_name": "black_manta_infanticidio_aquaman",
        "title": "Black Manta: El Asesinato del Hijo de Aquaman",
        "safe_name": "Black_Manta_El_Asesinato_del_Hijo_de_Aquaman",
        "character": "Black Manta",
        "scenes": [
            {"scene_number": 1, "text": "Buscando quebrar el alma de Aquaman para siempre, Black Manta secuestró a su pequeño hijo Arthur Jr. encerrándolo en una esfera que se llenaba de aire letal."},
            {"scene_number": 2, "text": "En una arena siniestra, el villano forzó a Aquaman y a su protegido Aqualad a luchar a muerte con tridentes para intentar salvar al infante."},
            {"scene_number": 3, "text": "Desesperado, el rey de Atlantis rompió las cadenas y lanzó su tridente con toda su furia para destrozar la prisión de cristal."},
            {"scene_number": 4, "text": "Pero el tiempo se agotó. Aquaman sostuvo en sus brazos el cuerpo sin vida de su bebé, marcando el crimen más desgarrador e imperdonable de los cómics."}
        ]
    },
    {
        "dir_name": "ghost_rider_vs_world_war_hulk",
        "title": "World War Hulk: Cuando Ghost Rider se Negó a Pelear contra Hulk",
        "safe_name": "World_War_Hulk_Cuando_Ghost_Rider_se_Negó_a_Pelear_contra_Hulk",
        "character": "Ghost Rider",
        "scenes": [
            {"scene_number": 1, "text": "Tras destruir a los Vengadores y someter a Nueva York, un colosal World War Hulk parecía un monstruo totalmente imparable para la Tierra."},
            {"scene_number": 2, "text": "Johnny Blaze desató al Espíritu de la Venganza y una tormenta de fuego infernal envolvió las calles para detener al gigante esmeralda."},
            {"scene_number": 3, "text": "Pero cuando Zarathos tomó el control total y miró fijamente el alma de Hulk, vio que no había maldad, sino una víctima inocente buscando justicia."},
            {"scene_number": 4, "text": "Dictando su veredicto divino, el vengador fantasma dio media vuelta en su motocicleta y se marchó, abandonando a los culpables Illuminati a su destino."}
        ]
    },
    {
        "dir_name": "daredevil_shadowland_bullseye",
        "title": "Daredevil Shadowland: La Muerte de Bullseye",
        "safe_name": "Daredevil_Shadowland_La_Muerte_de_Bullseye",
        "character": "Daredevil",
        "scenes": [
            {"scene_number": 1, "text": "Corrompido por la Bestia tras liderar a La Mano, Matt Murdock erigió una fortaleza de sombras en Hell's Kitchen bajo una ley implacable."},
            {"scene_number": 2, "text": "El asesino Bullseye llegó para desafiarlo en las azoteas, burlándose con arrogancia de la regla de no matar que siempre definió al demonio."},
            {"scene_number": 3, "text": "Pero esta vez Daredevil no dudó. Desarmó al villano en segundos y le fracturó ambos brazos con un crujido escalofriante."},
            {"scene_number": 4, "text": "Ante la mirada atónita de los héroes, Matt tomó el sai de Bullseye y se lo clavó en el corazón, repitiendo exactamente la misma muerte de Elektra."}
        ]
    },
    {
        "dir_name": "batman_red_death_speed_force",
        "title": "Batman Red Death: El Día en que Bruce Robó la Speed Force",
        "safe_name": "Batman_Red_Death_El_Día_en_que_Bruce_Robó_la_Speed_Force",
        "character": "Batman",
        "scenes": [
            {"scene_number": 1, "text": "En Tierra -52, Gotham colapsaba hacia el abismo y un Bruce Wayne envejecido vio morir a todos sus aliados cayendo en la desesperación total."},
            {"scene_number": 2, "text": "Convencido de que solo la Speed Force salvaría su mundo, Batman emboscó a Flash utilizando el arsenal congelante de los Rogues para someterlo."},
            {"scene_number": 3, "text": "Despiadado, Bruce encadenó a Barry sobre el capó del Batimóvil y aceleró directo a la tormenta temporal, ignorando las súplicas de su amigo."},
            {"scene_number": 4, "text": "La energía cósmica desgarró sus cuerpos fusionándolos a nivel atómico. Barry quedó atrapado en su mente, y Batman renació como Red Death."}
        ]
    }
]

FINAL_DEST_DIR = Path(r"C:\Users\Vanes\Downloads\video\Comics")

def process_project(proj: dict):
    dir_name = proj["dir_name"]
    proj_dir = Path("output") / dir_name
    print(f"\n=======================================================")
    print(f"PROCESANDO: {proj['title']}")
    print(f"Carpeta: {proj_dir}")

    # Limpiar composed y master_reel para forzar re-renderizado con las nuevas imágenes alineadas
    comp_dir = proj_dir / "composed"
    master_dir = proj_dir / "master_reel"
    if comp_dir.exists():
        shutil.rmtree(comp_dir, ignore_errors=True)
    if master_dir.exists():
        shutil.rmtree(master_dir, ignore_errors=True)

    # Preparar scene_videos
    scene_videos = []
    scenes_data = []
    for sc in proj["scenes"]:
        sn = sc["scene_number"]
        txt = sc["text"]
        sc_folder = proj_dir / f"scene_{sn:02d}"
        img_path = sc_folder / f"scene_{sn:02d}.jpg"
        if not img_path.exists():
            raise FileNotFoundError(f"No se encontró la imagen: {img_path}")
        
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
        "name": dir_name,
        "script": {
            "metadata": {
                "title": proj["title"],
                "character": proj["character"],
                "voice": "es-US-Studio-B"
            },
            "scenes": scenes_data
        },
        "scene_videos": scene_videos,
        "scene_count": len(scene_videos)
    }

    # Ejecutar pipeline vertical con el nuevo motor
    out_video = run_pipeline(
        generation=generation,
        output_name=dir_name,
        voice="es-US-Studio-B",
        output_root="output",
        width=1080,
        height=1920,
        final_video_dir=str(FINAL_DEST_DIR),
        generate_thumbnail=True
    )
    print(f"OK -> Video exportado a: {out_video}")
    return out_video


def main():
    FINAL_DEST_DIR.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        try:
            process_project(p)
        except Exception as e:
            print(f"ERROR en {p['title']}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
