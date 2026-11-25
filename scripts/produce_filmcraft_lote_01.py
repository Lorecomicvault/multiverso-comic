"""
Lote 1 Maestro (FilmCraft 60FPS + Voicebox 0.6B ES) — 10 Videos de ~75 Segundos
===============================================================================
Produce 10 videos virales de contexto completo (~1m 15s) editados 100% en FilmCraft
con aceleración GPU, subtítulos karaoke Blanco + Rosa Pastel, Hook Card flotante,
mezcla multicanal A1/A2/A3 y empaquetado prioritario en scheduled_queue/001_fc_*..010_fc_*.
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

import requests
from src.filmcraft_engine import assemble_filmcraft_reel, get_media_duration
from src.transcribe import extract_scene_word_timings
from scripts.produce_lote_common import (
    PROFILE_REFERENCIA,
    PROFILE_ZAZOOM,
    render_minimal_text_thumb,
)

VOICEBOX_URL = "http://127.0.0.1:17493"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"


def synthesize_voicebox_es(text: str, out_wav: Path, profile_id: str = PROFILE_REFERENCIA) -> Path:
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "profile_id": profile_id,
        "text": text,
        "language": "es",
        "model_size": "0.6B",
        "normalize": True,
    }

    for attempt in range(1, 6):
        # Wait politely if user is actively generating in Voicebox GUI
        for _ in range(60):
            try:
                act = requests.get(f"{VOICEBOX_URL}/tasks/active", timeout=5)
                if act.status_code == 200 and not act.json().get("generations"):
                    break
            except Exception:
                pass
            time.sleep(1.5)

        try:
            r = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=25)
            if r.status_code != 200:
                time.sleep(3)
                continue
            gid = r.json()["id"]
        except Exception as e:
            print(f"  [Voicebox Conn Error] {e} (intento {attempt})", flush=True)
            time.sleep(4)
            continue

        for _ in range(360):
            time.sleep(1.0)
            try:
                h = requests.get(f"{VOICEBOX_URL}/history/{gid}", timeout=10).json()
            except Exception:
                continue
            status = h.get("status")
            if status == "completed":
                aud = requests.get(f"{VOICEBOX_URL}/audio/{gid}", timeout=30)
                raw_tmp = str(out_wav) + ".raw.wav"
                with open(raw_tmp, "wb") as f:
                    f.write(aud.content)
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        raw_tmp,
                        "-af",
                        "silenceremove=start_periods=1:start_silence=0.12:start_threshold=-45dB,aresample=48000,apad=pad_dur=0.22",
                        "-acodec",
                        "pcm_s16le",
                        str(out_wav),
                    ],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if Path(raw_tmp).exists():
                    Path(raw_tmp).unlink()
                return out_wav
            elif status == "failed":
                print(f"  [Voicebox Error] {h.get('error')} (intento {attempt})", flush=True)
                time.sleep(3)
                break
    raise TimeoutError(f"Voicebox timeout para: {text[:45]}")


# Shortcuts to source asset directories
SRC = PROJECT_ROOT / "assets" / "comics_source"
ASM542 = SRC / "spiderman_back_in_black" / "extracted_asm_542" / "The Amazing Spider-Man 542 (2007) (digital) (Minutemen-InnerDemons)"
BIB248 = CURATED_BASE / "248_spiderman_back_in_black_disparo_tia_may"
SW08 = SRC / "secret_wars_2015" / "pages" / "issue_08"
BWL = SRC / "batman_who_laughs" / "extracted"
DEV = SRC / "batman_devastator" / "extracted"
IH8 = SRC / "immortal_hulk_8" / "extracted_pages_08"
SIEGE02 = SRC / "siege" / "extracted_siege_02"
PH105 = SRC / "planet_hulk" / "extracted_105" / "025 Planet Hulk Armageddon Incredible Hulk v3 105"
WVH = SRC / "wolverine_vs_hulk" / "extracted_pages"
CUSA1 = SRC / "carnage_usa" / "extracted_01"
CUSA2 = SRC / "carnage_usa" / "extracted_02"
DDGD = SRC / "daredevil_guardian_devil" / "extracted"


LOTE_01_PROJECTS = [
    {
        "slot": 1,
        "queue_folder": "001_fc_spiderman_back_in_black_kingpin",
        "id": "fc_01_spiderman_back_in_black_kingpin",
        "folder": "fc_01_spiderman_back_in_black_kingpin",
        "work_subdir": "filmcraft_pilot_01",  # reuses cached Voicebox audio from pilot
        "title": "Spider-Man: ¡Sin Máscara y Sin Piedad! La Humillación a Kingpin en Prisión 🕷️🩸",
        "character": "Spider-Man",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ SPIDER-MAN JURÓ MATAR A KINGPIN?",
        "thumb_text": "SIN MÁSCARA Y SIN PIEDAD",
        "thumb_scene_idx": 0,
        "description": "Amazing Spider-Man #542 (Back in Black): El día que Peter Parker abandonó su regla moral para destruir a Wilson Fisk frente a toda la cárcel.",
        "hashtags": "#SpiderMan #BackInBlack #Kingpin #MarvelComics #ComicsEnEspanol #Reels #Shorts",
        "scenes": [
            {
                "src": ASM542 / "The Amazing Spider-Man 542-008.jpg",
                "text": "Frente a cientos de reclusos en máxima seguridad, Peter Parker se quita lentamente la máscara. Hoy no viene como Spider-Man, viene como un hombre dispuesto a matar.",
            },
            {
                "src": BIB248 / "scene_1.jpg",
                "text": "Días atrás, tras revelar su identidad en la Guerra Civil, un francotirador ejecutó la orden de Wilson Fisk. La bala destrozó el pecho de la tía May frente a Mary Jane.",
            },
            {
                "src": BIB248 / "scene_2.jpg",
                "text": "Desesperado y sin llamar a los Vengadores, Peter recorrió la ciudad cargándola entre sus brazos, rompiendo cada ventana de su pasado con tal de mantenerla con vida.",
            },
            {
                "src": BIB248 / "scene_4.jpg",
                "text": "Esa noche desenterró su traje negro bajo la tormenta. Juró ante el cielo que cuando encontrara al verdadero culpable, abandonaría para siempre su regla de no asesinar.",
            },
            {
                "src": ASM542 / "The Amazing Spider-Man 542-014.jpg",
                "text": "Al llegar a prisión, Kingpin creyó poder aplastarlo con su enorme fuerza bruta. Pero Peter no esquivó ni hizo chistes: lo tomó de la piel y lo abofeteó sin piedad.",
            },
            {
                "src": ASM542 / "The Amazing Spider-Man 542-015.jpg",
                "text": "Frente a toda la cárcel paralizada por el miedo, lo levantó del cuello como a un muñeco de trapo, destruyendo en segundos el imperio de terror que Fisk construyó.",
            },
            {
                "src": ASM542 / "The Amazing Spider-Man 542-018.jpg",
                "text": "Con Kingpin sangrando en el suelo, Peter sentenció que si May muere, regresará y llenará sus pulmones de telaraña para ahogarlo en tres segundos.",
            },
            {
                "src": ASM542 / "The Amazing Spider-Man 542-019.jpg",
                "text": "Dejando a toda la prisión muda de pánico, Peter desapareció entre las sombras. Y tú, ¿cruzarías esa línea definitiva si tocaran a tu familia?",
            },
        ],
    },
    {
        "slot": 2,
        "queue_folder": "002_fc_secret_wars_doom_mata_thanos",
        "id": "fc_02_secret_wars_doom_mata_thanos",
        "folder": "fc_02_secret_wars_doom_mata_thanos",
        "title": "¡God Emperor Doom Arrancó el Esqueleto de Thanos de un Solo Golpe! 💀⚡👑",
        "character": "Doctor Doom",
        "voice_mode": "zazoom",
        "hook_card": "¿QUIÉN HUMILLÓ Y MATÓ A THANOS EN UN SEGUNDO?",
        "thumb_text": "DOOM DESTROZÓ A THANOS",
        "thumb_scene_idx": 4,
        "description": "Secret Wars #8 (Jonathan Hickman): Cuando Thanos desafió al Dios Emperador Doom sin las Gemas del Infinito y conoció su final más brutal.",
        "hashtags": "#DoctorDoom #Thanos #SecretWars #MarvelComics #Comics #Reels #Shorts",
        "scenes": [
            {
                "src": SW08 / "Secret Wars (2015-) 008-001.jpg",
                "text": "Con el multiverso reducido a un único planeta llamado Battleworld, Victor Von Doom gobierna como un dios absoluto tras robar el poder omnipotente de los Beyonders.",
            },
            {
                "src": SW08 / "Secret Wars (2015-) 008-014.jpg",
                "text": "Mientras los ejércitos de rebeldes atacan su fortaleza, Doom permanece sereno en su trono observando cómo los héroes más poderosos luchan por sobrevivir.",
            },
            {
                "src": SW08 / "Secret Wars (2015-) 008-019.jpg",
                "text": "Pero entre el caos emerge Thanos el Titán Loco, liderando una horda de monstruos para derrocar a Doom, convencido de que nadie en la creación puede igualarlo.",
            },
            {
                "src": SW08 / "Secret Wars (2015-) 008-020.jpg",
                "text": "Thanos le grita arrogante que es un simple impostor sin poder verdadero. Doom desciende lentamente y le pregunta con frialdad si aún posee el Guantelete del Infinito.",
            },
            {
                "src": SW08 / "Secret Wars (2015-) 008-021.jpg",
                "text": "Al confirmar que no lo tiene, Doom le responde que entonces es inferior. En un parpadeo, atraviesa la armadura de Thanos y le arranca toda la columna vertebral.",
            },
            {
                "src": SW08 / "Secret Wars (2015-) 008-022.jpg",
                "text": "El cuerpo del titán más temido del universo se desintegra en cenizas frente a sus propios aliados, dejando claro que el poder cósmico de Doom no tiene rival.",
            },
            {
                "src": SW08 / "Secret Wars (2015-) 008-023.jpg",
                "text": "Sosteniendo el cráneo aún ardiente de Thanos en su mano, Doom ordena aplastar la rebelión. ¿Algún villano de Marvel ha tenido una muerte tan humillante?",
            },
        ],
    },
    {
        "slot": 3,
        "queue_folder": "003_fc_batman_que_rie_origen_masacre",
        "id": "fc_03_batman_que_rie_origen_masacre",
        "folder": "fc_03_batman_que_rie_origen_masacre",
        "title": "El Batman Que Ríe: ¡El Día que Masacró a Toda la Liga de la Justicia! 🦇🤡🩸",
        "character": "Batman",
        "voice_mode": "referencia",
        "hook_card": "¿CÓMO BATMAN ASESINÓ A SUPERMAN Y SU FAMILIA?",
        "thumb_text": "MASACRE EN LA BATCUEVA",
        "thumb_scene_idx": 7,
        "description": "Dark Nights: The Batman Who Laughs — La perturbadora historia de Tierra-22 donde Bruce Wayne inhaló la toxina final del Joker y destruyó el mundo.",
        "hashtags": "#Batman #ElBatmanQueRie #Joker #DCComics #LigaDeLaJusticia #Comics #Reels",
        "scenes": [
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p002-003 [Digital-HD] [danke-Empire].jpg",
                "text": "En la oscura Tierra veintidós del multiverso negativo, el Joker desató un genocidio en Gotham, empujando finalmente a Bruce Wayne a cruzar su límite más sagrado.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p004-005 [Digital-HD] [danke-Empire].jpg",
                "text": "Consumido por la rabia, Batman le rompió el cuello al payaso. Pero la última risa del Joker liberó una nanotoxina secreta de su corazón directo al rostro de Bruce.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p008 [Digital-HD] [danke-Empire].jpg",
                "text": "Días después la mente brillante de Bruce quedó fusionada con la locura pura del Joker. Reunió a Nightwing, Batgirl y Red Hood solo para acribillarlos a sangre fría.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p011 [Digital-HD] [danke-Empire].jpg",
                "text": "Fingiendo seguir siendo un héroe, subió a la Atalaya de la Liga de la Justicia pidiendo ayuda a Superman para contener una supuesta amenaza en Gotham.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p013 [Digital-HD] [danke-Empire].jpg",
                "text": "De repente desató todo el arsenal letal que guardaba contra sus propios amigos, ejecutando sin piedad a Flash, Linterna Verde y la Mujer Maravilla frente a todos.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p016 [Digital-HD] [danke-Empire].jpg",
                "text": "Para su obra maestra, encerró a Superman, Lois Lane y al pequeño Jon, exponiendo al Hombre de Acero y a su hijo a una dosis mortal de kriptonita negra.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p017 [Digital-HD] [danke-Empire].jpg",
                "text": "Enloquecidos por la sustancia, Superman y su hijo perdieron toda razón y destrozaron a Lois frente a los ojos risueños de un Bruce completamente deformado.",
            },
            {
                "src": BWL / "Dark Nights - The Batman Who Laughs - c001 (web) - p020-021 [Digital-HD] [danke-Empire].jpg",
                "text": "Así nació el Batman Que Ríe, combinando el intelecto táctico de Bruce con la crueldad infinita del Joker. ¿Es esta la versión más aterradora de Batman?",
            },
        ],
    },
    {
        "slot": 4,
        "queue_folder": "004_fc_batman_devastator_mata_superman",
        "id": "fc_04_batman_devastator_mata_superman",
        "folder": "fc_04_batman_devastator_mata_superman",
        "title": "¡Batman se Inyectó el Virus Doomsday y Asesinó a Superman! 🦇🦖🩸",
        "character": "Batman",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ BATMAN SE CONVIRTIÓ EN DOOMSDAY?",
        "thumb_text": "BRUCE MATÓ A SUPERMAN",
        "thumb_scene_idx": 4,
        "description": "Batman: The Devastator #1 — Cuando Superman enloqueció en Tierra-1, Bruce Wayne usó su contramedida biológica más extrema.",
        "hashtags": "#Batman #Superman #Doomsday #BatmanDevastator #DCComics #Comics #Reels",
        "scenes": [
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-008.jpg",
                "text": "En Tierra menos uno, Superman perdió todo rastro de humanidad y comenzó a destruir el mundo, obligando a su antiguo mejor amigo Batman a enfrentarlo solo en Metrópolis.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-009.jpg",
                "text": "Bruce intentó apelar al recuerdo de su amistad usando la lanza de kriptonita, pero el Hombre de Acero la destruyó riéndose de la debilidad de los mortales.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-010.jpg",
                "text": "Sin contenerse ni un segundo, Superman disparó su visión de calor directamente contra Bruce, calcinando por completo su brazo derecho en medio de la nieve.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-011.jpg",
                "text": "Con la muerte a segundos de distancia, Batman liberó su plan de emergencia prohibido: se inyectó el virus Doomsday, transformándose en una bestia colosal e imparable.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-012.jpg",
                "text": "El monstruo atrapó a Superman en el aire y le respiró polvo letal de kriptonita en el rostro, derribándolo brutalmente contra las ruinas de la ciudad.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-013.jpg",
                "text": "Finalmente lo atravesó con sus espinas óseas frente a un planeta condenado, demostrando que su paranoia tenía razón: nadie podía confiar ciegamente en un dios.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-007.jpg",
                "text": "Consumido por la transformación, Bruce no pudo volver a ser humano jamás, desatando su furia como el Devastador al invadir nuestra realidad junto a Lois Lane.",
            },
            {
                "src": DEV / "Batman - The Devastator (2017-) 001-014.jpg",
                "text": "Reclutado por el Batman Que Ríe para los Caballeros Oscuros, su tragedia sigue siendo leyenda. ¿Hizo bien Bruce al inyectarse ese virus mortal?",
            },
        ],
    },
    {
        "slot": 5,
        "queue_folder": "005_fc_immortal_hulk_frascos_laboratorio",
        "id": "fc_05_immortal_hulk_frascos_laboratorio",
        "folder": "fc_05_immortal_hulk_frascos_laboratorio",
        "title": "Immortal Hulk: ¡Lo Descuartizaron Vivo en Frascos y Todo Terminó en Horror! 🧪💚🩸",
        "character": "Hulk",
        "voice_mode": "referencia",
        "hook_card": "¿QUÉ PASA SI CORTAN A HULK EN PEDAZOS?",
        "thumb_text": "DESCUARTIZADO EN FRASCOS",
        "thumb_scene_idx": 0,
        "description": "Immortal Hulk #8 (Al Ewing): La escena más escalofriante de terror corporal en Marvel cuando intentaron diseccionar vivo a Bruce Banner.",
        "hashtags": "#ImmortalHulk #Hulk #MarvelComics #Terror #ComicsEnEspanol #Reels #Shorts",
        "scenes": [
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-000.jpg",
                "text": "Tras capturar finalmente a Bruce Banner en una base secreta del gobierno, los científicos creyeron haber encontrado la forma definitiva de neutralizar al monstruo.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-002.jpg",
                "text": "Usando láseres de radiación ultravioleta para impedir su transformación, diseccionaron el cuerpo de Hulk pieza por pieza mientras su mente seguía completamente despierta.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-003.jpg",
                "text": "Su corazón, su cerebro, sus extremidades y cada órgano quedaron sellados en docenas de frascos de cristal, convencidos de que jamás podría volver a regenerarse.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-010.jpg",
                "text": "Pero el líder del experimento cometió la estupidez de burlarse frente al frasco con su rostro, sin notar que el ojo verde del monstruo lo observaba fijamente.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-011.jpg",
                "text": "Con una sonrisa siniestra detrás del vidrio, la mano amputada de Hulk en otro frasco se movió por voluntad propia y chasqueó los dedos contra el cristal.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-012.jpg",
                "text": "En un estallido ensordecedor todos los contenedores explotaron al mismo tiempo. Tentáculos de carne verde y huesos volaron por el laboratorio buscando unirse otra vez.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-013.jpg",
                "text": "Las vísceras vivas atraparon al científico aterrado, absorbiéndolo dentro de la masa muscular mientras el monstruo reconstruía su cuerpo alrededor del pobre hombre.",
            },
            {
                "src": IH8 / "Immortal Hulk (2018-) 008-014.jpg",
                "text": "Totalmente regenerado y con el científico atrapado en su interior, Hulk les enseñó que es verdaderamente inmortal. ¿Es esta la escena más terrorífica de Marvel?",
            },
        ],
    },
    {
        "slot": 6,
        "queue_folder": "006_fc_sentry_descuartiza_ares_asgard",
        "id": "fc_06_sentry_descuartiza_ares_asgard",
        "folder": "fc_06_sentry_descuartiza_ares_asgard",
        "title": "¡La Muerte Más Censurada de Marvel! Sentry Parte en Dos a Ares en Asgard 🩸⚡🌑",
        "character": "Sentry",
        "voice_mode": "zazoom",
        "hook_card": "¿LA MUERTE MÁS BRUTAL Y CENSURADA DE MARVEL?",
        "thumb_text": "PARTIDO EN DOS MITADES",
        "thumb_scene_idx": 6,
        "description": "Siege #2 (Brian Michael Bendis): El momento en que Sentry desató su lado oscuro y ejecutó al Dios de la Guerra frente a todo Asgard.",
        "hashtags": "#Sentry #Ares #Asgard #MarvelComics #Siege #ComicsEnEspanol #Reels",
        "scenes": [
            {
                "src": SIEGE02 / "Siege 02-009.jpg",
                "text": "Durante el brutal asedio contra Asgard liderado por Norman Osborn, el mismísimo Ares, Dios de la Guerra, descubre que fue engañado para invadir el hogar de los dioses.",
            },
            {
                "src": SIEGE02 / "Siege 02-010.jpg",
                "text": "Furioso por la traición, Ares jura arrancarle la cabeza a Osborn. Pero en su camino se interpone el guerrero más inestable y poderoso de Marvel: el Sentry.",
            },
            {
                "src": SIEGE02 / "Siege 02-011.jpg",
                "text": "Con los ojos brillando bajo la influencia oscura del Vacío, Sentry le ordena detenerse. Sin embargo, el orgullo inmortal de Ares no conoce la palabra retirada.",
            },
            {
                "src": SIEGE02 / "Siege 02-012.jpg",
                "text": "Ambos colosos chocan sobre las nubes asgardianas en una pelea salvaje que hace temblar la tierra entera con cada golpe cargado de energía cósmica.",
            },
            {
                "src": SIEGE02 / "Siege 02-013.jpg",
                "text": "Ares descarga toda la furia de sus hachas sobre el cuerpo de Sentry intentando partirlo, sin saber que solo está despertando a la pesadilla absoluta que vive dentro.",
            },
            {
                "src": SIEGE02 / "Siege 02-014.jpg",
                "text": "Inmune al dolor, Sentry atrapa al Dios de la Guerra en el aire sujetándolo con ambas manos de la cintura, mientras los demás héroes miran horrorizados desde abajo.",
            },
            {
                "src": SIEGE02 / "Siege 02-015.jpg",
                "text": "Sin pronunciar palabra, Sentry parte literalmente en dos mitades a Ares haciendo llover sangre sobre Asgard. ¿Alguna vez viste una ejecución tan salvaje en un cómic?",
            },
        ],
    },
    {
        "slot": 7,
        "queue_folder": "007_fc_world_war_hulk_muerte_caiera",
        "id": "fc_07_world_war_hulk_muerte_caiera",
        "folder": "fc_07_world_war_hulk_muerte_caiera",
        "title": "World War Hulk: ¡La Traición que Destruyó su Planeta y Desató su Venganza! 💥💚🔥",
        "character": "Hulk",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ HULK JURÓ DESTRUIR A LOS VENGADORES?",
        "thumb_text": "LA TRAICIÓN DE SAKAAR",
        "thumb_scene_idx": 5,
        "description": "Incredible Hulk #105 (Planet Hulk): La explosión que arrebató todo lo que Bruce Banner amaba y dio origen al Hulk más peligroso de la historia.",
        "hashtags": "#WorldWarHulk #PlanetHulk #Hulk #MarvelComics #Illuminati #Comics #Reels",
        "scenes": [
            {
                "src": PH105 / "IncredibleHulk105-003.jpg",
                "text": "Traicionado y exiliado al espacio por los Illuminati, Hulk cayó en el brutal planeta Sakaar, donde luchó como esclavo gladiador hasta conquistar la libertad y el trono.",
            },
            {
                "src": PH105 / "IncredibleHulk105-004.jpg",
                "text": "Por primera vez en su miserable vida, Banner encontró paz absoluta junto a su esposa Caiera, esperando un hijo y gobernando como el salvador de todo un mundo.",
            },
            {
                "src": PH105 / "IncredibleHulk105-005.jpg",
                "text": "Pero la tragedia esperaba oculta en la vieja nave en la que había llegado desde la Tierra. De pronto, los motores nucleares iniciaron una cuenta regresiva imparable.",
            },
            {
                "src": PH105 / "IncredibleHulk105-006.jpg",
                "text": "Antes de que Hulk pudiera detenerla, la nave detonó con la potencia de mil soles, desatando un infierno atómico capaz de evaporar ciudades enteras en segundos.",
            },
            {
                "src": PH105 / "IncredibleHulk105-007-008.jpg",
                "text": "La onda expansiva arrasó la capital entera asesinando a millones de inocentes en un instante, borrando el único hogar que había aceptado al monstruo sin miedo.",
            },
            {
                "src": PH105 / "IncredibleHulk105-014.jpg",
                "text": "Entre las ruinas humeantes, Hulk sostuvo en brazos el cuerpo calcinado de Caiera mientras se deshacía en cenizas frente a sus ojos llenos de lágrimas y odio.",
            },
            {
                "src": PH105 / "IncredibleHulk105-016.jpg",
                "text": "Creyendo que Tony Stark y Reed Richards programaron la bomba, su furia rompió la corteza del planeta entero, elevando su poder a un nivel jamás registrado.",
            },
            {
                "src": PH105 / "IncredibleHulk105-023-024.jpg",
                "text": "Con un ejército de sobrevivientes abordó una nave de guerra rumbo a la Tierra jurando hacer pagar a cada héroe. ¿Tenía Hulk toda la razón para destruirlos?",
            },
        ],
    },
    {
        "slot": 8,
        "queue_folder": "008_fc_wolverine_vs_hulk_partido_en_dos",
        "id": "fc_08_wolverine_vs_hulk_partido_en_dos",
        "folder": "fc_08_wolverine_vs_hulk_partido_en_dos",
        "title": "¡Hulk Partió a Wolverine en Dos Mitades y Arrojó sus Piernas a la Montaña! 🐺💚🩸",
        "character": "Wolverine",
        "voice_mode": "zazoom",
        "hook_card": "¿SOBREVIVE WOLVERINE SI LO PARTEN EN DOS?",
        "thumb_text": "PARTIDO POR LA MITAD",
        "thumb_scene_idx": 4,
        "description": "Ultimate Wolverine vs. Hulk #1: La brutal cacería en el Tíbet donde Hulk le dio a Logan la paliza más infame de toda su historia.",
        "hashtags": "#Wolverine #Hulk #MarvelComics #Logan #UltimateMarvel #Comics #Reels",
        "scenes": [
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-002.jpg",
                "text": "Cuando el gobierno descubrió que Bruce Banner seguía con vida oculto en las montañas del Tíbet, solo hubo un asesino capaz de aceptar la misión de eliminarlo.",
            },
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-007.jpg",
                "text": "Nick Fury contrató directamente a Wolverine prometiéndole silencio absoluto: nadie debía saber que SHIELD envió a un mutante para ejecutar a un antiguo compañero.",
            },
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-021.jpg",
                "text": "Durante días Logan escaló cumbres heladas guiándose únicamente por su olfato animal, dispuesto a clavar sus garras de adamantium antes de que el monstruo despertara.",
            },
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-023.jpg",
                "text": "Al encontrar a Banner convertido en rey de una aldea secreta, Wolverine sacó sus garras con su clásico sonido metálico esperando una cacería rápida.",
            },
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-003.jpg",
                "text": "Pero el error le costó caro. Enfurecido por la interrupción, Hulk lo atrapó en el aire y sin esfuerzo alguno partió el cuerpo de Wolverine en dos mitades exactas.",
            },
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-004.jpg",
                "text": "Burlándose del mutante inmortal, el gigante verde arrojó sus piernas a la cima de otra montaña nevada a kilómetros de distancia para dejarlo morir congelado.",
            },
            {
                "src": WVH / "Ultimate Comics Wolverine vs. Hulk-005.jpg",
                "text": "Pero Logan sobrevivió gracias a su factor curativo y se arrastró por la nieve siguiendo su propio olor. ¿Quién hubiera pensado que Hulk lo humillaría así?",
            },
        ],
    },
    {
        "slot": 9,
        "queue_folder": "009_fc_carnage_usa_infecta_vengadores",
        "id": "fc_09_carnage_usa_infecta_vengadores",
        "folder": "fc_09_carnage_usa_infecta_vengadores",
        "title": "Carnage U.S.A.: ¡El Día que Cletus Kasady Poseyó a Todos los Vengadores! 🩸🕷️🔥",
        "character": "Carnage",
        "voice_mode": "referencia",
        "hook_card": "¿QUÉ PASÓ CUANDO CARNAGE POSEYÓ A LOS VENGADORES?",
        "thumb_text": "VENGADORES INFECTADOS",
        "thumb_scene_idx": 5,
        "description": "Carnage U.S.A. #1–2: La invasión más retorcida del simbionte rojo cuando secuestró un pueblo entero y controló las mentes de los héroes.",
        "hashtags": "#Carnage #SpiderMan #Avengers #MarvelComics #Simbionte #Comics #Reels",
        "scenes": [
            {
                "src": CUSA1 / "Carnage USA 001-004.jpg",
                "text": "Cletus Kasady decidió dejar atrás los crímenes callejeros para demostrar su poder absoluto: tomó como rehén a un pueblo entero en Colorado bajo su control mental.",
            },
            {
                "src": CUSA1 / "Carnage USA 001-007.jpg",
                "text": "Cada hombre, mujer y niño del pueblo fue infectado por millones de esporas del simbionte carmesí, convirtiendo las calles tranquilas en una pesadilla viviente.",
            },
            {
                "src": CUSA1 / "Carnage USA 001-014.jpg",
                "text": "Al perder comunicación militar con la zona, el Capitán América lideró un escuadrón de choque con Wolverine, La Mole, Ojo de Halcón y Spider-Man para detenerlo.",
            },
            {
                "src": CUSA1 / "Carnage USA 001-015.jpg",
                "text": "Al bajar en el pueblo fantasma, los héroes quedaron paralizados viendo a los ciudadanos alineados como marionetas sonrientes esperando su llegada.",
            },
            {
                "src": CUSA1 / "Carnage USA 001-019.jpg",
                "text": "Antes de poder reaccionar, las masas de simbionte surgieron del suelo emboscando al equipo, cubriendo las armaduras y bocas de los Vengadores en cuestión de segundos.",
            },
            {
                "src": CUSA1 / "Carnage USA 001-020.jpg",
                "text": "Con las venas negras invadiendo sus cerebros, Wolverine, Cap y Hawkeye cayeron bajo las órdenes de Kasady, rodeando al pobre Spider-Man entre carcajadas.",
            },
            {
                "src": CUSA2 / "Carnage USA 002-001.jpg",
                "text": "Incluso La Mole terminó convertido en una bestia imparable de sangre y músculo rojo. ¿Cómo pudo Spider-Man sobrevivir solo frente a todo un escuadrón infectado?",
            },
        ],
    },
    {
        "slot": 10,
        "queue_folder": "010_fc_daredevil_muerte_karen_page",
        "id": "fc_10_daredevil_muerte_karen_page",
        "folder": "fc_10_daredevil_muerte_karen_page",
        "title": "Daredevil: ¡La Tragedia Más Cruel! Bullseye Mató a Karen Page Frente a Él 😈🩸⛪",
        "character": "Daredevil",
        "voice_mode": "zazoom",
        "hook_card": "¿LA MUERTE QUE DESTROZÓ PARA SIEMPRE A DAREDEVIL?",
        "thumb_text": "ADIÓS KAREN PAGE",
        "thumb_scene_idx": 5,
        "description": "Daredevil: Guardian Devil #5 (Kevin Smith & Joe Quesada): El asesinato más desgarrador en la vida de Matt Murdock dentro de su propia iglesia.",
        "hashtags": "#Daredevil #Bullseye #KarenPage #MarvelComics #MattMurdock #Comics #Reels",
        "scenes": [
            {
                "src": DDGD / "Daredevil - Guardian Devil-104.jpg",
                "text": "En medio de una conspiración religiosa diseñada por Mysterio para volver loco a Matt Murdock, el despiadado asesino Bullseye irrumpe en la iglesia buscando matar a un bebé.",
            },
            {
                "src": DDGD / "Daredevil - Guardian Devil-105.jpg",
                "text": "Sin ningún código moral ni remordimiento, Bullseye masacra a las monjas del convento usando todo objeto que encuentra como arma mortal de precisión quirúrgica.",
            },
            {
                "src": DDGD / "Daredevil - Guardian Devil-106.jpg",
                "text": "Herido y desorientado, Daredevil llega a la escena lanzándose desesperadamente contra su peor enemigo para impedir una carnicería frente al altar sagrado.",
            },
            {
                "src": DDGD / "Daredevil - Guardian Devil-108.jpg",
                "text": "En medio del combate brutal, Karen Page logra rescatar a la bebé en sus brazos intentando escapar antes de que el psicópata pueda alcanzarlas.",
            },
            {
                "src": DDGD / "Daredevil - Guardian Devil-111.jpg",
                "text": "Pero Bullseye arrebata el propio bastón de Daredevil y lo lanza como lanza mortal. Karen se interpone sacrificando su vida, siendo atravesada directamente en el corazón.",
            },
            {
                "src": DDGD / "Daredevil - Guardian Devil-113.jpg",
                "text": "El silencio cae sobre la catedral. Matt sostiene el cuerpo sin vida del gran amor de su vida llorando desconsolado bajo la mirada fría del altar.",
            },
            {
                "src": DDGD / "Daredevil - Guardian Devil-118.jpg",
                "text": "Esa muerte marcó para siempre el alma de Daredevil, convirtiéndolo en un hombre consumido por la culpa. ¿Cuál ha sido para ti la muerte más triste de Marvel?",
            },
        ],
    },
]


def produce_project(proj: dict):
    slot = proj["slot"]
    q_folder = proj["queue_folder"]
    q_dir = SCHEDULED_QUEUE / q_folder
    v_out = q_dir / "video.mp4"
    m_out = q_dir / "metadata.json"

    if v_out.exists() and m_out.exists() and v_out.stat().st_size > 10_000_000:
        sz_mb = v_out.stat().st_size / (1024 * 1024)
        dur = get_media_duration(v_out)
        if 60.0 <= dur <= 90.0 and sz_mb < 95.0:
            print(f"[SKIP] Slot {slot:02d} ({q_folder}) ya listo ({dur:.2f}s, {sz_mb:.1f} MB)", flush=True)
            return dur, sz_mb, "CACHED"

    print(f"\n=======================================================", flush=True)
    print(f"🎬 [LOTE 1 FILMCRAFT - VIDEO {slot}/10] {q_folder}", flush=True)
    print(f"   Título: {proj['title']}", flush=True)
    print(f"=======================================================", flush=True)

    curated_dir = CURATED_BASE / proj["folder"]
    curated_dir.mkdir(parents=True, exist_ok=True)
    work_dir = PROJECT_ROOT / "work" / proj.get("work_subdir", f"filmcraft_lote1_slot_{slot:02d}")
    work_dir.mkdir(parents=True, exist_ok=True)

    voice_mode = proj.get("voice_mode", "referencia").lower()
    prof_id = PROFILE_ZAZOOM if voice_mode == "zazoom" else PROFILE_REFERENCIA
    v_label = "Narrador Cómics ZaZooM" if voice_mode == "zazoom" else "Narrador Referencia Cómic"

    # 1. Stage Panels & Synthesize Voicebox Audio
    raw_audios = {}
    scenes = proj["scenes"]
    for idx, sc in enumerate(scenes, start=1):
        src_img = Path(sc["src"])
        if not src_img.exists():
            raise FileNotFoundError(f"Panel faltante en Slot {slot}: {src_img}")
        dst_img = curated_dir / f"scene_{idx}.jpg"
        if not dst_img.exists():
            shutil.copy2(src_img, dst_img)

        out_wav = work_dir / f"raw_scene_{idx:02d}.wav"
        if not out_wav.exists() or out_wav.stat().st_size < 5000:
            print(f"  [Voicebox - {v_label}] Escena {idx}/{len(scenes)}: {sc['text'][:48]}...", flush=True)
            synthesize_voicebox_es(sc["text"], out_wav, profile_id=prof_id)
        raw_audios[idx] = out_wav

    raw_durs = [get_media_duration(raw_audios[i]) for i in range(1, len(scenes) + 1)]
    sum_raw = sum(raw_durs)
    # Gentle natural speed targeting ~75.0s
    speed = max(0.92, min(1.09, sum_raw / 75.0))
    print(f"  [Voicebox] Suma cruda: {sum_raw:.2f}s | Factor atempo: {speed:.3f}", flush=True)

    cal_dir = work_dir / "calibrated"
    cal_dir.mkdir(parents=True, exist_ok=True)
    voice_results = {}
    scene_items = []

    for idx, sc in enumerate(scenes, start=1):
        cal_w = cal_dir / f"scene_{idx:02d}.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_audios[idx]),
                "-af",
                f"atempo={speed:.3f}",
                "-c:a",
                "pcm_s16le",
                str(cal_w),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        dur = get_media_duration(cal_w)
        voice_results[idx] = {"audio": str(cal_w), "text": sc["text"]}
        scene_items.append({"image": curated_dir / f"scene_{idx}.jpg", "duration": dur})

    # Concatenate full narration
    full_audio = work_dir / "narration_full.wav"
    cmd_cat = ["ffmpeg", "-y"]
    f_parts = []
    for i in range(len(scenes)):
        cmd_cat.extend(["-i", voice_results[i + 1]["audio"]])
        f_parts.append(f"[{i}:a]")
    cmd_cat.extend(
        [
            "-filter_complex",
            "".join(f_parts) + f"concat=n={len(scenes)}:v=0:a=1[outa]",
            "-map",
            "[outa]",
            str(full_audio),
        ]
    )
    subprocess.run(cmd_cat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_audio_dur = get_media_duration(full_audio)
    print(f"  [Audio] Narración concatenada: {total_audio_dur:.2f}s", flush=True)

    # 2. Whisper Word Timings
    word_json = work_dir / "word_timings.json"
    words_data = extract_scene_word_timings(voice_results, str(word_json), language="es", model_name="base")
    words_timing = [{"word": w["text"], "start": w["start"], "end": w["end"]} for w in words_data.get("words", [])]

    # 3. Render with FilmCraft GPU (6500 kbps -> ~58-68 MB safely under GitHub 100 MB limit)
    q_dir.mkdir(parents=True, exist_ok=True)
    final_dur = assemble_filmcraft_reel(
        scene_items=scene_items,
        words_timing=words_timing,
        narration_audio=full_audio,
        output_mp4=v_out,
        work_dir=work_dir / "fc_work",
        hook_text=proj["hook_card"],
        hook_duration=7.0,
        seq_name=f"Lote1_Slot_{slot:02d}",
        bitrate_kbps=6500,
    )

    # 4. Generate Thumbnail & Metadata
    thumb_idx = proj.get("thumb_scene_idx", 0) + 1
    thumb_path = q_dir / "thumb.jpg"
    render_minimal_text_thumb(
        image_path=curated_dir / f"scene_{thumb_idx}.jpg",
        text=proj["thumb_text"],
        output_path=thumb_path,
        text_y=240,
        text_color=(255, 235, 0),
        font_size=82,
    )

    sz_mb = v_out.stat().st_size / (1024 * 1024)
    meta = {
        "slot": slot,
        "queue_folder": q_folder,
        "id": proj["id"],
        "title": proj["title"],
        "character": proj["character"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "duration": round(final_dur, 2),
        "size_mb": round(sz_mb, 2),
        "video_file": "video.mp4",
        "thumbnail_file": "thumb.jpg",
        "format": "filmcraft_75s_60fps",
        "voice_profile": f"Voicebox 0.6B ES ({v_label})",
        "voice_mode": voice_mode,
        "editor": "FilmCraft 0.20.1 GPU",
        "produced_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(m_out, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"✅ [SLOT {slot:02d} LISTO] {v_out.name} ({final_dur:.2f}s, {sz_mb:.1f} MB)", flush=True)
    return final_dur, sz_mb, "OK"


def main():
    start_all = time.time()
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    summary = []

    for proj in LOTE_01_PROJECTS:
        try:
            dur, sz, st = produce_project(proj)
            summary.append((proj["slot"], proj["queue_folder"], dur, sz, st))
        except Exception as e:
            print(f"❌ ERROR en Slot {proj['slot']}: {e}", flush=True)
            summary.append((proj["slot"], proj["queue_folder"], 0.0, 0.0, f"ERROR: {e}"))

    elapsed_min = (time.time() - start_all) / 60.0
    print("\n" + "=" * 78, flush=True)
    print(f"AUDITORÍA FINAL - LOTE 1 FILMCRAFT 75s ({elapsed_min:.1f} min)", flush=True)
    print("=" * 78, flush=True)
    for slot, qf, dur, sz, st in summary:
        print(f"Slot {slot:02d} | {dur:6.2f}s | {sz:6.1f} MB | {st:<10} | {qf}", flush=True)
    print("=" * 78, flush=True)


if __name__ == "__main__":
    main()
