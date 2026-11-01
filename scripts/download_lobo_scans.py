import requests
from io import BytesIO
from PIL import Image

scans = [
    ("lobo_hell_01.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjwAKiSWSsyb6WBqKuP6dl8Oi1eM0GiXa1H-xF2azDfIINsPNKNX6mOKRMFCP-9-Fc18sy-d9AFPlYd97fZUYCmLjMoLbzHQ510zoUGjdj6lxbkL2sjzGmeKFurYqe4f_6tj19dXi3ZpKk/s1600/Lobo%2527s_Back_01-19.jpg"),
    ("lobo_heaven_02.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEif4lS4Ggr3YYXYgtWJeGo2oofEsI-siZIxgPpd-NAYii_gywAu34miZNJEbcN5o-bzFxwpN_YMIdptIMt0wpiWXGgCB2CZlcgvYzBQcEu_iiL8Wxp7eVhCFq3gIM_YHcO_M2LZU5eFwYg/s1600/lobo_heaven.jpg"),
    ("lobo_back_03.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi1G3md-xXGNFiW9e50PeiLzAZZLy1CDujpMuEM80Aj-X7HbeeUTgA-OoExODLEc_lqymHM2dUxRoMgeGGvKogRxQhkkzAjOZsSuz5UqzBt088L-Jj6O_iX-70whtWLplofZv2i12OhNVg/s1600/Lobo%2527s_Back_03-06.jpg"),
    ("lobo_back_04.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhWo79k1Wjs-HRN6eM8wtP9qsVli_9KHJLKQVw5nk3G_Xo-0WThz6je-H9Y9a_70GQQ1oSRY-7vWor1nN5yLYXsPxghObgN3qkR8n7QpGCX00f36vxKaZ7S8qbjf4pIZvTRT5FwGJKBGNU/s1600/Lobo%2527s+Back+%252304_03.jpg"),
    ("lobo_heaven_song.jpg", "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjnt0ugZpIC8Dfu2RIv_pAGOzwVYzcY4SG77LloKumA915XgSrs8ChtCf6KQAR5ZTnSK5D32_xD00RZppH3Tno59hhcESBwI6IJ-gGDbh-jJPh6GBaJISKAfLQ3ewHDObBmCQJvRJFubzk/s1600/b3_64857_0_LobosBack224HeavenIsAFourLette.jpg")
]

headers = {'User-Agent': 'Mozilla/5.0'}
for fname, u in scans:
    r = requests.get(u, headers=headers)
    print(f"Downloaded {fname}: status {r.status_code}, len {len(r.content)}")
    im = Image.open(BytesIO(r.content)).convert('RGB')
    im.save(fname, quality=95)
    print(f"  Saved {fname}, size: {im.size}")
