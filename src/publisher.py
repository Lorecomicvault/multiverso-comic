"""
Comic Lore Vault - Multi-Platform Social Publisher
Brand: Comic Lore Vault (@comicloreevault)
Supported Platforms:
- Facebook Page: Comic Lore Vault (ID: 1376898195488241)
- Instagram Business: @comicloreevault (ID: 17841427222576885)
"""

import os
import sys
import time
from pathlib import Path
import requests

DEFAULT_PAGE_ID = '1376898195488241'
DEFAULT_IG_USER_ID = '17841427222576885'
GRAPH_API_VERSION = 'v20.0'


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [Publisher] {msg}", flush=True)


def publish_to_facebook_page(
    video_path: str | Path,
    title: str,
    description: str,
    page_token: str | None = None,
    page_id: str | None = None,
    published: bool = True,
) -> dict:
    """Uploads and publishes a video directly to Comic Lore Vault Facebook Page (or saves as draft if published=False)."""
    token = page_token or os.environ.get('FB_PAGE_TOKEN')
    pid = page_id or os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)

    if not token:
        log("ERROR: FB_PAGE_TOKEN not provided or found in environment.")
        return {'success': False, 'error': 'Missing FB_PAGE_TOKEN'}

    vpath = Path(video_path)
    if not vpath.exists():
        log(f"ERROR: Video file not found: {video_path}")
        return {'success': False, 'error': f'File not found: {video_path}'}

    status_str = "PUBLISHED" if published else "DRAFT (Unpublished)"
    log(f"Publishing video to Facebook Page '{pid}' ({vpath.name}, {vpath.stat().st_size / (1024*1024):.1f} MB, mode: {status_str})...")
    url = f"https://graph-video.facebook.com/{GRAPH_API_VERSION}/{pid}/videos"

    payload = {
        'title': title,
        'description': description,
        'access_token': token,
        'published': 'true' if published else 'false',
    }

    try:
        with open(vpath, 'rb') as f:
            files = {'source': (vpath.name, f, 'video/mp4')}
            response = requests.post(url, data=payload, files=files, timeout=600)

        res_data = response.json()
        if response.status_code == 200 and 'id' in res_data:
            video_id = res_data['id']
            log(f"SUCCESS: Video published to Comic Lore Vault FB Page! Video ID: {video_id}")
            return {'success': True, 'video_id': video_id}
        else:
            log(f"ERROR: FB upload failed ({response.status_code}): {res_data}")
            return {'success': False, 'error': res_data}

    except Exception as e:
        log(f"EXCEPTION uploading to Facebook: {e}")
        return {'success': False, 'error': str(e)}


def publish_to_instagram_reels(
    video_url: str,
    caption: str,
    access_token: str | None = None,
    ig_user_id: str | None = None,
    max_wait_seconds: int = 300,
) -> dict:
    """Publishes a video as an Instagram Reel to @comicloreevault via Instagram Graph API container workflow."""
    token = access_token or os.environ.get('FB_PAGE_TOKEN')
    ig_id = ig_user_id or os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)

    if not token:
        log("ERROR: FB_PAGE_TOKEN not provided for Instagram publishing.")
        return {'success': False, 'error': 'Missing access token'}

    if not video_url or not video_url.startswith('http'):
        log("ERROR: Instagram Reels requires a valid publicly accessible HTTP/HTTPS video URL.")
        return {'success': False, 'error': 'Invalid video_url'}

    log(f"Step 1: Creating Instagram Reels container for @comicloreevault (ID: {ig_id})...")
    create_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media"
    create_payload = {
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': caption,
        'access_token': token,
    }

    try:
        r = requests.post(create_url, data=create_payload, timeout=60)
        res = r.json()
        if 'id' not in res:
            log(f"ERROR creating container ({r.status_code}): {res}")
            return {'success': False, 'error': res}

        creation_id = res['id']
        log(f"Container created successfully. Creation ID: {creation_id}")

        log("Step 2: Polling container processing status...")
        status_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{creation_id}"
        start_time = time.time()

        while time.time() - start_time < max_wait_seconds:
            time.sleep(10)
            status_res = requests.get(status_url, params={
                'fields': 'status_code,status',
                'access_token': token
            }, timeout=30).json()

            status_code = status_res.get('status_code')
            log(f"Container status: {status_code} ({status_res.get('status', '')})")

            if status_code == 'FINISHED':
                break
            elif status_code in ('ERROR', 'EXPIRED'):
                log(f"ERROR in processing: {status_res}")
                return {'success': False, 'error': status_res}

        if status_code != 'FINISHED':
            return {'success': False, 'error': 'Timeout waiting for video processing'}

        log("Step 3: Publishing Reel to @comicloreevault...")
        pub_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media_publish"
        pub_res = requests.post(pub_url, data={
            'creation_id': creation_id,
            'access_token': token
        }, timeout=60).json()

        if 'id' in pub_res:
            media_id = pub_res['id']
            log(f"SUCCESS: Reel published to @comicloreevault! Reel Media ID: {media_id}")
            return {'success': True, 'media_id': media_id}
        else:
            log(f"ERROR publishing container: {pub_res}")
            return {'success': False, 'error': pub_res}

    except Exception as e:
        log(f"EXCEPTION publishing to Instagram: {e}")
        return {'success': False, 'error': str(e)}


