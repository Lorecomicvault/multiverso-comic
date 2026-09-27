import os
import math
import random
import glob
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFilter

def generate_jagged_line(length, roughness=40):
    """Genera perfil fractal de rasgado mediante armónicos multi-octava."""
    oct1 = [random.uniform(-1, 1) for _ in range(8)]
    oct2 = [random.uniform(-1, 1) for _ in range(16)]
    oct3 = [random.uniform(-1, 1) for _ in range(32)]
    points = []
    for i in range(length + 1):
        rel = i / length
        o1 = oct1[min(int(rel * 7), 6)] * (1 - (rel * 7 % 1)) + oct1[min(int(rel * 7) + 1, 7)] * (rel * 7 % 1)
        o2 = oct2[min(int(rel * 14), 13)] * (1 - (rel * 14 % 1)) + oct2[min(int(rel * 14) + 1, 14)] * (rel * 14 % 1)
        o3 = oct3[min(int(rel * 30), 29)] * (1 - (rel * 30 % 1)) + oct3[min(int(rel * 30) + 1, 30)] * (rel * 30 % 1)
        points.append((o1 * 0.52 + o2 * 0.33 + o3 * 0.15) * roughness)
    return points

def render_torn_frame(img_a, img_b, progress, width=1080, height=1920, direction="left_to_right",
                      roughness=40, fiber_color=(235, 215, 175), fiber_width=22):
    """Mezcla dos imágenes generando borde deshilachado y sombra de profundidad 3D."""
    # Asegurar dimensiones exactas
    if img_a.size != (width, height):
        img_a = img_a.resize((width, height), Image.Resampling.LANCZOS)
    if img_b.size != (width, height):
        img_b = img_b.resize((width, height), Image.Resampling.LANCZOS)

    margin = 250
    slant_deg = 12 if direction == "left_to_right" else (-12 if direction == "right_to_left" else 8)
    slant_rad = math.tan(math.radians(slant_deg))
    mid_y = height / 2.0
    offsets = generate_jagged_line(height, roughness=roughness)

    center_x = -margin + progress * (width + 2 * margin) if direction == "left_to_right" else (width + margin) - progress * (width + 2 * margin)
    
    mask_b = Image.new("L", (width, height), 0)
    draw_b = ImageDraw.Draw(mask_b)
    poly = [(-60, -60)] if direction == "left_to_right" else [(width + 60, -60)]
    for y in range(height + 1):
        x = center_x + (y - mid_y) * slant_rad + offsets[y]
        poly.append((x, y))
    poly.append((-60, height + 60) if direction == "left_to_right" else (width + 60, height + 60))
    draw_b.polygon(poly, fill=255)

    comp = Image.composite(img_b, img_a, mask_b)

    # Sombra interna para dar volumen a la página superpuesta
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    step = 32 if direction == "left_to_right" else -32
    for y in range(0, height + 1, 2):
        x = center_x + (y - mid_y) * slant_rad + offsets[y]
        s_draw.line([(x, y), (x + step, y)], fill=(0, 0, 0, 190), width=3)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=7))

    # Borde de celulosa rasgada
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(overlay)
    r, g, b = fiber_color
    for y in range(height + 1):
        x = center_x + (y - mid_y) * slant_rad + offsets[y]
        pw = fiber_width + random.randint(-4, 4)
        x_start = x - pw if direction == "left_to_right" else x - 3
        x_end = x + 3 if direction == "left_to_right" else x + pw
        o_draw.line([(x_start, y), (x_end, y)], fill=(r, g, b, 255), width=2)

    final = Image.alpha_composite(comp.convert("RGBA"), shadow)
    final = Image.alpha_composite(final, overlay)
    return final.convert("RGB")

def build_torn_paper_clip(clip_a, clip_b, output_clip, temp_dir, duration=0.65, fps=30, direction="left_to_right"):
    """Extrae fotogramas de clips limítrofes, renderiza la transición y empaqueta en MP4."""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)
    n_frames = max(8, int(round(duration * fps)))

    # Extraer cola de clip A y cabeza de clip B
    fa_pat = os.path.join(temp_dir, "fa_%03d.png")
    fb_pat = os.path.join(temp_dir, "fb_%03d.png")
    subprocess.run(["ffmpeg", "-y", "-sseof", f"-{duration:.3f}", "-i", clip_a, "-frames:v", str(n_frames), "-vf", f"fps={fps}", fa_pat], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    subprocess.run(["ffmpeg", "-y", "-i", clip_b, "-frames:v", str(n_frames), "-vf", f"fps={fps}", fb_pat], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

    fa_files = sorted(glob.glob(os.path.join(temp_dir, "fa_*.png")))
    fb_files = sorted(glob.glob(os.path.join(temp_dir, "fb_*.png")))
    total = min(len(fa_files), len(fb_files))

    if total == 0:
        raise RuntimeError(f"No frames extracted for transition between {clip_a} and {clip_b}")

    for i in range(total):
        prog = (i + 1) / (total + 1)
        ia = Image.open(fa_files[i])
        ib = Image.open(fb_files[i])
        frame = render_torn_frame(ia, ib, prog, width=ia.width, height=ia.height, direction=direction)
        frame.save(os.path.join(temp_dir, f"torn_{i+1:03d}.png"))

    out_pat = os.path.join(temp_dir, "torn_%03d.png")
    subprocess.run(["ffmpeg", "-y", "-framerate", str(fps), "-i", out_pat, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", output_clip], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    return output_clip
