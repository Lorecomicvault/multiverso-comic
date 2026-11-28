"""
Lote 4 Maestro (FilmCraft 60FPS + Voicebox 0.6B ES) — Slots 31 al 40 (~75 Segundos)
=================================================================================
10 historias épicas de contexto completo (~1m 14s) editadas 100% en FilmCraft GPU
(1080x1920 @ 60fps) con Voicebox CUDA en español y Hook Card flotante en Escena 1.
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


def _sorted_imgs(folder: Path) -> list[Path]:
    return sorted(
        [
            p
            for p in folder.rglob("*")
            if p.suffix.lower() in (".jpg", ".jpeg", ".png")
            and "zwater" not in p.name.lower()
        ]
    )


ANN = _sorted_imgs(SRC / "annihilation" / "extracted")
S66 = CURATED_BASE / "66_sentry_alma_knull_valhalla"
BOD1 = _sorted_imgs(SRC / "books_of_doom" / "extracted_pages" / "200601 Books of Doom 001")
SW6 = _sorted_imgs(SRC / "secret_wars_2015" / "pages" / "issue_06")
SW7 = _sorted_imgs(SRC / "secret_wars_2015" / "pages" / "issue_07")
ULT = _sorted_imgs(SRC / "ultimatum" / "extracted_pages")
DD = _sorted_imgs(SRC / "daredevil_guardian_devil" / "extracted")
CFJ = _sorted_imgs(SRC / "cry_for_justice" / "extracted")
WVH = _sorted_imgs(SRC / "wolverine_vs_hulk" / "extracted_pages")
ASM539 = _sorted_imgs(SRC / "spiderman_back_in_black" / "extracted_asm_539")


LOTE_04_PROJECTS = [
    {
        "slot": 31,
        "queue_folder": "031_fc_annihilation_drax_corazon_thanos",
        "id": "fc_31_annihilation_drax_corazon_thanos",
        "folder": "fc_31_annihilation_drax_corazon_thanos",
        "title": "Annihilation #4: ¡Drax Atravesó el Pecho de Thanos y Le Arrancó el Corazón! 💚🩸💀",
        "character": "Drax el Destructor",
        "voice_mode": "referencia",
        "hook_card": "¿CÓMO MATÓ DRAX A THANOS CON UN SOLO GOLPE?",
        "thumb_text": "ARRANCÓ SU CORAZÓN",
        "thumb_scene_idx": 6,
        "description": "Annihilation #4 (Keith Giffen): La cacería implacable de Drax el Destructor que terminó atravesando el pecho del Titán Loco.",
        "hashtags": "#Drax #Thanos #Annihilation #MarvelComics #MarvelCosmic #Comics #Reels",
        "scenes": [
            {
                "src": ANN[95],
                "text": "Durante décadas el único propósito grabado en la mente de Drax el Destructor fue cazar y matar a Thanos de Titán sin importar el precio.",
            },
            {
                "src": ANN[96],
                "text": "En plena guerra de Aniquilación, Drax abordó completamente solo la gigantesca nave donde el Titán negociaba la destrucción del universo entero.",
            },
            {
                "src": ANN[99],
                "text": "A diferencia del pasado, esta versión ágil y despiadada destrozó a cientos de soldados insectoides avanzando pasillo por pasillo hacia su objetivo.",
            },
            {
                "src": ANN[104],
                "text": "Mientras tanto, en el núcleo de la nave, Thanos intentaba liberar al devorador de mundos Galactus de las cadenas cósmicas de Annihilus.",
            },
            {
                "src": ANN[106],
                "text": "Las explosiones sacudieron la fortaleza espacial abriendo paso entre fuego y chatarra al guerrero verde sediento de una venganza pendiente desde años.",
            },
            {
                "src": ANN[108],
                "text": "Ignorando las advertencias desesperadas de Star-Lord y Dragón Lunar sobre el peligro cósmico, Drax se lanzó directo por detrás sin pronunciar palabra.",
            },
            {
                "src": ANN[110],
                "text": "Con una velocidad brutal y letal, su puño atravesó la armadura y el pecho de Thanos para arrancarle el corazón todavía latiendo en su mano.",
            },
            {
                "src": ANN[115],
                "text": "El Titán Loco cayó fulminado sobre el suelo metálico mientras Galactus despertaba. ¿Crees que Thanos merecía un final tan frío y directo?",
            },
        ],
    },
    {
        "slot": 32,
        "queue_folder": "032_fc_annihilation_nova_arranca_annihilus",
        "id": "fc_32_annihilation_nova_arranca_annihilus",
        "folder": "fc_32_annihilation_nova_arranca_annihilus",
        "title": "Annihilation #6: ¡Nova Metió la Mano por la Boca de Annihilus y lo Destrozó! 💥🐛🌌",
        "character": "Nova (Richard Rider)",
        "voice_mode": "zazoom",
        "hook_card": "¿QUÉ LE HIZO NOVA A ANNIHILUS PARA SALVAR LA GALAXIA?",
        "thumb_text": "FIN DE ANNIHILUS",
        "thumb_scene_idx": 6,
        "description": "Annihilation #6 (Keith Giffen): El brutal duelo final donde Richard Rider arrancó las entrañas de Annihilus desde adentro.",
        "hashtags": "#Nova #Annihilus #Annihilation #MarvelComics #RichardRider #Comics #Reels",
        "scenes": [
            {
                "src": ANN[140],
                "text": "Con galaxias enteras reducidas a cenizas por la Ola de Aniquilación, un Galactus recién liberado desató su furia borrando millones de naves enemigas.",
            },
            {
                "src": ANN[143],
                "text": "En medio del caos espacial, Richard Rider asumió el mando definitivo liderando junto a Star-Lord y Phyla-Vell un último asalto suicida.",
            },
            {
                "src": ANN[147],
                "text": "Ronan el Acusador y los últimos sobrevivientes abrieron brecha entre explosiones mortales para que Nova pudiera entrar al puente de mando.",
            },
            {
                "src": ANN[148],
                "text": "Blindado con las Bandas Cuánticas robadas a Quasar, el tirano Annihilus creyó haberse vuelto un dios inmortal capaz de aplastar cualquier ejército.",
            },
            {
                "src": ANN[149],
                "text": "Portando toda la Fuerza Nova y la Mente Mundial Xandariana en su interior, Richard Rider descendió al duelo mano a mano sin retroceder.",
            },
            {
                "src": ANN[154],
                "text": "Justo cuando el combate estaba perdido, Phyla-Vell logró arrancarle las Bandas Cuánticas de los brazos dejando vulnerable al monstruo por un instante.",
            },
            {
                "src": ANN[156],
                "text": "Nova aprovechó esa fracción de segundo para forzarle la mandíbula, meter el brazo por su garganta y arrancarle las entrañas desde adentro.",
            },
            {
                "src": ANN[157],
                "text": "El cuerpo de Annihilus colapsó poniendo fin a la guerra cósmica más sangrienta. ¿Fue este el momento más épico de Richard Rider?",
            },
        ],
    },
    {
        "slot": 33,
        "queue_folder": "033_fc_king_in_black_sentry_knull_valhalla",
        "id": "fc_33_king_in_black_sentry_knull_valhalla",
        "folder": "fc_33_king_in_black_sentry_knull_valhalla",
        "title": "King in Black: ¡Knull Partió en Dos a Sentry y Un Celestial Robó Su Alma! 🌑⚡💀",
        "character": "Sentry",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ NADIE PUDO REVIVIR A SENTRY TRAS KING IN BLACK?",
        "thumb_text": "EL FIN DE SENTRY",
        "thumb_scene_idx": 2,
        "description": "King in Black #1 y King in Black: Return of the Valkyries: La humillante muerte de Sentry ante Knull y el destino maldito de su alma.",
        "hashtags": "#Sentry #Knull #KingInBlack #Valkyrie #MarvelComics #Venom #Comics #Reels",
        "scenes": [
            {
                "src": S66 / "02_sentry_rips_ares_siege_01.jpg",
                "text": "Durante años Sentry fue temido como el guerrero más poderoso de la Tierra, un ser con la energía explosiva de un millón de soles.",
            },
            {
                "src": S66 / "02_sentry_rips_ares_siege_02.jpg",
                "text": "Todo el mundo recordaba la pesadilla de Asgard cuando, poseído por el Vacío, tomó al dios de la guerra Ares y lo partió brutalmente.",
            },
            {
                "src": S66 / "01_knull_rips_sentry_king_in_black.jpg",
                "text": "Pero cuando Knull el dios de los simbiontes invadió Nueva York, atrapó a Sentry en pleno vuelo y lo desgarró exactamente en dos mitades.",
            },
            {
                "src": S66 / "03_sentry_soul_jane_foster_valkyrie.jpg",
                "text": "Tras morir instantáneamente ante los Vengadores horrorizados, su espíritu quedó vagando en la órbita terrestre hasta que llegó Jane Foster.",
            },
            {
                "src": S66 / "03b_sentry_soul_valhalla.jpg",
                "text": "Como nueva Valquiria, Jane intentó escoltar el alma cansada de Robert Reynolds rumbo al descanso eterno prometido en el legendario Valhalla.",
            },
            {
                "src": S66 / "04_headless_celestial_knull_origin.jpg",
                "text": "Sin embargo, la historia oculta de Knull escondía una trampa mortal vinculada al primer Celestial al que decapitó al inicio del universo.",
            },
            {
                "src": S66 / "04b_headless_celestial_reveal.jpg",
                "text": "Aquel gigante cósmico corrompido por la oscuridad sobrevivía consumiendo almas poderosas para reconstruir su propia voluntad desde el abismo.",
            },
            {
                "src": S66 / "05_celestial_ensnares_sentry_soul.jpg",
                "text": "Antes de cruzar las puertas divinas, el Celestial emboscó a Valkyrie y atrapó el alma de Sentry en las sombras. ¿Merecía Bob descansar en paz?",
            },
        ],
    },
    {
        "slot": 34,
        "queue_folder": "034_fc_books_of_doom_1_cynthia_pacto_mefisto",
        "id": "fc_34_books_of_doom_1_cynthia_pacto_mefisto",
        "folder": "fc_34_books_of_doom_1_cynthia_pacto_mefisto",
        "title": "Books of Doom #1: ¡El Pacto Maldito de Su Madre Que Condenó a Doctor Doom! 🔮🔥👑",
        "character": "Doctor Doom",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ DOCTOR DOOM NUNCA SE RINDE ANTE EL INFIERNO?",
        "thumb_text": "PACTO CON MEFISTO",
        "thumb_scene_idx": 6,
        "description": "Books of Doom #1 (Ed Brubaker & Pablo Raimondi): La tragedia de Cynthia Von Doom y el juramento eterno de Victor por rescatar su alma.",
        "hashtags": "#DoctorDoom #BooksOfDoom #Mephisto #Latveria #MarvelComics #Comics #Reels",
        "scenes": [
            {
                "src": BOD1[1],
                "text": "Detrás de la armadura indestructible del monarca más temido de Marvel, se esconde la herida infantil que convirtió a Victor Von Doom en tirano.",
            },
            {
                "src": BOD1[2],
                "text": "Victor nació en una tribu gitana perseguida brutalmente por el noble Barón de Latveria, creciendo entre el frío, la pobreza y las fogatas.",
            },
            {
                "src": BOD1[4],
                "text": "Desesperada por proteger a su familia, su madre Cynthia recurrió a antiguos tomos prohibidos e invocó un pacto secreto con el demonio Mefisto.",
            },
            {
                "src": BOD1[5],
                "text": "La magia infernal desató tormentas que masacraron a los soldados invasores, pero el precio oculto del trato también cobró la vida de niños inocentes.",
            },
            {
                "src": BOD1[6],
                "text": "Aterrada por la masacre que ella misma provocó, Cynthia cayó mortalmente herida y Mefisto arrastró su alma directo a las profundidades del Infierno.",
            },
            {
                "src": BOD1[17],
                "text": "Años después, el joven Victor descubrió el secreto oculto en los baúles familiares, obsesionándose por combinar la ciencia avanzada con brujería prohibida.",
            },
            {
                "src": BOD1[18],
                "text": "Encerrado dentro de círculos de fuego arcano, desafió directamente a los demonios jurando que algún día vencería al propio señor del abismo.",
            },
            {
                "src": BOD1[23],
                "text": "Al aceptar una beca rumbo a Estados Unidos, Victor inició la cruzada eterna para liberar a su madre. ¿Todo villano nace de una tragedia?",
            },
        ],
    },
    {
        "slot": 35,
        "queue_folder": "035_fc_secret_wars_7_rebelion_zombis_thanos",
        "id": "fc_35_secret_wars_7_rebelion_zombis_thanos",
        "folder": "fc_35_secret_wars_7_rebelion_zombis_thanos",
        "title": "Secret Wars #7: ¡Black Panther Desató un Ejército de Zombis Contra Doom! 🐾🧟‍♂️🔥",
        "character": "Black Panther",
        "voice_mode": "referencia",
        "hook_card": "¿CÓMO ROMPIÓ BLACK PANTHER EL REINO DE DIOS DOOM?",
        "thumb_text": "EJÉRCITO DE MUERTOS",
        "thumb_scene_idx": 7,
        "description": "Secret Wars #6 y #7 (Jonathan Hickman & Esad Ribic): La guerra total contra Dios Emperador Doom y el épico regreso de T'Challa con los muertos.",
        "hashtags": "#SecretWars #BlackPanther #DoctorDoom #MarvelZombies #MarvelComics #Reels",
        "scenes": [
            {
                "src": SW6[26],
                "text": "Tras semanas gobernando un planeta hecho de universos rotos, el reinado de Dios Emperador Doom comenzó a resquebrajarse desde el muro más peligroso.",
            },
            {
                "src": SW6[28],
                "text": "Thanos convenció al gigantesco Ben Grimm de que su verdadero pasado había sido borrado, provocando que la Mole se levantara rompiendo la muralla.",
            },
            {
                "src": SW7[2],
                "text": "Al mismo tiempo, un misterioso Profeta reunió a los ejércitos rebeldes de todos los barones descontentos para marchar directo hacia el castillo de Doom.",
            },
            {
                "src": SW7[7],
                "text": "Barones traidores, guerreros de Apocalipsis y escuadrones enteros desataron una batalla sangrienta a las puertas de la capital frente a la guardia imperial.",
            },
            {
                "src": SW7[12],
                "text": "Incluso el temido Cuerpo de Thors terminó fracturado por dentro cuando Jane Foster reveló la verdad oculta sobre el origen falso de Battleworld.",
            },
            {
                "src": SW7[16],
                "text": "Mientras tanto, la resistencia parecía condenada cuando el ejército entero de Hulks comandado por Maestro cayó del cielo aplastando las líneas rebeldes.",
            },
            {
                "src": SW7[20],
                "text": "Fue entonces cuando el sonido de un cuerno de guerra anunció la llegada imposible de Black Panther irrumpiendo en el campo de batalla.",
            },
            {
                "src": SW7[22],
                "text": "Gracias a un cetro ancestral, T'Challa lideraba a los Marvel Zombies, Ultrons y la Ola Aniquiladora. ¿Fue esta la mayor batalla de Secret Wars?",
            },
        ],
    },
    {
        "slot": 36,
        "queue_folder": "036_fc_ultimatum_avispa_blob_giant_man",
        "id": "fc_36_ultimatum_avispa_blob_giant_man",
        "folder": "fc_36_ultimatum_avispa_blob_giant_man",
        "title": "Ultimatum: ¡La Escena Más Perturbadora! Giant-Man Se Comió a Blob Tras Ver a Wasp 🩸😱",
        "character": "Hank Pym (Giant-Man)",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ ULTIMATUM FUE EL CÓMIC MÁS BRUTAL DE MARVEL?",
        "thumb_text": "VENGANZA SANGRIENTA",
        "thumb_scene_idx": 2,
        "description": "Ultimatum #2 y #3 (Jeph Loeb & David Finch): La escena que traumatizó a toda una generación cuando Hank Pym encontró a Blob devorando a Wasp.",
        "hashtags": "#Ultimatum #Wasp #GiantMan #MarvelComics #UltimateMarvel #Comics #Reels",
        "scenes": [
            {
                "src": ULT[34],
                "text": "Tras el cataclismo provocado por Magneto que sumergió toda Nueva York bajo el agua, Hank Pym salió desesperado a buscar a Janet Van Dyne.",
            },
            {
                "src": ULT[36],
                "text": "Sobrevolando rascacielos destruidos y miles de cadáveres flotando en las calles inundadas, el héroe gritaba el nombre de su esposa sin recibir respuesta.",
            },
            {
                "src": ULT[45],
                "text": "Pero lo que descubrió entre los escombros superó cualquier pesadilla imaginable: el monstruoso Blob estaba devorando vivo el cuerpo ensangrentado de Avispa.",
            },
            {
                "src": ULT[54],
                "text": "Destrozado por el horror y cegado por una rabia incontrolable, Hank Pym activó su tamaño gigante atrapando al mutante caníbal entre sus manos.",
            },
            {
                "src": ULT[55],
                "text": "En uno de los paneles más explícitos y polémicos jamás publicados por Marvel, Giant-Man le arrancó la cabeza de un mordisco por venganza.",
            },
            {
                "src": ULT[48],
                "text": "Al mismo tiempo en la mansión mutante, Magneto ejecutaba fríamente al Profesor X rompiéndole el cuello frente a sus estudiantes impotentes.",
            },
            {
                "src": ULT[59],
                "text": "Con el cuerpo sin vida de Janet en brazos, los pocos héroes sobrevivientes marcharon hacia la ciudadela flotante de Magneto sabiendo que morirían.",
            },
            {
                "src": ULT[64],
                "text": "Finalmente Hank se sacrificó haciéndose estallar junto a los clones explosivos para salvar al equipo. ¿Se pasó de la raya Marvel con Ultimatum?",
            },
        ],
    },
    {
        "slot": 37,
        "queue_folder": "037_fc_daredevil_mysterio_guardian_devil",
        "id": "fc_37_daredevil_mysterio_guardian_devil",
        "folder": "fc_37_daredevil_mysterio_guardian_devil",
        "title": "Daredevil: ¡Mysterio Orquestó Su Pesadilla y Se Voló la Cabeza Frente a Él! 🔮🔫😈",
        "character": "Daredevil",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ MYSTERIO DESTRUYÓ LA VIDA DE DAREDEVIL?",
        "thumb_text": "EL ÚLTIMO TRUCO",
        "thumb_scene_idx": 6,
        "description": "Daredevil: Guardian Devil #7 y #8 (Kevin Smith & Joe Quesada): El macabro plan final de Quentin Beck al descubrir que tenía cáncer terminal.",
        "hashtags": "#Daredevil #Mysterio #GuardianDevil #MarvelComics #MattMurdock #Comics #Reels",
        "scenes": [
            {
                "src": DD[135],
                "text": "Después de semanas de locura, traiciones y la trágica muerte de Karen Page, Matt Murdock finalmente encontró al culpable oculto entre el humo.",
            },
            {
                "src": DD[138],
                "text": "Contra todo pronóstico, el autor de la conspiración no era un demonio bíblico ni Kingpin, sino Quentin Beck, el viejo enemigo de Spider-Man.",
            },
            {
                "src": DD[142],
                "text": "Mysterio confesó haber comprado la identidad secreta de Daredevil para manipular a sus amigos con drogas alucinógenas y un bebé inocente como carnada.",
            },
            {
                "src": DD[152],
                "text": "Consumido por la rabia acumulada tras enterrar al amor de su vida, Daredevil atravesó todas las trampas y destrozó el casco de cristal.",
            },
            {
                "src": DD[154],
                "text": "Al desenmascararlo a golpes en medio del laboratorio ardiendo, Matt quedó paralizado al descubrir que Beck ya ni siquiera podía mantenerse en pie.",
            },
            {
                "src": DD[155],
                "text": "Mysterio reveló la verdad más patética: padecía cáncer cerebral terminal y necesitaba arruinar al menos la vida de un héroe antes de morir.",
            },
            {
                "src": DD[157],
                "text": "Despreciado por Matt, quien se negó a matarlo llamándolo una copia barata sin talento, Beck sacó un arma y jaló el gatillo al instante.",
            },
            {
                "src": DD[158],
                "text": "Quentin Beck murió en un charco de sangre dejando a Matt vacío en el silencio. ¿Fue este el final más oscuro de Daredevil?",
            },
        ],
    },
    {
        "slot": 38,
        "queue_folder": "038_fc_cry_for_justice_prometheus_star_city",
        "id": "fc_38_cry_for_justice_prometheus_star_city",
        "folder": "fc_38_cry_for_justice_prometheus_star_city",
        "title": "Cry For Justice: ¡Prometheus Le Cortó el Brazo a Arsenal y Voló Star City! 💣🩸🏹",
        "character": "Prometheus",
        "voice_mode": "zazoom",
        "hook_card": "¿CÓMO DERROTÓ PROMETHEUS SOLO A LA LIGA DE LA JUSTICIA?",
        "thumb_text": "DESTRUYÓ STAR CITY",
        "thumb_scene_idx": 5,
        "description": "Justice League: Cry for Justice #5–6 (James Robinson): El plan maestro más sádico contra la Liga de la Justicia y la tragedia de Roy Harper.",
        "hashtags": "#JusticeLeague #GreenArrow #Prometheus #Arsenal #DCComics #Comics #Reels",
        "scenes": [
            {
                "src": CFJ[105],
                "text": "Haciéndose pasar por Freddy Freeman tras derrotarlo en secreto, el calculador villano Prometheus logró infiltrarse en el corazón de la Atalaya espacial.",
            },
            {
                "src": CFJ[112],
                "text": "Al intentar detenerlo solo, Roy Harper pagó el precio más cruel cuando Prometheus le cercenó el brazo derecho con una espada letal.",
            },
            {
                "src": CFJ[120],
                "text": "Equipado con un casco que copiaba las técnicas de pelea de los mejores guerreros, neutralizó en minutos a Supergirl, Green Lantern y Flash.",
            },
            {
                "src": CFJ[126],
                "text": "Cuando toda la Liga yacía derrotada en el suelo, solamente The Atom logró enfrentarlo reduciéndose a tamaño microscópico para dañar su cerebro.",
            },
            {
                "src": CFJ[132],
                "text": "Pero el combate espacial era apenas una distracción mientras los dispositivos ocultos bajo los cimientos de Star City completaban su cuenta regresiva final.",
            },
            {
                "src": CFJ[136],
                "text": "Un terremoto artificial gigantesco borró toda la ciudad del mapa en segundos, dejando un cráter humeante y casi cien mil víctimas inocentes.",
            },
            {
                "src": CFJ[140],
                "text": "Hal Jordan y los héroes descubrieron horrorizados la tragedia total, incluyendo la muerte de la pequeña Lian, la hija de Roy Harper.",
            },
            {
                "src": CFJ[154],
                "text": "Acorralado poco después en su guarida, Prometheus esperó el juicio que llevaría a Green Arrow al límite. ¿Tiene perdón un crimen así?",
            },
        ],
    },
    {
        "slot": 39,
        "queue_folder": "039_fc_wolverine_cabeza_cortada_nick_fury",
        "id": "fc_39_wolverine_cabeza_cortada_nick_fury",
        "folder": "fc_39_wolverine_cabeza_cortada_nick_fury",
        "title": "Wolverine vs Hulk: ¡Sobrevivió Como Una Cabeza Cortada Sobre Una Mesa! 🧬🩸🐺",
        "character": "Wolverine",
        "voice_mode": "referencia",
        "hook_card": "¿HASTA DÓNDE LLEGA LA INMORTALIDAD DE WOLVERINE?",
        "thumb_text": "SOLO UNA CABEZA",
        "thumb_scene_idx": 4,
        "description": "Ultimate Wolverine vs. Hulk #1–2 (Damon Lindelof & Leinil Yu): El bizarro experimento de Nick Fury tras encontrar solo la cabeza viva de Logan.",
        "hashtags": "#Wolverine #Hulk #NickFury #UltimateMarvel #MarvelComics #Logan #Comics #Reels",
        "scenes": [
            {
                "src": WVH[3],
                "text": "Enviado por Nick Fury al Tíbet para eliminar a Bruce Banner, Wolverine cometió el error fatal de subestimar la fuerza del monstruo.",
            },
            {
                "src": WVH[5],
                "text": "Tras ser partido brutalmente en dos pedazos en la cima helada, Logan pasó días enterrado en la nieve buscando desesperadamente sus piernas.",
            },
            {
                "src": WVH[28],
                "text": "El impacto de Hulk había sido tan descomunal que sus extremidades terminaron lanzadas a kilómetros de distancia por un precipicio de hielo.",
            },
            {
                "src": WVH[7],
                "text": "Semanas más tarde, dentro de una instalación ultrasecreta, Nick Fury recibió finalmente un extraño maletín metálico rescatado desde la montaña congelada.",
            },
            {
                "src": WVH[11],
                "text": "Cuando los científicos abrieron la cámara de contención esperando un cadáver, quedaron petrificados al ver lo que descansaba sobre la bandeja de acero.",
            },
            {
                "src": WVH[12],
                "text": "Sin cuerpo, sin pulmones y completamente decapitado, la cabeza solitaria de Wolverine abrió los ojos mirando fijamente al director de S.H.I.E.L.D.",
            },
            {
                "src": WVH[15],
                "text": "Los investigadores revelaron asombrados que su factor curativo lo mantenía consciente respirando oxígeno directamente a través de los poros de su piel.",
            },
            {
                "src": WVH[17],
                "text": "Incluso reducido a una cabeza sin torso ni garras, Logan le prometió a Fury descuartizarlo en cuanto escapara. ¿Supera esto cualquier regeneración?",
            },
        ],
    },
    {
        "slot": 40,
        "queue_folder": "040_fc_spiderman_back_in_black_disparo_tia_may",
        "id": "fc_40_spiderman_back_in_black_disparo_tia_may",
        "folder": "fc_40_spiderman_back_in_black_disparo_tia_may",
        "title": "Back in Black: ¡El Disparo a la Tía May Que Desató al Spider-Man Sin Piedad! 🕷️🖤🩸",
        "character": "Spider-Man",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ SPIDER-MAN SE PUSO EL TRAJE NEGRO PARA MATAR?",
        "thumb_text": "ADIÓS A LAS REGLAS",
        "thumb_scene_idx": 7,
        "description": "The Amazing Spider-Man #539 (J. Michael Straczynski & Ron Garney): El instante trágico tras Civil War que rompió para siempre la paciencia de Peter Parker.",
        "hashtags": "#SpiderMan #BackInBlack #TiaMay #Kingpin #MarvelComics #Comics #Reels",
        "scenes": [
            {
                "src": ASM539[4],
                "text": "Tras cometer el error de revelar su rostro al mundo en Civil War, un francotirador contratado desde prisión apuntó directo a Peter Parker.",
            },
            {
                "src": ASM539[5],
                "text": "Su sentido arácnido lo alertó justo a tiempo para empujar a Mary Jane al suelo, pero la bala mortal atravesó a la Tía May.",
            },
            {
                "src": ASM539[6],
                "text": "Cargándola entre lágrimas mientras se desangraba rápidamente, Spider-Man irrumpió en la sala de urgencias suplicando desesperadamente que salvaran a su familia.",
            },
            {
                "src": ASM539[8],
                "text": "Desde su celda blindada de máxima seguridad, Wilson Fisk sonrió satisfecho sabiendo que aquel disparo destruiría la vida entera del trepamuros.",
            },
            {
                "src": ASM539[14],
                "text": "Quebrado por la culpa y consumido por una furia helada, Peter abandonó su código moral y salió de cacería completamente sin máscara.",
            },
            {
                "src": ASM539[19],
                "text": "Cuando localizó al hombre que suministró el rifle al sicario, lo masacró a puño limpio frente a todos sin contener su fuerza.",
            },
            {
                "src": ASM539[22],
                "text": "En el hospital, los médicos confirmaron en silencio que la herida era demasiado grave y la Tía May no volvería a despertar.",
            },
            {
                "src": ASM539[24],
                "text": "Bajo una tormenta eléctrica, Peter sacó su viejo traje negro del escondite jurando matar a los culpables. ¿Harías lo mismo en su lugar?",
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
    print(f"🎬 [LOTE 4 FILMCRAFT - VIDEO {slot}/40] {q_folder}", flush=True)
    print(f"   Título: {proj['title']}", flush=True)
    print(f"=======================================================", flush=True)

    curated_dir = CURATED_BASE / proj["folder"]
    curated_dir.mkdir(parents=True, exist_ok=True)
    work_dir = PROJECT_ROOT / "work" / f"filmcraft_lote4_slot_{slot:02d}"
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
            print(f"  [Voicebox - {v_label}] Escena {idx}/{len(scenes)}: {sc['text'][:48]}...", flush=True)
            synthesize_voicebox_es(sc["text"], out_wav, profile_id=prof_id)
        raw_audios[idx] = out_wav

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
        seq_name=f"Lote4_Slot_{slot:02d}",
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


def pregenerate_all_voicebox_audio():
    print("🎙️ [FASE 1] Pre-generando todas las voces Voicebox 0.6B ES con VRAM libre...", flush=True)
    for proj in LOTE_04_PROJECTS:
        slot = proj["slot"]
        q_dir = SCHEDULED_QUEUE / proj["queue_folder"]
        v_out = q_dir / "video.mp4"
        m_out = q_dir / "metadata.json"
        if v_out.exists() and m_out.exists() and v_out.stat().st_size > 10_000_000:
            dur = get_media_duration(v_out)
            sz_mb = v_out.stat().st_size / (1024 * 1024)
            if 60.0 <= dur <= 90.0 and sz_mb < 95.0:
                continue

        work_dir = PROJECT_ROOT / "work" / f"filmcraft_lote4_slot_{slot:02d}"
        work_dir.mkdir(parents=True, exist_ok=True)
        voice_mode = proj.get("voice_mode", "referencia").lower()
        prof_id = PROFILE_ZAZOOM if voice_mode == "zazoom" else PROFILE_REFERENCIA
        v_label = "Narrador Cómics ZaZooM" if voice_mode == "zazoom" else "Narrador Referencia Cómic"

        for idx, sc in enumerate(proj["scenes"], start=1):
            out_wav = work_dir / f"raw_scene_{idx:02d}.wav"
            if not out_wav.exists() or out_wav.stat().st_size < 5000:
                print(f"  [Slot {slot:02d} | {v_label}] Escena {idx}/{len(proj['scenes'])}: {sc['text'][:46]}...", flush=True)
                synthesize_voicebox_es(sc["text"], out_wav, profile_id=prof_id)


def main():
    for proj in LOTE_04_PROJECTS:
        for i, sc in enumerate(proj["scenes"], start=1):
            p = Path(sc["src"])
            if not p.exists():
                raise FileNotFoundError(f"Missing asset for Slot {proj['slot']} scene {i}: {p}")
    print(f"✓ Verificadas las rutas de todas las viñetas de los {len(LOTE_04_PROJECTS)} videos del Lote 4.", flush=True)

    pregenerate_all_voicebox_audio()

    start_all = time.time()
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    summary = []

    for proj in LOTE_04_PROJECTS:
        try:
            dur, sz, st = produce_project(proj)
            summary.append((proj["slot"], proj["queue_folder"], dur, sz, st))
        except Exception as e:
            print(f"❌ ERROR en Slot {proj['slot']}: {e}", flush=True)
            summary.append((proj["slot"], proj["queue_folder"], 0.0, 0.0, f"ERROR: {e}"))

    elapsed_min = (time.time() - start_all) / 60.0
    print("\n" + "=" * 78, flush=True)
    print(f"AUDITORÍA FINAL - LOTE 4 FILMCRAFT 75s ({elapsed_min:.1f} min)", flush=True)
    print("=" * 78, flush=True)
    for slot, qf, dur, sz, st in summary:
        print(f"Slot {slot:02d} | {dur:6.2f}s | {sz:6.1f} MB | {st:<10} | {qf}", flush=True)
    print("=" * 78, flush=True)


if __name__ == "__main__":
    main()
