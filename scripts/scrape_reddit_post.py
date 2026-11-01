import sys
import requests
import json
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF6poh9tUOzr3lwTfjLDVSXLLBPx2-wFRBodsuReQY1L83vDh35xVDBGBFoTX6TTHjPg7pvVDymevMowbBaFMsZU1Smh2DHu0ZDKDUtbULa7DNRx0yfXEvv-HT0eJGr1OIy9iAjk_C5riYl1W_zwi0dDQaUNAFnRNmF-WrVhKS2zPScf0h35UIBTZ_wB9L6ryVPzj__oFE=',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHTwZhXIL4IP6aQwgCmDL46QL1VrRJV23Ioz9b3DjnLmOmYPwmB9_vbOSmlqzskA0QIwmD0q6m4Z_pQ4w3DGE8ifXeihbLZdecof9NE1ik4fGEm158TFfg0H11bplwUsgKUyARBEn4Eh0Kz6kqThY7QB_fkCJEeu8Q3yyHHNE_5sDV6E3EGwnVKwDHMh18lhioN03SHDQ==',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFGbM75zgtGMHCTMEY04h5QkhearST8ulisrXiRC44d-_vnhYEPVii1K2gHFgv845_9jzXgsPMYlo2kPNYdXPqgUjJnekozuDVlwccdsPAxcQCpJ-jXxKDwU_devj-FeRIv2jaN6_nv1dKYp38Y6OvtCcJEH9MqlAcQi260MPVT6Q3ae4qixrDrrrDUjv2daQsBk9-GQuque5STesIBuF1medt5sA=='
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for u in urls:
    try:
        r = requests.get(u, allow_redirects=True, headers=headers, timeout=10)
        print('Resolved:', r.url)
        # Find i.redd.it or preview.redd.it
        matches = re.findall(r'https?://[^\s"\'<>]*(?:i\.redd\.it|preview\.redd\.it)[^\s"\'<>]*', r.text)
        print(f"Found {len(matches)} reddit images:")
        for m in set(matches):
            clean = m.split('&amp;')[0].replace('&amp;', '&')
            print('  ', clean)
    except Exception as e:
        print('Error:', e)
