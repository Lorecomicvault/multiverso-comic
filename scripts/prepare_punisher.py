import os
import sys
import requests
from io import BytesIO
from PIL import Image
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\Vanes\comics en espanol")
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(str(PROJECT_ROOT))

from src.cloud_runner import create_full_panel_frame
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

dest_dir = PROJECT_ROOT / "assets" / "curated_panels" / "punisher_oso_polar_zoologico_gnucci"
dest_dir.mkdir(parents=True, exist_ok=True)

# Scene 1: Already has authentic panel from Punisher Vol 5
# Scene 2: Frank fighting mobsters in zoo
# Scene 3: Frank punches polar bear in face (10/10)
# Scene 4: Polar bear mauls mobster in zoo (10/10)

headers = {'User-Agent': 'Mozilla/5.0'}

# Scene 2 candidate: http://photos1.blogger.com/img/198/4480/400/punisher%204%20groin1.jpg
r2 = requests.get('http://photos1.blogger.com/img/198/4480/400/punisher%204%20groin1.jpg', headers=headers)
im2 = Image.open(BytesIO(r2.content)).convert('RGB')
framed2 = create_full_panel_frame(im2, 1080, 1920)
framed2.save(dest_dir / 'scene_02.jpg', quality=95)

# Scene 3: Polar bear punch
r3 = requests.get('https://i.redd.it/qlv7lz54ymlf1.jpeg', headers=headers)
im3 = Image.open(BytesIO(r3.content)).convert('RGB')
framed3 = create_full_panel_frame(im3, 1080, 1920)
framed3.save(dest_dir / 'scene_03.jpg', quality=95)

# Scene 4: Polar bear attacks mobster
r4 = requests.get('http://photos1.blogger.com/img/198/4480/400/punisher%204%20bear%20swat1.jpg', headers=headers)
im4 = Image.open(BytesIO(r4.content)).convert('RGB')
framed4 = create_full_panel_frame(im4, 1080, 1920)
framed4.save(dest_dir / 'scene_04.jpg', quality=95)

scenes_texts = [
    "En su guerra sin cuartel contra la familia criminal Gnucci, Frank Castle persiguió a los últimos matones de la mafia a través del zoológico de Central Park en plena noche.",
    "Al verse acorralado frente a la fosa de exhibición, el sicario intentó abrir fuego, pero The Punisher esquivó las balas y lo desarmó con un golpe demoledor en la mandíbula.",
    "En lugar de gastar una bala, Frank levantó al criminal en peso y lo arrojó directamente al recinto helado, donde un gigantesco oso polar lo esperaba hambriento.",
    "Mientras los gritos del criminal resonaban en la noche y el depredador lo devoraba sin piedad, The Punisher simplemente se acomodó la gabardina y desapareció en las sombras."
]

print("AUDITING PUNISHER SCENES:")
for i, txt in enumerate(scenes_texts, 1):
    fpath = dest_dir / f"scene_{i:02d}.jpg"
    res = verify_visual_alignment_with_gemini(str(fpath), txt)
    print(f"Scene {i}: Score={res.get('score')}/10, Comic={res.get('is_comic_panel')}, Action={res.get('depicts_action')}")
    print(f"  Reason: {res.get('reason')}")
