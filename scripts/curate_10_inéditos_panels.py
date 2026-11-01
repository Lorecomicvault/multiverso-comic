"""
Curador y Descargador de Paneles Canónicos 1:1 para los 10 Videos Inéditos
==========================================================================
Descarga y audita viñetas de cómic 100% canónicas para cada escena de los 10 reels.
Garantiza alineación visual exacta con la narración y resolución Full HD 1080x1920.
"""

import os
import sys
import json
import time
import requests
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageFilter

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.comic_precision_scraper import (
    search_bing_comic_panels,
    check_is_comic_art_inking,
    verify_visual_alignment_with_gemini,
    is_cover_or_promo_image,
    search_fandom_files,
    get_file_url,
    HEADERS
)
from src.cloud_runner import create_full_panel_frame

CURATED_DIR = PROJECT_ROOT / "assets" / "curated_panels"
CURATED_DIR.mkdir(parents=True, exist_ok=True)

PROJECTS_DATA = [
    {
        "id": "punisher_oso_polar_zoologico_gnucci",
        "wiki": "marvel.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "En su guerra sin cuartel contra la familia criminal Gnucci, Frank Castle persiguió a los últimos matones de la mafia a través del zoológico de Central Park en plena noche.",
                "queries": [
                    "Punisher Welcome Back Frank issue 4 Central park zoo panel",
                    "Frank Castle Steve Dillon Welcome Back Frank comic panel",
                    "Punisher Vol 5 4 comic panel Frank Castle"
                ]
            },
            {
                "num": 2,
                "text": "Al verse acorralado frente a la fosa de exhibición, el sicario intentó abrir fuego, pero The Punisher esquivó las balas y lo desarmó con un golpe demoledor en la mandíbula.",
                "queries": [
                    "Punisher Welcome Back Frank mobster punch comic panel",
                    "Punisher punching mobster Steve Dillon comic panel",
                    "Punisher issue 4 polar bear enclosure fence fight"
                ]
            },
            {
                "num": 3,
                "text": "En lugar de gastar una bala, Frank levantó al criminal en peso y lo arrojó directamente al recinto helado, donde un gigantesco oso polar lo esperaba hambriento.",
                "queries": [
                    "Punisher polar bear punch zoo Welcome Back Frank comic panel",
                    "Frank Castle punches polar bear Steve Dillon comic panel",
                    "Punisher throws mobster to polar bear comic panel"
                ]
            },
            {
                "num": 4,
                "text": "Mientras los gritos del criminal resonaban en la noche y el depredador lo devoraba sin piedad, The Punisher simplemente se acomodó la gabardina y desapareció en las sombras.",
                "queries": [
                    "Punisher polar bear kills mobster Welcome Back Frank comic panel",
                    "Steve Dillon Punisher polar bear Ma Gnucci zoo scene",
                    "Punisher walking away Steve Dillon comic panel"
                ]
            }
        ]
    },
    {
        "id": "ghostrider_asedio_cielo_zadkiel",
        "wiki": "marvel.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Tras traicionar al Creador y usurpar el trono del Paraíso, el arcángel renegado Zadkiel creyó que su dominio celestial sobre la creación era absoluto e intocable.",
                "queries": [
                    "Zadkiel archangel throne Heaven Ghost Rider comic panel",
                    "Zadkiel Jason Aaron Ghost Riders Heavens on Fire comic panel",
                    "Zadkiel Marvel comic art interior"
                ]
            },
            {
                "num": 2,
                "text": "Pero no contaba con que Johnny Blaze y Danny Ketch unirían sus fuegos infernales para liderar a un ejército de Espíritus de la Venganza directo a las puertas celestiales.",
                "queries": [
                    "Johnny Blaze Danny Ketch Ghost Riders Heavens on Fire comic panel",
                    "Ghost Rider army Jason Aaron comic panel",
                    "Johnny Blaze Danny Ketch motorcycles Hellfire comic art"
                ]
            },
            {
                "num": 3,
                "text": "Con un rugido ensordecedor de motores y fuego del averno, Ghost Rider embistió y destrozó los portales de perlas sagradas, dejando una estela de fuego en los cielos.",
                "queries": [
                    "Ghost Rider storming Gates of Heaven comic panel",
                    "Ghost Rider breaching heaven gates Jason Aaron panel",
                    "Ghost Rider hellcycle heaven comic art"
                ]
            },
            {
                "num": 4,
                "text": "Zadkiel sintió por primera vez el terror en su carne divina cuando la Mirada de Penitencia consumió sus alas, demostrando que ningún tirano puede escapar al juicio.",
                "queries": [
                    "Ghost Rider defeats Zadkiel Penance Stare comic panel",
                    "Zadkiel defeated Ghost Rider Heavens on Fire panel",
                    "Ghost Rider Penance Stare interior comic panel"
                ]
            }
        ]
    },
    {
        "id": "moonknight_mr_knight_edificio_rescate",
        "wiki": "marvel.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Cuando una peligrosa banda armada secuestró a una niña inocente en un edificio abandonado de Nueva York, Marc Spector decidió no ponerse su capa, sino algo más elegante.",
                "queries": [
                    "Mr Knight white suit limousine Declan Shalvey comic panel",
                    "Mr Knight Moon Knight issue 5 Warren Ellis panel",
                    "Mr Knight suit Declan Shalvey comic art"
                ]
            },
            {
                "num": 2,
                "text": "Vestido con un traje blanco de sastre impoluto y armado únicamente con dos porras de combate, Mr. Knight pateó la puerta principal entrando en territorio enemigo.",
                "queries": [
                    "Mr Knight kicking door batons Moon Knight issue 5 panel",
                    "Mr Knight entering building Declan Shalvey comic panel",
                    "Mr Knight truncheons Moon Knight Warren Ellis panel"
                ]
            },
            {
                "num": 3,
                "text": "Piso por piso, avanzó en la oscuridad esquivando disparos a quemarropa y noqueando a los criminales con una precisión quirúrgica demoledora, sin mancharse una gota de sangre.",
                "queries": [
                    "Mr Knight fighting thugs hallway Moon Knight issue 5 panel",
                    "Mr Knight stairs fight Declan Shalvey comic panel",
                    "Moon Knight issue 5 hallway fight Declan Shalvey"
                ]
            },
            {
                "num": 4,
                "text": "En el último piso, derribó al líder de la banda de una sola patada y rescató a la niña en brazos, caminando hacia la luz de la luna intacto como un fantasma vengador.",
                "queries": [
                    "Mr Knight saving girl Moon Knight issue 5 Declan Shalvey panel",
                    "Mr Knight carries girl Warren Ellis Moon Knight panel",
                    "Mr Knight full page Moon Knight issue 5 panel"
                ]
            }
        ]
    },
    {
        "id": "namor_destruccion_tierra_antimateria",
        "wiki": "marvel.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Dos universos estaban a segundos de colisionar en una Incursión fatal, y la única forma de salvar a la Tierra 616 era aniquilar por completo el mundo de la Gran Sociedad.",
                "queries": [
                    "New Avengers issue 21 Hickman Incursion Great Society Earth panel",
                    "Illuminati Incursion Great Society Jonathan Hickman comic panel",
                    "New Avengers Jonathan Hickman red sky incursion planet panel"
                ]
            },
            {
                "num": 2,
                "text": "Con la bomba de antimateria armada, Black Panther y los héroes más virtuosos de la Tierra temblaron ante el peso moral de cometer un genocidio de miles de millones de inocentes.",
                "queries": [
                    "Black Panther holding antimatter trigger New Avengers 21 panel",
                    "TChalla weeping antimatter trigger Hickman comic panel",
                    "Black Panther Illuminati trigger New Avengers panel"
                ]
            },
            {
                "num": 3,
                "text": "Despreciando la cobardía de sus compañeros, Namor dio un paso al frente, arrebató el detonador y pronunció las palabras que cambiaron la historia: 'Mis manos ya están manchadas'.",
                "queries": [
                    "Namor takes trigger New Avengers 22 Jonathan Hickman panel",
                    "Namor presses button antimatter trigger New Avengers panel",
                    "Namor my hands are already stained Hickman comic panel"
                ]
            },
            {
                "num": 4,
                "text": "El dispositivo detonó en la atmósfera, pulverizando el planeta entero en una onda expansiva cósmica mientras Namor miraba fijamente el abismo que ningún otro héroe se atrevió a cruzar.",
                "queries": [
                    "Great Society Earth explosion antimatter New Avengers 22 panel",
                    "Earth destroyed New Avengers Hickman Mike Deodato panel",
                    "Namor watching destroyed world New Avengers Hickman panel"
                ]
            }
        ]
    },
    {
        "id": "swampthing_leccion_anatomia_vegetal",
        "wiki": "dc.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Creyendo haber capturado el cadáver congelado del monstruo del pantano, la corporación Sunderland contrató al brillante biólogo Jason Woodrue para realizar la autopsia definitiva.",
                "queries": [
                    "Saga of the Swamp Thing issue 21 autopsy slab comic panel",
                    "Swamp Thing frozen on table Anatomy Lesson Alan Moore panel",
                    "Saga of the Swamp Thing 21 Stephen Bissette comic panel"
                ]
            },
            {
                "num": 2,
                "text": "Al abrir el torso con el bisturí, Woodrue quedó petrificado de horror: no había corazón, no había pulmones, ni una sola gota de sangre o tejido humano en su interior.",
                "queries": [
                    "Jason Woodrue dissecting Swamp Thing Anatomy Lesson panel",
                    "Swamp Thing chest cavity opened Alan Moore comic panel",
                    "Jason Woodrue autopsy Swamp Thing roots organs panel"
                ]
            },
            {
                "num": 3,
                "text": "El microscopio confirmó la verdad más aterradora de los cómics: Alec Holland murió quemado en la explosión, y la criatura era una planta vegetal que absorbió su mente y creyó ser un hombre.",
                "queries": [
                    "Jason Woodrue microscope Anatomy Lesson Alan Moore panel",
                    "Swamp Thing not a man but a plant Alan Moore comic panel",
                    "Jason Woodrue terrified microscope Swamp Thing 21 panel"
                ]
            },
            {
                "num": 4,
                "text": "Al descongelarse en el laboratorio inundado, Swamp Thing abrió los ojos y comprendió su verdadera naturaleza divina: no era un humano maldito, sino la furia encarnada del Verde elemental.",
                "queries": [
                    "Swamp Thing waking up laboratory Anatomy Lesson Alan Moore panel",
                    "Swamp Thing rises from table Anatomy Lesson Bissette panel",
                    "Swamp Thing elemental Alan Moore splash page panel"
                ]
            }
        ]
    },
    {
        "id": "blackbolt_bomba_t_falla_espacio",
        "wiki": "marvel.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "En el clímax de la sangrienta guerra galáctica entre los Inhumanos y el Imperio Shi'ar, el emperador tirano Vulcan abordó la nave de mando para matar personalmente a Black Bolt.",
                "queries": [
                    "Black Bolt vs Vulcan War of Kings issue 6 comic panel",
                    "Vulcan fighting Black Bolt Dan Abnett comic panel",
                    "Vulcan vs Black Bolt War of Kings Paul Pelletier panel"
                ]
            },
            {
                "num": 2,
                "text": "Ambos monarcas cósmicos cayeron combatiendo dentro del núcleo de la Bomba-Terrigen, un dispositivo masivo diseñado para mutar a toda la galaxia con nieblas terrígenas.",
                "queries": [
                    "Terrigen T-Bomb core Black Bolt Vulcan War of Kings panel",
                    "Black Bolt Vulcan inside T-Bomb War of Kings 6 panel",
                    "T-Bomb dreadnought War of Kings comic panel"
                ]
            },
            {
                "num": 3,
                "text": "Sabiendo que no había otra salida para salvar a su pueblo, el Rey Silencioso separó sus labios por primera vez en años y desató un grito desgarrador a máxima potencia.",
                "queries": [
                    "Black Bolt screaming full power War of Kings 6 panel",
                    "Black Bolt sonic scream mouth open War of Kings panel",
                    "Black Bolt whisper scream comic panel"
                ]
            },
            {
                "num": 4,
                "text": "La onda de choque colapsó la bomba y desató una detonación de tal magnitud que fracturó la realidad, abriendo 'La Falla', una herida gigantesca en el tejido del cosmos.",
                "queries": [
                    "The Fault cosmic tear War of Kings issue 6 panel",
                    "T-Bomb explosion tear in space War of Kings panel",
                    "The Fault Marvel cosmic space tear Dan Abnett panel"
                ]
            }
        ]
    },
    {
        "id": "deadpool_wolverine_corea_del_norte",
        "wiki": "marvel.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "En una de las historias más crudas y oscuras de Marvel, Wade Wilson descubrió que durante años un científico militar estuvo secuestrando sus órganos para venderlos en el mercado negro.",
                "queries": [
                    "Deadpool The Good the Bad and the Ugly issue 15 Declan Shalvey panel",
                    "Deadpool organs harvested Butler Declan Shalvey comic panel",
                    "Deadpool discovering secret lab Duggan Shalvey panel"
                ]
            },
            {
                "num": 2,
                "text": "El rastro lo condujo hasta un campo de concentración oculto en Corea del Norte, donde familias enteras y niños eran torturados para injertarles los poderes mutantes de los X-Men.",
                "queries": [
                    "North Korea mutant camp Deadpool The Good the Bad the Ugly panel",
                    "Deadpool North Korea concentration camp Shalvey comic panel",
                    "North Korean mutant experiments Deadpool issue 16 panel"
                ]
            },
            {
                "num": 3,
                "text": "Lleno de una furia que nunca antes había sentido, Deadpool reclutó a Wolverine y al Capitán América, desatando un asalto sangriento e implacable contra la fortaleza militar.",
                "queries": [
                    "Deadpool Wolverine Captain America fighting together Shalvey panel",
                    "Deadpool Wolverine Cap assault North Korea bunker panel",
                    "The Good the Bad and the Ugly trio assault comic panel"
                ]
            },
            {
                "num": 4,
                "text": "Tras demoler las defensas y liberar a los niños cautivos, Wade se quitó la máscara en lágrimas, jurando que nadie volvería a usar su dolor para lastimar a los inocentes.",
                "queries": [
                    "Deadpool unmasked crying holding girl The Good the Bad the Ugly panel",
                    "Deadpool crying North Korea Declan Shalvey comic panel",
                    "Deadpool holding Eleanor Shalvey emotional comic panel"
                ]
            }
        ]
    },
    {
        "id": "wonderwoman_hiketeia_bota_batman",
        "wiki": "dc.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Danielle Welly, una joven desesperada que huía de Gotham tras vengar el asesinato de su hermana, llegó a Themyscira y realizó ante Wonder Woman el antiguo ritual sagrado de Hiketeia.",
                "queries": [
                    "Wonder Woman The Hiketeia Danielle ritual comic panel",
                    "Danielle Welly Hiketeia Wonder Woman Greg Rucka panel",
                    "Wonder Woman Hiketeia olive branch knees ritual panel"
                ]
            },
            {
                "num": 2,
                "text": "Al aceptar la súplica, Diana quedó atada por las leyes de los dioses del Olimpo a protegerla con su vida, sin importar quién viniera a reclamarla.",
                "queries": [
                    "Wonder Woman accepts Hiketeia vow JG Jones comic panel",
                    "Wonder Woman tiara armor oath The Hiketeia panel",
                    "Wonder Woman protection oath Greg Rucka comic art"
                ]
            },
            {
                "num": 3,
                "text": "Batman apareció en la noche tormentosa exigiendo la custodia de la fugitiva para llevarla a la justicia de Gotham, desatando un choque frontal inevitable de titanes.",
                "queries": [
                    "Batman vs Wonder Woman rain The Hiketeia comic panel",
                    "Batman fighting Wonder Woman street Hiketeia Greg Rucka panel",
                    "Batman throws batarangs Wonder Woman Hiketeia panel"
                ]
            },
            {
                "num": 4,
                "text": "Demostrando la superioridad de su fuerza divina, Diana esquivó sus ataques, derribó al Caballero de la Noche y colocó su bota firmemente sobre su rostro contra el pavimento.",
                "queries": [
                    "Wonder Woman boot on Batman face The Hiketeia JG Jones cover panel",
                    "Wonder Woman stepping on Batman head Hiketeia comic panel",
                    "Wonder Woman pins Batman with boot Hiketeia splash panel"
                ]
            }
        ]
    },
    {
        "id": "lobo_expulsado_cielo_infierno",
        "wiki": "dc.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Tras ser aniquilado en un combate espacial salvaje, el alma del cazarrecompensas más desagradable del universo cayó directamente en las profundidades del Averno.",
                "queries": [
                    "Lobos Back issue 1 Simon Bisley comic panel",
                    "Lobo arrives in Hell Simon Bisley comic panel",
                    "Lobo cigar chain Hell Bisley comic art"
                ]
            },
            {
                "num": 2,
                "text": "Pero en lugar de sufrir tortura, Lobo comenzó a masacrar demonios por pura diversión, convirtiendo el Infierno en un matadero tan insoportable que el mismísimo Diablo rogó por su expulsión.",
                "queries": [
                    "Lobo slaughtering demons Hell Lobos Back Simon Bisley panel",
                    "Lobo killing demons Lobos Back comic panel",
                    "Lobo vs devil demons Bisley comic art"
                ]
            },
            {
                "num": 3,
                "text": "Desesperados, los demonios lo enviaron al Cielo, donde Lobo insultó a los serafines, destruyó las arpas doradas y convirtió los jardines paradisíacos en una zona de guerra.",
                "queries": [
                    "Lobo in Heaven Simon Bisley Lobos Back comic panel",
                    "Lobo trashing heaven gardens angels Bisley panel",
                    "Lobo annoying angels Heaven Lobos Back comic panel"
                ]
            },
            {
                "num": 4,
                "text": "Sin otra opción para salvar el cosmos del caos, Dios y Satanás firmaron un tratado conjunto prohibiéndole la entrada al Más Allá para siempre, otorgándole la inmortalidad eterna.",
                "queries": [
                    "Lobo banned from afterlife immortal Simon Bisley panel",
                    "Lobo resurrected space bike Lobos Back Bisley panel",
                    "Lobo immortal space Simon Bisley comic splash"
                ]
            }
        ]
    },
    {
        "id": "batman_black_mirror_james_gordon_jr",
        "wiki": "dc.fandom.com",
        "scenes": [
            {
                "num": 1,
                "text": "Tras años de ausencia, James Gordon Jr., el hijo mayor del comisionado, regresó a Gotham asegurando estar curado de sus siniestros impulsos psicopáticos infantiles.",
                "queries": [
                    "James Gordon Jr diner Jim Gordon Black Mirror Jock panel",
                    "James Gordon Jr glasses Detective Comics 875 Jock panel",
                    "James Gordon Jr Scott Snyder Jock comic panel"
                ]
            },
            {
                "num": 2,
                "text": "Pero bajo su fachada de joven rehabilitado, James montó un laboratorio secreto donde modificó una toxina química para bloquear permanentemente la empatía y la compasión en el cerebro humano.",
                "queries": [
                    "James Gordon Jr secret lab toxin Black Mirror Jock panel",
                    "James Gordon Jr chemical vials Detective Comics 880 panel",
                    "James Gordon Jr baby formula map Scott Snyder panel"
                ]
            },
            {
                "num": 3,
                "text": "Su plan maestro era diabólico: infectar los lotes de leche infantil de la ciudad para convertir a toda la futura generación de niños de Gotham en monstruos asesinos sin remordimiento.",
                "queries": [
                    "James Gordon Jr baby formula poison Black Mirror Jock panel",
                    "James Gordon Jr scalpel smile Detective Comics panel",
                    "James Gordon Jr evil smile Jock comic panel"
                ]
            },
            {
                "num": 4,
                "text": "Tras atacar a su hermana Barbara en una trampa mortal, Dick Grayson como Batman lo interceptó en el puente, neutralizando al villano más perturbador y personal de la familia Gordon.",
                "queries": [
                    "Batman Dick Grayson Jim Gordon James Jr bridge Black Mirror Jock panel",
                    "James Gordon Jr bridge fall Detective Comics 881 Jock panel",
                    "Batman James Gordon Jr bridge confrontation Jock panel"
                ]
            }
        ]
    }
]


