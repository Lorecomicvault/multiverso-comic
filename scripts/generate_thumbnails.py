import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

DOWNLOADS_DIR = r"C:\Users\Vanes\Downloads\video\Comics"
GEN_IMAGE_PATH = r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb\knightfall_yt_thumb_1791072959586.jpg"
APARO_PANEL_PATH = r"C:\Users\Vanes\comics en espanol\assets\curated_panels\batman_knightfall_long\Bane_0020.jpg"
FONT_PATH = r"C:\Users\Vanes\comics en espanol\fonts\impact.ttf"

def draw_text_with_stroke_and_shadow(
    draw, text, font, pos, fill_color, stroke_color=(0, 0, 0), stroke_width=6, shadow_offset=(6, 6), shadow_color=(0, 0, 0, 220)
):
    x, y = pos
    # Draw drop shadow
    sx, sy = x + shadow_offset[0], y + shadow_offset[1]
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            draw.text((sx + dx, sy + dy), text, font=font, fill=shadow_color)
            
    # Draw stroke
    for dx in range(-stroke_width, stroke_width + 1):
        for dy in range(-stroke_width, stroke_width + 1):
            if dx != 0 or dy != 0:
                draw.text((x + dx, y + dy), text, font=font, fill=stroke_color)
                
    # Draw fill
    draw.text((x, y), text, font=font, fill=fill_color)

def generate_cinematic_thumbnail_clean():
    """Generates 1920x1080 pristine high-res art without text."""
    im = Image.open(GEN_IMAGE_PATH).convert("RGB")
    im_1080 = im.resize((1920, 1080), Image.Resampling.LANCZOS)
    
    # Slight contrast and color punch enhancement for YouTube mobile display
    enh_color = ImageEnhance.Color(im_1080)
    im_1080 = enh_color.enhance(1.08)
    enh_contrast = ImageEnhance.Contrast(im_1080)
    im_1080 = enh_contrast.enhance(1.05)
    
    out_path = os.path.join(DOWNLOADS_DIR, "Batman_Knightfall_Miniatura_Opcion1_Arte_Limpio.jpg")
    im_1080.save(out_path, quality=98)
    print(f"Generated clean art thumbnail: {out_path}")
    return out_path

def generate_cinematic_thumbnail_with_hook():
    """Generates 1920x1080 YouTube high-CTR thumbnail with bold text hook."""
    im = Image.open(GEN_IMAGE_PATH).convert("RGB")
    im_1080 = im.resize((1920, 1080), Image.Resampling.LANCZOS)
    
    # Slight contrast and saturation boost
    im_1080 = ImageEnhance.Color(im_1080).enhance(1.10)
    im_1080 = ImageEnhance.Contrast(im_1080).enhance(1.06)
    
    # Create an overlay for subtle dark gradient on the left behind text
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # Radial/linear gradient on top-left to make text pop against background
    for x in range(0, 850):
        alpha = int(140 * (1.0 - (x / 850.0) ** 1.3))
        ov_draw.line([(x, 0), (x, 700)], fill=(0, 0, 0, alpha))
        
    im_1080 = Image.alpha_composite(im_1080.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im_1080)
    
    # Load fonts
    font_badge = ImageFont.truetype(FONT_PATH, 42)
    font_l1 = ImageFont.truetype(FONT_PATH, 92)
    font_l2 = ImageFont.truetype(FONT_PATH, 130)
    font_l3 = ImageFont.truetype(FONT_PATH, 110)
    
    # 1. Badge: "HISTORIA COMPLETA"
    badge_x, badge_y = 70, 75
    badge_text = " HISTORIA COMPLETA "
    bbox = draw.textbbox((badge_x, badge_y), badge_text, font=font_badge)
    pad = 12
    draw.rounded_rectangle(
        [bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad],
        radius=10,
        fill=(225, 15, 15),
        outline=(255, 255, 255),
        width=3
    )
    draw.text((badge_x, badge_y), badge_text, font=font_badge, fill=(255, 255, 255))
    
    # 2. Main title hook:
    # EL DÍA QUE
    # BATMAN
    # FUE DESTRUIDO
    draw_text_with_stroke_and_shadow(
        draw, "EL DÍA QUE", font_l1, (70, 160), fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=8
    )
    draw_text_with_stroke_and_shadow(
        draw, "BATMAN", font_l2, (66, 260), fill_color=(255, 230, 0), stroke_color=(0, 0, 0), stroke_width=10
    )
    draw_text_with_stroke_and_shadow(
        draw, "FUE DESTRUIDO", font_l3, (70, 400), fill_color=(255, 50, 50), stroke_color=(0, 0, 0), stroke_width=9
    )
    
    # Small accent tag below
    font_sub = ImageFont.truetype(FONT_PATH, 38)
    draw_text_with_stroke_and_shadow(
        draw, "KNIGHTFALL / LA CAÍDA", font_sub, (72, 530), fill_color=(0, 240, 255), stroke_color=(0, 0, 0), stroke_width=5
    )
    
    out_path = os.path.join(DOWNLOADS_DIR, "Batman_Knightfall_Miniatura_Opcion2_YouTube_Hook.jpg")
    im_1080.save(out_path, quality=98)
    print(f"Generated Hook thumbnail: {out_path}")
    return out_path

