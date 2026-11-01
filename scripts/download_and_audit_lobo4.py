import requests
from io import BytesIO
from PIL import Image
import sys

PROJECT_ROOT = r"C:\Users\Vanes\comics en espanol"
sys.path.insert(0, PROJECT_ROOT)
from src.comic_precision_scraper import verify_visual_alignment_with_gemini

urls = [
    ("lobo_01_08.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEju6Vk2yAYtQqAlSi7rX2SKzIGD4Ynz4_FziGPUR1viNXPQj58uB3Cspo2jyiZFAhyN_uMrheyivJDLaurQfKzML0lzvwTuQlKpecLiUYRiEftqKoQVqdwgQjV41XOGOMjHzX9fTFYPcR8/s1600/Lobo%2527s_Back_01-08.jpg"),
    ("lobo_01_00a.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiETbOfvVur0lCvvPe7iSK55DSk5M-S6MuD77ApzeOEGdKBJmQoqzuVgAl5ARhZ-Bf-NgxYo39balhgyl2Fphwn7X8rczAYK1zc99koS1CJWR1yudt8OlZqetxJM2mqiLwZTIBXgzk838I/s1600/Lobo%2527s_Back_01-00a.jpg"),
    ("lobo_lb3.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjWxzZQViza-JlORYkViYt4gSB_eNsx7BGOSElu-u5A82RI91tuaKEdqrellv9OHidqEt5vJxMDAIS4_NG0fZL9wacfry2B2NEHk_TpSpdH1pxAm3lYCWF20mYBVTptul5U2knZM6PGtfU/s1600/LB3.jpg"),
    ("lobo_lb4.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgljr3x6DO0HsH1GkpnfHSz4fyyG7fE8G1Qos40XQpCup34Dy_kSNCkNXMBpQVYf3UP5PU09uK9tjpBmGMTaZ-PmJAhr0YECixQgoymhI5PThC6of039btlOk25nZOLzyqLJBXXGFWk7DM/s1600/LB4.jpg")
]

headers = {'User-Agent': 'Mozilla/5.0'}
for fname, u in urls:
    r = requests.get(u, headers=headers)
    print(f"Downloaded {fname}: status {r.status_code}, len {len(r.content)}")
    im = Image.open(BytesIO(r.content)).convert('RGB')
    im.save(fname, quality=95)
    audit = verify_visual_alignment_with_gemini(fname, "Lobo en el Infierno o Cielo o combatiendo o resucitando")
    print(f"Audit {fname}: Score={audit.get('score')}/10, Action={audit.get('depicts_action')}")
    print(f"  Reason: {audit.get('reason')}")
