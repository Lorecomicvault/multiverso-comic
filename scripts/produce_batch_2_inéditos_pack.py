"""
Master Production Engine: Batch 2 (10 Videos Inéditos de 60 Segundos o Más)
==========================================================================
Requisitos:
1. Duración estrictamente >= 60.0s (narraciones calibradas a 195-210 palabras por video).
2. Viñetas canónicas 1:1 curadas en assets/curated_panels/<folder>/scene_01..04.jpg.
3. Rotación de ganchos virales en los primeros 3 segundos.
4. Salida en scheduled_queue/11_... a scheduled_queue/20_...
"""

import os
import sys
import json
import time
import shutil
import re
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
from src.cloud_runner import build_cloud_generation
from src.composer import get_duration

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_2_inéditos"
PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    {
        "slot": 11,
        "queue_folder": "11_red_hulk_golpea_watcher_humilla_thor",
        "id": "red_hulk_golpea_watcher_humilla_thor",
        "title": "¡La Mayor Falta de Respeto de Marvel! Red Hulk Noqueó a The Watcher 🔴💥",
        "character": "Red Hulk",
        "folder": "01_red_hulk_golpea_watcher_humilla_thor",
        "theme_signature": "red_hulk:golpea_watcher:humilla_thor_hulk_vol2",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Esta es la mayor falta de respeto en toda la historia de Marvel! Red Hulk no solo desafió a los Vengadores, sino que viajó hasta el Área Azul de la Luna para encarar al mismísimo Uatu el Vigilante, un ser cósmico juramentado a la no intervención que jamás espera ser atacado."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin mediar una sola palabra ni titubear un segundo, el coloso escarlata descargó un brutal derechazo demoledor que impactó de lleno en la mandíbula del ser todopoderoso. Uatu cayó noqueado y humillado sobre el polvo lunar, convirtiéndose en el primer Vigilante derribado por la fuerza bruta de un mortal."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Furioso ante tanta arrogancia blasfema, Thor descendió desde Asgard desatando relámpagos galácticos. Pero en un giro táctico demencial, Red Hulk aprovechó la gravedad cero del espacio exterior para sujetar el martillo místico junto al brazo de Thor, arrastrando al Dios del Trueno hacia el vacío cósmico sin soltarlo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al llegar a la Luna, Red Hulk utilizó la propia inercia y el peso colosal de Thor para azotarlo salvajemente contra los cráteres, golpeándolo con su propia fuerza mística. El heredero de Odín quedó inconsciente en la superficie, en una de las victorias más despiadadas y controvertidas de la era moderna."
            }
        ],
        "description": "El día en que Red Hulk golpeó a The Watcher en la Luna y humilló a Thor. La mayor falta de respeto cósmica en Hulk Vol. 2.",
        "hashtags": "#RedHulk #Thor #TheWatcher #MarvelComics #Comics #Shorts #Reels #TikTok"
    },
    {
        "slot": 12,
        "queue_folder": "12_wolverine_decapito_red_skull_escudo_capitan",
        "id": "wolverine_decapito_red_skull_escudo_capitan",
        "title": "¡Wolverine Decapitó a Red Skull con el Escudo del Capitán América! 🩸🛡️",
        "character": "Wolverine",
        "folder": "02_wolverine_decapito_red_skull_escudo_capitan",
        "theme_signature": "wolverine:old_man_logan:decapita_red_skull_escudo",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El final más sangriento y despiadado jamás dibujado en un cómic! Wolverine tomó el legendario escudo del Capitán América para ejecutar la venganza definitiva contra el temible Red Skull en su propia sala presidencial de trofeos macabros, rodeado por los recuerdos profanados de los héroes caídos de Marvel."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tras cincuenta largos años ocultando sus garras de adamantium en el exilio, Logan descubrió la masacre de su amada esposa e hijos a manos de la banda de los Hulks. Consumido por una furia ciega e imparable, atravesó las defensas militares de Washington hasta acorralar al tirano nazi que gobernaba el país."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Red Skull empuñó la espada ceremonial de Steve Rogers burlándose sádicamente de la caída de los Vengadores, creyéndose completamente intocable. Pero el viejo mutante le arrebató el escudo indestructible de vibranium con un rugido salvaje, blandiendo su borde afilado con una potencia titánica directo hacia la garganta del tirano."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "De un solo tajo desgarrador y demoledor, el disco metálico cercenó limpiamente la cabeza de Red Skull, que rodó por el piso alfombrado de la Casa Blanca. Aquel golpe implacable puso fin para siempre a su pesadilla totalitaria, consagrando el renacer más brutal e implacable en la historia de Wolverine."
            }
        ],
        "description": "La ejecución más brutal de Old Man Logan: Wolverine decapita a Red Skull usando el escudo del Capitán América.",
        "hashtags": "#Wolverine #OldManLogan #RedSkull #CaptainAmerica #Marvel #Comics #Shorts #Reels"
    },
    {
        "slot": 13,
        "queue_folder": "13_hal_jordan_masacre_green_lantern_corps_parallax",
        "id": "hal_jordan_masacre_green_lantern_corps_parallax",
        "title": "¡Hal Jordan Perdió la Cordura y Masacró a los Green Lanterns! 🟢💀⚡",
        "character": "Green Lantern",
        "folder": "03_hal_jordan_masacre_green_lantern_corps_parallax",
        "theme_signature": "green_lantern:emerald_twilight:masacre_corps_parallax",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El día en que el mayor héroe de DC perdió la cordura y masacró a todos sus hermanos de armas! Tras contemplar su amada Coast City reducida a un cráter de cenizas radiactivas por Mongul, Hal Jordan utilizó todo el poder de su anillo para intentar resucitar a siete millones de inocentes."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Pero los arrogantes Guardianes de Oa proyectaron sus hologramas para prohibirle alterar el destino, exigiéndole entregarse a juicio y despojarlo de su anillo. Enloquecido de dolor y con el corazón destrozado, Hal desconectó su brújula moral y voló a máxima velocidad espacial hacia el planeta central con un único objetivo: drenarlo todo."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Uno a uno, los más nobles campeones de la corporación intentaron frenar su avance implacable en la órbita de Oa. Sin embargo, Hal los derrotó sin piedad alguna en el vacío del cosmos, arrancándoles sus anillos esmeralda con violencia para colocárselos todos en sus propios dedos ensangrentados y llenos de poder."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Tras quebrar el cuello de Sinestro y desintegrar a su querido mentor Kilowog, Hal Jordan se sumergió voluntariamente dentro de la Batería Central de Poder. Allí absorbió billones de años de energía verde pura, destruyendo la corporación y renaciendo ante el multiverso como la temible y todopoderosa entidad llamada Parallax."
            }
        ],
        "description": "Cuando Hal Jordan cayó en la locura y aniquiló a los Green Lantern Corps para convertirse en Parallax. Emerald Twilight.",
        "hashtags": "#GreenLantern #HalJordan #Parallax #DCComics #DC #Comics #Shorts #Reels"
    },
    {
        "slot": 14,
        "queue_folder": "14_spiderman_noquea_firelord_heraldo_galactus",
        "id": "spiderman_noquea_firelord_heraldo_galactus",
        "title": "¡Spider-Man Olvidó Contenerse y Noqueó a un Heraldo de Galactus! 🕷️🔥💥",
        "character": "Spider-Man",
        "folder": "04_spiderman_noquea_firelord_heraldo_galactus",
        "theme_signature": "spiderman:amazing_spider_man_270:noquea_firelord_galactus",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Nadie creía que Spider-Man pudiera noquear a puño limpio al mismísimo heraldo cósmico de Galactus! Cuando el ardiente Firelord aterrizó furioso en Manhattan calcinando rascacielos con llamaradas estelares capaces de derretir planetas, Peter Parker comprendió de inmediato que nadie en la ciudad acudiría a tiempo para salvarlo."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Completamente superado en escala de poder por un ser de pura energía viva, Peter recurrió a su extrema agilidad y astucia urbana: le arrojó vigas de acero candente, derribó sobre él los escombros de un edificio en construcción e incluso lo arrastró hasta una gasolinera que estalló en una bola de fuego devastadora."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero entre el humo abrasador, Firelord emergió totalmente ileso y sediento de sangre. En ese segundo crítico de terror absoluto, sabiendo que un solo toque de su vara incineraría su cuerpo, Peter desconectó por primera vez su código moral de contención y desató una ráfaga demencial de golpes continuos a velocidad sobrehumana."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con los nudillos destrozados y cegado por el pánico de morir, Spider-Man impactó al semidiós cósmico docenas de veces hasta quebrantar su resistencia alienígena y dejarlo noqueado en el asfalto. Tuvieron que intervenir el Capitán América y los Vengadores para apartar a Peter antes de que matara a golpes al heraldo."
            }
        ],
        "description": "La hazaña física más brutal de Spider-Man: Peter Parker noquea a Firelord, heraldo de Galactus, a puño limpio.",
        "hashtags": "#SpiderMan #PeterParker #Firelord #Galactus #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 15,
        "queue_folder": "15_daredevil_nuevo_rey_del_crimen_hells_kitchen",
        "id": "daredevil_nuevo_rey_del_crimen_hells_kitchen",
        "title": "¡Daredevil Destrozó a Kingpin y se Proclamó el Nuevo Rey del Crimen! 😈👑🩸",
        "character": "Daredevil",
        "folder": "05_daredevil_nuevo_rey_del_crimen_hells_kitchen",
        "theme_signature": "daredevil:hardcore_issue_50:nuevo_kingpin_hells_kitchen",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¿Qué pasa cuando empujas al hombre sin miedo mucho más allá de su límite moral? Agotado tras años de sangrientas guerras de mafia que devastaban Hell's Kitchen, Matt Murdock comprendió que los tribunales jamás detendrían a los monstruos que destruían su vecindario y amenazaban la vida de los suyos."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Wilson Fisk regresó a Nueva York decidido a reclamar su imperio criminal con intimidaciones sangrientas y ataques coordinados contra los aliados más cercanos de Matt. Confiado en su enorme tamaño y en que el héroe ciego jamás violaría su sagrado juramento de no matar, Kingpin creyó tener el control absoluto de la situación."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sin embargo, Murdock colapsó emocionalmente y se transformó en un ejecutor salvaje. En un enfrentamiento brutal y claustrofóbico a puño cerrado, Daredevil demolió a golpes la mandíbula y las costillas de Wilson Fisk, castigando su enorme anatomía con una furia animal que dejó al criminal cubierto de su propia sangre e indefenso."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Daredevil arrastró el cuerpo destrozado de Fisk hasta el bar de los mafiosos, arrojó sus restos ensangrentados sobre la mesa de billar y se quitó la máscara frente a docenas de capos aterrorizados. Con voz gélida, Matt les advirtió que si necesitaban un rey a quien temer, desde ese momento él era el nuevo Kingpin."
            }
        ],
        "description": "Cuando Matt Murdock rompió todos sus límites, destruyó a Wilson Fisk y se proclamó Kingpin de Hell's Kitchen.",
        "hashtags": "#Daredevil #MattMurdock #Kingpin #WilsonFisk #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 16,
        "queue_folder": "16_joker_mascara_cara_rebanada_death_of_family",
        "id": "joker_mascara_cara_rebanada_death_of_family",
        "title": "¡La Escena Más Turbia de Batman! Joker se Arrancó su Propia Cara 🃏🪓😱",
        "character": "Joker",
        "folder": "06_joker_mascara_cara_rebanada_death_of_family",
        "theme_signature": "joker:death_of_the_family:cara_rebanada_dollmaker",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Esta es la escena más perturbadora y censurada en toda la historia editorial de Batman! El Joker se despojó voluntariamente de la carne de su propio rostro sólo para enviarle un mensaje macabro al Caballero Oscuro: su locura enfermiza trasciende por completo el dolor físico y los límites de la mente humana."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "La atrocidad inició en lo profundo de los túneles del Asilo Arkham, donde el payaso encerrado pactó con el sádico cirujano clandestino Dollmaker. Guiado por una calma siniestra, permitió que le rebanaran con bisturí toda la piel de la cara, dejando el trozo carnoso clavado en la celda antes de desvanecerse en las cloacas."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Un año después de su desaparición, la pesadilla regresó a la jefatura de policía de Gotham en plena medianoche. Cortando la energía de la morgue, el asesino degolló silenciosamente a decenas de agentes en la penumbra para recuperar su rostro momificado, fijándolo de nuevo a su cabeza mediante toscos cinturones de cuero y garfios metálicos."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con su máscara putrefacta emanando un hedor pestilente y moscas revoloteando sobre su carne marchita, el Joker secuestró a toda la Batfamilia en las cavernas. Allí desató un banquete sádico y psicológico, intentando convencer a Bruce de que el odio que los une es infinitamente más poderoso que el amor hacia sus protegidos."
            }
        ],
        "description": "La historia más oscura del Joker en The New 52: se extirpa su rostro y regresa para torturar a la Batfamilia en Death of the Family.",
        "hashtags": "#Joker #Batman #DeathOfTheFamily #DCComics #DC #Comics #Shorts #Reels"
    },
    {
        "slot": 17,
        "queue_folder": "17_punisher_masacre_funeral_familia_mafia",
        "id": "punisher_masacre_funeral_familia_mafia",
        "title": "¡The Punisher Masacró a la Mafia en Pleno Funeral! 💀⚰️🔫",
        "character": "The Punisher",
        "folder": "07_punisher_masacre_funeral_familia_mafia",
        "theme_signature": "punisher:welcome_back_frank_issue_1:masacre_funeral_gnucci",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Frank Castle jamás negocia ni ofrece tregua alguna cuando se trata de castigar al hampa! En pleno funeral solemne de la temida familia criminal Gnucci, los capos, lugartenientes y guardaespaldas de la mafia creían sentirse invulnerables, rodeados por decenas de sicarios fuertemente armados y respaldados por millones en sobornos policiales."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "La implacable matriarca Ma Gnucci reunió a toda su cúpula de poder en el cementerio de Long Island para despedir a uno de sus hijos ejecutados, jurando venganza despiadada contra el justiciero en las sombras. Ninguno sospechaba que aquella reunión pública en el panteón familiar se convertiría en su sentencia de muerte colectiva."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Oculto en lo alto de un campanario adyacente cubierto por la vegetación, The Punisher mantenía el pulso firme observando a sus presas a través de la mira telescópica militar. Con una frialdad matemática gélida, calculó la distancia, la dirección del viento y la secuencia exacta de disparos para no permitir que ninguno escapara con vida."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En una fracción de segundo, el estruendo de proyectiles de alto calibre destrozó los ataúdes y abatió en cadena a los principales operadores de la familia en medio de una lluvia de plomo y esquirlas. El entierro derivó en un caos ensangrentado donde la organización criminal quedó descabezada, marcando el implacable retorno de The Punisher."
            }
        ],
        "description": "El día en que Frank Castle ejecutó a los líderes de la mafia Gnucci en pleno cementerio durante un funeral.",
        "hashtags": "#ThePunisher #FrankCastle #GnucciFamily #MarvelComics #Comics #Shorts #Reels"
    },
    {
        "slot": 18,
        "queue_folder": "18_superman_vuela_seis_soles_noquea_world_forger",
        "id": "superman_vuela_seis_soles_noquea_world_forger",
        "title": "¡Superman Atravesó Seis Soles y Noqueó a un Dios Cósmico! ☀️💥🌌",
        "character": "Superman",
        "folder": "08_superman_vuela_seis_soles_noquea_world_forger",
        "theme_signature": "superman:justice_league_25:seis_soles_world_forger",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Ni siquiera una deidad creadora de multiversos pudo soportar el impacto de este golpe histórico! Encerrado en una dimensión desierta y agonizante sin una sola estrella en millones de años luz a la redonda, Superman se encontraba colapsando al borde de la asfixia, completamente desprovisto de radiación solar para recargar su fuerza."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "En el centro del Sexto Cosmos, el World Forger empuñaba su mazo monumental sobre el yunque cósmico, preparado para reemplazar la línea temporal de la Tierra con una realidad supuestamente perfecta donde la libertad no existía, convencido de que el Hombre de Acero jamás lograría escapar de su trampa espacial."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero motivado por los recuerdos de su familia y la fe inquebrantable de la Liga de la Justicia, Superman desafió todas las leyes cósmicas: dio un salto colosal que fracturó el tejido espacial, acelerando a velocidades inimaginables en línea recta para atravesar en secuencia seis soles radiantes que sobrecargaron cada una de sus células kryptonianas."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Convertido en una supernova viviente envuelta en destellos dorados, el Hombre del Mañana colisionó a la velocidad de la luz contra la mandíbula del titán creador. El descomunal impacto pulverizó el yunque extradimensional en mil pedazos y noqueó en seco al World Forger, salvando toda la existencia del multiverso conocido."
            }
        ],
        "description": "La mayor hazaña de Superman: vuela a través de seis soles para noquear de un solo golpe al World Forger en Justice League #25.",
        "hashtags": "#Superman #JusticeLeague #WorldForger #DCComics #DC #Comics #Shorts #Reels"
    },
    {
        "slot": 19,
        "queue_folder": "19_thor_muerte_serpiente_midgard_nueve_pasos",
        "id": "thor_muerte_serpiente_midgard_nueve_pasos",
        "title": "¡Nueve Pasos Hacia la Muerte! El Sacrificio Legendario de Thor ⚡🐍⚰️",
        "character": "Thor",
        "folder": "09_thor_muerte_serpiente_midgard_nueve_pasos",
        "theme_signature": "thor:thor_380:serpiente_midgard_nueve_pasos",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡Nueve pasos fatales hacia la eternidad inmortal! La batalla más apocalíptica, grandiosa y desgarradora de Asgard se desató cuando la gigantesca Serpiente de Midgard emergió de las profundidades insondables de los reinos, rodeando el planeta entero para hacer realidad la fatídica profecía nórdica del Ragnarok y devorar la Tierra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con sus huesos totalmente frágiles y convertidos en cristal quebradizo por una maldición sádica de Hela, Thor debió enfundarse en una armadura de oro místico para que su cuerpo no colapsara bajo su propio peso. A pesar del dolor inhumano, el Dios del Trueno liberó un cataclismo de relámpagos que partió el firmamento en dos."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En un enfrentamiento titánico narrado en verso nórdico que sacudió los cimientos del árbol Yggdrasil, Thor canalizó la totalidad de su divinidad en una acometida desesperada. Blandiendo a Mjolnir con una fuerza incontenible, estrelló el martillo contra el cráneo colosal del monstruo, provocando una explosión atronadora que destrozó para siempre a la bestia."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Empapado por la niebla tóxica que emanaba de la serpiente agonizante, el Dios del Trueno dio exactamente nueve pasos tambaleantes hacia el horizonte antes de desplomarse inerte. Su espíritu ascendió a los cielos, dejando sobre el campo de batalla únicamente su armadura vacía y su fiel martillo como tributo a su máximo sacrificio."
            }
        ],
        "description": "La profecía nórdica en Thor #380: la batalla a muerte contra Jormungand y los legendarios nueve pasos de Thor.",
        "hashtags": "#Thor #MidgardSerpent #Jormungand #MarvelComics #Asgard #Comics #Shorts #Reels"
    },
    {
        "slot": 20,
        "queue_folder": "20_flash_barry_allen_se_convierte_en_rayo_crisis",
        "id": "flash_barry_allen_se_convierte_en_rayo_crisis",
        "title": "¡El Secreto del Rayo! Barry Allen Creó su Propio Origen al Morir ⚡🏃‍♂️🌀",
        "character": "The Flash",
        "folder": "10_flash_barry_allen_se_convierte_en_rayo_crisis",
        "theme_signature": "flash:crisis_on_infinite_earths:se_convierte_en_rayo",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El secreto cósmico más alucinante, fascinante y emotivo en la mitología de DC! El día en que el noble Barry Allen corrió hacia su trágico destino en la Crisis en Tierras Infinitas, su heroico sacrificio escondía una paradoja cuántica eterna que terminó dando origen a todos los velocistas del multiverso."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El gigantesco cañón de antimateria construido por el temible Anti-Monitor estaba a punto de disparar su haz letal para aniquilar los últimos universos de materia positiva. Con todos los demás superhéroes derrotados o incapaces de ingresar a la cámara de energía pura, Flash supo que detener aquella máquina exigiría entregar su propia existencia."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Sin vacilar, Barry corrió en sentido contrario al vórtice a una velocidad que superó la luz y las leyes del tiempo. Su avance desesperado generó una contrapresión que comenzó a consumir el cañón cósmico, pero la brutal fricción de la Speed Force fue desintegrando progresivamente su traje carmesí y desgastando su cuerpo biológico hasta evaporarlo."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Sin embargo, su energía vital no pereció en la nada: se transformó en un relámpago dorado de pura conciencia que viajó hacia atrás a través de las corrientes del tiempo. Aquel rayo atravesó la ventana del laboratorio policial en el pasado para golpear al joven Barry Allen junto a los químicos, creando el ciclo infinito de Flash."
            }
        ],
        "description": "El sacrificio supremo de Barry Allen en Crisis on Infinite Earths y la paradoja del rayo que le dio sus poderes.",
        "hashtags": "#TheFlash #BarryAllen #CrisisOnInfiniteEarths #DCComics #SpeedForce #Comics #Shorts #Reels"
    }
]

