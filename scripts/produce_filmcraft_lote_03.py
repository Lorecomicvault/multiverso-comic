"""
Lote 3 Maestro (FilmCraft 60FPS + Voicebox 0.6B ES) — Slots 21 al 30 (~75 Segundos)
=================================================================================
10 historias épicas de contexto completo (~1m 15s) editadas 100% en FilmCraft GPU
(1080x1920 @ 60fps) con Voicebox CUDA en español y Hook Visual en Escena 1.
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
        [p for p in folder.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg", ".png")]
    )


SW09 = _sorted_imgs(SRC / "secret_wars_2015" / "extracted_sw09")
SW04 = _sorted_imgs(SRC / "secret_wars_2015" / "pages" / "issue_04")
SW01 = _sorted_imgs(SRC / "secret_wars_2015" / "pages" / "issue_01")
PH095 = _sorted_imgs(SRC / "planet_hulk" / "extracted_095")
TW = _sorted_imgs(SRC / "thanos_wins" / "extracted_pages")
BOD6 = _sorted_imgs(SRC / "books_of_doom" / "extracted_pages" / "200606 Books of Doom 006")
WVH = _sorted_imgs(SRC / "wolverine_vs_hulk" / "extracted_pages")
UXF = _sorted_imgs(SRC / "uncanny_xforce" / "extracted_pages")
IM = _sorted_imgs(SRC / "iron_man_mysterium")
SUP = CURATED_BASE / "08_superman_vuela_seis_soles_noquea_world_forger"


LOTE_03_PROJECTS = [
    {
        "slot": 21,
        "queue_folder": "021_fc_secret_wars_9_pantera_guantelete_doom",
        "id": "fc_21_secret_wars_9_pantera_guantelete_doom",
        "folder": "fc_21_secret_wars_9_pantera_guantelete_doom",
        "title": "Secret Wars #9: ¡Black Panther Empuñó el Guantelete del Infinito Contra Dios Doom! 🐾💎👑",
        "character": "Black Panther",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ BLACK PANTHER USÓ LAS GEMAS CONTRA DOOM?",
        "thumb_text": "GUANTELETE VS DIOS DOOM",
        "thumb_scene_idx": 0,
        "description": "Secret Wars #9 (Jonathan Hickman): T'Challa desafía al omnipotente Dios Emperador Doom con el Guantelete del Infinito en la batalla final.",
        "hashtags": "#BlackPanther #DoctorDoom #SecretWars #GuanteleteDelInfinito #MarvelComics #Reels",
        "scenes": [
            {
                "src": SW09[0],
                "text": "Con el multiverso al borde de colapsar bajo el reinado absoluto de Dios Emperador Doom, un único rey mortal se atrevió a desafiarlo con las Gemas del Infinito.",
            },
            {
                "src": SW09[1],
                "text": "Armado con el Guantelete perfecto oculto durante años, T'Challa apareció frente al ejército de zombis de la fortaleza dispuesto a sacrificarlo todo.",
            },
            {
                "src": SW09[4],
                "text": "Black Panther desató ondas de realidad y tiempo contra el falso dios, haciendo temblar los cimientos enteros del castillo de Battleworld ante los rebeldes.",
            },
            {
                "src": SW09[9],
                "text": "Ambos monarcas chocaron con un poder cósmico capaz de borrar ejércitos enteros en un segundo, obligando a Doom a revelar su máxima furia divina.",
            },
            {
                "src": SW09[12],
                "text": "Aunque el poder infinito del guantelete era colosal, el secreto que T'Challa buscaba no era matarlo solo, sino distraerlo del verdadero golpe maestro.",
            },
            {
                "src": SW09[15],
                "text": "Mientras Doom creía haber ganado el combate, Reed Richards se infiltró en la cámara del Hombre Molécula para quitarle la fuente de su omnipotencia.",
            },
            {
                "src": SW09[20],
                "text": "Despojado repentinamente de sus poderes divinos en un estallido blanco, Battleworld explotó permitiendo reconstruir todo el multiverso Marvel.",
            },
            {
                "src": SW09[37],
                "text": "Como último regalo de Reed, Victor despertó sin cicatrices en su rostro comprendiendo por fin su derrota. ¿Merecía Doom esa segunda oportunidad?",
            },
        ],
    },
    {
        "slot": 22,
        "queue_folder": "022_fc_secret_wars_4_doom_rompe_cuello_cyclops_fenix",
        "id": "fc_22_secret_wars_4_doom_rompe_cuello_cyclops_fenix",
        "folder": "fc_22_secret_wars_4_doom_rompe_cuello_cyclops_fenix",
        "title": "Secret Wars #4: ¡Doom Le Rompió el Cuello a Cyclops Con el Poder Fénix En Segundos! 🔥💀👑",
        "character": "Doctor Doom",
        "voice_mode": "zazoom",
        "hook_card": "¿NI LA FUERZA FÉNIX PUDO CON DOCTOR DOOM?",
        "thumb_text": "DESTRUYÓ AL FÉNIX",
        "thumb_scene_idx": 0,
        "description": "Secret Wars #4 (Jonathan Hickman): Cuando Scott Summers usó la Fuerza Fénix contra el Dios Emperador Doom y conoció el terror de la omnipotencia.",
        "hashtags": "#DoctorDoom #Cyclops #Fenix #SecretWars #XMen #MarvelComics #Reels",
        "scenes": [
            {
                "src": SW04[33],
                "text": "Muchos aseguraban que la Fuerza Fénix era la entidad más imparable de todo Marvel, hasta el día que Scott Summers se atrevió a usarla contra Doctor Doom.",
            },
            {
                "src": SW04[23],
                "text": "Tras encontrar la nave secreta con los últimos sobrevivientes del universo destruido, Doom descendió del cielo con el poder absoluto de los Beyonders.",
            },
            {
                "src": SW04[24],
                "text": "Al reconocer entre los sobrevivientes a Reed Richards y a su eterna familia perdida, la furia y el rencor cegaron al Dios Emperador frente a todos.",
            },
            {
                "src": SW04[26],
                "text": "Negándose a arrodillarse ante el tirano, Cyclops liberó de golpe el huevo cósmico transformándose en el huésped ardiente de la Fuerza Fénix.",
            },
            {
                "src": SW04[27],
                "text": "Desatando llamas capaces de incinerar estrellas enteras, Scott quemó la capa de Victor jurando que ese reino de mentiras acabaría esa misma tarde.",
            },
            {
                "src": SW04[28],
                "text": "Pero el fuego cósmico no dejó ni un rasguño en el dios de acero. Con absoluta calma, Doom caminó entre las llamas directo hasta el mutante.",
            },
            {
                "src": SW04[29],
                "text": "Ante la mirada paralizada de los héroes, Doom tomó la cabeza de Cyclops y le partió el cuello en seco con un solo movimiento brutal.",
            },
            {
                "src": SW04[31],
                "text": "Cuando Doctor Strange teletransportó a los demás para salvarlos, Doom también lo ejecutó sin titubear. ¿Imaginaste un final tan cruel para el Fénix?",
            },
        ],
    },
    {
        "slot": 23,
        "queue_folder": "023_fc_secret_wars_1_fin_universo_marvel",
        "id": "fc_23_secret_wars_1_fin_universo_marvel",
        "folder": "fc_23_secret_wars_1_fin_universo_marvel",
        "title": "Secret Wars #1: ¡El Día que Todos los Héroes Murieron en el Fin del Universo Marvel! 💥🌍💀",
        "character": "Spider-Man",
        "voice_mode": "referencia",
        "hook_card": "¿CÓMO MURIERON TODOS LOS HÉROES DE MARVEL?",
        "thumb_text": "EL FIN DE MARVEL",
        "thumb_scene_idx": 0,
        "description": "Secret Wars #1 (Jonathan Hickman): La última incursión entre Tierra-616 y el Universo Ultimate donde nada pudo detener la extinción total.",
        "hashtags": "#SecretWars #SpiderMan #Avengers #MarvelComics #Multiverso #Comics #Reels",
        "scenes": [
            {
                "src": SW01[0],
                "text": "Durante décadas los héroes de Marvel lograron salvar la Tierra de cada invasión alienígena, hasta el día en que dos universos chocaron frente a frente.",
            },
            {
                "src": SW01[13],
                "text": "Sobre los cielos de Manhattan apareció otra Nueva York exactamente igual desatando la incursión final: solo quedaban minutos antes de la extinción total.",
            },
            {
                "src": SW01[24],
                "text": "Los Vengadores, los X-Men y los Hijos del Mañana se lanzaron a una guerra desesperada intentando destruir el otro planeta para salvar a sus propias familias.",
            },
            {
                "src": SW01[29],
                "text": "En medio del cielo en llamas, las flotas de helicarriers cayeron en picada mientras Punisher, Spider-Man y el Capitán América combatían hasta el último aliento.",
            },
            {
                "src": SW01[33],
                "text": "Ni siquiera Cyclops liberando el poder del Fénix ni los golpes de Hulk lograron frenar el impacto inevitable de ambas realidades colisionando.",
            },
            {
                "src": SW01[38],
                "text": "Reed Richards construyó un bote salvavidas desesperado para preservar el futuro de la humanidad mientras el universo entero se partía en dos.",
            },
            {
                "src": SW01[41],
                "text": "En la escena más desgarradora de todas, la nave falló y Sue Storm y sus hijos fueron tragados por el vacío blanco ante los ojos rotos de Reed.",
            },
            {
                "src": SW01[46],
                "text": "Con un blanco absoluto terminó la historia de Marvel de 1961 a 2015. ¿Recuerdas qué sentiste la primera vez que leíste este final?",
            },
        ],
    },
    {
        "slot": 24,
        "queue_folder": "024_fc_planet_hulk_95_hulk_vs_silver_surfer",
        "id": "fc_24_planet_hulk_95_hulk_vs_silver_surfer",
        "folder": "fc_24_planet_hulk_95_hulk_vs_silver_surfer",
        "title": "Planet Hulk #95: ¡Silver Surfer Cayó Esclavo y Hulk Casi Lo Mata a Golpes! 💚🛸💥",
        "character": "Hulk",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ SILVER SURFER PELEÓ A MUERTE CON HULK?",
        "thumb_text": "ESCLAVO EN LA ARENA",
        "thumb_scene_idx": 0,
        "description": "Incredible Hulk #95 (Planet Hulk): Debilitado por un disco de obediencia, Silver Surfer fue obligado a enfrentar al Cicatriz Verde en el coliseo de Sakaar.",
        "hashtags": "#PlanetHulk #Hulk #SilverSurfer #MarvelComics #Sakaar #Comics #Reels",
        "scenes": [
            {
                "src": PH095[0],
                "text": "En el coliseo sangriento del planeta Sakaar, el emperador tirano lanzó contra Hulk al arma secreta más temible que había esclavizado: Silver Surfer.",
            },
            {
                "src": PH095[4],
                "text": "Debilitado por el agujero negro y sometido con un disco de obediencia letal, el antiguo heraldo de Galactus fue obligado a pelear contra su propia voluntad.",
            },
            {
                "src": PH095[7],
                "text": "Hulk y sus hermanos gladiadores esperaban una ejecución rápida frente a la multitud hambrienta de sangre que llenaba el estadio gigante.",
            },
            {
                "src": PH095[9],
                "text": "Con una armadura plateada brillante y un mazo de guerra en su mano, Norrin Radd descendió de los cielos como el campeón invicto del Salvaje.",
            },
            {
                "src": PH095[10],
                "text": "En el primer choque titánico, el escudo de Hulk se estrelló contra el poder cósmico haciendo temblar toda la ciudad imperial bajo sus pies.",
            },
            {
                "src": PH095[13],
                "text": "El combate escaló hasta romper la arena entera mientras Hulk absorbía ráfagas solares directas en su pecho sin dar ni un solo paso atrás.",
            },
            {
                "src": PH095[14],
                "text": "Finalmente la ira del Cicatriz Verde estalló sin control: saltó sobre Surfer destrozando su tabla y golpeando su rostro sin piedad contra la tierra.",
            },
            {
                "src": PH095[21],
                "text": "Al ver destruido el disco que los controlaba, Silver Surfer recuperó su mente y liberó a los gladiadores. ¿Quién habría ganado sin el disco de control?",
            },
        ],
    },
    {
        "slot": 25,
        "queue_folder": "025_fc_cosmic_ghost_rider_origen_punisher_galactus",
        "id": "fc_25_cosmic_ghost_rider_origen_punisher_galactus",
        "folder": "fc_25_cosmic_ghost_rider_origen_punisher_galactus",
        "title": "Cosmic Ghost Rider: ¡Cómo Punisher Sirvió a Galactus y al Rey Thanos! 💀🔥⛓️",
        "character": "Ghost Rider",
        "voice_mode": "referencia",
        "hook_card": "¿EL ORIGEN MÁS LOCO DE PUNISHER EN MARVEL?",
        "thumb_text": "HERALDO DEL INFIERNO",
        "thumb_scene_idx": 0,
        "description": "Thanos #16 (Donny Cates): El delirante origen de Cosmic Ghost Rider cuando Frank Castle murió, pactó con Mephisto y se unió a Galactus.",
        "hashtags": "#CosmicGhostRider #Punisher #Galactus #Thanos #MarvelComics #Comics #Reels",
        "scenes": [
            {
                "src": TW[47],
                "text": "Aunque pocos lo saben, la mano derecha más letal y perturbadora del Rey Thanos fue en realidad un hombre que conocimos muy bien: Frank Castle, el Punisher.",
            },
            {
                "src": TW[63],
                "text": "En el día final de la Tierra, Frank murió acribillado defendiendo el planeta con sus últimas balas mientras Thanos ejecutaba a todos los héroes.",
            },
            {
                "src": TW[66],
                "text": "Al caer en lo más profundo del infierno, Frank hizo un trato desesperado con Mephisto pidiendo regresar con vida para castigar al Titán Loco.",
            },
            {
                "src": TW[67],
                "text": "Despertó convertido en el nuevo Ghost Rider sobre una Tierra muerta, enloqueciendo durante milenios en soledad al descubrir que no quedaba nadie a quien castigar.",
            },
            {
                "src": TW[68],
                "text": "Siglos después llegó un Galactus gravemente herido huyendo de Thanos, suplicando ayuda frente al único ser sobreviviente de aquel mundo en cenizas.",
            },
            {
                "src": TW[70],
                "text": "Frank aceptó servirle con una condición: beber el Poder Cósmico. Así se fusionaron el fuego infernal y la energía estelar en un solo monstruo.",
            },
            {
                "src": TW[72],
                "text": "Durante décadas el Cosmic Ghost Rider cabalgó las estrellas cazando mundos junto al Devorador, hasta que finalmente encontraron al Rey Thanos.",
            },
            {
                "src": TW[74],
                "text": "Pero Thanos decapitó a Galactus en un segundo obligando a Frank a jurarle lealtad eterna. ¿Te imaginabas esta locura de origen para Frank Castle?",
            },
        ],
    },
    {
        "slot": 26,
        "queue_folder": "026_fc_books_of_doom_6_conquista_latveria",
        "id": "fc_26_books_of_doom_6_conquista_latveria",
        "folder": "fc_26_books_of_doom_6_conquista_latveria",
        "title": "Books of Doom #6: ¡El Día que Victor Von Doom Derrocó al Tirano y Tomó Latveria! 👑🏰⚡",
        "character": "Doctor Doom",
        "voice_mode": "zazoom",
        "hook_card": "¿CÓMO VICTOR VON DOOM CONQUISTÓ SU PROPIO PAÍS?",
        "thumb_text": "REY DE LATVERIA",
        "thumb_scene_idx": 0,
        "description": "Books of Doom #6 (Ed Brubaker): La sangrienta rebelión con la que Victor regresó a su patria para derrocar al barón tirano y mostrar su verdadero rostro.",
        "hashtags": "#DoctorDoom #BooksOfDoom #Latveria #MarvelComics #Villanos #Comics #Reels",
        "scenes": [
            {
                "src": BOD6[14],
                "text": "Antes de amenazar al universo entero, Victor Von Doom tuvo que liberar a su propia tierra natal del sangriento régimen que asesinó a toda su familia.",
            },
            {
                "src": BOD6[2],
                "text": "Tras años en el exilio perfeccionando su armadura mágica, regresó a las fronteras de Latveria reuniendo a los campesinos perseguidos en un ejército rebelde.",
            },
            {
                "src": BOD6[8],
                "text": "Marchando en plena noche sobre las colinas del castillo real, sus tropas aplastaron a la guardia armada abriendo paso hasta el corazón del palacio.",
            },
            {
                "src": BOD6[12],
                "text": "Irrompiendo a través de los ventanales reales con rayos de energía, Doom confrontó al viejo monarca cobarde que había condenado a su pueblo al hambre.",
            },
            {
                "src": BOD6[13],
                "text": "Frente a un tirano que suplicaba por piedad de rodillas, Victor le rompió la resistencia sin dudar reclamando para siempre la corona legítima.",
            },
            {
                "src": BOD6[15],
                "text": "Aclamado por una nación entera que por fin veía caer sus cadenas, Latveria renació convertida en una superpotencia protegida con puño de hierro.",
            },
            {
                "src": BOD6[16],
                "text": "Desde ese trono oculto siguió realizando oscuros rituales contra el infierno cada año intentando rescatar el alma perdida de su propia madre.",
            },
            {
                "src": BOD6[19],
                "text": "Y cuando una periodista se atrevió a grabar su rostro desfigurado sin máscara, desapareció para siempre. ¿Fue Doom un salvador o un tirano peor?",
            },
        ],
    },
    {
        "slot": 27,
        "queue_folder": "027_fc_wolverine_vs_she_hulk_betty_ross",
        "id": "fc_27_wolverine_vs_she_hulk_betty_ross",
        "folder": "fc_27_wolverine_vs_she_hulk_betty_ross",
        "title": "Ultimate Wolverine vs Hulk: ¡La Sorpresa Mortal de Betty Ross Que Nadie Esperaba! 🐺💚🩸",
        "character": "Hulk",
        "voice_mode": "referencia",
        "hook_card": "¿QUIÉN ERA LA NUEVA SHE-HULK EN ULTIMATE MARVEL?",
        "thumb_text": "LA TRAICIÓN DE BETTY",
        "thumb_scene_idx": 0,
        "description": "Ultimate Wolverine vs. Hulk #4–5: La traición biológica de Betty Ross con la sangre de Banner y el choque triple contra Wolverine.",
        "hashtags": "#SheHulk #Hulk #Wolverine #UltimateMarvel #MarvelComics #Comics #Reels",
        "scenes": [
            {
                "src": WVH[91],
                "text": "Después de partir a Wolverine en dos en el Tíbet, Bruce Banner creyó estar a salvo, sin imaginar la traición mortal que preparaba su exesposa Betty Ross.",
            },
            {
                "src": WVH[68],
                "text": "Mientras SHIELD intentaba cazar tanto a Hulk como a Logan, una nueva y colosal She-Hulk apareció entre las montañas con un poder jamás visto.",
            },
            {
                "src": WVH[69],
                "text": "Nadie en la agencia sabía cómo había nacido este tercer monstruo capaz de destrozar a golpes simultáneamente al gigante verde y al mutante.",
            },
            {
                "src": WVH[73],
                "text": "Semanas antes, desesperada por los secretos militares de Nick Fury, Betty robó muestras modificadas del suero que Banner había ocultado en laboratorio.",
            },
            {
                "src": WVH[81],
                "text": "Cuando el propio Fury ordenó eliminar a Betty disparándole con un francotirador para borrar las pruebas del proyecto, cometió un error fatal.",
            },
            {
                "src": WVH[87],
                "text": "Herida y furiosa dentro del avión militar, Betty se inyectó la fórmula prohibida sufriendo una transformación monstruosa e imparable en pleno vuelo.",
            },
            {
                "src": WVH[88],
                "text": "Con fuerza capaz de desgarrar el acero blindado y humillar a los agentes élite, la nueva She-Hulk se lanzó directa contra ambos colosos.",
            },
            {
                "src": WVH[89],
                "text": "Acorralados en una batalla salvaje a tres bandas, el suelo entero colapsó bajo sus golpes. ¿Sabías que Betty fue She-Hulk en este universo?",
            },
        ],
    },
    {
        "slot": 28,
        "queue_folder": "028_fc_uncanny_xforce_archangel_apocalipsis",
        "id": "fc_28_uncanny_xforce_archangel_apocalipsis",
        "folder": "fc_28_uncanny_xforce_archangel_apocalipsis",
        "title": "Uncanny X-Force: ¡El Despertar Oscuro de Archangel Que Casi Extermina al Equipo! 🪽🩸⚔️",
        "character": "Wolverine",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ ARCHANGEL TRAICIONÓ A LOS X-MEN?",
        "thumb_text": "HEREDERO DE APOCALIPSIS",
        "thumb_scene_idx": 0,
        "description": "Uncanny X-Force (La Saga del Ángel Oscuro): Cuando la semilla de la muerte tomó el control total de Warren Worthington contra sus propios amigos.",
        "hashtags": "#Archangel #UncannyXForce #Wolverine #XMen #Apocalipsis #MarvelComics #Reels",
        "scenes": [
            {
                "src": UXF[52],
                "text": "Durante años Warren Worthington luchó para contener la maldición metálica en su sangre, hasta que la semilla de Apocalipsis despertó por completo en su mente.",
            },
            {
                "src": UXF[51],
                "text": "En medio de una emboscada brutal dentro de la base enemiga, los Jinetes Finales activaron la transformación oscura del antiguo ángel de los X-Men.",
            },
            {
                "src": UXF[62],
                "text": "Entre gritos desgarradores mientras su piel volvía a tornarse azul, las alas de acero de Archangel crecieron listas para aniquilar todo ser vivo.",
            },
            {
                "src": UXF[63],
                "text": "Sus propios compañeros intentaron contenerlo desesperadamente, pero cada ataque era inútil frente a un guerrero convertido en dios de la muerte.",
            },
            {
                "src": UXF[67],
                "text": "Los colosos enemigos cayeron destrozados en segundos mientras X-Force comprendía que el antiguo amigo que amaban ya había dejado de existir.",
            },
            {
                "src": UXF[73],
                "text": "Alzándose sobre el campo de ruinas en la luna, Archangel juró borrar el mundo viejo para iniciar una nueva era de evolución sangrienta.",
            },
            {
                "src": UXF[76],
                "text": "Wolverine, Psylocke y Deadpool se vieron obligados a cazar a su propio hermano antes de que desatara el apocalipsis final sobre la Tierra.",
            },
            {
                "src": UXF[81],
                "text": "En la pelea más triste y violenta del equipo, Psylocke tuvo que tomar una decisión imposible. ¿Crees que Warren merecía ser salvado o detenido?",
            },
        ],
    },
    {
        "slot": 29,
        "queue_folder": "029_fc_iron_man_guerra_armaduras_orchis",
        "id": "fc_29_iron_man_guerra_armaduras_orchis",
        "folder": "fc_29_iron_man_guerra_armaduras_orchis",
        "title": "Invincible Iron Man: ¡Tony Stark Desató Su Armadura Más Mortal Contra la Traición! 🔴⚡🤖",
        "character": "Iron Man",
        "voice_mode": "referencia",
        "hook_card": "¿LA ARMADURA SECRETA QUE DESTRUYÓ A LOS TRAIDORES?",
        "thumb_text": "TRAICIÓN A TONY STARK",
        "thumb_scene_idx": 0,
        "description": "Invincible Iron Man (Gerry Duggan): Cuando le robaron su empresa e intentaron cazarlo, Tony Stark contraatacó con pura furia tecnológica.",
        "hashtags": "#IronMan #TonyStark #MarvelComics #Avengers #ComicsEnEspanol #Reels #Shorts",
        "scenes": [
            {
                "src": IM[4],
                "text": "Despojado de su propia fortuna, acusado de crímenes que no cometió y con sus armaduras en manos de sus peores enemigos, Tony Stark tocó fondo.",
            },
            {
                "src": IM[6],
                "text": "Feilong y la organización Orchis usaron las patentes de Industrias Stark para construir Centinelas letales diseñados específicamente para cazar mutantes y héroes.",
            },
            {
                "src": IM[7],
                "text": "Cansado de esconderse mientras usaban su legado para asesinar inocentes, Tony reapareció en mitad del desierto listo para recuperar lo suyo.",
            },
            {
                "src": IM[9],
                "text": "Al infiltrarse en la base armada oculta bajo tierra, Iron Man desató un bombardeo implacable pulverizando cada defensa automatizada en segundos.",
            },
            {
                "src": IM[10],
                "text": "Pero los traidores lo esperaban equipados con su vieja armadura sigilosa modificada, creyendo que podrían humillar y derrotar fácilmente al creador.",
            },
            {
                "src": IM[14],
                "text": "En un duelo aéreo a velocidad supersónica, Tony demostró por qué ningún impostor puede igualar al genio original destrozando su coraza pieza a pieza.",
            },
            {
                "src": IM[16],
                "text": "Mientras toda la instalación estallaba en llamas gigantes, Iron Man borró cada servidor secreto impidiendo que crearan nuevas armas con su nombre.",
            },
            {
                "src": IM[24],
                "text": "Tras aplastar a su enemigo con un último golpe directo en el rostro, Tony juró hacer caer todo el imperio de Orchis. ¿Cuál es tu armadura favorita?",
            },
        ],
    },
    {
        "slot": 30,
        "queue_folder": "030_fc_superman_seis_soles_world_forger",
        "id": "fc_30_superman_seis_soles_world_forger",
        "folder": "fc_30_superman_seis_soles_world_forger",
        "title": "Superman: ¡Voló a Través de Seis Soles y Noqueó a Un Dios De Un Solo Golpe! ☀️🦸‍♂️💥",
        "character": "Superman",
        "voice_mode": "zazoom",
        "hook_card": "¿QUÉ PASA CUANDO SUPERMAN ATRAVIESA SEIS SOLES?",
        "thumb_text": "EL GOLPE MÁS PODEROSO",
        "thumb_scene_idx": 0,
        "description": "Justice League #25 (Scott Snyder): Atrapado en la oscuridad de la Sexta Dimensión sin luz ni esperanza, Kal-El rompió todos sus límites para salvar a la Liga.",
        "hashtags": "#Superman #JusticeLeague #DCComics #KalEl #WorldForger #Comics #Reels",
        "scenes": [
            {
                "src": SUP / "chi.jpg",
                "text": "Todos conocemos la fuerza increíble de Superman bajo nuestro sol amarillo de la Tierra, pero nadie en el multiverso estaba preparado para presenciar el día en que Kal-El rompió todos sus límites conocidos frente a un dios creador.",
            },
            {
                "src": SUP / "world_forger_01.jpg",
                "text": "Traicionado y encerrado en un universo oscuro de la Sexta Dimensión sin una sola estrella ni rastro de luz solar, el todopoderoso Forjador de Mundos dejó morir lentamente al Hombre de Acero creyendo haberlo vencido para siempre.",
            },
            {
                "src": SUP / "str2.jpeg",
                "text": "Mientras el gigante divino preparaba su martillo cósmico para destruir la Liga de la Justicia y reescribir la realidad entera, Kal-El escuchó en el vacío el latido lejano de su hijo Jon llamándolo desde la distancia.",
            },
            {
                "src": SUP / "str1.jpeg",
                "text": "Sacando una última chispa de esperanza, Batman alineó seis soles en su camino a través de la oscuridad espacial. Superman despegó a velocidad imposible atravesando una estrella tras otra, absorbiendo radiación pura en cada segundo.",
            },
            {
                "src": SUP / "punch_panel.png",
                "text": "Transformado en un cometa dorado imparable, Superman descendió con el puño cargado de energía estelar y conectó un golpe devastador que destrozó al Forjador de Mundos y partió en dos el universo entero. ¿Es esta la hazaña más grande de Superman?",
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
    print(f"🎬 [LOTE 3 FILMCRAFT - VIDEO {slot}/30] {q_folder}", flush=True)
    print(f"   Título: {proj['title']}", flush=True)
    print(f"=======================================================", flush=True)

    curated_dir = CURATED_BASE / proj["folder"]
    curated_dir.mkdir(parents=True, exist_ok=True)
    work_dir = PROJECT_ROOT / "work" / f"filmcraft_lote3_slot_{slot:02d}"
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
        seq_name=f"Lote3_Slot_{slot:02d}",
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


def main():
    for proj in LOTE_03_PROJECTS:
        for i, sc in enumerate(proj["scenes"], start=1):
            p = Path(sc["src"])
            if not p.exists():
                raise FileNotFoundError(f"Missing asset for Slot {proj['slot']} scene {i}: {p}")
    print(f"✓ Verificadas las rutas de todas las viñetas de los {len(LOTE_03_PROJECTS)} videos del Lote 3.", flush=True)

    start_all = time.time()
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    summary = []

    for proj in LOTE_03_PROJECTS:
        try:
            dur, sz, st = produce_project(proj)
            summary.append((proj["slot"], proj["queue_folder"], dur, sz, st))
        except Exception as e:
            print(f"❌ ERROR en Slot {proj['slot']}: {e}", flush=True)
            summary.append((proj["slot"], proj["queue_folder"], 0.0, 0.0, f"ERROR: {e}"))

    elapsed_min = (time.time() - start_all) / 60.0
    print("\n" + "=" * 78, flush=True)
    print(f"AUDITORÍA FINAL - LOTE 3 FILMCRAFT 75s ({elapsed_min:.1f} min)", flush=True)
    print("=" * 78, flush=True)
    for slot, qf, dur, sz, st in summary:
        print(f"Slot {slot:02d} | {dur:6.2f}s | {sz:6.1f} MB | {st:<10} | {qf}", flush=True)
    print("=" * 78, flush=True)


if __name__ == "__main__":
    main()
