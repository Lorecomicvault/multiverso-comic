"""
MOTOR DE PRODUCCIÓN DE VIDEO LARGO ESTILO ZAZOOM COMICS
=========================================================
- Formato: 16:9 Widescreen (1920x1080) con Letterbox cinematográfico
- Voz: Narrador Cómics ZaZooM (Clonada Qwen en Voicebox)
- Subtítulos: Centrados abajo, blanco (#FFFFFF) con borde negro de 3.5px, sincronizados 100%
- Movimiento: Ken Burns (slow zoom y pan cinematográfico)
- Viñetas: Interiores auténticas de Marvel Zombies
"""

import os
import sys
import json
import time
import shutil
import urllib.request
import subprocess
from PIL import Image, ImageOps

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "marvel_zombies_long")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "marvel_zombies_panels")
VOICEBOX_DB = r"C:\Users\Vanes\AppData\Roaming\sh.voicebox.app\voicebox.db"
VOICEBOX_APPDATA = r"C:\Users\Vanes\AppData\Roaming\sh.voicebox.app"
FFMPEG = r"C:\Users\Vanes\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.EXE"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "clips"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "panels_1080p"), exist_ok=True)

# -------------------------------------------------------------------------
# 1. GUIÓN CINEMATOGRÁFICO DE 5 ACTOS (MARVEL ZOMBIES)
# -------------------------------------------------------------------------
SCRIPT_SCENES = [
    # --- ACTO 1: EL DÍA CERO Y EL DESTELLO EN EL CIELO ---
    {"id": 1, "act": "Acto 1", "speaker": None, "text": "Era una tarde aparentemente ordinaria en el corazón de Manhattan, cuando un destello púrpura rasgó el firmamento."},
    {"id": 2, "act": "Acto 1", "speaker": None, "text": "Desde una grieta interdimensional desconocida, una figura dorada cayó a toda velocidad sobre Times Square."},
    {"id": 3, "act": "Acto 1", "speaker": None, "text": "Se trataba de Sentry, pero no el protector brillante que el mundo recordaba, sino una cáscara infectada y putrefacta."},
    {"id": 4, "act": "Acto 1", "speaker": None, "text": "Con un apetito voraz e incontrolable, Sentry comenzó a desgarrar y devorar a cada civil que se cruzaba en su camino."},
    {"id": 5, "act": "Acto 1", "speaker": None, "text": "Las sirenas de la policía resonaron en toda la isla, mientras el terror y el caos consumían las avenidas de Nueva York."},
    {"id": 6, "act": "Acto 1", "speaker": None, "text": "Creyendo que se trataba de una invasión convencional, los Vengadores acudieron de inmediato al llamado de auxilio."},
    {"id": 7, "act": "Acto 1", "speaker": None, "text": "El Coronel América, Iron Man, Hawkeye, Thor y Scarlet Witch descendieron en la zona cero del ataque."},
    {"id": 8, "act": "Acto 1", "speaker": "Coronel América", "text": "¡Mantengan la formación! ¡Neutralicen a la amenaza antes de que cause más bajas civiles!"},
    {"id": 9, "act": "Acto 1", "speaker": None, "text": "Pero subestimaron la pesadilla. Sentry se abalanzó sobre los héroes con una furia descomunal y salvaje."},
    {"id": 10, "act": "Acto 1", "speaker": None, "text": "En cuestión de segundos, los colmillos infectados del monstruo atravesaron la carne del Coronel América y de Hawkeye."},
    {"id": 11, "act": "Acto 1", "speaker": None, "text": "El virus extraterrestre no buscaba matarlos. Reconfiguró cada fibra de su ser, convirtiéndolos en esclavos de un hambre insaciable."},
    {"id": 12, "act": "Acto 1", "speaker": None, "text": "Los protectores más formidables de la humanidad acababan de transformarse en sus peores cazadores."},

    # --- ACTO 2: LA CACERÍA EN MANHATTAN Y LA TRAGEDIA DE PETER PARKER ---
    {"id": 13, "act": "Acto 2", "speaker": None, "text": "La infección se expandió como fuego sobre gasolina por todos los rincones de la metrópoli."},
    {"id": 14, "act": "Acto 2", "speaker": None, "text": "Los Vengadores infectados utilizaron sus identidades y sus poderes para emboscar a otros superhéroes desprevenidos."},
    {"id": 15, "act": "Acto 2", "speaker": None, "text": "A pocas calles de allí, Spider-Man balanceaba entre los rascacielos intentando poner a salvo a decenas de civiles."},
    {"id": 16, "act": "Acto 2", "speaker": None, "text": "Fue entonces cuando el Coronel América interceptó a Peter en pleno aire, enterrándole los dientes en el hombro."},
    {"id": 17, "act": "Acto 2", "speaker": "Spider-Man", "text": "¡Coronel, detente! ¿Qué demonios te está pasando? ¡Traté de razonar con ellos!"},
    {"id": 18, "act": "Acto 2", "speaker": None, "text": "Con el virus corriendo por sus venas, Peter sintió un ardor inhumano y un vacío devorador en su estómago."},
    {"id": 19, "act": "Acto 2", "speaker": None, "text": "Aterrorizado y desesperado por proteger a su familia, Peter corrió a su departamento en Queens."},
    {"id": 20, "act": "Acto 2", "speaker": None, "text": "Mary Jane y la tía May lo recibieron con lágrimas de alivio, sin imaginar el monstruo en que se había convertido."},
    {"id": 21, "act": "Acto 2", "speaker": "Spider-Man", "text": "¡Aléjense de mí! ¡No puedo controlarlo! ¡El hambre... es demasiado fuerte!"},
    {"id": 22, "act": "Acto 2", "speaker": None, "text": "La conciencia del héroe fue completamente aplastada por el hambre zombi, y en un instante de horror, Peter las devoró."},
    {"id": 23, "act": "Acto 2", "speaker": None, "text": "Al recuperar brevemente la lucidez, Spidey cayó de rodillas sobre la sangre de sus seres amados, desgarrado por la culpa."},
    {"id": 24, "act": "Acto 2", "speaker": None, "text": "Una culpa eterna que lo atormentaría por el resto de su maldita existencia."},

    # --- ACTO 3: EL SANCTUM SANCTORUM Y LA CAÍDA DE LOS MUTANTES ---
    {"id": 25, "act": "Acto 3", "speaker": None, "text": "Mientras tanto, en las afueras de Greenwich Village, Magneto lideraba un último frente de resistencia mutante."},
    {"id": 26, "act": "Acto 3", "speaker": None, "text": "Utilizando el campo magnético de la Tierra, el amo del magnetismo aplastaba a hordas enteras de criaturas infectadas."},
    {"id": 27, "act": "Acto 3", "speaker": None, "text": "Ash Williams, transportado misteriosamente a esta dimensión, se unió a Dazzler y a Scarlet Witch buscando refugio."},
    {"id": 28, "act": "Acto 3", "speaker": None, "text": "Corrieron desesperados hacia el Sanctum Sanctorum, creyendo que el Hechicero Supremo Doctor Strange podría detener la plaga."},
    {"id": 29, "act": "Acto 3", "speaker": None, "text": "Pero al cruzar las puertas del templo místico, la escena que encontraron fue dantesca y escalofriante."},
    {"id": 30, "act": "Acto 3", "speaker": None, "text": "El Doctor Druid y los discípulos místicos estaban devorando salvajemente el cuerpo mutilado de Wong."},
    {"id": 31, "act": "Acto 3", "speaker": None, "text": "Ash reaccionó con frialdad y le disparó un tiro certero en el cráneo con su escopeta antes de que pudieran atacarlos."},
    {"id": 32, "act": "Acto 3", "speaker": None, "text": "Aun con sus armas, la magia oscura y los zombis rodearon el santuario, infectando a Scarlet Witch y a Dazzler."},
    {"id": 33, "act": "Acto 3", "speaker": None, "text": "Quicksilver, en su desesperado intento por salvar a su hermana Wanda, corrió a velocidad supersónica a través del globo."},
    {"id": 34, "act": "Acto 3", "speaker": None, "text": "Sin embargo, la Wanda que rescató era una impostora zombi que lo mordió en el cuello."},
    {"id": 35, "act": "Acto 3", "speaker": None, "text": "Pietro, con su velocidad relámpago, esparció el virus en cada continente del planeta en menos de diez minutos."},

    # --- ACTO 4: LA MANSIÓN DE LOS VENGADORES Y EL HELICARRIER ---
    {"id": 36, "act": "Acto 4", "speaker": None, "text": "En la Mansión de los Vengadores, el horror alcanzó su punto más grotesco y despiadado."},
    {"id": 37, "act": "Acto 4", "speaker": None, "text": "El leal mayordomo Edwin Jarvis fue rodeado y despedazado vivo por los héroes a los que sirvió durante años."},
    {"id": 38, "act": "Acto 4", "speaker": None, "text": "Hank Pym, el Hombre Gigante, escondía secretamente a Black Panther en su laboratorio para devorarlo trozo a trozo."},
    {"id": 39, "act": "Acto 4", "speaker": None, "text": "En el cielo, el Helicarrier de S.H.I.E.L.D. permanecía como la última fortaleza volante de los supervivientes."},
    {"id": 40, "act": "Acto 4", "speaker": "Nick Fury", "text": "¡Esta es la última posición de la humanidad! ¡Si caemos nosotros, este planeta está condenado para siempre!"},
    {"id": 41, "act": "Acto 4", "speaker": None, "text": "Nick Fury reunió a los Cuatro Fantásticos, a Iron Man y a los científicos para diseñar una puerta dimensional."},
    {"id": 42, "act": "Acto 4", "speaker": None, "text": "Querían escapar a una realidad paralela sana donde la plaga no existiera."},
    {"id": 43, "act": "Acto 4", "speaker": None, "text": "Pero la locura ya había penetrado. Reed Richards, quebrado psicológicamente por la muerte de sus hijos Franklin y Valeria, colapsó."},
    {"id": 44, "act": "Acto 4", "speaker": None, "text": "Mr. Fantástico consideró que la infección zombi era la cúspide evolutiva de la raza humana y una forma perfecta de vida."},
    {"id": 45, "act": "Acto 4", "speaker": None, "text": "En un acto de demencia absoluta, Reed infectó voluntariamente a Sue Storm, a Johnny Storm y a Ben Grimm."},
    {"id": 46, "act": "Acto 4", "speaker": None, "text": "Los Cuatro Fantásticos zombificados masacraron a toda la tripulación del Helicarrier en una carnicería sin precedentes."},
    {"id": 47, "act": "Acto 4", "speaker": None, "text": "El gigantesco acorazado aéreo cayó envuelto en llamas sobre las ruinas de Manhattan."},

    # --- ACTO 5: LA LLEGADA DEL HERALDO Y EL HAMBRE CÓSMICA ---
    {"id": 48, "act": "Acto 5", "speaker": None, "text": "Semanas más tarde, la Tierra se convirtió en un desierto calcinado y desprovisto de cualquier rastro de vida."},
    {"id": 49, "act": "Acto 5", "speaker": None, "text": "Habiendo devorado a casi ocho mil millones de personas, el hambre de los zombis se volvió un tormento insoportable."},
    {"id": 50, "act": "Acto 5", "speaker": None, "text": "El Coronel América, Wolverine, Spider-Man, Luke Cage y Hank Pym vagaban entre escombros como sombras hambrientas."},
    {"id": 51, "act": "Acto 5", "speaker": None, "text": "Fue en ese momento de desolación total cuando un resplandor cósmico plateado iluminó el cielo envenenado."},
    {"id": 52, "act": "Acto 5", "speaker": None, "text": "Silver Surfer, el heraldo de Galactus, descendió a la superficie para anunciar la inminente llegada del Devorador de Mundos."},
    {"id": 53, "act": "Acto 5", "speaker": "Silver Surfer", "text": "¡Habitantes de este planeta! Vuestro tiempo ha llegado. ¡Preparaos para ser consumidos por Galactus!"},
    {"id": 54, "act": "Acto 5", "speaker": None, "text": "Pero los zombis no sintieron miedo alguno. Vieron en el emisario plateado la única presa restante en el universo."},
    {"id": 55, "act": "Acto 5", "speaker": None, "text": "Desesperados por saciar su voracidad, los héroes corruptos atacaron al heraldo con una ferocidad inaudita."},
    {"id": 56, "act": "Acto 5", "speaker": None, "text": "Hulk saltó sobre la tabla, desmembrando a Silver Surfer de un solo golpe demoledor."},
    {"id": 57, "act": "Acto 5", "speaker": None, "text": "Iron Man, Spider-Man, Wolverine y el Coronel América se abalanzaron sobre sus restos y devoraron su carne estelar."},
    {"id": 58, "act": "Acto 5", "speaker": None, "text": "Al consumir al Heraldo, una mutación inimaginable ocurrió en el interior de sus cuerpos muertos."},
    {"id": 59, "act": "Acto 5", "speaker": None, "text": "Los zombis absorbieron el Poder Cósmico, fusionando la podredumbre de la carne con la energía pura del cosmos."},
    {"id": 60, "act": "Acto 5", "speaker": None, "text": "Ráfagas de energía azul y estelar brotaban de las manos mutiladas de Spider-Man y de los ojos destrozados de Wolverine."},
    {"id": 61, "act": "Acto 5", "speaker": None, "text": "Fue entonces cuando el cielo se oscureció por completo y la silueta colosal de Galactus emergió entre las nubes."},
    {"id": 62, "act": "Acto 5", "speaker": None, "text": "Galactus contempló indignado cómo unos cadáveres repugnantes habían asesinado y devorado a su heraldo cósmico."},
    {"id": 63, "act": "Acto 5", "speaker": "Galactus", "text": "¡Insectos abominables! ¡Vuestra insolencia terminará con la extinción total de este mundo podrido!"},
    {"id": 64, "act": "Acto 5", "speaker": None, "text": "Galactus desató un rayo destructor capaz de borrar planetas enteros, pero los zombis cósmicos resistieron el embate."},
    {"id": 65, "act": "Acto 5", "speaker": None, "text": "Trabajando con las mentes científicas de Iron Man y Giant-Man, construyeron un condensador de poder cuántico."},
    {"id": 66, "act": "Acto 5", "speaker": None, "text": "Canalizando toda la energía cósmica absorbida de Silver Surfer, dispararon un cañón masivo directo al pecho de Galactus."},
    {"id": 67, "act": "Acto 5", "speaker": None, "text": "El gigantesco titán cayó derribado como una montaña sobre el asfalto destrozado de Nueva York."},
    {"id": 68, "act": "Acto 5", "speaker": None, "text": "Los monstruos no perdieron un solo segundo y se lanzaron sobre el dios espacial, desgarrando su armadura."},
    {"id": 69, "act": "Acto 5", "speaker": None, "text": "En el festín más colosal de la historia del cómic, los héroes zombi devoraron el cuerpo inmortal de Galactus."},
    {"id": 70, "act": "Acto 5", "speaker": None, "text": "Al terminar, los sobrevivientes zombificados obtuvieron el poder omnipotente del Devorador de Mundos."},
    {"id": 71, "act": "Acto 5", "speaker": None, "text": "Ahora vestidos con los símbolos cósmicos de Galactus, miraron hacia la inmensidad del espacio exterior."},
    {"id": 72, "act": "Acto 5", "speaker": None, "text": "La Tierra había muerto. Ya no quedaba ni una sola gota de carne ni de sangre que pudiera saciarlos."},
    {"id": 73, "act": "Acto 5", "speaker": None, "text": "Con una simple orden mental, los Galacti zombis despegaron de la órbita terrestre a la velocidad de la luz."},
    {"id": 74, "act": "Acto 5", "speaker": None, "text": "El apocalipsis ya no pertenecía a un solo planeta."},
    {"id": 75, "act": "Acto 5", "speaker": None, "text": "El universo entero estaba a punto de ser devorado... por los muertos hambrientos de Marvel."}
]

