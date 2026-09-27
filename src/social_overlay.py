import math
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\segoeui.ttf"

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
ICON_DIR = ASSETS_DIR / "social_icons"


def _draw_vector_heart(draw, cx: int, cy: int, size: int, color=(255, 255, 255, 255)):
    """Draws a clean vector heart icon."""
    r = size // 3
    draw.ellipse([cx - r, cy - r, cx, cy], fill=color)
    draw.ellipse([cx, cy - r, cx + r, cy], fill=color)
    draw.polygon([
        (cx - r, cy - r // 3),
        (cx + r, cy - r // 3),
        (cx, cy + r)
    ], fill=color)


def _draw_vector_share(draw, cx: int, cy: int, size: int, color=(255, 255, 255, 255), width: int = 3):
    """Draws a modern vector share / arrow icon."""
    s2 = size // 2
    draw.polygon([
        (cx + s2, cy - s2),
        (cx + s2 - int(size * 0.45), cy - s2),
        (cx + s2, cy - s2 + int(size * 0.45))
    ], fill=color)
    draw.line([
        (cx - s2 + int(size * 0.15), cy + s2 - int(size * 0.15)),
        (cx + s2 - 2, cy - s2 + 2)
    ], fill=color, width=width)


def _draw_vector_thumbs_up(draw, cx: int, cy: int, size: int, color=(255, 255, 255, 255), scale: int = 2):
    """Draws a crisp anti-aliased vector thumbs-up hand."""
    w = int(size * 0.72)
    h = int(size * 0.68)
    bx = cx - w // 3
    by = cy - h // 4
    draw.rounded_rectangle([bx, by, bx + w, by + h], radius=3 * scale, fill=color)
    cuff_w = 4 * scale
    draw.rounded_rectangle([bx - cuff_w - 2 * scale, by, bx - 2 * scale, by + h], radius=2 * scale, fill=color)
    tw = int(size * 0.30)
    th = int(size * 0.60)
    tx = bx + 2 * scale
    ty = by - th + 4 * scale
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=3 * scale, fill=color)


def render_dual_line_card(scale: int = 2) -> Image.Image:
    """
    Renders the enlarged Dual-Line card (930x154px target size):
    Row 1: YouTube, TikTok, Instagram, Facebook (48px) + @MultiversoComic (28pt) + CANAL OFICIAL badge
    Row 2: ¡SÍGUENOS! (Ruby red), COMPARTE (Sky blue), DALE LIKE (Emerald green) (44px height)
    """
    w = 930 * scale
    h = 154 * scale
    pad = 12 * scale
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = pad, pad

    # Premium dark glassmorphic container with vibrant cyan-blue border
    d.rounded_rectangle(
        [cx, cy, cx + w, cy + h],
        radius=26 * scale,
        fill=(13, 17, 28, 246),
        outline=(56, 189, 248, 210),
        width=int(2.5 * scale)
    )

    try:
        f_brand = ImageFont.truetype(FONT_BOLD_PATH, 28 * scale)
        f_sub = ImageFont.truetype(FONT_BOLD_PATH, 18 * scale)
        f_btn = ImageFont.truetype(FONT_BOLD_PATH, 15 * scale)
    except Exception:
        f_brand = f_sub = f_btn = ImageFont.load_default()

    # --- Row 1: 4 Social Icons (48px) + Brand Name + Official Badge ---
    icons = ["youtube.png", "tiktok.png", "instagram.png", "facebook.png"]
    isz = 48 * scale
    ix = cx + 24 * scale
    iy = cy + 18 * scale
    for i, name in enumerate(icons):
        icon_path = ICON_DIR / name
        if icon_path.exists():
            ic = Image.open(icon_path).resize((isz, isz), Image.Resampling.LANCZOS)
            im.paste(ic, (int(ix + i * (isz + 10 * scale)), int(iy)), ic)

    tx = ix + 4 * (isz + 10 * scale) + 16 * scale
    d.text((tx, iy + 7 * scale), "@MultiversoComic", fill=(255, 255, 255, 255), font=f_brand)

    # Official badge
    pill_w = 155 * scale
    pill_h = 34 * scale
    pill_x = cx + w - pill_w - 24 * scale
    pill_y = cy + 25 * scale
    d.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
        radius=pill_h // 2,
        fill=(30, 41, 59, 255),
        outline=(100, 116, 139, 190),
        width=1 * scale
    )
    d.text((pill_x + 18 * scale, pill_y + 6 * scale), "CANAL OFICIAL", fill=(148, 163, 184, 255), font=f_btn)

    # Divider line
    div_y = cy + 82 * scale
    d.line([cx + 24 * scale, div_y, cx + w - 24 * scale, div_y], fill=(51, 65, 85, 180), width=1 * scale)

    # --- Row 2: 3 Action Badges (44px height, larger spacing) ---
    r2_y = cy + 93 * scale
    b_w = 270 * scale
    b_h = 44 * scale
    gap = 14 * scale

    # 1. SÍGUENOS
    b1_x = cx + 24 * scale
    d.rounded_rectangle([b1_x, r2_y, b1_x + b_w, r2_y + b_h], radius=12 * scale, fill=(225, 29, 72, 255))
    _draw_vector_heart(d, b1_x + 38 * scale, r2_y + b_h // 2, 20 * scale)
    d.text((b1_x + 60 * scale, r2_y + 9 * scale), "¡SÍGUENOS!", fill=(255, 255, 255, 255), font=f_sub)

    # 2. COMPARTE
    b2_x = b1_x + b_w + gap
    d.rounded_rectangle([b2_x, r2_y, b2_x + b_w, r2_y + b_h], radius=12 * scale, fill=(14, 165, 233, 235))
    _draw_vector_share(d, b2_x + 38 * scale, r2_y + b_h // 2, 20 * scale, width=int(2.8 * scale))
    d.text((b2_x + 60 * scale, r2_y + 9 * scale), "COMPARTE", fill=(255, 255, 255, 255), font=f_sub)

    # 3. DALE LIKE
    b3_x = b2_x + b_w + gap
    d.rounded_rectangle([b3_x, r2_y, b3_x + b_w, r2_y + b_h], radius=12 * scale, fill=(34, 197, 94, 235))
    _draw_vector_thumbs_up(d, b3_x + 38 * scale, r2_y + b_h // 2, 20 * scale, scale=scale)
    d.text((b3_x + 60 * scale, r2_y + 9 * scale), "DALE LIKE", fill=(255, 255, 255, 255), font=f_sub)

    target_w = (w + pad * 2) // scale
    target_h = (h + pad * 2) // scale
    return im.resize((target_w, target_h), Image.Resampling.LANCZOS)



def render_single_pill_card(scale: int = 2) -> Image.Image:
    """
    Renders the Compact Pill variant (900x96px target size):
    Left: 4 logos + @MultiversoComic
    Right: Unified action button with thumbs-up icon
    """
    w = 900 * scale
    h = 96 * scale
    pad = 10 * scale
    im = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = pad, pad

    d.rounded_rectangle(
        [cx, cy, cx + w, cy + h],
        radius=h // 2,
        fill=(15, 23, 42, 245),
        outline=(56, 189, 248, 190),
        width=int(2 * scale)
    )

    try:
        f_brand = ImageFont.truetype(FONT_BOLD_PATH, 23 * scale)
        f_cta = ImageFont.truetype(FONT_BOLD_PATH, 17 * scale)
    except Exception:
        f_brand = f_cta = ImageFont.load_default()

    icons = ["youtube.png", "tiktok.png", "instagram.png", "facebook.png"]
    isz = 44 * scale
    ix = cx + 22 * scale
    iy = cy + (h - isz) // 2
    for i, name in enumerate(icons):
        icon_path = ICON_DIR / name
        if icon_path.exists():
            ic = Image.open(icon_path).resize((isz, isz), Image.Resampling.LANCZOS)
            im.paste(ic, (int(ix + i * (isz + 8 * scale)), int(iy)), ic)

    tx = ix + 4 * (isz + 8 * scale) + 12 * scale
    d.text((tx, cy + 32 * scale), "@MultiversoComic", fill=(255, 255, 255, 255), font=f_brand)

    btn_w = 345 * scale
    btn_h = 56 * scale
    btn_x = cx + w - btn_w - 18 * scale
    btn_y = cy + (h - btn_h) // 2
    d.rounded_rectangle(
        [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
        radius=btn_h // 2,
        fill=(225, 29, 72, 255),
        outline=(255, 255, 255, 120),
        width=1 * scale
    )
    _draw_vector_thumbs_up(d, btn_x + 30 * scale, btn_y + btn_h // 2, 20 * scale, scale=scale)
    d.text((btn_x + 50 * scale, btn_y + 16 * scale), "¡SÍGUENOS · COMPARTE · LIKE!", fill=(255, 255, 255, 255), font=f_cta)

    target_w = (w + pad * 2) // scale
    target_h = (h + pad * 2) // scale
    return im.resize((target_w, target_h), Image.Resampling.LANCZOS)


def render_vertical_cta_frame(
    t: float,
    card_img: Image.Image,
    total_dur: float = 5.0,
    width: int = 1080,
    height: int = 1920,
    target_y: int = 1460,
) -> Image.Image:
    """
    Renders a single 1080x1920 RGBA frame with smooth cubic ease-out slide-in
    and ease-in slide-out animation.
    """
    frame = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pos_x = (width - card_img.width) // 2

    # Animation phases:
    # 0.0 - 0.5s: Slide up from below screen (y = height + 20) to target_y
    # 0.5 - (total_dur - 0.5s): Rest cleanly at target_y
    # (total_dur - 0.5s) - total_dur: Slide down back below screen
    slide_dur = 0.5
    start_y = height + 20
    out_start = total_dur - slide_dur

    if t < slide_dur:
        prog = min(1.0, max(0.0, t / slide_dur))
        ease = 1.0 - (1.0 - prog) ** 3  # cubic ease-out
        cur_y = int(start_y - (start_y - target_y) * ease)
        frame.paste(card_img, (pos_x, cur_y), card_img)
    elif t < out_start:
        cur_y = target_y
        frame.paste(card_img, (pos_x, cur_y), card_img)
    elif t <= total_dur:
        prog = min(1.0, max(0.0, (t - out_start) / slide_dur))
        ease = prog ** 2  # quad ease-in
        cur_y = int(target_y + (start_y - target_y) * ease)
        alpha = max(0.0, 1.0 - prog)
        if alpha < 0.98:
            r, g, b, a = card_img.split()
            a = a.point(lambda p: int(p * alpha))
            faded_card = Image.merge("RGBA", (r, g, b, a))
            frame.paste(faded_card, (pos_x, cur_y), faded_card)
        else:
            frame.paste(card_img, (pos_x, cur_y), card_img)

    return frame


def generate_vertical_cta_mov(
    output_mov: str,
    duration: float = 5.0,
    fps: int = 30,
    style: str = "dual_line",
    target_y: int = 1460,
) -> str:
    """
    Renders all frames for the vertical CTA and compiles them into a transparent
    QuickTime Animation (.mov with codec qtrle) at 1080x1920.
    """
    out_path = Path(output_mov)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    temp_dir = out_path.parent / f"temp_vertical_cta_{style}_frames"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(duration * fps)
    print(f"[Vertical CTA] Generando tarjeta estilo '{style}' ({total_frames} fotogramas a {fps} fps)...")

    card = render_dual_line_card() if style == "dual_line" else render_single_pill_card()

    for f_idx in range(total_frames):
        t = f_idx / fps
        frame = render_vertical_cta_frame(t, card, total_dur=duration, target_y=target_y)
        frame.save(temp_dir / f"frame_{f_idx:04d}.png")

    print(f"[Vertical CTA] Codificando a video transparente QuickTime Animation (qtrle)...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(temp_dir / "frame_%04d.png"),
        "-c:v", "qtrle",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"[Vertical CTA] ¡Video MOV transparente generado con éxito! -> {out_path} ({out_path.stat().st_size // 1024} KB)")
    return str(out_path)


def get_or_create_vertical_cta_mov(style: str = "dual_line") -> str:
    """
    Returns the path to the cached vertical CTA MOV file, generating it once if needed.
    """
    cached_mov = ASSETS_DIR / f"vertical_cta_multiversocomic_{style}.mov"
    if not cached_mov.exists() or cached_mov.stat().st_size < 1000:
        generate_vertical_cta_mov(str(cached_mov), duration=5.0, fps=30, style=style)
    return str(cached_mov)


if __name__ == "__main__":
    print("Testing social_overlay.py standalone...")
    mov_path = get_or_create_vertical_cta_mov("dual_line")
    print(f"Result: {mov_path}")
