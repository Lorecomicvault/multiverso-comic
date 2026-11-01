"""
PRODUCCIÓN DEL VIDEO LARGO PARA YOUTUBE:
TODO LO QUE DEBES SABER DE DOCTOR DOOM ANTES DE AVENGERS: DOOMSDAY (HISTORIA COMPLETA)
===================================================================================
- Formato: 16:9 Full HD (1920x1080) Widescreen
- Voz: Voicebox neuronal (Qwen-TTS, Perfil 'Narrador Referencia Cómic')
- Viñetas: 100% CANÓNICAS Y ULTRA-PRECISAS de Books of Doom #1-6, Secret Wars #1-9, Fantastic Four #57, Infamous Iron Man #1
- Subtítulos: Comic Subtitles centrados abajo, blanco con borde negro de alto contraste
- Cámara: Movimiento cinemático Ken Burns (zoom-in, pan, zoom-out sutil)
- Música: Banda sonora orquestal cinemática sutil de misterio/tensión
"""

import os
import sys
import json
import time
import shutil
import subprocess
import requests
from PIL import Image, ImageFilter

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "doctor_doom_doomsday_long")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
PANELS_RAW = os.path.join(OUTPUT_DIR, "panels_raw")
PANELS_1080P = os.path.join(OUTPUT_DIR, "panels_1080p")
CLIPS_DIR = os.path.join(OUTPUT_DIR, "clips")
THUMBNAILS_DIR = os.path.join(OUTPUT_DIR, "thumbnails")

for d in [OUTPUT_DIR, AUDIO_DIR, PANELS_RAW, PANELS_1080P, CLIPS_DIR, THUMBNAILS_DIR]:
    os.makedirs(d, exist_ok=True)

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2" # Narrador Referencia Cómic

