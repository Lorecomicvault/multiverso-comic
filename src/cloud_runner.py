"""
Multiverso Comic - Autonomous Cloud Video Runner & Publisher (Spanish Engine)
Ironclad 5-Layer Anti-Duplication Engine: Guarantees ZERO repeated stories, character arcs, or themes.
Repository: multiverso-comic (main)
"""

import argparse
import io
import json
import os
import random
import re
import sys
import time
import unicodedata
from pathlib import Path
from PIL import Image, ImageFilter
import requests

from .comic_fetcher import get_fandom_comic_art
from .publisher import publish_comic_video, DEFAULT_PAGE_ID, DEFAULT_IG_USER_ID

LEDGER_PATH = Path("published_ledger.json")


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

EDITORIAL_STORIES = [
    {
        "id": "superior_spider_man_otto",
        "character": "Superior Spider-Man",
        "title": "Superior Spider-Man: La Mente de Otto Octavius en Peter Parker",
        "theme_signature": "spider_man:superior:otto_octavius_mente",
        "description": "Al borde de la muerte, el Doctor Octopus intercambió su mente con Peter Parker. Atrapado en el cuerpo de Spider-Man, Otto juró ser un héroe superior a su despiadado modo.",
        "hashtags": "#SuperiorSpiderMan #SpiderMan #DoctorOctopus #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Con su cuerpo consumido por el cáncer y al borde de la muerte, Otto Octavius logró la jugada maestra definitiva: transferir su conciencia al cuerpo de Peter Parker.",
            "Peter murió atrapado en el cuerpo decrépito de Octavius, pero en su último aliento le transmitió a Otto la aplastante carga de que un gran poder conlleva una gran responsabilidad.",
            "Conmovido pero impulsado por su soberbia colosal, Otto juró no solo continuar el legado arácnido, sino convertirse en un Spider-Man infinitamente superior.",
            "Diseñó una armadura mejorada con patas mecánicas retráctiles, desplegó miles de Spider-Bots de vigilancia por toda Nueva York y ejecutó criminales sin pestañear.",
            "Fundó Industrias Parker y obtuvo un doctorado, pero su arrogancia provocó que el Duende Verde creara un imperio subterráneo que arrasó la ciudad.",
            "Al darse cuenta de que solo el verdadero Peter podía salvar al amor de su vida, Otto borró voluntariamente su propia mente, devolviéndole el manto al único Spider-Man."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/3/36/Superior_Spider-Man_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/c2/Superior_Spider-Man_Vol_1_9.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/9/9d/Superior_Spider-Man_Midtown_Comics_Variant.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/3/36/Superior_Spider-Man_Vol_1_1_Ramos_Variant_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/d6/Superior_Spider-Man_London_Super_Comic_Convention_Variant.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/9/92/Superior_Spider-Man_Vol_1_1_Textless.png"
        ]
    },
    {
        "id": "deadpool_kills_marvel_universe",
        "character": "Deadpool",
        "title": "Deadpool Masacra el Universo Marvel: La Masacre Multiversal",
        "theme_signature": "deadpool:kills_marvel:rompiendo_cuarta_pared",
        "description": "Tras una sesión psiquiátrica que desbloquea la verdad existencial del cómic, Deadpool comprende que todos son títeres de los guionistas y decide matarlos a todos para liberarlos.",
        "hashtags": "#Deadpool #MarvelComics #DeadpoolKills #ComicsNarrados #Reels",
        "scenes": [
            "Llevado a un manicomio por los X-Men, Wade Wilson cayó en manos de Psycho-Man, cuyo tratamiento rompió la última barrera de cordura en su cerebro.",
            "Una voz siniestra se apoderó de Deadpool, revelándole la verdad más aterradora: todos los héroes y villanos solo existen como marionetas para el entretenimiento del lector.",
            "Convencido de que la única forma de liberar a sus amigos del sufrimiento eterno de los cómics era la muerte, Wade inició una masacre sistemática y despiadada.",
            "Incineró a los Cuatro Fantásticos con bombas de partículas, decapitó a Thor agrandando el Mjolnir con partículas Pym y ejecutó a Hulk cuando volvió a ser Banner.",
            "Ni siquiera Spider-Man pudo escapar de su mira, siendo ejecutado a quemarropa en pleno salto acrobático ante la mirada horrorizada de Nueva York.",
            "Tras cruzar portales interdimensionales y llegar a la mesa de los creadores de Marvel, Deadpool miró fijamente al lector y le advirtió que él sería el siguiente."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/1/19/Deadpool_Kills_the_Marvel_Universe_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/9/90/Deadpool_Kills_the_Marvel_Universe_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/1/12/Deadpool_Kills_the_Marvel_Universe_Vol_1_2_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/e/e2/Deadpool_Kills_the_Marvel_Universe_Vol_1_3.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/f/fc/Deadpool_Kills_the_Marvel_Universe_Vol_1_3_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/6/6c/Deadpool_Kills_the_Marvel_Universe_Vol_1_4.jpg"
        ]
    },
    {
        "id": "batman_hush_silencio",
        "character": "Batman",
        "title": "Batman: Silencio (Hush) - La Venganza de Thomas Elliot",
        "theme_signature": "batman:hush:thomas_elliot_conspiracion",
        "description": "Un misterioso villano vendado llamado Hush manipula a toda la galería de villanos de Gotham para quebrar física y mentalmente al Caballero de la Noche.",
        "hashtags": "#Batman #Hush #Silencio #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Desde las sombras de Gotham emergió un cerebro criminal con el rostro cubierto de vendas que conocía cada secreto y vulnerabilidad de Bruce Wayne: Hush.",
            "Orquestó una sinfonía de caos implacable, manipulando con precisión quirúrgica a Poison Ivy, Killer Croc y al mismísimo Joker para llevar a Batman al colapso.",
            "Utilizó esporas de control mental para poner a Superman en contra del Hombre Murciélago, forzando a Bruce a usar un anillo de kriptonita en un brutal choque callejero.",
            "La investigación reveló la más amarga de las traiciones: tras los vendajes se ocultaba el doctor Thomas Elliot, el mejor amigo de la infancia de Bruce.",
            "Consumido por la envidia infantil hacia la fortuna Wayne tras el fracaso en el asesinato de sus propios padres, Elliot dedicó su vida a perfeccionar su venganza.",
            "Con el apoyo de Catwoman y tras salvar a Gotham de un abismo de mentiras, Batman comprendió que sus peores fantasmas siempre provienen de su pasado."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/4/41/Batman_608.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/4/42/Batman_006.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/a/a1/Batman_012.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/f/f4/Batman_0405.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/6/68/Batman_Villains_0001.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/0/0a/Batman_Vol_1_619.jpg"
        ]
    },
    {
        "id": "sinestro_corps_war",
        "character": "Sinestro",
        "title": "La Guerra de los Sinestro Corps: El Terror Amarillo Conquista el Cosmos",
        "theme_signature": "green_lantern:sinestro_corps:guerra_miedo",
        "description": "Thaal Sinestro forja un ejército armado con la luz amarilla del miedo para derrocar a los Guardianes del Universo y sumergir el cosmos en una tiranía militar.",
        "hashtags": "#GreenLantern #Sinestro #SinestroCorps #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Exiliado al universo de antimateria de Qward, Thaal Sinestro dominó la entidad cósmica Parallax y forjó miles de anillos amarillos impulsados por el miedo puro.",
            "Reclutó a los monstruos más sádicos de la creación, como Arkillo y el temible Cyborg Superman, declarando la guerra total contra el Cuerpo de Green Lanterns.",
            "El asalto inicial fue devastador: los Sinestro Corps sitiaron el planeta Oa y masacraron a cientos de linternas, superando su voluntad con puro terror psicológico.",
            "Los Guardianes del Universo, acorralados, tomaron una decisión sin precedentes: reescribieron el Libro de Oa y autorizaron el uso de fuerza letal.",
            "La batalla decisiva estalló en los cielos de la Tierra, donde Hal Jordan y Kyle Rayner lideraron una contraofensiva desesperada contra el Antimonitor y Superboy Prime.",
            "En un duelo mano a mano sin anillos, Hal Jordan noqueó a Sinestro, demostrando que la voluntad inquebrantable siempre vencerá al miedo en la oscuridad."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/7/79/Sinestro_Corps_War.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/31/Green_Lanterns_vs_Sinestro_Corps_01.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/f/fb/Green_Lantern_Vol_4_25_Variant_Textless.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/1/11/Anti-Monitor_0011.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/5c/Anti-Monitor_boom.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/0/0a/War_of_Light.JPG"
        ]
    },

    {
        "id": "hulk_maestro_futuro_imperfecto",
        "character": "Hulk",
        "title": "Hulk Maestro: El Tirano del Futuro Imperfecto",
        "theme_signature": "hulk:future_imperfect:maestro_distopia",
        "description": "La historia épica de Hulk Maestro en Futuro Imperfecto: la caída de los héroes, la tétrica sala de trofeos de Rick Jones, la sangrienta guerra contra su versión del pasado y su condena final en la detonación de la Bomba Gamma.",
        "hashtags": "#Hulk #Maestro #MarvelComics #FuturoImperfecto #ComicsNarrados #Reels",
        "scenes": [
            "En un futuro postapocalíptico desolado, una devastadora guerra nuclear aniquiló al noventa y cinco por ciento de la humanidad y barrió con casi todos los superhéroes de la Tierra.",
            "Sobre las ruinas humeantes de la civilización se erigió la temible ciudadela de Distopía, patrullada por los letales Perros de Guerra y sometida a una tiranía militar absoluta.",
            "Mientras los demás héroes sucumbían ante el veneno atómico, Bruce Banner absorbió la radiación durante décadas, multiplicando su fuerza monstruosamente y conservando su genial intelecto.",
            "Despojándose de su moral y adoptando el nombre de Maestro, exterminó a sangre fría a todos los señores de la guerra rivales para autoproclamarse emperador supremo del planeta.",
            "En las profundidades de un búnker secreto, un anciano Rick Jones custodiaba la tétrica sala de trofeos donde yacían el escudo roto del Capitán América, el martillo de Thor y el cráneo de Wolverine.",
            "Desesperada por frenar esta pesadilla, la resistencia rebelde liderada por Janis Jones utilizó la máquina del tiempo del Doctor Doom para viajar al pasado en busca de auxilio.",
            "Trajeron al joven profesor Hulk desde el siglo veinte, enfrentándolo cara a cara contra la corrupta y despiadada abominación en la que el destino lo terminaría convirtiendo.",
            "El choque entre ambos titanes fue brutal e implacable; Maestro contaba con un siglo entero de experiencia en batalla y no dudó en quebrarle el cuello a su versión más joven.",
            "Aprovechando la soberbia del tirano, Hulk fingió su agonía y activó la plataforma temporal a sus espaldas, programando como destino las coordenadas exactas de su propio nacimiento.",
            "Maestro fue enviado al epicentro mismo donde detonó la Bomba Gamma original en Nuevo México, siendo desintegrado por la explosión nuclear que dio vida al monstruo."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/b/b1/Hulk_Future_Imperfect_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/a/a0/Dogs_of_War_%28Earth-9200%29_from_Hulk_Future_Imperfect_Vol_1_1_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/a/ab/Bruce_Banner_%28Earth-9200%29_from_Hulk_Future_Imperfect_Vol_1_1_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/8/87/Maestro_Vol_1_1_McGuinness_Variant_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/7/70/Richard_Jones_%28Earth-9200%29_from_Hulk_Future_Imperfect_Vol_1_2_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/f/ff/Bruce_Banner_%28Earth-616%29_from_Hulk_Future_Imperfect_Vol_1_1_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/db/Hulk_Future_Imperfect_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/5/5f/Bruce_Banner_%28Earth-9200%29_from_Hulk_Future_Imperfect_Vol_1_2_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/dd/Maestro_War_and_Pax_Vol_1_1_Stegman_Variant_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/a/aa/Maestro_Future_Imperfect_-_Marvel_Tales_Vol_1_1_Virgin_Variant.jpg"
        ]
    },
    {
        "id": "wolverine_old_man_logan",
        "character": "Wolverine",
        "title": "Wolverine: Old Man Logan - La Masacre de los X-Men",
        "theme_signature": "wolverine:old_man_logan:xmen_massacre",
        "description": "El trágico flashback donde la retorcida ilusión de Mysterio engaña a Wolverine para masacrar a sus propios y amados X-Men.",
        "hashtags": "#Wolverine #OldManLogan #XMen #Mysterio #MarvelComics #ComicLoreVault #ComicTok #Reels",
        "scenes": [
            "Cincuenta años después de que los supervillanos conquistaran el mundo, un anciano Logan vive como granjero pacifista en el páramo, negándose a sacar sus garras de adamantium.",
            "Esa oscura renuncia se remonta a una trágica noche en la Mansión Xavier, cuando las alarmas sonaron cuando cuarenta villanos irrumpieron repentinamente por las puertas.",
            "Creyendo que los estudiantes estaban en peligro mortal, Wolverine entró en una furia berserker ciega, destrozando a los intrusos habitación por habitación.",
            "Al degollar al último atacante, el humo se disipó cuando la niebla verde se desvaneció: Mysterio apareció carcajeándose, revelando que había nublado los sentidos de Logan.",
            "Horrorizado, Logan miró a su alrededor para descubrir la desgarradora verdad: no había villanos. En la lluvia yacían los cadáveres destrozados de sus amados X-Men.",
            "Roto sin remedio, Logan vagó por el desierto y colocó su cabeza sobre las vías del tren, pero su factor de curación se negó a dejarlo morir."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/a/a6/Wolverine_Vol_3_66_Wraparound_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/7/7f/Peter_Petruski_%28Earth-807128%29%2C_Norman_Osborn_%28Earth-807128%29%2C_James_Howlett_%28Earth-807128%29%2C_and_Kenuichio_Harada_%28Earth-807128%29_from_Wolverine_Vol_3_70_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/3/3a/Wolverine_Vol_3_70.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/cd/Jubilation_Lee_%28Earth-807128%29_and_James_Howlett_%28Earth-807128%29_from_Wolverine_Vol_3_70_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/b/b5/X-Men_%28Earth-807128%29_from_Wolverine_Vol_3_70_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/5/57/James_Howlett_%28Earth-807128%29_from_Wolverine_Vol_3_72_002.jpg"
        ]
    },
    {
        "id": "knull_el_dios_de_los_simbiontes",
        "character": "Knull",
        "title": "Knull El Dios de los Simbiontes",
        "theme_signature": "knull:simbiontes:rey_negro_invasion",
        "description": "Historia épica completa de cómic: Knull El Dios de los Simbiontes. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Knull #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "Antes de que existiera la luz, las estrellas o el propio Big Bang, solo existía la oscuridad absoluta, y en el centro de ese abismo reinaba un ser: Knull, el Dios de los Simbiontes.",
            "Cuando los Celestiales trajeron la luz al cosmos, Knull se sintió ultrajado: de su propia sombra forjó la legendaria Necroespada All-Black y decapitó a un dios Celestial de un solo tajo.",
            "Utilizando la cabeza del dios muerto como forja, Knull creó a la raza simbionte entera como una mente colmena viviente diseñada exclusivamente para devorar civilizaciones enteras.",
            "Millones de años después, Knull despertó de su prisión planetaria y marchó hacia la Tierra liderando un ejército incontable de dragones simbiontes que bloquearon el Sol por completo.",
            "Los Vengadores enviaron a su héroe más poderoso, Sentry, pero Knull lo agarró en el aire y lo partió por la mitad con sus manos desnudas, demostrando que ningún mortal podía dañarlo.",
            "Incluso le arrancó el simbionte a Eddie Brock lanzándolo al vacío desde lo alto de un rascacielos, sumiendo a los héroes de Marvel en su momento de mayor desesperación.",
            "Solo cuando la Fuerza Enigma eligió a Eddie Brock como el Dios de la Luz, armado con un hacha de energía pura, la humanidad tuvo una oportunidad de contraatacar.",
            "Eddie arrastró a Knull hasta el centro del Sol para incinerarlo, poniendo fin a la era del vacío y coronándose como el nuevo Rey de Negro del multiverso."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/6/64/King_in_Black_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/4/49/Venom_Vol_4_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/b/be/King_in_Black_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/2/22/King_in_Black_Vol_1_3.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/4/4b/King_in_Black_Vol_1_4.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/c5/Venom_Vol_4_2.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/0/0c/Edward_Brock_%28Earth-616%29_and_Venom_%28Symbiote%29_%28Earth-616%29_from_King_in_Black_Vol_1_5_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/7/73/Venom_Vol_4_3.jpg"
        ]
    },
    {
        "id": "superboy_prime_el_destructor_de_la_realidad",
        "character": "Superboy Prime",
        "title": "Superboy Prime El Destructor de la Realidad",
        "theme_signature": "superboy_prime:crisis_infinita:golpe_realidad",
        "description": "Historia épica completa de cómic: Superboy Prime El Destructor de la Realidad. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#SuperboyPrime #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué pasa si un fanático de los cómics de nuestro mundo real obtiene todos los poderes de Superman y enloquece? Este es Superboy Prime, el villano más temido de DC Cómics.",
            "Nacido en Tierra Prima, donde los superhéroes solo existían en historietas, descubrió sus poderes justo antes de que el Anti-Monitor destruyera su universo entero.",
            "Atrapado en una dimensión paraíso, su frustración fue tan colosal que comenzó a golpear las paredes del espacio-tiempo, alterando la historia y resucitando a Jason Todd.",
            "Al escapar a Nueva Tierra, enfrentó a los Jóvenes Titanes; creyendo que todo era un juego, desmembró a Pantha y masacró a docenas de héroes sin mostrar remordimiento.",
            "Cuando el Cuerpo de Green Lanterns intentó contenerlo, Superboy Prime asesinó a treinta y dos linternas con sus puños antes de ser arrojado al centro de un sol rojo.",
            "A diferencia de otros kryptonianos, Prime era totalmente inmune a la magia y a la kryptonita común, convirtiéndose en una fuerza imparable para la Liga de la Justicia.",
            "Se necesitaron dos Supermanes volando a través de los restos del planeta Krypton para debilitarlo lo suficiente y poder encerrarlo en un campo de fuerza eterno.",
            "Años más tarde, se sacrificó derrotando a The Darkest Knight para salvar el multiverso, probando que incluso el monstruo más desquiciado guardaba el corazón de un héroe."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/5/52/Infinite_Crisis_001.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/b/bc/Tales_from_the_Dark_Multiverse_Infinite_Crisis_Vol_1_1_Textless.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/2/20/Battle_of_the_Supermen.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/6/61/Battle_of_Metropolis_00.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/d/d1/Final_Crisis_Legion_of_Three_Worlds_1.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/f/f3/Adventure_Comics_Vol_2_4_Textless.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/59/Final_Crisis_Legion_of_Three_Worlds_Vol_1_5_Variant.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/4/41/Adventure_Comics_Vol_2_5_Textless.jpg"
        ]
    },
    {
        "id": "flashpoint_la_paradoja_que_destruyo_el_mundo",
        "character": "The Flash",
        "title": "Flashpoint La Paradoja del Tiempo",
        "theme_signature": "flash:flashpoint:paradoja_thomas_wayne",
        "description": "Historia épica completa de cómic: Flashpoint La Paradoja del Tiempo. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#TheFlash #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué pasa cuando el hombre más rápido del mundo comete un error egoísta y destruye la línea temporal? Esta es la pesadilla apocalíptica de Flashpoint.",
            "Barry Allen despertó en un mundo donde su madre estaba viva, pero la Liga de la Justicia jamás existió y él no tenía ningún rastro de su súper velocidad.",
            "Al buscar a Batman en la Baticueva, descubrió la brutal verdad: quien murió en el callejón fue Bruce Wayne, y el Batman de este mundo era su padre Thomas, un asesino sin piedad.",
            "Y la tragedia no terminaba ahí: enloquecida por la muerte de su hijo, Martha Wayne se cortó la boca para convertirse en el Joker más desgarrador de la historia.",
            "Mientras tanto, Atlantis y Themyscira libraban una guerra de aniquilación mutua, con Aquaman y Wonder Woman masacrando a millones en Europa.",
            "Cuando intentaron rescatar a Superman, encontraron a un hombre esquelético que el gobierno mantuvo encerrado en un búnker subterráneo sin ver jamás la luz del Sol.",
            "Reverse Flash apareció solo para revelarle la cruel verdad: el culpable de toda esta destrucción no fue nadie más que el propio Barry al romper la barrera del tiempo.",
            "Thomas Wayne asesinó a Thawne y le entregó una carta a Barry para su hijo Bruce, permitiéndole correr al pasado para restaurar la realidad en uno de los momentos más emotivos de DC."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/a/a8/Flashpoint_Vol_2_1.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/3c/Flashpoint_Vol_2_2.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/e/ed/Flashpoint_Batman_-_Knight_of_Vengeance_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/32/Flashpoint_Batman_-_Knight_of_Vengeance_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/5e/Flashpoint_Vol_2_3.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/6/6f/Flashpoint_Vol_2_4.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/8/88/Flashpoint_Vol_2_5.png",
            "https://static.wikia.nocookie.net/marvel_dc/images/9/9f/Flashpoint_Batman_-_Knight_of_Vengeance_Vol_1_3.jpg"
        ]
    },
    {
        "id": "cosmic_ghost_rider_el_vengador_del_infinito",
        "character": "Cosmic Ghost Rider",
        "title": "Cosmic Ghost Rider El Vengador del Infinito",
        "theme_signature": "cosmic_ghost_rider:frank_castle:vengador_galactus",
        "description": "Historia épica completa de cómic: Cosmic Ghost Rider El Vengador del Infinito. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#CosmicGhostRider #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué obtienes cuando combinas al Castigador, el Espíritu de la Venganza de Ghost Rider y el Poder Cósmico de Galactus? Este es Cosmic Ghost Rider.",
            "En un futuro donde Thanos aniquiló a todos los héroes, Frank Castle murió en combate y su alma descendió al infierno consumida por una rabia inagotable.",
            "Hizo un pacto con Mephisto para regresar como Ghost Rider, pero al volver encontró una Tierra totalmente vacía donde vagó en soledad durante millones de años hasta perder la cordura.",
            "Cuando un Galactus herido aterrizó buscando ayuda, Frank le ofreció el planeta a cambio de ser bendecido con el Poder Cósmico, convirtiéndose en el heraldo más desquiciado del universo.",
            "Juntos enfrentaron a King Thanos, pero tras la muerte de Galactus, Frank terminó convirtiéndose en el sirviente y verdugo personal del titán loco durante milenios.",
            "Harto de tanta destrucción, utilizó una gema del tiempo para viajar al pasado con la intención de eliminar a Thanos siendo apenas un bebé en su cuna.",
            "Sin embargo, al mirar los ojos del niño, Frank no fue capaz de matarlo y decidió criarlo él mismo por todo el cosmos intentando convertirlo en un héroe.",
            "Armado con cadenas forjadas con huesos de Cyttorak y montando una moto infernal capaz de viajar por el hiperespacio, Cosmic Ghost Rider se convirtió en una leyenda cósmica absoluta."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/9/93/Cosmic_Ghost_Rider_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/5/5e/Thanos_Vol_2_13.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/2/26/Cosmic_Ghost_Rider_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/2/21/Cosmic_Ghost_Rider_Vol_1_3.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/f/f9/Thanos_Vol_2_14.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/f/f7/Cosmic_Ghost_Rider_Vol_1_4.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/5/51/Cosmic_Ghost_Rider_Vol_1_5.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/7/7b/Thanos_Vol_2_15.jpg"
        ]
    },
    {
        "id": "dark_nights_metal_la_invasion_del_multiverso_oscuro",
        "character": "Batman",
        "title": "Dark Nights Metal La Invasión del Multiverso Oscuro",
        "theme_signature": "batman:dark_nights_metal:barbatos_invasion",
        "description": "Historia épica completa de cómic: Dark Nights Metal La Invasión del Multiverso Oscuro. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Batman #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué hay debajo del mapa del multiverso conocido? Un abismo de pesadillas llamado el Multiverso Oscuro, donde cada miedo de Batman se hizo realidad.",
            "El dios murciélago Barbatos utilizó metales místicos para transformar a Bruce Wayne en un portal viviente y liberar a su ejército de Caballeros Oscuros.",
            "Entre ellos llegó The Red Death, un Batman que encadenó a Flash en el Batmóvil para robarle la Speed Force y ejecutar a todos los criminales en segundos.",
            "The Devastator, un Batman que se inyectó el virus Doomsday para asesinar a Superman cuando el hombre de acero se volvió loco en su mundo.",
            "Y comandando a todas estas pesadillas estaba El Batman Que Ríe, el ser más sádico y despiadado que infectó la Tierra con cartas de metal oscuro.",
            "La Liga de la Justicia fue capturada una a una, con Superman y Mujer Maravilla siendo conectados a baterías cósmicas para arrastrar el planeta al abismo.",
            "Solo cuando Batman y la Liga descubrieron el Décimo Metal, la sustancia de la creación pura, forjaron armaduras de luz capaces de repeler la oscuridad.",
            "Con una alianza entre Batman y el Joker, lograron derrotar a las pesadillas y restaurar el multiverso, sellando la guerra más oscura en la historia de DC."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/0/05/Dark_Nights_Metal_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/a/ae/Dark_Nights_Metal_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/b/b2/Batman_The_Red_Death_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/3f/Batman_The_Devastator_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/d/d5/Dark_Nights_Metal_Vol_1_3.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/5b/Dark_Nights_Metal_Vol_1_4.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/1/11/Dark_Nights_Metal_Vol_1_5.jpg",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/3a/Dark_Nights_Metal_Vol_1_6.jpg"
        ]
    },
    {
        "id": "injustice_el_regimen_del_hombre_de_acero",
        "character": "Superman",
        "title": "Injustice El Regimen del Hombre de Acero",
        "theme_signature": "superman:injustice:regimen_tirania_joker",
        "description": "Historia épica completa de cómic: Injustice El Regimen del Hombre de Acero. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Superman #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué pasaría si el héroe más puro de la Tierra perdiera la cordura por completo? Esto no fue una pesadilla, fue el nacimiento del tirano más temido del multiverso.",
            "El Joker drogó a Superman con una toxina de kriptonita. En su alucinación creyó enfrentar a Doomsday, pero en realidad asesinó con sus propias manos a Lois Lane y a su hijo por nacer.",
            "La bomba atómica vinculada al corazón de Lois estalló, destruyendo Metrópolis. Roto por el dolor, Superman cruzó la línea definitiva y atravesó el pecho del Joker frente a Batman.",
            "Convencido de que la piedad era debilidad, Clark fundó el Régimen de la Tierra, imponiendo una dictadura global donde cualquier crimen se pagaba con la muerte inmediata.",
            "Héroes como Wonder Woman y Flash se arrodillaron ante él por lealtad o miedo, mientras Batman organizaba una resistencia clandestina para detener a su mejor amigo.",
            "Para igualar el poder de los dioses, la resistencia de Batman desarrolló píldoras nanotecnológicas que otorgaban a simples humanos la fuerza física de un kriptoniano.",
            "La guerra entre Batman y Superman desató batallas sangrientas en todo el planeta, donde héroes legendarios cayeron ejecutados sin piedad por el Hombre de Acero.",
            "El símbolo de la esperanza se convirtió en la mayor tiranía de la historia, demostrando que un solo día trágico puede transformar al mayor salvador en el peor dictador."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/8/8b/Injustice_Gods_Among_Us_Vol_1_1_Raapack_Variant.jpg/revision/latest?cb=20131202222220",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/58/Injustice_Gods_Among_Us_Vol_1_2.jpg/revision/latest?cb=20131202215321",
            "https://static.wikia.nocookie.net/marvel_dc/images/4/42/Injustice_Gods_Among_Us_Vol_1_3.jpg/revision/latest?cb=20131202222941",
            "https://static.wikia.nocookie.net/marvel_dc/images/7/77/Injustice_Gods_Among_Us_Vol_1_4.jpg/revision/latest?cb=20131202223326",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/3c/Injustice_Gods_Among_Us_Vol_1_5.jpg/revision/latest?cb=20131202223817",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/51/Injustice_Gods_Among_Us_Vol_1_6.jpg/revision/latest?cb=20131205130825",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/5b/Injustice_Gods_Among_Us_Vol_1_7.jpg/revision/latest?cb=20131205131214",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/3e/Injustice_Gods_Among_Us_Vol_1_8.jpg/revision/latest?cb=20131205154233"
        ]
    },
    {
        "id": "marvel_zombies_el_hambre_del_multiverso",
        "character": "Marvel Zombies",
        "title": "Marvel Zombies El Hambre del Multiverso",
        "theme_signature": "marvel_zombies:infeccion:hambre_cosmica",
        "description": "Historia épica completa de cómic: Marvel Zombies El Hambre del Multiverso. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#MarvelZombies #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "Existe un universo alterno donde los mayores protectores de la Tierra se convirtieron en la mayor plaga de la existencia, devorando todo a su paso con un apetito insaciable.",
            "Un misterioso destello trajo un virus alienígena hipercontagioso. En cuestión de pocas horas, los Vengadores, los X-Men y los Cuatro Fantásticos fueron infectados.",
            "Lo más aterrador del virus es que no destruyó su intelecto; conservaron sus recuerdos, su ingenio táctico y sus poderes, pero dominados por un hambre infinita.",
            "Tras devorar a casi toda la población humana del planeta, el Devorador de Mundos Galactus llegó a la Tierra, sin imaginar que esta vez él sería la presa.",
            "Hulk, Spider-Man, Wolverine y Iron Man zombificados unieron fuerzas, despedazaron a Galactus y lo devoraron vivo, absorbiendo en sus cuerpos el Poder Cósmico.",
            "Con la capacidad de volar por el espacio a la velocidad de la luz, los héroes zombi abandonaron la Tierra y comenzaron a consumir planetas enteros por todo el universo.",
            "Imperios intergalácticos gigantescos como los Kree y los Skrull cayeron ante la horda cósmica, que aniquiló mundos enteros en una implacable cacería espacial.",
            "El hambre voraz consumió galaxias enteras en décadas, dejando un vacío oscuro y silencioso en una de las historias más escalofriantes y brutales de Marvel Comics."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/2/23/Marvel_Zombies_Vol_1_1_Textless.jpg/revision/latest?cb=20071205234704",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/ca/Marvel_Zombies_Vol_1_2_Textless.jpg/revision/latest?cb=20071205232133",
            "https://static.wikia.nocookie.net/marveldatabase/images/1/14/Marvel_Zombies_Vol_1_3_Textless.jpg/revision/latest?cb=20071205234419",
            "https://static.wikia.nocookie.net/marveldatabase/images/1/13/Marvel_Zombies_Vol_1_4_Textless.jpg/revision/latest?cb=20141030091545",
            "https://static.wikia.nocookie.net/marveldatabase/images/a/ab/Marvel_Zombies_Vol_1_5_Textless.jpg/revision/latest?cb=20071205235112",
            "https://static.wikia.nocookie.net/marveldatabase/images/8/87/Marvel_Zombies_2_Vol_1_1_Textless.jpg/revision/latest?cb=20071206003407",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/c9/Marvel_Zombies_2_Vol_1_2_Textless.jpg/revision/latest?cb=20071206003727",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/cc/Marvel_Zombies_Return_Vol_1_1_Textless.png/revision/latest?cb=20191206182916"
        ]
    },
    {
        "id": "crisis_en_tierras_infinitas_el_sacrificio_de_los_heroes",
        "character": "The Flash",
        "title": "Crisis en Tierras Infinitas El Sacrificio de los Heroes",
        "theme_signature": "flash:crisis_tierras_infinitas:sacrificio_antimonitor",
        "description": "Historia épica completa de cómic: Crisis en Tierras Infinitas El Sacrificio de los Heroes. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#TheFlash #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "En los anales del cómic existe un cataclismo tan devastador que borró incontables universos enteros de la faz del tiempo: la legendaria Crisis en Tierras Infinitas.",
            "Desde el universo de antimateria, una entidad titánica conocida como el Antimonitor desató una ola destructora que consumió realidades paralelas como hojas al fuego.",
            "Héroes y villanos de múltiples Tierras tuvieron que aliarse bajo el liderazgo del Monitor para intentar salvar los últimos fragmentos de la existencia cósmica.",
            "Supergirl protagonizó uno de los sacrificios más heroicos de la historia al atacar directamente al Antimonitor, destruyendo su armadura antes de caer en batalla.",
            "Pero el momento culminante llegó cuando Barry Allen, Flash, fue capturado para alimentar el cañón de antimateria definitivo que destruiría las Tierras restantes.",
            "Flash corrió más rápido de lo que ningún mortal jamás lo había hecho, desafiando las leyes de la física para revertir el flujo de energía destructiva del cañón.",
            "Su cuerpo comenzó a envejecer y desintegrarse por la fricción temporal, convirtiéndose en energía pura y salvando al multiverso a costa de su propia vida.",
            "Cinco universos supervivientes se fusionaron en una sola línea temporal renacida, sellando el sacrificio más legendario en la historia de DC Comics."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/8/82/Crisis_on_Infinite_Earths_Vol_1_1.jpg/revision/latest?cb=20160825142130",
            "https://static.wikia.nocookie.net/marvel_dc/images/8/82/Crisis_on_Infinite_Earths_2.jpg/revision/latest?cb=20060521153332",
            "https://static.wikia.nocookie.net/marvel_dc/images/d/d9/Crisis_on_Infinite_Earths_3.jpg/revision/latest?cb=20060610031917",
            "https://static.wikia.nocookie.net/marvel_dc/images/0/03/Crisis_on_Infinite_Earths_4.jpg/revision/latest?cb=20070711122056",
            "https://static.wikia.nocookie.net/marvel_dc/images/7/71/Crisis_on_Infinite_Earths_7.jpg/revision/latest?cb=20070226142252",
            "https://static.wikia.nocookie.net/marvel_dc/images/7/78/Crisis_on_Infinite_Earths_8.jpg/revision/latest?cb=20070722135215",
            "https://static.wikia.nocookie.net/marvel_dc/images/4/43/Crisis_on_Infinite_Earths_10.jpg/revision/latest?cb=20070525163546",
            "https://static.wikia.nocookie.net/marvel_dc/images/e/e3/Crisis_on_Infinite_Earths_12.jpg/revision/latest?cb=20070108135253"
        ]
    },
    {
        "id": "thanos_wins_el_fin_de_la_existencia",
        "character": "Thanos",
        "title": "Thanos Wins El Fin de la Existencia",
        "theme_signature": "thanos:thanos_wins:rey_final_tiempo",
        "description": "Historia épica completa de cómic: Thanos Wins El Fin de la Existencia. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Thanos #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué pasaría si el Titán Loco finalmente lograra vencer a todos los seres del cosmos? Esta es la oscura historia donde Thanos se convierte en el amo del fin del tiempo.",
            "Millones de años en el futuro, el Rey Thanos ha exterminado a casi toda la vida cósmica: los Vengadores, los Celestiales y los dioses galácticos fueron aniquilados.",
            "En su solitario trono sobre el planeta Titán, Thanos mantiene a un envejecido Hulk encadenado en las profundidades como su bestia de caza personal.",
            "A su lado sirve el Motorista Fantasma Cósmico, Frank Castle, convertido en el heraldo demente que viaja por el cosmos ejecutando sus órdenes.",
            "Utilizando la Piedra del Tiempo, Thanos envía a Ghost Rider al pasado para secuestrar a su versión joven, trayéndolo directamente hasta el fin de los tiempos.",
            "El joven Thanos queda impactado al descubrir que su contraparte anciana no lo trajo para gobernar juntos, sino para pedirle un favor inaudito y desesperado.",
            "El Rey Thanos necesita ser asesinado en un combate a muerte por el único ser digno de arrebatarle la vida: él mismo, para poder reunirse con su amada Muerte.",
            "Una confrontación épica entre dos eras del mismo titán que demostró que el mayor enemigo de Thanos siempre fue su propia ambición infinita."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/1/12/Thanos_Vol_2_13_Textless.jpg/revision/latest?cb=20170823104559",
            "https://static.wikia.nocookie.net/marveldatabase/images/4/43/Thanos_Vol_2_14_Textless.jpg/revision/latest?cb=20170919222822",
            "https://static.wikia.nocookie.net/marveldatabase/images/8/8b/Thanos_Vol_2_15_Textless.jpg/revision/latest?cb=20171018003749",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/da/Thanos_Vol_2_16_Textless.jpg/revision/latest?cb=20171121210531",
            "https://static.wikia.nocookie.net/marveldatabase/images/b/b4/Thanos_Vol_2_17_Textless.jpg/revision/latest?cb=20171219190144",
            "https://static.wikia.nocookie.net/marveldatabase/images/6/6f/Thanos_Vol_2_18_Textless.jpg/revision/latest?cb=20180123193124",
            "https://static.wikia.nocookie.net/marveldatabase/images/6/66/Thanos_Annual_Vol_2_1_Textless.jpg/revision/latest?cb=20180123194334",
            "https://static.wikia.nocookie.net/marveldatabase/images/8/84/Thanos_Legacy_Vol_1_1_Textless.jpg/revision/latest?cb=20180620022624"
        ]
    },
    {
        "id": "blackest_night_la_rebelion_de_los_muertos",
        "character": "Green Lantern",
        "title": "Blackest Night La Rebelion de los Muertos",
        "theme_signature": "green_lantern:blackest_night:nekron_anillos_negros",
        "description": "Historia épica completa de cómic: Blackest Night La Rebelion de los Muertos. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#GreenLantern #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "Cuando los muertos del universo DC se levantaron de sus tumbas, la noche más oscura cubrió el cosmos en una de las historias más aterradoras jamás escritas.",
            "Nekron, la encarnación primordial de la muerte, junto a Black Hand, forjaron los anillos negros de poder que viajaron por las galaxias buscando a los difuntos.",
            "Héroes caídos como Batman, Aquaman, Superman y Detective Marciano regresaron como Linternas Negras con sus poderes corrompidos por el odio.",
            "Los Linternas Negras se alimentaban de las emociones de los vivos, arrancando los corazones de sus antiguos compañeros para acumular energía de muerte.",
            "Los siete cuerpos de linternas, desde los verdes de Hal Jordan hasta los amarillos de Sinestro y los rojos de Atrocitus, se vieron obligados a forjar una tregua.",
            "Hal Jordan y los líderes del espectro emocional combinaron la luz de todos los colores cósmicos, despertando a la milagrosa Entidad Blanca de la Vida.",
            "Sinestro y Hal Jordan empuñaron la luz blanca de la creación, transformando a los héroes en Linternas Blancos y resucitando a los caídos.",
            "La luz de la vida purificó la oscuridad eterna de Nekron, restaurando el balance cósmico en la batalla más monumental del universo de Linterna Verde."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marvel_dc/images/1/18/Blackest_Night_Vol_1_1.jpg/revision/latest?cb=20090716030734",
            "https://static.wikia.nocookie.net/marvel_dc/images/a/a5/Blackest_Night_Vol_1_2.jpg/revision/latest?cb=20090814001519",
            "https://static.wikia.nocookie.net/marvel_dc/images/0/07/Blackest_Night_3.jpg/revision/latest?cb=20090916213616",
            "https://static.wikia.nocookie.net/marvel_dc/images/8/81/Blackest_Night_4A.jpg/revision/latest?cb=20091028185626",
            "https://static.wikia.nocookie.net/marvel_dc/images/e/ed/Blackest_Night_5.jpg/revision/latest?cb=20091125202701",
            "https://static.wikia.nocookie.net/marvel_dc/images/3/3e/Blackest_Night_Vol_1_6.jpg/revision/latest?cb=20091230232824",
            "https://static.wikia.nocookie.net/marvel_dc/images/5/50/Blackest_Night_Vol_1_7.jpg/revision/latest?cb=20100225010212",
            "https://static.wikia.nocookie.net/marvel_dc/images/8/86/Blackest_Night_Vol_1_8.jpg/revision/latest?cb=20100401003910"
        ]
    },
    {
        "id": "world_war_hulk_la_furia_del_destructor_de_mundos",
        "character": "Hulk",
        "title": "World War Hulk La Furia del Destructor de Mundos",
        "theme_signature": "hulk:world_war_hulk:furia_destructor_mundos",
        "description": "Historia épica completa de cómic: World War Hulk La Furia del Destructor de Mundos. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Hulk #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué pasa cuando los mayores héroes de la Tierra traicionan a Hulk y lo destierran al espacio? Esta es la historia del día en que el gigante esmeralda regresó como un dios de la guerra para vengarse.",
            "Tras perder a su esposa y a su reino en el planeta Sakaar por una bomba de los Illuminati, Hulk aterrizó en la Luna, destrozó a Black Bolt de un solo golpe y lanzó un ultimátum a toda la humanidad.",
            "Tony Stark intentó frenarlo con la armadura Hulkbuster más avanzada jamás creada, pero la furia del coloso era infinita y demolió la Torre de los Vengadores dejando a Iron Man inconsciente.",
            "Ni siquiera el poder combinado de todos los X-Men y el imparable Juggernaut pudieron hacerle cosquillas; Hulk humilló a cada mutante que intentó proteger al Profesor Xavier.",
            "El Doctor Strange tuvo que fusionarse con el demonio Zom para igualar su fuerza brutal, pero Hulk resistió la magia prohibida y le rompió las manos al Hechicero Supremo.",
            "En su momento más oscuro, la Tierra recurrió a su última esperanza: Sentry, el héroe con el poder de un millón de soles explotando, desatando una colisión que casi parte el planeta en dos.",
            "Ambos titanes intercambiaron golpes capaces de alterar la atmósfera hasta que Sentry agotó toda su energía cósmica y cayó derrotado frente a la resistencia inquebrantable de Hulk.",
            "Liberando el estado de Destructor de Mundos, cada paso de Hulk amenazaba con hundir el continente entero, consolidando este día como la demostración de poder más devastadora en la historia de Marvel."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/9/9a/Incredible_Hulk_Vol_2_105_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/de/World_War_Hulk_Vol_1_1_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/e/e1/World_War_Hulk_Vol_1_2.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/1/13/World_War_Hulk_X-Men_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/d0/World_War_Hulk_Vol_1_3.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/0/08/World_War_Hulk_Vol_1_4.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/3/3b/World_War_Hulk_Vol_1_4_Romita_Jr._Variant.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/6/6c/World_War_Hulk_Vol_1_5_Textless.jpg"
        ]
    },
    {
        "id": "god_emperor_doom_el_amo_del_multiverso",
        "character": "Doctor Doom",
        "title": "God Emperor Doom El Amo del Multiverso",
        "theme_signature": "doctor_doom:secret_wars:amo_battleworld",
        "description": "Historia épica completa de cómic: God Emperor Doom El Amo del Multiverso. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#DoctorDoom #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Qué pasa cuando el multiverso entero es destruido y un solo hombre tiene el poder absoluto para reconstruir la existencia? Este es Doctor Doom como el Dios Emperador.",
            "Cuando los omnipotentes Beyonders desataron el fin de todas las realidades mediante las incursiones, ni los Vengadores ni los dioses cósmicos pudieron evitar la aniquilación total.",
            "Aliándose con el Hombre Molécula, Victor von Doom desafió a los propios creadores del cosmos, robando su energía ilimitada para convertirse en una deidad viviente.",
            "De las cenizas del multiverso muerto, Doom moldeó Battleworld, un mundo mosaico donde gobernó como dios omnipotente protegido por un ejército de Thors.",
            "Cuando Thanos osó desafiar su reinado proclamándose un dios, Doom ni siquiera titubeó: con una sola mano le arrancó la columna vertebral y el cráneo en un segundo.",
            "Incluso cuando Cíclope desató todo el poder cósmico de la Fuerza Fénix para derrocarlo, Doom le rompió el cuello con facilidad, probando que su poder estaba más allá de todo límite.",
            "Solo su eterno rival, Reed Richards, logró enfrentarlo en un duelo cósmico definitivo para decidir el destino de cada universo que alguna vez existió.",
            "Al final, Doom admitió la verdad y restauró el multiverso, dejando grabado en la eternidad el día en que un hombre fue el amo supremo del cosmos."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/1/14/Secret_Wars_Vol_1_8_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/f/fd/Secret_Wars_Vol_1_6_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/a/aa/Secret_Wars_Vol_1_7_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/3/3a/Secret_Wars_Vol_1_9_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/e/e0/Amazing_Spider-Man_Vol_5_11_Fantastic_Four_Villains_Variant_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/3/38/All-Out_Avengers_Vol_1_2_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/a/a6/Secret_Wars_Vol_1_7_Lee_Variant_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/b/b5/Books_of_Doom_Vol_1_2_Textless.jpg"
        ]
    },
    {
        "id": "gorr_el_carnicero_de_dioses",
        "character": "Thor",
        "title": "Gorr el Carnicero de Dioses",
        "theme_signature": "thor:gorr:carnicero_dioses_necroespada",
        "description": "Historia épica completa de cómic: Gorr el Carnicero de Dioses. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Thor #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Sabías que en el universo Marvel existió un simple mortal tan implacable que logró masacrar a panteones enteros de dioses durante miles de años? Este es Gorr, el Carnicero de Dioses.",
            "Nacido en un planeta desértico y hostil, vio morir de hambre a sus hijos mientras rezaban desesperadamente a dioses que jamás respondieron. Su devoción se transformó en un rencor eterno.",
            "Todo cambió cuando dos deidades cayeron a su mundo. Gorr reclamó la legendaria Necroespada 'All-Black', el primer simbionte forjado en la oscuridad primordial por Knull, el dios de los simbiontes.",
            "Empuñando una espada capaz de degollar seres cósmicos, Gorr inició una cruzada de sangre imparable a través de las galaxias con un único objetivo: la extinción total de toda deidad.",
            "Durante tres milenios torturó y decapitó a dioses de la guerra, de la magia y del tiempo, sembrando el terror cósmico en cada rincón del multiverso.",
            "Para su golpe maestro, esclavizó a los dioses supervivientes para forjar la Bomba Divina, un artefacto colosal diseñado para detonar y aniquilar a todos los dioses del pasado, presente y futuro.",
            "Hizo falta una alianza imposible entre tres versiones temporales de Thor: el joven vikingo, el Vengador del presente y el anciano Rey Thor del fin del tiempo para desafiar su poder.",
            "Al final, Gorr demostró una verdad aterradora: que cuando un mortal es traicionado por el destino, ni los propios dioses son inmortales."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/4/4a/Gorr_%28Earth-616%29_and_All-Black_%28Symbiote%29_%28Earth-616%29_from_Thor_God_of_Thunder_Vol_1_6_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/c9/Thor_God_of_Thunder_Vol_1_6.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/0/09/Gorr_%28Earth-616%29_and_All-Black_%28Symbiote%29_%28Earth-616%29_from_Thor_God_of_Thunder_Vol_1_9_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/d/d0/Thor_God_of_Thunder_Vol_1_5_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/e/e5/Thor_God_of_Thunder_Vol_1_8_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/4/4d/Gorr_%28Earth-616%29_from_King_Thor_Vol_1_1_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/2/2b/Thor_God_of_Thunder_Vol_1_1.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/4/4b/Gorr_%28Earth-616%29_and_All-Black_%28Symbiote%29_%28Earth-616%29_from_Phoenix_Vol_1_5_001.jpg"
        ]
    }
]


