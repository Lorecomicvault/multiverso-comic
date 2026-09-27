import math
import os
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_REG_PATH = r"C:\Windows\Fonts\segoeui.ttf"


def _get_fonts(scale: int = 2):
    try:
        f_title = ImageFont.truetype(FONT_BOLD_PATH, 16 * scale)
        f_sub = ImageFont.truetype(FONT_REG_PATH, 13 * scale)
        f_btn = ImageFont.truetype(FONT_BOLD_PATH, 14 * scale)
    except Exception:
        f_title = f_sub = f_btn = ImageFont.load_default()
    return f_title, f_sub, f_btn


def _draw_youtube_icon(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, scale: int = 2):
    """Draws a clean YouTube play logo."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8 * scale, fill=(255, 0, 0, 255))
    tx1 = x + int(w * 0.40)
    ty1 = y + int(h * 0.28)
    tx2 = tx1
    ty2 = y + int(h * 0.72)
    tx3 = x + int(w * 0.68)
    ty3 = y + int(h * 0.50)
    draw.polygon([(tx1, ty1), (tx2, ty2), (tx3, ty3)], fill=(255, 255, 255, 255))


def _draw_checkmark(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color=(255, 255, 255, 255), width: int = 2):
    """Draws a crisp anti-aliased vector checkmark."""
    p1 = (cx - size // 2, cy)
    p2 = (cx - size // 6, cy + size // 3)
    p3 = (cx + size // 2, cy - size // 2)
    draw.line([p1, p2, p3], fill=color, width=width, joint='curve')


def _draw_bell_icon(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, angle_deg: float = 0.0, ring: bool = False, scale: int = 2):
    """Draws a bell icon with optional tilt/ringing animation."""
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def rot(px, py):
        top_y = cy - size // 2
        dx = px - cx
        dy = py - top_y
        rx = dx * cos_a - dy * sin_a + cx
        ry = dx * sin_a + dy * cos_a + top_y
        return (rx, ry)

    top = rot(cx, cy - size // 2)
    b_left = rot(cx - size // 2, cy + size // 3)
    b_right = rot(cx + size // 2, cy + size // 3)
    flare_l = rot(cx - int(size * 0.65), cy + size // 2)
    flare_r = rot(cx + int(size * 0.65), cy + size // 2)
    clapper = rot(cx, cy + int(size * 0.72))

    color = (250, 204, 21, 255) if ring else (226, 232, 240, 255)
    draw.polygon([top, b_left, flare_l, flare_r, b_right], fill=color)
    draw.ellipse([clapper[0] - 3 * scale, clapper[1] - 3 * scale, clapper[0] + 3 * scale, clapper[1] + 3 * scale], fill=color)

    if ring:
        wave_color = (250, 204, 21, 220)
        draw.arc([cx - size, cy - size // 2, cx + size, cy + size // 2], start=-55, end=-10, fill=wave_color, width=2 * scale)
        draw.arc([cx - size, cy - size // 2, cx + size, cy + size // 2], start=190, end=235, fill=wave_color, width=2 * scale)


def _draw_thumbs_up(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, color=(255, 255, 255, 255), scale: int = 2):
    """Draws a modern vector thumbs up hand."""
    # Palm body
    w = int(size * 0.75)
    h = int(size * 0.70)
    bx = cx - w // 3
    by = cy - h // 4
    draw.rounded_rectangle([bx, by, bx + w, by + h], radius=3 * scale, fill=color)
    # Wrist cuff
    cuff_w = 4 * scale
    draw.rounded_rectangle([bx - cuff_w - 2 * scale, by, bx - 2 * scale, by + h], radius=2 * scale, fill=color)
    # Upright thumb
    tw = int(size * 0.32)
    th = int(size * 0.65)
    tx = bx + 2 * scale
    ty = by - th + 4 * scale
    draw.rounded_rectangle([tx, ty, tx + tw, ty + th], radius=3 * scale, fill=color)


def _draw_cursor(draw: ImageDraw.ImageDraw, x: int, y: int, scale: int = 2):
    """Draws a sleek pointer cursor."""
    points = [
        (x, y),
        (x, y + 20 * scale),
        (x + 5 * scale, y + 16 * scale),
        (x + 10 * scale, y + 25 * scale),
        (x + 14 * scale, y + 23 * scale),
        (x + 9 * scale, y + 14 * scale),
        (x + 16 * scale, y + 14 * scale),
    ]
    draw.polygon(points, fill=(255, 255, 255, 255), outline=(0, 0, 0, 255))


def render_subscribe_frame(t: float, total_dur: float = 5.5, scale: int = 2) -> Image.Image:
    """Renders a single frame of the Subscribe CTA card with alpha transparency."""
    card_w = 540 * scale
    card_h = 100 * scale
    canvas_w = card_w + 40 * scale
    canvas_h = card_h + 60 * scale

    in_dur = 0.5
    out_start = total_dur - 0.6
    out_dur = 0.6

    y_offset = 0.0
    alpha = 1.0

    if t < in_dur:
        p = t / in_dur
        e = 1.0 - (1.0 - p) ** 3
        y_offset = (1.0 - e) * 70 * scale
        alpha = min(1.0, max(0.0, p * 1.5))
    elif t > out_start:
        p = (t - out_start) / out_dur
        e = p ** 3
        y_offset = e * 70 * scale
        alpha = min(1.0, max(0.0, 1.0 - p))

    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    card_x = 20 * scale
    card_y = int(20 * scale + y_offset)

    bg_alpha = int(238 * alpha)
    border_alpha = int(80 * alpha)
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=22 * scale,
        fill=(15, 23, 42, bg_alpha),
        outline=(255, 255, 255, border_alpha),
        width=int(1.5 * scale),
    )

    f_title, f_sub, f_btn = _get_fonts(scale)

    # 1. Left Icon: YouTube Badge
    yt_w = 48 * scale
    yt_h = 34 * scale
    yt_x = card_x + 18 * scale
    yt_y = card_y + (card_h - yt_h) // 2
    _draw_youtube_icon(draw, yt_x, yt_y, yt_w, yt_h, scale=scale)

    # 2. Middle Text
    text_x = yt_x + yt_w + 16 * scale
    draw.text((text_x, card_y + 24 * scale), "¿TE GUSTA EL CÓMIC?", fill=(248, 250, 252, int(255 * alpha)), font=f_title)
    draw.text((text_x, card_y + 52 * scale), "Suscríbete y activa la campana", fill=(148, 163, 184, int(255 * alpha)), font=f_sub)

    # 3. Right Action Button
    btn_w = 150 * scale
    btn_h = 44 * scale
    btn_x = card_x + card_w - btn_w - 18 * scale
    btn_y = card_y + (card_h - btn_h) // 2

    is_clicked = t >= 2.5
    is_pressing = 2.4 <= t < 2.6

    press_shrink = int(2 * scale) if is_pressing else 0
    b_rect = [
        btn_x + press_shrink,
        btn_y + press_shrink,
        btn_x + btn_w - press_shrink,
        btn_y + btn_h - press_shrink,
    ]

    if not is_clicked:
        # Red Subscribe Button
        draw.rounded_rectangle(b_rect, radius=12 * scale, fill=(220, 38, 38, int(255 * alpha)))
        btn_text = "SUSCRIBIRSE"
        bbox = draw.textbbox((0, 0), btn_text, font=f_btn)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(
            (btn_x + (btn_w - tw) // 2, btn_y + (btn_h - th) // 2 - 2 * scale),
            btn_text,
            fill=(255, 255, 255, int(255 * alpha)),
            font=f_btn,
        )
    else:
        # Subscribed Gray Button + Vector Checkmark + Bell
        draw.rounded_rectangle(b_rect, radius=12 * scale, fill=(39, 39, 42, int(255 * alpha)), outline=(82, 82, 91, int(150 * alpha)), width=scale)
        btn_text = "SUSCRITO"
        bbox = draw.textbbox((0, 0), btn_text, font=f_btn)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        # Position checkmark + text + bell
        chk_cx = btn_x + 18 * scale
        chk_cy = btn_y + btn_h // 2
        _draw_checkmark(draw, chk_cx, chk_cy, size=14 * scale, color=(255, 255, 255, int(255 * alpha)), width=3 * scale)
        
        draw.text(
            (btn_x + 32 * scale, btn_y + (btn_h - th) // 2 - 2 * scale),
            btn_text,
            fill=(226, 232, 240, int(255 * alpha)),
            font=f_btn,
        )

        bell_t = t - 2.6
        ring = bell_t < 1.4
        bell_angle = 16.0 * math.sin(bell_t * 18.0) * math.exp(-bell_t * 2.0) if ring else 0.0
        bell_cx = btn_x + btn_w - 20 * scale
        bell_cy = btn_y + btn_h // 2
        _draw_bell_icon(draw, bell_cx, bell_cy, size=16 * scale, angle_deg=bell_angle, ring=ring, scale=scale)

    # 4. Pointer Cursor
    if 1.5 <= t <= 3.2:
        if t < 2.4:
            cp = (t - 1.5) / 0.9
            ce = 1.0 - (1.0 - cp) ** 2
            cur_x = int((btn_x + btn_w + 30 * scale) + (btn_x + btn_w // 2 - (btn_x + btn_w + 30 * scale)) * ce)
            cur_y = int((btn_y + 50 * scale) + (btn_y + btn_h // 2 - (btn_y + 50 * scale)) * ce)
        else:
            cur_x = btn_x + btn_w // 2
            cur_y = btn_y + btn_h // 2

        cur_alpha = max(0.0, 1.0 - (t - 2.8) / 0.4) if t > 2.8 else 1.0
        if cur_alpha > 0.05 and alpha > 0.1:
            _draw_cursor(draw, cur_x, cur_y, scale=scale)

    final_w = canvas_w // scale
    final_h = canvas_h // scale
    return img.resize((final_w, final_h), Image.Resampling.LANCZOS)


def render_like_frame(t: float, total_dur: float = 5.5, scale: int = 2) -> Image.Image:
    """Renders a single frame of the Like CTA card with alpha transparency."""
    card_w = 540 * scale
    card_h = 100 * scale
    canvas_w = card_w + 40 * scale
    canvas_h = card_h + 60 * scale

    in_dur = 0.5
    out_start = total_dur - 0.6
    out_dur = 0.6

    y_offset = 0.0
    alpha = 1.0

    if t < in_dur:
        p = t / in_dur
        e = 1.0 - (1.0 - p) ** 3
        y_offset = (1.0 - e) * 70 * scale
        alpha = min(1.0, max(0.0, p * 1.5))
    elif t > out_start:
        p = (t - out_start) / out_dur
        e = p ** 3
        y_offset = e * 70 * scale
        alpha = min(1.0, max(0.0, 1.0 - p))

    img = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    card_x = 20 * scale
    card_y = int(20 * scale + y_offset)

    bg_alpha = int(238 * alpha)
    border_alpha = int(80 * alpha)
    draw.rounded_rectangle(
        [card_x, card_y, card_x + card_w, card_y + card_h],
        radius=22 * scale,
        fill=(15, 23, 42, bg_alpha),
        outline=(255, 255, 255, border_alpha),
        width=int(1.5 * scale),
    )

    f_title, f_sub, f_btn = _get_fonts(scale)

    # 1. Left Icon: Glowing Thumbs Up Circle
    icon_r = 22 * scale
    icon_cx = card_x + 36 * scale
    icon_cy = card_y + card_h // 2
    is_liked = t >= 2.4
    circle_color = (37, 99, 235, int(255 * alpha)) if is_liked else (51, 65, 85, int(255 * alpha))
    draw.ellipse(
        [icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
        fill=circle_color,
    )
    _draw_thumbs_up(draw, icon_cx, icon_cy, size=20 * scale, color=(255, 255, 255, int(255 * alpha)), scale=scale)

    # 2. Middle Text
    text_x = card_x + 72 * scale
    if not is_liked:
        draw.text((text_x, card_y + 24 * scale), "¿DISFRUTAS LA HISTORIA?", fill=(248, 250, 252, int(255 * alpha)), font=f_title)
        draw.text((text_x, card_y + 52 * scale), "Deja tu Like para apoyar el video", fill=(148, 163, 184, int(255 * alpha)), font=f_sub)
    else:
        draw.text((text_x, card_y + 24 * scale), "¡GRACIAS POR TU APOYO!", fill=(96, 165, 250, int(255 * alpha)), font=f_title)
        draw.text((text_x, card_y + 52 * scale), "Tu Like ayuda a traer más historias", fill=(226, 232, 240, int(255 * alpha)), font=f_sub)

    # 3. Right Action Button
    btn_w = 140 * scale
    btn_h = 44 * scale
    btn_x = card_x + card_w - btn_w - 18 * scale
    btn_y = card_y + (card_h - btn_h) // 2

    is_pressing = 2.3 <= t < 2.5
    press_shrink = int(2 * scale) if is_pressing else 0
    b_rect = [
        btn_x + press_shrink,
        btn_y + press_shrink,
        btn_x + btn_w - press_shrink,
        btn_y + btn_h - press_shrink,
    ]

    if not is_liked:
        draw.rounded_rectangle(b_rect, radius=12 * scale, fill=(51, 65, 85, int(255 * alpha)), outline=(100, 116, 139, int(150 * alpha)), width=scale)
        btn_text = "DAR LIKE"
        bbox = draw.textbbox((0, 0), btn_text, font=f_btn)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        # Thumbs up icon inside button + text
        thumb_cx = btn_x + 22 * scale
        thumb_cy = btn_y + btn_h // 2
        _draw_thumbs_up(draw, thumb_cx, thumb_cy, size=15 * scale, color=(255, 255, 255, int(255 * alpha)), scale=scale)
        draw.text(
            (btn_x + 38 * scale, btn_y + (btn_h - th) // 2 - 2 * scale),
            btn_text,
            fill=(255, 255, 255, int(255 * alpha)),
            font=f_btn,
        )
    else:
        draw.rounded_rectangle(b_rect, radius=12 * scale, fill=(37, 99, 235, int(255 * alpha)))
        btn_text = "LIKED!"
        bbox = draw.textbbox((0, 0), btn_text, font=f_btn)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        
        chk_cx = btn_x + 24 * scale
        chk_cy = btn_y + btn_h // 2
        _draw_checkmark(draw, chk_cx, chk_cy, size=14 * scale, color=(255, 255, 255, int(255 * alpha)), width=3 * scale)
        draw.text(
            (btn_x + 42 * scale, btn_y + (btn_h - th) // 2 - 2 * scale),
            btn_text,
            fill=(255, 255, 255, int(255 * alpha)),
            font=f_btn,
        )

    # 4. Animated Cursor
    if 1.5 <= t <= 3.2:
        if t < 2.4:
            cp = (t - 1.5) / 0.9
            ce = 1.0 - (1.0 - cp) ** 2
            cur_x = int((btn_x + btn_w + 30 * scale) + (btn_x + btn_w // 2 - (btn_x + btn_w + 30 * scale)) * ce)
            cur_y = int((btn_y + 50 * scale) + (btn_y + btn_h // 2 - (btn_y + 50 * scale)) * ce)
        else:
            cur_x = btn_x + btn_w // 2
            cur_y = btn_y + btn_h // 2

        cur_alpha = max(0.0, 1.0 - (t - 2.8) / 0.4) if t > 2.8 else 1.0
        if cur_alpha > 0.05 and alpha > 0.1:
            _draw_cursor(draw, cur_x, cur_y, scale=scale)

    final_w = canvas_w // scale
    final_h = canvas_h // scale
    return img.resize((final_w, final_h), Image.Resampling.LANCZOS)


def generate_animated_cta_mov(cta_type: str, output_mov: str, duration: float = 5.5, fps: int = 30) -> str:
    """Renders all frames for the specified CTA type and encodes to transparent MOV (qtrle)."""
    out_path = Path(output_mov)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    temp_dir = out_path.parent / f"temp_{cta_type}_frames"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    total_frames = int(duration * fps)
    print(f"[CTA] Generando animación '{cta_type}' ({total_frames} fotogramas a {fps} fps)...")

    for f_idx in range(total_frames):
        t = f_idx / fps
        if cta_type == 'subscribe':
            frame = render_subscribe_frame(t, total_dur=duration)
        else:
            frame = render_like_frame(t, total_dur=duration)
        frame.save(temp_dir / f"frame_{f_idx:04d}.png")

    print(f"[CTA] Codificando a video transparente QuickTime Animation (qtrle)...")
    cmd = [
        'ffmpeg', '-y',
        '-framerate', str(fps),
        '-i', str(temp_dir / "frame_%04d.png"),
        '-c:v', 'qtrle',
        str(out_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    # Clean up frames
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"[CTA] ¡Animación lista! -> {out_path} ({out_path.stat().st_size // 1024} KB)")
    return str(out_path)
