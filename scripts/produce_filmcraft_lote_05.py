"""
Lote 5 Maestro: Top 20 Videos Más Virales de Facebook (Remake FilmCraft 60FPS + Voicebox)
=========================================================================================
Slots 41 al 60, ordenados estrictamente del #1 más viral (439,741 views) al #20 (18,123 views),
conservando exactamente los mismos hooks por los cuales se volvieron virales en Facebook,
expandidos a contexto completo (~71s-75s) en FilmCraft GPU 1080x1920 @ 60fps.
"""

import argparse
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

from src.filmcraft_engine import assemble_filmcraft_reel, get_media_duration
from src.transcribe import extract_scene_word_timings
from scripts.produce_lote_common import (
    PROFILE_REFERENCIA,
    PROFILE_ZAZOOM,
    render_minimal_text_thumb,
)
from scripts.produce_filmcraft_lote_01 import synthesize_voicebox_es

SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SRC = PROJECT_ROOT / "assets" / "comics_source"
SRC5 = PROJECT_ROOT / "assets" / "comics_source_lote5"


def _imgs(p: Path) -> list[Path]:
    return sorted(
        [
            x
            for x in p.rglob("*")
            if x.suffix.lower() in (".jpg", ".jpeg", ".png")
            and "zwater" not in x.name.lower()
        ]
    )


# Exact index-matched image pools (matching lote5_sheets)
S41 = _imgs(SRC5 / "041_superior_v1")
P51 = CURATED_BASE / "51_spiderman_escorpion_mandibula_superior"
FC04 = CURATED_BASE / "fc_04_batman_devastator_mata_superman"
S43 = _imgs(SRC5 / "043_hellboy_seed")
FC01 = CURATED_BASE / "fc_01_spiderman_back_in_black_kingpin"
FC06 = CURATED_BASE / "fc_06_sentry_descuartiza_ares_asgard"
SIEGE02 = SRC / "siege" / "extracted_siege_02"
FC03 = CURATED_BASE / "fc_03_batman_que_rie_origen_masacre"
S47 = _imgs(SRC5 / "047_thanos_rising")

_INJ_DIRS = sorted([d for d in (SRC5 / "048_injustice_y1").iterdir() if d.is_dir()])
S48 = sorted(list(_INJ_DIRS[-2].rglob("*.jpg")) + list(_INJ_DIRS[-1].rglob("*.jpg")))

S49 = _imgs(SRC5 / "049_knightsend")
FC02 = CURATED_BASE / "fc_02_secret_wars_doom_mata_thanos"
SW08 = SRC / "secret_wars_2015" / "pages" / "issue_08"

S51 = _imgs(SRC5 / "051_tower_babel")
PM = CURATED_BASE / "plastic_man_eel_obrian_resistencia_inmortal"
S52 = _imgs(SRC5 / "052_lobo_90" / "Lobo 01 (of 4) (1990) (The Last Czarnian)")

_F_DIRS = sorted(
    [d for d in (SRC5 / "053_flash_rebirth").iterdir() if d.is_dir() and "The Flash - Rebirth" in d.name]
)
S53 = [p for d in _F_DIRS for p in _imgs(d)]
RF_OLD = CURATED_BASE / "60_reverse_flash_odio_thawne"

_WWH_123 = sorted(
    [d for d in (SRC5 / "054_wwh").iterdir() if d.is_dir() and "World War Hulk #0" in d.name]
)
S54_A = [p for d in _WWH_123 for p in _imgs(d)]
_WWH_45 = []
for _dn in sorted([d.name for d in (SRC5 / "054_wwh").iterdir() if d.is_dir() and "hulk" in d.name.lower()]):
    if any(x in _dn for x in ["#04", "#05", "04", "05"]):
        _WWH_45.extend(sorted((SRC5 / "054_wwh" / _dn).rglob("*.jpg")))

S55 = _imgs(SRC5 / "055_knightfall_v2")
S56 = _imgs(SRC5 / "056_king_in_black_5")
S57 = _imgs(SRC5 / "057_thor_devourer")
S58 = _imgs(SRC5 / "058_identity_crisis")
S59 = _imgs(SRC5 / "059_thor_gorr_v1")

S60_1 = _imgs(SRC5 / "060_all_star" / "All Star Superman 001 (2006) (Digital) (Zone-Empire)")
S60_10 = sorted((SRC5 / "060_all_star" / "All Star Superman 010 (2008) (digital) (Minutemen-PhD)").glob("*.jpg"))
S60_12 = _imgs(SRC5 / "060_all_star" / "All Star Superman 012 (2008) (digital) (Minutemen-PhD)")
S60 = S60_1 + S60_10 + S60_12


