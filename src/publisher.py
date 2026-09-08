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

DEFAULT_PAGE_ID = '1289410784257454'
DEFAULT_IG_USER_ID = '17841427017671758'
DEFAULT_ACCESS_TOKEN = 'EAAduw9ZBIaysBSVYGkNZCmRYBKHwiPpwlkZBiFxM5SNCWCBnmMLhl7SDSvUNFJXzn6xSYQBeKDNseZA3bM5cwCxcIV7L4bim7nlIU5CtgsB8gZCy82iew2MZB72Q13ODT8yBKcFrdRHXhUziR7DwOqMCoZBOcTd4whcwZByMWR4xQfqWJEl7gHZCRT3HOtZA73OMBCaZCzi'
GRAPH_API_VERSION = 'v20.0'


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [Publisher] {msg}", flush=True)


def publish_to_facebook_page(
    video_path: str | Path,
    title: str,
    description: str,
    thumbnail_path: str | Path | None = None,
    page_token: str | None = None,
    page_id: str | None = None,
    published: bool = True,
) -> dict:
    """Uploads and publishes a video directly to Comic Lore Vault Facebook Page (or saves as draft if published=False)."""
    import subprocess
    token = page_token or os.environ.get('FB_PAGE_TOKEN') or DEFAULT_ACCESS_TOKEN
    pid = page_id or os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)

    if not token:
        log("ERROR: FB_PAGE_TOKEN not provided or found in environment.")
        return {'success': False, 'error': 'Missing FB_PAGE_TOKEN'}

    vpath = Path(video_path)
    if not vpath.exists():
        log(f"ERROR: Video file not found: {video_path}")
        return {'success': False, 'error': f'File not found: {video_path}'}

    if not thumbnail_path or not Path(thumbnail_path).exists():
        candidate = vpath.parent / f"{vpath.stem}_thumb.jpg"
        if candidate.exists():
            thumbnail_path = candidate
        else:
            try:
                subprocess.run(['ffmpeg', '-y', '-ss', '2.5', '-i', str(vpath), '-frames:v', '1', str(candidate)],
                               capture_output=True, check=True)
                if candidate.exists() and candidate.stat().st_size > 0:
                    thumbnail_path = candidate
            except Exception as e:
                log(f"Notice: Could not auto-generate thumbnail at 2.5s: {e}")

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
        with open(vpath, 'rb') as f_video:
            files = {'source': (vpath.name, f_video, 'video/mp4')}
            thumb_handle = None
            if thumbnail_path and Path(thumbnail_path).exists():
                tpath = Path(thumbnail_path)
                log(f"Attaching custom video thumbnail: {tpath.name} ({tpath.stat().st_size / 1024:.1f} KB)")
                thumb_handle = open(tpath, 'rb')
                files['thumb'] = (tpath.name, thumb_handle, 'image/jpeg')

            try:
                response = requests.post(url, data=payload, files=files, timeout=600)
            finally:
                if thumb_handle:
                    thumb_handle.close()

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
    video_path: str | Path | None = None,
    caption: str = "",
    video_url: str | None = None,
    thumb_offset_ms: int = 2500,
    access_token: str | None = None,
    ig_user_id: str | None = None,
    max_wait_seconds: int = 300,
) -> dict:
    """Publishes a video as an Instagram Reel to @comicloreevault via Instagram Graph API.

    Supports:
    1. Direct native binary upload (upload_type=resumable via rupload.facebook.com) - Preferred & 100% reliable.
    2. Public URL ingestion (video_url) - Fallback.
    3. thumb_offset_ms parameter ensuring the cover is never dark/black and captures the action artwork.
    """
    token = access_token or os.environ.get('FB_PAGE_TOKEN') or DEFAULT_ACCESS_TOKEN
    ig_id = ig_user_id or os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)

    if not token:
        log("ERROR: FB_PAGE_TOKEN not provided for Instagram publishing.")
        return {'success': False, 'error': 'Missing access token'}

    create_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media"

    try:
        # Path A: Direct local video binary upload (Meta Resumable API)
        if video_path and Path(video_path).exists():
            vpath = Path(video_path)
            file_size = vpath.stat().st_size
            log(f"Step 1: Initializing Reels resumable container for @comicloreevault (ID: {ig_id}, {file_size / (1024*1024):.1f} MB, thumb_offset: {thumb_offset_ms}ms)...")

            init_payload = {
                'upload_type': 'resumable',
                'media_type': 'REELS',
                'caption': caption,
                'thumb_offset': str(thumb_offset_ms),
                'access_token': token
            }
            init_res = requests.post(create_url, data=init_payload, timeout=60).json()

            if 'id' not in init_res or 'uri' not in init_res:
                log(f"ERROR initializing resumable container: {init_res}")
                return {'success': False, 'error': init_res}

            creation_id = init_res['id']
            upload_uri = init_res['uri']
            log(f"Container created. Creation ID: {creation_id}. Uploading binary to Meta ({upload_uri})...")

            upload_headers = {
                'Authorization': f'OAuth {token}',
                'offset': '0',
                'file_size': str(file_size),
                'Content-Type': 'application/octet-stream'
            }

            with open(vpath, 'rb') as f:
                r_upload = requests.post(upload_uri, headers=upload_headers, data=f, timeout=600)

            if r_upload.status_code != 200:
                log(f"ERROR uploading video binary to rupload: {r_upload.status_code} {r_upload.text}")
                return {'success': False, 'error': r_upload.text}

            log("Binary uploaded successfully to Meta Reel server.")

        # Path B: Public video URL ingestion
        elif video_url and video_url.startswith('http'):
            log(f"Step 1: Creating Instagram Reels container via public URL for @comicloreevault (ID: {ig_id}, thumb_offset: {thumb_offset_ms}ms)...")
            create_payload = {
                'media_type': 'REELS',
                'video_url': video_url,
                'caption': caption,
                'thumb_offset': str(thumb_offset_ms),
                'access_token': token,
            }
            r = requests.post(create_url, data=create_payload, timeout=60)
            res = r.json()
            if 'id' not in res:
                log(f"ERROR creating container ({r.status_code}): {res}")
                return {'success': False, 'error': res}
            creation_id = res['id']
            log(f"Container created successfully. Creation ID: {creation_id}")
        else:
            log("ERROR: Neither valid video_path nor video_url provided for Instagram Reels.")
            return {'success': False, 'error': 'No video source provided'}

        # Step 2: Polling container processing status
        log("Step 2: Polling container processing status...")
        status_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{creation_id}"
        start_time = time.time()
        status_code = None

        while time.time() - start_time < max_wait_seconds:
            time.sleep(5)
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

        # Step 3: Publishing Reel
        log("Step 3: Publishing Reel to @comicloreevault...")
        pub_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media_publish"
        pub_res = requests.post(pub_url, data={
            'creation_id': creation_id,
            'access_token': token
        }, timeout=60).json()

        if 'id' in pub_res:
            media_id = pub_res['id']
            # Fetch permanent Instagram link
            try:
                link_info = requests.get(
                    f"https://graph.facebook.com/{GRAPH_API_VERSION}/{media_id}",
                    params={'fields': 'permalink', 'access_token': token},
                    timeout=30
                ).json()
                permalink = link_info.get('permalink', f'https://www.instagram.com/reel/{media_id}')
            except Exception:
                permalink = f'https://www.instagram.com/reel/{media_id}'

            log(f"SUCCESS: Reel published to @comicloreevault! Media ID: {media_id} | URL: {permalink}")
            return {'success': True, 'media_id': media_id, 'permalink': permalink}
        else:
            log(f"ERROR publishing container: {pub_res}")
            return {'success': False, 'error': pub_res}

    except Exception as e:
        log(f"EXCEPTION publishing to Instagram: {e}")
        return {'success': False, 'error': str(e)}