def load_ledger() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Warning reading ledger: {e}")
        return []


def save_ledger(ledger: list[dict]):
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def normalize_text(text: str) -> str:
    """Lowercase, strip accents, punctuation, and extra whitespace."""
    nfkd = unicodedata.normalize('NFKD', str(text or ""))
    cleaned = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    return " ".join(cleaned.split())


def is_duplicate(story: dict, ledger: list[dict]) -> tuple[bool, str]:
    """
    5-Layer Anti-Duplication Shield:
    1. Exact ID Collision Check
    2. Canonical Theme Signature Collision Check
    3. Normalized Exact Title Collision Check
    4. Canonical Theme Sub-Tag Multi-Intersection Collision Check
    5. Character Arc & Semantic Keyword Topic Overlap Collision Check (>50% match)
    """
    story_id = story.get("id", "").strip().lower()
    story_theme = story.get("theme_signature", "").strip().lower()
    story_title_norm = normalize_text(story.get("title", ""))
    story_char = normalize_text(story.get("character", ""))

    stopwords = {
        "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "en", "por",
        "con", "que", "del", "al", "para", "the", "of", "and", "in", "to", "su", "sus"
    }

    story_title_tokens = set(w for w in story_title_norm.split() if len(w) > 3 and w not in stopwords)
    story_theme_tokens = set(w for w in normalize_text(story_theme.replace(":", " ")).split() if len(w) > 3 and w not in stopwords)
    all_story_tokens = story_title_tokens.union(story_theme_tokens)

    for item in ledger:
        item_id = item.get("id", "").strip().lower()
        item_theme = item.get("theme_signature", "").strip().lower()
        item_title_norm = normalize_text(item.get("title", ""))
        item_char = normalize_text(item.get("character", ""))

        # Layer 1: Exact ID match
        if story_id and item_id and story_id == item_id:
            return True, f"Layer 1 (ID Collision): Story ID '{story_id}' was already produced ({item.get('date', 'past')})"

        # Layer 2: Exact Theme Signature match
        if story_theme and item_theme and story_theme == item_theme:
            return True, f"Layer 2 (Theme Collision): Signature '{story_theme}' already published in '{item.get('title')}'"

        # Layer 3: Normalized Title exact match
        if story_title_norm and item_title_norm and story_title_norm == item_title_norm:
            return True, f"Layer 3 (Title Collision): Title matches existing entry '{item.get('title')}'"

        # Layer 4: Canonical Theme Sub-Tag Intersection (>= 2 sub-tags match)
        if story_theme and item_theme:
            story_tags = set(p for p in story_theme.split(":") if p)
            item_tags = set(p for p in item_theme.split(":") if p)
            common_tags = story_tags.intersection(item_tags)
            if len(common_tags) >= 2:
                return True, f"Layer 4 (Theme Sub-tag Collision): Shared arc tags {common_tags} with '{item.get('title')}'"

        # Layer 5: Character Arc & Semantic Keyword Topic Overlap
        if all_story_tokens:
            item_title_tok = set(w for w in item_title_norm.split() if len(w) > 3 and w not in stopwords)
            item_theme_tok = set(w for w in normalize_text(item_theme.replace(":", " ")).split() if len(w) > 3 and w not in stopwords)
            all_item_tokens = item_title_tok.union(item_theme_tok)

            overlap = all_story_tokens.intersection(all_item_tokens)

            # If both feature the same character, require only 2 specific topical arc words to block
            if story_char and item_char and (story_char in item_char or item_char in story_char):
                char_tokens = set(story_char.split())
                specific_overlap = overlap - char_tokens
                if len(specific_overlap) >= 2:
                    return True, f"Layer 5 (Character Arc Collision): Character '{story_char}' has redundant arc topics {specific_overlap} with '{item.get('title')}'"
            # Or if across any character, 3 or more thematic keywords overlap
            elif len(overlap) >= 3:
                return True, f"Layer 5 (High Semantic Collision): Redundant thematic tokens {overlap} with '{item.get('title')}'"

    return False, ""


