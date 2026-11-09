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
                subprocess.run(['ffmpeg', '-y', '-ss', '0.0', '-i', str(vpath), '-frames:v', '1', str(candidate)],
                               capture_output=True, check=True)
                if candidate.exists() and candidate.stat().st_size > 0:
                    thumbnail_path = candidate
            except Exception as e:
                log(f"Notice: Could not auto-generate thumbnail at 0.0s: {e}")

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
    thumb_offset_ms: int = 0,
    access_token: str | None = None,
    ig_user_id: str | None = None,
    max_wait_seconds: int = 300,
) -> dict:
    """Publishes a video as an Instagram Reel to @multiversoocomic via Instagram Graph API.

    Supports:
    1. Public URL ingestion (video_url) - Highly recommended & 100% reliable for Meta.
    2. Auto-resolution to GitHub raw CDN if video is in scheduled_queue.
    3. Direct native binary upload (upload_type=resumable via rupload.facebook.com) - Fallback.
    4. Emergency temporary host fallback (tmpfiles.org) if binary upload hits gateway timeouts.
    5. thumb_offset_ms parameter ensuring the cover captures the action artwork.
    """
    token = access_token or os.environ.get('FB_PAGE_TOKEN') or DEFAULT_ACCESS_TOKEN
    ig_id = ig_user_id or os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)

    if not token:
        log("ERROR: FB_PAGE_TOKEN not provided for Instagram publishing.")
        return {'success': False, 'error': 'Missing access token'}

    create_url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{ig_id}/media"

    # Auto-resolve public video URL if not explicitly provided
    if not video_url and video_path:
        vpath = Path(video_path)
        posix_str = vpath.as_posix()
        if "scheduled_queue/" in posix_str:
            subpath = posix_str[posix_str.find("scheduled_queue/"):]
            video_url = f"https://raw.githubusercontent.com/Lorecomicvault/multiverso-comic/main/{subpath}"
            log(f"Auto-resolved GitHub raw URL for Instagram Reels: {video_url}")

    creation_id = None

    try:
        # Strategy 1: Public video URL ingestion (Preferred & robust against gateway timeouts)
        if video_url and video_url.startswith('http'):
            log(f"Step 1: Creating Instagram Reels container via public URL for @multiversoocomic (ID: {ig_id}, URL: {video_url})...")
            create_payload = {
                'media_type': 'REELS',
                'video_url': video_url,
                'caption': caption,
                'thumb_offset': str(thumb_offset_ms),
                'access_token': token,
            }
            r = requests.post(create_url, data=create_payload, timeout=60)
            res = r.json()
            if 'id' in res:
                creation_id = res['id']
                log(f"Container created successfully via URL. Creation ID: {creation_id}")
            else:
                log(f"WARNING: URL container creation failed ({r.status_code}): {res}. Falling back to binary upload...")

        # Strategy 2: Direct local video binary upload (Meta Resumable API) if Strategy 1 not used or failed
        if not creation_id and video_path and Path(video_path).exists():
            vpath = Path(video_path)
            file_size = vpath.stat().st_size
            log(f"Step 1 (Fallback): Initializing Reels resumable container for @multiversoocomic (ID: {ig_id}, {file_size / (1024*1024):.1f} MB)...")

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

            with open(vpath, 'rb') as f:
                video_bytes = f.read()

            upload_headers = {
                'Authorization': f'OAuth {token}',
                'offset': '0',
                'file_size': str(file_size),
                'Content-Length': str(len(video_bytes)),
                'Content-Type': 'application/octet-stream'
            }

            r_upload = requests.post(upload_uri, headers=upload_headers, data=video_bytes, timeout=600)

            # Retry once if Meta returns a transient error on rupload
            if r_upload.status_code not in (200, 201):
                log(f"WARNING: Initial rupload failed ({r_upload.status_code}: {r_upload.text}). Retrying with fresh container in 5s...")
                time.sleep(5)
                retry_init = requests.post(create_url, data=init_payload, timeout=60).json()
                if 'id' in retry_init and 'uri' in retry_init:
                    creation_id = retry_init['id']
                    upload_uri = retry_init['uri']
                    r_upload = requests.post(upload_uri, headers=upload_headers, data=video_bytes, timeout=600)

            if r_upload.status_code not in (200, 201):
                # If rupload failed, try emergency temporary public URL (tmpfiles.org)
                log(f"WARNING: rupload failed ({r_upload.status_code}). Attempting emergency temporary host fallback...")
                try:
                    from .buffer_publisher import upload_to_temporary_public_url
                    temp_url = upload_to_temporary_public_url(vpath)
                    log(f"Emergency public URL obtained: {temp_url}. Creating container...")
                    r_temp = requests.post(create_url, data={
                        'media_type': 'REELS',
                        'video_url': temp_url,
                        'caption': caption,
                        'thumb_offset': str(thumb_offset_ms),
                        'access_token': token,
                    }, timeout=60).json()
                    if 'id' in r_temp:
                        creation_id = r_temp['id']
                        log(f"Container created successfully via emergency URL. ID: {creation_id}")
                    else:
                        return {'success': False, 'error': f"rupload failed and emergency url failed: {r_temp}"}
                except Exception as ex_temp:
                    log(f"ERROR: Emergency fallback failed: {ex_temp}")
                    return {'success': False, 'error': r_upload.text}
            else:
                log("Binary uploaded successfully to Meta Reel server.")

        if not creation_id:
            log("ERROR: Could not create Instagram Reels container through any method.")
            return {'success': False, 'error': 'No container created'}

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
        log("Step 3: Publishing Reel to @multiversoocomic...")
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

            log(f"SUCCESS: Reel published to @multiversoocomic! Media ID: {media_id} | URL: {permalink}")
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
    thumb_offset_ms: int = 0,
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

    # 3. Publish to TikTok via Buffer (if configured)
    tiktok_token = os.environ.get('BUFFER_TIKTOK_ACCESS_TOKEN') or os.environ.get('BUFFER_ACCESS_TOKEN')
    if tiktok_token and not draft_only:
        try:
            from .buffer_publisher import publish_to_tiktok_via_buffer
            tt_res = publish_to_tiktok_via_buffer(
                video_path=video_path,
                caption=full_caption,
                thumb_offset_ms=thumb_offset_ms,
                access_token=tiktok_token,
                channel_id=os.environ.get('BUFFER_TIKTOK_CHANNEL_ID'),
            )
            results['tiktok'] = tt_res
        except Exception as e:
            log(f"Warning publishing to TikTok via Buffer: {e}")
            results['tiktok'] = {'success': False, 'error': str(e)}
    elif not tiktok_token:
        results['tiktok'] = {'skipped': True, 'reason': 'BUFFER token not set for TikTok'}

    # 4. Publish to YouTube Shorts via Buffer (if configured)
    youtube_token = os.environ.get('BUFFER_YOUTUBE_ACCESS_TOKEN') or os.environ.get('BUFFER_ACCESS_TOKEN')
    if youtube_token and not draft_only:
        try:
            from .buffer_publisher import publish_to_youtube_via_buffer
            yt_res = publish_to_youtube_via_buffer(
                video_path=video_path,
                title=title,
                description=full_caption,
                access_token=youtube_token,
                channel_id=os.environ.get('BUFFER_YOUTUBE_CHANNEL_ID'),
            )
            results['youtube'] = yt_res
        except Exception as e:
            log(f"Warning publishing to YouTube Shorts via Buffer: {e}")
            results['youtube'] = {'success': False, 'error': str(e)}
    elif not youtube_token:
        results['youtube'] = {'skipped': True, 'reason': 'BUFFER token not set for YouTube'}

    return results


if __name__ == '__main__':
    print("Comic Lore Vault Social Publisher Module")
    print(f"Target FB Page: {DEFAULT_PAGE_ID} (Comic Lore Vault)")
    print(f"Target Instagram: {DEFAULT_IG_USER_ID} (@comicloreevault)")
    token_status = 'DETECTED' if os.environ.get('FB_PAGE_TOKEN') else 'NOT SET (will read from GitHub Secret)'
    print(f"FB_PAGE_TOKEN: {token_status}")
