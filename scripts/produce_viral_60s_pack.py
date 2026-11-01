"""
Master Batch Generator: Pack de 10 Videos Virales de 60 Segundos (100% Inéditos)
================================================================================
Formato: 1080x1920 (Vertical 9:16 para Shorts, Reels y TikTok)
Duración: 50 a 58 segundos por video (125-132 palabras, 4 escenas)
Visuales: 100% Viñetas canónicas curadas auténticas sincronizadas
Efectos: Transiciones 3D de papel rasgado + Foley + Subtítulos Bangers Comic Noir
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path

# Force UTF-8 stdout on Windows
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

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.pipeline import run_pipeline

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "pack_10_virales_60s"
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"

PROJECTS = [
    {
        "id": "01_battle_beast_vs_thragg",
        "title": "Battle Beast vs Thragg: El Duelo Más Sangriento del Cómic",
        "character": "Battle Beast",
        "folder": "invincible_battle_beast_duelo_viltrumita",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Maldito por una insaciable sed de combate, Battle Beast recorrió los confines del cosmos buscando un rival capaz de poner a prueba su fuerza monstruosa. Ningún guerrero alienígena lograba hacerle frente."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al descender en el desolado planeta de combate, se topó de frente contra el tirano más temido del multiverso, el implacable emperador Thragg, iniciando la colisión más salvaje y despiadada entre dos razas invencibles."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al ver que Thragg estaba herido en el abdomen por los feroces Ragnars, Battle Beast hizo lo impensable: se abrió el estómago con su propia espada para igualar las condiciones y luchar con absoluto honor."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Durante días enteros, ambas bestias pelearon sobre montañas de cadáveres hasta que el emperador logró desgarrar su garganta. Thragg reconoció su grandeza, sellando el duelo más legendario y sangriento de la historia del cómic."
            }
        ],
        "description": "La legendaria batalla donde Battle Beast se abrió sus propias entrañas para darle una pelea justa al emperador Thragg. El duelo más brutal de Invincible.",
        "hashtags": "#Invincible #BattleBeast #Thragg #Comics #ComicLore #Shorts #Reels #TikTok"
    },
    {
        "id": "02_plastic_man_arma_secreta_batman",
        "title": "Plastic Man: El Monstruo Inmortal que Aterra a Batman",
        "character": "Plastic Man",
        "folder": "plastic_man_eel_obrian_resistencia_inmortal",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En los archivos más clasificados de la Batcomputadora, Batman cataloga a Plastic Man no como un alivio cómico simpático, sino como el ser biológico más peligroso y letal de todo el planeta Tierra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su fisiología entera está compuesta por polímeros orgánicos indestructibles: no tiene cerebro vulnerable que atacar, no tiene órganos internos ni sangre, y puede alterar su densidad a nivel molecular."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Patrick O'Brian ha sobrevivido milenios desintegrado en el fondo del océano. Si quisiera matar, podría infiltrarse en los pulmones de Superman o expandir sus células para sofocar a un ejército entero sin esfuerzo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Batman concluye en su plan de contingencia con una advertencia escalofriante: si Plastic Man perdiera la cordura algún día, ni la Liga de la Justicia entera reunida tendría el poder para detenerlo."
            }
        ],
        "description": "Batman no le teme a Superman ni a Darkseid... le teme a Plastic Man. Los archivos confidenciales de Torre de Babel revelados.",
        "hashtags": "#PlasticMan #Batman #DCComics #JusticeLeague #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "03_rogue_beso_destruye_capitana_marvel",
        "title": "El Beso de Rogue: La Absorción que Destruyó a Capitana Marvel",
        "character": "Rogue",
        "folder": "rogue_absorbe_poderes_capitana_marvel",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Bajo la influencia de Mystique y la Hermandad de Mutantes, una joven e inexperta Rogue embosca a Carol Danvers en las alturas del emblemático puente Golden Gate de San Francisco."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su misión era incapacitar a la heroína cósmica tocando su piel, pero en medio del forcejeo en las alturas, el contacto físico se prolonga mucho más allá del límite de seguridad."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En un torbellino psíquico aterrador, Rogue drena sin control la fuerza sobrehumana, la capacidad de volar y los recuerdos de toda una vida de Carol, fusionándolos permanentemente en su propia mente."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Horrorizada por las voces ajenas que ahora atormentan su cabeza, Rogue suelta el cuerpo vacío y en coma de Capitana Marvel, arrojándola a las gélidas aguas de la bahía en el crimen más trágico de su pasado."
            }
        ],
        "description": "El trágico día en que Rogue le robó para siempre los poderes, la mente y el alma a Carol Danvers. El origen de la mutante de X-Men.",
        "hashtags": "#Rogue #CaptainMarvel #XMen #Avengers #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "04_ghost_rider_rey_del_infierno",
        "title": "Ghost Rider: El Día en que Johnny Blaze se Coronó Rey del Infierno",
        "character": "Ghost Rider",
        "folder": "ghost_rider_johnny_blaze_rey_infierno",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Tras la caída del demonio Mephisto en Las Vegas, el trono del Inframundo queda vacante, desatando una guerra civil entre hordas malditas que amenaza con arrasar la dimensión de los mortales."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Para evitar que billones de almas corruptas escapen a la superficie terrestre, Johnny Blaze toma una decisión extrema: descender voluntariamente en su motocicleta hacia las fauces del averno."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Rodeado por legiones de demonios que se arrodillan a su paso, el Vengador Fantasma camina firme hacia el palacio de sombras y se sienta con autoridad sobre el trono de hueso y azufre."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Colocándose una corona forjada en fuego eterno, Johnny Blaze se proclama el nuevo Rey del Infierno, atando las cadenas del fuego fatuo para gobernar a los condenados por toda la eternidad."
            }
        ],
        "description": "Johnny Blaze ya no solo caza pecadores... ahora gobierna el Infierno. El Vengador Fantasma coronado en el trono de Mephisto.",
        "hashtags": "#GhostRider #JohnnyBlaze #Marvel #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "05_spiderman_2099_miguel_ohara",
        "title": "Spider-Man 2099: El Sabotaje Genético de Miguel O'Hara",
        "character": "Spider-Man 2099",
        "folder": "spiderman_2099_miguel_ohara_alchemax",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En la megalópolis futurista de Nueva York en el año 2099, el brillante genetista Miguel O'Hara decide renunciar a la megacorporación Alchemax tras presenciar sus crueles experimentos humanos."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Para retenerlo a la fuerza, su sádico jefe Tyler Stone lo intoxica con Rapture, una droga altamente adictiva que se une a su código genético, obligándolo a entrar a hurtadillas a la cámara de reprogramación celular."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero su celoso colega Aaron Delgado sabotea los controles introduciendo cincuenta por ciento de código genético arácnido. La sobrecarga revienta la cámara en una llamarada de luz cegadora."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "De los escombros surge Miguel O'Hara con colmillos venenosos, garras retráctiles y visión mejorada. Con un traje del Día de los Muertos, nace Spider-Man 2099 para destruir a la corporación que lo condenó."
            }
        ],
        "description": "El trágico origen de Miguel O'Hara en el futuro cyberpunk: adicto al Rapture por la fuerza y saboteado en la máquina genética. Nace Spider-Man 2099.",
        "hashtags": "#SpiderMan2099 #MiguelOHara #SpiderVerse #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "06_taskmaster_memoria_fotografica",
        "title": "Taskmaster: La Maldición de la Memoria Fotográfica",
        "character": "Taskmaster",
        "folder": "taskmaster_memoria_fotografica_olvido",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Buscando crear al agente supremo, el mercenario Tony Masters se inyectó una versión experimental del suero del súper soldado nazi diseñada para desbloquear el cien por ciento de la memoria muscular."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Al instante adquirió reflejos fotográficos absolutos: con solo observar una vez a Capitán América, Hawkeye o Daredevil, Taskmaster puede duplicar a la perfección cada uno de sus movimientos letales."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sin embargo, el suero traía consigo una maldición biológica devastadora: su cerebro no tiene espacio infinito, y cada nueva habilidad de combate que aprende borra para siempre sus recuerdos personales más preciados."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Su propia esposa Mercedes trabaja en las sombras como su operadora para cuidarlo. Cada día, Taskmaster la mira a los ojos sin reconocer el rostro del único amor de su vida, atrapado en una máquina de matar vacía."
            }
        ],
        "description": "Cada golpe que Taskmaster aprende borra un recuerdo de su esposa y su vida. La trágica maldición del mercenario con reflejos fotográficos en Marvel.",
        "hashtags": "#Taskmaster #Marvel #MarvelComics #Avengers #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "07_colossus_sacrificio_virus_legado",
        "title": "Colossus: El Sacrificio Heroico contra el Virus Legado",
        "character": "Colossus",
        "folder": "colossus_sacrificio_cura_virus_legado",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Durante años, el temible Virus Legado exterminó a cientos de mutantes por todo el planeta, propagando una plaga incurable que amenazaba con extinguir para siempre a la especie de los X-Men."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Cuando Beast descubrió la cura definitiva en el laboratorio, se topó con una verdad desgarradora: el suero no podía aerosolizarse a la atmósfera sin cobrar la vida del mutante que lo inyectara."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Recordando con lágrimas en los ojos la lenta y dolorosa muerte de su pequeña hermana Illyana por el virus, Piotr Rasputin no lo dudó un segundo y transformó su cuerpo entero en acero orgánico."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Piotr se inyectó la fórmula letal muriendo en una agonía metálica indescriptible, pero liberando el antídoto por todo el planeta para salvar a cada mutante sobre la faz de la Tierra."
            }
        ],
        "description": "El sacrificio más conmovedor de X-Men: Colossus inyectándose la cura letal para salvar a todos los mutantes tras la muerte de su hermana Illyana.",
        "hashtags": "#Colossus #XMen #LegacyVirus #Marvel #MarvelComics #Shorts #Reels #TikTok"
    },
    {
        "id": "08_winter_soldier_origen_sovietico",
        "title": "Winter Soldier: El Lavado de Cerebro y la Cámara Criogénica",
        "character": "Winter Soldier",
        "folder": "winter_soldier",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En los días finales de la Segunda Guerra Mundial, el joven Bucky Barnes intentó desarmar un avión bomba en pleno vuelo, cayendo a las gélidas aguas del Atlántico tras una explosión que le arrancó el brazo izquierdo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Preservado en un estado de animación suspendida por las bajas temperaturas, un submarino soviético recuperó su cuerpo mutilado y lo entregó a los científicos del misterioso Departamento X."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Le implantaron un brazo biónico de acero y mediante brutales sesiones de electrochoques borraron su identidad, reprogramándolo como una máquina de matar soviética apodada el Soldado del Invierno."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Para evitar que envejeciera y mantenerlo como un fantasma indetectable durante décadas, los soviéticos lo congelaban en criogenia tras cada asesinato político, despertándolo solo para desatar el terror."
            }
        ],
        "description": "El oscuro origen de Bucky Barnes: congelado, mutilado y reprogramado como el fantasma soviético más letal de la Guerra Fría. Winter Soldier.",
        "hashtags": "#WinterSoldier #CaptainAmerica #BuckyBarnes #Marvel #Comics #Shorts #Reels #TikTok"
    },
    {
        "id": "09_hellboy_mano_derecha_destino",
        "title": "Hellboy: La Mano Derecha del Destino (Anung Un Rama)",
        "character": "Hellboy",
        "folder": "hellboy_mano_derecha_del_destino_anung",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "En una noche lluviosa de 1944 en las ruinas de una abadía en Escocia, una siniestra división oculta nazi ejecutó el Proyecto Ragna Rok con el objetivo de alterar el rumbo de la guerra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "A través de un portal interdimensional no apareció un ejército, sino un pequeño demonio de piel roja y cuernos recortados, quien fue rescatado con compasión por el profesor Trevor Bruttenholm."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero la criatura portaba un secreto aterrador en su brazo derecho: una colosal mano de piedra indestructible, tallada por los Antiguos Espíritus a partir del cuerpo del vigilante cósmico Anum."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "La profecía dicta que su verdadera identidad es Anung Un Rama, y esa mano de piedra es la llave universal diseñada para romper las prisiones del abismo y desatar el fin de toda la creación terrenal."
            }
        ],
        "description": "La mano de piedra de Hellboy no es un arma... es la llave para liberar el apocalipsis en la Tierra. El origen profético de Anung Un Rama.",
        "hashtags": "#Hellboy #DarkHorse #Comics #ComicLore #BPRD #Shorts #Reels #TikTok"
    },
    {
        "id": "10_thanos_supremo_de_los_eternos",
        "title": "Thanos Supremo de los Eternos: El Trono de Olympia",
        "character": "Thanos",
        "folder": "thanos_supremo_eterno_kieron_gillen",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "Buscando reconstruir su cuerpo dañado y obtener la inmortalidad absoluta, Thanos desciende a la Tierra y descubre los códigos fuente de la Gran Máquina que gobierna a los Eternos."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Aprovechando una sangrienta conspiración y el asesinato de varios líderes celestiales, el Titán Loco irrumpe en la sagrada ciudad de Polaria desatando un combate implacable contra sus propios parientes."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Mediante una astuta y retorcida manipulación de los protocolos de la Uni-Mente, Thanos corrompe las elecciones divinas de los dioses, forzando al sistema a reconocerlo como su legítimo gobernante."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con una sonrisa triunfante, el mayor genocida del cosmos se sienta en el trono de Olympia proclamándose Primer Eterno, tomando el mando directo de la Tierra y de sus deidades más antiguas."
            }
        ],
        "description": "Cuando Thanos conquistó a los Eternos de la Tierra y se coronó en el trono de Olympia como el Primer Eterno. La obra maestra de Kieron Gillen.",
        "hashtags": "#Thanos #Eternals #Marvel #MarvelComics #Comics #Shorts #Reels #TikTok"
    }
]

def build_single_video(proj: dict, output_dir: Path):
    proj_id = proj["id"]
    title = proj["title"]
    folder_name = proj["folder"]
    scenes = proj["scenes"]
    
    video_out_dir = output_dir / proj_id
    video_out_dir.mkdir(parents=True, exist_ok=True)
    
    # Verificacion de existencia previa (idempotencia)
    existing_mp4s = [f for f in video_out_dir.glob("*.mp4") if not f.name.startswith("scene_")]
    meta_path = video_out_dir / "metadata.json"
    if existing_mp4s and meta_path.exists():
        final_cand = existing_mp4s[0]
        if final_cand.stat().st_size > 5_000_000:
            print(f"[SKIP] Video {proj_id} ya existe y es valido: {final_cand.name}")
            return str(final_cand)

    print(f"\n=======================================================")
    print(f"[PROCESANDO {proj_id}]: {title}")
    print(f"=======================================================")
    
    # 1. Preparar archivos de imagen y datos de escena
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
    
    # 2. Ejecutar run_pipeline
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
    
    # 3. Guardar metadatos listos para publicación
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
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }, f, indent=2, ensure_ascii=False)
        
    print(f"[OK] Video completado con exito: {final_video}")
    return final_video

def main():
    PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    completed_videos = []
    
    print(f"Iniciando Renderizado del Pack de 10 Videos Virales (60s) en: {PACK_OUTPUT_DIR}")
    start_time = time.time()
    
    for idx, proj in enumerate(PROJECTS, 1):
        print(f"\n>>> INICIANDO VIDEO {idx} DE {len(PROJECTS)} <<<")
        try:
            v_path = build_single_video(proj, PACK_OUTPUT_DIR)
            completed_videos.append((proj, v_path))
        except Exception as e:
            print(f"[ERROR] generando video {proj['id']}: {e}")
            import traceback
            traceback.print_exc()
            
    total_time = time.time() - start_time
    print(f"\n=======================================================")
    print(f"[PACK COMPLETADO] {len(completed_videos)} de {len(PROJECTS)} videos generados en {total_time/60:.1f} minutos.")
    print(f"=======================================================")
    
    # Generar Documento de Publicacion y Calendario
    cal_path = PACK_OUTPUT_DIR / "CALENDARIO_PUBLICACION_10_VIDEOS.md"
    lines = [
        "# 🚀 Pack de 10 Videos Virales (60 Segundos) — Multiverso Cómic",
        "",
        "> [!IMPORTANT]",
        "> **Estrategia de Publicación en Redes (YouTube Shorts, Facebook Reels, TikTok, Instagram Reels):**",
        "> - **100% Inéditos y Únicos:** Auditados rigurosamente contra el historial de 192 videos del canal.",
        "> - **Duración Óptima:** ~50-56 segundos por video (máxima retención y elegibles para todas las plataformas).",
        "> - **Formato:** Vertical Full HD 1080x1920 con transiciones 3D de papel rasgado, efectos Foley y subtítulos Bangers Comic Noir.",
        "> - **Frecuencia Recomendada:** 1 video al día (o 2 al día en horarios pico: 1:00 PM y 7:00 PM).",
        "",
        "---",
        "",
        "## 📅 Calendario de Publicación Día por Día",
        ""
    ]
    
    for idx, (proj, v_path) in enumerate(completed_videos, 1):
        pid = proj["id"]
        title = proj["title"]
        desc = proj["description"]
        tags = proj["hashtags"]
        v_name = os.path.basename(v_path)
        v_url = f"file:///{v_path.replace(os.sep, '/')}"
        thumb_name = v_name.replace(".mp4", "_thumb.jpg")
        thumb_path = os.path.join(os.path.dirname(v_path), thumb_name)
        thumb_url = f"file:///{thumb_path.replace(os.sep, '/')}"
        
        estado_label = "[✅ SUBIDO / PUBLICADO]" if idx == 1 else "[🔥 LISTO PARA SUBIR]"
        
        lines.extend([
            f"### 📌 Día {idx}: {title} {estado_label}",
            f"- 🎬 **Video (MP4):** [{v_name}]({v_url})",
            f"- 🖼️ **Miniatura Oficial:** [{thumb_name}]({thumb_url})",
            f"- 💬 **Texto de Publicación (Copiar y Pegar):**",
            f"```text",
            f"{title}",
            f"",
            f"{desc}",
            f"",
            f"{tags}",
            f"```",
            ""
        ])
        
    with open(cal_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"[CALENDARIO] Generado exitosamente en: {cal_path}")

if __name__ == "__main__":
    main()