def record_production(story: dict, mode: str, video_path: str):
    ledger = load_ledger()
    record = {
        "id": story["id"],
        "title": story["title"],
        "character": story.get("character", "Unknown"),
        "theme_signature": story.get("theme_signature", ""),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "mode": mode,
        "video_file": Path(video_path).name,
        "status": "published" if mode == "live_release" else ("draft" if mode == "draft_only" else "produced"),
    }
    ledger.append(record)
    save_ledger(ledger)


def create_full_panel_frame(im: Image.Image, target_w: int = 1080, target_h: int = 1920) -> Image.Image:
    """
    Guarantees 100% COMPLETE comic panel visibility (Zero Cropping):
    1. Background Layer: Scaled to cover 1080x1920 with smooth Gaussian blur (radius=28) and dark tint.
    2. Foreground Panel: Scaled to contain within 94% width and 65% height, leaving bottom area for Remotion subtitles.
    3. Border: Clean black comic outline so the vignette pops.
    """
    bg_scale = max(target_w / im.width, target_h / im.height)
    bg_w, bg_h = int(im.width * bg_scale), int(im.height * bg_scale)
    bg = im.resize((bg_w, bg_h), Image.Resampling.BILINEAR)
    left = (bg_w - target_w) // 2
    top = (bg_h - target_h) // 2
    bg = bg.crop((left, top, left + target_w, top + target_h))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=28))

    dark_overlay = Image.new('RGB', (target_w, target_h), (12, 14, 20))
    bg = Image.blend(bg, dark_overlay, alpha=0.55)

    max_fg_w = int(target_w * 0.94)
    max_fg_h = int(target_h * 0.65)
    fg_scale = min(max_fg_w / im.width, max_fg_h / im.height)
    fg_w, fg_h = int(im.width * fg_scale), int(im.height * fg_scale)
    fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

    fg_x = (target_w - fg_w) // 2
    fg_y = max(130, int((target_h * 0.68 - fg_h) / 2) + 40)

    border_w = 4
    border_img = Image.new('RGB', (fg_w + border_w * 2, fg_h + border_w * 2), (0, 0, 0))
    border_img.paste(fg, (border_w, border_w))

    bg.paste(border_img, (fg_x - border_w, fg_y - border_w))
    return bg


