"""
Comic Lore Vault - Autonomous Cloud Video Runner & Publisher (Spanish Engine)
Anti-Duplication Engine: Guarantees zero repeated stories, characters arcs, or themes.
Repository: comic-lore-espanol (main)
"""

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from PIL import Image
import requests

from .comic_fetcher import get_fandom_comic_art
from .pipeline import run_pipeline
from .publisher import publish_comic_video, DEFAULT_PAGE_ID, DEFAULT_IG_USER_ID

LEDGER_PATH = Path("published_ledger.json")

EDITORIAL_STORIES = [
    {
        "id": "knull_dios_simbiontes",
        "character": "Knull",
        "title": "Knull: El Dios de los Simbiontes y la Necroespada",
        "theme_signature": "knull:simbiontes:king_in_black",
        "description": "Antes de la luz y las estrellas, Knull reinaba en el abismo. De su sombra forjó la Necroespada y decapitó a un Celestial, creando la mente colmena simbionte.",
        "hashtags": "#Knull #Venom #KingInBlack #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Antes de que existiera la luz, las estrellas o el propio Big Bang, solo existía la oscuridad absoluta, y en el centro de ese abismo reinaba un ser: Knull, el Dios de los Simbiontes.",
            "Cuando los Celestiales trajeron la luz al cosmos, Knull se sintió ultrajado: de su propia sombra forjó la legendaria Necroespada All-Black y decapitó a un dios Celestial de un solo tajo.",
            "Utilizando la cabeza del dios muerto como forja, Knull creó a la raza simbionte entera como una mente colmena viviente diseñada exclusivamente para devorar civilizaciones enteras.",
            "Millones de años después, Knull despertó de su prisión planetaria y marchó hacia la Tierra liderando un ejército incontable de dragones simbiontes que bloquearon el Sol por completo.",
            "Los Vengadores enviaron a su héroe más poderoso, Sentry, pero Knull lo agarró en el aire y lo partió por la mitad con sus manos desnudas, demostrando que ningún mortal podía dañarlo.",
            "Solo cuando Eddie Brock se fusionó con la Fuerza Enigma para convertirse en el Dios de la Luz, el reinado de sombras de Knull llegó a su sangriento y definitivo final."
        ]
    },
    {
        "id": "batman_que_rie",
        "character": "The Batman Who Laughs",
        "title": "El Batman Que Ríe: La Pesadilla del Multiverso Oscuro",
        "theme_signature": "batman:batman_who_laughs:dark_multiverse",
        "description": "¿Qué pasaría si Batman cruzara la línea y se transformara en el Joker? La inteligencia táctica de Bruce Wayne fusionada con la demencia absoluta del Guasón.",
        "hashtags": "#BatmanQueRie #TheBatmanWhoLaughs #DCComics #DarkMultiverse #ComicsNarrados #Reels",
        "scenes": [
            "¿Qué pasaría si Batman cruzara la línea y se transformara en el Joker? Esta es la pesadilla viva del Multiverso Oscuro.",
            "Al quebrar el cuello del Joker en su última batalla, una neurotoxina purificada infectó el corazón de Bruce Wayne, fusionando su mente maestra con una demencia sin límites.",
            "En solo veinticuatro horas, el Batman Que Ríe ejecutó fríamente a toda la Liga de la Justicia utilizando los planes de contingencia que él mismo había diseñado.",
            "Masacró a los Jóvenes Titanes y aniquiló a la mismísima Batifamilia en la Baticueva sin titubear ni mostrar un ápice de remordimiento.",
            "Con su visor de metal oscuro que le permite ver a través de las dimensiones y los miedos del alma humana, conquistó el cosmos entero.",
            "Convirtiéndose en el Rey de las Sombras y sirviente de Perpetua, demostró que un Batman sin código moral es el monstruo más letal de la creación."
        ]
    },
    {
        "id": "injustice_regimen_superman",
        "character": "Superman",
        "title": "Injustice: El Régimen del Hombre de Acero",
        "theme_signature": "superman:injustice:regimen_tirania",
        "description": "El día en que el héroe más puro de la Tierra perdió la cordura y se convirtió en el dictador más temido del multiverso.",
        "hashtags": "#Injustice #Superman #Batman #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "¿Qué pasaría si el héroe más puro de la Tierra perdiera la cordura por completo? Este fue el trágico nacimiento del tirano más temido del multiverso.",
            "El Joker drogó a Superman con toxina del miedo y kriptonita: creyendo enfrentar a Doomsday en el espacio, Clark asesinó con sus manos a Lois Lane y a su hijo por nacer.",
            "La bomba nuclear vinculada al corazón de Lois estalló, pulverizando Metrópolis; roto por el dolor, Superman atravesó el pecho del Joker ante los ojos de Batman.",
            "Convencido de que la piedad era debilidad, Clark fundó el Régimen Global de la Tierra, ejecutando criminales y gobernando con puño de hierro absoluto.",
            "Héroes como Wonder Woman lo respaldaron mientras Batman forjaba una resistencia clandestina, desarrollando píldoras nanotecnológicas para igualar la fuerza de los dioses.",
            "El símbolo de la esperanza eterna se transformó en la mayor dictadura de la historia, demostrando que un solo día trágico puede corromper al dios más noble."
        ]
    },
    {
        "id": "gorr_carnicero_dioses",
        "character": "Gorr the God Butcher",
        "title": "Gorr el Carnicero de Dioses: La Venganza de la Necroespada",
        "theme_signature": "thor:gorr:god_butcher_necrosword",
        "description": "Tras ver morir a su familia en un mundo desértico mientras los dioses ignoraban sus rezos, Gorr juró purgar el cosmos de cada deidad viviente.",
        "hashtags": "#Thor #Gorr #GodButcher #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "En un mundo árido y desolado, Gorr vio morir de hambre a su madre, su esposa y sus hijos mientras los dioses del cielo ignoraban cada una de sus plegarias.",
            "Cuando dos deidades cayeron heridas del firmamento pidiendo auxilio, la furia de Gorr explotó: tomó la Necroespada All-Black y juró extinguir a cada dios del cosmos.",
            "Durante tres mil años cazó y descuartizó panteones enteros a lo largo del universo, dejando templos en ruinas y ríos de sangre divina a su paso.",
            "Ni siquiera el poderoso Thor de joven pudo detener su avance despiadado, siendo capturado y torturado durante semanas en las cavernas del terror.",
            "Gorr esclavizó a cientos de dioses para construir la Bomba Divina, un artefacto capaz de aniquilar a todas las deidades en el pasado, presente y futuro de golpe.",
            "Solo la alianza temporal de tres versiones de Thor de distintas épocas pudo desafiar al carnicero en la batalla más épica de la mitología nórdica."
        ]
    },
    {
        "id": "world_war_hulk_coloso",
        "character": "Hulk",
        "title": "World War Hulk: La Venganza del Rompemundos",
        "theme_signature": "hulk:world_war_hulk:venganza_coloso",
        "description": "Exiliado por los Illuminati y devastado por la muerte de su reina en Sakaar, Hulk regresa a la Tierra con una furia incontrolable.",
        "hashtags": "#WorldWarHulk #Hulk #MarvelComics #Illuminati #ComicsNarrados #Reels",
        "scenes": [
            "Traicionado y exiliado al espacio por los Illuminati, Hulk conquistó el planeta Sakaar, convirtiéndose en rey y encontrando al fin la paz junto a su reina.",
            "Pero la nave en que lo enviaron explotó, aniquilando a millones de inocentes y matando a su esposa embarazada; en ese instante nació el Hulk Rompemundos.",
            "Acompañado por su armada alienígena de Warbound, Hulk aterrizó en la Luna y destrozó a Black Bolt con una furia salvaje que estremeció el espacio.",
            "Al llegar a Manhattan, pulverizó la armadura Hulkbuster de Iron Man, derribó la Torre Stark y humilló a Reed Richards en el corazón de su laboratorio.",
            "Convirtió el Madison Square Garden en un coliseo de gladiadores, obligando a los héroes que lo traicionaron a combatir a muerte por sus vidas.",
            "Solo el poder supremo de Sentry, equivalente a un millón de soles explotando, pudo contener la radiación gamma antes de que Hulk partiera el continente en dos."
        ]
    },
    {
        "id": "civil_war_caida_heroes",
        "character": "Captain America",
        "title": "Civil War: La Trágica Caída de los Héroes",
        "theme_signature": "marvel:civil_war:ironman_vs_cap",
        "description": "La tragedia de Stamford divide a la comunidad superheroica: Iron Man y el Capitán América enfrentados a muerte por el Acta de Registro.",
        "hashtags": "#CivilWar #CaptainAmerica #IronMan #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Cuando una explosión provocada por villanos en Stamford arrebató la vida a seiscientos civiles inocentes, el gobierno exigió el Acta de Registro de Superhumanos.",
            "Iron Man apoyó la ley por el bien de la seguridad nacional, pero el Capitán América se negó a comprometer la libertad individual, convirtiéndose en fugitivo.",
            "La comunidad superheroica se fracturó en dos bandos irreconciliables, transformando a antiguos hermanos de armas en feroces enemigos en combate.",
            "Peter Parker reveló su identidad secreta al mundo en televisión para apoyar a Stark, desatando una cacería implacable contra sus seres más queridos.",
            "En las calles de Nueva York, Iron Man y el Capitán América libraron un duelo a muerte brutal donde sus armaduras y escudos terminaron destrozados.",
            "Al ver el terror en los ojos de los ciudadanos que juró proteger, Steve Rogers bajó la guardia y se rindió, pagando el precio definitivo de la guerra."
        ]
    },
    {
        "id": "blackest_night_rebelion",
        "character": "Green Lantern",
        "title": "Blackest Night: La Rebelión de los Muertos",
        "theme_signature": "green_lantern:blackest_night:nekron",
        "description": "La profecía más oscura de los Guardianes se cumple: anillos negros resucitan a héroes y villanos caídos como zombis cósmicos insaciables.",
        "hashtags": "#BlackestNight #GreenLantern #DCComics #Nekron #ComicsNarrados #Reels",
        "scenes": [
            "La profecía milenaria de la Noche más Oscura se cumplió cuando millones de anillos negros descendieron sobre el universo desde el abismo de Nekron.",
            "Héroes y villanos caídos regresaron de la tumba convertidos en Black Lanterns, consumiendo las emociones de sus antiguos seres queridos con horror indescriptible.",
            "Hal Jordan y los Green Lanterns vieron cómo amigos legendarios como Martian Manhunter y Superman resurgían como monstruos sin piedad.",
            "La Tierra se convirtió en el epicentro de la muerte cuando la batería de poder negra brotó en Coast City, amenazando con extinguir la vida cósmica.",
            "Para detener la marea fúnebre, los líderes de los siete cuerpos emocionales tuvieron que unir sus luces y canalizar la Entidad Blanca de la Creación.",
            "La luz blanca de la vida triunfó sobre el vacío eterno de Nekron, resucitando a doce héroes y restaurando la esperanza en el multiverso."
        ]
    },
    {
        "id": "secret_wars_dios_doom",
        "character": "Doctor Doom",
        "title": "Secret Wars: Dios Emperor Doom y el Fin del Multiverso",
        "theme_signature": "doctor_doom:secret_wars:god_emperor",
        "description": "Las incursiones colapsan el multiverso Marvel. De los restos del cosmos, Victor Von Doom forja Battleworld y reina como dios supremo omnipotente.",
        "hashtags": "#DoctorDoom #SecretWars #MarvelComics #GodEmperorDoom #ComicsNarrados #Reels",
        "scenes": [
            "Las incursiones dimensionales colapsaron cada realidad del multiverso hasta que solo quedaron cenizas flotando en el vacío infinito.",
            "En el último instante de la existencia, Victor Von Doom robó el poder omnipotente de los Beyonders y salvó los fragmentos restantes del cosmos.",
            "De esas ruinas forjó Battleworld, un planeta mosaico donde Doom fue venerado como emperador supremo y dios creador absoluto.",
            "Con Stephen Strange como su sheriff místico y un ejército de Thors patrullando los cielos, nadie se atrevía a cuestionar la voluntad de hierro de Doom.",
            "Pero un puñado de supervivientes de la Tierra original emergió de una balsa salvavidas, liderados por Reed Richards, para derrocar al falso creador.",
            "En su duelo final, Doom admitió que Reed habría sido un mejor dios, entregando la chispa que restauró el multiverso infinito para siempre."
        ]
    },
    {
        "id": "flashpoint_paradoja",
        "character": "The Flash",
        "title": "Flashpoint: La Paradoja que Destruyó el Mundo",
        "theme_signature": "flash:flashpoint:thomas_wayne_batman",
        "description": "Barry Allen viaja al pasado para salvar a su madre y despierta en una pesadilla donde Atlantis y Temiscira destruyen el planeta.",
        "hashtags": "#Flashpoint #TheFlash #Batman #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Desesperado por cambiar su destino, Barry Allen corrió hacia el pasado para evitar el asesinato de su madre, fracturando la corriente temporal.",
            "Despertó sin poderes en un mundo de pesadilla donde Bruce Wayne murió en el callejón, convirtiendo a su padre Thomas Wayne en un Batman letal.",
            "Devastada por la pérdida de su hijo, Martha Wayne cayó en la locura absoluta, cortándose el rostro para convertirse en el Joker de esa realidad.",
            "Atlantis y Temiscira libraban una guerra global apocalíptica, sumergiendo a Europa bajo el océano con millones de bajas inocentes.",
            "Thomas Wayne ayudó a Barry a recuperar su velocidad mediante un rayo directo, sacrificando su vida para permitirle corregir la línea temporal.",
            "Antes de desvanecerse en la Speed Force, Thomas le entregó a Barry una carta de despedida para Bruce, uniendo a padre e hijo a través del multiverso."
        ]
    },
    {
        "id": "killing_joke_broma_asesina",
        "character": "Joker",
        "title": "Batman: La Broma Asesina (The Killing Joke)",
        "theme_signature": "joker:killing_joke:un_mal_dia",
        "description": "El Joker intenta demostrar que solo se necesita un mal día para que el hombre más cuerdo caiga en la locura.",
        "hashtags": "#TheKillingJoke #Batman #Joker #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Escapando de Arkham una vez más, el Joker se propuso demostrar su más retorcida teoría: la cordura humana es un frágil castillo de naipes.",
            "Llegó al departamento de Barbara Gordon y le disparó a quemarropa en la columna vertebral, dejándola paralizada para siempre.",
            "Secuestró al Comisionado Gordon llevándolo a un parque de diversiones abandonado, sometiéndolo a horrores psicológicos para quebrar su razón.",
            "A pesar de la tortura demencial, Gordon se mantuvo íntegro, exigiendo a Batman que capturara al payaso respetando la ley.",
            "Batman acorraló al Joker en la sala de espejos, ofreciéndole una última oportunidad genuina de rehabilitación y redención.",
            "El payaso rechazó la oferta con un trágico chiste sobre dos lunáticos, y bajo la lluvia torrencial, ambos compartieron una risa estremecedora."
        ]
    },
    {
        "id": "red_hood_capucha_roja",
        "character": "Red Hood",
        "title": "Batman: Bajo la Capucha Roja - El Regreso de Jason Todd",
        "theme_signature": "batman:red_hood:regreso_jason_todd",
        "description": "El segundo Robin, asesinado a golpes por el Joker, regresa como el implacable vigilante Red Hood para cobrar venganza de Batman.",
        "hashtags": "#RedHood #Batman #JasonTodd #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Un nuevo señor del crimen apareció en Gotham City, tomando el control del bajo mundo con tácticas militares despiadadas bajo el nombre de Red Hood.",
            "Batman persiguió al misterioso vigilante por los tejados, sorprendido por su dominio íntimo del arsenal y los estilos de combate de Wayne Enterprises.",
            "Durante una persecución brutal, Red Hood se quitó el casco revelando lo impensable: Jason Todd, el segundo Robin que murió a manos del Joker.",
            "Jason arrastró a Bruce hasta un apartamento donde tenía al Joker atado a una silla ensangrentada junto a una palanca de hierro.",
            "Con lágrimas de rabia en los ojos, Jason obligó a Batman a elegir: ejecutar al Joker para vengar su muerte o ver cómo Jason apretaba el gatillo.",
            "Negándose a cruzar su código moral, Batman desarmó a Jason con un batarang mientras una bomba detonaba, desvaneciendo a Red Hood entre el humo."
        ]
    },
    {
        "id": "franklin_richards_creador",
        "character": "Franklin Richards",
        "title": "Franklin Richards: El Niño que Crea Universos",
        "theme_signature": "franklin_richards:celestials:creador_multiverso",
        "description": "El hijo mutante de Reed Richards y Sue Storm, poseedor de un poder de alteración de la realidad que asombra a los Celestiales.",
        "hashtags": "#FranklinRichards #FantasticFour #Galactus #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Nacido de la unión entre Reed Richards y Sue Storm, Franklin Richards demostró desde su infancia un poder que sobrepasaba a los dioses cósmicos.",
            "Clasificado como un mutante de nivel Omega más allá de cualquier escala, su mente infantil era capaz de crear universos enteros en su bolsillo.",
            "Cuando los Celestiales Oscuros invadieron la Tierra para erradicar la realidad, Franklin adulto viajó en el tiempo para apoyar a su familia.",
            "Canalizando la energía cósmica de su versión infantil, resucitó a Galactus y lo convirtió en su propio heraldo leal para la batalla final.",
            "El devorador de mundos luchó codo a codo junto al niño mutante, derrotando a los titanes cósmicos en un espectáculo de poder divino.",
            "Franklin Richards consolidó su legado como el mortal más poderoso del universo Marvel, el arquitecto supremo de la nueva creación."
        ]
    },
    {
        "id": "thanos_wins_fin_existencia",
        "character": "Thanos",
        "title": "Thanos Wins: El Fin de Toda la Existencia",
        "theme_signature": "thanos:thanos_wins:rey_thanos_fin",
        "description": "En el final de los tiempos, un anciano Rey Thanos ha masacrado a cada héroe y dios cósmico, esperando su última petición a la Muerte.",
        "hashtags": "#Thanos #ThanosWins #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Millones de años en el futuro, el Titán Loco finalmente triunfó: cada estrella se apagó y cada héroe y dios cósmico fue aniquilado.",
            "Coronado como el Rey Thanos en un trono forjado con los huesos de los Celestiales, gobernaba sobre un páramo desértico y silencioso.",
            "Mantenía a Hulk encadenado en las mazmorras como su mascota salvaje, alimentándolo con los restos de sus antiguos aliados.",
            "Utilizando el poder místico de Cosmic Ghost Rider y el fragmento del Tiempo, trajo a su versión joven al final de los tiempos.",
            "El anciano Thanos no deseaba pelear, sino una última petición: necesitaba que su yo joven lo asesinara para reunirse al fin con su amada Muerte.",
            "Horrorizado por ver en qué patético monstruo se convertiría, el joven Thanos rechazó ese futuro y regresó a su época para alterar su destino."
        ]
    },
    {
        "id": "dark_nights_metal",
        "character": "Batman",
        "title": "Dark Nights Metal: La Invasión del Multiverso Oscuro",
        "theme_signature": "dc:dark_nights_metal:barbatos_caballeros",
        "description": "El dios demonio Barbatos desata a los Caballeros Oscuros: versiones corrompidas de Batman con los poderes de la Liga de la Justicia.",
        "hashtags": "#DarkNightsMetal #Batman #DCComics #Barbatos #ComicsNarrados #Reels",
        "scenes": [
            "Cinco metales místicos abrieron el portal hacia el abismo del Multiverso Oscuro, permitiendo la llegada del dios murciélago Barbatos a la Tierra.",
            "Siete versiones corrompidas de Batman invadieron Gotham City, cada una portando las habilidades robadas de los miembros de la Liga de la Justicia.",
            "El Red Death fusionó a Batman con la velocidad de Flash, mientras The Drowned ahogaba continentes enteros con aguas abisales mutadas.",
            "Los héroes de DC cayeron derrotados uno a uno ante la brutalidad estratégica de pesadilla de sus propios dobles oscuros.",
            "Para revertir el colapso del multiverso, Batman y Superman viajaron al núcleo de la creación para obtener el legendario Décimo Metal.",
            "Armados con la armadura pura de la chispa vital, la Liga de la Justicia disipó la oscuridad de Barbatos y restauró la luz cósmica."
        ]
    },
    {
        "id": "muerte_superman",
        "character": "Superman",
        "title": "La Muerte de Superman: El Sacrificio Final ante Doomsday",
        "theme_signature": "superman:doomsday:muerte_sacrificio",
        "description": "Doomsday arrasa con la Liga de la Justicia. En las calles de Metrópolis, Superman entrega su vida en el combate más desgarrador de los cómics.",
        "hashtags": "#LaMuerteDeSuperman #Doomsday #Superman #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "De las entrañas de la Tierra emergió una fuerza de destrucción imparable: Doomsday, una bestia prehistórica con un odio ciego hacia toda forma de vida.",
            "La Liga de la Justicia intentó contener su paso arrollador, pero cayeron mutilados y derrotados en cuestión de minutos ante sus puños de hueso.",
            "Solo Superman pudo interponerse entre el monstruo y la aniquilación de Metrópolis, librando una batalla titánica que destrozó cuadras enteras.",
            "Cada golpe intercambiado entre ambos colosos generaba ondas de choque sísmicas que retumbaban por toda la costa este.",
            "Con su capa desgarrada y su sangre tiñendo el asfalto, Clark concentró toda su energía solar en un último y devastador puñetazo.",
            "Ambos colosos cayeron sin vida simultáneamente; en los brazos de Lois Lane, el héroe más grande del mundo exhaló su último aliento."
        ]
    },
    {
        "id": "old_man_logan",
        "character": "Wolverine",
        "title": "Wolverine: Old Man Logan - La Masacre de los X-Men",
        "theme_signature": "wolverine:old_man_logan:engano_mysterio",
        "description": "El truco mental de Mysterio que obligó a Wolverine a matar a todos sus compañeros mutantes en la Mansión X.",
        "hashtags": "#OldManLogan #Wolverine #MarvelComics #XMen #ComicsNarrados #Reels",
        "scenes": [
            "Cincuenta años después de la caída de los héroes, los Estados Unidos se convirtieron en un páramo desolado gobernado por villanos despiadados.",
            "Wolverine se convirtió en un anciano pacifista que se negaba a sacar sus garras de adamantium, atormentado por un secreto inconfesable.",
            "La noche en que todo cambió, una horda de supervillanos asaltó la Mansión X; Logan peleó a muerte para proteger a los jóvenes estudiantes.",
            "Al degollar al último atacante, el humo verde de las ilusiones se disipó: Mysterio había engañado sus sentidos y olfato por completo.",
            "A sus pies yacían los cadáveres destrozados de Cíclope, Jean Grey y todos los X-Men, asesinados por sus propias garras de adamantium.",
            "Roto por la culpa, Logan apoyó la cabeza en las vías del tren esperando la muerte, jurando no volver a derramar una sola gota de sangre."
        ]
    },
    {
        "id": "muerte_gwen_stacy",
        "character": "Spider-Man",
        "title": "Spider-Man: La Trágica Noche en que Murió Gwen Stacy",
        "theme_signature": "spiderman:gwen_stacy:duende_verde_puente",
        "description": "El Duende Verde descubre la identidad de Peter Parker y lanza a Gwen Stacy desde lo alto del puente George Washington.",
        "hashtags": "#SpiderMan #GwenStacy #GreenGoblin #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Al descubrir que Peter Parker era Spider-Man, Norman Osborn perdió los últimos vestigios de cordura bajo la máscara del Duende Verde.",
            "Secuestró a Gwen Stacy, el gran amor de Peter, y la llevó a la cima del puente George Washington para tenderle una emboscada mortal.",
            "En medio del feroz combate aéreo en las alturas, el Duende arrojó a Gwen al vacío hacia las gélidas aguas del río Hudson.",
            "Desesperado, Peter disparó su telaraña atrapándola justo a tiempo antes de estrellarse contra la superficie.",
            "Pero al levantarla entre sus brazos, el chasquido del látigo cervical había quebrado su cuello al detener la caída de golpe.",
            "Esa noche marcó el fin de la inocencia de los cómics y forjó el alma de Spider-Man con el dolor más amargo de su existencia."
        ]
    },
    {
        "id": "superboy_prime",
        "character": "Superboy Prime",
        "title": "Superboy Prime: El Destructor de la Realidad",
        "theme_signature": "superboy_prime:infinite_crisis:golpe_realidad",
        "description": "El héroe de la Tierra Primordial cuya frustración y locura quebraron las barreras mismas del espacio y el tiempo.",
        "hashtags": "#SuperboyPrime #DCComics #InfiniteCrisis #ComicsNarrados #Reels",
        "scenes": [
            "Originario de la Tierra Primordial donde los cómics eran solo ficción, Clark Kent descubrió que él era el único ser con poderes reales.",
            "Tras ayudar a salvar el multiverso en la primera Crisis, fue confinado a una dimensión paraíso donde observaba la corrupción de los nuevos héroes.",
            "Consumido por la envidia y la rabia, comenzó a golpear la barrera de cristal de la realidad con sus puños kriptonianos indestructibles.",
            "Cada golpe sísmico alteró la historia del universo DC: revivió a Jason Todd, cambió orígenes y reescribió la continuidad cósmica.",
            "Al liberarse en Infinite Crisis, masacró a decenas de Jóvenes Titanes y héroes legendarios con una furia infantil desquiciada.",
            "Superboy Prime demostró ser la pesadilla definitiva: un dios con el poder ilimitado de la Edad de Plata y la inmadurez de un niño furioso."
        ]
    },
    {
        "id": "torre_de_babel",
        "character": "Batman",
        "title": "Batman: Torre de Babel y los Planes de Contingencia",
        "theme_signature": "batman:torre_de_babel:planes_contingencia",
        "description": "Ra's al Ghul roba los archivos secretos de Batman diseñados para neutralizar a cada miembro de la Liga de la Justicia.",
        "hashtags": "#TorreDeBabel #Batman #JusticeLeague #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Por años, la paranoia táctica de Batman lo llevó a diseñar protocolos secretos para incapacitar a cada miembro de la Liga de la Justicia.",
            "El villano inmortal Ra's al Ghul hackeó la computadora de la Baticueva y robó cada uno de los planes para ejecutar su plan maestro.",
            "Superman fue expuesto a kriptonita roja sintetizada por Bruce que volvía su piel transparente y sobrecargaba sus células solares de agonía.",
            "Flash fue impactado por una bala vibratoria que provocaba convulsiones a la velocidad de la luz, mientras Wonder Woman peleaba con una ilusión eterna.",
            "Los héroes cayeron uno tras otro neutralizados por la mente de su propio líder táctico sin comprender quién los atacaba.",
            "Aunque Batman logró salvar el día, la Liga de la Justicia votó su expulsión inmediata, destruyendo la confianza en el Caballero de la Noche."
        ]
    },
    {
        "id": "cosmic_ghost_rider",
        "character": "Cosmic Ghost Rider",
        "title": "Cosmic Ghost Rider: El Castigador del Infinito",
        "theme_signature": "cosmic_ghost_rider:frank_castle:galactus_thanos",
        "description": "Frank Castle muere, hace un pacto con Mephisto, se convierte en heraldo de Galactus y finalmente en sirviente del Rey Thanos.",
        "hashtags": "#CosmicGhostRider #Punisher #MarvelComics #Galactus #ComicsNarrados #Reels",
        "scenes": [
            "Durante la última invasión de Thanos a la Tierra, Frank Castle murió aplastado por los escombros de un rascacielos.",
            "En el infierno, desesperado por cobrar venganza, hizo un pacto con Mephisto para convertirse en el nuevo Ghost Rider del planeta desierto.",
            "Al quedar solo en un mundo muerto durante siglos, Galactus llegó herido buscando un heraldo; Frank aceptó el Poder Cósmico.",
            "Transformado en el Cosmic Ghost Rider, combinó el Fuego del Infierno con la energía cósmica de las estrellas en una mezcla demencial.",
            "Junto a Galactus batalló contra Thanos, pero el titán decapitó al devorador y le ofreció a Frank unirse a su corte imperial.",
            "Con una locura desbordante y una mirada de penitencia cósmica, Frank Castle se convirtió en el sirviente más letal del fin del universo."
        ]
    },
    {
        "id": "crisis_tierras_infinitas",
        "character": "The Flash",
        "title": "Crisis en Tierras Infinitas: El Sacrificio de los Héroes",
        "theme_signature": "dc:crisis_tierras_infinitas:sacrificio_barry_allen",
        "description": "El Antimonitor devora universos con antimateria. Barry Allen corre más rápido que la luz y da su vida para salvar la creación.",
        "hashtags": "#CrisisEnTierrasInfinitas #TheFlash #Supergirl #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Una ola gigantesca de antimateria se propagó por el multiverso, devorando miles de tierras paralelas y millones de vidas inocentes.",
            "El dios de la destrucción cósmica, el Antimonitor, preparó un cañón de antimateria en el corazón del universo de Qward para erradicar la realidad.",
            "Supergirl fue la primera en sacrificar su vida arremetiendo contra el coloso para darle tiempo a Superman de escapar.",
            "Barry Allen escapó de su prisión y corrió a velocidades jamás alcanzadas alrededor del núcleo del cañón de energía.",
            "Corrió tan rápido que su cuerpo físico comenzó a desintegrarse átomo por átomo, disolviendo el cañón en la corriente temporal.",
            "Barry se desvaneció con una sonrisa en el rostro, salvando a todo el multiverso y convirtiéndose en la leyenda máxima del heroísmo."
        ]
    },
    {
        "id": "marvel_zombies",
        "character": "Spider-Man",
        "title": "Marvel Zombies: El Hambre del Multiverso",
        "theme_signature": "marvel_zombies:hambre_infinita:galactus_devorado",
        "description": "Un virus alienígena infecta a los Vengadores, convirtiendo a los protectores del mundo en monstruos caníbales insaciables.",
        "hashtags": "#MarvelZombies #SpiderMan #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Un destello en el cielo de Nueva York trajo un virus alienígena imparable que infectó a los héroes más poderosos del planeta.",
            "Los Vengadores mantuvieron su inteligencia y habilidades sobrehumanas, pero consumidos por un hambre caníbal insaciable de carne viva.",
            "Spider-Man devoró a la Tía May y a Mary Jane en un ataque de desesperación, quedando sumido en un tormento de culpa eterna.",
            "En cuestión de días, la población entera de la Tierra fue devorada hasta que no quedó ningún ser vivo en el continente.",
            "Cuando Silver Surfer y Galactus llegaron para consumir el mundo, los héroes zombis los atacaron en jorda y devoraron al dios cósmico.",
            "Al absorber el Poder Cósmico de Galactus, los Vengadores zombis surcaron las estrellas para devorar civilizaciones enteras en el cosmos."
        ]
    },
    {
        "id": "robo_del_mysterium",
        "character": "Iron Man",
        "title": "El Robo del Mysterium: Tony Stark y Emma Frost",
        "theme_signature": "ironman:mysterium:emma_frost_fall_of_x",
        "description": "Durante Fall of X, Tony Stark y Emma Frost unen fuerzas para infiltrarse en las bóvedas de Orchis y forjar la armadura definitiva.",
        "hashtags": "#IronMan #EmmaFrost #FallOfX #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "Con la nación mutante de Krakoa destruida por la organización Orchis, los supervivientes se dispersaron perseguidos por Centinelas Stark.",
            "Despojado de su compañía y de su dinero, Tony Stark juró destruir a Feilong y detener el genocidio mutante a toda costa.",
            "Bajo la identidad clandestina de Hazel Kendal, Emma Frost se alió en matrimonio estratégico con Tony para coordinar la resistencia.",
            "Juntos planearon una infiltración de alto riesgo en las bóvedas más protegidas para robar un cargamento de Mysterium puro.",
            "El Mysterium, un metal milagroso inmune a la magia y más resistente que el adamantium, fue la clave para la salvación.",
            "En las forjas secretas de Stark nació la Mark 72, la armadura de Mysterium diseñada para destrozar al ejército de Centinelas."
        ]
    },
    {
        "id": "batman_corte_de_los_buhos",
        "character": "Batman",
        "title": "Batman: La Corte de los Búhos - El Laberinto de Gotham",
        "theme_signature": "batman:court_of_owls:talon_laberinto",
        "description": "Batman descubre una sociedad milenaria que ha gobernado Gotham en secreto y es arrojado a un laberinto subterráneo mortal.",
        "hashtags": "#LaCorteDeLosBuhos #Batman #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "Durante generaciones, una canción de cuna advertía sobre la Corte de los Búhos, una élite secreta que gobernaba Gotham desde las sombras.",
            "Bruce Wayne siempre lo consideró un mito urbano, hasta que un asesino inmortal llamado Talon intentó ejecutarlo públicamente.",
            "Al investigar sus guaridas subterráneas, Batman cayó en un gigantesco laberinto de piedra oculto bajo los cimientos de la ciudad.",
            "Encerrado durante ocho días tortuosos sin comida ni agua, la mente de Bruce comenzó a fragmentarse bajo la mirada burlona de las máscaras.",
            "A punto de ser ejecutado por los garras, Batman desató la furia salvaje de su determinación, derrotando a decenas de asesinos inmortales.",
            "De regreso a la Mansión Wayne, se enfundó en una armadura mecanizada pesada para librar la batalla total por el alma de Gotham."
        ]
    }
]


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [CloudRunner-ES] {msg}", flush=True)


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


