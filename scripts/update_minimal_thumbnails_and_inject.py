"""
Engine: Miniaturas con Poco Texto e Imagen Interesante Protagonista (Slots 51 al 65)
===================================================================================
1. Texto ultra-conciso (2 a 4 palabras máximo por video).
2. Sin banners oscuros gigantescos que tapen el arte.
3. El arte del cómic es 100% visible, centrado y protagonista.
4. Inyección obligatoria en el fotograma exacto t=0.000s de cada video.
"""

import os
import sys
import json
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
QUEUE_DIR = PROJECT_ROOT / "scheduled_queue"
CURATED_BASE = PROJECT_ROOT / "assets" / "curated_panels"
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
        # Doble página o apaisada: fondo desenfocado y viñeta centrada grande
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
        # Retrato o vertical: reescalar y centrar para máxima acción
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

    # Si el texto es más ancho que 980px, ajustar tamaño automáticamente
    if tw > 960:
        adjusted_size = int(font_size * (940 / tw))
        font = ImageFont.truetype(FONT_IMPACT, adjusted_size)
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

    tx = (1080 - tw) // 2 - bbox[0]
    ty = text_y

    # Sombra localizada suave directamente detrás de las letras (cero franjas oscuras que tapen el cómic)
    canvas_rgba = canvas.convert("RGBA")
    shadow_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((tx, ty + 7), text, font=font, fill=(0, 0, 0, 240), stroke_width=20, stroke_fill=(0, 0, 0, 240))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))

    canvas_rgba = Image.alpha_composite(canvas_rgba, shadow_layer)

    # Texto nítido con trazo negro pronunciado para máxima legibilidad
    text_layer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    t_draw.text((tx, ty), text, font=font, fill=text_color, stroke_width=11, stroke_fill=(0, 0, 0))

    final_im = Image.alpha_composite(canvas_rgba, text_layer).convert("RGB")
    final_im.save(output_path, "JPEG", quality=95, optimize=True)
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
        print(f"  [ERROR] Video resultante corrupto: {temp_out.stat().st_size} bytes")
        temp_out.unlink()
        return False

    # Extraer frame 0 para auditoría estricta
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
    return True