LOTE_05_PROJECTS = [
    # #1 MOST VIRAL (439,741 views)
    {
        "slot": 41,
        "fb_views": 439741,
        "queue_folder": "041_fc_v1_superior_spiderman_mandibula",
        "id": "fc_41_v1_superior_spiderman_mandibula",
        "folder": "fc_41_v1_superior_spiderman_mandibula",
        "title": "¡Spider-Man Siempre se Contuvo! El Golpe que le Arrancó la Mandíbula a Escorpión 🕷️💥",
        "character": "Superior Spider-Man",
        "voice_mode": "referencia",
        "hook_card": "¿SABÍAS QUE SPIDER-MAN SIEMPRE CONTUVO SU FUERZA PARA NO MATAR?",
        "thumb_text": "MANDÍBULA ARRANCADA",
        "thumb_scene_idx": 4,
        "description": "Top #1 Viral (439K views) en FilmCraft 60fps: ¿Sabías que Spider-Man siempre usó una mínima fracción de su fuerza? Cuando Otto Octavius tomó su cuerpo, le arrancó la mandíbula al Escorpión.",
        "hashtags": "#SpiderMan #SuperiorSpiderMan #OttoOctavius #Escorpion #MarvelComics #Reels",
        "scenes": [
            {"src": S41[3], "text": "¿Sabías que Spider-Man siempre usó una mínima fracción de su fuerza para no matar? Todo cambió cuando Doctor Octopus robó su mente y su cuerpo."},
            {"src": S41[6], "text": "Tras dejar morir a Peter Parker en su viejo cuerpo enfermo, Otto Octavius juró demostrar que sería un Spider-Man superior en todos los sentidos."},
            {"src": P51 / "scene_01.jpg", "text": "Su primera prueba real llegó cuando el temible Escorpión irrumpió en el hospital amenazando con asesinar a Jonás Jameson y a todos los civiles."},
            {"src": P51 / "scene_02.jpg", "text": "Sin perder un segundo con chistes ni advertencias como hacía Peter, el nuevo Spider-Man saltó directo al cuello del villano decidido a acabar rápido."},
            {"src": P51 / "scene_03.jpg", "text": "Acostumbrado a pelear usando su armadura, Otto descargó un solo puñetazo sin frenar su poder... ¡y le arrancó la mandíbula entera al Escorpión!"},
            {"src": P51 / "scene_04.jpg", "text": "Viendo el hueso y la sangre caer al suelo ante el horror de todos, Otto observó sus propios nudillos completamente paralizado por el shock."},
            {"src": S41[18], "text": "En ese instante aterrador comprendió que Peter Parker siempre se contuvo en cada pelea para no matar a sus enemigos de un solo golpe."},
            {"src": S41[24], "text": "Aunque el fantasma de Peter intentaba frenarlo en silencio, el Spider-Man sin piedad había nacido. ¿Fue este el secreto más brutal de Marvel?"},
        ],
    },
    # #2 MOST VIRAL (398,206 views)
    {
        "slot": 42,
        "fb_views": 398206,
        "queue_folder": "042_fc_v2_batman_devastator_virus_doomsday",
        "id": "fc_42_v2_batman_devastator_virus_doomsday",
        "folder": "fc_42_v2_batman_devastator_virus_doomsday",
        "title": "¡Batman se Inyectó el Virus Doomsday! El Monstruo que Asesinó a Superman 🦇💀",
        "character": "Batman The Devastator",
        "voice_mode": "zazoom",
        "hook_card": "¡BATMAN SE INYECTÓ EL VIRUS DOOMSDAY PARA MATAR A SUPERMAN!",
        "thumb_text": "VIRUS DOOMSDAY",
        "thumb_scene_idx": 6,
        "description": "Top #2 Viral (398K views) en FilmCraft 60fps: Cuando un Superman enloquecido traicionó al mundo, Bruce Wayne se clavó el virus Doomsday para matar a su mejor amigo.",
        "hashtags": "#Batman #Superman #Doomsday #TheDevastator #DarkMultiverse #DCComics #Reels",
        "scenes": [
            {"src": FC04 / "scene_1.jpg", "text": "Cuando un Superman enloquecido traicionó al mundo y masacró a los héroes de la Tierra, Bruce Wayne tomó la decisión más trágica del Multiverso Oscuro."},
            {"src": FC04 / "scene_2.jpg", "text": "Cegado por una furia imparable, el Hombre de Acero asesinó incluso a Lois Lane frente a todos y desató un reinado de terror absoluto."},
            {"src": FC04 / "scene_3.jpg", "text": "Desesperado por frenar al dios caído, Batman intentó detenerlo con una lanza de kryptonita verde, pero Superman le arrancó el brazo de un rayo."},
            {"src": FC04 / "scene_4.jpg", "text": "Acorralado y sangrando entre los escombros de Gotham, Bruce sacó su último plan de contingencia prohibido: una jeringa cargada con el virus Doomsday."},
            {"src": FC04 / "scene_5.jpg", "text": "Sin dudarlo ni un segundo, Batman se la clavó directo en el pecho, sacrificando su humanidad para desatar a la única bestia capaz de matarlo."},
            {"src": FC04 / "scene_6.jpg", "text": "Huesos afilados rompieron su piel regenerando su brazo perdido mientras Bruce desaparecía dentro del coloso de roca imparable conocido como El Devastador."},
            {"src": FC04 / "scene_7.jpg", "text": "Ni la visión de calor ni los golpes sónicos pudieron herirlo; Batman aplastó a su excompañero empalándolo con púas gigantes y aliento de kryptonita."},
            {"src": FC04 / "scene_8.jpg", "text": "Convertido en monstruo sobre el cadáver de Superman, la pesadilla se extendió por todo el planeta. ¿Tenía otra opción Bruce Wayne para detenerlo?"},
        ],
    },
    # #3 MOST VIRAL (282,070 views)
    {
        "slot": 43,
        "fb_views": 282070,
        "queue_folder": "043_fc_v3_hellboy_mano_derecha_apocalipsis",
        "id": "fc_43_v3_hellboy_mano_derecha_apocalipsis",
        "folder": "fc_43_v3_hellboy_mano_derecha_apocalipsis",
        "title": "¡El Secreto de la Mano de Hellboy! La Llave del Apocalipsis 🔴🔑",
        "character": "Hellboy",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ LA MANO DE HELLBOY ES DE PIEDRA ROJA?",
        "thumb_text": "LLAVE DEL APOCALIPSIS",
        "thumb_scene_idx": 5,
        "description": "Top #3 Viral (282K views) en FilmCraft 60fps: ¿Por qué la mano de Hellboy es de piedra roja? El secreto oculto de la Mano Derecha del Destino y Anung Un Rama.",
        "hashtags": "#Hellboy #MikeMignola #AnungUnRama #DarkHorse #Comics #Reels",
        "scenes": [
            {"src": S43[5], "text": "¿Por qué la mano de Hellboy es de piedra roja? Todo comenzó en mil novecientos cuarenta y cuatro, cuando ocultistas nazis liderados por Rasputín abrieron un portal."},
            {"src": S43[7], "text": "Su ritual buscaba invocar a los dioses del caos, pero soldados aliados lograron rescatar entre las ruinas a un pequeño demonio recién nacido y huérfano."},
            {"src": S43[11], "text": "Criado como un investigador paranormal humano llamado Hellboy, todos creían que su descomunal brazo derecho de roca era solamente una curiosa deformidad."},
            {"src": S43[14], "text": "Aunque él mismo limaba sus cuernos para parecer normal y defendía al mundo de monstruos oscuros, su verdadero origen escondía una profecía devastadora."},
            {"src": S43[21], "text": "Esa mano indestructible no fue forjada para pelear contra bestias, pues es el último fragmento vivo de los antiguos espíritus que moldearon la Tierra."},
            {"src": S43[63], "text": "Su nombre real es Anung Un Rama, y su Mano Derecha del Destino es literalmente la llave sagrada diseñada para desatar el apocalipsis final."},
            {"src": S43[108], "text": "Cuando Rasputín lo encadenó en las cavernas ocultas intentando activar el sello del fin del mundo, las cadenas despertaron el poder dormido del abismo."},
            {"src": S43[111], "text": "Pero Hellboy rechazó su corona infernal eligiendo ser humano hasta el final, usando la llave del fin para aplastar al caos. ¿Es el mejor antihéroe?"},
        ],
    },
    # #4 MOST VIRAL (144,709 views)
    {
        "slot": 44,
        "fb_views": 144709,
        "queue_folder": "044_fc_v4_spiderman_back_in_black_kingpin",
        "id": "fc_44_v4_spiderman_back_in_black_kingpin",
        "folder": "fc_44_v4_spiderman_back_in_black_kingpin",
        "title": "¡Sin Máscara y Sin Piedad! Spider-Man Humilla a Kingpin en la Cárcel 🕷️⛓️",
        "character": "Spider-Man",
        "voice_mode": "zazoom",
        "hook_card": "¡SIN MÁSCARA Y SIN PIEDAD! SPIDER-MAN HUMILLÓ A KINGPIN",
        "thumb_text": "HUMILLÓ A KINGPIN",
        "thumb_scene_idx": 5,
        "description": "Top #4 Viral (144K views) en FilmCraft 60fps: Tras el disparo a la Tía May, Peter Parker vistió el traje negro y entró a Ryker's Island sin máscara.",
        "hashtags": "#SpiderMan #Kingpin #BackInBlack #PeterParker #MarvelComics #Reels",
        "scenes": [
            {"src": FC01 / "scene_1.jpg", "text": "Tras el disparo de un francotirador contra la Tía May, Peter Parker vistió el traje negro y entró a la prisión de Ryker buscando venganza."},
            {"src": FC01 / "scene_2.jpg", "text": "Wilson Fisk, el temido Kingpin del crimen, esperaba confiado rodeado por cientos de reclusos convencido de que el héroe jamás cruzaría la línea."},
            {"src": FC01 / "scene_3.jpg", "text": "En completo silencio y sin soltar un solo chiste, Spider-Man cayó directo al patio frente a toda la cárcel en la pelea más esperada."},
            {"src": FC01 / "scene_4.jpg", "text": "Antes de atacar, Peter se quitó la máscara mirando a los ojos a Fisk: hoy no venía como Spider-Man, sino como un hombre dispuesto a matar."},
            {"src": FC01 / "scene_5.jpg", "text": "Kingpin lanzó golpes mortales creyendo que su masa aplastaría al joven, pero Peter esquivó cada puñetazo con una velocidad humillante frente a todos."},
            {"src": FC01 / "scene_6.jpg", "text": "Lo levantó por la piel del pecho y lo molió a bofetadas y golpes brutales, rompiéndole las costillas mientras los presos miraban en absoluto silencio."},
            {"src": FC01 / "scene_7.jpg", "text": "Agarrando a Fisk del cuello al borde de la asfixia, Peter le juró que si su tía moría, volvería para llenarle los pulmones de telaraña."},
            {"src": FC01 / "scene_8.jpg", "text": "Dejando al rey del crimen sangrando e inconsciente ante toda la prisión, Peter demostró por qué nunca debes romper su paciencia. ¿Merecía Fisk más?"},
        ],
    },
    # #5 MOST VIRAL (117,727 views)
    {
        "slot": 45,
        "fb_views": 117727,
        "queue_folder": "045_fc_v5_sentry_descuartiza_ares_siege",
        "id": "fc_45_v5_sentry_descuartiza_ares_siege",
        "folder": "fc_45_v5_sentry_descuartiza_ares_siege",
        "title": "¡La Muerte Más Censurada de Marvel! Sentry Descuartiza a Ares en Dos Mitades ⚡🩸",
        "character": "Sentry",
        "voice_mode": "referencia",
        "hook_card": "¡LA MUERTE MÁS CENSURADA DE MARVEL! SENTRY PARTIÓ EN DOS A ARES",
        "thumb_text": "PARTIDO EN DOS",
        "thumb_scene_idx": 6,
        "description": "Top #5 Viral (117K views) en FilmCraft 60fps: En el clímax del Asedio de Asgard, Sentry fue consumido por The Void y partió en dos a Ares.",
        "hashtags": "#Sentry #Ares #Siege #TheVoid #MarvelComics #Reels",
        "scenes": [
            {"src": FC06 / "scene_1.jpg", "text": "En el clímax del Asedio de Asgard, Sentry fue consumido por la entidad The Void y cometió el acto más perturbador de todo Marvel."},
            {"src": FC06 / "scene_2.jpg", "text": "Al descubrir que Norman Osborn lo manipuló para invadir el hogar de los dioses, el Dios de la Guerra Ares juró arrancarle la cabeza."},
            {"src": FC06 / "scene_3.jpg", "text": "Pero antes de llegar al tirano, descendió de los cielos el guerrero con la fuerza de un millón de soles explotando: Robert Reynolds."},
            {"src": FC06 / "scene_4.jpg", "text": "Ares no dudó ni un instante y chocó en el cielo contra Sentry con una ferocidad capaz de sacudir las murallas doradas de Asgard."},
            {"src": FC06 / "scene_5.jpg", "text": "Descargando golpes con su hacha divina directamente contra el pecho del coloso, Ares creyó tener ventaja cuando la sangre comenzó a brotar."},
            {"src": FC06 / "scene_6.jpg", "text": "Sin embargo, el dolor solo despertó por completo a The Void, quien sujetó al dios por la cintura inmovilizándolo frente a todos los héroes."},
            {"src": FC06 / "scene_7.jpg", "text": "Con sus propias manos desnudas, Sentry tomó al Dios de la Guerra y lo partió brutalmente por la mitad en una lluvia de sangre."},
            {"src": SIEGE02 / "Siege 02-016.jpg", "text": "Los Vengadores observaron petrificados cómo caían las dos mitades de un inmortal. ¿Es esta realmente la muerte más salvaje que publicó Marvel?"},
        ],
    },
    # #6 MOST VIRAL (103,677 views)
    {
        "slot": 46,
        "fb_views": 103677,
        "queue_folder": "046_fc_v6_el_batman_que_rie_origen",
        "id": "fc_46_v6_el_batman_que_rie_origen",
        "folder": "fc_46_v6_el_batman_que_rie_origen",
        "title": "¡El Batman Que Ríe! La Fusión Más Siniestra entre Bruce Wayne y el Joker 🃏🦇",
        "character": "Batman Que Ríe",
        "voice_mode": "zazoom",
        "hook_card": "¡LA FUSIÓN MÁS SINIESTRA ENTRE BRUCE WAYNE Y EL JOKER!",
        "thumb_text": "EL BATMAN QUE RÍE",
        "thumb_scene_idx": 7,
        "description": "Top #6 Viral (103K views) en FilmCraft 60fps: Al matar al Joker, una toxina cardíaca infectó a Bruce Wayne creando al Batman Que Ríe.",
        "hashtags": "#BatmanQueRie #TheBatmanWhoLaughs #Batman #Joker #DCComics #Reels",
        "scenes": [
            {"src": FC03 / "scene_1.jpg", "text": "Al matar al Joker, una toxina cardíaca infectó a Bruce Wayne, combinando el intelecto del mejor estratega con la psicopatía pura del payaso del crimen."},
            {"src": FC03 / "scene_2.jpg", "text": "Todo ocurrió en la Tierra menos veintidós cuando el Joker destruyó Gotham entera, asesinando al Comisionado Gordon y obligando a Bruce a presenciar el horror."},
            {"src": FC03 / "scene_3.jpg", "text": "Por primera vez en su historia, Batman rompió su regla sagrada y le quebró el cuello al Joker, sin saber que liberaba una trampa química."},
            {"src": FC03 / "scene_4.jpg", "text": "Días después en la Baticueva, la toxina comenzó a borrar la empatía de Bruce mientras su cerebro intacto mantenía cada plan táctico contra sus aliados."},
            {"src": FC03 / "scene_5.jpg", "text": "Cuando Nightwing, Batgirl y Red Hood notaron su macabra sonrisa e intentaron detenerlo, Bruce respondió sacando ametralladoras ocultas en la oscuridad."},
            {"src": FC03 / "scene_6.jpg", "text": "En segundos ejecutó sin piedad a toda su propia Batifamilia dentro de su hogar, riendo sin parar mientras la sangre cubría las computadoras."},
            {"src": FC03 / "scene_7.jpg", "text": "Después masacró a la Liga de la Justicia y obligó a Superman con kryptonita negra a asesinar a Lois Lane y a su propio hijo."},
            {"src": FC03 / "scene_8.jpg", "text": "Dejando un mundo de cenizas encadenado por Robins salvajes, nació el Batman Que Ríe. ¿Es este el villano más aterrador de todo DC?"},
        ],
    },
    # #7 MOST VIRAL (100,314 views)
    {
        "slot": 47,
        "fb_views": 100314,
        "queue_folder": "047_fc_v7_thanos_rising_origen_muerte",
        "id": "fc_47_v7_thanos_rising_origen_muerte",
        "folder": "fc_47_v7_thanos_rising_origen_muerte",
        "title": "Thanos: El Perturbador Origen y la Obsesión con la Muerte 💀🌌",
        "character": "Thanos",
        "voice_mode": "referencia",
        "hook_card": "EL PERTURBADOR ORIGEN DE THANOS Y SU OBSESIÓN CON LA MUERTE",
        "thumb_text": "ORIGEN DE THANOS",
        "thumb_scene_idx": 3,
        "description": "Top #7 Viral (100K views) en FilmCraft 60fps: Nacido como una anomalía en Titán, Thanos comenzó diseccionando criaturas hasta enamorarse de la Muerte.",
        "hashtags": "#Thanos #ThanosRising #LadyDeath #MarvelComics #Comics #Reels",
        "scenes": [
            {"src": S47[6], "text": "Nacido como una anomalía genética en la pacífica luna Titán, Thanos fue rechazado desde el primer segundo por el horror que inspiraba su piel púrpura."},
            {"src": S47[21], "text": "Aunque intentó ser un niño amable y brillante junto a sus compañeros, el rechazo constante y las pesadillas nocturnas fueron pudriendo su mente solitaria."},
            {"src": S47[27], "text": "Convencido por una misteriosa niña encapuchada de enfrentar su miedo a la sangre, bajó a las cavernas ocultas donde comenzó a cazar bestias."},
            {"src": S47[36], "text": "Pronto los animales no fueron suficientes; obsesionado por descifrar por qué era diferente, secuestró y diseccionó vivos a sus propios amigos en secreto."},
            {"src": S47[51], "text": "Aquella joven resultó ser la mismísima Señora Muerte personificada, quien lo manipuló prometiéndole su amor solo si le entregaba millones de almas."},
            {"src": S47[66], "text": "Thanos recorrió el cosmos como un pirata sanguinario dejando planetas estériles y cadáveres, pero la Muerte jamás quedaba satisfecha con sus sacrificios."},
            {"src": S47[99], "text": "Ciego por ganar su corazón, regresó con su flota al mundo que lo vio nacer y desató un bombardeo nuclear que extinguió toda Titán."},
            {"src": S47[114], "text": "Tras asesinar incluso a su propia madre y padre, el Titán Loco descubrió la verdad de su condena. ¿Nació malvado Thanos o lo destruyeron?"},
        ],
    },
    # #8 MOST VIRAL (97,979 views)
    {
        "slot": 48,
        "fb_views": 97979,
        "queue_folder": "048_fc_v8_injustice_alfred_humilla_superman",
        "id": "fc_48_v8_injustice_alfred_humilla_superman",
        "folder": "fc_48_v8_injustice_alfred_humilla_superman",
        "title": "¡Alfred Humilló a Superman! El Mayordomo que le Rompió la Nariz al Hombre de Acero 👊💥",
        "character": "Alfred Pennyworth",
        "voice_mode": "zazoom",
        "hook_card": "¡ALFRED HUMILLÓ A SUPERMAN Y LE REVENTÓ LA NARIZ!",
        "thumb_text": "HUMILLÓ A SUPERMAN",
        "thumb_scene_idx": 5,
        "description": "Top #8 Viral (98K views) en FilmCraft 60fps: Cuando Superman le rompió la espalda a Batman en la Baticueva, Alfred tomó la píldora 5-U-93-R y lo molió a golpes.",
        "hashtags": "#AlfredPennyworth #Superman #Injustice #Batman #DCComics #Reels",
        "scenes": [
            {"src": S48[6], "text": "Cuando un Superman cegado por la tiranía irrumpió en la Baticueva para destruir los planes de la resistencia, nadie creyó que algo pudiera frenarlo."},
            {"src": S48[15], "text": "Mientras los servidores procesaban el secreto de las píldoras kryptonianas, Bruce Wayne luchó con todo lo que tenía para ganar unos segundos vitales."},
            {"src": S48[21], "text": "Furioso por su desafío, Superman atrapó al Caballero de la Noche en el aire y le rompió brutalmente la espalda sobre su rodilla."},
            {"src": S48[31], "text": "Con Bruce indefenso en el suelo, el dictador se acercó confiado para darle el golpe de gracia... sin notar quién lo esperaba en las sombras."},
            {"src": S48[35], "text": "Alfred Pennyworth había ingerido en silencio la píldora cinco-U-nueve-tres-R de nanotecnología kryptoniana, obteniendo la misma fuerza de un dios."},
            {"src": S48[36], "text": "Sin pronunciar palabra, el fiel mayordomo le propinó un cabezazo atronador que le reventó la nariz al Hombre de Acero en un estallido de sangre."},
            {"src": S48[38], "text": "Atrapado por la sorpresa y el dolor, Superman cayó al suelo mientras Alfred lo molía a puñetazos y pisotones rompiéndole la bota encima de su cara."},
            {"src": S48[40], "text": "Tras advertirle que jamás volvería a lastimar a su familia, Alfred rescató a Bruce. ¿Es Alfred Pennyworth el mejor personaje de todo DC?"},
        ],
    },
    # #9 MOST VIRAL (76,077 views)
    {
        "slot": 49,
        "fb_views": 76077,
        "queue_folder": "049_fc_v9_bruce_wayne_reclama_gotham_azrael",
        "id": "fc_49_v9_bruce_wayne_reclama_gotham_azrael",
        "folder": "fc_49_v9_bruce_wayne_reclama_gotham_azrael",
        "title": "¡Bruce Wayne Reclama Gotham! El Retorno del Verdadero Defensor de la Noche 🦇⚔️",
        "character": "Bruce Wayne",
        "voice_mode": "referencia",
        "hook_card": "¡BRUCE WAYNE REGRESÓ PARA ARRANCARLE EL MANTO A AZRAEL!",
        "thumb_text": "REGRESA EL VERDADERO",
        "thumb_scene_idx": 6,
        "description": "Top #9 Viral (76K views) en FilmCraft 60fps: Tras meses de rehabilitación física y mental, Bruce Wayne volvió para derrotar al violento Azrael en KnightsEnd.",
        "hashtags": "#Batman #BruceWayne #Azrael #KnightsEnd #Knightfall #DCComics #Reels",
        "scenes": [
            {"src": S49[252], "text": "Tras meses de dolorosa rehabilitación física y mental después de que Bane le quebrara la columna, Bruce Wayne regresó finalmente para reclamar Gotham City."},
            {"src": S49[261], "text": "Durante su ausencia, Jean-Paul Valley había deshonrado el símbolo del murciélago convirtiéndolo en una máquina armada con cuchillas que dejaba morir criminales."},
            {"src": S49[276], "text": "Con el corazón de la ciudad al borde del caos, el verdadero Batman descendió a las profundidades oscuras de su propia cueva buscando al impostor."},
            {"src": S49[282], "text": "Frente a frente bajo las sombras de la mansión Wayne, Jean-Paul rechazó devolver el manto creyendo que la nueva armadura letal lo volvía invencible."},
            {"src": S49[288], "text": "En un combate brutal entre pasadizos estrechos, Bruce usó su entrenamiento clásico enfrentando lanzallamas, garras de acero y pura fuerza desquiciada."},
            {"src": S49[294], "text": "Sabiendo que no podía vencer una armadura pesada a golpes directos, el detective llevó la pelea hasta el túnel más estrecho de la Baticueva."},
            {"src": S49[297], "text": "Allí Bruce quitó su cinturón y abrió de golpe la compuerta superior, inundando la cueva entera con una cegadora ráfaga de luz solar."},
            {"src": S49[300], "text": "Incapaz de soportar el brillo al quitarse el casco, Azrael cayó de rodillas reconociendo al verdadero Batman. ¿Fue este el mejor regreso de Bruce?"},
        ],
    },
    # #10 MOST VIRAL (72,766 views)
    {
        "slot": 50,
        "fb_views": 72766,
        "queue_folder": "050_fc_v10_secret_wars_doom_mata_thanos",
        "id": "fc_50_fc_v10_secret_wars_doom_mata_thanos" if False else "050_fc_v10_secret_wars_doom_mata_thanos",
        "id": "fc_50_v10_secret_wars_doom_mata_thanos",
        "folder": "fc_50_v10_secret_wars_doom_mata_thanos",
        "title": "¡El Peor Error de Thanos! Desafió a Doctor Doom Dios y Pagó el Precio ⚡🩸",
        "character": "Doctor Doom",
        "voice_mode": "zazoom",
        "hook_card": "¡EL PEOR ERROR DE THANOS! DESAFIÓ A DIOS DOOM SIN EL GUANTELETE",
        "thumb_text": "COLUMNA ARRANCADA",
        "thumb_scene_idx": 4,
        "description": "Top #10 Viral (72K views) en FilmCraft 60fps: En Battleworld, Thanos creyó superar el poder de Dios Emperador Doom y terminó hecho polvo.",
        "hashtags": "#DoctorDoom #Thanos #SecretWars #GodEmperorDoom #MarvelComics #Reels",
        "scenes": [
            {"src": FC02 / "scene_1.jpg", "text": "En Battleworld, Thanos creyó que su ego superaba el poder de los Beyonders y cometió el peor error de su existencia frente al Dios Emperador Doom."},
            {"src": FC02 / "scene_2.jpg", "text": "Mientras los ejércitos rebeldes destruían las murallas del castillo real, Victor Von Doom descendió con absoluta calma para enfrentar la amenaza."},
            {"src": FC02 / "scene_3.jpg", "text": "Rodeado de sus hordas, el Titán Loco se burló en la cara de Doom llamándolo un simple mortal disfrazado con poder robado."},
            {"src": FC02 / "scene_4.jpg", "text": "Sin perder la compostura ni un segundo, Doom lo miró desde arriba y le hizo una sola pregunta letal: ¿tienes el Guantelete del Infinito contigo?"},
            {"src": FC02 / "scene_5.jpg", "text": "Cuando Thanos respondió orgulloso que no necesitaba gemas para aplastarlo, Doom sonrió respondiendo que entonces ese era su final... ¡y le arrancó la columna!"},
            {"src": FC02 / "scene_6.jpg", "text": "En un parpadeo aterrador, la mano blindada atravesó su pecho reduciendo al titán más temido del universo a un montón de huesos y polvo."},
            {"src": FC02 / "scene_7.jpg", "text": "Con el cráneo de Thanos aún ardiendo en su mano ante la rebelión congelada del miedo, Victor ordenó continuar la guerra sin piedad."},
            {"src": SW08 / "Secret Wars (2015-) 008-024.jpg", "text": "Nadie en la historia había humillado así al Titán Loco en un solo segundo. ¿Es Dios Doom el villano más supremo de Marvel?"},
        ],
    },
    # #11 MOST VIRAL (51,901 views)
    {
        "slot": 51,
        "fb_views": 51901,
        "queue_folder": "051_fc_v11_plastic_man_terror_batman",
        "id": "fc_51_v11_plastic_man_terror_batman",
        "folder": "fc_51_v11_plastic_man_terror_batman",
        "title": "Plastic Man: ¡El Terror Oculto de Batman en la Liga de la Justicia! 🕶️⚠️",
        "character": "Plastic Man",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ BATMAN LE TEME A PLASTIC MAN?",
        "thumb_text": "EL TERROR DE BATMAN",
        "thumb_scene_idx": 3,
        "description": "Top #11 Viral (51.9K views) en FilmCraft 60fps: En sus archivos secretos, Batman confiesa la verdad sobre Plastic Man, un ser inmortal imposible de matar.",
        "hashtags": "#PlasticMan #Batman #JusticeLeague #TowerOfBabel #DCComics #Reels",
        "scenes": [
            {"src": S51[0], "text": "En sus archivos secretos de contingencia, Batman confiesa la aterradora verdad sobre Plastic Man: el único héroe al que ninguna fuerza puede aniquilar."},
            {"src": PM / "scene_01.jpg", "text": "Aunque frente a la Liga de la Justicia Eel O'Brian finge ser solo un payaso inofensivo con gafas oscuras, su cuerpo desafía toda lógica biológica."},
            {"src": S51[54], "text": "Incluso durante el ataque de Ra's al Ghul en La Torre de Babel, cuando cada héroe fue neutralizado con trampas mortales, Plastic Man siguió resistiendo."},
            {"src": PM / "scene_02.jpg", "text": "Sus moléculas elásticas son prácticamente eternas: no envejece, no sangra, es inmune al control mental y puede cambiar a cualquier tamaño o arma."},
            {"src": PM / "scene_03.jpg", "text": "En la saga La Era de Obsidiana, fue congelado y despedazado en mil fragmentos bajo el océano durante tres mil años... y despertó intacto."},
            {"src": S51[69], "text": "Por eso Batman escribió con alarma que la única medida contra él es congelarlo con nitrógeno líquido, sabiendo que solo retrasaría lo inevitable."},
            {"src": PM / "scene_04.jpg", "text": "En su informe más oscuro, Bruce advirtió que si perdiera la razón podría infiltrarse microscópicamente por la garganta de cualquiera y destruirlo desde adentro."},
            {"src": S51[90], "text": "Ni Superman ni Flash tienen una defensa real contra una pesadilla inmortal así. ¿Creías que Plastic Man escondía un poder tan aterrador?"},
        ],
    },
    # #12 MOST VIRAL (50,582 views)
    {
        "slot": 52,
        "fb_views": 50582,
        "queue_folder": "052_fc_v12_lobo_genocidio_czarnia",
        "id": "fc_52_v12_lobo_genocidio_czarnia",
        "folder": "fc_52_v12_lobo_genocidio_czarnia",
        "title": "Lobo: El Genocidio de Czarnia 💀🩸🚀",
        "character": "Lobo",
        "voice_mode": "zazoom",
        "hook_card": "¿CÓMO EXTINGUIÓ LOBO A TODO SU PLANETA?",
        "thumb_text": "GENOCIDIO CZARNIA",
        "thumb_scene_idx": 5,
        "description": "Top #12 Viral (50.5K views) en FilmCraft 60fps: Descubre la retorcida verdad de cómo Lobo extinguió a toda su pacífica civilización por una razón sádica.",
        "hashtags": "#Lobo #Czarnia #TheMainMan #DCComics #Comics #Reels",
        "scenes": [
            {"src": S52[0], "text": "Descubre la oscura y retorcida verdad de cómo Lobo extinguió a toda su pacífica civilización de cinco mil millones de habitantes por pura diversión."},
            {"src": S52[1], "text": "El planeta Czarnia era el paraíso más perfecto de la galaxia: una utopía inmortal donde no existían la violencia, las enfermedades ni el crimen."},
            {"src": S52[2], "text": "Hasta que nació una anomalía genética absoluta cuyo primer acto al salir del vientre fue arrancarle cuatro dedos a mordiscos a la partera."},
            {"src": S52[7], "text": "A medida que crecía odiando la paz infinita de sus vecinos, el joven Lobo diseñó en secreto una plaga biológica dentro de su laboratorio escolar."},
            {"src": S52[8], "text": "Creó un enjambre microscópico de escorpiones voladores cuyo veneno causaba una muerte lenta y agonizante en cualquier ser czarniano que picaran."},
            {"src": S52[9], "text": "Liberando millones de insectos sobre todo el planeta como su proyecto científico final, desató el caos mientras observaba riendo desde las azoteas."},
            {"src": S52[12], "text": "En menos de una semana murieron los cinco mil millones de habitantes y Lobo obtuvo una calificación perfecta de sobresaliente en su clase."},
            {"src": S52[24], "text": "Autoproclamándose El Último Czarniano, despegó en su motocicleta espacial buscando cazar por toda la galaxia. ¿Es Lobo el antihéroe más sádico de DC?"},
        ],
    },
    # #13 MOST VIRAL (50,319 views)
    {
        "slot": 53,
        "fb_views": 50319,
        "queue_folder": "053_fc_v13_flash_reverso_destruye_barry",
        "id": "fc_53_v13_flash_reverso_destruye_barry",
        "folder": "fc_53_v13_flash_reverso_destruye_barry",
        "title": "¡El Villano Más Retorcido de DC! Por Qué Flash Reverso Destruyó la Vida de Barry Allen ⚡🔪",
        "character": "Reverse Flash",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ FLASH REVERSO ARRUINÓ A BARRY ALLEN?",
        "thumb_text": "ODIO DE THAWNE",
        "thumb_scene_idx": 5,
        "description": "Top #13 Viral (50.3K views) en FilmCraft 60fps: La obsesión enferma de Eobard Thawne viajando en el tiempo para arruinar cada instante de la vida de Barry Allen.",
        "hashtags": "#ReverseFlash #Flash #BarryAllen #EobardThawne #DCComics #Reels",
        "scenes": [
            {"src": S53[0], "text": "La obsesión de Eobard Thawne no tenía límites: viajó por el tiempo para destruir cada segundo de la vida del hombre que admiraba, Barry Allen."},
            {"src": S53[24], "text": "Cuando Barry finalmente regresó de la Speed Force tras sacrificarse en la Crisis, el mundo parecía celebrar por fin su milagroso retorno."},
            {"src": S53[40], "text": "Sin embargo, la historia de su familia había cambiado brutalmente, despertando una herida abierta sobre el asesinato nunca resuelto de su madre."},
            {"src": S53[84], "text": "Envuelto en rayos rojos de la Fuerza de Velocidad Negativa, Flash Reverso reapareció burlándose de la inocencia del velocista escarlata."},
            {"src": S53[92], "text": "Eobard le confesó la verdad más enferma: como las reglas temporales le impedían matar al Barry adulto sin borrarse a sí mismo, atacó su infancia."},
            {"src": S53[108], "text": "Viajó atrás para empujar al pequeño Barry por las escaleras, incendiar su casa, matar a su perro y borrar de la existencia a su mejor amigo."},
            {"src": S53[120], "text": "Pero su golpe maestro fue apuñalar a Nora Allen directamente en el corazón e incriminar al padre inocente de Barry en prisión."},
            {"src": S53[136], "text": "Aunque Flash logró vencerlo junto a toda su familia, el trauma quedó grabado para siempre. ¿Existe un odio más enfermo que el de Reverse Flash?"},
        ],
    },
    # #14 MOST VIRAL (48,344 views)
    {
        "slot": 54,
        "fb_views": 48344,
        "queue_folder": "054_fc_v14_world_war_hulk_illuminati",
        "id": "fc_54_v14_world_war_hulk_illuminati",
        "folder": "fc_54_v14_world_war_hulk_illuminati",
        "title": "¡Hulk Aplasta a los Illuminati! La Venganza de World War Hulk 🟢👑",
        "character": "Hulk",
        "voice_mode": "zazoom",
        "hook_card": "¡TRAICIONADO AL ESPACIO! LA VENGANZA DE WORLD WAR HULK",
        "thumb_text": "APLASTÓ A TODOS",
        "thumb_scene_idx": 2,
        "description": "Top #14 Viral (48.3K views) en FilmCraft 60fps: Traicionado y exiliado por sus amigos, Hulk regresó con armadura de gladiador para humillar a los Illuminati.",
        "hashtags": "#WorldWarHulk #Hulk #Illuminati #MarvelComics #Comics #Reels",
        "scenes": [
            {"src": S54_A[0], "text": "Traicionado y exiliado al espacio por sus propios amigos, Hulk regresó a la Tierra con armadura de gladiador para humillar y someter a los Illuminati."},
            {"src": S54_A[15], "text": "Primero aplastó sin piedad a Black Bolt en la Luna tras recibir de frente su grito sónico, avisando a Nueva York que venía por los culpables."},
            {"src": S54_A[25], "text": "Cuando Iron Man salió al cielo usando su armadura Hulkbuster más poderosa equipada con nanobots inhibidores, la pelea duró apenas unos segundos."},
            {"src": S54_A[35], "text": "Hulk destrozó el reactor del traje a puñetazos limpios y derrumbó entera la Torre Stark reduciendo el símbolo de Tony a puro polvo."},
            {"src": S54_A[55], "text": "Desesperado por frenar al gigante verde antes de que destruyera Manhattan, Doctor Strange invocó la magia oscura prohibida del demonio Zom."},
            {"src": S54_A[60], "text": "Aun poseído por fuerzas infernales, Strange terminó aplastado cuando Hulk le rompió ambas manos para impedirle lanzar cualquier otro hechizo."},
            {"src": _WWH_45[81], "text": "Luego encadenó a Iron Man, Reed Richards y Black Bolt con discos de obediencia en un coliseo obligándolos a matarse frente al mundo."},
            {"src": _WWH_45[126], "text": "Incluso cuando Sentry descendió del cielo descargando un millón de soles en un empate épico, la ira de Hulk ya había vencido. ¿Tenía razón?"},
        ],
    },
    # #15 MOST VIRAL (43,775 views)
    {
        "slot": 55,
        "fb_views": 43775,
        "queue_folder": "055_fc_v15_azrael_batman_destroza_bane",
        "id": "fc_55_v15_azrael_batman_destroza_bane",
        "folder": "fc_55_v15_azrael_batman_destroza_bane",
        "title": "¡El Batman Dorado de Azrael! Jean-Paul Valley Destrozó a Bane con Cuchillas y Fuego 🦇⚔️",
        "character": "Azrael Batman",
        "voice_mode": "referencia",
        "hook_card": "¡AZRAEL DESTROZÓ A BANE CON CUCHILLAS Y FUEGO!",
        "thumb_text": "DESTROZÓ A BANE",
        "thumb_scene_idx": 5,
        "description": "Top #15 Viral (43.7K views) en FilmCraft 60fps: Tras la caída de Bruce Wayne, Jean-Paul Valley construyó una armadura letal y pulverizó a Bane.",
        "hashtags": "#Azrael #Batman #Bane #Knightfall #DCComics #Reels",
        "scenes": [
            {"src": S55[244], "text": "Tras la caída de Bruce Wayne, Jean-Paul Valley reemplazó a Batman construyendo una aterradora armadura armada con garras y lanzallamas para imponer justicia despiadada."},
            {"src": S55[246], "text": "Durante semanas Bane gobernó las calles de Gotham City convencido de que el legendario murciélago había sido borrado definitivamente tras partirle la espalda."},
            {"src": S55[274], "text": "Sin embargo, el antiguo asesino de la Orden de San Dumas evolucionó el traje clásico hacia una máquina blindada llena de cuchillas afiladas."},
            {"src": S55[276], "text": "Patrullando desde los rascacielos con su capa metálica y un visor infrarrojo letal, Azrael rastreó al dictador de Santa Prisca sin descanso."},
            {"src": S55[284], "text": "Cuando ambos colosos chocaron en un tren nocturno y en las azoteas de Gotham, Bane descubrió aterrado que este Batman no contenía sus golpes."},
            {"src": S55[292], "text": "Ignorando el código moral de Bruce, Jean-Paul atacó con ráfagas cortantes y rebanó por completo las mangueras que bombeaban el suero Venom."},
            {"src": S55[294], "text": "Sin su droga venenosa en las venas, el cuerpo gigante de Bane colapsó sangrando mientras las cuchillas doradas desgarrraban su orgullo ante toda la ciudad."},
            {"src": S55[300], "text": "A punto de matarlo a sangre fría antes de contenerse por última vez, Azrael reclamó la noche. ¿Preferías su brutalidad o las reglas de Bruce?"},
        ],
    },
    # #16 MOST VIRAL (40,542 views)
    {
        "slot": 56,
        "fb_views": 40542,
        "queue_folder": "056_fc_v16_venom_dios_de_la_luz_knull",
        "id": "fc_56_v16_venom_dios_de_la_luz_knull",
        "folder": "fc_56_v16_venom_dios_de_la_luz_knull",
        "title": "¡El Hacha de Luz que Destruyó la Oscuridad! La Apoteosis Cósmica en King in Black 🤍⚡",
        "character": "Venom Dios de la Luz",
        "voice_mode": "zazoom",
        "hook_card": "¡EL HACHA DE LUZ QUE MATÓ AL DIOS SIMBIONTE!",
        "thumb_text": "DIOS DE LA LUZ",
        "thumb_scene_idx": 3,
        "description": "Top #16 Viral (40.5K views) en FilmCraft 60fps: Cuando Knull conquistó la Tierra, la Fuerza Enigma resucitó a Eddie Brock como el Dios de la Luz.",
        "hashtags": "#Venom #KingInBlack #Knull #EddieBrock #MarvelComics #Reels",
        "scenes": [
            {"src": S56[1], "text": "Cuando Knull conquistó la Tierra con oscuridad absoluta, la legendaria Fuerza Enigma eligió y resucitó a Eddie Brock como el Dios de la Luz."},
            {"src": S56[3], "text": "Minutos antes, los Vengadores y los X-Men parecían condenados tras ver al creador de los simbiontes partir a Sentry y encerrar al planeta."},
            {"src": S56[5], "text": "Pero desde la mente colectiva surgió un Venom blanco bañado en llamas estelares, portando todo el poder del Capitán Universo en sus venas."},
            {"src": S56[7], "text": "En plena batalla en el cielo, Eddie arrancó la tabla de Silver Surfer y el Mjolnir de Thor para fundirlos en un hacha cósmica."},
            {"src": S56[10], "text": "Desgarrando hordas enteras de dragones simbiontes de un solo tajo luminoso, el nuevo dios iluminó la noche entera de Nueva York."},
            {"src": S56[15], "text": "Al chocar frente a frente contra la Necroespada de Knull, Eddie partió su armadura oscura en pedazos y le desintegró los brazos al tirano."},
            {"src": S56[20], "text": "Agarrando al inmortal rey del abismo por la garganta, Venom voló a máxima velocidad rompiendo la atmósfera directo hacia el centro del Sol."},
            {"src": S56[21], "text": "Allí arrojó a Knull dentro del fuego solar borrándolo para siempre de la existencia. ¿Fue esta la transformación más épica de Eddie Brock?"},
        ],
    },
    # #17 MOST VIRAL (31,749 views)
    {
        "slot": 57,
        "fb_views": 31749,
        "queue_folder": "057_fc_v17_thor_asesino_a_galactus",
        "id": "fc_57_v17_thor_asesino_a_galactus",
        "folder": "fc_57_v17_thor_asesino_a_galactus",
        "title": "¡Thor Asesinó a Galactus! La Brutal Ejecución del Devorador de Mundos ⚡👑",
        "character": "Thor",
        "voice_mode": "referencia",
        "hook_card": "¡EL DÍA QUE THOR ASESINÓ A GALACTUS!",
        "thumb_text": "EJECUTÓ A GALACTUS",
        "thumb_scene_idx": 6,
        "description": "Top #17 Viral (31.7K views) en FilmCraft 60fps: Tras ser nombrado Heraldo del Trueno, el Rey Thor drenó el Poder Cósmico de Galactus y lo ejecutó.",
        "hashtags": "#Thor #Galactus #HeraldOfThunder #MarvelComics #Asgard #Reels",
        "scenes": [
            {"src": S57[3], "text": "Tras ser nombrado Heraldo del Trueno para enfrentar al Invierno Negro, Thor descubrió el terrible secreto detrás de la existencia de Galactus."},
            {"src": S57[18], "text": "El gigantesco Devorador de Mundos había recurrido al nuevo Rey de Asgard, entregándole una fracción infinita del Poder Cósmico para frenar el fin universal."},
            {"src": S57[90], "text": "Juntos viajaron al borde de la creación devorando cinco planetas especiales mientras las explosiones cósmicas sacudían las galaxias vecinas."},
            {"src": S57[94], "text": "Sin embargo, cuando la nube oscura del Invierno Negro apareció frente a ellos, confesó que Galactus era solamente su heraldo esclavo."},
            {"src": S57[116], "text": "Harto de haber sido usado y traicionado para destruir mundos inocentes por miedo de su maestro, el Dios del Trueno tomó una decisión letal."},
            {"src": S57[122], "text": "En lugar de dejarlo huir, Thor sujetó al gigante cósmico y comenzó a drenarle hasta la última gota de Poder Cósmico dejándolo seco."},
            {"src": S57[126], "text": "Convertido en una bomba viva de energía blanca, Thor descargó toda la fuerza divina y voló en mil pedazos el cráneo de Galactus."},
            {"src": S57[132], "text": "Como advertencia eterna a los cielos, convirtió el gigantesco casco del devorador en las puertas de Asgard. ¿Fue justa esta brutal ejecución?"},
        ],
    },
    # #18 MOST VIRAL (29,036 views)
    {
        "slot": 58,
        "fb_views": 29036,
        "queue_folder": "058_fc_v18_deathstroke_humilla_liga_justicia",
        "id": "fc_58_v18_deathstroke_humilla_liga_justicia",
        "folder": "fc_58_v18_deathstroke_humilla_liga_justicia",
        "title": "¡Un Solo Mercenario Humilló a la Liga de la Justicia! La Hazaña de Deathstroke ⚔️🔥",
        "character": "Deathstroke",
        "voice_mode": "zazoom",
        "hook_card": "¡UN MERCENARIO HUMILLÓ A LA LIGA DE LA JUSTICIA!",
        "thumb_text": "HUMILLÓ A LA LIGA",
        "thumb_scene_idx": 1,
        "description": "Top #18 Viral (29K views) en FilmCraft 60fps: En Identity Crisis, Slade Wilson derrotó solo a Flash, Zatanna, Hawkman, Green Arrow y Green Lantern.",
        "hashtags": "#Deathstroke #JusticeLeague #IdentityCrisis #SladeWilson #DCComics #Reels",
        "scenes": [
            {"src": S58[0], "text": "En Crisis de Identidad, Slade Wilson demostró por qué la preparación táctica supera a los superpoderes enfrentando completamente solo a la Liga de la Justicia."},
            {"src": S58[1], "text": "Contratado como guardia personal del Doctor Light, Deathstroke quedó rodeado en segundos por siete de los guerreros más poderosos de la Tierra."},
            {"src": S58[2], "text": "Primero calculó con exactitud matemática los ángulos de rebote para atrapar y neutralizar a The Atom con un puntero láser directo al traje."},
            {"src": S58[3], "text": "Antes de que Zatanna pudiera pronunciar un solo conjuro mágico al revés, Slade la golpeó en el plexo solar dejándola sin aire para hablar."},
            {"src": S58[4], "text": "Cuando Hawkman cargó desde arriba en picada, el mercenario cortó las correas de su arnés de metal Nth enviándolo a estrellarse contra el pavimento."},
            {"src": S58[5], "text": "Con un giro relámpago de su espada de prometio partió las flechas de Oliver Queen y humilló a Black Canary cerrándole la boca."},
            {"src": S58[8], "text": "Al ver correr a Wally West a supervelocidad, anticipó su ruta exacta obligando a Flash a empalarse directo contra la hoja de su espada."},
            {"src": S58[9], "text": "Finalmente aplastó la mano de Green Lantern anulando el poder de su anillo con pura fuerza mental. ¿Es Deathstroke el mejor estratega de DC?"},
        ],
    },
    # #19 MOST VIRAL (23,152 views)
    {
        "slot": 59,
        "fb_views": 23152,
        "queue_folder": "059_fc_v19_gorr_carnicero_de_dioses",
        "id": "fc_59_v19_gorr_carnicero_de_dioses",
        "folder": "fc_59_v19_gorr_carnicero_de_dioses",
        "title": "¡Gorr el Carnicero de Dioses! El Mortal que Juró Asesinar a Todas las Deidades ⚔️⚡",
        "character": "Gorr & Thor",
        "voice_mode": "referencia",
        "hook_card": "¡EL MORTAL QUE JURÓ MATAR A TODOS LOS DIOSES!",
        "thumb_text": "CARNICERO DE DIOSES",
        "thumb_scene_idx": 4,
        "description": "Top #19 Viral (23.1K views) en FilmCraft 60fps: Armado con la Necroespada All-Black forjada por Knull, Gorr masacró panteones hasta enfrentar a tres Thors.",
        "hashtags": "#Gorr #Thor #Necrosword #MarvelComics #JasonAaron #Reels",
        "scenes": [
            {"src": S59[0], "text": "Armado con la Necroespada All-Black forjada por Knull, Gorr viajó durante miles de años torturando y exterminando a cada panteón de dioses del cosmos."},
            {"src": S59[35], "text": "Consumido por el odio tras ver morir de hambre a su familia mientras sus plegarias nunca tuvieron respuesta, el humilde extraterrestre declaró la guerra divina."},
            {"src": S59[49], "text": "Siglos atrás en Islandia, un joven y arrogante Thor siguió un rastro de cadáveres celestiales hasta toparse con el asesino envuelto en sombras vivientes."},
            {"src": S59[63], "text": "Capturado y encadenado dentro de una caverna helada, Thor resistió diecisiete días seguidos de tortura antes de cortar el brazo del monstruo."},
            {"src": S59[98], "text": "Nueve mil años en el futuro, Gorr esclavizó a miles de dioses restantes para construir la Bomba Divina capaz de borrar toda deidad."},
            {"src": S59[119], "text": "Para detener la extinción definitiva del universo, el Thor del presente unió fuerzas con su yo vikingo del pasado y el viejo Rey Thor."},
            {"src": S59[168], "text": "Los tres guerreros del trueno cargaron juntos contra las legiones oscuras de berserkers, abriéndose paso a martillazos hasta el corazón de la máquina."},
            {"src": S59[189], "text": "Alzando dos martillos Mjolnir a la vez, Thor absorbió entera la Bomba Divina destruyendo al Carnicero. ¿Es Gorr el mejor villano moderno de Thor?"},
        ],
    },
    # #20 MOST VIRAL (18,123 views)
    {
        "slot": 60,
        "fb_views": 18123,
        "queue_folder": "060_fc_v20_all_star_superman_final",
        "id": "fc_60_v20_all_star_superman_final",
        "folder": "fc_60_v20_all_star_superman_final",
        "title": "El cómic más perfecto de Superman: cuando solo le quedaba un año de vida ☀️💔",
        "character": "All-Star Superman",
        "voice_mode": "zazoom",
        "hook_card": "CUANDO A SUPERMAN SOLO LE QUEDABA UN AÑO DE VIDA...",
        "thumb_text": "UN AÑO DE VIDA",
        "thumb_scene_idx": 5,
        "description": "Top #20 Viral (18.1K views) en FilmCraft 60fps: Saboteado por Lex Luthor con radiación solar letal, Clark Kent salvó a la Tierra una última vez.",
        "hashtags": "#Superman #AllStarSuperman #DCComics #GrantMorrison #Reels",
        "scenes": [
            {"src": S60[0], "text": "El cómic más perfecto de Superman comenzó cuando solo le quedaba un año de vida y decidió salvar a la Tierra una última vez."},
            {"src": S60[2], "text": "Saboteado por una trampa secreta de Lex Luthor mientras rescataba una misión científica cerca del Sol, sus células absorbieron radiación letal irreversible."},
            {"src": S60[10], "text": "Condenado a disolverse en pura energía dorada en pocos meses, Clark Kent mantuvo la calma sin contarle la verdad a nadie por piedad."},
            {"src": S60[14], "text": "Dedicó sus últimos días a cumplir doce hazañas imposibles y regaló a Lois Lane un suero para compartir sus superpoderes durante veinticuatro horas."},
            {"src": S60_10[12], "text": "Pero el momento que definió su corazón eterno ocurrió al detenerse un segundo para abrazar a una joven desesperada: eres más fuerte de lo que crees."},
            {"src": S60[34], "text": "Con una despedida serena dejando todo en paz y creando un nuevo universo sin un Superman en su laboratorio, Clark enfrentó el final."},
            {"src": S60[52], "text": "Derrotó a un Lex Luthor superpoderoso y al sol viviente Solaris, antes de volar directo al núcleo de nuestra estrella para repararla desde adentro."},
            {"src": S60[64], "text": "Hoy vive en el corazón del Sol manteniendo viva su luz para siempre. ¿Consideras a All-Star Superman la mejor obra del Hombre de Acero?"},
        ],
    },
]