def is_duplicate(story: dict, ledger: list[dict]) -> tuple[bool, str]:
    story_id = story.get("id", "").lower()
    story_theme = story.get("theme_signature", "").lower()
    story_title = story.get("title", "").lower()

    for item in ledger:
        item_id = item.get("id", "").lower()
        item_theme = item.get("theme_signature", "").lower()
        item_title = item.get("title", "").lower()

        if story_id and item_id and story_id == item_id:
            return True, f"Duplicate ID: Story '{story_id}' was already produced on {item.get('date', 'past')}"
        if story_theme and item_theme and story_theme == item_theme:
            return True, f"Duplicate Theme: Theme '{story_theme}' was already covered by '{item.get('title')}'"
        if story_title and item_title and story_title == item_title:
            return True, f"Duplicate Title: Exact title '{story_title}' already exists in ledger"

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
                    import io
                    im = Image.open(io.BytesIO(r.content)).convert('RGB')
                    target_w, target_h = 1080, 1920
                    scale = max(target_w / im.width, target_h / im.height)
                    nw, nh = max(target_w, int(im.width * scale)), max(target_h, int(im.height * scale))
                    im_resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
                    left = (nw - target_w) // 2
                    top = (nh - target_h) // 2
                    im_cropped = im_resized.crop((left, top, left + target_w, top + target_h))
                    im_cropped.save(img_file, quality=92)
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
    parser = argparse.ArgumentParser(description="Comic Lore Vault Autonomous Cloud Generation & Publisher (Spanish)")
    parser.add_argument("--story-id", type=str, help="Specific story ID to generate")
    parser.add_argument("--publish", action="store_true", help="Auto-publish to FB Page and IG after generation")
    parser.add_argument("--draft", action="store_true", help="Save as unpublished draft on FB and skip public IG")
    parser.add_argument("--dry-run", action="store_true", help="Test workflow without video generation or publishing")
    args = parser.parse_args()

    log("Initializing Spanish Comic Video Engine with Anti-Duplication Protection...")
    log(f"Branch: spanish-videos")
    log(f"FB Page ID: {os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)}")
    log(f"IG Account ID: {os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)}")

    ledger = load_ledger()
    log(f"Historical Ledger: {len(ledger)} previously produced videos registered.")

    # Story Selection & Anti-Duplication Verification
    if args.story_id and args.story_id != "any":
        selected = next((s for s in EDITORIAL_STORIES if s["id"] == args.story_id), None)
        if not selected:
            log(f"Error: Story ID '{args.story_id}' not found in catalog.")
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
            log("All cataloged stories have been produced! No duplicates permitted.")
            log("Add new storylines to EDITORIAL_STORIES before running next production.")
            sys.exit(0)

        selected = random.choice(available)

    log(f"Selected Unique Story: {selected['title']} (ID: {selected['id']})")

    if args.dry_run:
        log("DRY RUN mode enabled. Verification successful. Exiting without render.")
        sys.exit(0)

    work_dir = Path("scratch_cloud_gen")
    work_dir.mkdir(parents=True, exist_ok=True)
    generation = build_cloud_generation(selected, work_dir)

    output_root = Path("output")
    output_root.mkdir(parents=True, exist_ok=True)

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