def upload_temp_video_url(video_path: str | Path) -> str | None:
    """Uploads video to a temporary direct hosting URL (1h expiry) for Instagram Reel container ingestion."""
    vpath = Path(video_path)
    log(f"Uploading temporary video copy for Instagram Reels ingestion ({vpath.name}, {vpath.stat().st_size / (1024*1024):.1f} MB)...")
    try:
        data = {'reqtype': 'fileupload', 'time': '1h'}
        with open(vpath, 'rb') as f:
            files = {'fileToUpload': (vpath.name, f, 'video/mp4')}
            r = requests.post('https://litterbox.catbox.moe/resources/internals/api.php', data=data, files=files, timeout=180)
        if r.status_code == 200 and r.text.strip().startswith('http'):
            direct_url = r.text.strip()
            log(f"Temporary direct video URL ready: {direct_url}")
            return direct_url
        else:
            log(f"Warning: Temp video upload returned: {r.status_code} {r.text}")
            return None
    except Exception as e:
        log(f"Exception uploading temp video: {e}")
        return None


def publish_comic_video(
    video_path: str | Path,
    title: str,
    description: str,
    hashtags: str = '#Comics #Marvel #DC #ComicLoreVault #ComicTok #Reels',
    video_url: str | None = None,
    draft_only: bool = False,
) -> dict:
    """Orchestrates publishing across Comic Lore Vault Facebook and Instagram destinations."""
    results = {}
    full_caption = f"{title}\n\n{description}\n\n{hashtags}".strip()

    # 1. Publish to Facebook Page (direct multipart upload)
    fb_res = publish_to_facebook_page(
        video_path=video_path,
        title=title,
        description=full_caption,
        published=not draft_only,
    )
    results['facebook'] = fb_res

    # 2. Publish to Instagram Reels
    if draft_only:
        log("Notice: draft_only=True. Skipping public Instagram publication.")
        results['instagram'] = {'skipped': True, 'reason': 'draft_only mode enabled'}
    else:
        if not video_url:
            video_url = upload_temp_video_url(video_path)

        if video_url:
            ig_res = publish_to_instagram_reels(
                video_url=video_url,
                caption=full_caption,
            )
            results['instagram'] = ig_res
        else:
            log("ERROR: Could not obtain public video URL for Instagram Reel.")
            results['instagram'] = {'success': False, 'error': 'Could not obtain public video URL'}

    return results


if __name__ == '__main__':
    print("Comic Lore Vault Social Publisher Module")
    print(f"Target FB Page: {DEFAULT_PAGE_ID} (Comic Lore Vault)")
    print(f"Target Instagram: {DEFAULT_IG_USER_ID} (@comicloreevault)")
    token_status = 'DETECTED' if os.environ.get('FB_PAGE_TOKEN') else 'NOT SET (will read from GitHub Secret)'
    print(f"FB_PAGE_TOKEN: {token_status}")
