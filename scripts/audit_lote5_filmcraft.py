import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, default=41)
parser.add_argument("--end", type=int, default=60)
args = parser.parse_args()

q = Path("scheduled_queue")
slots = sorted(
    [
        d
        for d in q.iterdir()
        if d.is_dir()
        and "_fc_" in d.name
        and d.name[:3].isdigit()
        and args.start <= int(d.name[:3]) <= args.end
        and (d / "video.mp4").exists()
        and (d / "metadata.json").exists()
    ]
)
print(f"Encontrados {len(slots)} slots FilmCraft Lote 5 ({args.start}-{args.end}):")
if not slots:
    raise SystemExit(0)

cols = 5
rows = max(1, (len(slots) + cols - 1) // cols)
tw, th = 220, 390
sheet_f0 = Image.new("RGB", (cols * tw, rows * th), (15, 15, 15))
sheet_mid = Image.new("RGB", (cols * tw, rows * th), (15, 15, 15))
d0, dmid = ImageDraw.Draw(sheet_f0), ImageDraw.Draw(sheet_mid)

for idx, s in enumerate(slots):
    v = s / "video.mp4"
    probe = json.loads(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(v)],
            text=True,
        )
    )
    streams = probe["streams"]
    v_st = next(x for x in streams if x["codec_type"] == "video")
    a_st = next(x for x in streams if x["codec_type"] == "audio")
    dur = float(probe["format"]["duration"])
    sz = v.stat().st_size / (1024 * 1024)
    print(
        f"  {s.name:<48} | {v_st['width']}x{v_st['height']} {v_st['r_frame_rate']}fps | "
        f"{a_st['codec_name']} {a_st['sample_rate']}Hz | {dur:.2f}s | {sz:.1f}MB"
    )

    f0_tmp = Path("output") / f"_audit5_{idx}_f0.jpg"
    fm_tmp = Path("output") / f"_audit5_{idx}_mid.jpg"
    subprocess.run(
        ["ffmpeg", "-y", "-ss", "0.0", "-i", str(v), "-frames:v", "1", str(f0_tmp)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-ss", f"{dur*0.55:.1f}", "-i", str(v), "-frames:v", "1", str(fm_tmp)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    im0 = Image.open(f0_tmp).resize((tw - 6, th - 24))
    imm = Image.open(fm_tmp).resize((tw - 6, th - 24))
    x, y = (idx % cols) * tw + 3, (idx // cols) * th + 20
    sheet_f0.paste(im0, (x, y))
    d0.text((x + 4, y - 18), f"{s.name[:24]}", fill=(255, 255, 0))
    sheet_mid.paste(imm, (x, y))
    dmid.text((x + 4, y - 18), f"{s.name[:24]}", fill=(0, 255, 255))

tag = f"{args.start}_{args.end}"
sheet_f0.save(f"output/audit_lote5_{tag}_frame0.jpg", quality=88)
sheet_mid.save(f"output/audit_lote5_{tag}_mid.jpg", quality=88)
print(f"Saved output/audit_lote5_{tag}_frame0.jpg & output/audit_lote5_{tag}_mid.jpg")
