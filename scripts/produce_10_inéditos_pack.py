"""
Master Production Engine: 10 Videos Virales Inéditos de 60 Segundos (100% Nuevos)
================================================================================
Formato: 1080x1920 (Vertical 9:16 para Shorts, Reels y TikTok)
Duración: 55 a 60 segundos por video
Visuales: 100% Viñetas canónicas curadas 1:1 con la narración
Efectos: Transiciones 3D de papel rasgado + Foley + Subtítulos Bangers Comic Noir
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path

# Force UTF-8 stdout
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.pipeline import run_pipeline
from src.cloud_runner import record_production, load_ledger, is_duplicate, build_cloud_generation

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_10_inéditos"
PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"

PROJECTS = [
    {
        "id": "punisher_oso_polar_zoologico_gnucci",
        "title": "¡The Punisher Alimentó a un Oso Polar con un Gangster en el Zoológico! 🐻❄️",
        "character": "The Punisher",
        "folder": "punisher_oso_polar_zoologico_gnucci",
        "theme_signature": "punisher:welcome_back_frank:oso_polar_zoologico_gnucci",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En su guerra sin cuartel contra la familia criminal Gnucci, Frank Castle persiguió a los últimos matones de la mafia a través del zoológico de Central Park en plena noche."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin piedad alguna, Frank Castle neutralizó a los sicarios de la mafia sometiéndolos por la fuerza bruta para abrirse paso en la oscuridad."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Para desatar el caos, The Punisher saltó a la exhibición y le propinó un brutal puñetazo en la mandíbula a un oso polar para enfurecerlo contra los criminales."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El oso polar enfurecido arremetió con furia salvaje y decapitó de un zarpazo mortal al matón de la mafia, dejando una masacre en el zoológico."
            }
        ],
        "description": "El día en que The Punisher alimentó a un oso polar con un mafioso en Central Park. La justicia más brutal de Frank Castle en Welcome Back, Frank.",
        "hashtags": "#ThePunisher #FrankCastle #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "ghostrider_asedio_cielo_zadkiel",
        "title": "¡Ghost Rider Condujo su Moto Directo al Cielo para Quemar a Zadkiel! 🔥🏍️⚡",
        "character": "Ghost Rider",
        "folder": "ghostrider_asedio_cielo_zadkiel",
        "theme_signature": "ghost_rider:heaven_on_fire:asedio_cielo_zadkiel_jason_aaron",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras traicionar al Creador y usurpar el trono del Paraíso, el arcángel renegado Zadkiel creyó que su dominio celestial sobre la creación era absoluto e intocable."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero no contaba con que Johnny Blaze y Danny Ketch unirían sus fuegos infernales para liderar a un ejército de Espíritus de la Venganza directo a las puertas celestiales."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Con un rugido ensordecedor de motores y fuego del averno, Ghost Rider embistió y destrozó los portales de perlas sagradas, dejando una estela de fuego en los cielos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Zadkiel sintió por primera vez el terror en su carne divina cuando la Mirada de Penitencia consumió sus alas, demostrando que ningún tirano puede escapar al juicio."
            }
        ],
        "description": "Cuando Ghost Rider asaltó el Paraíso para quemar al arcángel rebelde Zadkiel. La batalla celestial más épica de Marvel.",
        "hashtags": "#GhostRider #JohnnyBlaze #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "moonknight_mr_knight_edificio_rescate",
        "title": "¡Mr. Knight Limpió un Edificio Entero de Secuestradores con Traje Blanco! 🌙🥋",
        "character": "Moon Knight",
        "folder": "moonknight_mr_knight_edificio_rescate",
        "theme_signature": "moon_knight:mr_knight_edificio:traje_blanco_secuestro",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Cuando una peligrosa banda armada secuestró a una niña inocente en un edificio abandonado de Nueva York, Marc Spector decidió no ponerse su capa, sino algo más elegante."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Vestido con un traje blanco de sastre impoluto y armado únicamente con dos porras de combate, Mr. Knight pateó la puerta principal entrando en territorio enemigo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Piso por piso, avanzó en la oscuridad esquivando disparos a quemarropa y noqueando a los criminales con una precisión quirúrgica demoledora, sin mancharse una gota de sangre."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En el último piso, derribó al líder de la banda de una sola patada y rescató a la niña en brazos, caminando hacia la luz de la luna intacto como un fantasma vengador."
            }
        ],
        "description": "La legendaria escena de acción de Mr. Knight limpiando un edificio piso por piso en traje blanco. Moon Knight de Warren Ellis.",
        "hashtags": "#MoonKnight #MrKnight #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "namor_destruccion_tierra_antimateria",
        "title": "¡Namor Apretó el Gatillo y Destruyó una Tierra Entera para Salvar a Marvel! 🌊💣",
        "character": "Namor",
        "folder": "namor_destruccion_tierra_antimateria",
        "theme_signature": "namor:illuminati_new_avengers:bomba_antimateria_great_society",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Dos universos estaban a segundos de colisionar en una Incursión fatal, y la única forma de salvar a la Tierra 616 era aniquilar por completo el mundo de la Gran Sociedad."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con la bomba de antimateria armada, Black Panther y los héroes más virtuosos de la Tierra temblaron ante el peso moral de cometer un genocidio de miles de millones de inocentes."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Despreciando la cobardía de sus compañeros, Namor dio un paso al frente, arrebató el detonador y pronunció las palabras que cambiaron la historia: 'Mis manos ya están manchadas'."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El dispositivo detonó en la atmósfera, pulverizando el planeta entero en una onda expansiva cósmica mientras Namor miraba fijamente el abismo que ningún otro héroe se atrevió a cruzar."
            }
        ],
        "description": "El día en que Namor apretó el detonador de antimateria para destruir un planeta entero durante las Incursiones de Hickman.",
        "hashtags": "#Namor #Illuminati #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "swampthing_leccion_anatomia_vegetal",
        "title": "¡El Secreto más Oscuro de Swamp Thing! La Planta que Creía Ser Humana 🌿🧪",
        "character": "Swamp Thing",
        "folder": "swampthing_leccion_anatomia_vegetal",
        "theme_signature": "swamp_thing:the_anatomy_lesson:autopsia_planta_humana_moore",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Creyendo haber capturado el cadáver congelado del monstruo del pantano, la corporación Sunderland contrató al brillante biólogo Jason Woodrue para realizar la autopsia definitiva."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al abrir el torso con el bisturí, Woodrue quedó petrificado de horror: no había corazón, no había pulmones, ni una sola gota de sangre o tejido humano en su interior."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "El microscopio confirmó la verdad más aterradora de los cómics: Alec Holland murió quemado en la explosión, y la criatura era una planta vegetal que absorbió su mente y creyó ser un hombre."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al descongelarse en el laboratorio inundado, Swamp Thing abrió los ojos y comprendió su verdadera naturaleza divina: no era un humano maldito, sino la furia encarnada del Verde elemental."
            }
        ],
        "description": "La perturbadora revelación de Alan Moore: Swamp Thing nunca fue humano, sino una planta que creyó ser un hombre.",
        "hashtags": "#SwampThing #AlanMoore #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "blackbolt_bomba_t_falla_espacio",
        "title": "¡Black Bolt Destruyó el Espacio con su Voz y Abrió una Falla en el Cosmos! 👑⚡",
        "character": "Black Bolt",
        "folder": "blackbolt_bomba_t_falla_espacio",
        "theme_signature": "black_bolt:war_of_kings:grito_bomba_t_falla_cosmica",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En el clímax de la sangrienta guerra galáctica entre los Inhumanos y el Imperio Shi'ar, el emperador tirano Vulcan abordó la nave de mando para matar personalmente a Black Bolt."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Ambos monarcas cósmicos cayeron combatiendo dentro del núcleo de la Bomba-Terrigen, un dispositivo masivo diseñado para mutar a toda la galaxia con nieblas terrígenas."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sabiendo que no había otra salida para salvar a su pueblo, el Rey Silencioso separó sus labios por primera vez en años y desató un grito desgarrador a máxima potencia."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "La onda de choque colapsó la bomba y desató una detonación de tal magnitud que fracturó la realidad, abriendo 'La Falla', una herida gigantesca en el tejido del cosmos."
            }
        ],
        "description": "El grito de Black Bolt que desgarró el espacio cósmico y creó La Falla en War of Kings.",
        "hashtags": "#BlackBolt #Inhumans #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "deadpool_wolverine_corea_del_norte",
        "title": "¡Deadpool y Wolverine Rescataron a Niños Mutantes en Corea del Norte! ⚔️🇰🇷",
        "character": "Deadpool",
        "folder": "deadpool_wolverine_corea_del_norte",
        "theme_signature": "deadpool:the_good_the_bad_the_ugly:campamentos_corea_norte",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En una de las historias más crudas de Marvel, el siniestro científico Bartol Utler engañó a Wade Wilson para secuestrar y extirpar sus órganos en un laboratorio secreto."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El rastro condujo a un campo de concentración en Corea del Norte, donde sujetos de prueba eran torturados para replicar los poderes de los X-Men."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Decidido a irrumpir en el campamento, Deadpool empuñó sus armas y preparó su ofensiva armada listo para la acción."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En el interior del complejo liberado, el Capitán América y Deadpool contemplaron el desenlace de la misión, confrontando la tragedia de los experimentos mutantes."
            }
        ],
        "description": "La desgarradora misión de Deadpool, Wolverine y Cap en Corea del Norte en The Good, the Bad and the Ugly.",
        "hashtags": "#Deadpool #Wolverine #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "wonderwoman_hiketeia_bota_batman",
        "title": "¡Wonder Woman le Puso la Bota en la Cara a Batman por un Juramento Sagrado! 🏛️⚔️",
        "character": "Wonder Woman",
        "folder": "wonderwoman_hiketeia_bota_batman",
        "theme_signature": "wonder_woman:the_hiketeia:juramento_sagrado_bota_batman",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Bajo la mirada silenciosa de las temibles Erinias, los espíritus vengadores de la tragedia griega, una fugitiva desesperada acudió a Themyscira para invocar el antiguo ritual sagrado de Hiketeia."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con su indumentaria de guerra y lista para el combate en las calles de la ciudad, Wonder Woman montó guardia implacable, decidida a frenar a quien intentara romper el juramento."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Batman irrumpió en la noche exigiendo la custodia de la fugitiva, desatando un combate frontal implacable donde Wonder Woman sometió al murciélago contra el pavimento."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Demostrando la superioridad absoluta de su fuerza divina, Diana derribó al Caballero de la Noche y colocó su bota firmemente sobre su rostro, sellando su juramento."
            }
        ],
        "description": "El legendario enfrentamiento en The Hiketeia: Wonder Woman vence a Batman y le coloca su bota en el rostro por un juramento sagrado.",
        "hashtags": "#WonderWoman #Batman #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "lobo_expulsado_cielo_infierno",
        "title": "¡El Cielo y el Infierno Expulsaron a Lobo Porque Nadie lo Soportaba! 🚬💀",
        "character": "Lobo",
        "folder": "lobo_expulsado_cielo_infierno",
        "theme_signature": "lobo:lobos_back:expulsion_cielo_infierno_inmortal",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En un duelo sangriento e implacable a través del cosmos, Lobo, el cazarrecompensas más brutal de la galaxia, arrasó con sus enemigos en un combate cuerpo a cuerpo feroz."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al llegar al Infierno, Lobo comenzó una sangrienta carnicería contra hordas de demonios, convirtiendo el averno en un caos absoluto hasta que el Diablo exigió su expulsión."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Enviado de inmediato al Paraíso, Lobo profanó el santuario celestial, aterrorizando a los serafines y convirtiendo las nubes benditas en un campo de batalla."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Expulsado para siempre del Más Allá y devuelto a la vida, Lobo desató una masacre salvaje aplastando a sus enemigos con una furia indestructible."
            }
        ],
        "description": "Por qué Lobo es inmortal: el Cielo y el Infierno lo expulsaron porque nadie podía soportarlo en Lobo's Back.",
        "hashtags": "#Lobo #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "batman_black_mirror_james_gordon_jr",
        "title": "¡El Hijo Psicópata del Comisionado Gordon que Aterrorizó a Gotham! 🔪🩸🦇",
        "character": "Batman",
        "folder": "batman_black_mirror_james_gordon_jr",
        "theme_signature": "batman:the_black_mirror:james_gordon_jr_psicopata_snyder",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras años de ausencia, James Gordon Jr., el hijo mayor del comisionado, regresó a Gotham asegurando estar curado de sus siniestros impulsos psicopáticos infantiles."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero bajo su fachada de joven rehabilitado, James montó un laboratorio secreto donde modificó una toxina química para bloquear permanentemente la empatía y la compasión en el cerebro humano."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Su plan maestro era diabólico: infectar los lotes de leche infantil de la ciudad para convertir a toda la futura generación de niños de Gotham en monstruos asesinos sin remordimiento."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Tras atacar a su hermana Barbara en una trampa mortal, Dick Grayson como Batman lo interceptó en el puente, neutralizando al villano más perturbador y personal de la familia Gordon."
            }
        ],
        "description": "La escalofriante historia de James Gordon Jr., el hijo psicópata de Jim Gordon en Batman: The Black Mirror.",
        "hashtags": "#Batman #TheBlackMirror #DCComics #Comics #Shorts #Reels #TikTok"
    }
]


def produce_single_project(proj: dict) -> str | None:
    proj_id = proj["id"]
    folder_name = proj["folder"]
    curated_folder = CURATED_BASE / folder_name

    print(f"\n========================================================")
    print(f"PRODUCIENDO VIDEO: {proj['title']}")
    print(f"ID: {proj_id} | Carpeta de Viñetas: {curated_folder}")
    print(f"========================================================")

    # Validar que los 4 paneles existan
    missing_panels = []
    scene_art_urls = []
    scenes_text = []
    for sc in proj["scenes"]:
        panel_path = curated_folder / sc["file"]
        if not panel_path.exists():
            missing_panels.append(sc["file"])
        scene_art_urls.append(str(panel_path))
        scenes_text.append(sc["text"])

    if missing_panels:
        print(f"[ERROR] Faltan {len(missing_panels)} paneles en {curated_folder}: {missing_panels}")
        return None

    # Adaptar para build_cloud_generation
    story_payload = dict(proj)
    story_payload["scenes"] = scenes_text
    story_payload["scene_art_urls"] = scene_art_urls

    work_dir = PROJECT_ROOT / "work" / f"batch_{proj_id}"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"-> Verificando viñetas y ejecutando Quality Gate...")
    generation = build_cloud_generation(story_payload, work_dir)

    voice_choice = proj.get("voice", "Puck")
    final_output_dir = PACK_OUTPUT_DIR / "finals"
    final_output_dir.mkdir(parents=True, exist_ok=True)

    try:
        final_video_path = run_pipeline(
            generation=generation,
            output_name=proj_id,
            voice=voice_choice,
            output_root=str(PACK_OUTPUT_DIR),
            width=1080,
            height=1920,
            final_video_dir=str(final_output_dir),
            generate_thumbnail=True
        )
        print(f"[OK] Video generado con éxito: {final_video_path}")
        return final_video_path
    except Exception as e:
        print(f"[ERROR] Falló la compilación de {proj_id}: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Produce los 10 videos virales inéditos")
    parser.add_argument("--index", type=int, default=None, help="Índice específico (1-10) a producir")
    parser.add_argument("--all", action="store_true", help="Producir todos los 10 videos")
    args = parser.parse_args()

    if args.index:
        idx = args.index - 1
        if 0 <= idx < len(PROJECTS):
            produce_single_project(PROJECTS[idx])
        else:
            print(f"Índice {args.index} fuera de rango (1-{len(PROJECTS)})")
    elif args.all:
        print(f"Iniciando producción en lote de los 10 videos...")
        for p in PROJECTS:
            produce_single_project(p)
    else:
        print("Uso: python produce_10_inéditos_pack.py --all  o  --index <1-10>")

if __name__ == "__main__":
    main()