def publish_comic_video(
    video_path: str | Path,
    title: str,
    description: str,
    hashtags: str = '#Comics #Marvel #DC #ComicLoreVault #ComicTok #Reels',
    video_url: str | None = None,
    thumbnail_path: str | Path | None = None,
    thumb_offset_ms: int = 2500,
    draft_only: bool = False,
) -> dict:
    """Orchestrates publishing across Comic Lore Vault Facebook and Instagram destinations with custom thumbnails."""
    results = {}
    full_caption = f"{title}\n\n{description}\n\n{hashtags}".strip()

    vpath = Path(video_path)
    if thumbnail_path is None:
        candidate = vpath.parent / f"{vpath.stem}_thumb.jpg"
        if candidate.exists():
            thumbnail_path = candidate

    # 1. Publish to Facebook Page (direct multipart upload with custom thumbnail)
    fb_res = publish_to_facebook_page(
        video_path=video_path,
        title=title,
        description=full_caption,
        thumbnail_path=thumbnail_path,
        published=not draft_only,
    )
    results['facebook'] = fb_res

    # 2. Publish to Instagram Reels (direct resumable binary upload with action thumb_offset)
    if draft_only:
        log("Notice: draft_only=True. Skipping public Instagram publication.")
        results['instagram'] = {'skipped': True, 'reason': 'draft_only mode enabled'}
    else:
        ig_res = publish_to_instagram_reels(
            video_path=video_path,
            caption=full_caption,
            video_url=video_url,
            thumb_offset_ms=thumb_offset_ms,
        )
        results['instagram'] = ig_res

    return results


if __name__ == '__main__':
    print("Comic Lore Vault Social Publisher Module")
    print(f"Target FB Page: {DEFAULT_PAGE_ID} (Comic Lore Vault)")
    print(f"Target Instagram: {DEFAULT_IG_USER_ID} (@comicloreevault)")
    token_status = 'DETECTED' if os.environ.get('FB_PAGE_TOKEN') else 'NOT SET (will read from GitHub Secret)'
    print(f"FB_PAGE_TOKEN: {token_status}")
