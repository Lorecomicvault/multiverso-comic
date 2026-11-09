"""
Master Production Engine: Top 5 Remastered Mega Hits (Slots 51 al 55)
====================================================================
1. Slot 51: Superior Spider-Man vs Escorpión (Mandíbula brutal)
2. Slot 52: Batman se inyecta el Virus Doomsday (The Devastator)
3. Slot 53: Spider-Man humilla a Kingpin en Ryker's (Back in Black)
4. Slot 54: Sentry descuartiza a Ares en dos mitades (Siege)
5. Slot 55: El Batman Que Ríe (Origen en Crime Alley)
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.pipeline import run_pipeline
from src.cloud_runner import build_cloud_generation
from src.composer import get_duration

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_remaster_hits"
PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)

REMASTER_PROJECTS = [
    {
        "slot": 51,
        "queue_folder": "51_spiderman_escorpion_mandibula_superior",
        "id": "spiderman_escorpion_mandibula_superior",
        "title": "¡Spider-Man Jamás Usó Toda su Fuerza! El Puñetazo que Destrozó a Escorpión 🕷️💥🩸",
        "character": "Spider-Man",
        "folder": "51_spiderman_escorpion_mandibula_superior",
        "theme_signature": "spiderman:superior_1:scorpion_jaw_shattered",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El secreto más escalofriante de Peter Parker que redefine por completo la verdadera fuerza de Spider-Man! Durante décadas, todos creyeron que el arácnido apenas superaba la fuerza de diez hombres. Sin embargo, cuando el Doctor Octopus robó la mente y el cuerpo del héroe convirtiéndose en el Superior Spider-Man, una catástrofe estaba a punto de estallar en Manhattan."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El despiadado villano cibernético Mac Gargan, alias el Escorpión, escapó de prisión y asaltó un hospital civil tomando como rehén a la mismísima tía May. Confiado en que Spider-Man respondería con sus bromas habituales y golpes contenidos de siempre, el criminal amenazó con atravesar a los inocentes con su aguijón de ácido hirviente."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero Otto Octavius no conocía la piedad ni el autocontrol moral de Peter. Furioso ante la insolencia del enemigo, Otto cerró su puño arácnido con el cien por ciento de su potencia sobrehumana y descargó un golpe seco y demoledor directo al rostro de Escorpión, arrancándole de cuajo la mandíbula entera de titanio en una explosión de sangre y hueso."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Mirando horrorizado sus nudillos ensangrentados, Otto comprendió la verdad más perturbadora de Marvel: Peter Parker siempre contuvo sus golpes para no asesinarlo durante años. ¿Crees que Peter debió desatar su verdadera fuerza antes, o su contención lo hace el héroe supremo? ¡Déjanos tu opinión en los comentarios!"
            }
        ],
        "description": "La legendaria revelación de Dan Slott y Ryan Stegman: Superior Spider-Man #1. El puñetazo que arrancó la mandíbula de Escorpión.",
        "hashtags": "#SpiderMan #SuperiorSpiderMan #Scorpion #DoctorOctopus #PeterParker #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 52,
        "queue_folder": "52_batman_virus_doomsday_devastator",
        "id": "batman_virus_doomsday_devastator",
        "title": "¡Batman se Clavó el Virus Doomsday en el Pecho! La Caída del Hombre de Acero 🦇💉💀",
        "character": "Batman",
        "folder": "52_batman_virus_doomsday_devastator",
        "theme_signature": "batman:the_devastator_1:doomsday_virus_injection",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La decisión más oscura y desesperada en toda la historia de Bruce Wayne para destruir a su mejor amigo! En la retorcida Tierra Menos Uno del Multiverso Oscuro, un Superman enloquecido traicionó todos sus ideales, usando su visión térmica para masacrar sin piedad a la Liga de la Justicia y aniquilar a la población del planeta entero."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Acorralado sobre los escombros humeantes de Metrópolis con la lanza de kryptonita rota y su brazo destrozado, Batman observó cómo Superman descendía con los ojos inyectados en sangre para darle el golpe de gracia, burlándose de lo débil y patético que era el ser humano común ante el poder de un dios alienígena."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sabiendo que la humanidad no sobreviviría, Bruce extrajo de su cinturón una jeringa oculta que contenía una cepa experimental modificada del virus Doomsday. Sin dudarlo un segundo, Batman se clavó la aguja directamente en el centro del corazón, fracturando sus propios huesos mientras espinas masivas de roca gris emergían brutalmente de su piel."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Mutado en el imparable coloso Devastator, Batman exhaló una nube de esporas tóxicas que petrificó al Hombre de Acero, arrancándole la vida con sus propias garras monstruosas. ¿Cruzarías la línea definitiva de convertirte en un monstruo para salvar al mundo? ¡Comenta abajo qué habrías hecho tú!"
            }
        ],
        "description": "La escalofriante pesadilla de Frank Tieri y Tony Daniel: Batman: The Devastator #1. El nacimiento del Batman Doomsday.",
        "hashtags": "#Batman #Superman #Doomsday #TheDevastator #DarkMultiverse #DCComics #JusticeLeague #Comics #Shorts #Reels"
    },
    {
        "slot": 53,
        "queue_folder": "53_spiderman_back_in_black_kingpin",
        "id": "spiderman_back_in_black_kingpin",
        "title": "¡Spider-Man Humilló a Kingpin en la Cárcel! La Furia de Back in Black 🕷️⛓️🩸",
        "character": "Spider-Man",
        "folder": "53_spiderman_back_in_black_kingpin",
        "theme_signature": "spiderman:back_in_black:kingpin_rykers_prison_beating",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El día en que Peter Parker abandonó el color rojo y azul para convertirse en la peor pesadilla del bajo mundo neoyorquino! Tras los sangrientos eventos de Civil War, un francotirador contratado disparó una bala letal que dejó a la tía May debatiéndose entre la vida y la muerte en una cama de cuidados intensivos."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Consumido por una furia helada, Peter vistió nuevamente el traje negro de tela y caminó en absoluto silencio hacia la prisión de máxima seguridad de Ryker's Island. Sin máscara y a cara descubierta frente a cientos de reclusos que lo abucheaban, Parker entró en el patio central para confrontar al autor intelectual del atentado: Wilson Fisk."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Kingpin creyó que su descomunal masa muscular de trescientos kilos intimidaría al joven justiciero. Pero Peter esquivó cada embestida como si fuera un niño y comenzó a moler a Kingpin a bofetadas secas a mano abierta, destrozándole la nariz, fracturando sus costillas y haciéndolo gatear de rodillas como una rata asustada."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Sujetando a Fisk de la papada ensangrentada, Peter le advirtió que el día que May muriera regresaría para llenar sus pulmones de telaraña hasta asfixiarlo lentamente frente a los convictos. ¿Hizo bien Spider-Man en humillar a Kingpin sin máscara? ¡Escribe tu veredicto en los comentarios!"
            }
        ],
        "description": "La legendaria obra maestra de J. Michael Straczynski y Ron Garney: Amazing Spider-Man #542. La paliza a Wilson Fisk en Ryker's.",
        "hashtags": "#SpiderMan #Kingpin #BackInBlack #PeterParker #WilsonFisk #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 54,
        "queue_folder": "54_sentry_descuartiza_ares_siege",
        "id": "sentry_descuartiza_ares_siege",
        "title": "¡Sentry Descuartizó a Ares con sus Propias Manos! La Muerte Más Brutal de Marvel ⚡🪓🩸",
        "character": "Sentry",
        "folder": "54_sentry_descuartiza_ares_siege",
        "theme_signature": "sentry:siege_2:ares_ripped_in_half_void",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El momento más censurado, aterrador e impactante jamás publicado en las páginas de un cómic de superhéroes! Durante el clímax de la sangrienta saga Siege, el tirano Norman Osborn orquestó una invasión militar masiva sobre el reino flotante de Asgard en los cielos de Broxton, Oklahoma, para destruir a los dioses nórdicos."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Ares, el temible Dios de la Guerra olímpico, descubrió que Osborn lo había manipulado con mentiras para atacar a sus antiguos aliados. Enfurecido por la traición, el dios levantó su hacha de combate y se abalanzó salvajemente contra Norman, jurando arrancarle la cabeza en pleno campo de batalla."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Antes de que el filo alcanzara a Osborn, una sombra dorada descendió a la velocidad de la luz: Robert Reynolds, el Sentry. Pero Reynolds ya no tenía el control de su cuerpo; la entidad demoníaca conocida como The Void había consumido su mente, inyectando una mirada de oscuridad absoluta en sus pupilas vacías."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Sentry sujetó a Ares por la armadura del pecho y con una fuerza divina sobrehumana, partió al Dios de la Guerra en dos mitades en el aire, derramando sus vísceras frente al silencio sepulcral de los Vengadores horrorizados. ¿Es Sentry el héroe más peligroso e inestable de Marvel? ¡Coméntanos qué opinas!"
            }
        ],
        "description": "El brutal clímax de Brian Michael Bendis y Olivier Coipel: Siege #2. Sentry descuartiza a Ares, Dios de la Guerra.",
        "hashtags": "#Sentry #Ares #Siege #TheVoid #NormanOsborn #Avengers #Marvel #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 55,
        "queue_folder": "55_batman_que_rie_dark_multiverse",
        "id": "batman_que_rie_dark_multiverse",
        "title": "¡El Origen del Batman Que Ríe! La Noche que Bruce Wayne Rompió su Código 🃏🦇🩸",
        "character": "The Batman Who Laughs",
        "folder": "55_batman_que_rie_dark_multiverse",
        "theme_signature": "batman:the_batman_who_laughs_1:joker_neck_snapped_toxin",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La transformación más siniestra, macabra y temida que condenó a muerte a todo un multiverso entero! En la Tierra Menos Veintidós del Dark Multiverse, el Joker desató su masacre definitiva en Gotham City: asesinó al comisionado Gordon con ácido y dinamitó la ciudad entera obligando a Batman a presenciar el horror."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El payaso del crimen reunió en el hospital a cientos de familias inocentes y comenzó a matar a los padres delante de sus pequeños hijos, infectando a los huérfanos con su veneno de la risa para recrear traumáticamente el callejón donde Bruce vio morir a Thomas y Martha Wayne."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Cegado por una rabia incontrolable que superó décadas de disciplina mental, Batman perdió los estribos, derribó al villano contra el pavimento y le rompió el cuello con sus propias manos. Pero al expirar su último aliento, una toxina cardíaca ultrasecreta brotó del cuerpo del Joker rociando directamente el rostro de Bruce."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "La toxina combinó la mente táctica más brillante del planeta con la locura asesina más pura. Días después, Bruce reunió a Nightwing, Red Hood y Batgirl en la Baticueva y los acribilló a balazos con una sonrisa sangrienta, naciendo El Batman Que Ríe. ¿Podrá algún héroe detenerlo jamás? ¡Déjanos tu comentario!"
            }
        ],
        "description": "El origen definitivo creado por James Tynion IV y Riley Rossmo: Dark Nights: The Batman Who Laughs #1. El fin de Bruce Wayne.",
        "hashtags": "#TheBatmanWhoLaughs #Batman #Joker #DarkMultiverse #DCComics #BatmanQueRie #Comics #Shorts #Reels"
    }
]

def produce_remaster_project(proj):
    proj_id = proj["id"]
    slot_num = proj["slot"]
    queue_name = proj["queue_folder"]
    print(f"\n{'='*75}")
    print(f"🎬 PRODUCIENDO REMASTER SLOT {slot_num}: {proj['title']}")
    print(f"{'='*75}")

    curated_folder = CURATED_BASE / proj["folder"]
    scene_art_urls = []
    scenes_text = []
    for s in proj["scenes"]:
        p_path = curated_folder / s["file"]
        if not p_path.exists():
            print(f"[ERROR] Panel no encontrado: {p_path}")
            return None
        scene_art_urls.append(str(p_path))
        scenes_text.append(s["text"])

    story_payload = dict(proj)
    story_payload["scenes"] = scenes_text
    story_payload["scene_art_urls"] = scene_art_urls

    proj_out_dir = PACK_OUTPUT_DIR / proj_id
    if proj_out_dir.exists():
        shutil.rmtree(proj_out_dir, ignore_errors=True)

    work_dir = PROJECT_ROOT / "work" / f"remaster_{proj_id}"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    generation = build_cloud_generation(story_payload, work_dir)
    voice_choice = proj.get("voice", "Puck")
    final_output_dir = PACK_OUTPUT_DIR / "finals"
    final_output_dir.mkdir(parents=True, exist_ok=True)

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

    if not final_video_path or not Path(final_video_path).exists():
        print(f"[ERROR] No se generó el video final para {proj_id}")
        return None

    dur = get_duration(str(final_video_path))
    print(f"📊 Duración del video generado: {dur:.2f} segundos")
    if dur < 60.0:
        print(f"⚠️ ADVERTENCIA: Duración {dur:.2f}s es menor a 60.0s!")
        return None
    else:
        print(f"✅ EXCELENTE: Duración {dur:.2f}s >= 60.0s (CALIDAD GARANTIZADA)")

    thumb_path = Path(final_video_path).parent / f"{Path(final_video_path).stem}_thumb.jpg"
    if not thumb_path.exists():
        thumb_path = Path(final_video_path).with_suffix('.jpg')

    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_video = dest_dir / "video.mp4"
    dest_thumb = dest_dir / "thumb.jpg"
    dest_meta = dest_dir / "metadata.json"

    shutil.copy2(final_video_path, dest_video)
    if thumb_path.exists():
        shutil.copy2(thumb_path, dest_thumb)

    meta_payload = {
        "title": proj["title"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "character": proj["character"],
        "theme_signature": proj["theme_signature"],
        "duration_seconds": round(dur, 2),
        "scheduled_slot": slot_num,
        "queue_folder": queue_name,
        "source": "remastered_mega_hits_curated_panels",
        "original_views_tier": "100k_to_440k_views",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(dest_meta, "w", encoding="utf-8") as mf:
        json.dump(meta_payload, mf, indent=2, ensure_ascii=False)

    print(f"✅ Video encolado exitosamente en {dest_dir}")
    return dest_dir

if __name__ == "__main__":
    target_slot = None
    force_mode = "--force" in [a.lower() for a in sys.argv]
    for a in sys.argv[1:]:
        if a.strip().isdigit():
            target_slot = int(a.strip())

    print("=" * 80)
    print("🚀 INICIANDO PRODUCCIÓN AUTOMATIZADA DE REMASTERS VIRALES (SLOTS 51 AL 55)")
    print("=" * 80)

    completed = []
    failed = []

    for proj in REMASTER_PROJECTS:
        slot = proj["slot"]
        if target_slot and slot != target_slot:
            continue
        
        dest = SCHEDULED_QUEUE / proj["queue_folder"]
        if not force_mode and (dest / "video.mp4").exists() and (dest / "metadata.json").exists():
            print(f"⏩ Slot {slot} ya existe en scheduled_queue. Saltando.")
            continue

        max_attempts = 3
        success = False
        for attempt in range(1, max_attempts + 1):
            print(f"\n--- [Intento {attempt}/{max_attempts}] Compilando Slot {slot} ---")
            try:
                res = produce_remaster_project(proj)
                if res and (res / "video.mp4").exists():
                    completed.append(slot)
                    success = True
                    break
                else:
                    print(f"⚠️ Reintentando slot {slot}...")
                    time.sleep(3)
            except Exception as e:
                print(f"❌ Error en slot {slot}: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(4)

        if not success:
            failed.append(slot)
            print(f"🚨 FATAL: Slot {slot} falló.")
            break

    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL DE REMASTERIZACIONES")
    print(f"✅ Slots completados: {completed}")
    print(f"❌ Slots fallidos: {failed}")
    print("=" * 80)

    if failed:
        sys.exit(1)
    else:
        print("🎉 ¡TODOS LOS 5 MEGA HITS FUERON REMASTERIZADOS Y ENCOLADOS CON ÉXITO!")
        sys.exit(0)