def produce_single_project(proj):
    proj_id = proj["id"]
    slot_num = proj["slot"]
    queue_name = proj["queue_folder"]
    print(f"\n{'='*70}")
    print(f"🎬 PRODUCIENDO SLOT {slot_num}: {proj['title']}")
    print(f"{'='*70}")

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

    work_dir = PROJECT_ROOT / "work" / f"batch2_{proj_id}"
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
    else:
        print(f"✅ EXCELENTE: Duración {dur:.2f}s >= 60.0s (CALIDAD GARANTIZADA)")

    # Thumbnail
    thumb_path = Path(final_video_path).parent / f"{Path(final_video_path).stem}_thumb.jpg"
    if not thumb_path.exists():
        thumb_path = Path(final_video_path).with_suffix('.jpg')

    # Encolar en scheduled_queue
    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest_video = dest_dir / "video.mp4"
    dest_thumb = dest_dir / "thumb.jpg"
    dest_meta = dest_dir / "metadata.json"

    shutil.copy2(final_video_path, dest_video)
    if thumb_path.exists():
        shutil.copy2(thumb_path, dest_thumb)
    else:
        from src.composer import extract_thumbnail
        extract_thumbnail(str(dest_video), str(dest_thumb), at_second=3.0)

    meta_content = {
        "title": proj["title"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "character": proj["character"],
        "theme_signature": proj["theme_signature"],
        "duration_seconds": round(dur, 2),
        "scheduled_slot": slot_num,
        "queue_folder": queue_name,
        "source": "curated_canonical_interior_panels",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    dest_meta.write_text(json.dumps(meta_content, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"🚀 ENCOLADO EXITOSO EN: {dest_dir}")
    return dest_dir

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Produce Batch 2 de 10 videos inéditos de 60s+")
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
        print("Iniciando producción en lote de los 10 videos...")
        for p in PROJECTS:
            produce_single_project(p)
    else:
        print("Uso: python produce_batch_2_inéditos_pack.py --all  o  --index <1-10>")

if __name__ == "__main__":
    main()
