"""
PRODUCCIÓN DEL VIDEO LARGO PARA YOUTUBE:
SUPERIOR SPIDER-MAN: EL DÍA QUE PETER DEJÓ DE CONTENERSE (HISTORIA COMPLETA)
=============================================================================
- Formato: 16:9 Full HD (1920x1080) Widescreen
- Voz: Voicebox neuronal (Qwen-TTS, Perfil 'Narrador Referencia Cómic')
- Viñetas: 100% canónicas de Amazing Spider-Man #698, #699, #700 y Superior Spider-Man #1
- Subtítulos: ZaZooM Comic Style (centrado inferior, blanco con trazo negro nítido)
- Cámara: Movimiento cinemático Ken Burns (zoom y pan sutil)
- Música: Banda sonora cinemática sutil de misterio/tensión a -32 dB
"""

import os
import sys
import json
import time
import shutil
import subprocess
import requests
from PIL import Image

PROJECT_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output", "superior_spiderman_long")
AUDIO_DIR = os.path.join(OUTPUT_DIR, "audio")
PANELS_RAW = os.path.join(OUTPUT_DIR, "panels_raw")
PANELS_1080P = os.path.join(OUTPUT_DIR, "panels_1080p")
CLIPS_DIR = os.path.join(OUTPUT_DIR, "clips")

for d in [OUTPUT_DIR, AUDIO_DIR, PANELS_RAW, PANELS_1080P, CLIPS_DIR]:
    os.makedirs(d, exist_ok=True)

VOICEBOX_URL = "http://127.0.0.1:17493"
PROFILE_ID = "28078056-1a1d-43d4-9d57-d616275f13c2" # Narrador Referencia Cómic

