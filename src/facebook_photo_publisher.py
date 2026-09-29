"""
Comic Lore Vault - Facebook Photo Publisher & Progressive Scheduler
Automates progressive publishing of authentic viral comic panels to the Facebook Page.
Fulfills Facebook Professional Dashboard goals:
- "Crea 19 publicaciones públicas nuevas con fotos"
- "Crea 19 publicaciones públicas nuevas"
"""

import os
import sys
import time
import datetime
from pathlib import Path
import requests

PAGE_ID = os.environ.get('FB_PAGE_ID', '1289410784257454')
ACCESS_TOKEN = os.environ.get('FB_PAGE_TOKEN', 'EAAduw9ZBIaysBSVYGkNZCmRYBKHwiPpwlkZBiFxM5SNCWCBnmMLhl7SDSvUNFJXzn6xSYQBeKDNseZA3bM5cwCxcIV7L4bim7nlIU5CtgsB8gZCy82iew2MZB72Q13ODT8yBKcFrdRHXhUziR7DwOqMCoZBOcTd4whcwZByMWR4xQfqWJEl7gHZCRT3HOtZA73OMBCaZCzi')
GRAPH_API_VERSION = 'v20.0'

# Best engagement hours for Latin American / Spanish-speaking Facebook audiences:
# Window 1: 12:30 PM (Midday lunch/work break)
# Window 2: 07:30 PM (Evening prime-time relaxation)
OPTIMAL_HOURS = [(12, 30), (19, 30)]


def publish_facebook_photo(
    image_path: str | Path,
    caption: str,
    scheduled_timestamp: int | None = None,
    page_id: str | None = None,
    page_token: str | None = None
) -> dict:
    """Publishes immediately or schedules a photo on the Facebook Page via Graph API."""
    pid = page_id or PAGE_ID
    token = page_token or ACCESS_TOKEN
    img_file = Path(image_path)

    if not img_file.exists():
        return {'success': False, 'error': f'Image not found: {image_path}'}

    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{pid}/photos"
    payload = {
        'caption': caption,
        'access_token': token
    }

    if scheduled_timestamp:
        payload['published'] = 'false'
        payload['scheduled_publish_time'] = str(scheduled_timestamp)
    else:
        payload['published'] = 'true'

    mime = 'image/png' if img_file.suffix.lower() == '.png' else 'image/jpeg'

    try:
        with open(img_file, 'rb') as f:
            files = {'source': (img_file.name, f, mime)}
            res = requests.post(url, data=payload, files=files, timeout=60).json()

        if 'id' in res:
            return {'success': True, 'id': res['id'], 'post_id': res.get('post_id')}
        else:
            return {'success': False, 'error': res}
    except Exception as e:
        return {'success': False, 'error': str(e)}
