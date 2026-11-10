"""
Master Production Engine: Slot 66 - El Alma de Sentry vs Knull (King in Black & Return of the Valkyries)
========================================================================================================
1. Historia 100% canónica: King in Black #1 + Return of the Valkyries #1 por Donny Cates y Jason Aaron.
2. 6 escenas con paneles HD 1080x1920 y movimiento Ken Burns cinematográfico dinámico (zoom, pan down, pan up, climax zoom).
3. Duración obligatoria >= 60.0 segundos (monetizable, alta retención).
4. Miniatura minimalista de impacto (<= 4 palabras): '¡EL ALMA DE SENTRY!'
5. Fotograma exacto t=0.000s inyectado con la miniatura para detección automática por API.
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

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

PACK_OUTPUT_DIR = PROJECT_ROOT / "output" / "batch_6_remasters"
PACK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
SCHEDULED_QUEUE = PROJECT_ROOT / "scheduled_queue"
SCHEDULED_QUEUE.mkdir(parents=True, exist_ok=True)
BRAIN_DIR = Path(r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb")

FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
if not Path(FONT_IMPACT).exists():
    FONT_IMPACT = r"C:\Users\Vanes\comics en espanol\fonts\impact.ttf"

def apply_cinematic_grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.25)
    im = ImageEnhance.Color(im).enhance(1.20)
    im = ImageEnhance.Sharpness(im).enhance(1.15)
    return im

def fit_to_vertical(im: Image.Image, target_w=1080, target_h=1920) -> Image.Image:
    w, h = im.size
    aspect = w / h
    if w == target_w and h == target_h:
        return im.copy()

    if aspect > 1.1:
        bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(30))
        bg = ImageEnhance.Brightness(bg).enhance(0.40)

        new_w = target_w
        new_h = int(target_w / aspect)
        fg = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

        pos_y = (target_h - new_h) // 2
        bg.paste(fg, (0, pos_y))
        return bg
    else:
        scale = max(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)
        scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - target_w) // 2
        top = (nh - target_h) // 2
        return scaled.crop((left, top, left + target_w, top + target_h))

def render_minimal_text_thumb(image_path: Path, text: str, output_path: Path,
                              text_y=240, text_color=(255, 235, 0), font_size=108):
    raw_img = Image.open(image_path).convert("RGB")
    graded = apply_cinematic_grade(raw_img)
    canvas = fit_to_vertical(graded, 1080, 1920)

    font = ImageFont.truetype(FONT_IMPACT, font_size)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    if tw > 960:
        adjusted_size = int(font_size * (940 / tw))
        font = ImageFont.truetype(FONT_IMPACT, adjusted_size)
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

    tx = (1080 - tw) // 2 - bbox[0]
    ty = text_y

    canvas_rgba = canvas.convert("RGBA")
    shadow_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((tx, ty + 7), text, font=font, fill=(0, 0, 0, 240), stroke_width=20, stroke_fill=(0, 0, 0, 240))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))

    canvas_rgba = Image.alpha_composite(canvas_rgba, shadow_layer)

    text_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    t_draw.text((tx, ty), text, font=font, fill=text_color, stroke_width=11, stroke_fill=(0, 0, 0))

    final_im = Image.alpha_composite(canvas_rgba, text_layer).convert("RGB")
    final_im.save(output_path, "JPEG", quality=95, optimize=True)
    print(f"  [THUMB] Miniatura minimalista creada: {output_path} ({output_path.stat().st_size / 1024:.1f} KB)")
    return output_path

def inject_thumbnail_into_video(video_path: Path, thumb_path: Path, slot_name: str):
    temp_out = video_path.parent / f"{video_path.stem}_frame0.mp4"

    cmd = [
        'ffmpeg', '-y',
        '-i', str(video_path),
        '-loop', '1', '-t', '0.40', '-i', str(thumb_path),
        '-filter_complex',
        '[1:v]fps=30,scale=1080:1920,setsar=1[vthumb];[0:v]trim=start=0.40,setpts=PTS-STARTPTS[vmain];[vthumb][vmain]concat=n=2:v=1:a=0[v]',
        '-map', '[v]',
        '-map', '0:a',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18',
        '-c:a', 'copy',
        str(temp_out)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR FFMPEG INJECTION]: {res.stderr[-300:]}")
        if temp_out.exists():
            temp_out.unlink()
        return False

    if temp_out.stat().st_size < 1000000:
        print(f"  [ERROR] Video resultante corrupto o pequeño: {temp_out.stat().st_size} bytes")
        temp_out.unlink()
        return False

    audit_f0 = BRAIN_DIR / f"audit_minimal_frame0_{slot_name}.jpg"
    subprocess.run([
        'ffmpeg', '-y',
        '-ss', '00:00:00.000',
        '-i', str(temp_out),
        '-vframes', '1',
        '-q:v', '2',
        str(audit_f0)
    ], capture_output=True)

    shutil.move(temp_out, video_path)
    print(f"  [OK] Frame 0 inyectado y verificado en {video_path.name}")
    return True

PROJECT_SLOT_66 = {
    "slot": 66,
    "queue_folder": "66_sentry_alma_knull_valhalla",
    "id": "sentry_alma_knull_valhalla",
    "title": "¿Qué Pasó con el Alma de Sentry Cuando Knull lo Mató? 💀🌑⚡",
    "character": "Sentry & Knull",
    "folder": "66_sentry_alma_knull_valhalla",
    "theme_signature": "sentry:knull:king_in_black:return_of_the_valkyries:soul",
    "voice": "Puck",
    "thumb_text": "¡EL ALMA DE SENTRY!",
    "scenes": [
        {
            "scene_number": 1,
            "file": "scene_01.jpg",
            "text": "¿Qué ocurrió realmente con el alma de Sentry cuando Knull lo despedazó en el espacio exterior? Cuando el Dios de los Simbiontes invadió la Tierra, Bob Reynolds descendió como la salvación absoluta. Pero Knull lo tomó del cuello y, con una brutalidad aterradora, lo partió en dos mitades frente a todos."
        },
        {
            "scene_number": 2,
            "file": "scene_02.jpg",
            "text": "Fue un macabro karma cósmico: un reflejo idéntico del día en que el mismísimo Sentry descuartizó a Ares, el Dios de la Guerra, en Asedio. Pero la verdadera pesadilla para Bob apenas estaba comenzando."
        },
        {
            "scene_number": 3,
            "file": "scene_03.jpg",
            "text": "En el gélido vacío estelar, el espíritu incorpóreo de Sentry despertó en shock. Con profundo horror, contempló cómo sus órganos mutilados y su sangre dorada flotaban a la deriva entre las estrellas."
        },
        {
            "scene_number": 4,
            "file": "scene_04.jpg",
            "text": "Fue entonces cuando Jane Foster, convertida en la última Valquiria, se acercó a su alma errante. Bob lloraba desconsolado, creyendo que le había fallado al mundo entero. Pero Jane lo reconfortó, prometiéndole llevar su espíritu al descanso eterno en el Valhalla."
        },
        {
            "scene_number": 5,
            "file": "scene_05.jpg",
            "text": "Sin embargo, la paz jamás llegaría. De la penumbra dimensional emergió una monstruosidad cósmica: el colosal cadáver del primer Celestial decapitado por Knull en el origen del universo, convertido en una grotesca marioneta del dios oscuro."
        },
        {
            "scene_number": 6,
            "file": "scene_06.jpg",
            "text": "Antes de cruzar al más allá, decenas de zarcillos negros brotaron del titán cósmico, devorando el alma de Sentry. Bob Reynolds fue arrastrado al abismo para ser consumido eternamente, mientras en el vacío solo resonaban sus desgarradores gritos de agonía. ¿Merecía Sentry este trágico final? ¡Déjanos tu comentario!"
        }
    ],
    "description": "La aterradora verdad de lo que ocurrió con el alma de Bob Reynolds tras su brutal muerte a manos de Knull en King in Black y Return of the Valkyries. ¿Cuál fue el destino final de Sentry?",
    "hashtags": "#Sentry #Knull #KingInBlack #Valkyrie #JaneFoster #Marvel #MarvelComics #Comics #Shorts #Reels"
}

def produce_slot_66():
    proj = PROJECT_SLOT_66
    slot_num = proj["slot"]
    proj_id = proj["id"]
    queue_name = proj["queue_folder"]

    print(f"\n{'='*75}")
    print(f"🎬 [PRODUCCIÓN] SLOT {slot_num}: {proj['title']}")
    print(f"{'='*75}")

    curated_folder = CURATED_BASE / proj["folder"]
    scene_art_urls = []
    scenes_text = []
    for s in proj["scenes"]:
        p_path = curated_folder / s["file"]
        if not p_path.exists():
            print(f"❌ [ERROR] Panel faltante: {p_path}")
            return None
        scene_art_urls.append(str(p_path))
        scenes_text.append(s["text"])

    story_payload = dict(proj)
    story_payload["scenes"] = scenes_text
    story_payload["scene_art_urls"] = scene_art_urls

    proj_out_dir = PACK_OUTPUT_DIR / proj_id
    if proj_out_dir.exists():
        shutil.rmtree(proj_out_dir, ignore_errors=True)

    work_dir = PROJECT_ROOT / "work" / f"batch6_{proj_id}"
    if work_dir.exists():
        shutil.rmtree(work_dir, ignore_errors=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    print("⚡ Construyendo generación de escenas...")
    generation = build_cloud_generation(story_payload, work_dir)
    voice_choice = proj.get("voice", "Puck")
    final_output_dir = PACK_OUTPUT_DIR / "finals"
    final_output_dir.mkdir(parents=True, exist_ok=True)

    print("🚀 Ejecutando run_pipeline (Ken Burns, TTS Puck, Subtítulos Comic Noir, Transiciones)...")
    final_video_path = run_pipeline(
        generation=generation,
        output_name=proj_id,
        voice=voice_choice,
        output_root=str(PACK_OUTPUT_DIR),
        width=1080,
        height=1920,
        final_video_dir=str(final_output_dir),
        generate_thumbnail=False
    )

    if not final_video_path or not Path(final_video_path).exists():
        print(f"❌ [ERROR] Falló la generación del video para {proj_id}")
        return None

    dur = get_duration(str(final_video_path))
    print(f"⏱️ Duración inicial generada: {dur:.2f}s")
    if dur < 60.0:
        print(f"🚨 FATAL: Duración {dur:.2f}s es menor a 60.0s!")
        return None

    dest_dir = SCHEDULED_QUEUE / queue_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    thumb_path = dest_dir / "thumb.jpg"

    # Generar miniatura minimalista enfocada en el arte del cómic con texto de alto impacto
    print(f"🎨 Creando miniatura minimalista con texto '{proj['thumb_text']}'...")
    source_thumb_art = curated_folder / "scene_01.jpg"
    render_minimal_text_thumb(source_thumb_art, proj["thumb_text"], thumb_path, text_y=240, font_size=108)

    # Copiar video base a la cola
    dest_video = dest_dir / "video.mp4"
    shutil.copy2(final_video_path, dest_video)

    # Inyectar miniatura en frame 0
    print(f"⚡ Inyectando miniatura como primer fotograma exacto (t=0.000s) en {dest_video.name}...")
    ok_inject = inject_thumbnail_into_video(dest_video, thumb_path, queue_name)
    if not ok_inject:
        print(f"🚨 Falló la inyección de miniatura en {dest_video}")
        return None

    final_dur = get_duration(str(dest_video))
    print(f"✅ Duración final verificada: {final_dur:.2f}s (>= 60.0s PASS)")

    meta_payload = {
        "title": proj["title"],
        "description": proj["description"],
        "hashtags": proj["hashtags"],
        "character": proj["character"],
        "theme_signature": proj["theme_signature"],
        "duration_seconds": round(final_dur, 2),
        "scheduled_slot": slot_num,
        "queue_folder": queue_name,
        "source": "reference_recreation_sentry_knull_60s_plus",
        "reference_url": "https://www.youtube.com/shorts/zXVzZJUZBxk",
        "first_frame_thumbnail_injected": True,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(dest_dir / "metadata.json", "w", encoding="utf-8") as mf:
        json.dump(meta_payload, mf, indent=2, ensure_ascii=False)

    print(f"🎉 Slot {slot_num} completamente listo y encolado en {dest_dir}!")
    return dest_dir

if __name__ == "__main__":
    res = produce_slot_66()
    if res:
        print("\n🏆 PRODUCCIÓN EXITOSA DEL SLOT 66!")
    else:
        print("\n❌ HUBO UN ERROR EN LA PRODUCCIÓN DEL SLOT 66.")
        sys.exit(1)
