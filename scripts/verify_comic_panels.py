import os
import sys
import base64
import json
from pathlib import Path
from dotenv import load_dotenv
import requests

load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')

def verify_image(path):
    p = Path(path)
    if not p.exists():
        return "FILE NOT FOUND"
    try:
        with open(p, 'rb') as f:
            b64_data = base64.b64encode(f.read()).decode('utf-8')
        
        prompt = "Describe this comic image in 1-2 sentences: is it an authentic comic book panel/drawing? Which characters, scene, and publisher (DC or Marvel) are shown?"
        payload = {
            "contents": [{
                "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_data}},
                    {"text": prompt}
                ]
            }]
        }
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        if r.status_code == 200:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            return f"API Error {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    images_to_check = {
        'post_04_flash_crisis': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_04_flash_crisis.jpg',
        'post_10_daredevil': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_10_daredevil_bullseye.jpg',
        'post_11_black_adam': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_11_black_adam_ww3.jpg',
        'post_13_grim_knight': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_13_grim_knight.jpg',
        'post_14_punisher': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_14_punisher_kills_marvel.jpg',
        'post_15_ruins_banner': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_15_marvel_ruins_banner.jpg',
        'post_16_black_manta': r'C:\Users\Vanes\comics en espanol\assets\facebook_posts\post_16_black_manta_aquaman.jpg',
        'audit_ghost_rider_hulk': r'C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb\audit_ghost_rider_vs_world_war_hulk.jpg',
        'audit_red_death': r'C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb\audit_batman_red_death_speed_force.jpg',
        'tower_babel': r'C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb\tower_babel_scene2_1788289631737.jpg',
        'cap_scenes': r'C:\Users\Vanes\.gemini\antigravity\brain\40b9647f-2c85-4ec0-9b46-8cbfa1fadfdb\cap_scenes.jpg'
    }

    for name, p in images_to_check.items():
        print(f"=== {name} ===")
        desc = verify_image(p)
        print(desc)
        print()
