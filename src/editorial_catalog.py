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
            "assets/curated_panels/thanos_rising/scene_01.jpg",
            "assets/curated_panels/thanos_rising/scene_02.jpg",
            "assets/curated_panels/thanos_rising/scene_03.jpg",
            "assets/curated_panels/thanos_rising/scene_04.jpg"
        ],
        "art_queries": [
            "Thanos newborn mother Sui-San horror comic panel",
            "Young Thanos dissecting creatures cave Simone Bianchi comic panel",
            "Thanos bloody massacre corpses Simone Bianchi comic panel",
            "Thanos galactic destruction cosmic death Simone Bianchi comic panel"
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
    },
    {
        "id": "captain_america_el_soldado_del_invierno",
        "universe": "Marvel",
        "character": "Captain America",
        "title": "Capitán América: El Regreso del Soldado del Invierno",
        "theme_signature": "captain_america:winter_soldier:bucky_barnes_asesino_cosmic_cube",
        "description": "Steve Rogers descubre la desgarradora verdad: su querido hermano de armas Bucky Barnes sobrevivió a la guerra convertido en el despiadado asesino de HYDRA, el Soldado del Invierno.",
        "hashtags": "#CaptainAmerica #WinterSoldier #BuckyBarnes #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que tras décadas de creerlo muerto, el Capitán América descubrió que Bucky Barnes era el asesino más letal de HYDRA?",
            "Con un brazo biónico de titanio y la memoria borrada, el Soldado del Invierno ejecutó a cientos de objetivos en las sombras.",
            "Sometido a crueles cirugías en laboratorios clandestinos, le injertaron el implante cibernético para transformarlo en un arma letal.",
            "Al recuperar finalmente sus recuerdos perdidos, Bucky juró redimirse combatiendo las amenazas más oscuras del mundo."
        ],
        "scene_art_urls": [
            "assets/curated_panels/winter_soldier/scene_01.jpg",
            "assets/curated_panels/winter_soldier/scene_02.jpg",
            "assets/curated_panels/winter_soldier/scene_03.jpg",
            "assets/curated_panels/winter_soldier/scene_04.jpg"
        ],
        "art_queries": [
            "Captain America Winter Soldier snowy forest sniper comic panel",
            "Winter Soldier bionic arm cybernetic red star comic panel",
            "Winter Soldier surgical lab clandestine operation bionic arm panel",
            "Bucky Barnes redemption determination comic panel"
        ]
    },
    {
        "id": "ghost_rider_penance_stare_galactus",
        "universe": "Marvel",
        "character": "Ghost Rider",
        "title": "Ghost Rider: La Mirada de Penitencia a Galactus",
        "theme_signature": "ghost_rider:galactus:mirada_penitencia_trillones_almas",
        "description": "El día que Ghost Rider miró a los ojos al Devorador de Mundos Galactus, haciéndole sentir la agonía y el tormento de trillones de almas extintas.",
        "hashtags": "#GhostRider #Galactus #MarvelComics #PenanceStare #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que Ghost Rider utilizó su Mirada de Penitencia contra el mismísimo Devorador de Mundos Galactus?",
            "Ante el colosal titán cósmico, Danny Ketch encendió sus llamas del infierno y clavó su mirada en la deidad.",
            "Galactus experimentó instantáneamente el dolor y sufrimiento de trillones de seres que había devorado durante eones.",
            "Incapaz de soportar el peso de sus pecados cósmicos, el gigante cayó de rodillas derrotado por el Juicio del Espíritu."
        ],
        "art_queries": [
            "Ghost Rider staring down Galactus cosmic comic panel",
            "Ghost Rider flaming skull eyes penance stare comic panel",
            "Galactus screaming pain Penance Stare Ghost Rider comic panel",
            "Galactus falls to knees defeated Ghost Rider comic panel"
        ]
    },
    {
        "id": "dceased_infeccion_anti_vida_batman",
        "universe": "DC",
        "character": "Batman",
        "title": "DCeased: La Caída de Batman y la Trágica Despedida a Alfred",
        "theme_signature": "dceased:anti_vida:infeccion_batcueva_alfred",
        "description": "Cuando la Ecuación Anti-Vida infectó la Tierra a través de las pantallas, Batman fue mordido en la Baticueva y tuvo que despedirse de Alfred antes de perder la mente.",
        "hashtags": "#DCeased #Batman #Alfred #DCComics #AntiLifeVirus #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que cuando la Ecuación Anti-Vida infectó la Tierra, Batman vio a la humanidad sucumbir ante la locura digital?",
            "Nightwing y sus aliados infectados se transformaron en monstruos caníbales atacando brutalmente a sus seres queridos.",
            "Al ser mordido en combate, Batman se puso el traje de Mr. Freeze para retrasar el virus mortal.",
            "Roto de dolor en la oscuridad, Alfred activó el protocolo final para despedir a su amo."
        ],
        "scene_art_urls": [
            "assets/curated_panels/dceased_batman/scene_01.jpg",
            "assets/curated_panels/dceased_batman/scene_02.jpg",
            "assets/curated_panels/dceased_batman/scene_03.jpg",
            "assets/curated_panels/dceased_batman/scene_04.jpg"
        ],
        "art_queries": [
            "DCeased Batman Batcave computer infected world comic panel",
            "DCeased zombie Nightwing bloody monster comic panel",
            "DCeased Batman in Mr Freeze cryogenic suit infected comic panel",
            "DCeased Alfred Pennyworth weeping activating protocol final comic panel"
        ]
    },
    {
        "id": "batman_white_knight_joker_cuerdo",
        "universe": "DC",
        "character": "The Joker",
        "title": "Batman White Knight: El Día que el Joker se Volvió Cuerdo",
        "theme_signature": "joker:white_knight:jack_napier_cuerdo_juicio",
        "description": "En Batman White Knight, una sobredosis de medicamentos curó la psicopatía del Joker transformándolo en Jack Napier, el político que desenmascaró los crímenes de Batman.",
        "hashtags": "#BatmanWhiteKnight #TheJoker #JackNapier #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que en Batman White Knight, una sobredosis forzada de medicamentos curó por completo la locura del Joker?",
            "Convertido en el elocuente Jack Napier, denunció ante las cámaras de televisión la brutalidad ilegal y destructiva de Batman.",
            "Vistiendo un impecable traje blanco, se convirtió en líder popular y usó las leyes de Gotham para encarcelar al héroe.",
            "Por primera vez en la historia, Batman fue declarado el verdadero villano mientras el Joker era aclamado como salvador."
        ],
        "art_queries": [
            "Batman White Knight Joker pills sane Jack Napier comic panel",
            "Batman White Knight Jack Napier press conference television comic panel",
            "Jack Napier white suit lawyer Batman White Knight comic panel",
            "Batman arrested White Knight Sean Murphy comic panel"
        ]
    },
    {
        "id": "martian_manhunter_fernus_llama_ardiente",
        "universe": "DC",
        "character": "Martian Manhunter",
        "title": "Martian Manhunter: Fernus la Llama Ardiente",
        "theme_signature": "martian_manhunter:fernus:llama_ardiente_aniquilacion_liga",
        "description": "Al intentar superar su fobia al fuego, J'onn J'onzz liberó a Fernus la Llama Ardiente, la entidad marciana ancestral que humilló y destrozó a toda la Liga de la Justicia.",
        "hashtags": "#MartianManhunter #Fernus #JusticeLeague #DCComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que cuando Martian Manhunter superó su miedo al fuego, desató a un monstruo ancestral llamado Fernus?",
            "Esta encarnación ardiente poseía todo el arsenal de poderes marcianos sin ninguna de sus restricciones morales.",
            "Con telepatía destructiva y ferocidad implacable, Fernus doblegó a Superman, Wonder Woman y a toda la Liga de la Justicia.",
            "El mundo se salvó solo cuando el alma de J'onn J'onzz luchó desde el plano mental para destruir a la criatura para siempre."
        ],
        "art_queries": [
            "Martian Manhunter Fernus Burning Martian fire comic panel",
            "Fernus burning martian Justice League JLA Trial by Fire comic panel",
            "Fernus defeats Superman Justice League comic panel",
            "J'onn J'onzz defeats Fernus psychic battle comic panel"
        ]
    },
    {
        "id": "darth_vader_vader_down_hombres_muertos",
        "universe": "Star Wars / Marvel",
        "character": "Darth Vader",
        "title": "Darth Vader: Solo Veo Miedo y Hombres Muertos",
        "theme_signature": "darth_vader:vader_down:emboscada_hombres_muertos",
        "description": "Rodeado por un ejército rebelde entero con tanques y artillería pesada que le exigían rendición, Darth Vader encendió su sable carmesí y pronunció la frase más legendaria del cómic.",
        "hashtags": "#DarthVader #StarWars #VaderDown #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que tras estrellar su caza en el planeta Vrogas Vas, Darth Vader quedó solo en un desierto hostil?",
            "Un caza rebelde colisionó violentamente contra la nave de Vader en un choque aéreo devastador.",
            "Rodeado por el ejército enemigo, Vader encendió su sable y sentenció: 'Todo lo que veo es miedo... y hombres muertos'.",
            "Bajo una lluvia mortal de disparos láser, Vader desvió el fuego con la Fuerza y contraatacó implacable."
        ],
        "scene_art_urls": [
            "assets/curated_panels/darth_vader_down/scene_01.jpg",
            "assets/curated_panels/darth_vader_down/scene_02.jpg",
            "assets/curated_panels/darth_vader_down/scene_03.jpg",
            "assets/curated_panels/darth_vader_down/scene_04.jpg"
        ],
        "art_queries": [
            "Darth Vader alone desert Vrogas Vas surface comic panel",
            "Luke Skywalker X-wing crashes into Darth Vader TIE fighter comic panel",
            "Darth Vader all I am surrounded by is fear and dead men comic panel",
            "Darth Vader deflecting blaster fire with the Force comic panel"
        ]
    },
    {
        "id": "xmen_dias_del_futuro_pasado_centinelas",
        "universe": "Marvel",
        "character": "X-Men",
        "title": "Días del Futuro Pasado: El Exterminio Mutante de los Centinelas",
        "theme_signature": "x_men:days_of_future_past:sentinels_extermination_wolverine_logan",
        "description": "En un futuro postapocalíptico dominado por los Centinelas, los últimos mutantes son perseguidos y aniquilados en campos de concentración.",
        "hashtags": "#XMen #DaysOfFuturePast #Wolverine #Sentinels #MarvelComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que en Días del Futuro Pasado los gigantescos Centinelas cazaron y asesinaron a casi todos los mutantes?",
            "Los pocos X-Men supervivientes fueron encerrados en campos de concentración portando collares inhibidores de poder.",
            "Wolverine lideró un asalto desesperado, pero una ráfaga de plasma del Centinela redujo su cuerpo a cenizas.",
            "Enviando la mente de Kitty Pryde al pasado, los mutantes jugaron su última carta para reescribir la historia."
        ],
        "scene_art_urls": [
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_01.jpg",
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_02.jpg",
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_03.jpg",
            "assets/curated_panels/xmen_dias_del_futuro_pasado/scene_04.jpg"
        ],
        "art_queries": [
            "Days of Future Past Sentinel poster mutant gravestones comic panel",
            "X-Men concentration camp inhibitor collars John Byrne comic panel",
            "Wolverine disintegrated Sentinel blast Days of Future Past comic panel",
            "Kitty Pryde time travel mind transfer Days of Future Past comic panel"
        ]
    },
    {
        "id": "vengadores_desunidos_la_locura_de_wanda",
        "universe": "Marvel",
        "character": "Scarlet Witch",
        "title": "Vengadores Desunidos: El Día en que Wanda Destruyó a los Héroes",
        "theme_signature": "scarlet_witch:avengers_disassembled:wanda_maximoff_chaos_magic_vision",
        "description": "Al recordar a sus hijos borrados de la realidad, Wanda Maximoff pierde la cordura y desata su magia del caos contra la Mansión de los Vengadores.",
        "hashtags": "#ScarletWitch #Avengers #AvengersDisassembled #MarvelComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que la tragedia más devastadora de los Vengadores no fue provocada por un villano, sino por Wanda Maximoff?",
            "Al recordar a sus hijos perdidos, la mente de Wanda se quebró desatando una marea imparable de magia del caos.",
            "Un Jack of Hearts reanimado explotó sobre la Mansión y Visión colapsó atacando a sus propios compañeros de equipo.",
            "Entre los escombros y los cuerpos caídos, los Vengadores comprendieron que su era dorada había terminado."
        ],
        "art_queries": [
            "Scarlet Witch chaos magic Avengers Mansion explosion comic panel",
            "Jack of Hearts explodes Avengers Mansion David Finch comic panel",
            "Vision melting attacking Avengers Disassembled comic panel",
            "Avengers ruins fallen heroes Hawkeye Disassembled comic panel"
        ]
    },
    {
        "id": "daredevil_el_hombre_sin_miedo_origen_quimico",
        "universe": "Marvel",
        "character": "Daredevil",
        "title": "Daredevil: El Accidente Químico que Creó al Hombre Sin Miedo",
        "theme_signature": "daredevil:the_man_without_fear:blindness_toxic_waste_radar_sense",
        "description": "Matt Murdock salva a un anciano de ser atropellado por un camión, pero los desechos radiactivos le quitan la vista y despiertan sus sentidos hipersensibles.",
        "hashtags": "#Daredevil #MattMurdock #ManWithoutFear #MarvelComics #FrankMiller #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Matt Murdock obtuvo sus increíbles poderes salvando la vida de un anciano en Hell's Kitchen?",
            "Un camión perdió el control y un cilindro con desechos radiactivos impactó directamente en los ojos del joven Matt.",
            "La sustancia química le arrebató la vista para siempre, pero agudizó sus restantes cuatro sentidos a niveles superhumanos.",
            "Entrenado en secreto por el maestro ciego Stick, Matt juró proteger su barrio como el justiciero Daredevil."
        ],
        "scene_art_urls": [
            "assets/curated_panels/daredevil_hombre_sin_miedo/scene_01.jpg",
            "assets/curated_panels/daredevil_hombre_sin_miedo/scene_02.jpg",
            "assets/curated_panels/daredevil_hombre_sin_miedo/scene_03.jpg",
            "assets/curated_panels/daredevil_hombre_sin_miedo/scene_04.jpg"
        ],
        "art_queries": [
            "Young Matt Murdock saves blind man truck toxic waste comic panel",
            "Radioactive canister hits Matt Murdock eyes blinding comic panel",
            "Matt Murdock sensory overload radar sense hospital comic panel",
            "Stick training young Matt Murdock martial arts Man Without Fear panel"
        ]
    },
    {
        "id": "aquaman_mano_arpon_charybdis",
        "universe": "DC",
        "character": "Aquaman",
        "title": "Aquaman: El Día en que las Pirañas Devoraron su Mano",
        "theme_signature": "aquaman:harpoon_hand:charybdis_piranhas_peter_david",
        "description": "En una de las historias más oscuras de DC Comics, el villano Charybdis sumerge la mano de Arthur Curry en un pozo de pirañas carnívoras.",
        "hashtags": "#Aquaman #ArthurCurry #PeterDavid #DCComics #HarpoonHand #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Aquaman perdió su mano izquierda cuando un villano se la sumergió en un pozo de pirañas hambrientas?",
            "El sádico terrorista Charybdis neutralizó sus poderes telepáticos marinos y sostuvo el brazo de Arthur bajo el agua.",
            "En cuestión de segundos, los peces devoraron la carne viva de su mano hasta dejar los huesos completamente expuestos.",
            "En lugar de rendirse, Arthur se colocó un arpón metálico retráctil convirtiéndose en el rey guerrero de Atlantis."
        ],
        "art_queries": [
            "Aquaman fight Charybdis Time and Tide Peter David comic panel",
            "Charybdis forces Aquaman hand piranha pool comic panel",
            "Aquaman screaming skeletal hand piranha bite comic panel",
            "Aquaman harpoon hand beard shirtless warrior king comic panel"
        ]
    },
    {
        "id": "green_lantern_kyle_rayner_major_force",
        "universe": "DC",
        "character": "Kyle Rayner",
        "title": "Kyle Rayner: El Día en que Major Force Asesinó a su Novia",
        "theme_signature": "kyle_rayner:green_lantern:major_force_refrigerator_alex",
        "description": "El brutal momento en que el nuevo Green Lantern Kyle Rayner regresa a su departamento y descubre que Major Force asesinó a su novia Alex DeWitt.",
        "hashtags": "#GreenLantern #KyleRayner #MajorForce #DCComics #RonMarz #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Kyle Rayner vivió una de las tragedias más impactantes de DC apenas días después de recibir su anillo?",
            "El despiadado villano Major Force fue enviado por el gobierno para arrebatarle el último anillo de Green Lantern.",
            "Al entrar a su departamento en Nueva York, Kyle encontró una nota sobre el refrigerador y al abrirlo vio el cuerpo sin vida de su novia.",
            "Enceguecido por la furia esmeralda, Kyle desató todo el poder del anillo derrotando a Major Force en una feroz batalla."
        ],
        "art_queries": [
            "Kyle Rayner Green Lantern apartment Alex DeWitt comic panel",
            "Major Force Green Lantern 54 Ron Marz comic panel",
            "Kyle Rayner finds Alex refrigerator Green Lantern 54 comic panel",
            "Green Lantern Kyle Rayner green energy blast Major Force comic panel"
        ]
    },
    {
        "id": "doctor_strange_dormammu_bucle_dimension_oscura",
        "universe": "Marvel",
        "character": "Doctor Strange",
        "title": "Doctor Strange: El Duelo Eterno contra Dormammu en la Dimensión Oscura",
        "theme_signature": "doctor_strange:dormammu:dark_dimension_eternity_clea",
        "description": "Doctor Strange viaja a la aterradora Dimensión Oscura para desafiar a la entidad cósmica Dormammu y salvar la Tierra.",
        "hashtags": "#DoctorStrange #Dormammu #DarkDimension #MarvelComics #SteveDitko #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías que Doctor Strange desafió solo al dios de la Dimensión Oscura para evitar que devorara nuestra realidad?",
            "Dormammu, un ser titánico de puro fuego místico, juró convertir la Tierra en parte de su reino de pesadilla.",
            "Con el Ojo de Agamotto brillando en su pecho, Strange tejió un laberinto de hechizos antiguos contra las llamas oscuras.",
            "Incapaz de doblegar la voluntad del Hechicero Supremo, Dormammu tuvo que pactar y jurar jamás invadir la Tierra."
        ],
        "scene_art_urls": [
            "assets/curated_panels/doctor_strange_dormammu/scene_01.jpg",
            "assets/curated_panels/doctor_strange_dormammu/scene_02.jpg",
            "assets/curated_panels/doctor_strange_dormammu/scene_03.jpg",
            "assets/curated_panels/doctor_strange_dormammu/scene_04.jpg"
        ],
        "art_queries": [
            "Doctor Strange enters Dark Dimension Steve Ditko comic panel",
            "Dormammu giant flaming head cosmic demon Steve Ditko comic panel",
            "Doctor Strange Eye of Agamotto mystical shields battle comic panel",
            "Doctor Strange defeats Dormammu mystical oath Ditko comic panel"
        ]
    },
    {
        "id": "sentry_nacimiento_del_vacio",
        "universe": "Marvel",
        "character": "The Sentry",
        "title": "Sentry: La Maldición del Vacío y la Muerte del Millón de Soles",
        "theme_signature": "sentry:the_void:oscuridad_robert_reynolds",
        "description": "Robert Reynolds descubre la aterradora verdad de sus poderes divinos: cada milagro que realiza da vida al Vacío, una entidad cósmica capaz de consumir la Tierra.",
        "hashtags": "#Sentry #TheVoid #MarvelComics #Avengers #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías que el héroe más poderoso de Marvel esconde un monstruo capaz de devorar planetas?",
            "Robert Reynolds descubrió que cada milagro que realizaba como Sentry daba vida a su contraparte: el Vacío.",
            "El Vacío emergió como una tormenta de sombras vivientes, destruyendo Asgard y quebrando a los Vengadores.",
            "Para salvar al universo, Robert suplicó a Thor que lo ejecutara con un rayo fulminante."
        ],
        "art_queries": [
            "Sentry glowing golden power comic panel",
            "The Void cosmic darkness monster shadowy entity comic panel",
            "The Void destroys Asgard Siege Marvel comic panel",
            "Thor kills Sentry lightning bolt funeral comic panel"
        ]
    },
    {
        "id": "magneto_venganza_red_skull",
        "universe": "Marvel",
        "character": "Magneto",
        "title": "Magneto vs Red Skull: El Castigo del Holocausto en el Búnker",
        "theme_signature": "magneto:red_skull:bunker_entierro_auschwitz",
        "description": "Como superviviente del Holocausto, Magneto captura a Red Skull y rechaza darle una muerte rápida, encerrándolo vivo en un búnker subterráneo eterno.",
        "hashtags": "#Magneto #RedSkull #XMen #CaptainAmerica #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "¿Sabías que cuando Magneto capturó a Red Skull se negó a asesinarlo con sus poderes mutantes?",
            "Como superviviente de Auschwitz, Magneto despreciaba la ideología nazi más que a cualquier enemigo en la Tierra.",
            "Encerró al líder de Hydra en un búnker subterráneo blindado, sin luz, sin aire y sin salida.",
            "Dejándole solo un poco de agua, lo abandonó a una agonía eterna en la oscuridad."
        ],
        "art_queries": [
            "Magneto confronting Red Skull comic panel Acts of Vengeance",
            "Magneto holocaust survivor tattoo memory comic panel",
            "Magneto burying Red Skull underground bunker comic panel",
            "Red Skull trapped in dark bunker tomb comic panel"
        ]
    },
    {
        "id": "flash_muerte_iris_west",
        "universe": "DC",
        "character": "The Flash",
        "title": "The Flash: La Noche en que Eobard Thawne Asesinó a Iris West",
        "theme_signature": "flash:iris_west:vibracion_craneal_fiesta_disfraces",
        "description": "Eobard Thawne viaja en el tiempo para ejecutar el crimen más devastador en la vida de Barry Allen: asesinar a su esposa Iris West durante una fiesta.",
        "hashtags": "#TheFlash #ReverseFlash #BarryAllen #DCComics #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que el mayor dolor de Barry Allen comenzó en una fiesta de disfraces en Central City?",
            "El villano Reverse-Flash se infiltró en el evento obsesionado con destruir para siempre la felicidad de Flash.",
            "Al negarse Iris a amarlo, Thawne vibró sus dedos a súper velocidad atravesando su cráneo.",
            "Barry llegó solo para encontrar el cuerpo inerte de su amada esposa en el suelo frío."
        ],
        "art_queries": [
            "Barry Allen Iris West costume party The Flash 275 comic panel",
            "Reverse Flash Eobard Thawne smiling evil speedster comic panel",
            "Reverse Flash kills Iris West vibrating hand head comic panel",
            "Barry Allen crying holding dead Iris West comic panel"
        ]
    },
    {
        "id": "black_panther_derrota_mephisto",
        "universe": "Marvel",
        "character": "Black Panther",
        "title": "Black Panther: El Rey de Wakanda que Engañó al Demonio Mephisto",
        "theme_signature": "black_panther:t_challa:engano_infierno_dios_pantera",
        "description": "T'Challa desciende al reino infernal y engaña al señor de las mentiras Mephisto, usando la fuerza espiritual de los reyes pasados de Wakanda.",
        "hashtags": "#BlackPanther #Mephisto #MarvelComics #Wakanda #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que Black Panther viajó al infierno y logró derrotar al mismísimo demonio Mephisto?",
            "El señor del infierno exigió el alma del rey de Wakanda a cambio de salvar a su nación.",
            "T'Challa aceptó el pacto, pero liberó el espíritu de todos los ancestros de la Pantera Negra.",
            "Los antiguos reyes despedazaron al demonio desde su propio interior, expulsándolo derrotado de su reino."
        ],
        "art_queries": [
            "Black Panther confronting Mephisto hell Christopher Priest comic panel",
            "Mephisto demon laughing flaming throne Marvel comic panel",
            "Black Panther Panther God spirits attacking Mephisto comic panel",
            "T'Challa standing victorious leaving hell comic panel"
        ]
    },
    {
        "id": "batman_adiccion_venom_origen",
        "universe": "DC",
        "character": "Batman",
        "title": "Batman: La Oscura Adicción al Veneno en las Sombras",
        "theme_signature": "batman:venom_addiction:pastillas_cueva_fuerza_extrema",
        "description": "Tras fracasar en el rescate de una niña atrapada, Bruce Wayne recurre a una peligrosa droga experimental para superar sus límites humanos.",
        "hashtags": "#Batman #Venom #DCComics #LegendsOfTheDarkKnight #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que tras no poder salvar a una niña atrapada, Batman cayó en una oscura adicción?",
            "Frustrado por sus límites físicos, Bruce Wayne comenzó a consumir un esteroide experimental llamado Veneno.",
            "La sustancia le dio fuerza monstruosa, pero nubló su mente volviéndolo violento, paranoico e incontrolable.",
            "Para purgarse, Batman se encerró durante un mes en la cueva viviendo un infierno de abstinencia."
        ],
        "art_queries": [
            "Batman failing to lift boulder drowning girl Legends of Dark Knight comic panel",
            "Bruce Wayne taking venom pills dark room comic panel",
            "Batman raging aggressive steroid venom comic panel",
            "Batman locked in batcave detox withdrawal beard comic panel"
        ]
    },
    {
        "id": "green_lantern_hal_destruccion_oa",
        "universe": "DC",
        "character": "Green Lantern",
        "title": "Green Lantern: La Masacre de Hal Jordan en la Batería de Oa",
        "theme_signature": "hal_jordan:destruccion_oa:diez_anillos_muerte_kilowog",
        "description": "Enloquecido por el dolor tras la destrucción de Coast City, el mejor Linterna Verde del universo aniquila a sus hermanos de armas en busca de poder absoluto.",
        "hashtags": "#GreenLantern #HalJordan #Parallax #EmeraldTwilight #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "¿Sabías que tras la destrucción de Coast City, Hal Jordan enloqueció y masacró a los Green Lanterns?",
            "Desesperado por reconstruir su ciudad natal, voló hacia el planeta Oa asesinando a sus propios compañeros.",
            "Arrancó diez anillos de poder de sus cadáveres y masacró al gigante Kilowog a sangre fría.",
            "Sumergiéndose en la Batería Central, absorbió toda la energía cósmica renaciendo como el villano Parallax."
        ],
        "art_queries": [
            "Hal Jordan grief Coast City destroyed Emerald Twilight comic panel",
            "Hal Jordan fighting Green Lanterns space battle comic panel",
            "Hal Jordan wearing multiple power rings hands comic panel",
            "Hal Jordan entering Central Power Battery Parallax armor comic panel"
        ]
    },
    {
        "id": "wolverine_x23_olor_detonante",
        "universe": "Marvel",
        "character": "X-23",
        "title": "X-23: El Olor Detonante y el Trágico Asesinato de su Madre",
        "theme_signature": "x23:laura_kinney:olor_detonante_asesinato_sarah_kinney",
        "description": "El brutal origen de Laura Kinney: convertida en una asesina desde niña, un compuesto químico la obliga a cometer su mayor pecado.",
        "hashtags": "#X23 #Wolverine #LauraKinney #XMen #MarvelComics #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que la clon de Wolverine, Laura Kinney, fue diseñada como el arma más sanguinaria del mundo?",
            "Científicos del proyecto crearon un aroma sintético capaz de nublar su mente y desatar furia asesina.",
            "Sometida al olor detonante durante una fuga, Laura perdió el control y atacó a su creadora.",
            "Al recobrar la conciencia, descubrió con horror que acababa de asesinar a su propia madre."
        ],
        "art_queries": [
            "Young Laura Kinney X-23 claws surgical facility comic panel",
            "X-23 berserker rage trigger scent red eyes comic panel",
            "X-23 slashing facility soldiers claws comic panel",
            "X-23 crying holding dying mother Sarah Kinney comic panel"
        ]
    },
    {
        "id": "namor_inundacion_wakanda_avx",
        "universe": "Marvel",
        "character": "Namor",
        "title": "Namor: La Gran Inundación que Ahogó a Wakanda",
        "theme_signature": "namor:phoenix_force:tsunami_wakanda_avx_guerra",
        "description": "Namor desata el poder del Fénix sobre Wakanda provocando una inundación catastrófica que marca a fuego la rivalidad con Pantera Negra.",
        "hashtags": "#Namor #BlackPanther #AvengersVsXMen #MarvelComics #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que durante la guerra entre Vengadores y X-Men, Namor cometió el mayor genocidio en Wakanda?",
            "Empoderado por una quinta parte de la Fuerza Fénix, el rey atlante marchó con furia imparable.",
            "Invocó un colosal tsunami cósmico que azotó la ciudad dorada ahogando a miles de inocentes.",
            "El ataque quebró el orgullo de Pantera Negra e inició una guerra eterna entre ambas naciones."
        ],
        "art_queries": [
            "Namor Phoenix Five glowing fire suit comic panel",
            "Namor summoning giant tidal wave tsunami ocean comic panel",
            "Tsunami crushing Wakanda golden city water flood comic panel",
            "Black Panther standing in ruined flooded Wakanda comic panel"
        ]
    },
    {
        "id": "punisher_jigsaw_desfiguracion_billy_russo",
        "universe": "Marvel",
        "character": "The Punisher",
        "title": "The Punisher: El Rostro Destrozado de Billy Russo",
        "theme_signature": "the_punisher:billy_russo:jigsaw_trituradora_cristales",
        "description": "Frank Castle ejecuta su venganza contra el sicario de la mafia Billy Russo, arrojándolo contra los cristales para crear a su enemigo más temido.",
        "hashtags": "#ThePunisher #Jigsaw #BillyRusso #MarvelComics #ComicsNarrados #Shorts #Reels #TikTok",
        "scenes": [
            "¿Sabías cómo Frank Castle creó a su archienemigo más perturbador en el bajo mundo de Nueva York?",
            "Tras eliminar a una banda de asesinos, The Punisher acorraló al sádico sicario Billy Russo.",
            "En lugar de dispararle, Frank arrojó brutalmente a Russo de cabeza contra una enorme cristalera.",
            "Los cirujanos reconstruyeron su rostro como un rompecabezas sangriento, naciendo el temido monstruo Jigsaw."
        ],
        "scene_art_urls": [
            "assets/curated_panels/punisher_jigsaw/scene_01.jpg",
            "assets/curated_panels/punisher_jigsaw/scene_02.jpg",
            "assets/curated_panels/punisher_jigsaw/scene_03.jpg",
            "assets/curated_panels/punisher_jigsaw/scene_04.jpg"
        ],
        "art_queries": [
            "Frank Castle The Punisher skull vest aiming gun comic panel",
            "Billy Russo handsome mob hitman suit comic panel",
            "Punisher smashing Billy Russo face through glass window comic panel",
            "Jigsaw stitched face monster bandages mirror comic panel"
        ]
    },
    {
        "id": "damian_wayne_muerte_hereje",
        "universe": "DC",
        "character": "Robin (Damian Wayne)",
        "title": "Robin: El Trágico Sacrificio y Muerte de Damian Wayne",
        "theme_signature": "damian_wayne:the_heretic:espada_empalamiento_torre_wayne",
        "description": "El hijo de Batman lucha hasta el final contra un clon titánico para proteger la ciudad de Gotham, entregando su vida con apenas diez años.",
        "hashtags": "#Robin #DamianWayne #Batman #BatmanIncorporated #DCComics #ComicsNarrados #Reels",
        "scenes": [
            "¿Sabías que el hijo de Batman, Damian Wayne, murió defendiendo Gotham con apenas diez años?",
            "Durante el asedio a la Torre Wayne, un clon monstruoso llamado El Hereje acorraló al joven Robin.",
            "Luchando con honor hasta el último aliento, Damian fue atravesado en el pecho por una espada gigantesca.",
            "Batman llegó demasiado tarde, encontrando el cadáver de su único hijo bañado en lágrimas de dolor."
        ],
        "art_queries": [
            "Damian Wayne Robin fighting sword Wayne Tower comic panel",
            "The Heretic giant clone brute Batman Inc comic panel",
            "The Heretic impales Damian Wayne sword splash page comic panel",
            "Batman holding dead Damian Wayne crying rain comic panel"
        ]
    },
    {
        "id": "doctor_fate_nabu_posesion_divina",
        "universe": "DC",
        "character": "Doctor Fate",
        "title": "Doctor Fate: La Posesión de Nabu y el Sacrificio Humano",
        "theme_signature": "doctor_fate:nabu:yelmo_dorado_posesion_hechicero",
        "description": "Kent Nelson descubre el aterrador precio de portar el Casco de Nabu: cada vez que invoca su magia, la entidad cósmica toma el control absoluto de su cuerpo borrando su humanidad.",
        "hashtags": "#DoctorFate #DCComics #JusticeSociety #Nabu #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que el casco dorado de Doctor Fate borra por completo la humanidad de quien lo porta?",
            "Cuando Kent Nelson se coloca el yelmo, su cuerpo es poseído por la entidad milenaria Nabu.",
            "Nabu utiliza su carne como una marioneta despiadada, desintegrando a sus rivales con magia cósmica.",
            "Al quitárselo, Nelson despierta envejecido y aterrado, comprendiendo que ya no es dueño de su alma."
        ],
        "art_queries": [
            "Doctor Fate helmet comic panel",
            "Kent Nelson glowing eyes Nabu comic panel",
            "Doctor Fate spell magic symbol comic panel",
            "Doctor Fate removing helmet exhausted comic panel"
        ]
    },
    {
        "id": "ghost_rider_zarathos_posesion_oscura",
        "universe": "Marvel",
        "character": "Ghost Rider",
        "title": "Ghost Rider: La Furia Desatada de Zarathos y el Fuego Infernal",
        "theme_signature": "ghost_rider:zarathos:posesion_fuego_infernal_maldicion",
        "description": "Cuando Johnny Blaze pierde el control emocional, el antiguo demonio Zarathos toma el mando total desatando una masacre de fuego que calcina el alma de sus enemigos.",
        "hashtags": "#GhostRider #MarvelComics #Zarathos #MidnightSons #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías que el Espíritu de la Venganza no es un poder, sino una maldición que devora almas?",
            "Cuando Johnny Blaze pierde el control emocional, el antiguo demonio Zarathos toma el mando total de su cuerpo.",
            "Envuelto en fuego infernal indestructible, Zarathos calcina a los criminales con una crueldad sin límites.",
            "Blaze queda atrapado dentro de su propia mente, condenado a presenciar la masacre sin poder detenerla."
        ],
        "art_queries": [
            "Ghost Rider flaming skull comic panel",
            "Johnny Blaze turning Ghost Rider comic panel",
            "Ghost Rider hellfire chain comic panel",
            "Ghost Rider penance stare comic panel"
        ]
    },
    {
        "id": "constantine_engano_triunvirato_infierno",
        "universe": "DC",
        "character": "John Constantine",
        "title": "John Constantine: El Engaño al Triunvirato del Infierno",
        "theme_signature": "constantine:dangerous_habits:triunvirato_infierno_cancer",
        "description": "Agonizando por un cáncer terminal, John Constantine vende su alma a los tres reyes del infierno por separado, forzándolos a salvarle la vida para evitar una guerra cósmica.",
        "hashtags": "#Constantine #Hellblazer #DCComics #Vertigo #ComicsNarrados #Shorts #Reels",
        "scenes": [
            "¿Sabías cómo John Constantine engañó a los tres señores del infierno para salvar su propia vida?",
            "Agonizando por un cáncer terminal, Constantine vendió su alma a los tres reyes demoníacos por separado.",
            "Al enterarse de que reclamarlo desataría una guerra sangrienta entre ellos, los demonios se vieron forzados a curarlo.",
            "El estafador de lo oculto sonrió victorioso, fumando un cigarrillo frente a la furia de los señores infernales."
        ],
        "art_queries": [
            "John Constantine trench coat lighter Hellblazer comic panel",
            "Constantine selling soul devil contract comic panel",
            "Three lords of hell devils angry comic panel",
            "Constantine smiling smoking middle finger comic panel"
        ]
    },
    {
        "id": "magneto_atracciones_fatales_adamantium",
        "universe": "Marvel",
        "character": "Magneto",
        "title": "Magneto: La Extracción Brutal del Adamantium de Wolverine",
        "theme_signature": "magneto:fatal_attractions:extraccion_adamantium_avalon",
        "description": "En una de las escenas más sangrientas de Marvel, Magneto utiliza su control magnético absoluto para arrancar el metal líquido directamente de los huesos de Wolverine.",
        "hashtags": "#Magneto #Wolverine #XMen #FatalAttractions #MarvelComics #ComicsNarrados #Reels",
        "scenes": [
            "¿Sabías cuál fue la tortura más brutal y sanguinaria que sufrió Wolverine a manos de Magneto?",
            "Durante la batalla espacial en Avalon, Wolverine atravesó el pecho de Magneto con sus garras de adamantium.",
            "Enloquecido de ira, el maestro del magnetismo controló el metal fundido adherido a los huesos de Logan.",
            "Magneto arrancó el adamantium líquido desgarrando su piel y músculos, dejándolo al borde de la muerte definitiva."
        ],
        "art_queries": [
            "Wolverine slashing Magneto chest claws Avalon comic panel",
            "Magneto ripping adamantium Wolverine Fatal Attractions comic panel",
            "Adamantium liquid coming out Wolverine pores comic panel",
            "Wolverine dying bleeding bone claws comic panel"
        ]
    },
    {
        "id": "carnage_ravencroft_masacre_origen",
        "universe": "Marvel",
        "character": "Carnage",
        "title": "Carnage: La Masacre Sangrienta en Ravencroft y el Nacimiento del Monstruo",
        "theme_signature": "carnage:cletus_kasady:ravencroft_sangre_nacimiento",
        "description": "Cletus Kasady se fusiona con la descendencia de Venom a través de su propio torrente sanguíneo, desatando al psicópata simbiótico más sádico en la prisión de Ravencroft.",
        "hashtags": "#Carnage #Venom #SpiderMan #MaximumCarnage #MarvelComics #ComicsNarrados #Shorts",
        "scenes": [
            "¿Sabías cómo nació Carnage en una diminuta celda de máxima seguridad en Nueva York?",
            "El asesino serial Cletus Kasady compartía celda con Eddie Brock cuando el simbionte Venom acudió a rescatarlo.",
            "Al escapar, el simbionte dejó un residuo rojizo que se filtró directamente en la sangre de Kasady.",
            "Fusionado con su torrente sanguíneo, Cletus desató una carnicería imparable riendo mientras aniquilaba a los guardias de Ravencroft."
        ],
        "art_queries": [
            "Cletus Kasady prison cell Ravencroft comic panel",
            "Venom symbiote leaving red offspring comic panel",
            "Carnage first transformation red tendrils comic panel",
            "Carnage killing prison guards laughing comic panel"
        ]
    }
]

# Configuración automática de voz Puck (Gemini 3.8 TTS) para todas las historias editoriales
for _s in EDITORIAL_STORIES:
    _s.setdefault("voice", "Puck")
    _s.setdefault("tts_model", "gemini-3.8-flash-tts")
    _s.setdefault("fallback_tts_model", "gemini-3.8-flash-lite-tts")
    _s.setdefault("style_direction", "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano")

