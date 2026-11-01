import sys
import requests
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGe89bV5lm9XPFfEV1GO__Bv_gXf9BrS3h5gfyisurobNpEzAqcJwuf0Ks8MhN9OoT4vxY38BVmK2-HH-wmBXfRIzz2ZdCzpKwcWfZZ0Ddhywy8gKP3uFRH4UZmhq_K392TV_t0FqU4f4WgWN2cFuj7TqYYD-ZWqmjvEKl7GigsMrfrpfo=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHRYfjFTNHvbXd1CYwkF2mnHIyOZKeeW2LYZWfFsJnoVqoLWTMn7s4z1RHWraifLHYDXnvPY-FhdTVTm6WWCvtZJ8AkxKf94XZhngi7N9o0d8v9GYjzygq2ekvKcVzYui1kx5hom13LW81W6DD2dUGcTRjnQpb13arR5LGSJQCJ"
]

for u in urls:
    try:
        r = requests.get(u, allow_redirects=False, timeout=10)
        target = r.headers.get('Location', '')
        print("Target:", target)
        if target:
            r2 = requests.get(target, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}, timeout=15)
            imgs = re.findall(r'https://[^"\']+\.(?:jpg|png|webp|jpeg)', r2.text)
            for img in set(imgs):
                if any(k in img.lower() for k in ['daredevil', 'kingpin', 'fisk', 'maleev', 'preview', 'i.redd.it', 'external-preview']):
                    print("  Img:", img)
    except Exception as e:
        print("Error:", e)