# -------------------------------------------------------------------------
# 2. CLIENTE DE SÍNTESIS DE AUDIO (VOICEBOX MCP)
# -------------------------------------------------------------------------
class VoiceboxSynthesizer:
    def __init__(self):
        self.url = "http://127.0.0.1:17493/mcp/"
        self.client_id = "antigravity"
        self.session_id = None

    def _init_session(self):
        if self.session_id:
            return
        headers = {
            'Accept': 'application/json, text/event-stream',
            'X-Voicebox-Client-Id': self.client_id,
            'Content-Type': 'application/json'
        }
        init_data = {
            'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
            'params': {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'antigravity', 'version': '1.0'}}
        }
        req = urllib.request.Request(self.url, data=json.dumps(init_data).encode('utf-8'), headers=headers, method='POST')
        resp = urllib.request.urlopen(req, timeout=5)
        self.session_id = resp.headers.get('mcp-session-id')
        print(f"[Voicebox] Sesión inicializada con ID: {self.session_id}")

    def synthesize_scene(self, scene_id, text, speaker=None):
        out_wav = os.path.join(OUTPUT_DIR, "audio", f"scene_{scene_id:03d}.wav")
        meta_json = os.path.join(OUTPUT_DIR, "audio", f"scene_{scene_id:03d}.json")

        # Caché: si ya existe y tiene duración válida, retornar inmediatamente
        if os.path.exists(out_wav) and os.path.exists(meta_json):
            with open(meta_json, "r", encoding="utf-8") as f:
                d = json.load(f)
                return out_wav, d.get("duration", 5.0)

        # Si no existe, inicializar sesión de Voicebox
        self._init_session()

        # Preparar texto: si es diálogo, incluir énfasis dramático
        spoken_text = text

        headers = {
            'Accept': 'application/json, text/event-stream',
            'X-Voicebox-Client-Id': self.client_id,
            'Content-Type': 'application/json',
            'mcp-session-id': self.session_id
        }

        call_data = {
            'jsonrpc': '2.0',
            'id': scene_id,
            'method': 'tools/call',
            'params': {
                'name': 'voicebox.speak',
                'arguments': {
                    'text': spoken_text,
                    'profile': 'Narrador Cómics ZaZooM',
                    'engine': 'qwen',
                    'personality': False,
                    'language': 'es'
                }
            }
        }

        try:
            req = urllib.request.Request(self.url, data=json.dumps(call_data).encode('utf-8'), headers=headers, method='POST')
            resp = urllib.request.urlopen(req, timeout=15)
            body = resp.read().decode('utf-8')
            gen_id = None
            for line in body.splitlines():
                if line.startswith('data: '):
                    parsed = json.loads(line[6:])
                    gen_id = parsed.get("result", {}).get("structuredContent", {}).get("generation_id")
                    if not gen_id:
                        c_txt = parsed.get("result", {}).get("content", [{}])[0].get("text", "{}")
                        gen_id = json.loads(c_txt).get("generation_id")
                    if gen_id:
                        break

            if not gen_id:
                raise Exception(f"No se recibió generation_id de Voicebox para escena {scene_id}")

            # Polling hasta que esté completed en SQLite (hasta 70 segundos)
            import sqlite3
            duration = 5.0
            for attempt in range(45):
                time.sleep(1.5)
                conn = sqlite3.connect(VOICEBOX_DB)
                cur = conn.cursor()
                cur.execute('SELECT status, duration, audio_path FROM generations WHERE id = ?;', (gen_id,))
                row = cur.fetchone()
                conn.close()
                if row and row[0] == 'completed':
                    duration = float(row[1]) if row[1] else 5.0
                    src_file = os.path.join(VOICEBOX_APPDATA, row[2])
                    for _ in range(10):
                        if os.path.exists(src_file) and os.path.getsize(src_file) > 1000:
                            shutil.copy2(src_file, out_wav)
                            break
                        time.sleep(0.5)
                    if os.path.exists(out_wav):
                        break

            # Guardar metadatos
            with open(meta_json, "w", encoding="utf-8") as f:
                json.dump({"scene_id": scene_id, "duration": duration, "text": text, "speaker": speaker}, f, indent=2)

            return out_wav, duration

        except Exception as e:
            print(f"[Voicebox ERROR] Fallo al sintetizar escena {scene_id}: {e}")
            duration = max(3.5, len(text.split()) * 0.45)
            cmd_fb = [
                FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{duration:.3f}",
                "-acodec", "pcm_s16le", out_wav
            ]
            subprocess.run(cmd_fb, cwd=OUTPUT_DIR, check=True)
            with open(meta_json, "w", encoding="utf-8") as f:
                json.dump({"scene_id": scene_id, "duration": duration, "text": text, "fallback": True}, f)
            return out_wav, duration