def produce_project(proj: dict, mode: str = "all"):
    slot = proj["slot"]
    q_folder = proj["queue_folder"]
    q_dir = SCHEDULED_QUEUE / q_folder
    v_out = q_dir / "video.mp4"
    m_out = q_dir / "metadata.json"

    if mode != "audio" and v_out.exists() and m_out.exists() and v_out.stat().st_size > 10_000_000:
        sz_mb = v_out.stat().st_size / (1024 * 1024)
        dur = get_media_duration(v_out)
        if 60.0 <= dur <= 90.0 and sz_mb < 95.0:
            print(f"[SKIP] Slot {slot:02d} ({q_folder}) ya listo ({dur:.2f}s, {sz_mb:.1f} MB)", flush=True)
            return dur, sz_mb, "CACHED"

    curated_dir = CURATED_BASE / proj["folder"]
    curated_dir.mkdir(parents=True, exist_ok=True)
    work_dir = PROJECT_ROOT / "work" / f"filmcraft_lote5_slot_{slot:02d}"
    work_dir.mkdir(parents=True, exist_ok=True)

    voice_mode = proj.get("voice_mode", "referencia").lower()
    prof_id = PROFILE_ZAZOOM if voice_mode == "zazoom" else PROFILE_REFERENCIA
    v_label = "Narrador Cómics ZaZooM" if voice_mode == "zazoom" else "Narrador Referencia Cómic"

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
            print(f"  [Slot {slot:02d} | {v_label}] Escena {idx}/{len(scenes)}: {sc['text'][:48]}...", flush=True)
            synthesize_voicebox_es(sc["text"], out_wav, profile_id=prof_id)
        raw_audios[idx] = out_wav

    if mode == "audio":
        return 0.0, 0.0, "AUDIO_OK"

    print(f"\n=======================================================", flush=True)
    print(f"🎬 [LOTE 5 TOP #{slot-40} ({proj['fb_views']:,} views)] {q_folder}", flush=True)
    print(f"   Título: {proj['title']}", flush=True)
    print(f"=======================================================", flush=True)

    raw_durs = [get_media_duration(raw_audios[i]) for i in range(1, len(scenes) + 1)]
    sum_raw = sum(raw_durs)
    speed = max(0.90, min(1.09, sum_raw / 74.5))
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

    word_json = work_dir / "word_timings.json"
    words_data = extract_scene_word_timings(voice_results, str(word_json), language="es", model_name="base")
    words_timing = [{"word": w["text"], "start": w["start"], "end": w["end"]} for w in words_data.get("words", [])]

    q_dir.mkdir(parents=True, exist_ok=True)
    final_dur = assemble_filmcraft_reel(
        scene_items=scene_items,
        words_timing=words_timing,
        narration_audio=full_audio,
        output_mp4=v_out,
        work_dir=work_dir / "fc_work",
        hook_text=proj["hook_card"],
        hook_duration=7.0,
        seq_name=f"Lote5_Slot_{slot:02d}",
        bitrate_kbps=5500,
    )

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
        "fb_viral_rank": slot - 40,
        "fb_original_views": proj["fb_views"],
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=41)
    parser.add_argument("--end", type=int, default=60)
    parser.add_argument("--audio-only", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    selected = [p for p in LOTE_05_PROJECTS if args.start <= p["slot"] <= args.end]
    for proj in selected:
        for i, sc in enumerate(proj["scenes"], start=1):
            p = Path(sc["src"])
            if not p.exists():
                raise FileNotFoundError(f"Missing asset for Slot {proj['slot']} scene {i}: {p}")
    print(f"✓ Verificadas las rutas y guiones de {len(selected)} videos (Slots {args.start}-{args.end}).", flush=True)

    if args.check_only:
        for p in selected:
            wc = sum(len(s["text"].split()) for s in p["scenes"])
            print(f"  Slot {p['slot']:02d} (#{p['slot']-40:2d} | {p['fb_views']:>7,} views | {p['voice_mode']:<10} | {wc:3d} words): {p['queue_folder']}")
        return

    mode = "audio" if args.audio_only else "all"
    start_all = time.time()
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    summary = []

    for proj in selected:
        try:
            dur, sz, st = produce_project(proj, mode=mode)
            summary.append((proj["slot"], proj["queue_folder"], dur, sz, st))
        except Exception as e:
            print(f"❌ ERROR en Slot {proj['slot']}: {e}", flush=True)
            summary.append((proj["slot"], proj["queue_folder"], 0.0, 0.0, f"ERROR: {e}"))

    elapsed_min = (time.time() - start_all) / 60.0
    print("\n" + "=" * 78, flush=True)
    print(f"RESUMEN LOTE 5 ({mode.upper()} | Slots {args.start}-{args.end} | {elapsed_min:.1f} min)", flush=True)
    print("=" * 78, flush=True)
    for slot, qf, dur, sz, st in summary:
        print(f"Slot {slot:02d} | {dur:6.2f}s | {sz:6.1f} MB | {st:<10} | {qf}", flush=True)
    print("=" * 78, flush=True)


if __name__ == "__main__":
    main()
