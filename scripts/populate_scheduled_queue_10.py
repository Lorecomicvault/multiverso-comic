import os
import sys
import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

FINALS_DIR = PROJECT_ROOT / "output" / "batch_10_inéditos" / "finals"
QUEUE_DIR = PROJECT_ROOT / "scheduled_queue"

SLOTS = [
    {
        "slot": "01_punisher_oso_polar_zoologico",
        "id": "punisher_oso_polar_zoologico_gnucci",
        "mp4": "The_Punisher_Alimentó_a_un_Oso_Polar_con_un_Gangster_en_el_Zoológico.mp4",
        "thumb": "The_Punisher_Alimentó_a_un_Oso_Polar_con_un_Gangster_en_el_Zoológico_thumb.jpg",
        "title": "¡The Punisher Alimentó a un Oso Polar con un Gangster en el Zoológico! 🐻❄️",
        "character": "The Punisher",
        "description": "El día en que The Punisher alimentó a un oso polar con un mafioso en Central Park. La justicia más brutal de Frank Castle en Welcome Back, Frank.",
        "hashtags": "#ThePunisher #FrankCastle #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "02_ghostrider_asedio_cielo_zadkiel",
        "id": "ghostrider_asedio_cielo_zadkiel",
        "mp4": "Ghost_Rider_Condujo_su_Moto_Directo_al_Cielo_para_Quemar_a_Zadkiel.mp4",
        "thumb": "Ghost_Rider_Condujo_su_Moto_Directo_al_Cielo_para_Quemar_a_Zadkiel_thumb.jpg",
        "title": "¡Ghost Rider Condujo su Moto Directo al Cielo para Quemar a Zadkiel! 🔥🏍️⚡",
        "character": "Ghost Rider",
        "description": "Cuando Ghost Rider asaltó el Paraíso para quemar al arcángel rebelde Zadkiel. La batalla celestial más épica de Marvel.",
        "hashtags": "#GhostRider #JohnnyBlaze #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "03_moonknight_mr_knight_edificio",
        "id": "moonknight_mr_knight_edificio_rescate",
        "mp4": "Mr_Knight_Limpió_un_Edificio_Entero_de_Secuestradores_con_Traje_Blanco.mp4",
        "thumb": "Mr_Knight_Limpió_un_Edificio_Entero_de_Secuestradores_con_Traje_Blanco_thumb.jpg",
        "title": "¡Mr. Knight Limpió un Edificio Entero de Secuestradores con Traje Blanco! 🌙🥋",
        "character": "Moon Knight",
        "description": "La legendaria escena de acción de Mr. Knight limpiando un edificio piso por piso en traje blanco. Moon Knight de Warren Ellis.",
        "hashtags": "#MoonKnight #MrKnight #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "04_namor_destruccion_tierra_antimateria",
        "id": "namor_destruccion_tierra_antimateria",
        "mp4": "Namor_Apretó_el_Gatillo_y_Destruyó_una_Tierra_Entera_para_Salvar_a_Marvel.mp4",
        "thumb": "Namor_Apretó_el_Gatillo_y_Destruyó_una_Tierra_Entera_para_Salvar_a_Marvel_thumb.jpg",
        "title": "¡Namor Apretó el Gatillo y Destruyó una Tierra Entera para Salvar a Marvel! 🌊💣",
        "character": "Namor",
        "description": "El día en que Namor apretó el detonador de antimateria para destruir un planeta entero durante las Incursiones de Hickman.",
        "hashtags": "#Namor #Illuminati #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "05_swampthing_leccion_anatomia_vegetal",
        "id": "swampthing_leccion_anatomia_vegetal",
        "mp4": "El_Secreto_más_Oscuro_de_Swamp_Thing_La_Planta_que_Creía_Ser_Humana.mp4",
        "thumb": "El_Secreto_más_Oscuro_de_Swamp_Thing_La_Planta_que_Creía_Ser_Humana_thumb.jpg",
        "title": "¡El Secreto más Oscuro de Swamp Thing! La Planta que Creía Ser Humana 🌿🧪",
        "character": "Swamp Thing",
        "description": "La perturbadora revelación de Alan Moore: Swamp Thing nunca fue humano, sino una planta que creyó ser un hombre.",
        "hashtags": "#SwampThing #AlanMoore #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "06_blackbolt_bomba_t_falla_espacio",
        "id": "blackbolt_bomba_t_falla_espacio",
        "mp4": "Black_Bolt_Destruyó_el_Espacio_con_su_Voz_y_Abrió_una_Falla_en_el_Cosmos.mp4",
        "thumb": "Black_Bolt_Destruyó_el_Espacio_con_su_Voz_y_Abrió_una_Falla_en_el_Cosmos_thumb.jpg",
        "title": "¡Black Bolt Destruyó el Espacio con su Voz y Abrió una Falla en el Cosmos! 👑⚡",
        "character": "Black Bolt",
        "description": "El grito de Black Bolt que desgarró el espacio cósmico y creó La Falla en War of Kings.",
        "hashtags": "#BlackBolt #Inhumans #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "07_deadpool_wolverine_corea_norte",
        "id": "deadpool_wolverine_corea_del_norte",
        "mp4": "Deadpool_y_Wolverine_Rescataron_a_Niños_Mutantes_en_Corea_del_Norte.mp4",
        "thumb": "Deadpool_y_Wolverine_Rescataron_a_Niños_Mutantes_en_Corea_del_Norte_thumb.jpg",
        "title": "¡Deadpool y Wolverine Rescataron a Niños Mutantes en Corea del Norte! ⚔️🇰🇷",
        "character": "Deadpool",
        "description": "La desgarradora misión de Deadpool, Wolverine y Cap en Corea del Norte en The Good, the Bad and the Ugly.",
        "hashtags": "#Deadpool #Wolverine #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "08_wonderwoman_hiketeia_bota_batman",
        "id": "wonderwoman_hiketeia_bota_batman",
        "mp4": "Wonder_Woman_le_Puso_la_Bota_en_la_Cara_a_Batman_por_un_Juramento_Sagrado.mp4",
        "thumb": "Wonder_Woman_le_Puso_la_Bota_en_la_Cara_a_Batman_por_un_Juramento_Sagrado_thumb.jpg",
        "title": "¡Wonder Woman le Puso la Bota en la Cara a Batman por un Juramento Sagrado! 🏛️⚔️",
        "character": "Wonder Woman",
        "description": "El legendario enfrentamiento en The Hiketeia: Wonder Woman vence a Batman y le coloca su bota en el rostro por un juramento sagrado.",
        "hashtags": "#WonderWoman #Batman #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "09_lobo_expulsado_cielo_infierno",
        "id": "lobo_expulsado_cielo_infierno",
        "mp4": "El_Cielo_y_el_Infierno_Expulsaron_a_Lobo_Porque_Nadie_lo_Soportaba.mp4",
        "thumb": "El_Cielo_y_el_Infierno_Expulsaron_a_Lobo_Porque_Nadie_lo_Soportaba_thumb.jpg",
        "title": "¡El Cielo y el Infierno Expulsaron a Lobo Porque Nadie lo Soportaba! 🚬💀",
        "character": "Lobo",
        "description": "Por qué Lobo es inmortal: el Cielo y el Infierno lo expulsaron porque nadie podía soportarlo en Lobo's Back.",
        "hashtags": "#Lobo #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": "10_batman_black_mirror_james_gordon",
        "id": "batman_black_mirror_james_gordon_jr",
        "mp4": "El_Hijo_Psicópata_del_Comisionado_Gordon_que_Aterrorizó_a_Gotham.mp4",
        "thumb": "El_Hijo_Psicópata_del_Comisionado_Gordon_que_Aterrorizó_a_Gotham_thumb.jpg",
        "title": "¡El Hijo Psicópata del Comisionado Gordon que Aterrorizó a Gotham! 🔪🩸🦇",
        "character": "Batman",
        "description": "La siniestra historia de James Gordon Jr., el hijo del comisionado que intentó convertir a los niños de Gotham en psicópatas.",
        "hashtags": "#Batman #JamesGordonJr #TheBlackMirror #DCComics #Shorts #Reels #TikTok"
    }
]

