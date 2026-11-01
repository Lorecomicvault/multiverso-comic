import requests
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF0Zg6UPU9XfOiB_ZiiNCDKXRgNcLlYd5BlGl8sfpnZm5M0e8X2aUq2h4o6hpgH3Tcp418moWqdiDGDM1y2gTboJr8SKKAaNAQxeIAMmK1XJ9VYEPmiu1GiDPx16xXVKz46Pe0PI9BRXvYewaxr-9LSyJbsYCRobgQCip3CbUqMkyGCtf_JqZ3ItgP_0bMgRiZW',
    'https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF2P_ZWdgmGqlOlomfOSProsxaeBnL9bpKDdSJmcqPCxpS070KYVqIaonUPb5Q3hhsI3tMnCI_6_wlrNwy0D1zsEPz8etOELLPuxjYHyAcsRdaRcaMM0Yl_fpuvjsNEMMtug8XQsKbQM6Uk_dP1jUBg4igFrzGqtC7SjEDoxYWWM4wnLUbk3hoZ8T5cqEAcvzq6KHOJignD'
]

for idx, u in enumerate(urls, 1):
    try:
        r = requests.get(u, headers=headers, timeout=6)
        print(f"URL {idx} -> {r.url}")
        m = re.findall(r'(https?://(?:i\.redd\.it|preview\.redd\.it|i\.imgur\.com)/[^\s\"\'<>&]+)', r.text)
        print(f"  Found {len(m)} images:")
        for im in set(m):
            print("   ", im)
    except Exception as e:
        print(f"Error {idx}: {e}")
