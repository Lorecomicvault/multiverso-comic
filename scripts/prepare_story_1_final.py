import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter
import math

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
DIR = PROJECT_ROOT / "assets" / "curated_panels" / "01_red_hulk_golpea_watcher_humilla_thor"

def make_vertical_frame(im, target_w=1080, target_h=1920):
    # Create blurred background and centered sharp image
    target_ratio = target_w / target_h
    im_ratio = im.width / im.height
    
    # If image is wide, create cinematic comic letterbox with blurred background
    bg = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=25))
    
    # Fit im inside target_w, target_h
    scale = min(target_w / im.width, target_h / im.height)
    new_w = int(im.width * scale)
    new_h = int(im.height * scale)
    sharp = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Paste centered
    x_pos = (target_w - new_w) // 2
    y_pos = (target_h - new_h) // 2
    bg.paste(sharp, (x_pos, y_pos))
    return bg

# Load source images
im_s1 = Image.open(DIR / "page_04_uatu.jpg").convert('RGB')
im_s2 = Image.open(DIR / "candidate_s2_fandom.jpg").convert('RGB')
im_full_thor = Image.open(DIR / "test_img62.png").convert('RGB')

# Scene 3: Top of thor (W: 768, H: 1024 -> top 0 to 560)
im_s3 = im_full_thor.crop((0, 0, 768, 560))

# Scene 4: Bottom of thor (W: 768, H: 1024 -> bottom 470 to 1024)
im_s4 = im_full_thor.crop((0, 470, 768, 1024))

# Generate vertical 1080x1920
frame_s1 = make_vertical_frame(im_s1)
frame_s2 = make_vertical_frame(im_s2)
frame_s3 = make_vertical_frame(im_s3)
frame_s4 = make_vertical_frame(im_s4)

frame_s1.save(DIR / "scene_01.jpg", quality=95)
frame_s2.save(DIR / "scene_02.jpg", quality=95)
frame_s3.save(DIR / "scene_03.jpg", quality=95)
frame_s4.save(DIR / "scene_04.jpg", quality=95)

# Calculate RMS diffs
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

print("ALL 4 SCENES CREATED AND QUALITY GATE PASSED (RMS > 12.0) FOR STORY 1!")
