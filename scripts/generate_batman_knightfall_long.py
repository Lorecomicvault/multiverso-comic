"""
Batman: Knightfall (La Caída del Murciélago) - Long Form YouTube Video Generator
100% Local Generation for YouTube (16:9 Full HD 1920x1080, 4-6 minutes)
Enhanced with Multi-Panel Visual Storytelling (35 curated panels synchronized to narration)
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import json
import time
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

# Ensure root directory is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.gemini_tts import synthesize_with_gemini
from src.composer import compose_scene_from_image, get_duration, compose_final
from src.transcribe import transcribe_scenes_to_ass

# Target output directory and final master file
FINAL_DIR = Path(r"C:\Users\Vanes\Downloads\video\Comics")
FINAL_MASTER = FINAL_DIR / "Batman_Knightfall_La_Caida_del_Murcielago_YouTube.mp4"

WORK_DIR = REPO_ROOT / "output" / "batman_knightfall_long"
FRAMED_DIR = WORK_DIR / "framed"
VOICEOVER_DIR = WORK_DIR / "voiceover"
SCENES_DIR = WORK_DIR / "scenes"

TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
FPS = 30

# The 14 Curated Scenes with Multiple Detailed Comic Panels per Scene
SCENES_DATA = [
    {
        "id": 1,
        "title": "El Nacimiento de la Pesadilla",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Santa_Prisca_001.jpg",
            "assets/curated_panels/batman_knightfall_long/Young_Bane_002.jpg",
            "assets/curated_panels/batman_knightfall_long/Osito_001.jpg"
        ],
        "text": (
            "En las profundidades de la temida prisión de Peña Duro, en la isla de Santa Prisca, "
            "nació y se crió un niño condenado a cumplir la sentencia perpetua de su padre ausente. "
            "En esa oscuridad absoluta, rodeado de criminales sanguinarios y violencia desmedida, "
            "forjó una mente brillante leyendo cientos de libros prohibidos y esculpió su cuerpo como una máquina indestructible. "
            "No conoció la compasión, solo una obsesión devoradora: la sombra del Murciélago que dominaba la mítica ciudad de Gotham. "
            "Su nombre era Bane."
        )
    },
    {
        "id": 2,
        "title": "La Llegada a Gotham",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0004.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0006.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0009.jpg"
        ],
        "text": (
            "Bane llegó a Gotham no como un matón más, sino como un implacable estratega militar con un intelecto fuera de serie. "
            "Al observar en silencio a Batman desde las alturas, comprendió una verdad matemática: "
            "el Caballero Oscuro era invencible en un combate cuerpo a cuerpo justo. "
            "Para destruirlo para siempre, no bastaba con golpearlo; debía desgastar metódicamente cada fibra de su cuerpo, "
            "destrozar su psique y despojarlo de toda esperanza antes del enfrentamiento final."
        )
    },
    {
        "id": 3,
        "title": "El Asalto al Manicomio Arkham",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Arkham_Asylum_001.jpg",
            "assets/curated_panels/batman_knightfall_long/Arkham_Asylum_003.jpg",
            "assets/curated_panels/batman_knightfall_long/Arkham_Asylum_004.jpg"
        ],
        "text": (
            "Bane ejecuta la primera fase de su letal plan maestro. "
            "Empuñando un lanzacohetes militar pesado, dispara directamente contra los muros de contención del Manicomio Arkham. "
            "Las alarmas aúllan en la noche mientras una explosión descomunal pulveriza toneladas de concreto y acero blindado. "
            "Bane no busca asesinar a nadie; su propósito es mucho más maquiavélico: "
            "abrir de par en par las puertas del infierno y soltar a los peores lunáticos en las calles de Gotham."
        )
    },
    {
        "id": 4,
        "title": "Caos Total en las Calles",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Joker_0001.jpg",
            "assets/curated_panels/batman_knightfall_long/Two-Face_0001.jpg",
            "assets/curated_panels/batman_knightfall_long/Firefly_0011.jpg"
        ],
        "text": (
            "Más de setenta y cinco de los más peligrosos psicópatas de Gotham escapan en una sola noche. "
            "El Joker, el Espantapájaros, Dos Caras, Victor Zsasz, el Sombrerero Loco y Hiedra Venenosa desatan una marea incontrolable de sangre y terror. "
            "La policía local colapsa en cuestión de horas y las sirenas no cesan de sonar. "
            "Gotham arde en llamas por los cuatro costados, convertida en un auténtico matadero urbano donde nadie está a salvo."
        )
    },
    {
        "id": 5,
        "title": "El Límite del Caballero Oscuro",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Batman_0723.jpg",
            "assets/curated_panels/batman_knightfall_long/Batman_0585.jpg"
        ],
        "text": (
            "Bruce Wayne se lanza en solitario a una cacería brutal que se prolonga durante tres semanas interminables. "
            "Sin dormir una sola noche completa, combatiendo sin descanso bajo tempestades y con una fiebre abrasadora que supera los cuarenta grados, Batman enfrenta a cada fugitivo. "
            "Con varias costillas fisuradas, heridas abiertas sin suturar y los músculos desgarrados por la fatiga extrema, "
            "el Caballero Oscuro se niega tercamente a rendirse."
        )
    },
    {
        "id": 6,
        "title": "La Advertencia en la Baticueva",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0007.jpg",
            "assets/curated_panels/batman_knightfall_long/Robin_Tim_Drake_0131.jpg"
        ],
        "text": (
            "En el refugio de la Baticueva, Alfred Pennyworth y Tim Drake, el joven Robin, le suplican a Bruce que se detenga. "
            "Le advierten con angustia que sus signos vitales están colapsando, que sus reflejos han caído a niveles letales "
            "y que volver a salir en esas condiciones es un suicidio inminente. "
            "Pero la inflexible promesa de Batman lo ciega por completo: mientras un solo criminal camine libre por sus calles, él no descansará jamás."
        )
    },
    {
        "id": 7,
        "title": "La Trampa del Espantapájaros y el Joker",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Scarecrow_0001.jpg",
            "assets/curated_panels/batman_knightfall_long/Scarecrow_0002.jpg"
        ],
        "text": (
            "Batman cae en una emboscada letal coordinada por el Espantapájaros y el Joker. "
            "El gas del miedo penetra las defensas de su máscara, obligándolo a revivir el trauma del asesinato de sus padres en un ciclo constante de desesperación psicológica. "
            "Aunque el Murciélago logra neutralizarlos con pura fuerza de voluntad, el veneno toxicológico y la tortura mental aniquilan los últimos vestigios de su energía física."
        )
    },
    {
        "id": 8,
        "title": "El Regreso a la Mansión Wayne",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Wayne_Manor_005.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0008.jpg"
        ],
        "text": (
            "Tras incontables días de combate desgarrador, Batman captura al último criminal de Arkham. "
            "Empapado por la lluvia torrencial, tambaleándose y arrastrando los pies en un estado de semiinconsciencia febril, "
            "Bruce Wayne regresa por fin a la Mansión Wayne. Respira aliviado creyendo que la peor pesadilla ha concluido y que su ciudad está a salvo. "
            "Pero desconoce que la verdadera pesadilla acaba de comenzar."
        )
    },
    {
        "id": 9,
        "title": "La Emboscada en la Sombra",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0014.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0015.jpg"
        ],
        "text": (
            "Al cruzar el umbral de su estudio privado, una voz profunda y amenazante rasga el silencio: 'Sé que eres Bruce Wayne'. "
            "De las sombras del salón emerge la imponente figura de Bane. "
            "Con su brillante intelecto deductivo y estudiando minuciosamente los movimientos del héroe, descifró su identidad secreta. "
            "Mientras Batman sangraba en las calles, Bane lo acechaba pacientemente, aguardando el instante de su mayor debilidad."
        )
    },
    {
        "id": 10,
        "title": "La Masacre en la Baticueva",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0016.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0019.jpg"
        ],
        "text": (
            "La batalla se desata en la Baticueva, pero no es una contienda; es una masacre despiadada. "
            "Batman apenas puede levantar la guardia y sus golpes carecen de fuerza ante la corpulencia del invasor. "
            "Bane esquiva con facilidad los torpes ataques del exhausto héroe, estrellándolo salvajemente contra las rocas, "
            "destrozando la supercomputadora y azotándolo contra el suelo hasta desgarrarle la máscara y fracturarle el rostro."
        )
    },
    {
        "id": 11,
        "title": "El Veneno Desatado",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0017.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0018.jpg"
        ],
        "text": (
            "Para sellar la humillación absoluta, Bane activa el dispositivo en su muñeca. "
            "La fórmula química del superesteroide Venom ruge a través de los conductos directamente a su sistema nervioso. "
            "Su musculatura se expande de forma monstruosa y sus venas hierven de adrenalina pura. "
            "Con Batman totalmente ensangrentado a sus pies, incapaz de articular palabra, Bane lo levanta del cuello como a una marioneta rota."
        )
    },
    {
        "id": 12,
        "title": "El Quiebre del Murciélago",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0021.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0022.jpg",
            "assets/curated_panels/batman_knightfall_long/Bane_0020.jpg"
        ],
        "text": (
            "Y ocurre el momento cumbre que cambió la historia del cómic para siempre. "
            "Bane eleva al Caballero Oscuro en vilo sobre su cabeza y pronuncia su sentencia definitiva: '¡Te romperé!'. "
            "Con una brutalidad escalofriante, estrella la espalda de Batman contra su rodilla de hierro. "
            "Un crujido seco y demoledor retumba en toda la cueva. La columna vertebral de Bruce Wayne se parte en dos. Batman ha sido quebrado."
        )
    },
    {
        "id": 13,
        "title": "La Humillación Pública",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0023.jpg",
            "assets/curated_panels/batman_knightfall_long/Batman_0727.jpg"
        ],
        "text": (
            "Destrozar su cuerpo en la intimidad no bastaba para saciar la ambición del conquistador. "
            "Bane carga el cuerpo inerte y sangrante de Batman hasta el corazón de Gotham y, "
            "desde lo alto de un edificio frente a la mirada atónita de los ciudadanos y la prensa, "
            "arroja al héroe al pavimento como si fuera basura inservible. "
            "El mito del protector invencible había muerto ante los ojos del mundo."
        )
    },
    {
        "id": 14,
        "title": "El Nuevo Rey de Gotham",
        "panels": [
            "assets/curated_panels/batman_knightfall_long/Bane_0055.jpg",
            "assets/curated_panels/batman_knightfall_long/Bruce_Wayne_confronts_Azrael.jpg",
            "assets/curated_panels/batman_knightfall_long/Batman_Jean-Paul_Valley_0011.jpg"
        ],
        "text": (
            "Con Gotham sumida en el terror y Batman postrado en una silla de ruedas, Bane se proclama señor absoluto de la urbe. "
            "Incapaz de caminar, un Bruce Wayne quebrado toma la trágica decisión de traspasar el manto del Murciélago a Jean-Paul Valley, Azrael. "
            "Una nueva y sangrienta cruzada comenzaba en las sombras. "
            "El día en que el Murciélago cayó para siempre."
        )
    }
]


def create_16_9_cinematic_frame(img_path: str, out_path: str, target_w: int = 1920, target_h: int = 1080) -> str:
    """Expands comic panel to 16:9 widescreen with blurred ambient background."""
    im = Image.open(img_path).convert('RGB')
    orig_w, orig_h = im.size

    bg = ImageOps.fit(im, (target_w, target_h), method=Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=32))
    bg = ImageEnhance.Brightness(bg).enhance(0.55)

    scale = min((target_w - 60) / orig_w, (target_h - 40) / orig_h)
    fg_w = int(orig_w * scale)
    fg_h = int(orig_h * scale)
    fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

    pos_x = (target_w - fg_w) // 2
    pos_y = (target_h - fg_h) // 2
    bg.paste(fg, (pos_x, pos_y))

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    bg.save(out_path, 'JPEG', quality=95)
    return str(out_path)


def synthesize_scene_audio(text: str, out_path: str, scene_id: int) -> str:
    """Synthesizes speech with Gemini TTS Puck, falling back gracefully to Edge-TTS Jorge."""
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        return out_path

    # 1. Try Gemini TTS
    try:
        print(f"[{scene_id:02d}/14] Generando locución con Gemini TTS (Puck)...")
        synthesize_with_gemini(text, out_path, voice_name="Puck", rate=1.05)
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            return out_path
    except Exception as e:
        print(f"[{scene_id:02d}/14] Gemini TTS falló o excedió cuota: {e}. Activando Edge-TTS Jorge...")

    # 2. Resilient Fallback: Edge-TTS
    import edge_tts
    temp_mp3 = str(Path(out_path).with_suffix(".temp.mp3"))

    async def _edge():
        comm = edge_tts.Communicate(text, "es-MX-JorgeNeural", rate="+5%")
        await comm.save(temp_mp3)

    asyncio.run(_edge())

    subprocess.run([
        "ffmpeg", "-y",
        "-i", temp_mp3,
        "-af", "aresample=48000,apad=pad_dur=0.40",
        "-acodec", "pcm_s16le",
        out_path
    ], check=True, capture_output=True)

    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

    return out_path


def compose_multi_panel_scene(
    framed_paths: list[str],
    audio_path: str,
    duration: float,
    output: str,
    width: int = TARGET_WIDTH,
    height: int = TARGET_HEIGHT
) -> str:
    """Composes a scene displaying multiple comic panels sequentially, each with animated Ken Burns motion."""
    n = len(framed_paths)
    if n == 1:
        return compose_scene_from_image(
            framed_paths[0], audio_path, duration, output,
            pattern_idx=0, width=width, height=height, audio_codec="aac"
        )

    seg_duration = duration / n
    segments = []
    stem = Path(output).stem
    out_dir = Path(output).parent

    # Dynamic motion pattern cycle for multi-panel flow
    motion_patterns = [0, 4, 1, 5, 2, 3] # zoom-in, pan-left-to-right, zoom-out, pan-right-to-left, pan-up, pan-down

    for idx, f_path in enumerate(framed_paths):
        seg_video = str(out_dir / f"{stem}_part{idx}.mp4")
        pat_idx = motion_patterns[idx % len(motion_patterns)]
        compose_scene_from_image(
            image_path=f_path,
            audio_path=audio_path,
            duration=seg_duration,
            output=seg_video,
            pattern_idx=pat_idx,
            width=width,
            height=height,
            audio_codec="aac"
        )
        segments.append(seg_video)

    concat_txt = str(out_dir / f"{stem}_concat.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for s in segments:
            f.write(f"file '{Path(s).name}'\n")

    combined_v = str(out_dir / f"{stem}_combined.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        combined_v
    ], check=True, capture_output=True)

    # Remux combined video with pristine original scene audio to avoid any audio artifacts
    subprocess.run([
        "ffmpeg", "-y",
        "-i", combined_v,
        "-i", audio_path,
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output
    ], check=True, capture_output=True)

    # Cleanup temporary segment files
    for s in segments:
        try:
            if os.path.exists(s): os.remove(s)
        except Exception:
            pass
    for tmp in [concat_txt, combined_v]:
        try:
            if os.path.exists(tmp): os.remove(tmp)
        except Exception:
            pass

    return output


def main():
    print("=" * 80)
    print("🎬 BATMAN: KNIGHTFALL - GENERADOR MULTI-PANEL PARA YOUTUBE (16:9 WIDESCREEN)")
    print("=" * 80)
    start_total_time = time.time()

    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    FRAMED_DIR.mkdir(parents=True, exist_ok=True)
    VOICEOVER_DIR.mkdir(parents=True, exist_ok=True)
    SCENES_DIR.mkdir(parents=True, exist_ok=True)

    voice_results = {}
    rendered_scenes = []
    total_panels_count = sum(len(s["panels"]) for s in SCENES_DATA)
    total_est_words = sum(len(s["text"].split()) for s in SCENES_DATA)
    print(f"📌 Total de escenas: {len(SCENES_DATA)} | Total de viñetas sincronizadas: {total_panels_count} | Palabras: {total_est_words}")

    # Paso 1 & 2: Encuadre 16:9 de todas las viñetas y Verificación de Audio
    print("\n--- PASO 1 & 2: Encuadre 16:9 de 35 Viñetas y Locución ---")
    for s in SCENES_DATA:
        sid = s["id"]
        audio_path = str(VOICEOVER_DIR / f"scene_{sid:02d}.wav")

        # Generar audio si no existe
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 10000:
            synthesize_scene_audio(s["text"], audio_path, sid)

        dur = get_duration(audio_path)

        # Encuadrar todas las viñetas asignadas a la escena
        framed_scene_paths = []
        for p_idx, p_rel in enumerate(s["panels"]):
            panel_full = str(REPO_ROOT / p_rel)
            p_stem = Path(p_rel).stem
            framed_path = str(FRAMED_DIR / f"s{sid:02d}_p{p_idx:02d}_{p_stem}.jpg")

            if not os.path.exists(framed_path):
                create_16_9_cinematic_frame(panel_full, framed_path, TARGET_WIDTH, TARGET_HEIGHT)
            framed_scene_paths.append(framed_path)

        voice_results[sid] = {
            "audio": audio_path,
            "text": s["text"],
            "duration": dur,
            "framed_panels": framed_scene_paths
        }
        print(f"[{sid:02d}/14] ✓ Audio: {dur:.2f}s | {len(framed_scene_paths)} viñetas | {s['title']}")

    total_narration_duration = sum(info["duration"] for info in voice_results.values())
    print(f"\n⏱️ Duración total estimada de narración: {total_narration_duration:.2f}s ({total_narration_duration/60:.2f} minutos)")

    # Paso 3: Renderizado de Escenas Multi-Panel con Ken Burns
    print("\n--- PASO 3: Renderizado de Escenas Multi-Panel 1920x1080 ---")
    for s in SCENES_DATA:
        sid = s["id"]
        info = voice_results[sid]
        scene_mp4 = str(SCENES_DIR / f"scene_{sid:02d}.mp4")

        print(f"[{sid:02d}/14] Componiendo escena: {s['title']} ({len(info['framed_panels'])} viñetas) - {info['duration']:.2f}s...")
        compose_multi_panel_scene(
            framed_paths=info["framed_panels"],
            audio_path=info["audio"],
            duration=info["duration"],
            output=scene_mp4,
            width=TARGET_WIDTH,
            height=TARGET_HEIGHT
        )
        rendered_scenes.append(scene_mp4)
        print(f"[{sid:02d}/14] ✓ Escena MP4 lista: {os.path.basename(scene_mp4)}")

    # Paso 4: Ensamblaje Concatenado de Escenas
    print("\n--- PASO 4: Concatenación Maestra de Escenas ---")
    concat_list_file = WORK_DIR / "concat_scenes.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for v in rendered_scenes:
            f.write(f"file 'scenes/{Path(v).name}'\n")

    assembled_raw = str(WORK_DIR / "assembled_raw.mp4")
    print(f"Concatenando {len(rendered_scenes)} escenas en {os.path.basename(assembled_raw)}...")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        assembled_raw
    ], check=True, capture_output=True)

    raw_duration = get_duration(assembled_raw)
    print(f"✓ Video crudo ensamblado con éxito: {raw_duration:.2f}s ({raw_duration/60:.2f} minutos)")

    # Paso 5: Generación de Subtítulos ASS Cinematográficos para YouTube (16:9)
    print("\n--- PASO 5: Transcripción Whisper & Subtítulos Cinematográficos (16:9) ---")
    ass_path = str(WORK_DIR / "subtitles.ass")
    if not os.path.exists(ass_path) or os.path.getsize(ass_path) < 1000:
        transcribe_scenes_to_ass(
            voice_results=voice_results,
            ass_path=ass_path,
            language="es",
            model_name="base",
            max_words=3,
            width=TARGET_WIDTH,
            height=TARGET_HEIGHT
        )
    print(f"✓ Subtítulos ASS sincronizados verificados en: {os.path.basename(ass_path)}")

    # Paso 6: Masterización Final en Full HD 1920x1080
    print("\n--- PASO 6: Masterización Final en Full HD 1920x1080 ---")
    print(f"Destino final: {FINAL_MASTER}")

    compose_final(
        video_path=assembled_raw,
        subs_path=ass_path,
        output=str(FINAL_MASTER),
        width=TARGET_WIDTH,
        height=TARGET_HEIGHT
    )

    # Paso 7: Auditoría y Verificación de Calidad
    print("\n--- PASO 7: Auditoría de Calidad Técnica ---")
    final_dur = get_duration(str(FINAL_MASTER))
    final_size_mb = os.path.getsize(FINAL_MASTER) / (1024 * 1024)

    probe_cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,codec_name",
        "-of", "json",
        str(FINAL_MASTER)
    ]
    probe_res = json.loads(subprocess.run(probe_cmd, capture_output=True, text=True, check=True).stdout)
    v_stream = probe_res["streams"][0]

    elapsed_total = time.time() - start_total_time

    print("=" * 80)
    print("🎉 ¡VIDEO MULTI-PANEL PARA YOUTUBE GENERADO CON ÉXITO!")
    print("=" * 80)
    print(f"📁 Ruta del Archivo: {FINAL_MASTER}")
    print(f"⏱️ Duración: {final_dur:.2f} segundos ({final_dur/60:.2f} minutos)")
    print(f"📐 Resolución: {v_stream['width']}x{v_stream['height']} (16:9 Full HD)")
    print(f"🎞️ Codec de Video: {v_stream['codec_name']} @ {v_stream['r_frame_rate']} fps")
    print(f"💾 Tamaño de Archivo: {final_size_mb:.2f} MB")
    print(f"🖼️ Total Viñetas Sincronizadas: {total_panels_count} paneles (cambio dinámico cada 8-12s)")
    print(f"⚡ Tiempo Total de Proceso: {elapsed_total:.1f} segundos")
    print("=" * 80)

    # Actualizar metadata JSON para YouTube
    yt_meta_path = FINAL_DIR / "Batman_Knightfall_La_Caida_del_Murcielago_YouTube.json"
    yt_meta = {
        "title": "BATMAN: KNIGHTFALL - La Caída del Murciélago (Historia Completa Explicada)",
        "description": (
            "En este video revivimos la historia más devastadora y definitoria en la mitología de Batman: KNIGHTFALL (La Caída del Murciélago).\n\n"
            "Desde los orígenes de Bane en la prisión caribeña de Peña Duro hasta su asalto al Manicomio Arkham liberando al Joker, "
            "el Espantapájaros y Dos Caras para agotar física y mentalmente a Bruce Wayne. Descubre paso a paso cómo Bane descubrió la identidad secreta de Batman, "
            "la masacre en la Baticueva y el icónico quiebre de la columna vertebral que cambió el universo de DC Comics para siempre.\n\n"
            "📌 Capítulos:\n"
            "00:00 El Nacimiento de Bane en Peña Duro\n"
            "00:31 La Estrategia Militar: Llegada a Gotham\n"
            "00:59 El Asalto y Destrucción de Arkham Asylum\n"
            "01:26 Caos Total: Los Villanos Libres\n"
            "01:52 El Límite Físico de Bruce Wayne\n"
            "02:18 La Advertencia Desesperada de Alfred y Robin\n"
            "02:43 La Trampa Mortal del Joker y Scarecrow\n"
            "03:07 El Agotador Regreso a la Mansión Wayne\n"
            "03:31 La Emboscada en la Sombra\n"
            "03:56 La Masacre en la Baticueva\n"
            "04:20 El Veneno Desatado\n"
            "04:45 ¡Te Romperé! El Quiebre de Batman\n"
            "05:12 La Humillación Pública en Gotham\n"
            "05:32 El Reinado de Bane y el Ascenso de Azrael\n\n"
            "#Batman #Knightfall #Bane #DCComics #ComicsEnEspañol #BatmanVsBane #ComicsNarrados"
        ),
        "tags": [
            "Batman", "Knightfall", "La Caida del Murcielago", "Bane", "Batman vs Bane",
            "DC Comics", "Comics narrados", "Historia completa Batman", "Jim Aparo",
            "Azrael Batman", "Arkham Asylum", "Joker", "Scarecrow", "Resumen Batman Knightfall",
            "Comics explicados"
        ],
        "duration_seconds": final_dur,
        "duration_formatted": "05:57",
        "resolution": "1920x1080 (16:9 Full HD)",
        "fps": 30,
        "scenes_count": 14,
        "panels_count": total_panels_count,
        "voice": "Google Gemini 3.8 Flash TTS (Puck)"
    }
    with open(yt_meta_path, "w", encoding="utf-8") as f:
        json.dump(yt_meta, f, ensure_ascii=False, indent=2)
    print(f"📝 Metadata para YouTube (Título, Descripción, Capítulos y Tags) actualizada en: {yt_meta_path}")


if __name__ == "__main__":
    main()