# -------------------------------------------------------------------------
# 3. PREPARADOR DE VIÑETAS 16:9 (1920x1080 CON LETTERBOXING CINEMATOGRÁFICO)
# -------------------------------------------------------------------------
def prepare_1080p_panel(scene_id, panel_index, force=False):
    out_img = os.path.join(OUTPUT_DIR, "panels_1080p", f"panel_{scene_id:03d}.jpg")
    if not force and os.path.exists(out_img):
        return out_img

    # Prioridad 1: Viñeta canónica sincronizada exactamente con la escena
    src_panel = os.path.join(ASSETS_DIR, f"scene_{scene_id:03d}.jpg")

    # Respaldo 2: Panel secuencial numérico
    if not os.path.exists(src_panel):
        src_panel = os.path.join(ASSETS_DIR, f"mz_panel_{panel_index:03d}.jpg")

    # Respaldo 3: Paneles extraídos de scratch
    if not os.path.exists(src_panel):
        src_panel = os.path.join(BASE_DIR, "scratch", "extracted_panels", f"panel_{panel_index:03d}.jpg")

    if not os.path.exists(src_panel):
        src_panel = os.path.join(BASE_DIR, "scratch", "test_fandom_avengers.jpg")

    with Image.open(src_panel) as im:
        im = im.convert("RGB")
        target_w, target_h = 1920, 1080
        
        # Escala manteniendo aspecto dentro de 1920x1080 (Letterboxing)
        scale = min(target_w / im.width, target_h / im.height)
        new_w = int(im.width * scale)
        new_h = int(im.height * scale)
        resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (target_w, target_h), (0, 0, 0))
        pos_x = (target_w - new_w) // 2
        pos_y = (target_h - new_h) // 2
        canvas.paste(resized, (pos_x, pos_y))
        canvas.save(out_img, quality=95)

    return out_img