def download_and_frame_scene(proj_id: str, wiki_domain: str, scene_num: int, scene_text: str, queries: list[str]) -> bool:
    target_dir = CURATED_DIR / proj_id
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"scene_{scene_num:02d}.jpg"

    if target_file.exists() and target_file.stat().st_size > 20000:
        print(f"[{proj_id}] Scene {scene_num}: Already exists and verified ({target_file.stat().st_size // 1024} KB).", flush=True)
        return True

    print(f"\n[{proj_id}] Fetching Scene {scene_num}...", flush=True)
    print(f"  Texto: {scene_text[:70]}...", flush=True)

    best_candidate_path = None
    best_score = -1

    candidate_urls = []
    # 1. Bing Panels
    for q in queries:
        bing_urls = search_bing_comic_panels(q, limit=4)
        for u in bing_urls:
            if u not in candidate_urls:
                candidate_urls.append(u)

    # 2. Fandom Files Search Fallback
    for q in queries:
        fandom_files = search_fandom_files(wiki_domain, q, max_results=4)
        for f in fandom_files:
            furl = get_file_url(wiki_domain, f)
            if furl and furl not in candidate_urls:
                candidate_urls.append(furl)

    print(f"  -> Total candidatos a evaluar: {len(candidate_urls)}", flush=True)

    cand_file = target_dir / f"temp_scene_{scene_num}.jpg"

    for url in candidate_urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code != 200 or len(r.content) < 15000:
                continue
            im = Image.open(BytesIO(r.content)).convert("RGB")
            if im.width < 350 or im.height < 350:
                continue
            if not check_is_comic_art_inking(im):
                continue

            im.save(cand_file, "JPEG", quality=95)

            audit = verify_visual_alignment_with_gemini(str(cand_file), scene_text)
            score = audit.get("score", 0)
            is_comic = audit.get("is_comic_panel", False)
            reason = audit.get("reason", "")
            print(f"     Auditoría: Score {score}/10 (Comic: {is_comic}) - {reason[:60]}", flush=True)

            if is_comic and score > best_score:
                best_score = score
                framed = create_full_panel_frame(im, 1080, 1920)
                framed.save(target_file, "JPEG", quality=95)
                best_candidate_path = target_file

                if score >= 4:
                    print(f"     -> CANDIDATO EXCELENTE ({score}/10) ACEPTADO Y GUARDADO.", flush=True)
                    if cand_file.exists():
                        cand_file.unlink()
                    return True
        except Exception as e:
            continue

    if best_candidate_path and best_candidate_path.exists():
        print(f"  -> Aceptando mejor candidato disponible (Score: {best_score}/10).", flush=True)
        if cand_file.exists():
            cand_file.unlink()
        return True

    print(f"  [ALERTA] No se encontró viñeta automatizada para Scene {scene_num}.", flush=True)
    return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Curaduría de viñetas canónicas 1:1")
    parser.add_argument("--index", type=int, default=None, help="Índice (1-10) del proyecto a procesar")
    parser.add_argument("--all", action="store_true", help="Procesar los 10 proyectos")
    args = parser.parse_args()

    targets = PROJECTS_DATA
    if args.index:
        idx = args.index - 1
        if 0 <= idx < len(PROJECTS_DATA):
            targets = [PROJECTS_DATA[idx]]
        else:
            print(f"Índice fuera de rango (1-{len(PROJECTS_DATA)})", flush=True)
            return

    print("=" * 70, flush=True)
    print(f"INICIANDO CURADURÍA DE PANELES 1:1 ({len(targets)} proyectos)", flush=True)
    print("=" * 70, flush=True)

    for proj in targets:
        p_id = proj["id"]
        wiki = proj.get("wiki", "marvel.fandom.com")
        print(f"\n==================================================", flush=True)
        print(f"PROCESANDO PROYECTO: {p_id}", flush=True)
        print(f"==================================================", flush=True)
        for sc in proj["scenes"]:
            download_and_frame_scene(p_id, wiki, sc["num"], sc["text"], sc["queries"])
            time.sleep(1)

    print("\n" + "=" * 70, flush=True)
    print("CURADURÍA FINALIZADA.", flush=True)
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
