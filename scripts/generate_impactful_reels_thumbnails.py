import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

sys.stdout.reconfigure(encoding='utf-8')

FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
if not Path(FONT_IMPACT).exists():
    FONT_IMPACT = r"C:\Users\Vanes\comics en espanol\fonts\impact.ttf"

def apply_cinematic_grade(im: Image.Image) -> Image.Image:
    im = ImageEnhance.Contrast(im).enhance(1.22)
    im = ImageEnhance.Color(im).enhance(1.20)
    im = ImageEnhance.Sharpness(im).enhance(1.15)
    return im

def fit_to_vertical(im: Image.Image, target_w=1080, target_h=1920) -> Image.Image:
    """Intelligently fits or fills the image into 1080x1920 vertical canvas with blurred backdrop if needed."""
    w, h = im.size
    aspect = w / h
    target_aspect = target_w / target_h

    # If already exact vertical
    if w == target_w and h == target_h:
        return im.copy()

    # If it's a wide double spread or landscape
    if aspect > 1.1:
        # Create blurred ambient background
        bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        bg = bg.filter(ImageFilter.GaussianBlur(35))
        bg = ImageEnhance.Brightness(bg).enhance(0.40)

        # Scale main art to fill width
        new_w = target_w
        new_h = int(target_w / aspect)
        fg = im.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Center in vertical canvas
        pos_y = (target_h - new_h) // 2
        bg.paste(fg, (0, pos_y))
        return bg
    else:
        # Portrait: crop or fit
        scale = max(target_w / w, target_h / h)
        nw, nh = int(w * scale), int(h * scale)
        scaled = im.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - target_w) // 2
        top = (nh - target_h) // 2
        return scaled.crop((left, top, left + target_w, top + target_h))

def draw_pill_badge(canvas: Image.Image, text: str, center_x: int, y: int, font: ImageFont.FreeTypeFont,
                    bg_color=(15, 15, 15, 220), border_color=(255, 230, 0, 255), border_width=3,
                    text_color=(255, 255, 255), pad_x=28, pad_y=10, radius=18) -> Image.Image:
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    x1 = center_x - tw // 2 - pad_x
    x2 = center_x + tw // 2 + pad_x
    y1 = y
    y2 = y + th + pad_y * 2

    # Shadow
    d.rounded_rectangle([x1 + 3, y1 + 4, x2 + 3, y2 + 4], radius=radius, fill=(0, 0, 0, 180))
    # Box & Border
    d.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg_color, outline=border_color, width=border_width)
    # Text
    tx = center_x - tw // 2 - bbox[0]
    ty = y + pad_y - bbox[1]
    d.text((tx, ty), text, font=font, fill=text_color)

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

def draw_curved_drop_shadow(d_shadow: ImageDraw.ImageDraw, pos, text, font, offset=(0, 6), blur=12, alpha=230):
    x, y = pos
    ox, oy = offset
    d_shadow.text((x + ox, y + oy), text, font=font, fill=(0, 0, 0, alpha), stroke_width=12, stroke_fill=(0, 0, 0, alpha))

def draw_impact_text(canvas: Image.Image, lines: list[dict], center_x=540, start_y=520, line_spacing=18) -> Image.Image:
    """
    Renders multi-line high CTR text with heavy stroke, Gaussian blur drop-shadow,
    and centered alignment.
    Each item in lines: {'text': str, 'size': int, 'color': (R, G, B), 'stroke_color': (R,G,B), 'stroke_w': int}
    """
    canvas_rgba = canvas.convert("RGBA")
    w, h = canvas.size

    # 1. Measure and compute coordinates
    line_layouts = []
    curr_y = start_y

    for item in lines:
        font = ImageFont.truetype(FONT_IMPACT, item.get('size', 96))
        txt = item['text']
        bbox = font.getbbox(txt)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = center_x - tw // 2 - bbox[0]
        line_layouts.append({
            'text': txt,
            'font': font,
            'pos': (x, curr_y),
            'color': item.get('color', (255, 235, 0)),
            'stroke_color': item.get('stroke_color', (0, 0, 0)),
            'stroke_w': item.get('stroke_w', 9),
            'shadow_blur': item.get('shadow_blur', 12),
            'shadow_offset': item.get('shadow_offset', (0, 7)),
        })
        curr_y += th + line_spacing

    # 2. Render blurred shadow layer
    shadow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)

    for layout in line_layouts:
        x, y = layout['pos']
        ox, oy = layout['shadow_offset']
        s_draw.text((x + ox, y + oy), layout['text'], font=layout['font'],
                    fill=(0, 0, 0, 230),
                    stroke_width=layout['stroke_w'] + 6,
                    stroke_fill=(0, 0, 0, 230))

    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(10))
    canvas_rgba = Image.alpha_composite(canvas_rgba, shadow_layer)

    # 3. Render crisp text with thick stroke
    text_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)

    for layout in line_layouts:
        x, y = layout['pos']
        t_draw.text((x, y), layout['text'], font=layout['font'],
                    fill=layout['color'],
                    stroke_width=layout['stroke_w'],
                    stroke_fill=layout['stroke_color'])

    final_im = Image.alpha_composite(canvas_rgba, text_layer)
    return final_im.convert("RGB")

