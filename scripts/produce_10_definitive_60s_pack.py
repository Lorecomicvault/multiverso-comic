"""
Master Production Engine: 10 Videos Virales Inéditos de 60 Segundos (100% Nuevos)
================================================================================
Formato: 1080x1920 (Vertical 9:16 para Shorts, Reels y TikTok)
Duración: 58 a 60 segundos exactos por video
Visuales: 100% Viñetas canónicas curadas auténticas sincronizadas 1:1 con la narración
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
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.pipeline import run_pipeline
from src.composer import get_duration

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_10_nuevos_virales_60s"
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"

PROJECTS = [
    {
        "id": "01_wonder_woman_ceguera_medusa",
        "title": "Wonder Woman: El Sacrificio Ciego Contra Medusa",
        "character": "Wonder Woman",
        "folder": "wonder_woman_ceguera_medusa",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Resucitada por la hechicera Circe en medio de un coliseo moderno abarrotado, la temible Gorgona Medusa desafió a Wonder Woman a un duelo a muerte transmitido en vivo ante la mirada aterrada de todo el planeta."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con miles de inocentes como rehenes, Diana de Themyscira descendió a la arena sabiendo que el más mínimo reflejo en los ojos de Medusa convertiría su carne amazona en estatua de piedra sólida para siempre."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sabiendo que no podría vencer con la mirada descubierta, Diana tomó una decisión desgarradora: agarró una serpiente venenosa viva y frotó su letal fluido directamente sobre sus pupilas, quemando su vista en una agonía indescriptible."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Completamente ciega y guiándose únicamente por las vibraciones del aire y su instinto guerrero milenario, la princesa amazona esquivó las garras de la Gorgona y cercenó su cabeza de un solo tajo de espada."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Alzando el trofeo sangriento en alto, Wonder Woman demostró que el verdadero poder de un héroe no reside en sus ojos, sino en la inquebrantable pureza de su alma. ¿Fue este su sacrificio más glorioso?"
            }
        ],
        "description": "El día en que Wonder Woman se arrancó la vista con veneno de serpiente para decapitar a Medusa y salvar a miles de inocentes. La hazaña más heroica de DC Comics.",
        "hashtags": "#WonderWoman #Medusa #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "02_constantine_triunvirato_infierno",
        "title": "Constantine: La Gran Estafa a los Reyes del Infierno",
        "character": "John Constantine",
        "folder": "constantine_triunvirato_infierno",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Desahuciado por los médicos y tosiendo sangre por un cáncer de pulmón terminal incurable, el detective de lo oculto John Constantine descubrió que solo le quedaban escasos días de vida antes de ser arrastrado al averno."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Consciente de que su alma era la más codiciada por las tinieblas, visitó en secreto a los tres gobernantes absolutos del inframundo: el Primer Caído, Azazel y Beelzebub, ofreciéndole su alma a cada uno por separado."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sin que ninguno supiera del otro, los tres reyes infernales firmaron el pacto prohibido, creyendo que por fin poseían el alma del mago más escurridizo de la Tierra, sellando sin saberlo su propia trampa legal."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al llegar la hora fatal, Constantine aceleró su muerte y los tres señores se manifestaron en su habitación. Al verse cara a cara, descubrieron la triple estafa que desataría una guerra civil cósmica por su alma."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Para evitar que el Infierno entero se autodestruyera, Lucifer no tuvo más opción que extirparle el cáncer milagrosamente y devolverle la vida. Constantine encendió un cigarro, burlándose en la cara de los señores del abismo."
            }
        ],
        "description": "John Constantine engañó a Lucifer, Azazel y Beelzebub vendiendo su alma tres veces para obligarlos a curarle el cáncer terminal. La mayor estafa al Infierno.",
        "hashtags": "#JohnConstantine #Hellblazer #DCComics #Vertigo #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "03_spiderman_vs_juggernaut",
        "title": "Spider-Man vs Juggernaut: La Trampa de Hormigón Líquido",
        "character": "Spider-Man",
        "folder": "spiderman_vs_juggernaut",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Un coloso imparable de fuerza ilimitada caminó en línea recta por las calles de Manhattan, demoliendo rascacielos, tanques policiales y edificios enteros sin que ninguna fuerza del planeta fuera capaz de frenar su avance."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Enviado por Black Tom Cassidy para capturar los poderes psíquicos de la clarividente Madame Web, Juggernaut atravesó los muros blindados de su apartamento ignorando con desprecio cada golpe de Spider-Man."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Desesperado por proteger a la anciana, Peter Parker desató todo su ingenio: le arrojó encima grúas de construcción enteras y lo electrocutó con cables de alto voltaje, pero el monstruo ni siquiera pestañeó."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al borde de la asfixia, Spider-Man saltó sobre la gigantesca espalda del titán y disparó telarañas directas a las ranuras de su casco blindado, cegándolo por completo para obligarlo a caminar hacia una zona de obras."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Juggernaut dio un paso en falso y cayó en un foso de cemento líquido de doce metros de profundidad que se solidificó al instante, sepultando a la bestia bajo toneladas de roca. ¿Fue esta la hazaña más épica de Spidey?"
            }
        ],
        "description": "¡Nada puede detener al Juggernaut! Excepto el ingenio de Spider-Man enterrándolo en doce metros de cemento líquido para salvar a Madame Web.",
        "hashtags": "#SpiderMan #Juggernaut #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "04_nova_annihilus_desgarro",
        "title": "Nova vs Annihilus: El Despiadado Desgarro Cósmico",
        "character": "Nova",
        "folder": "nova_annihilus_desgarro",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Surgiendo desde las profundidades oscuras de la Zona Negativa, la Ola de Aniquilación arrasó galaxias completas, devorando civilizaciones y masacrando a billones de seres vivos sin que nada pudiera detenerla."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El despiadado señor insectoide Annihilus destruyó la capital dorada de Xandar y exterminó al legendario Cuerpo Nova, dejando al joven terrestre Richard Rider como el último guardián superviviente de la galaxia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cargando con la totalidad de la mente colectiva del Worldmind y toda la Nova Force cósmica fluyendo por sus venas, Richard Rider lideró el Frente Unido lanzándose en una misión suicida final."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En una colisión salvaje cuerpo a cuerpo en el vacío espacial, Nova clavó su puño directo por las fauces de Annihilus y tiró con toda su fuerza, arrancándole las entrañas de adentro hacia afuera en un acto sangriento definitivo."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Sosteniendo el cadáver despedazado del tirano cósmico y despojándolo de la Barra de Control, Nova salvó al universo entero demostrando hasta dónde llega la voluntad de un verdadero protector de las estrellas."
            }
        ],
        "description": "Richard Rider le arrancó las entrañas a Annihilus desde adentro para vengar al Cuerpo Nova y salvar al universo entero. El momento más salvaje de Annihilation.",
        "hashtags": "#Nova #Annihilus #Annihilation #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "05_red_goblin_osborn_carnage",
        "title": "Red Goblin: La Fusión de Norman Osborn y Carnage",
        "character": "Norman Osborn",
        "folder": "red_goblin_osborn_carnage",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Desesperado tras perder los poderes del suero del Duende Verde y obsesionado con destruir a Peter Parker, Norman Osborn asaltó las instalaciones secretas para apoderarse del simbionte más sanguinario: Carnage."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al fusionar su mente psicópata con el simbionte alienígena, nació el Duende Rojo: un monstruo imparable con la astucia mortal de Osborn y la ferocidad sádica de Carnage, completamente inmune al fuego y al sonido."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Desatando el pánico absoluto en Manhattan, infectó a su propio nieto con microduendes simbióticos para obligarlo a matar y atacó a los seres queridos de Spider-Man en una noche de pesadilla sin escape."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Viendo a sus aliados caer, Spider-Man tomó una medida desesperada: se unió al simbionte Venom para igualar el poder de la bestia, provocando el orgullo de Osborn para forzarlo a luchar sin la criatura."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Tras un brutal combate final, el Duende Rojo fue despojado, pero el trauma neuronal destruyó la mente de Norman para siempre, dejándolo encerrado en Ravencroft creyendo que él es el verdadero Cletus Kasady."
            }
        ],
        "description": "La pesadilla carmesí: Norman Osborn fusionado con Carnage para crear al Duende Rojo, inmune al fuego y las ondas sonoras. El clímax de Dan Slott.",
        "hashtags": "#RedGoblin #Carnage #SpiderMan #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "06_flash_human_race",
        "title": "The Flash: Más Rápido que la Teletransportación Instantánea",
        "character": "The Flash",
        "folder": "flash_human_race",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Unos colosales seres interdimensionales conocidos como los Apostadores Cósmicos llegaron a nuestro sector amenazando con desintegrar la Tierra si su campeón, The Flash, perdía una carrera a través del universo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El desafío era una trampa matemática mortal: el contrincante alienígena no corría, sino que poseía teletransportación instantánea, haciendo inútil cualquier velocidad física conocida en las leyes del espacio y tiempo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Wally West contactó a cada ser humano de la Tierra mediante Krakkl y les pidió que corrieran todos a la vez. Absorbiendo la energía cinética de seis mil millones de personas, Flash superó la velocidad trans-temporal."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Quebrando el tiempo de Planck, Flash cruzó la línea de meta en un tiempo negativo, llegando a su destino una fracción de segundo antes de que la teletransportación instantánea se materializara, salvando al planeta entero."
            }
        ],
        "description": "Wally West rompió la física: corrió más rápido que la teletransportación instantánea absorbiendo la energía cinética de toda la humanidad. The Human Race.",
        "hashtags": "#TheFlash #WallyWest #DCComics #SpeedForce #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "07_saint_walker_linterna_azul",
        "title": "Saint Walker: La Esperanza que Salvó a Hal Jordan",
        "character": "Saint Walker",
        "folder": "saint_walker_linterna_azul",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Bajo el sol moribundo de su mundo natal Astonia, un pacífico habitante llamado Bro'Dee Walker perdió a toda su familia en un trágico cataclismo, pero se negó a rendirse ante la desesperación cósmica."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Guiado por una fe inquebrantable, escaló la montaña sagrada donde los Guardianes Ganthet y Sayd lo consagraron como el Primer Linterna Azul del cosmos, empuñando la luz pura de la Esperanza."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cuando Hal Jordan fue capturado en el planeta de fuego Ysmault y consumido por la sangre rabiosa de los Red Lanterns, Saint Walker descendió en medio del combate para realizar un milagro divino."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Colocando un anillo azul en la mano de Jordan y susurrando con amor ¡Todo estará bien!, la luz de la esperanza neutralizó el veneno de la ira, arrancando el anillo rojo sin detener su corazón."
            },
            {
                "scene_number": 5,
                "file": "scene_05.jpg",
                "text": "Demostró ante el cosmos que la esperanza es el motor que enciende la voluntad, supercargando las baterías verdes al doscientos por ciento para salvar a los héroes de la oscuridad absoluta."
            }
        ],
        "description": "¡Todo estará bien! Bro'Dee Walker se convirtió en el primer Linterna Azul y salvó el corazón de Hal Jordan de la ira roja. La luz de la esperanza.",
        "hashtags": "#SaintWalker #GreenLantern #BlueLantern #DCComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "08_shazam_billy_batson_relampago_dioses",
        "title": "Shazam: El Huérfano y el Relámpago de los Dioses",
        "character": "Shazam",
        "folder": "shazam_billy_batson_relampago_dioses",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Vagando solo y abandonado por las frías calles de la ciudad, el pequeño huérfano Billy Batson sobrevivía en las estaciones del metro, manteniendo su bondad intacta pese a la crueldad del mundo moderno."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Una noche misteriosa, un tren subterráneo desprovisto de conductor abrió sus puertas mágicas y lo transportó a través de dimensiones ocultas hasta la milenaria y cavernosa Roca de la Eternidad."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Frente al trono de piedra de los siete pecados capitales, el anciano Mago Shazam examinó el corazón del niño y decidió heredarle el poder absoluto de Salomón, Hércules, Atlas, Zeus, Aquiles y Mercurio."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al pronunciar con valentía la palabra sagrada ¡SHAZAM!, un relámpago divino descendió de los cielos transformando al indefenso niño en el Campeón Supremo de la magia, protector eterno de la Tierra."
            }
        ],
        "description": "El origen místico del Campeón de la Magia: Billy Batson en la Roca de la Eternidad y el relámpago sagrado de los seis dioses inmortales. ¡SHAZAM!",
        "hashtags": "#Shazam #BillyBatson #DCComics #CaptainMarvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "09_zatanna_magia_inversa_conjuro_sombras",
        "title": "Zatanna: El Poder Prohibido de la Magia Inversa",
        "character": "Zatanna",
        "folder": "zatanna_magia_inversa_conjuro_sombras",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Heredera del legendario linaje de los Homo Magi y de su padre Giovanni Zatara, Zatanna creció deslumbrando a multitudes en los teatros de Gotham como la ilusionista más elegante y aclamada del mundo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero cuando entidades oscuras y demonios de pesadilla intentan romper la frontera dimensional para devorar a los inocentes, Zatanna abandona el truco teatral para desatar la verdadera magia primordial de la creación."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pronunciando cada conjuro en orden inverso, las palabras mágicas doblan las leyes de la física, congelando el tiempo, encadenando sombras infernales y transmutando la realidad misma con una sola orden hablada."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Ajustando su sombrero de copa y empuñando su varita de plata, Zatanna destierra a los monstruos al abismo con una sonrisa confiada, protegiendo el multiverso con el poder de su voz."
            }
        ],
        "description": "Zatanna y el misterio del lenguaje inverso: cuando hablar al revés dobla las leyes de la física y expulsa a los demonios del multiverso.",
        "hashtags": "#Zatanna #JusticeLeagueDark #DCComics #Magic #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "10_moon_knight_manicomio_khonshu_lemire",
        "title": "Moon Knight: El Manicomio de Khonshu y las Mentes de Marc Spector",
        "character": "Moon Knight",
        "folder": "moon_knight_manicomio_khonshu_lemire",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Marc Spector despertó atado con una camisa de fuerza en las celdas asépticas del hospital psiquiátrico New Bain, golpeado por enfermeros brutales y rodeado de pacientes que parecían antiguos aliados de guerra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "La directora del asilo, la doctora Emmet, intentó convencerlo con terapias de shock de que su vida como vigilante enmascarado y sus dioses egipcios eran solo delirios provocados por su grave trastorno de identidad disociativo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero al mirar fijamente a través de las ventanas bajo la luna llena, Marc descubrió la aterradora verdad: todo el hospital era una ilusión mágica y el personal médico eran sirvientes momificados de la deidad Ammit."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Desgarrando sus ataduras con furia mística y unificando sus mentes fracturadas, Marc abrazó el poder del Dios Khonshu para recuperar su armadura blanca y escapar del manicomio de dioses."
            }
        ],
        "description": "Marc Spector encerrado en un psiquiátrico donde los doctores son demonios egipcios de Ammit. La obra maestra psicológica de Moon Knight por Jeff Lemire.",
        "hashtags": "#MoonKnight #MarcSpector #Khonshu #MarvelComics #Marvel #Comics #Shorts #Reels #TikTok"
    }
]

def build_single_video(proj: dict, output_dir: Path):
    proj_id = proj["id"]
    title = proj["title"]
    folder_name = proj["folder"]
    scenes = proj["scenes"]
    
    video_out_dir = output_dir / proj_id
    video_out_dir.mkdir(parents=True, exist_ok=True)
    
    # Verificacion de existencia previa
    existing_mp4s = [f for f in video_out_dir.glob("*.mp4") if not f.name.startswith("scene_")]
    meta_path = video_out_dir / "metadata.json"
    if existing_mp4s and meta_path.exists():
        final_cand = existing_mp4s[0]
        if final_cand.stat().st_size > 5_000_000:
            dur = get_duration(str(final_cand))
            print(f"[SKIP] Video {proj_id} ya existe y es valido: {final_cand.name} ({dur:.1f}s)")
            return str(final_cand)

    print(f"\n=======================================================")
    print(f"[PROCESANDO {proj_id}]: {title}")
    print(f"=======================================================")
    
    curated_folder = CURATED_BASE / folder_name
    if not curated_folder.exists():
        raise FileNotFoundError(f"Carpeta curada no encontrada: {curated_folder}")
        
    scene_videos = []
    script_scenes = []
    
    for sc in scenes:
        sn = sc["scene_number"]
        img_name = sc["file"]
        src_img = curated_folder / img_name
        if not src_img.exists():
            raise FileNotFoundError(f"Imagen de escena no encontrada: {src_img}")
            
        scene_dir = video_out_dir / f"scene_{sn:02d}"
        scene_dir.mkdir(parents=True, exist_ok=True)
        dst_img = scene_dir / f"scene_{sn:02d}.jpg"
        shutil.copy2(src_img, dst_img)
        
        scene_videos.append({
            "scene_number": sn,
            "video": str(dst_img),
            "is_image": True,
            "visual_guide": f"Panel {sn} de {title}"
        })
        
        script_scenes.append({
            "scene_number": sn,
            "voiceover_text": sc["text"],
            "narration": sc["text"],
            "visual_guide": f"Panel {sn} de {title}"
        })
        
    generation = {
        "path": str(video_out_dir),
        "scene_videos": scene_videos,
        "script": {
            "metadata": {"title": title},
            "scenes": script_scenes
        }
    }
    
    final_video = run_pipeline(
        generation=generation,
        output_name=proj_id,
        voice="es-MX-JorgeNeural",
        output_root=str(video_out_dir / "build"),
        width=1080,
        height=1920,
        final_video_dir=str(video_out_dir),
        generate_thumbnail=True
    )
    
    dur = get_duration(final_video)
    print(f"[DURACION FINAL] {proj_id} -> {dur:.2f} segundos")
    
    meta_path = video_out_dir / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "id": proj_id,
            "title": title,
            "character": proj["character"],
            "description": proj["description"],
            "hashtags": proj["hashtags"],
            "scenes": [s["text"] for s in scenes],
            "video_file": os.path.basename(final_video),
            "duration_seconds": dur,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2, ensure_ascii=False)
        
    print(f"[OK] Video {proj_id} completado con éxito: {final_video}")
    return final_video

def main():
    PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    completed_videos = []
    
    print(f"Iniciando Renderizado del Pack de 10 Videos Nuevos (60s) en: {PACK_OUTPUT_DIR}")
    start_time = time.time()
    
    for idx, proj in enumerate(PROJECTS, 1):
        print(f"\n>>> INICIANDO VIDEO {idx} DE {len(PROJECTS)}: {proj['id']} <<<")
        try:
            v_path = build_single_video(proj, PACK_OUTPUT_DIR)
            dur = get_duration(v_path)
            completed_videos.append((proj, v_path, dur))
        except Exception as e:
            print(f"[ERROR] generando video {proj['id']}: {e}")
            import traceback
            traceback.print_exc()

    total_time = time.time() - start_time
    print(f"\n=======================================================")
    print(f"RESUMEN FINAL: {len(completed_videos)}/10 Videos Renderizados con Éxito")
    print(f"Tiempo Total de Procesamiento: {total_time/60:.2f} minutos")
    print(f"=======================================================")
    for proj, v_path, dur in completed_videos:
        print(f" - [{dur:.1f}s] {proj['id']}: {os.path.basename(v_path)}")

if __name__ == "__main__":
    main()
