"""
Master Production Engine: Batch 5 (Slots 41 al 50 - 10 Videos Inéditos Calibrados)
=============================================================================
Requisitos estrictos del usuario:
1. "se debe mostrar lo que se narra de manera muy precisa" -> Paneles canónicos 1:1.
2. Duración >= 60.0s (calibrada a ~205-210 palabras, 74s-78s de video).
3. Cero duplicados contra los 25,306 registros históricos del canal.
4. Cero Marvel Zombies.
5. Salida en scheduled_queue/41_... a scheduled_queue/50_... (video.mp4, thumb.jpg, metadata.json).
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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_5_inéditos"
PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)

PROJECTS = [
    {
        "slot": 41,
        "queue_folder": "41_superman_black_mercy_mongul",
        "id": "superman_black_mercy_mongul",
        "title": "¡La Mayor Crueldad Contra Superman! La Falsa Vida en Krypton que le Rompió el Corazón ☀️🥀💔",
        "character": "Superman",
        "folder": "41_superman_black_mercy_mongul",
        "theme_signature": "superman:annual_11:black_mercy_van_el",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La tortura psicológica más desgarradora que ha sufrido el Hombre de Acero en toda la historia de DC Comics! En el día de su cumpleaños, Batman, Robin y Wonder Woman llegaron a la solitaria Fortaleza de la Soledad para celebrar, solo para encontrar a Superman completamente paralizado y atrapado por una enredadera alienígena."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "El tirano cósmico Mongul le había colocado en el pecho la Clemencia Negra, una planta parasitaria que sume a su víctima en una ilusión perfecta de su mayor deseo. En su mente, Clark vivía una vida pacífica en un planeta Krypton que jamás explotó, felizmente casado y criando a su pequeño hijo Van-El."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero cuando las anomalías del sueño comenzaron a fracturar la fantasía, Superman comprendió con horror que su amada familia no era real. Con lágrimas quemándole el rostro, Clark tuvo que abrazar a su hijo mientras el pequeño le suplicaba que no lo dejara morir, viendo cómo su niño se desvanecía en la nada."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Despertando con los ojos inyectados en fuego solar y una furia asesina como el universo jamás había visto, Superman arrancó el parásito de su carne y se abalanzó salvajemente contra Mongul, demostrando que arrebatarle el sueño de su familia fue el error más peligroso y letal que el tirano pudo cometer."
            }
        ],
        "description": "La legendaria obra maestra de Alan Moore y Dave Gibbons: Superman Annual #11 'Para el hombre que lo tiene todo'. La desgarradora pérdida de Van-El.",
        "hashtags": "#Superman #AlanMoore #DCComics #Mongul #BlackMercy #Krypton #Comics #Shorts #Reels"
    },
    {
        "slot": 42,
        "queue_folder": "42_doctor_strange_the_oath_cirugia",
        "id": "doctor_strange_the_oath_cirugia",
        "title": "¡Doctor Strange se Operó a Sí Mismo en Forma Astral! La Balacera en el Sanctum 🔮🫀🏥",
        "character": "Doctor Strange",
        "folder": "42_doctor_strange_the_oath_cirugia",
        "theme_signature": "doctor_strange:the_oath:astral_surgery_night_nurse",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El Hechicero Supremo de Marvel enfrentó a la mismísima muerte utilizando sus dos grandes vocaciones: la magia mística y la medicina de urgencia! Tras sufrir una misteriosa emboscada dentro del Sanctum Sanctorum, Stephen Strange recibió un disparo a quemarropa con una letal bala de plata encantada directamente en el centro del pecho."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Su fiel sirviente Wong trasladó su cuerpo ensangrentado a la clínica secreta de Night Nurse, la enfermera clandestina de los superhéroes. Con la bala alojada peligrosamente junto al pericardio y los monitores cardíacos marcando un paro inminente, el pulso del hechicero se detuvo por completo sobre la fría mesa de operaciones."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Negándose a cruzar al más allá, Stephen proyectó su forma astral luminosa fuera de su carne sin vida. Flotando como un espectro etéreo sobre su propio cadáver abierto, Strange comenzó a dictar instrucciones quirúrgicas precisas a Linda Carter, guiando con calma milimétrica el bisturí para evitar que una hemorragia masiva fuera irreversible."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Al mismo tiempo que combatía a los demonios espirituales que acechaban para devorar su alma desprotegida, la enfermera logró extraer el proyectil maldito con las pinzas, permitiendo que el corazón de Strange volviera a latir y demostrando que su juramento hipocrático de salvar vidas prevalecerá incluso sobre su propia muerte física."
            }
        ],
        "description": "La brillante historia de Brian K. Vaughan y Marcos Martín: Doctor Strange: The Oath. La cirugía astral más impactante de Marvel.",
        "hashtags": "#DoctorStrange #NightNurse #Marvel #MarvelComics #HechiceroSupremo #TheOath #Comics #Shorts #Reels"
    },
    {
        "slot": 43,
        "queue_folder": "43_flashpoint_carta_thomas_wayne",
        "id": "flashpoint_carta_thomas_wayne",
        "title": "¡El Día que Batman Lloró Desconsoladamente! La Última Carta de Thomas Wayne a su Hijo 🦇📜💧",
        "character": "Batman",
        "folder": "43_flashpoint_carta_thomas_wayne",
        "theme_signature": "batman:flashpoint_5:thomas_wayne_letter_bruce",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El instante más conmovedor y humano en la legendaria historia de Batman donde el justiciero más frío de Gotham City se quebró en llanto! En la brutal línea temporal alternativa de Flashpoint, Thomas Wayne se convirtió en un sanguinario Caballero Oscuro tras presenciar cómo el pequeño Bruce era asesinado en el callejón."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Para restaurar la realidad original y permitir que su hijo viva aunque él deba desaparecer para siempre, Thomas luchó con ferocidad suicida hasta quedar herido de muerte. Mientras el universo colapsaba en una cegadora luz blanca, el padre agonizante escribió apresuradamente una carta de despedida a lápiz y se la confió a Flash."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Corriendo a través de la corriente temporal hacia el universo reconstruido, Barry Allen llegó exhausto a la Baticueva. Ante la mirada atónita de Bruce Wayne, Flash extendió el sobre arrugado y manchado de sangre, revelándole que un hombre extraordinario en un mundo moribundo le había enviado un último mensaje directo del corazón."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con manos temblorosas, Bruce leyó las palabras de su padre diciéndole que era el mejor regalo que la vida le dio y rogándole que encontrara la felicidad. Una solitaria lágrima rodó por la máscara del héroe, quien conmovido susurró un sincero agradecimiento a Barry por haberle devuelto la voz de su padre."
            }
        ],
        "description": "El inolvidable final de Flashpoint #5 por Geoff Johns y Andy Kubert. La emotiva carta de Thomas Wayne a Bruce.",
        "hashtags": "#Batman #Flashpoint #ThomasWayne #TheFlash #DCComics #BruceWayne #BarryAllen #Comics #Shorts #Reels"
    },
    {
        "slot": 44,
        "queue_folder": "44_punisher_the_end_bunker",
        "id": "punisher_the_end_bunker",
        "title": "¡El Fin del Mundo No Detuvo a Punisher! La Última Ejecución de Frank Castle en las Cenizas Radiactivas 💀☢️🔥",
        "character": "The Punisher",
        "folder": "44_punisher_the_end_bunker",
        "theme_signature": "punisher:the_end_1:nuclear_bunker_execution",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La última y más sombría misión de Frank Castle en un mundo devastado donde la civilización humana colapsó en cenizas nucleares! En la aclamada obra Punisher The End, la Tercera Guerra Mundial aniquiló a casi toda la población del planeta, dejando a un anciano y enfermo Frank Castle deambulando por las ruinas de Manhattan."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Tosiendo sangre y consumido lentamente por la radiación ambiental, Punisher descendió a las profundidades de un refugio atómico militar blindado. Allí se ocultaba la élite corrupta de políticos, magnates y banqueros que financiaron y orquestaron el holocausto atómico, disfrutando de comodidades artificiales mientras millones de personas inocentes ardieron en la superficie."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Al ver entrar al veterano armado, los magnates cayeron de rodillas llorando y suplicando piedad. Argumentaron con arrogancia que ellos eran los últimos seres humanos fértiles con el conocimiento necesario para reconstruir la civilización, afirmando que si Frank los ejecutaba, la raza humana se extinguiría para siempre de la faz de la Tierra."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Mirándolos con frío desprecio, Punisher cargó su rifle y respondió con voz de acero que una especie capaz de destruir su propio hogar no merecía una segunda oportunidad. Frank abrió fuego masivo sin dudar un segundo, selló el búnker para siempre y salió a caminar bajo la nieve atómica esperando su pacífico final."
            }
        ],
        "description": "La desgarradora novela gráfica de Garth Ennis y Richard Corben: Punisher: The End. El castigo final tras el fin del mundo.",
        "hashtags": "#Punisher #FrankCastle #MarvelMAX #GarthEnnis #Marvel #MarvelComics #PostApocalyptic #Comics #Shorts #Reels"
    },
    {
        "slot": 45,
        "queue_folder": "45_annihilation_drax_thanos_corazon",
        "id": "annihilation_drax_thanos_corazon",
        "title": "¡Drax le Arrancó el Corazón a Thanos con la Mano Desnuda! La Muerte Más Brutal del Titán Loco 🖤👊🩸",
        "character": "Drax the Destroyer",
        "folder": "45_annihilation_drax_thanos_corazon",
        "theme_signature": "drax:annihilation_4:thanos_heart_ripped",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El momento más brutal y sanguinario en toda la historia cósmica de Marvel donde el villano más temido del multiverso fue ejecutado sin piedad! Durante la masacre masiva de la Guerra de Aniquilación, el Titán Loco Thanos se alió inicialmente con Annihilus para estudiar la imparable fuerza destructiva de la Zona Negativa."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Sin embargo, al descubrir que el verdadero plan de Annihilus era extinguir toda la vida del cosmos incluyendo a la Muerte misma, Thanos comprendió la magnitud de su error. El Titán corrió hacia la consola de control para liberar al prisionero Galactus y permitir que el devorador de mundos destruyera a la armada invasora."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Justo cuando Thanos extendió la mano para desactivar los grilletes estelares, una sombra imparable emergió a sus espaldas: Drax el Destructor. Creado genéticamente por Kronos con un único propósito biológico en su existencia, Drax ignoró que Thanos intentaba salvar el universo y clavó su puño desnudo directo a través del pecho blindado del Titán."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "En una viñeta icónica que conmocionó a los lectores, Drax arrancó el corazón palpitante de Thanos de un solo tirón, viendo al conquistador desplomarse inerte en un charco de sangre cósmica. Aunque Thanos sonrió al reunirse con su amada Muerte, Drax cumplió su sangriento destino galáctico grabando su nombre en la eternidad."
            }
        ],
        "description": "El clímax histórico de Keith Giffen y Andrea Di Vito: Annihilation #4. La muerte de Thanos a manos de Drax el Destructor.",
        "hashtags": "#Thanos #Drax #Annihilation #MarvelCosmic #Marvel #MarvelComics #Galactus #Comics #Shorts #Reels"
    },
    {
        "slot": 46,
        "queue_folder": "46_daredevil_muerte_karen_page",
        "id": "daredevil_muerte_karen_page",
        "title": "¡Bullseye Asesinó al Gran Amor de Daredevil! La Tragedia en el Altar de la Iglesia 😈⛪💔",
        "character": "Daredevil",
        "folder": "46_daredevil_muerte_karen_page",
        "theme_signature": "daredevil:guardian_devil_5:karen_page_death_bullseye",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La pérdida más devastadora y desgarradora que quebró para siempre el alma y la fe católica del Hombre sin Miedo! En la célebre saga Guardian Devil escrita por Kevin Smith, el psicópata asesino a sueldo Bullseye fue contratado por Mysterio para quebrar psicológicamente a Matt Murdock atacando a sus seres más queridos."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Bullseye rastreó a Daredevil hasta la iglesia de Clinton Church en Hell's Kitchen, donde el héroe ciego intentaba proteger a un bebé indefenso. Mientras el demonio de Hell's Kitchen combatía ferozmente cuerpo a cuerpo contra el villano, Karen Page, el gran amor de la vida de Matt, observaba horrorizada desde las sombras del altar."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "En medio del violento forcejeo, Bullseye le arrebató su propio bastón multipropósito a Daredevil. Con una puntería mortal infalible, el maníaco apuntó el garrote directamente hacia la cabeza del justiciero derribado. Pero en una fracción de segundo de heroísmo puro, Karen se interpuso valientemente en la trayectoria para salvar la vida de su amado."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "El proyectil de madera y acero atravesó brutalmente el corazón de Karen, desplomándose agonizante en los brazos de un Matt destrozado que gritaba desesperado ante el crucifijo de la iglesia. Karen murió susurrando su perdón, dejando a Daredevil consumido por un dolor infinito que cambió la mitología de Hell's Kitchen para siempre."
            }
        ],
        "description": "La desgarradora tragedia de Kevin Smith y Joe Quesada: Daredevil: Guardian Devil #5. El asesinato de Karen Page.",
        "hashtags": "#Daredevil #Bullseye #KarenPage #MattMurdock #Marvel #MarvelComics #HellsKitchen #Comics #Shorts #Reels"
    },
    {
        "slot": 47,
        "queue_folder": "47_carnage_usa_dover_oklahoma",
        "id": "carnage_usa_dover_oklahoma",
        "title": "¡Carnage Sometió a un Pueblo Entero! La Aterradora Posesión de Dover, Oklahoma 🩸🥩😱",
        "character": "Carnage",
        "folder": "47_carnage_usa_dover_oklahoma",
        "theme_signature": "carnage:usa_1:dover_oklahoma_meat_packing",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La invasión simbionte más perturbadora y terrorífica en la historia de Marvel Comics que convirtió a una comunidad pacífica en un infierno de sangre! En la miniserie Carnage USA, el despiadado asesino serial Cletus Kasady viajó hasta el pequeño y aislado pueblo ganadero de Dover en el estado de Oklahoma."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Cletus se infiltró en la gigantesca planta procesadora de carne local y arrojó fragmentos vivos de su masa celular roja en las calderas de agua potable. A través de las tuberías subterráneas, el simbionte rojo se extendió como una plaga biológica voraz, brotando de lavabos y grifos para someter simultáneamente a miles de ciudadanos inocentes."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Hombres, mujeres, ancianos y niños se transformaron en marionetas carniceras con dientes afilados y ojos desquiciados obedeciendo la mente colmena de Kasady. Cuando un equipo de Vengadores compuesto por Capitán América, Hawkeye, Wolverine y Thing llegó a investigar, fueron emboscados en la niebla y absorbidos completamente por la vorágine roja."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Con los propios héroes más poderosos de la Tierra convertidos en títeres poseídos por Carnage patrullando las calles ensangrentadas, Spider-Man y un contingente militar especial tuvieron que desplegar tanques sónicos para contener una de las peores pesadillas biológicas jamás desatadas en territorio norteamericano por el sádico monstruo carmesí."
            }
        ],
        "description": "La escalofriante historia de Zeb Wells y Clayton Crain: Carnage U.S.A. #1-5. La posesión masiva de Dover, Oklahoma.",
        "hashtags": "#Carnage #SpiderMan #Avengers #Marvel #MarvelComics #CletusKasady #Symbiote #Comics #Shorts #Reels"
    },
    {
        "slot": 48,
        "queue_folder": "48_xmen_schism_cyclops_wolverine",
        "id": "xmen_schism_cyclops_wolverine",
        "title": "¡La Pelea que Destruyó a los X-Men! La Sangrienta Guerra Moral entre Wolverine y Cyclops ⚔️🩸❌",
        "character": "X-Men",
        "folder": "48_xmen_schism_cyclops_wolverine",
        "theme_signature": "xmen:schism_5:cyclops_wolverine_ideological_war",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La fractura ideológica más amarga y violenta que separó para siempre a los dos líderes más importantes de la raza mutante! En la impactante saga X-Men Schism, la pequeña nación mutante de Utopía en la bahía de San Francisco quedó rodeada por un colosal Super Centinela programado para la aniquilación total."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Con los adultos heridos y sin refuerzos disponibles, Cyclops tomó una decisión radical: ordenó a los niños mutantes tomar las armas y matar al enemigo para defender la patria. Sin embargo, Wolverine se opuso enfurecido, afirmando con dolor que los niños deben ser protegidos y educados, jamás convertidos en soldados desechables de guerra."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "La tensión acumulada durante décadas explotó en un duelo a muerte sobre los acantilados. Mientras el gigantesco robot asesino aterrizaba a sus espaldas, Logan y Scott se atacaron salvajemente: Cyclops quemando el rostro de Wolverine con devastadores rayos ópticos y Logan cortando el visor de Scott con sus garras de adamantium afiladas."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Aunque los jóvenes mutantes lograron derrotar al Centinela trabajando en equipo, la hermandad de los X-Men murió esa misma noche. Wolverine abandonó Utopía con la mitad de la población para reconstruir la escuela de Xavier en Nueva York, partiendo al pueblo mutante en dos facciones irreconciliables que jamás volvieron a ser iguales."
            }
        ],
        "description": "El histórico evento de Jason Aaron y Carlos Pacheco: X-Men: Schism #4-5. El enfrentamiento que dividió a los mutantes.",
        "hashtags": "#XMen #Wolverine #Cyclops #Schism #Marvel #MarvelComics #Mutants #Comics #Shorts #Reels"
    },
    {
        "slot": 49,
        "queue_folder": "49_green_arrow_cry_for_justice_prometheus",
        "id": "green_arrow_cry_for_justice_prometheus",
        "title": "¡Green Arrow Cruzó la Línea que Batman Jamás Cruzaría! La Venganza por Star City 🏹🎯🩸",
        "character": "Green Arrow",
        "folder": "49_green_arrow_cry_for_justice_prometheus",
        "theme_signature": "green_arrow:cry_for_justice_7:prometheus_execution",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡El instante más oscuro y polémico de Flecha Verde donde el arquero esmeralda abandonó todos sus ideales éticos para ejecutar venganza! En la trágica saga Cry for Justice, el brillante supervillano táctico Prometheus diseñó un elaborado ataque sorpresa contra la Liga de la Justicia para humillar a los héroes más grandes de la Tierra."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "Prometheus detonó un dispositivo de teletransportación masivo en Star City, borrando del mapa el centro de la metrópoli y causando la muerte instantánea de cien mil ciudadanos inocentes, incluyendo a la pequeña Lian Harper, la nieta adoptiva de Oliver Queen, dejando al héroe destrozado entre los escombros humeantes."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Para evitar que destruyera más ciudades, la Liga aceptó dejar escapar libre al villano hacia su guarida secreta en otra dimensión. Confiado en que el código moral de no matar de Batman y Superman siempre lo mantendría a salvo, Prometheus caminaba sonriente por su fortaleza creyéndose intocable ante la ley metahumana."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Pero de la oscuridad de los rincones emergió en silencio Oliver Queen con su arco tensado al máximo. Antes de que el villano pudiera reaccionar, Green Arrow disparó una certera flecha que perforó el centro de la frente de Prometheus a sangre fría, cruzando una frontera moral sin retorno que lo convirtió en un proscrito solitario."
            }
        ],
        "description": "El oscuro desenlace de Justice League: Cry for Justice #7 por James Robinson y Mauro Cascioli. La venganza de Green Arrow.",
        "hashtags": "#GreenArrow #JusticeLeague #Prometheus #DCComics #StarCity #OliverQueen #Comics #Shorts #Reels"
    },
    {
        "slot": 50,
        "queue_folder": "50_planet_hulk_muerte_caiera",
        "id": "planet_hulk_muerte_caiera",
        "title": "¡La Muerte que Destruyó la Paz de Hulk! El Trágico Fin de Caiera y el Nacimiento del Worldbreaker 🌋💔🟢",
        "character": "Hulk",
        "folder": "50_planet_hulk_muerte_caiera",
        "theme_signature": "hulk:incredible_hulk_105:death_of_caiera_worldbreaker",
        "voice": "Puck",
        "scenes": [
            {
                "scene_number": 1,
                "file": "scene_01.jpg",
                "text": "¡La pérdida más desgarradora que transformó al Gigante Esmeralda en una imparable fuerza de destrucción cósmica capaz de quebrar continentes enteros! En el planeta salvaje de Sakaar, tras sobrevivir como gladiador y derrocar al Rey Rojo, Hulk encontró por primera vez en su vida la paz, siendo coronado como emperador amado."
            },
            {
                "scene_number": 2,
                "file": "scene_02.jpg",
                "text": "A su lado reinaba Caiera la Oldstrong, su poderosa esposa guerrera que llevaba en su vientre al futuro heredero del gigante verde. Juntos comenzaron a reconstruir el mundo devastado entre celebraciones y esperanza. Como monumento a su nueva vida, colocaron en la plaza central la nave espacial que lo había traído desde la Tierra."
            },
            {
                "scene_number": 3,
                "file": "scene_03.jpg",
                "text": "Pero sin previo aviso, el motor warp de la nave comenzó a emitir un zumbido mortal: una ojiva de antimateria oculta se activó para detonar. En una fracción de segundo de catástrofe, la explosión colosal vaporizó la capital entera y fracturó la corteza tectónica, haciendo brotar ríos de magma hirviente que consumieron a millones de inocentes."
            },
            {
                "scene_number": 4,
                "file": "scene_04.jpg",
                "text": "Protegiendo el cuerpo de su esposo con su propia piel de roca hasta el último aliento, Caiera se desintegró en cenizas en los brazos de Hulk. Enloquecido de dolor y furia pura, el gigante absorbió la radiación del núcleo convirtiéndose en el destructor Worldbreaker, jurando regresar a la Tierra para aniquilar a los Illuminati que le arrebataron su felicidad."
            }
        ],
        "description": "La devastadora culminación de Greg Pak y Carlo Pagulayan: Incredible Hulk #105. El origen de la furia de World War Hulk.",
        "hashtags": "#Hulk #PlanetHulk #Caiera #WorldWarHulk #Marvel #MarvelComics #Illuminati #Comics #Shorts #Reels"
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

    proj_out_dir = PACK_OUTPUT_DIR / proj_id
    if proj_out_dir.exists():
        shutil.rmtree(proj_out_dir, ignore_errors=True)

    work_dir = PROJECT_ROOT / "work" / f"batch5_{proj_id}"
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
        "source": "batch_5_inéditos_curated_panels",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(dest_meta, "w", encoding="utf-8") as mf:
        json.dump(meta_payload, mf, indent=2, ensure_ascii=False)

    print(f"✅ Video encolado exitosamente en {dest_dir}")
    return dest_dir

if __name__ == "__main__":
    target_slot = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg.isdigit():
            target_slot = int(arg)

    print(f"🎬 Batch 5 Master Production Engine (Slots 41 al 50)")
    for proj in PROJECTS:
        slot = proj["slot"]
        if target_slot and slot != target_slot:
            continue
        
        dest = SCHEDULED_QUEUE / proj["queue_folder"]
        if (dest / "video.mp4").exists() and (dest / "metadata.json").exists():
            print(f"⏩ Slot {slot} ya existe en scheduled_queue. Saltando.")
            continue

        res = produce_single_project(proj)
        if not res:
            print(f"❌ Falló producción del Slot {slot}")
        else:
            print(f"🎉 Slot {slot} completado y encolado en {dest}")