def generate_comic_classic_thumbnail():
    """Generates 1920x1080 thumbnail using the iconic Jim Aparo comic panel."""
    aparo = Image.open(APARO_PANEL_PATH).convert("RGB")
    
    # Create 1920x1080 canvas
    canvas = Image.new("RGB", (1920, 1080), (10, 10, 15))
    
    # Blurred background fill from the panel itself
    bg = aparo.copy().resize((1920, 1080), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=28))
    bg = ImageEnhance.Brightness(bg).enhance(0.40)
    canvas.paste(bg, (0, 0))
    
    # Resize aparo panel to fit height nicely (1080 or slightly framed)
    aparo_h = 1040
    aparo_w = int(aparo.width * (aparo_h / aparo.height))
    aparo_fitted = aparo.resize((aparo_w, aparo_h), Image.Resampling.LANCZOS)
    
    # Place on the right side
    pos_x = 1920 - aparo_w - 40
    pos_y = (1080 - aparo_h) // 2
    
    # Add comic border and shadow to the panel
    panel_frame = Image.new("RGBA", (aparo_w + 24, aparo_h + 24), (255, 255, 255, 255))
    canvas.paste(panel_frame, (pos_x - 12, pos_y - 12))
    canvas.paste(aparo_fitted, (pos_x, pos_y))
    
    # Typography on the left side
    draw = ImageDraw.Draw(canvas)
    
    font_badge = ImageFont.truetype(FONT_PATH, 42)
    font_t1 = ImageFont.truetype(FONT_PATH, 115)
    font_t2 = ImageFont.truetype(FONT_PATH, 130)
    font_t3 = ImageFont.truetype(FONT_PATH, 90)
    
    # Badge: DC COMICS CLÁSICO
    badge_x, badge_y = 70, 120
    badge_text = " DC COMICS CLÁSICO "
    bbox = draw.textbbox((badge_x, badge_y), badge_text, font=font_badge)
    pad = 12
    draw.rounded_rectangle(
        [bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad],
        radius=10,
        fill=(0, 110, 240),
        outline=(255, 255, 255),
        width=3
    )
    draw.text((badge_x, badge_y), badge_text, font=font_badge, fill=(255, 255, 255))
    
    # Text Hook:
    # KNIGHTFALL
    # ¡EL QUIEBRE!
    # BANE VS BATMAN
    draw_text_with_stroke_and_shadow(
        draw, "KNIGHTFALL", font_t1, (70, 230), fill_color=(255, 230, 0), stroke_color=(0, 0, 0), stroke_width=9
    )
    draw_text_with_stroke_and_shadow(
        draw, "¡EL QUIEBRE!", font_t2, (66, 370), fill_color=(255, 30, 30), stroke_color=(0, 0, 0), stroke_width=10
    )
    draw_text_with_stroke_and_shadow(
        draw, "BANE VS BATMAN", font_t3, (72, 530), fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_width=7
    )
    
    out_path = os.path.join(DOWNLOADS_DIR, "Batman_Knightfall_Miniatura_Opcion3_Comic_Clasico.jpg")
    canvas.save(out_path, quality=98)
    print(f"Generated Classic Comic thumbnail: {out_path}")
    return out_path

if __name__ == "__main__":
    generate_cinematic_thumbnail_clean()
    generate_cinematic_thumbnail_with_hook()
    generate_comic_classic_thumbnail()