SCENES = [
    # --- ACTO 1: LA AGONÍA DEL PULPO Y LA GRAN CONSPIRACIÓN (ASM #698) ---
    {"id": 1, "act": "Acto 1", "text": "En las profundidades de la prisión de máxima seguridad La Balsa, un anciano yace postrado en una camilla médica, con su cuerpo marchito consumido por años de radiación y daño cerebral."},
    {"id": 2, "act": "Acto 1", "text": "Es el Doctor Otto Octavius, el legendario Doctor Octopus. Los médicos del gobierno confirman que sus órganos están colapsando y le quedan apenas unas horas de vida."},
    {"id": 3, "act": "Acto 1", "text": "De pronto, una silueta familiar desciende por las paredes de la celda: Spider-Man acude a visitar a su más antiguo archienemigo en su lecho de muerte."},
    {"id": 4, "act": "Acto 1", "text": "Pero el arácnido no se mueve ni habla con la compasión habitual. Su postura es rígida, calculadora y fría."},
    {"id": 5, "act": "Acto 1", "text": "Otto, haciendo acopio de su último aliento, balbucea con agonía el nombre de Peter Parker."},
    {"id": 6, "act": "Acto 1", "text": "En ese instante, Spider-Man se inclina hacia su oído y le susurra con una sonrisa siniestra: Te equivocas, muchacho. Yo soy Otto Octavius. Y tú... eres Peter Parker."},
    {"id": 7, "act": "Acto 1", "text": "Meses atrás, Otto había diseñado en secreto un Octobot dorado especial, capaz de transmitir sus patrones cerebrales directamente a través de la red neuronal de Spider-Man."},
    {"id": 8, "act": "Acto 1", "text": "La trampa perfecta se había cerrado: la mente de Otto ahora habitaba el cuerpo joven, ágil y sobrehumano de Peter Parker, mientras que el alma del héroe quedó condenada a morir dentro de un cuerpo decrépito."},

    # --- ACTO 2: ATRAPADO EN EL INFIERNO (ASM #699) ---
    {"id": 9, "act": "Acto 2", "text": "Peter Parker despierta dentro de la prisión de carne enferma de Octavius, sintiendo un dolor abrasador en cada músculo y respirando únicamente gracias a una máquina de soporte vital."},
    {"id": 10, "act": "Acto 2", "text": "El terror lo invade al comprobar que está ciego de un ojo, paralizado y con el corazón latiendo al borde de un infarto inminente."},
    {"id": 11, "act": "Acto 2", "text": "Peter comprende que Otto no solo le ha robado sus poderes, sino que ahora tiene acceso a su departamento, a sus amigos, a Mary Jane y a su anciana tía May."},
    {"id": 12, "act": "Acto 2", "text": "Desesperado por escapar, Peter logra activar un comando de emergencia oculto en el software de los tentáculos mecánicos de Otto, enviando una señal de socorro a sus antiguos aliados del mal."},
    {"id": 13, "act": "Acto 2", "text": "En cuestión de minutos, Trapster e Hydro-Man asaltan La Balsa, destruyendo los muros y liberando al supuesto Doctor Octopus ante la mirada atónita de los guardias."},
    {"id": 14, "act": "Acto 2", "text": "Los villanos creen que están rescatando a su líder criminal para un golpe final, sin sospechar jamás que la mente que habita esos restos es la de su más acérrimo enemigo."},

    # --- ACTO 3: LA CACERÍA Y LA CONFRONTACIÓN FINAL (ASM #700) ---
    {"id": 15, "act": "Acto 3", "text": "Mientras tanto, en las calles de Manhattan, Otto Octavius disfruta de la gloria, el vigor y la adrenalina del cuerpo de Spider-Man, patrullando con una arrogancia desmedida."},
    {"id": 16, "act": "Acto 3", "text": "Pero la noticia de la fuga de La Balsa llega a sus oídos. Otto sabe que si Peter logra conectar un nuevo Octobot a su cerebro, podría revertir el intercambio mental."},
    {"id": 17, "act": "Acto 3", "text": "Para proteger su nueva vida, Otto reúne a Mary Jane, a la tía May y a los seres queridos de Peter en lo alto de la Torre de los Vengadores, fingiendo ponerlos a salvo de un ataque terrorista."},
    {"id": 18, "act": "Acto 3", "text": "Peter, atado a un exoesqueleto médico rudimentario con los cuatro tentáculos mecánicos, arriba a la torre para el duelo más dramático y surrealista de su historia."},
    {"id": 19, "act": "Acto 3", "text": "El enfrentamiento es brutal y desigual: un anciano mutilado con brazos metálicos torpes luchando desesperadamente contra su propio cuerpo en la cima de sus facultades físicas."},
    {"id": 20, "act": "Acto 3", "text": "Ambos colisionan rompiendo los ventanales de la torre y cayendo al vacío hacia el asfalto neoyorquino."},
    {"id": 21, "act": "Acto 3", "text": "Spider-Man amortigua la caída con telarañas, pero el impacto contra el suelo desencadena el colapso cardiovascular definitivo en el cuerpo de Otto Octavius."},

    # --- ACTO 4: LA MUERTE DE PETER PARKER Y EL LEGADO ---
    {"id": 22, "act": "Acto 4", "text": "Peter agoniza en el suelo frío mientras los paramédicos y la policía intentan en vano reanimarlo. Sabe que el final ha llegado y ya no hay tiempo para recuperar su cuerpo."},
    {"id": 23, "act": "Acto 4", "text": "Con su último destello de voluntad, Peter activa los receptores neuronales del Octobot dañado, creando un puente telepático directo con la mente de Otto."},
    {"id": 24, "act": "Acto 4", "text": "En lugar de maldecirlo o buscar venganza, Peter le transfiere a Otto la totalidad de sus recuerdos, dolores y sacrificios."},
    {"id": 25, "act": "Acto 4", "text": "Otto experimenta en carne viva el dolor de perder a sus padres, la culpa desgarradora de la muerte del tío Ben en el almacén, y la agonía de sostener el cuerpo sin vida de Gwen Stacy en el puente de Brooklyn."},
    {"id": 26, "act": "Acto 4", "text": "Por primera vez en su vida, el arrogante científico comprende el peso titánico de la frase: Un gran poder conlleva una gran responsabilidad."},
    {"id": 27, "act": "Acto 4", "text": "Quebrado psicológicamente y derramando lágrimas bajo la máscara, Otto sostiene la mano del hombre que acaba de morir en su lugar."},
    {"id": 28, "act": "Acto 4", "text": "Peter Parker exhala su último suspiro y fallece. Otto Octavius jura frente a su cadáver: No seré un villano. Usaré mi intelecto para ser mejor de lo que tú fuiste. Seré... el Hombre Araña Superior."},

    # --- ACTO 5: EL PUÑETAZO A ESCORPIÓN (EL CLÍMAX DE SANGRE) ---
    {"id": 29, "act": "Acto 5", "text": "Días después, Otto asume el rol de Spider-Man con un uniforme modificado, armadura oscura y un comportamiento frío y metódico."},
    {"id": 30, "act": "Acto 5", "text": "La alarma de la ciudad se enciende cuando Mac Gargan, el temible Escorpión, escapa y desata el caos buscando venganza contra J. Jonah Jameson y amenazando a civiles en un hospital."},
    {"id": 31, "act": "Acto 5", "text": "Entre los rehenes se encuentra la tía May. Escorpión se prepara para atravesarla con su aguijón de ácido cuando una telaraña desciende a gran velocidad."},
    {"id": 32, "act": "Acto 5", "text": "Otto cae en el centro del combate, enfurecido de que un criminal de tercera clase se atreva a amenazar a la mujer que ahora representa a su propia familia."},
    {"id": 33, "act": "Acto 5", "text": "Escorpión sonríe confiado bajo su armadura cibernética, esperando las acrobacias defensivas y los chistes sarcásticos a los que Spider-Man siempre lo acostumbró."},
    {"id": 34, "act": "Acto 5", "text": "Pero Otto no es Peter. Otto no conoce la contención, ni mide las proporciones biológicas de la masa muscular de una araña humana."},
    {"id": 35, "act": "Acto 5", "text": "Cerrando el puño con toda la fuerza bruta disponible en el cuerpo arácnido, Otto descarga un derechazo colosal y seco directo al rostro de Escorpión."},
    {"id": 36, "act": "Acto 5", "text": "El estruendo es demoledor: el puño de Spider-Man pulveriza el blindaje facial de titanio y arranca de cuajo la mandíbula inferior entera de Mac Gargan, enviando dientes, lengua y hueso volando en una lluvia de sangre."},
    {"id": 37, "act": "Acto 5", "text": "Escorpión se desploma sobre el suelo en shock traumático, ahogándose en su propia sangre y con el rostro completamente mutilado."},

    # --- ACTO 6: LA ATERRADORA REVELACIÓN PSICOLÓGICA ---
    {"id": 38, "act": "Acto 6", "text": "Otto se queda inmóvil, mirando con los ojos desorbitados sus nudillos cubiertos de sangre y hueso roto."},
    {"id": 39, "act": "Acto 6", "text": "Un pensamiento escalofriante cruza por la mente del científico: Su mandíbula... se desprendió por completo. Mac Gargan no tiene piel súper densa... debajo del traje es un ser humano normal. Y yo usé toda la fuerza del cuerpo."},
    {"id": 40, "act": "Acto 6", "text": "El silencio se apodera de Nueva York mientras Otto comprende la verdad más perturbadora de Marvel: Durante todos estos años... en cada enfrentamiento en el banco, en el laboratorio, en los puentes... ¡Peter Parker siempre contuvo sus golpes! Pudo haberme arrancado la cabeza de un solo puñetazo en cualquier momento... y jamás lo hizo."},
    {"id": 41, "act": "Acto 6", "text": "Otto comprende que la bondad de Peter no era debilidad, sino un autocontrol digno de un dios compasivo. Pero él no es Peter Parker. Otto despliega sus patas mecánicas y jura que en su nueva era, el crimen pagará con sangre. Nace el Superior Spider-Man."}
]

