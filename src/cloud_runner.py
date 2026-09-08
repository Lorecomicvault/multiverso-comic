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

EDITORIAL_STORIES = [
    {
        "id": "hulk_maestro_futuro_imperfecto",
        "character": "Hulk",
        "title": "Hulk Maestro: El Tirano del Futuro Imperfecto",
        "theme_signature": "hulk:future_imperfect:maestro_distopia",
        "description": "En un futuro postapocalíptico donde una guerra nuclear aniquiló a los héroes, Hulk absorbió la radiación, conservó la mente de Banner y se coronó como el cruel emperador Maestro.",
        "hashtags": "#Hulk #Maestro #MarvelComics #FuturoImperfecto #ComicsNarrados #Reels",
        "scenes": [
            "En un futuro desolado donde una guerra nuclear arrasó a la civilización y mató a casi todos los héroes, solo un ser prosperó en las cenizas radiactivas: Hulk.",
            "Habiendo absorbido décadas de radiación residual, su fuerza física se multiplicó monstruosamente, pero esta vez conservó la brillante e implacable mente de Bruce Banner.",
            "Adoptando el nombre de 'Maestro', erradicó a los últimos señores de la guerra y construyó Dystopia, proclamándose gobernante supremo y tirano absoluto del planeta.",
            "En su sala de trofeos personal coleccionó los restos de sus antiguos amigos: el escudo roto del Capitán América, el martillo de Thor y el cráneo de Wolverine.",
            "Desesperados, los rebeldes viajaron en el tiempo para traer al Hulk del pasado, esperando que el gigante esmeralda pudiera derrocar a su propia versión anciana.",
            "Tras una sangrienta colisión titánica, Hulk utilizó la máquina del tiempo para enviar a Maestro al epicentro exacto de la explosión de la Bomba Gamma original."
        ]
    },
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
        ]
    },
    {
        "id": "kingdom_come_justicia_divina",
        "character": "Superman",
        "title": "Kingdom Come: El Juicio Final de los Antiguos Dioses",
        "theme_signature": "superman:kingdom_come:magog_apocalipsis",
        "description": "En un futuro donde una nueva generación de metahumanos despiadados siembra el caos, un envejecido Superman sale de su retiro para imponer orden moral.",
        "hashtags": "#KingdomCome #Superman #Batman #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Tras el asesinato del Joker a manos de Magog y el aplauso de la sociedad a la violencia letal, un Superman desilusionado se recluyó en su granja durante una década.",
            "Sin la guía moral de la Liga de la Justicia original, una nueva generación de antihéroes irresponsables convirtió al mundo en un campo de batalla anárquico.",
            "El desastre nuclear en Kansas forzó al Hombre de Acero a descender de los cielos con su escudo negro y rojo para refundar la Liga y encarcelar a los rebeldes.",
            "Batman se opuso a los métodos autoritarios de Kal-El, aliándose con humanos y marginados mediante armaduras mecanizadas para defender la libertad de elección.",
            "La tensión estalló en el Gulag Metahumano, desatando una guerra colosal donde Lex Luthor lavó el cerebro de Shazam para enfrentarlo a muerte contra Superman.",
            "Cuando las Naciones Unidas lanzaron una bomba nuclear para aniquilar a todos los metahumanos, Shazam se sacrificó para salvar la coexistencia entre humanos y dioses."
        ]
    },
    {
        "id": "all_star_superman_morrison",
        "character": "Superman",
        "title": "All-Star Superman: Los Doce Trabajos del Héroe Moribundo",
        "theme_signature": "superman:all_star:muerte_celular_sol",
        "description": "Envenenado por una sobredosis de radiación solar en una trampa de Luthor, a Superman le queda un año de vida y decide consagrar sus últimos días a salvar el futuro.",
        "hashtags": "#AllStarSuperman #Superman #LexLuthor #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Durante una misión de rescate en el corazón del Sol saboteada por Lex Luthor, las células de Superman absorbieron una cantidad letal de energía solar.",
            "El diagnóstico fue demoledor: la sobrecarga celular le otorgaba poderes multiplicados, pero consumiría su cuerpo mortal en menos de trescientos días.",
            "Lejos de caer en la desesperación, Clark Kent decidió dedicar su tiempo restante a completar doce hazañas míticas para dejar a la humanidad en paz.",
            "Le reveló su identidad a Lois Lane, le obsequió sus poderes por veinticuatro horas y viajó al inframundo para responder la pregunta fundamental de la Esfinge.",
            "Lex Luthor ingirió una fórmula para obtener el poder de Superman, pero al ver el universo con la percepción divina de Clark, rompió en llanto al comprender la belleza cósmica.",
            "Con su cuerpo disolviéndose en energía pura, el Hombre de Acero voló hacia el centro del Sol moribundo para reparar su corazón y brillar como luz eterna."
        ]
    },
    {
        "id": "magneto_testamento_origen",
        "character": "Magneto",
        "title": "Magneto: Testamento - La Forja del Dolor en Auschwitz",
        "theme_signature": "magneto:testamento:origen_auschwitz",
        "description": "Antes de liderar a los mutantes o llamarse Magneto, un joven judío llamado Max Eisenhardt sobrevivió al horror del campo de exterminio de Auschwitz.",
        "hashtags": "#Magneto #XMen #MarvelComics #MagnetoTestament #ComicsNarrados #Reels",
        "scenes": [
            "Mucho antes de proclamarse el Amo del Magnetismo, un joven judío alemán llamado Max Eisenhardt vio cómo el mundo civilizado se transformaba en una pesadilla nazi.",
            "Durante la Segunda Guerra Mundial, su familia fue capturada y ejecutada sumariamente, mientras Max era arrojado a las fauces de Auschwitz.",
            "Obligado a formar parte de los Sonderkommando, tuvo la siniestra tarea de transportar los cuerpos de miles de inocentes hacia los hornos crematorios.",
            "En medio del lodo, el hambre y la crueldad más atroz, Max no utilizó poderes mágicos: sobrevivió únicamente gracias a una férrea voluntad de hierro.",
            "Al reencontrarse con Magda, el amor de su vida, organizó una revuelta desesperada dinamitando los crematorios y escapando a través de los bosques congelados.",
            "Aquel niño que vio morir a su pueblo juró una sola cosa: que ninguna especie volvería a ser perseguida jamás. Así nació la leyenda implacable de Magneto."
        ]
    },
    {
        "id": "daredevil_born_again",
        "character": "Daredevil",
        "title": "Daredevil: Born Again - La Destrucción y Renacer de Matt Murdock",
        "theme_signature": "daredevil:born_again:kingpin_venganza",
        "description": "Karen Page vende la identidad secreta de Daredevil por una dosis de heroína. Kingpin desmantela la vida de Matt Murdock pieza por pieza hasta que solo queda el hombre sin miedo.",
        "hashtags": "#Daredevil #BornAgain #Kingpin #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Hundida en la adicción a las drogas en México, Karen Page vendió el secreto más peligroso del mundo por una dosis de heroína: la identidad civil de Daredevil.",
            "La información llegó a las manos de Wilson Fisk, el Kingpin, quien no ordenó asesinar a Matt Murdock, sino destruir minuciosamente cada pilar de su existencia.",
            "Fisk congeló sus cuentas bancarias, le retiró su licencia de abogado con falsas acusaciones y dinamitó su departamento en Hell's Kitchen mientras dormía.",
            "Despojado de todo, vagando como un indigente enfermo y al borde de la demencia por las calles congeladas, Murdock tocó el fondo del abismo.",
            "Pero cuando Kingpin creyó haberlo aniquilado, comprendió su error más fatal: un hombre sin esperanza es un hombre que ya no tiene nada que temer.",
            "Enfundado en su traje rojo y blandiendo sus bastones, Daredevil resurgió del fuego para desmantelar al supersoldado Nuke y humillar al imperio de Kingpin."
        ]
    },
    {
        "id": "wolverine_arma_x",
        "character": "Wolverine",
        "title": "Wolverine: Arma X - La Agonía del Adamantium",
        "theme_signature": "wolverine:weapon_x:implante_adamantium",
        "description": "En las frías instalaciones secretas de Canadá, científicos del Proyecto Arma X secuestran a Logan para someterlo al brutal implante de adamantium líquido.",
        "hashtags": "#Wolverine #ArmaX #WeaponX #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "En lo profundo de los bosques congelados de Canadá, el misterioso consorcio del Proyecto Arma X secuestró a Logan para convertirlo en el arma perfecta.",
            "Conectado a tubos respiratorios y monitores cerebrales, su factor curativo mutante fue llevado al límite absoluto del dolor humano.",
            "Adamantium líquido a temperaturas extremas fue bombeado directamente a través de sus huesos, fundiéndose molecularmente con su esqueleto entero.",
            "Los científicos borraron sistemáticamente sus recuerdos, intentando reducir al hombre a una bestia asesina sin alma controlada por computadoras.",
            "Pero el salvajismo primario de Wolverine despertó en un estallido de garras metálicas ensangrentadas, destrozando el tanque de contención de vidrio.",
            "Masacró a todo el personal de seguridad en un frenesí despiadado y huyó descalzo por la nieve ensangrentada, libre pero marcado para siempre."
        ]
    },
    {
        "id": "punisher_born_vietnam",
        "character": "The Punisher",
        "title": "The Punisher: Born - El Pacto Maldito de Frank Castle en Vietnam",
        "theme_signature": "punisher:born:valle_fong_dra",
        "description": "En la base militar de Valley Forge durante la guerra de Vietnam, el capitán Frank Castle escucha una voz en la oscuridad que le ofrece sobrevivir a cambio de una guerra eterna.",
        "hashtags": "#ThePunisher #FrankCastle #MarvelComics #PunisherBorn #ComicsNarrados #Reels",
        "scenes": [
            "En el año 1971, en la remota base de avanzada Valley Forge en Vietnam, el capitán de marines Frank Castle comandaba a un pelotón rodeado por el enemigo.",
            "Mientras la locura de la jungla consumía a sus soldados y los suministros se agotaban, Frank sentía una fascinación siniestra por la carnicería del combate.",
            "En la noche más oscura, bajo un monzón torrencial, una división entera del Viet Cong atacó la base en una embestida suicida imparable.",
            "Todos los compañeros de Frank cayeron acribillados; herido y bañado en sangre, una voz espectral en su mente le susurró un trato macabro.",
            "La entidad le ofreció la fuerza para sobrevivir a esa noche a cambio de un compromiso eterno: entregar su alma a una guerra sin fin que nunca terminaría.",
            "Castle aceptó sin dudar. Años después, la mafia mató a su familia en Central Park, desatando al monstruo que ya había nacido en aquella colina."
        ]
    },
    {
        "id": "thor_ragnarok_crepusculo",
        "character": "Thor",
        "title": "Thor: Ragnarok - El Sacrificio de los Ojos y el Fin de Asgard",
        "theme_signature": "thor:ragnarok:yggdrasil_hilos_destino",
        "description": "El ciclo interminable del Ragnarok amenaza con destruir Asgard una vez más, pero Thor descubre a las sombras cósmicas que se alimentan de la tragedia de los dioses.",
        "hashtags": "#Thor #Ragnarok #MarvelComics #Asgard #ComicsNarrados #Reels",
        "scenes": [
            "Las profecías nórdicas comenzaron a cumplirse: Loki forjó armas de Uru con el fuego de Surtur y marchó sobre Asgard liderando un ejército de pesadilla.",
            "El reino dorado cayó en ruinas, el puente Bifrost fue destrozado y los dioses guerreros murieron uno a uno en una carnicería mitológica sin precedentes.",
            "Thor comprendió que la fuerza bruta de su martillo no bastaba: acudió al Pozo de Mimir y sacrificó sus dos ojos para alcanzar la Sabiduría Rúnica absoluta.",
            "Colgado de las ramas del Árbol del Mundo Yggdrasil hasta las puertas de la muerte, Thor descubrió la verdad cósmica más oscura de la existencia.",
            "Un panteón de parásitos dimensionales llamados 'Aquellos que se sientan en las sombras' manipulaban el ciclo del Ragnarok para alimentarse de la muerte de los dioses.",
            "Con un golpe monumental de su poder rúnico, Thor quebró el telar del destino, destruyendo a los falsos dioses y liberando a su pueblo del ciclo eterno."
        ]
    },
    {
        "id": "knightfall_la_caida_del_murcielago",
        "character": "Bane",
        "title": "Knightfall: El Día en que Bane Quebró la Espalda de Batman",
        "theme_signature": "batman:knightfall:bane_quiebra_columna",
        "description": "Bane libera a todos los reclusos del Asilo Arkham para agotar a Batman hasta el límite físico, para luego emboscarlo en la Mansión Wayne y partir su columna en dos.",
        "hashtags": "#Knightfall #Batman #Bane #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Nacido en la infernal prisión caribeña de Peña Duro, el coloso táctico conocido como Bane fijó su objetivo supremo: conquistar Gotham y destruir a Batman.",
            "Utilizando un lanzacohetes, voló los muros del Asilo Arkham liberando al Joker, Acertijo, Espantapájaros y a cada demente para sembrar el caos.",
            "Durante tres meses agotadores, Bruce Wayne patrulló sin dormir ni alimentarse, capturando a cada prófugo hasta que su cuerpo colapsó de agotamiento.",
            "Cuando un Batman agonizante y febril regresó a la Mansión Wayne, Bane lo esperaba tranquilamente en la oscuridad de la sala principal.",
            "Sin fuerzas para defenderse, el Murciélago fue golpeado salvajemente por el titán potenciado con Veneno, quien lo arrojó como a un muñeco de trapo.",
            "Alzando a Bruce sobre su cabeza, Bane estrelló la espalda del héroe contra su rodilla con un crujido seco que quebró la columna del Caballero de la Noche."
        ]
    },
    {
        "id": "moon_knight_khonshu_locura",
        "character": "Moon Knight",
        "title": "Moon Knight: La Venganza de Khonshu y el Desollamiento de Bushman",
        "theme_signature": "moon_knight:khonshu:bushman_venganza",
        "description": "Marc Spector toca fondo con las piernas rotas y abandonado por sus aliados, hasta que la voz del dios Khonshu lo impulsa a una venganza visceral contra Bushman.",
        "hashtags": "#MoonKnight #Khonshu #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "En lo alto de un rascacielos de Nueva York, Marc Spector libró una batalla a muerte contra su archienemigo Raoul Bushman, cayendo al vacío y rompiéndose las piernas.",
            "En un ataque de furia psicótica bajo la luna llena, Marc tomó su daga con forma de media luna y desolló el rostro entero de Bushman ante el horror de la noche.",
            "Traumatizado por su propia barbarie y lisiado, Spector se sumió en la depresión, la adicción a los analgésicos y el aislamiento más absoluto.",
            "Sus personalidades fragmentadas, Steven Grant y Jake Lockley, lo atormentaban en su mente mientras sus amigos más leales le daban la espalda.",
            "Pero el dios de la luna Khonshu, manifestándose con el rostro putrefacto de Bushman, exigió que su avatar se pusiera de pie para derramar más sangre.",
            "Con exoesqueletos en sus piernas y su capa blanca impecable, el Caballero Luna regresó a las calles para demostrar que la locura es su mayor armadura."
        ]
    },
    {
        "id": "silver_surfer_requiem",
        "character": "Silver Surfer",
        "title": "Silver Surfer: Réquiem - El Último Vuelo del Heraldo",
        "theme_signature": "silver_surfer:requiem:muerte_norrin_radd",
        "description": "Norrin Radd descubre que su piel plateada se está deteriorando y le quedan pocas semanas de vida. En su viaje final, regala a la Tierra el don de la armonía absoluta.",
        "hashtags": "#SilverSurfer #Galactus #MarvelComics #Requiem #ComicsNarrados #Reels",
        "scenes": [
            "Al examinar su cuerpo cósmico, Reed Richards descubrió una verdad trágica: la membrana plateada de Silver Surfer se estaba desintegrando irreversiblemente.",
            "Sabiendo que le quedaban pocos días de existencia, Norrin Radd no buscó curas ni guardó rencor: decidió despedirse de los seres que más amaba en el cosmos.",
            "Se reunió con Spider-Man en lo alto de un puente para contemplar la belleza de la humanidad, antes de realizar su regalo final a la Tierra.",
            "Utilizando hasta el último gramo de su Poder Cósmico, envolvió al planeta entero en una onda de empatía que detuvo todas las guerras y el odio por cinco minutos.",
            "Emprendió su último viaje hacia su planeta natal Zenn-La, donde Galactus descendió de las estrellas para rendir homenaje al más noble de sus heraldos.",
            "En el instante final, Galactus creó una estrella brillante en su memoria para que la luz de Norrin Radd ilumine el universo por toda la eternidad."
        ]
    },
    {
        "id": "maximum_carnage_matanza",
        "character": "Carnage",
        "title": "Maximum Carnage: El Reinado de Pura Demencia de Cletus Kasady",
        "theme_signature": "carnage:maximum_carnage:masacre_nueva_york",
        "description": "El psicópata Cletus Kasady escapa del Instituto Ravencroft y forma una sádica familia con Shriek para convertir las calles de Manhattan en un río de sangre.",
        "hashtags": "#Carnage #SpiderMan #Venom #MarvelComics #MaximumCarnage #Reels",
        "scenes": [
            "Recluido en el Instituto Ravencroft, la sangre mutada del asesino en serie Cletus Kasady regeneró al simbionte Carnage desde su propio torrente sanguíneo.",
            "Tras masacrar a los guardias, reclutó a villanos dementes como Shriek, Demogoblin y Carrion, autoproclamándose una sádica familia de la muerte.",
            "Utilizando los poderes sónicos de Shriek para infectar las mentes de los ciudadanos, Carnage sumergió a Manhattan en una ola de violencia caníbal incontrolable.",
            "Spider-Man intentó frenar la masacre, pero fue superado y gravemente herido en las costillas, comprendiendo que la justicia ordinaria era inútil.",
            "Desesperado, el arácnido tuvo que romper su principio más sagrado y forjar una tregua incómoda con Venom, Black Cat y Cloak and Dagger.",
            "En una batalla colosal en Central Park, Venom arrojó a Carnage contra un generador de microondas industriales, sofocando la carnicería carmesí."
        ]
    },
    {
        "id": "doctor_strange_el_juramento",
        "character": "Doctor Strange",
        "title": "Doctor Strange: El Juramento - La Búsqueda del Elixir de Otkid",
        "theme_signature": "doctor_strange:the_oath:elixir_salvacion_wong",
        "description": "Cuando a Wong le diagnostican un tumor cerebral inoperable, el Hechicero Supremo arriesga su alma en una dimensión letal para robar el elixir mágico de Otkid.",
        "hashtags": "#DoctorStrange #Wong #MarvelComics #TheOath #ComicsNarrados #Reels",
        "scenes": [
            "El mundo de Stephen Strange se derrumbó cuando los médicos diagnosticaron a Wong, su fiel compañero y mejor amigo, un cáncer cerebral terminal inoperable.",
            "Negándose a aceptar la pérdida, Strange viajó al plano astral y penetró en las bóvedas cósmicas de Otkid para robar la poción mágica de sanación definitiva.",
            "Al regresar a su Sanctum Sanctorum, un intruso encapuchado le disparó en el corazón con una bala de plata mística, dejándolo desangrándose en el suelo.",
            "Manifestando su forma astral para dirigir a la Enfermera Nocturna durante su propia cirugía de emergencia, Strange logró salvar su vida por segundos.",
            "La conspiración era aterradora: una farmacéutica multimillonaria contrató a Nicodemus West para destruir el elixir y evitar que las enfermedades fueran erradicadas.",
            "Obligado a elegir entre sanar al mundo o salvar a su hermano del alma, Strange administró la última gota a Wong, reafirmando el valor supremo de la lealtad."
        ]
    },
    {
        "id": "green_lantern_crepusculo_esmeralda",
        "character": "Green Lantern",
        "title": "Emerald Twilight: La Caída de Hal Jordan y el Nacimiento de Parallax",
        "theme_signature": "green_lantern:emerald_twilight:hal_jordan_parallax",
        "description": "Tras la destrucción total de Coast City por Mongul, Hal Jordan pierde la razón, masacra al Cuerpo de Linternas Verdes y absorbe la Batería Central como Parallax.",
        "hashtags": "#GreenLantern #HalJordan #Parallax #DCComics #EmeraldTwilight #Reels",
        "scenes": [
            "Al regresar a la Tierra tras la invasión de Mongul y Cyborg Superman, Hal Jordan encontró su amada Coast City reducida a un cráter humeante de siete millones de muertos.",
            "Consumido por un dolor insoportable, utilizó su anillo de poder para recrear la ciudad entera con constructos verdes, hablando con los fantasmas de sus seres queridos.",
            "Los Guardianes de Oa lo reprendieron fríamente por usar el anillo con fines personales y le ordenaron entregarlo de inmediato para ser juzgado.",
            "La ira de Hal estalló en locura: voló a través del espacio hacia Oa, derrotando y despojando de sus anillos a cada compañero Linterna Verde que intentó frenarlo.",
            "En las puertas de la Batería Central, ejecutó a Sinestro rompiéndole el cuello y asesinó a Kilowog antes de sumergirse directamente en el reactor esmeralda.",
            "Al absorber la energía total de la batería cósmica, Hal Jordan emergió renacido como la entidad destructora Parallax, extinguiendo al Cuerpo por completo."
        ]
    },
    {
        "id": "kravens_last_hunt_spider_man",
        "character": "Spider-Man",
        "title": "La Última Cacería de Kraven: La Muerte del Cazador y el Ataúd de Peter",
        "theme_signature": "spider_man:kravens_last_hunt:entierro_cazador",
        "description": "Kraven el Cazador derrota a Spider-Man, lo sepulta vivo en una tumba y asume su identidad para demostrar que es un depredador infinitamente superior.",
        "hashtags": "#SpiderMan #Kraven #MarvelComics #KravensLastHunt #ComicsNarrados #Reels",
        "scenes": [
            "Sintiendo la vejez y la muerte pisándole los talones, Kraven el Cazador se propuso un único objetivo para coronar su vida: cazar y destruir a Spider-Man.",
            "En un callejón lluvioso, le disparó al arácnido con un potente dardo tranquilizante, noqueándolo por completo antes de arrojarlo a un ataúd de madera.",
            "Kraven enterró a Spider-Man dos metros bajo tierra en un cementerio abandonado, dejándolo sepultado en una asfixiante oscuridad absoluta.",
            "Durante dos semanas, Kraven vistió el traje negro de Spidey, patrullando las calles y propinando brutales golpizas a los criminales para superar al héroe.",
            "Impulsado por el amor a Mary Jane y su inquebrantable fuerza de voluntad, Peter Parker arañó la madera, emergiendo de la tierra lodosa como un espectro.",
            "Al ver que su victoria sobre la araña era total y que nada más le quedaba por demostrar, Kraven sonrió satisfecho y puso fin a su propia vida."
        ]
    },
    {
        "id": "invincible_omni_man_conquista",
        "character": "Omni-Man",
        "title": "Invincible: La Traición de Omni-Man y la Masacre de los Guardianes",
        "theme_signature": "invincible:omni_man:masacre_guardianes_globo",
        "description": "Nolan Grayson reúne a los legendarios Guardianes del Globo bajo una falsa alarma y los descuartiza sin piedad para preparar la conquista viltrumita de la Tierra.",
        "hashtags": "#Invincible #OmniMan #MarkGrayson #ComicsNarrados #Reels",
        "scenes": [
            "Durante dos décadas, Nolan Grayson fingió ser el protector más benevolente y poderoso de la Tierra bajo el nombre de Omni-Man.",
            "Convocó a los legendarios Guardianes del Globo a su cuartel general secreto con una alerta de máxima emergencia, cerrando las compuertas de seguridad tras de sí.",
            "En una emboscada aterradora, decapitó a Red Rush, partió en dos a War Woman y masacró a sangre fría a cada héroe legendario del planeta.",
            "Semanas después, al revelarle a su hijo Mark la verdad sobre el despiadado Imperio Viltrumita, le exigió unirse a la conquista de la Tierra.",
            "Cuando Mark se negó a traicionar a la humanidad, Omni-Man desató una paliza colosal, usándolo como ariete para partir en dos un tren repleto de civiles.",
            "Con Mark ensangrentado y al borde de la muerte preguntándole qué le quedaría después de quinientos años, Nolan susurró 'a ti' y huyó llorando al espacio."
        ]
    },
    {
        "id": "soldado_del_invierno_resurreccion",
        "character": "Winter Soldier",
        "title": "El Soldado del Invierno: El Fantasma de Bucky Barnes",
        "theme_signature": "captain_america:winter_soldier:bucky_codo_acero",
        "description": "Un asesino soviético con brazo cibernético asesina a Red Skull y a Jack Monroe. Steve Rogers descubre con dolor que el ejecutor es Bucky Barnes, resucitado y condicionado.",
        "hashtags": "#CapitanAmerica #WinterSoldier #BuckyBarnes #MarvelComics #Reels",
        "scenes": [
            "En las sombras de la Guerra Fría, un asesino fantasma con un brazo biónico soviético sembró el terror en misiones secretas de ejecución quirúrgica.",
            "Cuando el criminal apareció en Washington asesinando a Red Skull y robando el Cubo Cósmico, el Capitán América inició una cacería implacable.",
            "Durante un sangriento tiroteo en una refinería, Steve Rogers logró arrancarle la máscara al asesino, reconociendo el rostro que lo persiguió en sus pesadillas.",
            "Era Bucky Barnes, su leal compañero de la Segunda Guerra Mundial, a quien creyó ver morir en la explosión de un avión en el Atlántico Norte.",
            "Los rusos lo habían rescatado de las aguas congeladas, implantándole un brazo de titanio y borrando su mente con choques eléctricos tras cada misión.",
            "Al usar el poder del Cubo Cósmico para ordenarle 'recuerda quién eres', Bucky rompió en llanto al recuperar su memoria y huyó al abismo de la culpa."
        ]
    },
    {
        "id": "batman_endgame_joker_final",
        "character": "Batman",
        "title": "Batman: Endgame - La Guerra Química Final del Joker",
        "theme_signature": "batman:endgame:dionisio_muerte_caverna",
        "description": "El Joker infecta a la Liga de la Justicia para atacar a Batman, desatando luego una toxina mortal aerotransportada en Gotham alimentada por Dionisio puro.",
        "hashtags": "#Batman #Joker #Endgame #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Sin previo aviso, Wonder Woman, Flash, Aquaman y Superman atacaron a Batman en Gotham con miradas vacías y sonrisas demenciales en sus rostros.",
            "Bruce tuvo que desplegar el colosal traje mecha Fenrir para neutralizar a la Liga de la Justicia, descubriendo que el Joker los había infectado con una toxina personalizada.",
            "El Príncipe Payaso del Crimen reveló su verdadero juego: una cepa vírica incurable que convirtió a millones de ciudadanos de Gotham en zombis maníacos.",
            "El Guasón afirmó ser una criatura inmortal que caminaba por la ciudad antes de su fundación, alimentado por el estanque regenerativo de Dionisio.",
            "En las cavernas más profundas bajo la Baticueva, Batman y el Joker se enfrentaron en un duelo a muerte salvaje a puñaladas y golpes brutales.",
            "Con la caverna derrumbándose sobre sus cuerpos desangrados, Bruce retuvo al villano en las sombras mientras susurraba que al fin descansarían juntos."
        ]
    },
    {
        "id": "spawn_malebolgia_guerra",
        "character": "Spawn",
        "title": "Spawn: El Pacto con Malebolgia y la Venganza de Al Simmons",
        "theme_signature": "spawn:malebolgia:octavo_circulo_infierno",
        "description": "Traicionado y quemado vivo por su propio gobierno, el asesino Al Simmons entrega su alma al señor demoníaco Malebolgia para volver a ver a su esposa Wanda.",
        "hashtags": "#Spawn #AlSimmons #Malebolgia #ToddMcFarlane #ComicsNarrados #Reels",
        "scenes": [
            "Al Simmons era el asesino más letal de la CIA, hasta que sus propios superiores lo traicionaron, ordenando quemarlo vivo en una misión clandestina.",
            "Al descender al Octavo Círculo del Infierno, su desesperación por volver a ver a su amada esposa Wanda llamó la atención del señor demoníaco Malebolgia.",
            "Malebolgia le ofreció un trato: volver a la Tierra con vida a cambio de convertirse en el general de su armada infernal como un Hellspawn.",
            "Simmons aceptó, despertando cinco años después en los callejones hediondos de Nueva York con su carne carbonizada oculta bajo un traje simbiótico viviente.",
            "Al buscar a Wanda, descubrió la verdad más desgarradora: ella se había casado con su mejor amigo y había formado una hermosa familia sin él.",
            "Lleno de ira y dolor, Spawn juró usar las cadenas y el necroplasma del infierno para masacrar tanto a mafiosos terrenales como a los demonios de Malebolgia."
        ]
    },
    {
        "id": "guerra_de_bromas_y_acertijos",
        "character": "The Riddler",
        "title": "La Guerra de Bromas y Acertijos: Gotham Dividida por el Caos",
        "theme_signature": "batman:war_jokes_riddles:joker_vs_riddler",
        "description": "Gotham se convierte en un sangriento tablero de guerra cuando el Joker y el Acertijo reclutan ejércitos de supervillanos para competir por matar a Batman.",
        "hashtags": "#Batman #TheJoker #TheRiddler #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Incapaz de reír tras meses de frustración, el Joker fue abordado por el Acertijo, quien le propuso aliarse para resolver el enigma definitivo: Batman.",
            "El Joker le disparó a quemarropa en el abdomen y se marchó; aquel balazo desató la guerra civil más sangrienta en la historia criminal de Gotham.",
            "Cada villano tuvo que elegir bando: Deadshot y Deathstroke libraron una batalla de cinco días matando a cientos de civiles atrapados en el fuego cruzado.",
            "Durante un año de asedio, la ciudad fue dividida en dos fortalezas militares con francotiradores, gas hilarante y trampas de acertijos mortales.",
            "Para poner fin a la matanza de inocentes, Batman se vio obligado a infiltrarse y sentar a ambos monstruos en una mesa de negociación en la Mansión Wayne.",
            "Al descubrir la maquiavélica frialdad de Edward Nygma, Bruce estuvo a punto de degollarlo con un cuchillo, siendo detenido en el último segundo por el propio Joker."
        ]
    },
    {
        "id": "infinity_gauntlet_original_thanos",
        "character": "Thanos",
        "title": "The Infinity Gauntlet: El Chasquido Original por Amor a la Muerte",
        "theme_signature": "thanos:infinity_gauntlet_1991:chasquido_lady_death",
        "description": "En la saga original de 1991, Thanos reúne las seis Gemas del Infinito y con un simple chasquido de dedos borra al 50% de la vida cósmica como ofrenda a su amada Muerte.",
        "hashtags": "#Thanos #InfinityGauntlet #MarvelComics #LadyDeath #ComicsNarrados #Reels",
        "scenes": [
            "Resucitado por la Muerte para corregir el desequilibrio cósmico de la vida en el universo, el Titán Loco Thanos fijó la mirada en las seis Gemas del Infinito.",
            "Con astucia y crueldad inauditas, engañó a los Ancianos del Universo y derrotó al Intermediario para incrustar las gemas en su guantelete de oro.",
            "Con el poder de la omnipotencia en su puño, construyó un templo de obsidiana en el espacio y convocó a su adorada amante cósmica: la Señora Muerte.",
            "Al ver que la entidad ignoraba sus ruegos y lo consideraba un ser repulsivo, Mephisto le susurró al oído la demostración definitiva de devoción.",
            "Con un chasquido seco de sus dedos enjoyados, la mitad de toda la vida inteligente del cosmos se desvaneció en polvo en una milésima de segundo.",
            "Entidades cósmicas como Galactus, Kronos y el Tribunal Viviente se estremecieron al comprender que Thanos se había convertido en el dios absoluto de la creación."
        ]
    }
]


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [MultiversoComic-AntiDup] {msg}", flush=True)


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
        img_file = sc_dir / f"{sc_name}.png"

        saved = False
        if art_urls and idx <= len(art_urls):
            try:
                r = requests.get(art_urls[idx - 1], headers=headers, timeout=15)
                if r.status_code == 200 and len(r.content) > 10000:
                    im = Image.open(io.BytesIO(r.content)).convert('RGB')
                    frame_img = create_full_panel_frame(im, target_w=1080, target_h=1920)
                    frame_img.save(img_file, quality=94)
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
