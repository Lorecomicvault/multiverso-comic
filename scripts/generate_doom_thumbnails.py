"""
GENERADOR DE THUMBNAILS DE ALTO CTR PARA YOUTUBE
================================================
- Formato: 1280x720 (16:9 Estándar de YouTube)
- 3 Variantes con gancho psicológico extremo y contraste visual máximo
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

BASE_DIR = r"C:\Users\Vanes\comics en espanol"
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "doctor_doom_doomsday_long")
THUMBNAILS_DIR = os.path.join(OUTPUT_DIR, "thumbnails")
PANELS_RAW = os.path.join(OUTPUT_DIR, "panels_raw")
ARTIFACT_DIR = r"C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb"

os.makedirs(THUMBNAILS_DIR, exist_ok=True)

# Buscar fuentes disponibles
FONT_IMPACT = r"C:\Windows\Fonts\impact.ttf"
if not os.path.exists(FONT_IMPACT):
    FONT_IMPACT = r"C:\Windows\Fonts\arialbd.ttf"

def draw_text_with_outline(draw, text, pos, font, fill_color, outline_color, outline_width=6):
    x, y = pos
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx*dx + dy*dy <= outline_width*outline_width:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    draw.text((x, y), text, font=font, fill=fill_color)

def generate_thumbnail_option1():
    # Opción 1: DOOM ARRANCANDO LA ESPINA DE THANOS
    # Archivo: panel_038_Doom_Rips_Thanos_Spine_Secret_Wars_8.jpg
    p38 = [f for f in os.listdir(PANELS_RAW) if "038" in f]
    if not p38:
        print("Panel 38 no encontrado para thumbnail 1")
        return
    src_path = os.path.join(PANELS_RAW, p38[0])
    
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        target_w, target_h = 1280, 720
        # Crop enfocado en el torso de Doom y el esqueleto de Thanos
        scale = max(target_w / im.width, target_h / im.height)
        w = int(im.width * scale)
        h = int(im.height * scale)
        im = im.resize((w, h), Image.Resampling.LANCZOS)
        left = (w - target_w) // 2
        top = max(0, (h - target_h) // 3)
        canvas = im.crop((left, top, left + target_w, top + target_h))
        
        # Aumentar contraste y saturación para impacto visual en YouTube
        enhancer = ImageEnhance.Contrast(canvas)
        canvas = enhancer.enhance(1.25)
        enhancer = ImageEnhance.Color(canvas)
        canvas = enhancer.enhance(1.20)
        
        # Añadir viñeteado oscuro en bordes para destacar texto
        draw = ImageDraw.Draw(canvas)
        # Barra lateral izquierda oscura con gradiente simulado
        overlay = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
        ov_draw = ImageDraw.Draw(overlay)
        for i in range(500):
            alpha = int(220 * (1 - i / 500))
            ov_draw.line([(i, 0), (i, target_h)], fill=(0, 0, 0, alpha))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        draw = ImageDraw.Draw(canvas)
        
        # Tipografía Viral
        font_large = ImageFont.truetype(FONT_IMPACT, 72)
        font_sub = ImageFont.truetype(FONT_IMPACT, 52)
        font_badge = ImageFont.truetype(FONT_IMPACT, 32)
        
        # Badge Superior
        draw.rectangle([(50, 40), (280, 95)], fill=(220, 20, 60))
        draw.text((65, 45), "CANÓNICO", font=font_badge, fill=(255, 255, 255))
        
        draw_text_with_outline(draw, "¡HUMILLÓ A", (50, 120), font_large, (255, 255, 255), (0, 0, 0), 7)
        draw_text_with_outline(draw, "THANOS!", (50, 200), font_large, (255, 215, 0), (0, 0, 0), 8)
        draw_text_with_outline(draw, "LE ARRANCÓ LA ESPINA", (50, 300), font_sub, (255, 50, 50), (0, 0, 0), 6)
        
        out_path = os.path.join(THUMBNAILS_DIR, "thumbnail_opcion1_humillo_a_thanos.jpg")
        canvas.save(out_path, "JPEG", quality=95)
        shutil.copy2(out_path, os.path.join(ARTIFACT_DIR, "thumbnail_opcion1_humillo_a_thanos.jpg"))
        print("Thumbnail Opción 1 generada exitosamente!")

def generate_thumbnail_option2():
    # Opción 2: LA MÁSCARA AL ROJO VIVO (ORIGEN OSCURO)
    p23 = r"C:\Users\Vanes\comics en espanol\scratch\ff_ann_2_monks.jpg"
    if not os.path.exists(p23):
        return
    with Image.open(p23) as im:
        im = im.convert("RGB")
        target_w, target_h = 1280, 720
        scale = max(target_w / im.width, target_h / im.height)
        w = int(im.width * scale)
        h = int(im.height * scale)
        im = im.resize((w, h), Image.Resampling.LANCZOS)
        left = (w - target_w) // 2
        top = (h - target_h) // 2
        canvas = im.crop((left, top, left + target_w, top + target_h))
        
        enhancer = ImageEnhance.Contrast(canvas)
        canvas = enhancer.enhance(1.30)
        
        draw = ImageDraw.Draw(canvas)
        font_large = ImageFont.truetype(FONT_IMPACT, 75)
        font_sub = ImageFont.truetype(FONT_IMPACT, 48)
        font_badge = ImageFont.truetype(FONT_IMPACT, 32)
        
        draw.rectangle([(50, 40), (320, 95)], fill=(0, 128, 0))
        draw.text((65, 45), "ORIGEN REAL", font=font_badge, fill=(255, 255, 255))
        
        draw_text_with_outline(draw, "HIERRO AL", (50, 120), font_large, (255, 255, 255), (0, 0, 0), 7)
        draw_text_with_outline(draw, "ROJO VIVO", (50, 205), font_large, (255, 69, 0), (0, 0, 0), 8)
        draw_text_with_outline(draw, "EL SECRETO DE SU MÁSCARA", (50, 310), font_sub, (255, 215, 0), (0, 0, 0), 6)
        
        out_path = os.path.join(THUMBNAILS_DIR, "thumbnail_opcion2_mascara_rojo_vivo.jpg")
        canvas.save(out_path, "JPEG", quality=95)
        shutil.copy2(out_path, os.path.join(ARTIFACT_DIR, "thumbnail_opcion2_mascara_rojo_vivo.jpg"))
        print("Thumbnail Opción 2 generada exitosamente!")

def generate_thumbnail_option3():
    # Opción 3: DIOS EMPERADOR DOOM EN EL TRONO
    p35 = [f for f in os.listdir(PANELS_RAW) if "035" in f]
    if not p35:
        return
    src_path = os.path.join(PANELS_RAW, p35[0])
    with Image.open(src_path) as im:
        im = im.convert("RGB")
        target_w, target_h = 1280, 720
        scale = max(target_w / im.width, target_h / im.height)
        w = int(im.width * scale)
        h = int(im.height * scale)
        im = im.resize((w, h), Image.Resampling.LANCZOS)
        left = (w - target_w) // 2
        top = (h - target_h) // 4
        canvas = im.crop((left, top, left + target_w, top + target_h))
        
        enhancer = ImageEnhance.Contrast(canvas)
        canvas = enhancer.enhance(1.20)
        
        draw = ImageDraw.Draw(canvas)
        font_large = ImageFont.truetype(FONT_IMPACT, 72)
        font_sub = ImageFont.truetype(FONT_IMPACT, 48)
        font_badge = ImageFont.truetype(FONT_IMPACT, 32)
        
        draw.rectangle([(50, 40), (380, 95)], fill=(128, 0, 128))
        draw.text((65, 45), "AVENGERS: DOOMSDAY", font=font_badge, fill=(255, 255, 255))
        
        draw_text_with_outline(draw, "MÁS PODEROSO", (50, 120), font_large, (255, 255, 255), (0, 0, 0), 7)
        draw_text_with_outline(draw, "QUE DIOS", (50, 200), font_large, (0, 255, 255), (0, 0, 0), 8)
        draw_text_with_outline(draw, "TODO LO QUE DEBES SABER", (50, 305), font_sub, (255, 215, 0), (0, 0, 0), 6)
        
        out_path = os.path.join(THUMBNAILS_DIR, "thumbnail_opcion3_dios_emperador.jpg")
        canvas.save(out_path, "JPEG", quality=95)
        shutil.copy2(out_path, os.path.join(ARTIFACT_DIR, "thumbnail_opcion3_dios_emperador.jpg"))
        print("Thumbnail Opción 3 generada exitosamente!")

if __name__ == "__main__":
    generate_thumbnail_option1()
    generate_thumbnail_option2()
    generate_thumbnail_option3()