def synthesize_all_audio():
    print("=== [Paso 1] Síntesis de Locución Neuronal con Voicebox ===")
    
    # Si la escena 1 ya fue generada en el test, copiarla
    test_s1 = r"C:\Users\Vanes\comics en espanol\scratch\voicebox_test_scene1\scene_01_test.wav"
    s1_dest = os.path.join(AUDIO_DIR, "scene_001.wav")
    if os.path.exists(test_s1) and not os.path.exists(s1_dest):
        shutil.copy2(test_s1, s1_dest)
        with open(os.path.join(AUDIO_DIR, "scene_001.json"), "w", encoding="utf-8") as f:
            json.dump({"id": 1, "duration": 9.36, "text": SCENES[0]["text"]}, f)
        print("-> Escena 1 restaurada de caché de prueba.")

    for s in SCENES:
        sid = s["id"]
        wav_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.wav")
        meta_path = os.path.join(AUDIO_DIR, f"scene_{sid:03d}.json")
        
        if os.path.exists(wav_path) and os.path.exists(meta_path) and os.path.getsize(wav_path) > 10000:
            print(f"[{sid:02d}/41] Ya existe en caché, omitiendo...")
            continue
            
        print(f"[{sid:02d}/41] Sintetizando: {s['text'][:60]}...")
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
            
            # Polling hasta completar
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
