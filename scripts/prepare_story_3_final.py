import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter
import math

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
DIR = PROJECT_ROOT / "assets" / "curated_panels" / "03_hal_jordan_masacre_green_lantern_corps_parallax"

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

im_s1 = Image.open(DIR / "raw_s1.jpg").convert('RGB')
im_s2 = Image.open(DIR / "raw_s2.jpg").convert('RGB')

# Scene 3: Crop left panel of emeraldtwilightfinale.png (Hal snapping Sinestro's neck)
im_finale = Image.open(DIR / "emeraldtwilightfinale.png").convert('RGB')
# W is around 1024 or full, let's get left 28% of width
w, h = im_finale.size
im_s3 = im_finale.crop((0, 0, int(w * 0.28), h))

im_s4 = Image.open(DIR / "raw_s4.jpg").convert('RGB')

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
        h = diff.histogram()
        sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
        sum_sq = sum(sq)
        rms = math.sqrt(sum_sq / float(1080 * 1920 * 3))
        print(f"RMS diff S{i+1} vs S{j+1}: {rms:.2f}")
        assert rms > 12.0, f"RMS too low between S{i+1} and S{j+1}!"

print("ALL 4 SCENES CREATED AND QUALITY GATE PASSED FOR STORY 3!")