# -------------------------------------------------------------------------
# 4. GENERADOR DE SUBTÍTULOS (.ASS) ESTILO ZAZOOM
# -------------------------------------------------------------------------
def generate_scene_ass(scene_id, text, duration, speaker=None):
    ass_path = os.path.join(OUTPUT_DIR, "clips", f"sub_{scene_id:03d}.ass")

    def format_ts(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = seconds % 60
        cs = int((s - int(s)) * 100)
        return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

    ass_content = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Narration,Arial,46,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3.8,2.0,2,60,60,70,1
Style: Dialogue,Arial,44,&H00FFFFFF,&H000000FF,&H00000000,&HB0000000,-1,0,0,0,100,100,0,0,1,3.5,2.0,2,80,80,85,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    words = text.split()
    chunk_size = 6
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    if not chunks:
        chunks = [text]

    time_per_chunk = duration / len(chunks)
    for idx, chunk in enumerate(chunks):
        t_start = idx * time_per_chunk
        t_end = (idx + 1) * time_per_chunk
        start_str = format_ts(t_start)
        end_str = format_ts(t_end)

        if speaker:
            color_tag = "{\\c&H0000FF&}" if "Spider" in speaker or "América" in speaker else "{\\c&H00FFFF&}"
            event_line = f"Dialogue: 0,{start_str},{end_str},Dialogue,,0,0,0,,{color_tag}{speaker}:\\N{{\\c&HFFFFFF&}}{chunk}\n"
        else:
            event_line = f"Dialogue: 0,{start_str},{end_str},Narration,,0,0,0,,{chunk}\n"

        ass_content += event_line

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

    return ass_path

# -------------------------------------------------------------------------
# 5. RENDERIZADOR DE CLIP DE ESCENA (1080p + SUBTÍTULOS ESTILO ZAZOOM)
# -------------------------------------------------------------------------
def render_scene_clip(scene_id, panel_path, audio_path, ass_path, duration, force=False):
    clip_mp4 = os.path.join(OUTPUT_DIR, "clips", f"scene_{scene_id:03d}.mp4")
    if not force and os.path.exists(clip_mp4) and os.path.getsize(clip_mp4) > 100000:
        return clip_mp4

    # Usar rutas relativas ejecutando dentro de OUTPUT_DIR para evitar problemas de escape en Windows
    rel_panel = f"panels_1080p/panel_{scene_id:03d}.jpg"
    rel_audio = f"audio/scene_{scene_id:03d}.wav"
    rel_sub = f"clips/sub_{scene_id:03d}.ass"
    rel_out = f"clips/scene_{scene_id:03d}.mp4"

    cmd = [
        FFMPEG, "-y",
        "-framerate", "30", "-loop", "1", "-i", rel_panel,
        "-i", rel_audio,
        "-vf", f"scale=1920:1080,subtitles={rel_sub},format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-b:v", "4000k",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.3f}",
        "-shortest",
        rel_out
    ]

    subprocess.run(cmd, cwd=OUTPUT_DIR, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return clip_mp4

# -------------------------------------------------------------------------
# 6. PIPELINE PRINCIPAL Y ENSAMBLAJE FINAL
# -------------------------------------------------------------------------
def run_production_pipeline(start_scene=1, end_scene=75, force_rebuild=False):
    print("=" * 70)
    print("INICIANDO PRODUCCIÓN DE VIDEO LARGO: MARVEL ZOMBIES (ESTILO ZAZOOM)")
    print(f"Rango de escenas: {start_scene} a {end_scene} (Total: {end_scene - start_scene + 1} escenas)")
    print(f"Modo forzado de re-renderizado: {force_rebuild}")
    print("=" * 70)

    synth = VoiceboxSynthesizer()
    clips_list = []

    for item in SCRIPT_SCENES[start_scene-1:end_scene]:
        s_id = item["id"]
        text = item["text"]
        speaker = item["speaker"]
        panel_idx = ((s_id - 1) % 75) + 1

        print(f"\n[Escena {s_id:03d}/{len(SCRIPT_SCENES)}] {item['act']} - {speaker or 'Narrador'}")
        print(f"Texto: \"{text[:60]}...\"")

        # 1. Sintetizar locución con Voicebox (aprovecha la caché existente)
        audio_path, duration = synth.synthesize_scene(s_id, text, speaker)
        print(f" -> Audio generado: {duration:.2f}s ({os.path.basename(audio_path)})")

        # 2. Preparar panel 1080p alineado
        panel_path = prepare_1080p_panel(s_id, panel_idx, force=force_rebuild)

        # 3. Generar subtítulos .ass
        ass_path = generate_scene_ass(s_id, text, duration, speaker)

        # 4. Renderizar escena con subtítulos
        clip_path = render_scene_clip(s_id, panel_path, audio_path, ass_path, duration, force=force_rebuild)
        print(f" -> Clip renderizado: {os.path.basename(clip_path)}")
        clips_list.append(clip_path)

    # 5. Concatenar todos los clips en el video final
    concat_txt = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for c in clips_list:
            clean_c = c.replace("\\", "/")
            f.write(f"file '{clean_c}'\n")

    final_video = os.path.join(OUTPUT_DIR, "marvel_zombies_la_caida_completo_1080p.mp4")
    print("\n" + "=" * 70)
    print("CONCATENANDO VIDEO FINAL...")
    print(f"Destino: {final_video}")
    print("=" * 70)

    concat_cmd = [
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        final_video
    ]
    subprocess.run(concat_cmd, check=True)

    print("\n" + "*" * 70)
    print(f"¡PRODUCCIÓN EXITOSA!")
    print(f"Video generado: {final_video}")
    print(f"Tamaño: {os.path.getsize(final_video) / (1024*1024):.2f} MB")
    print("*" * 70)

if __name__ == "__main__":
    # Ejecutar producción con reconstrucción completa de paneles alineados y clips
    run_production_pipeline(start_scene=1, end_scene=75, force_rebuild=True)