def apply_text_vignette(canvas: Image.Image, top_y=380, bottom_y=860, max_alpha=190) -> Image.Image:
    """Applies a soft horizontal dark band gradient behind text to guarantee 100% readability."""
    w, h = canvas.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)

    mid_y = (top_y + bottom_y) // 2
    height_range = (bottom_y - top_y) / 2.0

    for y in range(top_y, bottom_y):
        dist = abs(y - mid_y) / height_range
        alpha = int(max_alpha * (1.0 - (dist ** 2)))
        alpha = max(0, min(255, alpha))
        if alpha > 0:
            ov_draw.line([(0, y), (w, y)], fill=(0, 0, 0, alpha))

    return Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")


SLOTS_DATA = [
    {
        "slot_id": 49,
        "folder": "49_green_arrow_cry_for_justice_prometheus",
        "source_art": r"assets/curated_panels/49_green_arrow_cry_for_justice_prometheus/scene_04.jpg",
        "badge": "DC COMICS • CANÓNICO",
        "badge_border": (255, 230, 0, 255),
        "text_start_y": 480,
        "vignette": (410, 850),
        "lines": [
            {"text": "¡CRUZÓ LA LÍNEA!", "size": 105, "color": (255, 235, 0), "stroke_w": 10},
            {"text": "ASESINÓ A PROMETHEUS", "size": 86, "color": (255, 255, 255), "stroke_w": 9},
            {"text": "JUSTICIA POR STAR CITY", "size": 64, "color": (0, 230, 255), "stroke_w": 8},
        ]
    },
    {
        "slot_id": 50,
        "folder": "50_planet_hulk_muerte_caiera",
        "source_art": r"assets/curated_panels/50_planet_hulk_muerte_caiera/scene_04.jpg",
        "badge": "MARVEL COMICS • CANÓNICO",
        "badge_border": (255, 30, 40, 255),
        "text_start_y": 460,
        "vignette": (390, 840),
        "lines": [
            {"text": "¡LA MUERTE DE CAIERA!", "size": 96, "color": (255, 35, 45), "stroke_w": 10},
            {"text": "NACE EL WORLDBREAKER", "size": 86, "color": (255, 235, 0), "stroke_w": 9},
            {"text": "LA FURIA CIEGA DE HULK", "size": 64, "color": (255, 255, 255), "stroke_w": 8},
        ]
    },
    {
        "slot_id": 51,
        "folder": "51_spiderman_escorpion_mandibula_superior",
        "source_art": r"assets/curated_panels/51_spiderman_escorpion_mandibula_superior/scene_03.jpg",
        "badge": "MARVEL COMICS • CANÓNICO",
        "badge_border": (255, 230, 0, 255),
        "text_start_y": 480,
        "vignette": (410, 850),
        "lines": [
            {"text": "¡LE ARRANCÓ LA MANDÍBULA!", "size": 94, "color": (255, 235, 0), "stroke_w": 10},
            {"text": "DE UN SOLO GOLPE", "size": 90, "color": (255, 255, 255), "stroke_w": 9},
            {"text": "EL PODER OCULTO DE SPIDER-MAN", "size": 60, "color": (0, 230, 255), "stroke_w": 8},
        ]
    },
    {
        "slot_id": 52,
        "folder": "52_batman_virus_doomsday_devastator",
        "source_art": r"C:/Users/Vanes/.gemini/antigravity/brain/40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb/devastator_test_11.jpg",
        "badge": "DC COMICS • MULTIVERSO OSCURO",
        "badge_border": (255, 30, 40, 255),
        "text_start_y": 460,
        "vignette": (390, 840),
        "lines": [
            {"text": "¡SE INYECTÓ EL VIRUS!", "size": 98, "color": (255, 235, 0), "stroke_w": 10},
            {"text": "BATMAN DOOMSDAY", "size": 94, "color": (255, 35, 45), "stroke_w": 9},
            {"text": "PARA DESTRUIR A SUPERMAN", "size": 64, "color": (255, 255, 255), "stroke_w": 8},
        ]
    },
    {
        "slot_id": 53,
        "folder": "53_spiderman_back_in_black_kingpin",
        "source_art": r"C:/Users/Vanes/.gemini/antigravity/brain/40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb/asm_test_15.jpg",
        "badge": "MARVEL COMICS • CANÓNICO",
        "badge_border": (255, 230, 0, 255),
        "text_start_y": 460,
        "vignette": (390, 840),
        "lines": [
            {"text": "¡HUMILLÓ A KINGPIN!", "size": 102, "color": (255, 235, 0), "stroke_w": 10},
            {"text": "SIN MÁSCARA EN PRISIÓN", "size": 84, "color": (255, 255, 255), "stroke_w": 9},
            {"text": "SPIDER-MAN SIN PIEDAD", "size": 66, "color": (255, 35, 45), "stroke_w": 8},
        ]
    },
    {
        "slot_id": 54,
        "folder": "54_sentry_descuartiza_ares_siege",
        "source_art": r"C:/Users/Vanes/.gemini/antigravity/brain/40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb/siege_015_spread.jpg",
        "badge": "MARVEL COMICS • SIEGE #2",
        "badge_border": (255, 30, 40, 255),
        "text_start_y": 460,
        "vignette": (390, 840),
        "lines": [
            {"text": "¡DESCUARTIZÓ A UN DIOS!", "size": 96, "color": (255, 35, 45), "stroke_w": 10},
            {"text": "EN DOS MITADES", "size": 92, "color": (255, 235, 0), "stroke_w": 9},
            {"text": "SENTRY DESTROZA A ARES", "size": 66, "color": (255, 255, 255), "stroke_w": 8},
        ]
    },
    {
        "slot_id": 55,
        "folder": "55_batman_que_rie_dark_multiverse",
        "source_art": r"C:/Users/Vanes/.gemini/antigravity/brain/40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb/bwl_test_p013.jpg",
        "badge": "DC COMICS • MULTIVERSO OSCURO",
        "badge_border": (0, 255, 120, 255),
        "text_start_y": 460,
        "vignette": (390, 840),
        "lines": [
            {"text": "¡MASACRÓ A SU FAMILIA!", "size": 96, "color": (255, 35, 45), "stroke_w": 10},
            {"text": "NACE EL BATMAN QUE RÍE", "size": 84, "color": (0, 255, 120), "stroke_w": 9},
            {"text": "LA TOXINA PURIFICADA DEL JOKER", "size": 60, "color": (255, 255, 255), "stroke_w": 8},
        ]
    },
]