SCENES = [
    # --- ACTO 1: EL IMPACTO DEL ANUNCIO Y LA VERDADERA NATURALEZA DE DOOM ---
    {
        "id": 1,
        "act": "Acto 1: El Shock del Multiverso",
        "text": "El anuncio de Robert Downey Jr. como Victor von Doom sacudió los cimientos de Marvel. Pero para comprender la verdadera magnitud de lo que se avecina en Avengers: Doomsday, debemos olvidar la armadura de Iron Man.",
        "search_term": "Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 2,
        "act": "Acto 1: El Shock del Multiverso",
        "text": "Doctor Doom no es un simple villano de cómic. Es la mente más calculadora, peligrosa y trágicamente compleja que jamás haya pisado el Universo Marvel.",
        "search_term": "Books of Doom Vol 1 6 Victor von Doom",
        "comic_source": "Books of Doom #6"
    },
    {
        "id": 3,
        "act": "Acto 1: El Shock del Multiverso",
        "text": "A diferencia de Thanos, que dependía de las Gemas del Infinito, o Kang, que depende de sus variantes temporales, el poder de Doom reside en una combinación aterradora: es el segundo científico más brillante del planeta, y a la vez, el segundo hechicero más letal después del Hechicero Supremo.",
        "search_term": "Doctor Strange Doctor Doom Triumph and Torment",
        "comic_source": "Triumph and Torment"
    },
    {
        "id": 4,
        "act": "Acto 1: El Shock del Multiverso",
        "text": "Esta síntesis perfecta entre tecnología cuántica y magia arcana convierte a Victor von Doom en una amenaza imposible de clasificar, un hombre que no busca destruir el mundo, sino gobernarlo porque cree firmemente que es el único capaz de salvarlo.",
        "search_term": "Books of Doom Vol 1 3 Doctor Doom armor",
        "comic_source": "Books of Doom #3"
    },

    # --- ACTO 2: EL ORIGEN TRÁGICO: LATVERIA Y EL PACTO INFERNAL ---
    {
        "id": 5,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Todo comenzó en los fríos valles de Latveria. Allí, bajo la tiranía opresiva del Rey Vladimir, una pequeña tribu de gitanos Zefiro intentaba subsistir en la miseria.",
        "search_term": "Books of Doom Vol 1 1 Latveria Zefiro",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 6,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Entre ellos nació Victor, hijo de Werner von Doom, un respetado médico herbolario, y Cynthia von Doom, una mujer que escondía un secreto místico prohibido.",
        "search_term": "Werner von Doom Cynthia von Doom Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 7,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Desesperada por liberar a su pueblo de las cadenas de los soldados latverianos, Cynthia recurrió a las artes oscuras y selló un pacto de sangre con el mismísimo señor del inframundo: Mefisto.",
        "search_term": "Cynthia von Doom Mephisto Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },
    {
        "id": 8,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Pero la magia demoníaca tiene un precio brutal. Cuando Cynthia usó su poder para castigar a los guardias, el conjuro se descontroló cobrando la vida de inocentes. Mortalmente herida y maldita, Cynthia murió en los brazos de Werner.",
        "search_term": "Cynthia von Doom death Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 9,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "El alma de Cynthia fue arrastrada al abismo infernal, donde Mefisto la condenó a una eternidad de tormento. Esta herida psicológica jamás cerraría en el corazón del pequeño Victor.",
        "search_term": "Cynthia von Doom Hell Mephisto Triumph and Torment",
        "comic_source": "Triumph and Torment"
    },
    {
        "id": 10,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "La tragedia no terminó ahí. Cuando la esposa del Barón enfermó de muerte, este amenazó a Werner con ejecutar a todo su clan si no la salvaba. Incapaz de curarla, Werner tomó al niño Victor y huyeron a través de la ventisca helada.",
        "search_term": "Werner von Doom Victor escape blizzard Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 11,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "En medio de la tormenta de nieve, Werner se despojó de sus propias ropas para abrigar a su hijo. Victor sobrevivió, pero su padre murió congelado protegiéndolo con su último aliento.",
        "search_term": "Werner von Doom death ice Victor Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 12,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Huérfano y devorado por el dolor, Victor descubrió el baúl oculto de su madre, repleto de antiguos grimorios, pociones y talismanes de brujería gitana.",
        "search_term": "Victor von Doom chest mother sorcery Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 13,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Victor juró vengarse del mundo. Comenzó a fusionar los hechizos maternos con mecanismos mecánicos de precisión, creando inventos con los que ridiculizaba y saboteaba sistemáticamente al ejército latveriano.",
        "search_term": "Victor von Doom inventions young Books of Doom Vol 1 1",
        "comic_source": "Books of Doom #1"
    },
    {
        "id": 14,
        "act": "Acto 2: La Tragedia en Latveria",
        "text": "Su prodigioso intelecto cruzó fronteras. El gobierno de los Estados Unidos, asombrado por sus planos científicos, le ofreció una beca de honor en la Universidad Empire State de Nueva York.",
        "search_term": "Victor von Doom scholarship Empire State Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },

    # --- ACTO 3: LA RIVALIDAD CON REED RICHARDS Y LA MÁSCARA DE HIERRO ---
    {
        "id": 15,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Fue en los pasillos universitarios donde el destino unió a Victor con su eterno rival: Reed Richards. Ambos eran titanes intelectuales, pero mientras Reed personificaba la humildad y la ciencia pura, Doom destilaba soberbia.",
        "search_term": "Reed Richards Victor von Doom Empire State Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },
    {
        "id": 16,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Obsesionado con un único propósito, Victor construyó en secreto un proyector dimensional para traspasar la barrera del más allá y rescatar el alma de su madre de las garras de Mefisto.",
        "search_term": "Victor machine netherworld Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },
    {
        "id": 17,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Reed Richards examinó de reojo las ecuaciones de la máquina y le advirtió de inmediato: «Victor, tienes un error decimal en los cálculos. Si activas el dispositivo, la sobrecarga será catastrófica».",
        "search_term": "Reed warns Victor calculations Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },
    {
        "id": 18,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Ofendido de que alguien osara corregirlo, Doom encendió el portal. El generador estalló en una brutal onda expansiva que destruyó el laboratorio y lanzó a Victor contra los cristales rotos.",
        "search_term": "Machine explosion Victor face Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },
    {
        "id": 19,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "La explosión le dejó una pequeña cicatriz en el rostro. Para cualquier otro hombre no habría sido nada, pero para la vanidad absoluta de Victor, su perfección física había sido destruida para siempre.",
        "search_term": "Victor von Doom scarred mirror Books of Doom Vol 1 2",
        "comic_source": "Books of Doom #2"
    },
    {
        "id": 20,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Culpando ciegamente a Reed Richards de sabotaje, Victor fue expulsado de la universidad. Despojado de todo, vagó por el mundo hasta llegar a los monasterios más aislados del Tíbet.",
        "search_term": "Victor Tibet monastery monks Books of Doom Vol 1 3",
        "comic_source": "Books of Doom #3"
    },
    {
        "id": 21,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Allí se encontró con una misteriosa hermandad de monjes versados en alquimia y metalurgia arcana. En pocos meses, Victor aprendió todos sus secretos y se convirtió en su maestro indiscutido.",
        "search_term": "Victor master monks Tibet Books of Doom Vol 1 3",
        "comic_source": "Books of Doom #3"
    },
    {
        "id": 22,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Bajo sus órdenes, los monjes forjaron una armadura completa de titanio. Pero impaciente por consumar su transformación, Doom no esperó a que el metal se enfriara.",
        "search_term": "Monks forge mask Doctor Doom Books of Doom Vol 1 3",
        "comic_source": "Books of Doom #3"
    },
    {
        "id": 23,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Con tenazas de hierro, ordenó a los monjes estampar la máscara incandescente directamente sobre su carne viva. El calor derritió su piel, sellando su rostro con acero para siempre. El hombre había muerto; nació el Doctor Doom.",
        "search_term": "Doom molten mask red hot Books of Doom Vol 1 3",
        "comic_source": "Books of Doom #3"
    },
    {
        "id": 24,
        "act": "Acto 3: La Máscara de Hierro",
        "text": "Doom regresó a Latveria con poderío imparable. Aplastó las tropas del tirano Vladimir, derrocó a la monarquía corrupta y se coronó a sí mismo como el Soberano Supremo de Latveria.",
        "search_term": "Doom throne Latveria crowned Books of Doom Vol 1 4",
        "comic_source": "Books of Doom #4"
    },

    # --- ACTO 4: LAS MAYORES HUMILLACIONES Y ROBO DE PODER CÓSMICO ---
    {
        "id": 25,
        "act": "Acto 4: El Ladrón de Dioses",
        "text": "Bajo su puño de hierro, Latveria se transformó en una utopía hipertecnológica con cero pobreza y cero crimen, resguardada por legiones de centinelas mecánicos: los temidos Doombots.",
        "search_term": "Doombot Books of Doom Vol 1 6",
        "comic_source": "Books of Doom #6"
    },
    {
        "id": 26,
        "act": "Acto 4: El Ladrón de Dioses",
        "text": "Pero la ambición de Doom no conocía fronteras terrestres. En Fantastic Four número 57, Victor invitó cordialmente al Silver Surfer a su castillo, solo para tenderle una emboscada maestra.",
        "search_term": "Fantastic Four Vol 1 57 Silver Surfer Doctor Doom",
        "comic_source": "Fantastic Four #57"
    },
    {
        "id": 27,
        "act": "Acto 4: El Ladrón de Dioses",
        "text": "Con un dispositivo bioeléctrico de su propia creación, Doom drenó la totalidad del Poder Cósmico del heraldo de Galactus, montó su tabla plateada y se convirtió en una deidad cósmica imparable.",
        "search_term": "Doom Silver Surfer cosmic power Fantastic Four 57",
        "comic_source": "Fantastic Four #57"
    },
    {
        "id": 28,
        "act": "Acto 4: El Ladrón de Dioses",
        "text": "Años después, en las legendarias Guerras Secretas de 1984, una entidad omnipotente conocida como el Beyonder transportó a los mayores héroes y villanos a Battleworld para combatir por diversión.",
        "search_term": "Secret Wars 1984 Doctor Doom Beyonder",
        "comic_source": "Secret Wars (1984) #10"
    },
    {
        "id": 29,
        "act": "Acto 4: El Ladrón de Dioses",
        "text": "Lejos de jugar el juego del Beyonder, Doom utilizó tecnología de absorción para doblegar a Galactus y despojar al mismísimo Beyonder de su omnipotencia divina, demostrando que ningún dios escapa al intelecto de Victor von Doom.",
        "search_term": "Doctor Doom Galactus Secret Wars 10 1984",
        "comic_source": "Secret Wars (1984) #10"
    },

    # --- ACTO 5: LA ANIQUILACIÓN DEL MULTIVERSO Y DIOS EMPERADOR DOOM ---
    {
        "id": 30,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "En 2015, el Multiverso entero colapsó en el evento más colosal de los cómics: Secret Wars. Un fenómeno catastrófico conocido como 'Las Incursiones' hacía chocar universos enteros hasta su destrucción mutua.",
        "search_term": "Incursion Earth colliding New Avengers Secret Wars",
        "comic_source": "New Avengers Vol 3 #1"
    },
    {
        "id": 31,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Los arquitectos del fin de los tiempos eran los Beyonders: dioses hiperdimensionales que habían asesinado a los Celestiales, aniquilado a Eternity y dejado el cadáver mutilado del Tribunal Viviente flotando en el cosmos.",
        "search_term": "Living Tribunal dead Beyonders New Avengers 30",
        "comic_source": "New Avengers Vol 3 #30"
    },
    {
        "id": 32,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Mientras los Vengadores e Illuminati caían en desesperación y peleaban entre sí, Doctor Doom tomó cartas en el asunto junto al Hombre Molécula, Owen Reece, y Doctor Strange.",
        "search_term": "Doctor Doom Owen Reece Stephen Strange Secret Wars",
        "comic_source": "New Avengers Vol 3 #33"
    },
    {
        "id": 33,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Doom confrontó a los Beyonders cara a cara. Utilizando a Owen Reece como conducto multiversal, detonó una bomba cósmica que asesinó a los creadores de la destrucción y absorbió la totalidad de su poder omnímodo.",
        "search_term": "Doom kills Beyonders Molecule Man Secret Wars",
        "comic_source": "Secret Wars (2015) #4"
    },
    {
        "id": 34,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Cuando el Multiverso fue borrado de la existencia, Victor tomó los fragmentos dispersos de las realidades moribundas y con su propia voluntad forjó un único mundo unificado: Battleworld.",
        "search_term": "Battleworld map planet Secret Wars 2015",
        "comic_source": "Secret Wars (2015) #2"
    },
    {
        "id": 35,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Allí, vestido con una túnica inmaculada de blanco puro, Victor von Doom no era un rey... era Dios Emperador Doom. El amo supremo de la realidad, con Stephen Strange sirviendo como su sheriff leal.",
        "search_term": "God Emperor Doom throne white Secret Wars 3",
        "comic_source": "Secret Wars (2015) #3"
    },
    {
        "id": 36,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "El momento más estremecedor ocurrió cuando Thanos se rebeló y marchó con una legión ante el trono de Doom, burlándose con desprecio y llamándolo un falso dios sin agallas.",
        "search_term": "Thanos confronts God Emperor Doom Secret Wars 8",
        "comic_source": "Secret Wars (2015) #8"
    },
    {
        "id": 37,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Doom bajó con calma y le preguntó al Titán Loco si poseía el Guantelete del Infinito. Cuando Thanos respondió con arrogancia que no lo necesitaba, Doom extendió su brazo.",
        "search_term": "Victor von Doom Thanos Secret Wars Vol 1 8",
        "comic_source": "Secret Wars (2015) #8"
    },
    {
        "id": 38,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "En una fracción de segundo, Doom atravesó el pecho blindado de Thanos y le arrancó de cuajo toda la columna vertebral y el cráneo con su mano desnuda, convirtiendo al Titán en polvo cósmico.",
        "search_term": "Victor von Doom Thanos Secret Wars Vol 1 8 001",
        "comic_source": "Secret Wars (2015) #8"
    },
    {
        "id": 39,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "Pero en la batalla climática contra Reed Richards por el alma del universo, Reed logró que Victor confesara la verdad que siempre intentó ocultar: que Reed habría salvado a todos con verdadera justicia.",
        "search_term": "Reed Richards God Emperor Doom final battle Secret Wars 9",
        "comic_source": "Secret Wars (2015) #9"
    },
    {
        "id": 40,
        "act": "Acto 5: Dios Emperador Doom",
        "text": "El Hombre Molécula transfirió el poder a Reed, quien reconstruyó el Multiverso. En un gesto de redención y piedad, Reed curó por completo el rostro de Victor, dejándolo sin cicatrices en Latveria.",
        "search_term": "Doom face healed smiling Secret Wars 9",
        "comic_source": "Secret Wars (2015) #9"
    },

    # --- ACTO 6: INFAMOUS IRON MAN Y LA CLAVE DE DOOMSDAY ---
    {
        "id": 41,
        "act": "Acto 6: La Conexión Doomsday",
        "text": "Con su rostro curado y Tony Stark caído tras Civil War II, Doom tomó una decisión insólita: asumir el manto de Iron Man para proteger al mundo a su manera en la serie Infamous Iron Man.",
        "search_term": "Infamous Iron Man Vol 1 1 Victor von Doom",
        "comic_source": "Infamous Iron Man #1"
    },
    {
        "id": 42,
        "act": "Acto 6: La Conexión Doomsday",
        "text": "Esta conexión entre Victor von Doom y Tony Stark no es casualidad. En What If? Iron Man: Demon in an Armor, ambos genios ya habían intercambiado cuerpos y destinos en una realidad paralela.",
        "search_term": "What If Iron Man Demon in an Armor Vol 1 1",
        "comic_source": "What If? Demon in an Armor"
    },
    {
        "id": 43,
        "act": "Acto 6: La Conexión Doomsday",
        "text": "El fichaje de Robert Downey Jr. no será un truco barato ni un Tony Stark malvado. Será la exploración de lo que sucede cuando una mente genial abraza la tragedia pura, la magia prohibida y una voluntad inquebrantable.",
        "search_term": "Books of Doom Vol 1 6",
        "comic_source": "Books of Doom #6"
    },
    {
        "id": 44,
        "act": "Acto 6: La Conexión Doomsday",
        "text": "En Avengers: Doomsday, los héroes no enfrentarán a un conquistador más... enfrentarán al único hombre que cree sinceramente que para salvar el cosmos entero, todos deben arrodillarse ante Doom.",
        "search_term": "Victor von Doom kneel Books of Doom Vol 1 6",
        "comic_source": "Books of Doom #6"
    }
]

def synthesize_all_audio():
    print("=== [Paso 1] Síntesis de Locución Neuronal con Voicebox ===")
    total = len(SCENES)
    for s in SCENES:
        sid = s["id"]
        wav_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.wav")
        meta_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.json")
        
        if os.path.exists(wav_path) and os.path.exists(meta_path) and os.path.getsize(wav_path) > 10000:
            print(f"[{sid:02d}/{total}] Ya existe en caché, omitiendo...")
            continue
            
        print(f"[{sid:02d}/{total}] Sintetizando: {s['text'][:65]}...")
        payload = {
            'profile_id': PROFILE_ID,
            'text': s['text'],
            'language': 'es',
            'engine': 'qwen',
            'max_chunk_chars': 1500,
            'crossfade_ms': 80,
            'normalize': True
        }
        
        try:
            r = requests.post(f"{VOICEBOX_URL}/generate", json=payload, timeout=60)
            if r.status_code != 200:
                print(f"   Error HTTP {r.status_code} al solicitar generación.")
                continue
            gen_id = r.json()['id']
            
            for attempt in range(60):
                time.sleep(2)
                sr = requests.get(f"{VOICEBOX_URL}/history/{gen_id}")
                if sr.status_code == 200:
                    sdata = sr.json()
                    status = sdata.get('status')
                    if status == 'completed':
                        dur = float(sdata.get('duration', 5.0))
                        ar = requests.get(f"{VOICEBOX_URL}/audio/{gen_id}")
                        with open(wav_path, 'wb') as f:
                            f.write(ar.content)
                        with open(meta_path, 'w', encoding='utf-8') as f:
                            json.dump({"id": sid, "duration": dur, "text": s['text']}, f, indent=2)
                        print(f"   -> Escena {sid:02d} completada! Duración: {dur:.2f}s")
                        break
                    elif status == 'failed':
                        print(f"   -> Fallo en escena {sid:02d}: {sdata.get('error')}")
                        break
        except Exception as e:
            print(f"   Excepción en escena {sid:02d}: {e}")

if __name__ == "__main__":
    synthesize_all_audio()