def populate():
    print(f"Poblando scheduled_queue con 10 slots inéditos en: {QUEUE_DIR}")
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)

    for item in SLOTS:
        slot_dir = QUEUE_DIR / item["slot"]
        slot_dir.mkdir(parents=True, exist_ok=True)

        src_mp4 = FINALS_DIR / item["mp4"]
        dst_mp4 = slot_dir / "video.mp4"
        if not src_mp4.exists():
            print(f"ERROR: Archivo no encontrado: {src_mp4}")
            continue
        shutil.copy2(src_mp4, dst_mp4)

        src_thumb = FINALS_DIR / item["thumb"]
        dst_thumb = slot_dir / "thumb.jpg"
        if src_thumb.exists():
            shutil.copy2(src_thumb, dst_thumb)

        meta = {
            "id": item["id"],
            "title": item["title"],
            "character": item["character"],
            "description": item["description"],
            "hashtags": item["hashtags"],
            "video_file": "video.mp4",
            "source": "batch_10_inéditos",
            "voice": "Puck"
        }
        with open(slot_dir / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        print(f"  [OK] {item['slot']} listo ({dst_mp4.stat().st_size // 1024 // 1024} MB)")

    print("\nVerificación de scheduled_queue completa!")

if __name__ == "__main__":
    populate()
