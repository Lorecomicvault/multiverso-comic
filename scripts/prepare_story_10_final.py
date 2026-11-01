import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter
import math

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
DIR = PROJECT_ROOT / "assets" / "curated_panels" / "10_flash_barry_allen_se_convierte_en_rayo_crisis"

def make_vertical_frame(im, target_w=1080, target_h=1920):
    bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=25))
    
    scale = min(target_w / im.width, target_h / im.height)
    new_w = int(im.width * scale)
    new_h = int(im.height * scale)
    sharp = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    x_pos = (target_w - new_w) // 2
    y_pos = (target_h - new_h) // 2
    bg.paste(sharp, (x_pos, y_pos))
    return bg

full = Image.open(DIR / "flash_0050.jpg").convert('RGB')
w, h = full.size
mid_x = w // 2
mid_y = h // 2

# Quadrant 1: Top-Left (Page 237)
im_s1 = full.crop((0, 0, mid_x, mid_y))

# Quadrant 2: Top-Right (Page 238)
im_s2 = full.crop((mid_x, 0, w, mid_y))

# Quadrant 3: Bottom-Left (Page 239)
im_s3 = full.crop((0, mid_y, mid_x, h))

# Quadrant 4: Bottom-Right (Page 240)
im_s4 = full.crop((mid_x, mid_y, w, h))

frame_s1 = make_vertical_frame(im_s1)
frame_s2 = make_vertical_frame(im_s2)
frame_s3 = make_vertical_frame(im_s3)
frame_s4 = make_vertical_frame(im_s4)

frame_s1.save(DIR / "scene_01.jpg", quality=95)
frame_s2.save(DIR / "scene_02.jpg", quality=95)
frame_s3.save(DIR / "scene_03.jpg", quality=95)
frame_s4.save(DIR / "scene_04.jpg", quality=95)

frames = [frame_s1, frame_s2, frame_s3, frame_s4]
for i in range(len(frames)):
    for j in range(i + 1, len(frames)):
        diff = ImageChops.difference(frames[i], frames[j])
        h_hist = diff.histogram()
        sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h_hist))
        sum_sq = sum(sq)
        rms = math.sqrt(sum_sq / float(1080 * 1920 * 3))
        print(f"RMS diff S{i+1} vs S{j+1}: {rms:.2f}")
        assert rms > 12.0, f"RMS too low between S{i+1} and S{j+1}!"

print("ALL 4 SCENES CREATED AND QUALITY GATE PASSED FOR STORY 10!")
