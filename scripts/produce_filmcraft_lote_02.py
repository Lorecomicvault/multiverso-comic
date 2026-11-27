"""
Lote 2 Maestro (FilmCraft 60FPS + Voicebox 0.6B ES) — Slots 11 al 20 (~75 Segundos)
=================================================================================
10 nuevas historias virales Tier-1 con contexto narrativo completo (~1m 15s),
editadas 100% en FilmCraft GPU (1080x1920 @ 60fps), con Close-Up Icónico en Escena 1
para maximizar retención en los primeros 3 segundos.
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


TW = _sorted_imgs(SRC / "thanos_wins" / "extracted_pages")
BOD4 = _sorted_imgs(SRC / "books_of_doom" / "extracted_pages" / "200604 Books of Doom 004")
UXF = _sorted_imgs(SRC / "uncanny_xforce" / "extracted_pages")
CFJ = _sorted_imgs(SRC / "cry_for_justice" / "extracted")
SIEGE = _sorted_imgs(SRC / "siege")
ULT = _sorted_imgs(SRC / "ultimatum" / "extracted_pages")
SCH = _sorted_imgs(SRC / "xmen_schism")
RUINS = _sorted_imgs(SRC / "marvel_ruins")
DD50 = CURATED_BASE / "05_daredevil_nuevo_rey_del_crimen_hells_kitchen"


LOTE_02_PROJECTS = [
    {
        "slot": 11,
        "queue_folder": "011_fc_silver_surfer_mjolnir_vs_rey_thanos",
        "id": "fc_11_silver_surfer_mjolnir_vs_rey_thanos",
        "folder": "fc_11_silver_surfer_mjolnir_vs_rey_thanos",
        "title": "¡El Día que Silver Surfer Levantó el Mjolnir de Thor Para Matar a Thanos! ⚡🔨🌌",
        "character": "Silver Surfer",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ SILVER SURFER EMPUÑÓ EL MARTILLO DE THOR?",
        "thumb_text": "DIGNO DE MJOLNIR",
        "thumb_scene_idx": 0,
        "description": "Thanos #17 (Donny Cates): El momento épico en el fin de los tiempos cuando Norrin Radd se volvió digno del Mjolnir para enfrentar al Rey Thanos.",
        "hashtags": "#SilverSurfer #Thanos #Mjolnir #Thor #MarvelComics #Comics #Reels #Shorts",
        "scenes": [
            {
                "src": TW[81],
                "text": "En un futuro oscuro donde casi todo el universo fue exterminado por el Rey Thanos, un último guerrero surgió de las estrellas empuñando el mítico martillo de Thor.",
            },
            {
                "src": TW[83],
                "text": "Durante milenios Norrin Radd vagó por galaxias muertas esperando volverse digno del Mjolnir, preparándose en secreto para vengar a cada héroe asesinado.",
            },
            {
                "src": TW[84],
                "text": "Con su piel ennegrecida por la fuerza cósmica de la Aniquilación, el Caído enfrentó cara a cara al Rey Thanos y a su versión más joven frente al trono.",
            },
            {
                "src": TW[89],
                "text": "Ni siquiera el Ghost Rider Cósmico pudo frenar el descenso de Surfer, quien desató relámpagos divinos sobre la fortaleza destruyendo todo a su paso.",
            },
            {
                "src": TW[91],
                "text": "Incluso cuando Thanos soltó de sus cadenas a un Hulk salvaje y anciano para devorarlo vivo, el poder combinado del martillo logró contener a la bestia.",
            },
            {
                "src": TW[96],
                "text": "Pero el combate contra dos versiones del Titán Loco era imposible de ganar solo. En un descuido mortal, Thanos atravesó el pecho de Surfer con una hoja.",
            },
            {
                "src": TW[98],
                "text": "Sujetándolo con desprecio mientras le arrebataba la gloria, el Rey Thanos aplastó el rostro del Caído golpeándolo brutalmente contra su propio martillo.",
            },
            {
                "src": TW[100],
                "text": "Así cayó el último defensor digno del cosmos en brazos del tirano. ¿Merecía Silver Surfer vencer a Thanos con el poder absoluto de Thor?",
            },
        ],
    },
    {
        "slot": 12,
        "queue_folder": "012_fc_books_of_doom_mascara_ardiente",
        "id": "fc_12_books_of_doom_mascara_ardiente",
        "folder": "fc_12_books_of_doom_mascara_ardiente",
        "title": "Doctor Doom: ¡Se Puso la Máscara Al Rojo Vivo Directo en su Rostro Quemado! 🔥👑💀",
        "character": "Doctor Doom",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ DOOM SE SOLDÓ LA MÁSCARA ARDIENDO?",
        "thumb_text": "MÁSCARA AL ROJO VIVO",
        "thumb_scene_idx": 0,
        "description": "Books of Doom #4 (Ed Brubaker): La verdad oculta sobre el accidente que desfiguró a Victor Von Doom y cómo forjó su armadura en el Tíbet.",
        "hashtags": "#DoctorDoom #VictorVonDoom #MarvelComics #Latveria #Comics #Reels #Shorts",
        "scenes": [
            {
                "src": BOD4[10],
                "text": "Muchos creen que el orgullo de Victor Von Doom lo llevó a ocultarse tras una máscara de acero, pero la verdad detrás de su rostro es mucho más escalofriante.",
            },
            {
                "src": BOD4[3],
                "text": "Tras la explosión en su laboratorio universitario junto a Reed Richards, un joven Victor huyó humillado hasta las cumbres más heladas del Tíbet buscando magia ancestral.",
            },
            {
                "src": BOD4[4],
                "text": "Al borde de morir congelado entre la nieve y devorado por bestias, una orden secreta de monjes lo rescató jurando forjar para él una armadura legendaria.",
            },
            {
                "src": BOD4[14],
                "text": "Durante meses ocultó su rostro bajo vendajes sangrientos, culpando eternamente a Reed por la horrible cicatriz que le impedía volver a mirarse al espejo.",
            },
            {
                "src": BOD4[18],
                "text": "En la fragua sagrada del monasterio, los herreros fundieron el metal de su nueva máscara frente al fuego, advirtiéndole que debía esperar a que enfriara.",
            },
            {
                "src": BOD4[19],
                "text": "Pero consumido por la impaciencia y el odio, Victor les arrebató la máscara todavía al rojo vivo y ordenó presionarla directo sobre su carne viva.",
            },
            {
                "src": BOD4[20],
                "text": "Mientras el metal ardiente se fundía para siempre con su propia piel entre gritos infernales, murió el humano y nació Doctor Doom. ¿Temías su origen real?",
            },
        ],
    },
    {
        "slot": 13,
        "queue_folder": "013_fc_uncanny_xforce_ejecucion_apocalipsis",
        "id": "fc_13_uncanny_xforce_ejecucion_apocalipsis",
        "folder": "fc_13_uncanny_xforce_ejecucion_apocalipsis",
        "title": "Uncanny X-Force: ¡Fantomex Ejecutó de Un Disparo a un Niño Apocalipsis! 🔫🩸❌",
        "character": "Wolverine",
        "voice_mode": "referencia",
        "hook_card": "¿EL CRIMEN QUE ROMPIÓ PARA SIEMPRE A X-FORCE?",
        "thumb_text": "DISPARO A SANGRE FRÍA",
        "thumb_scene_idx": 0,
        "description": "Uncanny X-Force #4 (Rick Remender): El dilema moral más oscuro de Marvel cuando el escuadrón secreto encontró a Apocalipsis reencarnado en un niño.",
        "hashtags": "#UncannyXForce #Wolverine #Deadpool #Apocalipsis #XMen #MarvelComics #Reels",
        "scenes": [
            {
                "src": UXF[99],
                "text": "Cansados de que los enemigos mutantes regresaran una y otra vez, Wolverine formó en secreto a X-Force para ejecutar amenazas antes de que pudieran matar.",
            },
            {
                "src": UXF[86],
                "text": "Al infiltrarse en la nave lunar del clan Akkaba esperando enfrentar a un monstruo invencible, descubrieron una verdad paralizante: Apocalipsis había reencarnado en un niño.",
            },
            {
                "src": UXF[88],
                "text": "El pequeño En Sabah Nur ni siquiera recordaba su vida pasada de genocidios y suplicó asustado sin comprender por qué esos guerreros armados querían matarlo.",
            },
            {
                "src": UXF[89],
                "text": "Incluso Logan, el asesino más despiadado de los X-Men, guardó sus garras diciendo que ninguno de ellos podía convertirse en verdugo de un niño inocente.",
            },
            {
                "src": UXF[90],
                "text": "Psylocke juró proteger al muchacho para educarlo lejos de la oscuridad y demostrarle al universo que hasta el peor tirano podía cambiar su destino.",
            },
            {
                "src": UXF[92],
                "text": "De pronto, sin pedir permiso ni mostrar una sola duda, Fantomex levantó su pistola directo hacia la frente del niño mientras Deadpool gritaba desesperado.",
            },
            {
                "src": UXF[93],
                "text": "Un disparo seco rompió el silencio dejando el cuerpo pequeño tendido en un charco de sangre ante la mirada horrorizada de todo su propio equipo.",
            },
            {
                "src": UXF[94],
                "text": "Fantomex dijo que alguien debía cargar con ese pecado para salvar al mundo. Y tú, ¿habrías salvado al niño o apretado el gatillo?",
            },
        ],
    },
    {
        "slot": 14,
        "queue_folder": "014_fc_cry_for_justice_green_arrow_mata_prometheus",
        "id": "fc_14_cry_for_justice_green_arrow_mata_prometheus",
        "folder": "fc_14_cry_for_justice_green_arrow_mata_prometheus",
        "title": "Green Arrow: ¡Rompió su Regla y Atravesó Entre los Ojos a Prometheus! 🏹🩸⚖️",
        "character": "Green Arrow",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ FLECHA VERDE EJECUTÓ A SANGRE FRÍA?",
        "thumb_text": "SIN PIEDAD ENTRE LOS OJOS",
        "thumb_scene_idx": 0,
        "description": "Justice League: Cry For Justice #7 — Tras la destrucción de Star City y el asesinato de la hija de Roy Harper, Oliver Queen cruzó su límite.",
        "hashtags": "#GreenArrow #Prometheus #JusticeLeague #DCComics #Comics #Reels #Shorts",
        "scenes": [
            {
                "src": CFJ[173],
                "text": "Prometheus siempre se consideró la versión malvada de Batman, usando su genio táctico para humillar a los héroes más grandes de la Liga de la Justicia.",
            },
            {
                "src": CFJ[174],
                "text": "En el golpe maestro de su vida logró neutralizar a todo el equipo, cortándole brutalmente el brazo derecho a Arsenal en medio de su propia base secreta.",
            },
            {
                "src": CFJ[175],
                "text": "Pero su verdadera crueldad llegó cuando activó un artefacto de teletransportación masiva para destruir Star City, el hogar sagrado de Flecha Verde.",
            },
            {
                "src": CFJ[176],
                "text": "En segundos más de noventa mil civiles inocentes murieron aplastados entre los escombros, incluyendo a la pequeña hija de Roy Harper bajo las ruinas.",
            },
            {
                "src": CFJ[177],
                "text": "Con la ciudad hecha polvo, los héroes capturaron a Prometheus vivos en un pacto para que no detonara más bombas en otras ciudades del planeta.",
            },
            {
                "src": CFJ[178],
                "text": "Sin embargo, Oliver Queen se infiltró solo en la guarida del asesino en medio de la noche sin avisarle a Batman ni a la Liga de la Justicia.",
            },
            {
                "src": CFJ[179],
                "text": "Diciendo que la justicia legal nunca alcanzaría para ese monstruo, disparó una flecha directo entre sus ojos. ¿Hizo bien Oliver al ejecutarlo así?",
            },
        ],
    },
    {
        "slot": 15,
        "queue_folder": "015_fc_siege_4_muerte_loki_y_void",
        "id": "fc_15_siege_4_muerte_loki_y_void",
        "folder": "fc_15_siege_4_muerte_loki_y_void",
        "title": "Siege #4: ¡El Sacrificio de Loki y la Ejecución Final del Monstruo The Void! ⚡🐍🌑",
        "character": "Thor",
        "voice_mode": "referencia",
        "hook_card": "¿EL DÍA QUE LOKI SE SACRIFICÓ PARA SALVAR ASGARD?",
        "thumb_text": "EL FIN DE THE VOID",
        "thumb_scene_idx": 0,
        "description": "Siege #4 (Brian Michael Bendis): Cuando The Void destruyó Asgard y Loki dio su vida arrepentido para darle a los Vengadores su última oportunidad.",
        "hashtags": "#Thor #Loki #Sentry #TheVoid #Avengers #MarvelComics #Comics #Reels",
        "scenes": [
            {
                "src": SIEGE[55],
                "text": "Con Asgard reducida a escombros humeantes, los Vengadores originales se unieron por última vez frente a la peor entidad oscura de Marvel: el Vacío.",
            },
            {
                "src": SIEGE[59],
                "text": "Tras derrumbar toda la ciudad dorada de los dioses, el cuerpo de Robert Reynolds desapareció por completo dejando paso a una pesadilla lovecraftiana imparable.",
            },
            {
                "src": SIEGE[61],
                "text": "Al comprender que su engaño había provocado la destrucción de su propio hogar, Loki entregó las Piedras Norn mágicas para fortalecer a los héroes.",
            },
            {
                "src": SIEGE[62],
                "text": "Pagando el precio máximo por su traición, el dios de las mentiras fue desgarrado en pedazos frente a su hermano Thor mientras le pedía perdón al morir.",
            },
            {
                "src": SIEGE[64],
                "text": "Cegado por la furia y el dolor, el Dios del Trueno descargó cada relámpago de Mjolnir contra la sombra gigante en una batalla apocalíptica.",
            },
            {
                "src": SIEGE[67],
                "text": "Aprovechando la distracción, Tony Stark hackeó todo el Helicarrier flotante de SHIELD estrellándolo como una bala gigante directo sobre el monstruo.",
            },
            {
                "src": SIEGE[70],
                "text": "Atrapado entre la agonía, el propio Robert suplicó a gritos que lo mataran antes de que la oscuridad volviera a devorar la Tierra entera.",
            },
            {
                "src": SIEGE[72],
                "text": "Con un golpe definitivo de relámpagos, Thor puso fin al Sentry arrojando sus restos al corazón del sol. ¿Te conmovió el sacrificio final de Loki?",
            },
        ],
    },
    {
        "slot": 16,
        "queue_folder": "016_fc_ultimatum_magneto_destruye_wolverine",
        "id": "fc_16_ultimatum_magneto_destruye_wolverine",
        "folder": "fc_16_ultimatum_magneto_destruye_wolverine",
        "title": "Ultimatum: ¡Magneto Desintegró a Wolverine Hasta Dejar Solo Sus Huesos! 💀⚡🩸",
        "character": "Wolverine",
        "voice_mode": "zazoom",
        "hook_card": "¿CÓMO MAGNETO MATÓ A WOLVERINE PARA SIEMPRE?",
        "thumb_text": "ESQUELETO SIN CARNE",
        "thumb_scene_idx": 0,
        "description": "Ultimatum #5 (Jeph Loeb & David Finch): La ejecución más extrema de Magneto cuando arrancó todo el adamantium y pulverizó a Logan.",
        "hashtags": "#Wolverine #Magneto #Ultimatum #XMen #MarvelComics #Comics #Reels #Shorts",
        "scenes": [
            {
                "src": ULT[90],
                "text": "Después de perder a sus hijos Quicksilver y Scarlet Witch, Magneto enloqueció declarando el exterminio total de la raza humana y de cualquier héroe en su camino.",
            },
            {
                "src": ULT[10],
                "text": "Invirtiendo los polos magnéticos de la Tierra, levantó una ola gigantesca sobre Manhattan que ahogó a millones de personas y decenas de héroes al instante.",
            },
            {
                "src": ULT[91],
                "text": "Sobrevivientes desesperados encabezados por Wolverine asaltaron la ciudadela flotante de Magneto dispuestos a matarlo antes de que destruyera el resto del mundo.",
            },
            {
                "src": ULT[92],
                "text": "Logan logró clavar sus garras en el pecho del amo del magnetismo, pero cometió el error fatal de pelear con metal contra un dios magnético furioso.",
            },
            {
                "src": ULT[93],
                "text": "Magneto controló al instante los rayos de Iron Man y de Cyclops para disparárselos a quemarropa a Logan, destrozando por completo su factor curativo.",
            },
            {
                "src": ULT[94],
                "text": "Sin piedad alguna, arrancó todo el adamantium de sus huesos y pulverizó hasta la última célula de su cuerpo dejando solo una lluvia de cenizas.",
            },
            {
                "src": ULT[95],
                "text": "Los X-Men quedaron paralizados observando lo único que quedó del mutante más resistente: su brazo y cráneo calcinados sobre el suelo frío.",
            },
            {
                "src": ULT[106],
                "text": "Cegado por la venganza, Cyclops se acercó al villano y le voló la cabeza de un rayo óptico letal. ¿Fue esta la muerte más brutal de Wolverine?",
            },
        ],
    },
    {
        "slot": 17,
        "queue_folder": "017_fc_xmen_schism_duelo_wolverine_cyclops",
        "id": "fc_17_xmen_schism_duelo_wolverine_cyclops",
        "folder": "fc_17_xmen_schism_duelo_wolverine_cyclops",
        "title": "X-Men Schism: ¡La Pelea a Muerte Entre Wolverine y Cyclops Que Partió al Equipo! ⚔️❌🔥",
        "character": "Wolverine",
        "voice_mode": "referencia",
        "hook_card": "¿POR QUÉ WOLVERINE Y CYCLOPS SE MATARON A GOLPES?",
        "thumb_text": "X-MEN DIVIDIDOS EN DOS",
        "thumb_scene_idx": 0,
        "description": "X-Men: Schism #4–5 (Jason Aaron): El choque filosófico y sangriento entre Scott Summers y Logan mientras un Centinela gigante caía sobre Utopía.",
        "hashtags": "#Wolverine #Cyclops #XMen #Schism #MarvelComics #Comics #Reels #Shorts",
        "scenes": [
            {
                "src": SCH[166],
                "text": "Durante años pelearon hombro a hombro, pero la guerra por el futuro de los mutantes convirtió a Wolverine y a Cyclops en enemigos irreconciliables.",
            },
            {
                "src": SCH[99],
                "text": "Cuando un Centinela gigante marchó para aplastar la isla de Utopía, Scott ordenó enviar a los niños mutantes al frente como soldados desesperados.",
            },
            {
                "src": SCH[102],
                "text": "Furioso al negarse a sacrificar más inocentes, Logan activó el detonador para volar la isla, provocando que Cyclops lo derribara de un rayo óptico.",
            },
            {
                "src": SCH[103],
                "text": "Ya harto de contenerse, Wolverine saltó sobre su líder clavando sus garras en la arena mientras ambos se insultaban recordando todas sus viejas heridas.",
            },
            {
                "src": SCH[105],
                "text": "Scott se arrancó el visor desatando el máximo poder de su rayo carmesí directo contra el pecho de Logan, quemando su traje y carne hasta los huesos.",
            },
            {
                "src": SCH[108],
                "text": "Aun sangrando y sin aliento, Wolverine soportó la ráfaga mortal y le reventó el rostro a golpes a Cyclops mientras el robot colosal caía encima.",
            },
            {
                "src": SCH[112],
                "text": "Tras aplastar juntos al Centinela con sus últimas fuerzas, ambos comprendieron que su hermandad había muerto y ya nunca podrían volver a confiar.",
            },
            {
                "src": SCH[134],
                "text": "La mitad del equipo eligió volver a la escuela con Logan dejando atrás la guerra de Scott. Y tú, ¿de qué lado estabas: Team Logan o Team Cyclops?",
            },
        ],
    },
    {
        "slot": 18,
        "queue_folder": "018_fc_thanos_wins_rey_thanos_vs_joven",
        "id": "fc_18_thanos_wins_rey_thanos_vs_joven",
        "folder": "fc_18_thanos_wins_rey_thanos_vs_joven",
        "title": "Thanos Wins: ¡Rey Thanos Peleó Contra Su Yo del Pasado y Suplicó Morir! 👑💀⏳",
        "character": "Thanos",
        "voice_mode": "zazoom",
        "hook_card": "¿POR QUÉ REY THANOS SE ENFRENTÓ A SÍ MISMO?",
        "thumb_text": "SUPLICÓ POR SU MUERTE",
        "thumb_scene_idx": 0,
        "description": "Thanos #18 (Donny Cates): El retorcido final donde el Rey Thanos conquistó todo el universo solo para descubrir que la Muerte aún exigía un sacrificio.",
        "hashtags": "#Thanos #ThanosWins #MarvelComics #Muerte #ComicsEnEspanol #Reels #Shorts",
        "scenes": [
            {
                "src": TW[124],
                "text": "Al final de los tiempos, un anciano Rey Thanos logró lo imposible: asesinó a cada héroe, dios y entidad cósmica sentándose sobre un trono de cráneos.",
            },
            {
                "src": TW[104],
                "text": "Sin embargo, la Dama Muerte aún se negaba a besarlo porque faltaba alguien vivo en el cosmos: el único guerrero capaz de matarlo, el propio Thanos.",
            },
            {
                "src": TW[106],
                "text": "Usando la gema del tiempo trajo al joven Thanos de nuestra era al futuro, revelándole que todo su reino glorioso necesitaba una última batalla mortal.",
            },
            {
                "src": TW[111],
                "text": "Al oír que su versión anciana deseaba entregar su propia vida por amor a la Muerte, el joven Thanos se sintió asqueado por su debilidad.",
            },
            {
                "src": TW[117],
                "text": "Ambos titanes desataron un combate salvaje haciendo temblar las ruinas muertas del universo mientras se destrozaban a golpes sin piedad alguna.",
            },
            {
                "src": TW[118],
                "text": "El joven Thanos superó finalmente en brutalidad al anciano, moliendo su rostro a puñetazos sobre las piedras manchadas de sangre cósmica.",
            },
            {
                "src": TW[120],
                "text": "Con la mandíbula rota y sonriendo feliz, el Rey Thanos le suplicó a su versión joven que terminara el golpe para abrazar por fin a la Muerte.",
            },
            {
                "src": TW[122],
                "text": "Pero el joven Thanos se negó humillándolo y volvió al pasado jurando jamás volverse patético. ¿Cuál de los dos Thanos te pareció más despiadado?",
            },
        ],
    },
    {
        "slot": 19,
        "queue_folder": "019_fc_marvel_ruins_universo_maldito",
        "id": "fc_19_marvel_ruins_universo_maldito",
        "folder": "fc_19_marvel_ruins_universo_maldito",
        "title": "Marvel Ruins: ¡El Universo Más Perturbador Donde Todo Salió Horriblemente Mal! ☢️💀🕷️",
        "character": "Marvel",
        "voice_mode": "referencia",
        "hook_card": "¿QUÉ PASÓ EN EL UNIVERSO MARVEL MÁS MALDITO?",
        "thumb_text": "DIOS MUERTO EN EL ESPACIO",
        "thumb_scene_idx": 0,
        "description": "Ruins #1 (Warren Ellis): La realidad más oscura y realista donde la radiación gamma no dio poderes, sino cáncer mortal y horror absoluto.",
        "hashtags": "#MarvelRuins #MarvelComics #Terror #SpiderMan #Wolverine #Comics #Reels",
        "scenes": [
            {
                "src": RUINS[0],
                "text": "En nuestro universo un accidente radiactivo crea héroes maravillosos. Pero en la realidad de Marvel Ruins, todo lo que podía salir mal salió terriblemente mal.",
            },
            {
                "src": RUINS[5],
                "text": "Aquí los Vengadores nunca defendieron la Tierra; se convirtieron en rebeldes derrotados y fusilados en masa bajo la dictadura del presidente Charles Xavier.",
            },
            {
                "src": RUINS[6],
                "text": "Bruce Banner jamás se transformó en el poderoso Hulk. La bomba gamma lo convirtió en una masa deforme de tumores gigantes agonizando dentro de un laboratorio.",
            },
            {
                "src": RUINS[7],
                "text": "Wolverine tampoco tuvo un factor curativo mágico: su propio esqueleto de metal le provocó envenenamiento lento mientras perdía lentamente la razón en un bar.",
            },
            {
                "src": RUINS[9],
                "text": "Los mutantes fueron encerrados en campos de exterminio en medio del desierto, siendo torturados y mutilados para experimentar con sus mutaciones fallidas.",
            },
            {
                "src": RUINS[12],
                "text": "Al quedar atrapados sin aire en su cohete espacial, Reed Richards y los Cuatro Fantásticos ardieron y murieron de formas atroces antes de regresar.",
            },
            {
                "src": RUINS[13],
                "text": "Hasta Silver Surfer enloqueció por la falta de oxígeno en el vacío cósmico, desgarrándose su propio pecho con sus manos intentando respirar.",
            },
            {
                "src": RUINS[23],
                "text": "Incluso encontraron en Marte el cadáver congelado de un dios olvidado. ¿Crees que este es el cómic más perturbador que Marvel publicó jamás?",
            },
        ],
    },
    {
        "slot": 20,
        "queue_folder": "020_fc_daredevil_nuevo_rey_hells_kitchen",
        "id": "fc_20_daredevil_nuevo_rey_hells_kitchen",
        "folder": "fc_20_daredevil_nuevo_rey_hells_kitchen",
        "title": "Daredevil #50: ¡Masacró a Kingpin y Se Coronó Nuevo Rey de Hell's Kitchen! 😈👑🩸",
        "character": "Daredevil",
        "voice_mode": "zazoom",
        "hook_card": "¿EL DÍA QUE DAREDEVIL SE CONVIRTIÓ EN KINGPIN?",
        "thumb_text": "EL NUEVO KINGPIN",
        "thumb_scene_idx": 0,
        "description": "Daredevil Vol. 2 #50 (Brian Michael Bendis): Harto de ver volver a Wilson Fisk tras rejas, Matt Murdock lo destruyó y tomó el control total del crimen.",
        "hashtags": "#Daredevil #Kingpin #HellsKitchen #MarvelComics #MattMurdock #Comics #Reels",
        "scenes": [
            {
                "src": DD50 / "dd50_cover.jpg",
                "text": "Durante años Matt Murdock creyó en la ley de Nueva York, hasta que comprendió que mientras Wilson Fisk siguiera respirando, jamás habría paz en Hell's Kitchen.",
            },
            {
                "src": DD50 / "daredevil11.jpg",
                "text": "Tras sufrir atentados contra su vida y ver revelada su identidad secreta en los periódicos, el abogado ciego perdió por completo su paciencia.",
            },
            {
                "src": DD50 / "daredevil12.jpg",
                "text": "Cuando Kingpin regresó triunfante al barrio seguro de recuperar su imperio criminal, ordenó eliminar a cualquiera que desafiara su vieja corona.",
            },
            {
                "src": DD50 / "daredevil13.jpg",
                "text": "Pero esta vez no enfrentó a un vigilante buscando arrestarlo. Daredevil irrumpió furioso en el club frente a todos los jefes de la mafia.",
            },
            {
                "src": DD50 / "daredevil14.jpg",
                "text": "Ignorando las balas y los guardaespaldas, masacró a la escolta entera con violencia brutal hasta quedar cara a cara frente al mismo Kingpin.",
            },
            {
                "src": DD50 / "daredevil15.jpg",
                "text": "Con una lluvia incesante de golpes implacables que quebraron sus huesos, Matt humilló al tirano dejándolo destrozado y suplicando sobre el suelo.",
            },
            {
                "src": DD50 / "daredevil16.jpg",
                "text": "Luego agarró el cadáver de hierro del poder criminal frente a los capos temblorosos y proclamó una nueva ley bajo su puño definitivo.",
            },
            {
                "src": DD50 / "scene_04.jpg",
                "text": "Desde esa noche Matt se declaró el nuevo Kingpin del barrio para imponer paz con miedo. ¿Crees que Daredevil actuó como héroe o villano?",
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
    print(f"🎬 [LOTE 2 FILMCRAFT - VIDEO {slot}/20] {q_folder}", flush=True)
    print(f"   Título: {proj['title']}", flush=True)
    print(f"=======================================================", flush=True)

    curated_dir = CURATED_BASE / proj["folder"]
    curated_dir.mkdir(parents=True, exist_ok=True)
    work_dir = PROJECT_ROOT / "work" / f"filmcraft_lote2_slot_{slot:02d}"
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
        seq_name=f"Lote2_Slot_{slot:02d}",
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
    # Pre-verify every source panel exists before starting rendering!
    for proj in LOTE_02_PROJECTS:
        for i, sc in enumerate(proj["scenes"], start=1):
            p = Path(sc["src"])
            if not p.exists():
                raise FileNotFoundError(f"Missing asset for Slot {proj['slot']} scene {i}: {p}")
    print(f"✓ Verificadas las rutas de todas las viñetas de los {len(LOTE_02_PROJECTS)} videos del Lote 2.", flush=True)

    start_all = time.time()
    SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
    summary = []

    for proj in LOTE_02_PROJECTS:
        try:
            dur, sz, st = produce_project(proj)
            summary.append((proj["slot"], proj["queue_folder"], dur, sz, st))
        except Exception as e:
            print(f"❌ ERROR en Slot {proj['slot']}: {e}", flush=True)
            summary.append((proj["slot"], proj["queue_folder"], 0.0, 0.0, f"ERROR: {e}"))

    elapsed_min = (time.time() - start_all) / 60.0
    print("\n" + "=" * 78, flush=True)
    print(f"AUDITORÍA FINAL - LOTE 2 FILMCRAFT 75s ({elapsed_min:.1f} min)", flush=True)
    print("=" * 78, flush=True)
    for slot, qf, dur, sz, st in summary:
        print(f"Slot {slot:02d} | {dur:6.2f}s | {sz:6.1f} MB | {st:<10} | {qf}", flush=True)
    print("=" * 78, flush=True)


if __name__ == "__main__":
    main()