def build_cloud_generation(story: dict, work_dir: Path) -> dict:
    gen_dir = work_dir / story["id"]
    gen_dir.mkdir(parents=True, exist_ok=True)

    curated_urls = story.get("scene_art_urls", [])
    if curated_urls:
        log(f"Using {len(curated_urls)} curated 1:1 comic panels for '{story['title']}'...")
        art_urls = curated_urls
    else:
        log(f"Obtaining official comic art for '{story['character']}'...")
        art_urls = story.get("image_urls") or get_fandom_comic_art(story.get("character", "Batman"), count=len(story["scenes"]) + 5)
    log(f"Discovered {len(art_urls)} high-resolution comic assets.")

    scenes_data = []
    scene_videos = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    for idx, narration in enumerate(story["scenes"], 1):
        sc_name = f"scene_{idx:02d}"
        sc_dir = gen_dir / sc_name
        sc_dir.mkdir(parents=True, exist_ok=True)
        img_file = sc_dir / f"{sc_name}.jpg"

        saved = False
        if art_urls and idx <= len(art_urls):
            try:
                r = requests.get(art_urls[idx - 1], headers=headers, timeout=15)
                if r.status_code == 200 and len(r.content) > 10000:
                    im = Image.open(io.BytesIO(r.content)).convert('RGB')
                    # Guardar el arte oficial de cómic en resolución completa (Full-screen Ken Burns idéntico a local)
                    im.save(img_file, "JPEG", quality=95)
                    saved = True
            except Exception as e:
                log(f"Warning processing image {idx}: {e}")
                saved = False

        if not saved or not img_file.exists():
            im = Image.new("RGB", (1080, 1920), color=(15, 18, 25))
            im.save(img_file, quality=92)

        scenes_data.append({
            "scene_number": idx,
            "voiceover_text": narration,
            "narration": narration
        })

        scene_videos.append({
            "folder": sc_name,
            "video": str(img_file),
            "images": [str(img_file)],
            "scene_number": idx,
            "is_image": True,
            "image_count": 1
        })

    script_data = {
        "metadata": {
            "title": story["title"],
            "description": story["description"],
            "hashtags": story["hashtags"],
            "voice": os.environ.get("VOICE", "es-US-Studio-B")
        },
        "scenes": scenes_data
    }

    script_path = gen_dir / "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    return {
        "path": str(gen_dir),
        "name": story["id"],
        "script": script_data,
        "scene_videos": scene_videos,
        "scene_count": len(scene_videos)
    }