def generate_all_thumbnails():
    queue_root = Path("scheduled_queue")
    brain_dir = Path(r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb")
    font_badge = ImageFont.truetype(FONT_IMPACT, 38)

    print("=== GENERANDO MINIATURAS IMPACTANTES 1080x1920 (HIGH CTR) ===")
    for item in SLOTS_DATA:
        sid = item["slot_id"]
        folder_name = item["folder"]
        slot_dir = queue_root / folder_name
        dest_thumb = slot_dir / "thumb.jpg"
        brain_thumb = brain_dir / f"high_impact_thumb_slot_{sid}.jpg"

        print(f"\nProcesando Slot {sid}: {folder_name}...")
        raw_art = Image.open(item["source_art"]).convert("RGB")
        graded = apply_cinematic_grade(raw_art)
        canvas = fit_to_vertical(graded, target_w=1080, target_h=1920)

        # 1. Vignette behind text
        top_v, bot_v = item["vignette"]
        canvas = apply_text_vignette(canvas, top_y=top_v, bottom_y=bot_v, max_alpha=190)

        # 2. Badge
        badge_y = item["text_start_y"] - 75
        canvas = draw_pill_badge(canvas, item["badge"], center_x=540, y=badge_y,
                                 font=font_badge, border_color=item["badge_border"],
                                 border_width=3)

        # 3. Text lines
        canvas = draw_impact_text(canvas, item["lines"], center_x=540, start_y=item["text_start_y"], line_spacing=16)

        # Save to scheduled_queue and brain
        dest_thumb.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(dest_thumb, quality=98)
        canvas.save(brain_thumb, quality=98)
        print(f"  OK -> Miniatura guardada en {dest_thumb} ({dest_thumb.stat().st_size / 1024:.1f} KB)")
        print(f"  OK -> Copia en brain: {brain_thumb.name}")

if __name__ == "__main__":
    generate_all_thumbnails()
