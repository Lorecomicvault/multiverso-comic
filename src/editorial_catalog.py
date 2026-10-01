"""
Multiverso Comic - Editorial Story Catalog
Strict 4-Scene Cinematic Standard (20-30s Duration)
Every story features:
- Exactly 4 punchy scenes (55-65 words total = ~22-26s TTS narration).
- Exactly 4 high-resolution official comic panels (resolved via Fandom API with Referer).
- 100% adherence to 20-30 second viral duration window.
"""

EDITORIAL_STORIES = [
    {
        "id": "venom_el_origen_del_simbionte_letal",
        "character": "Venom",
        "title": "Venom: El Nacimiento del Protector Letal",
        "theme_signature": "venom:eddie_brock:origen_iglesia_simbionte",
        "description": "La oscura historia de como Eddie Brock se unio al simbionte alienigena en una iglesia para convertirse en Venom, el protector letal mas implacable de Marvel.",
        "hashtags": "#Venom #SpiderMan #MarvelComics #ToddMcFarlane #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que Venom nació en una iglesia cuando Eddie Brock rezaba desesperado por su vida arruinada?",
            "El simbionte alienígena rechazado por Spider-Man cayó sobre Eddie, fusionándose con su odio y dolor más profundo.",
            "Al unirse, sus mentes crearon a Venom, un monstruo con colmillos letales y la emblemática araña blanca en el pecho.",
            "Jurando proteger a los inocentes y aniquilar a Peter Parker, nació el protector letal más temido de Marvel."
        ],
        "scene_art_urls": [
            "assets/curated_panels/venom_origen/scene_01.jpg",
            "assets/curated_panels/venom_origen/scene_02.jpg",
            "assets/curated_panels/venom_origen/scene_03.jpg",
            "assets/curated_panels/venom_origen/scene_04.jpg"
        ],
        "art_queries": [
            "Eddie Brock praying Our Lady of Saints Church Amazing Spider-Man 300 comic panel",
            "Symbiote bonding with Eddie Brock I was joined comic panel",
            "Venom first full appearance smiling white spider Todd McFarlane comic panel",
            "Venom swinging webs night New York Amazing Spider-Man 300 comic panel"
        ]
    },
    {
        "id": "flash_godspeed_el_ladron_de_velocidad",
        "character": "The Flash",
        "title": "The Flash: Godspeed, el Despiadado Asesino de Velocistas",
        "theme_signature": "flash:godspeed:august_heart_speed_force",
        "description": "August Heart, compañero de Barry Allen, es alcanzado por la tormenta de la Speed Force y se convierte en Godspeed, un juez implacable que roba la velocidad asesinando a otros velocistas.",
        "hashtags": "#TheFlash #Godspeed #DCComics #SpeedForce #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que cuando una tormenta de Speed Force azotó Central City, nació el velocista más despiadado de DC?",
            "August Heart, el mejor amigo de Barry Allen, adoptó el manto de Godspeed jurando ejecutar a todo criminal.",
            "Descubrió que arrancándole el corazón a otros velocistas absorbía su velocidad, volviéndose tan rápido que podía clonarse.",
            "Barry Allen tuvo que aliarse con Kid Flash para drenar su energía y encerrarlo en Iron Heights."
        ],
        "scene_art_urls": [
            "The_Flash_Vol_5_3.jpg",
            "The_Flash_Vol_5_4.jpg",
            "The_Flash_Vol_5_6.jpg",
            "The_Flash_Vol_5_8.jpg"
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
            "¿Sabías que Thaal Sinestro forjó un ejército con la luz amarilla del miedo para derrocar a los Green Lanterns?",
            "Reclutó a los monstruos más temibles del cosmos como Arkillo y Superboy Prime, sitiando el planeta Oa.",
            "Los Guardianes del Universo reescribieron sus leyes sagradas autorizando el uso de fuerza letal en batalla.",
            "En un duelo sin anillos, Hal Jordan noqueó a Sinestro probando que la voluntad siempre vence al miedo."
        ],
        "scene_art_urls": [
            "Sinestro_Corps_War.jpg",
            "Green_Lanterns_vs_Sinestro_Corps_01.jpg",
            "Sinestro corps special 1.jpg",
            "GL 4 25 Sinestro defeated.jpg"
        ]
    },
    {
        "id": "thanos_rising_el_origen_del_titan_loco",
        "character": "Thanos",
        "title": "Thanos: El Perturbador Origen y la Obsesión con la Muerte",
        "theme_signature": "thanos:rising:origen_titan_loco_asesinato",
        "description": "Nacido como una anomalía en la luna Titán, Thanos comenzó diseccionando criaturas en cuevas secretas hasta convertirse en el genocida cósmico obsesionado con cortejar a la Señora Muerte.",
        "hashtags": "#Thanos #MarvelComics #ThanosRising #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que Thanos nació en la luna Titán como una anomalía monstruosa que horrorizó a su propia madre?",
            "Guiado por una niña misteriosa, comenzó realizando sádicas disecciones biológicas a sus propios compañeros de clase.",
            "Al descubrir que la niña era la personificación de la Muerte, Thanos asesinó a su madre para cortejarla.",
            "Años después, bombardeó Titán con ojivas nucleares extinguiendo a su especie entera en nombre de su amada."
        ],
        "scene_art_urls": [
            "Thanos_Rising_Vol_1_1.jpg",
            "Thanos_Rising_Vol_1_2.jpg",
            "Thanos_Rising_Vol_1_3.jpg",
            "Thanos_Rising_Vol_1_5.jpg"
        ]
    },
    {
        "id": "marvel_ruins_el_universo_maldito",
        "character": "Marvel Ruins",
        "title": "Marvel Ruins: El Universo Donde Todo lo que Podía Salir Mal, Salió Mal",
        "theme_signature": "marvel:ruins:distopia_enfermedad_pesadilla",
        "description": "En este aterrador universo alternativo creado por Warren Ellis, ningún héroe obtuvo superpoderes: cada accidente provocó mutaciones atroces, cánceres deformes y pesadillas biológicas.",
        "hashtags": "#MarvelRuins #MarvelComics #WarrenEllis #ComicsDeTerror #Shorts #Reels",
        "scenes": [
            "¿Sabías que en Marvel Ruins ningún héroe obtuvo poderes y cada accidente se convirtió en una atroz pesadilla?",
            "Al recibir la radiación gamma, Bruce Banner no se convirtió en Hulk, sino en una aterradora masa viva de tumores deformes.",
            "Magneto perdió el control magnético, atrapado en un arnés defectuoso mientras decenas de sierras voladoras lo descuartizaban vivo.",
            "Y en el espacio, Silver Surfer perdió la cordura, desgarrándose el pecho con sus manos en una dolorosa agonía cósmica."
        ],
        "scene_art_urls": [
            "Ruins_Vol_1_1.jpg",
            "Bruce Banner (Earth-9591) from Ruins Vol 1 1 001.jpg",
            "Ruins_Vol_1_2.jpg",
            "Norrin Radd (Earth-9591) from Ruins Vol 1 1 0001.jpg"
        ]
    },
    {
        "id": "superior_iron_man_extremis",
        "character": "Iron Man",
        "title": "Superior Iron Man: La Armadura Endo-Sym y la Ambición de Tony Stark",
        "theme_signature": "iron_man:superior:endo_sym_inversion",
        "description": "Invertido moralmente tras el evento Axis, Tony Stark se convierte en un magnate sin escrúpulos con una armadura líquida simbionte y el virus Extremis 3.0.",
        "hashtags": "#IronMan #SuperiorIronMan #MarvelComics #Extremis #ComicsNarrados #Reels",
        "scenes": [
            "¿Sabías que tras el evento Axis, Tony Stark se convirtió en el villano más narcisista y peligroso de Marvel?",
            "Creó la armadura Endo-Sym a partir de metal líquido y biología simbionte, controlándola únicamente con su mente.",
            "Liberó el virus Extremis 3.0 en San Francisco, otorgando belleza perfecta a cambio de una suscripción millonaria diaria.",
            "Incluso encerró a Daredevil para proteger su negocio, demostrando que su mayor enemigo siempre fue su ego desmedido."
        ],
        "scene_art_urls": [
            "Superior_Iron_Man_Vol_1_1.jpg",
            "Superior_Iron_Man_Vol_1_2.jpg",
            "Superior_Iron_Man_Vol_1_3.jpg",
            "Superior_Iron_Man_Vol_1_4.jpg"
        ]
    },
    {
        "id": "daredevil_born_again_kingpin",
        "character": "Daredevil",
        "title": "Daredevil: Born Again y la Caida de Matt Murdock",
        "theme_signature": "daredevil:born_again:venganza_kingpin",
        "description": "La legendaria obra maestra de Frank Miller: cuando Karen Page vende el secreto de Daredevil, Kingpin destruye metódicamente la vida de Matt Murdock.",
        "hashtags": "#Daredevil #BornAgain #Kingpin #FrankMiller #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "¿Sabías que cuando Karen Page vendió la identidad de Daredevil por una dosis de heroína, Kingpin destruyó su vida?",
            "Wilson Fisk congeló sus cuentas bancarias, le retiró su licencia de abogado e hizo volar en pedazos su casa.",
            "Indigente, paranoico y al borde de la locura, Matt Murdock sobrevivió a puñaladas en los barrios bajos de Nueva York.",
            "Cuidado por su madre Maggie en una iglesia, renació como el demonio justiciero para desmantelar el imperio de Fisk."
        ],
        "scene_art_urls": [
            "Daredevil_Vol_1_227.jpg",
            "Daredevil_Vol_1_228.jpg",
            "Daredevil_Vol_1_229.jpg",
            "Daredevil_Vol_1_232.jpg"
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
            "¿Sabías que al borde de la muerte, el Doctor Octopus intercambió su mente con Peter Parker?",
            "Peter murió atrapado en el cuerpo decrépito de Octavius, pero le transmitió la sagrada carga de la responsabilidad.",
            "Con soberbia colosal, Otto juró ser un Spider-Man superior desplegando Spider-Bots y aniquilando criminales sin piedad.",
            "Al ver que solo el verdadero Peter podía salvar a la ciudad, Otto borró voluntariamente su propia mente."
        ],
        "scene_art_urls": [
            "Superior_Spider-Man_Vol_1_1.jpg",
            "Superior_Spider-Man_Vol_1_2.jpg",
            "Superior_Spider-Man_Midtown_Comics_Variant.jpg",
            "Superior_Spider-Man_Vol_1_1_Textless.png"
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
            "¿Sabías que Psycho-Man intentó lavar el cerebro de Deadpool y terminó desatando su psicopatía más sanguinaria?",
            "Wade comprendió que todos eran marionetas ficticias y decidió matarlos a todos para liberarlos del sufrimiento eterno.",
            "Incineró a los Cuatro Fantásticos, decapitó a Thor agrandando el Mjolnir y aniquiló a Hulk en segundos.",
            "Tras llegar a la mesa de los guionistas de Marvel, Deadpool advirtió que el lector sería el siguiente."
        ],
        "scene_art_urls": [
            "Deadpool_Kills_the_Marvel_Universe_Vol_1_1.jpg",
            "Deadpool_Kills_the_Marvel_Universe_Vol_1_2.jpg",
            "Deadpool_Kills_the_Marvel_Universe_Vol_1_3.jpg",
            "Deadpool_Kills_the_Marvel_Universe_Vol_1_4.jpg"
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
            "¿Sabías que Thomas Elliot, amigo de la infancia de Bruce Wayne, orquestó la mayor venganza contra Batman?",
            "Bajo el manto vendado de Hush, manipuló a Killer Croc, Poison Ivy y al mismísimo Superman con kriptonita.",
            "Consumido por la envidia infantil hacia la fortuna Wayne, Elliot dedicó toda su vida a destruir a Bruce.",
            "Batman salvó a Gotham tras descubrir la amarga traición de quien alguna vez fue su hermano de sangre."
        ],
        "scene_art_urls": [
            "Batman_608.jpg",
            "Batman_006.jpg",
            "Batman_012.jpg",
            "Batman_Vol_1_619.jpg"
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
            "¿Sabías que en un futuro postapocalíptico, Hulk absorbió la radiación nuclear y se convirtió en el tirano Maestro?",
            "Gobernó la ciudadela de Distopía y guardó los cráneos de los héroes caídos en un tétrico búnker.",
            "La resistencia rebelde trajo al joven Hulk del pasado para enfrentar a su corrupta versión anciana.",
            "Hulk envió a Maestro a través del tiempo al epicentro mismo de la Bomba Gamma original que lo aniquiló."
        ],
        "scene_art_urls": [
            "Hulk_Future_Imperfect_Vol_1_1.jpg",
            "Hulk_Future_Imperfect_Vol_1_2.jpg",
            "Maestro_Vol_1_1_McGuinness_Variant_Textless.jpg",
            "Maestro_War_and_Pax_Vol_1_1_Stegman_Variant_Textless.jpg"
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
            "¿Sabías que en Old Man Logan, Mysterio utilizó ilusiones ópticas para quebrar mentalmente a Wolverine?",
            "Creyendo defender a los estudiantes de cuarenta villanos armados, Logan desató una furia berserker sangrienta.",
            "Al disiparse el humo verde, descubrió la desgarradora verdad: acababa de masacrar a todos los X-Men.",
            "Roto de dolor, intentó quitarse la vida sobre las vías de un tren, pero su factor curativo se lo impidió."
        ],
        "scene_art_urls": [
            "Wolverine_Vol_3_66_Wraparound_Textless.jpg",
            "Wolverine_Vol_3_70.jpg",
            "X-Men_(Earth-807128)_from_Wolverine_Vol_3_70_001.jpg",
            "James_Howlett_(Earth-807128)_from_Wolverine_Vol_3_72_002.jpg"
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
            "¿Sabías que antes del Big Bang, Knull reinaba en la oscuridad hasta que decapitó a un Celestial con su sombra?",
            "De la cabeza del dios muerto forjó la Necroespada y engendró a la raza simbionte entera.",
            "Al despertar invadió la Tierra con dragones espaciales y partió por la mitad a Sentry con sus manos.",
            "Eddie Brock canalizó la Fuerza Enigma de la Luz y arrojó a Knull al centro del Sol coronándose Rey de Negro."
        ],
        "scene_art_urls": [
            "King_in_Black_Vol_1_1.jpg",
            "Venom_Vol_4_1.jpg",
            "King_in_Black_Vol_1_3.jpg",
            "Venom_Vol_4_2.jpg"
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
            "¿Sabías que Superboy Prime, un fanático con poderes de Superman, enloqueció y casi destruye el multiverso?",
            "Golpeó las paredes del espacio-tiempo con tanta fuerza que alteró la realidad y resucitó a Jason Todd.",
            "Inmune a la magia y a la kriptonita, masacró a docenas de Titanes y a treinta y dos Linternas Verdes.",
            "Se necesitaron dos Supermanes atravesando los restos de Krypton para someterlo en un campo de fuerza eterno."
        ],
        "scene_art_urls": [
            "Infinite_Crisis_001.jpg",
            "Battle_of_the_Supermen.jpg",
            "Final_Crisis_Legion_of_Three_Worlds_1.jpg",
            "Adventure_Comics_Vol_2_5_Textless.jpg"
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
            "¿Sabías que al salvar a su madre en el pasado, Barry Allen destruyó la línea temporal creando Flashpoint?",
            "Despertó sin poderes en un mundo al borde del colapso bélico entre Wonder Woman y Aquaman.",
            "En la Baticueva descubrió que quien murió fue Bruce, y Batman era su padre Thomas, un justiciero despiadado.",
            "Aceptando el destino, Barry revirtió la paradoja entregándole a Bruce la última carta escrita por su padre."
        ],
        "scene_art_urls": [
            "Flashpoint_Vol_2_1.jpg",
            "Flashpoint_Vol_2_2.jpg",
            "Flashpoint_Vol_2_3.jpg",
            "Flashpoint_Vol_2_5.png"
        ]
    },
    {
        "id": "batman_who_laughs_la_pesadilla_del_multiverso",
        "character": "Batman Who Laughs",
        "title": "Batman Who Laughs La Pesadilla del Multiverso",
        "theme_signature": "batman:batman_who_laughs:pesadilla_multiverso",
        "description": "Historia épica completa de cómic: Batman Who Laughs La Pesadilla del Multiverso. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#BatmanWhoLaughs #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Sabías que cuando Batman rompió su regla y asesinó al Joker, inhaló una toxina nanotecnológica incurable?",
            "La toxina fusionó el intelecto táctico de Bruce Wayne con la psicopatía pura y sádica del Joker.",
            "Masacró a toda la Batifamilia en la Baticueva y aniquiló a la Liga de la Justicia con armas personalizadas.",
            "Conquistó el Multiverso Oscuro liderando a los Caballeros Oscuros y sembrando pesadillas en cada realidad."
        ],
        "scene_art_urls": [
            "The_Batman_Who_Laughs_Vol_2_1.jpg",
            "The_Batman_Who_Laughs_Vol_2_2.jpg",
            "The_Batman_Who_Laughs_Vol_2_3.jpg",
            "The_Batman_Who_Laughs_Vol_2_4.jpg"
        ]
    },
    {
        "id": "injustice_el_regimen_del_tirano_superman",
        "character": "Superman",
        "title": "Injustice El Regimen del Tirano Superman",
        "theme_signature": "superman:injustice:regimen_tirania",
        "description": "Historia épica completa de cómic: Injustice El Regimen del Tirano Superman. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#Superman #Injustice #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Sabías que engañado por el Joker, Superman asesinó a Lois Lane y detonó una ojiva nuclear en Metrópolis?",
            "Enloquecido de dolor, atravesó el pecho del Joker con su puño y juró imponer la paz por la fuerza.",
            "Fundó el Régimen Global ejecutando a criminales y héroes rebeldes, transformando la Tierra en un estado militar.",
            "Batman lideró la resistencia clandestina demostrando que la libertad jamás debe sacrificarse ante el miedo."
        ],
        "scene_art_urls": [
            "Injustice_Gods_Among_Us_Vol_1_1.jpg",
            "Injustice_Gods_Among_Us_Vol_1_2.jpg",
            "Injustice_Gods_Among_Us_Vol_1_3.jpg",
            "Injustice_Gods_Among_Us_Vol_1_4.jpg"
        ]
    },
    {
        "id": "marvel_zombies_la_infeccion_multiversal",
        "character": "Marvel Zombies",
        "title": "Marvel Zombies La Infeccion Multiversal",
        "theme_signature": "marvel_zombies:infeccion:hambre_canibal",
        "description": "Historia épica completa de cómic: Marvel Zombies La Infeccion Multiversal. Narración cinematográfica con viñetas oficiales.",
        "hashtags": "#MarvelZombies #ComicsNarrados #ComicLoreVault #Marvel #DC #Reels #Shorts",
        "scenes": [
            "¿Sabías que un rayo púrpura estrelló a Sentry zombificado en Nueva York infectando a los Avengers en minutos?",
            "Conservando su intelecto pero dominados por un hambre caníbal insaciable, devoraron a la humanidad entera.",
            "Cuando Silver Surfer y Galactus llegaron a la Tierra, los héroes zombis los descuartizaron y devoraron.",
            "Absorbieron el poder cósmico de Galactus y viajaron por el espacio devorando planetas enteros sin piedad."
        ],
        "scene_art_urls": [
            "Marvel_Zombies_Vol_1_1.jpg",
            "Marvel_Zombies_Vol_1_2.jpg",
            "Marvel_Zombies_Vol_1_3.jpg",
            "Marvel_Zombies_Vol_1_4.jpg"
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
            "¿Sabías que el Antimonitor desató una ola de antimateria que borró infinitos universos de la faz del tiempo?",
            "Supergirl protagonizó un sacrificio heroico destruyendo la armadura del titán antes de caer en batalla.",
            "Barry Allen corrió a hipervelocidad destruyendo el cañón de antimateria mientras su cuerpo se desintegraba en energía.",
            "Cinco universos supervivientes se fusionaron en una sola línea renacida gracias al sacrificio legendario de Flash."
        ],
        "scene_art_urls": [
            "Crisis_on_Infinite_Earths_Vol_1_1.jpg",
            "Crisis_on_Infinite_Earths_7.jpg",
            "Crisis_on_Infinite_Earths_8.jpg",
            "Crisis_on_Infinite_Earths_10.jpg"
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
            "¿Sabías que millones de años en el futuro, el Rey Thanos exterminó a todos los héroes y celestiales cósmicos?",
            "Mantiene a Hulk anciano encadenado como su bestia de caza y a Ghost Rider Cósmico como su heraldo.",
            "Usó la Piedra del Tiempo para secuestrar a su versión joven con un pedido desesperado: que lo asesinara en combate.",
            "Solo el propio Thanos era digno de arrebatarle la vida para que pudiera reunirse con su amada Muerte."
        ],
        "scene_art_urls": [
            "Thanos_Vol_2_13_Textless.jpg",
            "Thanos_Vol_2_14_Textless.jpg",
            "Thanos_Vol_2_16_Textless.jpg",
            "Thanos_Vol_2_18_Textless.jpg"
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
            "¿Sabías que Nekron forjó anillos negros resucitando a héroes caídos como monstruos sádicos en Blackest Night?",
            "Los Linternas Negras arrancaban los corazones de sus antiguos compañeros para absorber su energía vital.",
            "Los siete cuerpos de linternas forjaron una tregua cósmica inédita combinando todos los colores del espectro emocional.",
            "Despertaron la milagrosa Entidad Blanca, resucitando a los héroes y desintegrando la oscuridad eterna de Nekron."
        ],
        "scene_art_urls": [
            "Blackest_Night_Vol_1_1.jpg",
            "Blackest_Night_Vol_1_2.jpg",
            "Blackest_Night_5.jpg",
            "Blackest_Night_Vol_1_8.jpg"
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
            "¿Sabías que traicionado por los Illuminati y tras la destrucción de su reino, Hulk regresó buscando venganza?",
            "Destrozó la armadura Hulkbuster de Iron Man y humilló a cada miembro de los X-Men sin despeinarse.",
            "Resistió la magia prohibida de Doctor Strange y colisionó contra Sentry en una batalla que sacudió la atmósfera.",
            "Desatando el modo Rompemundos, cada paso de Hulk amenazaba con partir el continente entero en dos."
        ],
        "scene_art_urls": [
            "Incredible_Hulk_Vol_2_105_Textless.jpg",
            "World_War_Hulk_Vol_1_1_Textless.jpg",
            "World_War_Hulk_Vol_1_3.jpg",
            "World_War_Hulk_Vol_1_5_Textless.jpg"
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
            "¿Sabías que cuando los Beyonders destruyeron el multiverso, Victor von Doom robó su poder convirtiéndose en dios supremo?",
            "De las cenizas cósmicas moldeó Battleworld, gobernando como deidad absoluta protegido por un ejército de Thors.",
            "Le arrancó la columna vertebral a Thanos de un solo golpe y quebró el cuello de Cíclope con la Fuerza Fénix.",
            "Tras admitir que Reed Richards podía salvarlo mejor, restauró el multiverso tras haber sido el amo del cosmos."
        ],
        "scene_art_urls": [
            "Secret_Wars_Vol_1_8_Textless.jpg",
            "Secret_Wars_Vol_1_6_Textless.jpg",
            "Secret_Wars_Vol_1_7_Textless.jpg",
            "Secret_Wars_Vol_1_9_Textless.jpg"
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
            "¿Sabías que tras ver morir a sus hijos de hambre rezando a dioses mudos, Gorr juró su extinción total?",
            "Empuñó la temible Necroespada All-Black forjada por Knull, asesinando a deidades por las galaxias durante milenios.",
            "Esclavizó a los dioses supervivientes para construir la Bomba Divina, diseñada para aniquilar a todo dios en el tiempo.",
            "Hizo falta una alianza imposible entre tres versiones de Thor para detener la cruzada más sanguinaria de Marvel."
        ],
        "scene_art_urls": [
            "Thor_God_of_Thunder_Vol_1_6.jpg",
            "Thor_God_of_Thunder_Vol_1_5_Textless.jpg",
            "Thor_God_of_Thunder_Vol_1_8_Textless.jpg",
            "Thor_God_of_Thunder_Vol_1_1.jpg"
        ]
    },
    {
        "id": "batman_tribunal_de_los_buhos_laberinto",
        "character": "Batman",
        "title": "Batman: El Tribunal de los Búhos y el Laberinto Subterráneo",
        "theme_signature": "batman:court_of_owls:laberinto_tortura",
        "description": "Durante ocho días de agonía, Batman es atrapado en un laberinto subterráneo sin agua ni luz por el Tribunal de los Búhos, perdiendo la cordura antes de su feroz contraataque.",
        "hashtags": "#Batman #CourtOfOwls #DCComics #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que el Tribunal de los Búhos atrapó a Batman en un laberinto subterráneo secreto bajo Gotham?",
            "Sin comida, bebiendo agua envenenada y bajo luz fluorescente, resistió ocho días de tortura psicológica absoluta.",
            "El asesino Talon atravesó su abdomen con una espada frente a la corte para rematarlo como trofeo.",
            "Recordando su promesa a Gotham, Batman se levantó furioso, demolió a Talon a golpes y juró destruirlos."
        ],
        "scene_art_urls": [
            "Batman_Vol_2_5.jpg",
            "Batman_Vol_2_6_Textless.jpg",
            "Batman_Vol_2_7_Textless.jpg",
            "Batman_Vol_2_8.jpg"
        ]
    },
    {
        "id": "batman_grim_knight_crime_alley",
        "universe": "DC",
        "character": "The Grim Knight",
        "title": "The Grim Knight: El Batman que Disparó a Matar en Crime Alley",
        "theme_signature": "batman:grim_knight:crime_alley_arsenal_militar",
        "description": "En este oscuro universo alternativo, Bruce Wayne no lloró la muerte de sus padres: recogió el arma de Joe Chill y lo ejecutó en el acto convirtiéndose en el despiadado Grim Knight.",
        "hashtags": "#TheGrimKnight #Batman #DCComics #DarkMultiverse #BatmanWhoLaughs #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que en el Multiverso Oscuro, la noche en que asesinaron a sus padres, Bruce Wayne no derramó lágrimas?",
            "Viendo el revólver de Joe Chill sobre el asfalto, el niño lo recogió y le disparó en el pecho sin piedad.",
            "Sin código moral, convirtió a Gotham en una zona de guerra ejecutando a cada villano con tácticas militares letales.",
            "Armado hasta los dientes y aliado con el Batman que Ríe, se consagró como el implacable Grim Knight."
        ],
        "scene_art_urls": [
            "Wayne_Murder_Grim_Knight_0001.jpg",
            "Joe_Chill_Grim_Knight_0001.PNG",
            "Batman_Villains_Grim_Knight_0001.PNG",
            "The_Batman_Who_Laughs_The_Grim_Knight_Vol_1_1_Textless.jpg"
        ]
    },
    {
        "id": "superman_red_son_comunismo",
        "universe": "DC",
        "character": "Superman",
        "title": "Superman Red Son: El Hijo Rojo de la Unión Soviética",
        "theme_signature": "superman:red_son:ucrania_stalin_guerra_fria",
        "description": "En este universo alternativo, la cápsula de Kal-El aterrizó en la Unión Soviética convirtiendo a Superman en el arma suprema del comunismo.",
        "hashtags": "#Superman #RedSon #DCComics #SovietSuperman #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que la cápsula espacial de Kal-El no cayó en Kansas, sino en una granja colectiva de la Unión Soviética?",
            "Criado bajo la doctrina comunista, Superman se convirtió en el arma suprema de Joseph Stalin para dominar el mundo.",
            "Para derrocar su tiranía roja, un Batman soviético con gorro de invierno usó lámparas solares rojas y lo puso de rodillas.",
            "Antes de ser capturado, Batman detonó una bomba en su propio estómago sacrificando su vida como símbolo eterno de libertad."
        ],
        "scene_art_urls": [
            "Superman Red Son 01.jpg",
            "Joseph Stalin Earth-30 001.jpg",
            "Batman Red Son 02.jpg",
            "Comrade of Steel.jpg"
        ],
        "art_queries": [
            "Superman Red Son Soviet ship landing collective farm",
            "Superman Soviet Stalin hammer sickle",
            "Batmankoff Soviet Batman ushanka red son",
            "Soviet Batman bomb Red Son sacrifice"
        ]
    },
    {
        "id": "punisher_kills_marvel_universe",
        "universe": "Marvel",
        "character": "The Punisher",
        "title": "The Punisher: El Día en que Frank Castle Masacró a Marvel",
        "theme_signature": "punisher:kills_marvel:venganza_familia_mutantes",
        "description": "Cuando los superhéroes mataron accidentalmente a su familia en Central Park, Frank Castle juró aniquilar a cada héroe y villano de Marvel.",
        "hashtags": "#ThePunisher #FrankCastle #MarvelComics #PunisherKills #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que cuando la batalla de los Vengadores contra los alienígenas mató a su familia, Frank Castle enloqueció de odio?",
            "Sin dudar un instante, levantó su rifle en Central Park y ejecutó a Cyclops y Hawkeye de un solo disparo en la cabeza.",
            "Armado con ojivas nucleares de Doctor Doom, engañó a todos los mutantes en la Luna y detonó una explosión cósmica.",
            "Tras liquidar a Spider-Man, Wolverine y Daredevil, Frank se apuntó con su propia pistola cerrando su venganza final."
        ],
        "scene_art_urls": [
            "Thor Odinson (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 0001.jpg",
            "Scott Summers (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 0001.jpg",
            "Victor von Doom (Earth-95126) and Francis Castle (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 0001.jpg",
            "Peter Parker (Earth-95126) from Punisher Kills the Marvel Universe Vol 1 1 002.jpg"
        ],
        "art_queries": [
            "Punisher Kills Marvel Universe Central Park family dead",
            "Punisher rifle shoot Cyclops Hawkeye",
            "Punisher nuclear missile Moon X-Men",
            "Punisher gun final kill Punisher Kills"
        ]
    },
    {
        "id": "flash_forward_wally_west_doctor_manhattan",
        "universe": "DC",
        "character": "The Flash",
        "title": "Flash Forward: Wally West y los Poderes de Doctor Manhattan",
        "theme_signature": "wally_west:flash_forward:mobius_chair_manhattan",
        "description": "Al sentarse en la Silla de Mobius imbuida con la energía de Doctor Manhattan, Wally West ascendió como el velocista cósmico supremo.",
        "hashtags": "#TheFlash #WallyWest #DoctorManhattan #FlashForward #DCComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Wally West se sentó en la legendaria Silla de Mobius y absorbió el poder supremo de Doctor Manhattan?",
            "En el centro del Multiverso Oscuro, una grieta dimensional amenazaba con devorar todas las realidades existentes.",
            "La energía cósmica azul envolvió su traje, grabando el símbolo del átomo en su frente y volviéndolo omnisciente.",
            "Con un simple parpadeo mental, Wally reescribió las líneas temporales y salvó a sus hijos atrapados en el olvido."
        ],
        "art_queries": [
            "Wally West Mobius chair Doctor Manhattan",
            "Dark Multiverse rift Flash Forward",
            "Wally West Manhattan suit atom symbol glowing blue",
            "Wally West Flash Forward saving children multiverse"
        ],
        "scene_art_urls": [
            "Mobius_Chair_Prime_Earth_001.jpg",
            "Flash_Wally_West_Prime_Earth_0017.jpg",
            "Flash_Wally_West_Prime_Earth_0018.jpg",
            "Flash_Wally_West_Prime_Earth_0032.jpg"
        ]
    },
    {
        "id": "hulk_the_end_ultimo_humano",
        "universe": "Marvel",
        "character": "Hulk",
        "title": "Hulk The End: El Último Ser Vivo en la Tierra",
        "theme_signature": "hulk:the_end:cucarachas_soledad_muerte_banner",
        "description": "Tras el holocausto nuclear, Hulk sobrevive solo en una Tierra muerta, regenerándose cada día de los enjambres de cucarachas carnívoras.",
        "hashtags": "#Hulk #TheEnd #MarvelComics #PeterDavid #ComicsDeTerror #Shorts #Reels",
        "scenes": [
            "¿Sabías que en un futuro devastado por una guerra nuclear, Hulk es el único ser humano que sobrevive en la Tierra?",
            "Cada día, enjambres de cucarachas gigantes carnívoras devoran su piel viva mientras su factor curativo lo regenera dolorosamente.",
            "Dentro de su mente, un anciano y enfermo Bruce Banner le ruega a Hulk que lo deje morir en paz.",
            "Cuando el corazón de Banner se detiene para siempre, Hulk queda solo en la oscuridad absoluta, anhelando un final que jamás llegará."
        ],
        "scene_art_urls": [
            "assets/curated_panels/hulk_the_end/scene_01.jpg",
            "assets/curated_panels/hulk_the_end/scene_02.jpg",
            "assets/curated_panels/hulk_the_end/scene_03.jpg",
            "assets/curated_panels/hulk_the_end/scene_04.jpg"
        ],
        "art_queries": [
            "Bruce Banner (Earth-2081) from Incredible Hulk The End Vol 1 1 0001.jpg",
            "Bruce Banner (Earth-2081) from Incredible Hulk The End Vol 1 1 0002.jpg",
            "Hulk The End regenerating Dale Keown comic panel",
            "Hulk The End feels cold final panel"
        ]
    }
]

# Configuración automática de voz en español (Edge-TTS Jorge) para todas las historias editoriales
for _s in EDITORIAL_STORIES:
    _s.setdefault("voice", "es-MX-JorgeNeural")
    _s.setdefault("tts_model", "edge-tts")
    _s.setdefault("fallback_tts_model", "edge-tts")
    _s.setdefault("style_direction", "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano")