def main():
    parser = argparse.ArgumentParser(description="Multiverso Comic Autonomous Cloud Generation & Publisher")
    parser.add_argument("--story-id", type=str, help="Specific story ID to generate (or 'any' for auto queue)")
    parser.add_argument("--publish", action="store_true", help="Auto-publish to FB Page and IG after generation")
    parser.add_argument("--draft", action="store_true", help="Save as unpublished draft on FB and skip public IG")
    parser.add_argument("--dry-run", action="store_true", help="Test workflow without video generation or publishing")
    args = parser.parse_args()

    log("Initializing Multiverso Comic Engine with Ironclad Anti-Duplication Shield...")
    log("Repository: multiverso-comic (branch: main)")
    log(f"FB Page ID: {os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)}")
    log(f"IG Account ID: {os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)}")

    ledger = load_ledger()
    log(f"Historical Ledger: {len(ledger)} previously produced videos registered.")

    # Story Selection & Anti-Duplication Verification
    if args.story_id and args.story_id != "any":
        selected = next((s for s in EDITORIAL_STORIES if s["id"] == args.story_id), None)
        if not selected:
            # Check if this ID was an old historical story
            old_item = next((item for item in ledger if item.get("id") == args.story_id), None)
            if old_item:
                log(f"CRITICAL ANTI-DUPLICATION SHIELD: Requested story '{args.story_id}' is in historical ledger (Produced: {old_item.get('date')}).")
                log(f"Existing Title: {old_item.get('title')}")
                log("ABORTING: Duplicates are strictly prohibited.")
                sys.exit(0)
            else:
                log(f"Error: Story ID '{args.story_id}' not found in catalog or ledger.")
                sys.exit(1)

        is_dup, reason = is_duplicate(selected, ledger)
        if is_dup:
            log(f"CRITICAL ANTI-DUPLICATION SHIELD: Story '{selected['title']}' rejected.")
            log(f"Reason: {reason}")
            log("No duplicate videos will ever be produced. Aborting safely.")
            sys.exit(0)
    else:
        available = [s for s in EDITORIAL_STORIES if not is_duplicate(s, ledger)[0]]
        log(f"Available unproduced stories in catalog: {len(available)} / {len(EDITORIAL_STORIES)}")

        if not available:
            log("ALL cataloged stories have already been produced! Zero duplicates permitted.")
            log("Add new storylines to EDITORIAL_STORIES before running next production.")
            sys.exit(0)

        selected = random.choice(available)

    log(f"Selected Unique Story: {selected['title']} (ID: {selected['id']})")

    if args.dry_run:
        log("DRY RUN mode verified. Story is 100% unique and passed all 5 anti-duplication layers.")
        log("Exiting without video render or Meta publish as requested.")
        sys.exit(0)

    work_dir = Path("scratch_cloud_gen")
    work_dir.mkdir(parents=True, exist_ok=True)
    generation = build_cloud_generation(selected, work_dir)

    output_root = Path("output")
    output_root.mkdir(parents=True, exist_ok=True)

    # Lazy import pipeline to allow test environments to run without heavy whisper dependencies
    from .pipeline import run_pipeline

    voice_choice = os.environ.get("VOICE", "es-US-Studio-B")
    log(f"Starting video compilation pipeline with voice: {voice_choice}...")
    final_video_path = run_pipeline(
        generation=generation,
        output_name=selected["id"],
        voice=voice_choice,
        output_root=str(output_root),
        final_video_dir=str(output_root / "finals")
    )

    log(f"Render completed: {final_video_path}")

    mode_str = "render_only"
    if args.publish or os.environ.get("AUTO_PUBLISH", "").lower() in ("true", "1", "yes"):
        is_draft = args.draft or os.environ.get("DRAFT_ONLY", "").lower() in ("true", "1", "yes")
        mode_str = "draft_only" if is_draft else "live_release"
        log(f"Initiating publication to Meta (mode: {'DRAFT ONLY' if is_draft else 'LIVE PUBLIC'})...")
        publish_comic_video(
            video_path=final_video_path,
            title=selected["title"],
            description=selected["description"],
            hashtags=selected["hashtags"],
            draft_only=is_draft,
        )
    else:
        log("Publication skipped (render_only mode).")

    record_production(selected, mode_str, final_video_path)
    log(f"Anti-duplication registry updated: '{selected['id']}' locked permanently.")


if __name__ == "__main__":
    main()