MINIMAL_THUMBS_CONFIG = [
    {
        "slot": 51,
        "folder": "51_spiderman_escorpion_mandibula_superior",
        "source_art": CURATED_BASE / "51_spiderman_escorpion_mandibula_superior" / "scene_03.jpg",
        "text": "¡MANDÍBULA DESTROZADA!",
        "text_y": 240,
        "color": (255, 235, 0),
        "size": 105
    },
    {
        "slot": 52,
        "folder": "52_batman_virus_doomsday_devastator",
        "source_art": CURATED_BASE / "52_batman_virus_doomsday_devastator" / "scene_03.jpg",
        "text": "¡SE INYECTÓ EL VIRUS!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 105
    },
    {
        "slot": 53,
        "folder": "53_spiderman_back_in_black_kingpin",
        "source_art": CURATED_BASE / "53_spiderman_back_in_black_kingpin" / "scene_03.jpg",
        "text": "¡HUMILLÓ A KINGPIN!",
        "text_y": 220,
        "color": (255, 35, 45),
        "size": 108
    },
    {
        "slot": 54,
        "folder": "54_sentry_descuartiza_ares_siege",
        "source_art": CURATED_BASE / "54_sentry_descuartiza_ares_siege" / "scene_03.jpg",
        "text": "¡LO PARTIÓ EN DOS!",
        "text_y": 240,
        "color": (255, 235, 0),
        "size": 110
    },
    {
        "slot": 55,
        "folder": "55_batman_que_rie_dark_multiverse",
        "source_art": CURATED_BASE / "55_batman_que_rie_dark_multiverse" / "scene_04.jpg",
        "text": "¡EL BATMAN QUE RÍE!",
        "text_y": 220,
        "color": (255, 35, 45),
        "size": 108
    },
    {
        "slot": 56,
        "folder": "56_hellboy_mano_derecha_apocalipsis",
        "source_art": CURATED_BASE / "56_hellboy_mano_derecha_apocalipsis" / "scene_04.jpg",
        "text": "¡LA MANO DEL DESTINO!",
        "text_y": 200,
        "color": (255, 235, 0),
        "size": 105
    },
    {
        "slot": 57,
        "folder": "57_injustice_alfred_superman",
        "source_art": CURATED_BASE / "57_injustice_alfred_superman" / "scene_03.jpg",
        "text": "¡ALFRED VS SUPERMAN!",
        "text_y": 260,
        "color": (255, 235, 0),
        "size": 105
    },
    {
        "slot": 58,
        "folder": "58_batman_recupera_manto_derrota_azrael",
        "source_art": CURATED_BASE / "58_batman_recupera_manto_derrota_azrael" / "scene_02.jpg",
        "text": "¡LA CAÍDA DE AZRAEL!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 108
    },
    {
        "slot": 59,
        "folder": "59_doctor_doom_destruye_thanos_secret_wars",
        "source_art": CURATED_BASE / "59_doctor_doom_destruye_thanos_secret_wars" / "scene_04.jpg",
        "text": "¡EL FIN DE THANOS!",
        "text_y": 180,
        "color": (255, 35, 45),
        "size": 110
    },
    {
        "slot": 60,
        "folder": "60_reverse_flash_odio_thawne",
        "source_art": CURATED_BASE / "60_reverse_flash_odio_thawne" / "scene_02.jpg",
        "text": "¡EL PEOR VILLANO!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 110
    },
    {
        "slot": 61,
        "folder": "61_lobo_expulsado_cielo_infierno",
        "source_art": CURATED_BASE / "61_lobo_expulsado_cielo_infierno" / "scene_03.jpg",
        "text": "¡LOBO ES INMORTAL!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 108
    },
    {
        "slot": 62,
        "folder": "62_hulk_world_war_venganza_illuminati",
        "source_art": CURATED_BASE / "62_hulk_world_war_venganza_illuminati" / "scene_02.jpg",
        "text": "¡LA FURIA DE HULK!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 108
    },
    {
        "slot": 63,
        "folder": "63_azrael_batman_destroza_bane",
        "source_art": CURATED_BASE / "63_azrael_batman_destroza_bane" / "scene_03.jpg",
        "text": "¡DESTROZÓ A BANE!",
        "text_y": 220,
        "color": (255, 35, 45),
        "size": 110
    },
    {
        "slot": 64,
        "folder": "64_plastic_man_pesadilla_batman",
        "source_art": CURATED_BASE / "64_plastic_man_pesadilla_batman" / "scene_04.jpg",
        "text": "¡EL TERROR DE BATMAN!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 105
    },
    {
        "slot": 65,
        "folder": "65_venom_dios_de_la_luz_knull",
        "source_art": CURATED_BASE / "65_venom_dios_de_la_luz_knull" / "scene_04.jpg",
        "text": "¡EL DIOS DE LA LUZ!",
        "text_y": 220,
        "color": (255, 235, 0),
        "size": 108
    }
]

def main():
    print("=" * 80)
    print("🚀 ACTUALIZANDO MINIATURAS: POCO TEXTO E IMAGEN PROTAGONISTA (SLOTS 51 AL 65)")
    print("=" * 80)

    success_count = 0
    for cfg in MINIMAL_THUMBS_CONFIG:
        sid = cfg["slot"]
        folder_matches = list(QUEUE_DIR.glob(f"{sid}_*"))
        if not folder_matches:
            print(f"⚠️ [SKIP] No se encontró carpeta para slot {sid}")
            continue

        slot_dir = folder_matches[0]
        thumb_file = slot_dir / "thumb.jpg"
        video_file = slot_dir / "video.mp4"

        print(f"\nProcesando Slot {sid}: {slot_dir.name}...")
        print(f"  Texto: {cfg['text']}")
        print(f"  Fuente arte: {cfg['source_art'].name}")

        # 1. Generar miniatura minimalista con imagen protagonista
        render_minimal_text_thumb(
            image_path=cfg["source_art"],
            text=cfg["text"],
            output_path=thumb_file,
            text_y=cfg["text_y"],
            text_color=cfg["color"],
            font_size=cfg["size"]
        )
        print(f"  ✓ Miniatura guardada: {thumb_file.stat().st_size / 1024:.1f} KB")

        # 2. Inyectar como primer frame exacto (t=0.000s)
        if video_file.exists():
            print(f"  ⚡ Inyectando en frame 0 de {video_file.name}...")
            ok = inject_thumbnail_into_video(video_file, thumb_file, slot_dir.name)
            if ok:
                print(f"  ✓ Frame 0 inyectado exitosamente.")
                success_count += 1
            else:
                print(f"  ❌ Error inyectando frame 0")

    print("\n" + "=" * 80)
    print(f"🎉 FINALIZADO: {success_count} de {len(MINIMAL_THUMBS_CONFIG)} videos actualizados con éxito!")
    print("=" * 80)

if __name__ == "__main__":
    main()
