"""
Comic Lore Vault - Buffer Multi-Platform Publisher (TikTok Integration)
Enables 1-click automatic publishing to TikTok via Buffer GraphQL API.
"""

import os
import time
from pathlib import Path
import requests

BUFFER_GRAPHQL_URL = "https://api.buffer.com"


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [Buffer/TikTok] {msg}", flush=True)


def upload_to_temporary_public_url(video_path: str | Path) -> str:
    """
    Uploads the local MP4 video to a fast, temporary direct HTTPS host (tmpfiles.org)
    so Buffer's media fetcher can pull the file directly for publishing.
    """
    vpath = Path(video_path)
    if not vpath.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    log(f"Uploading {vpath.name} ({vpath.stat().st_size / (1024*1024):.1f} MB) to temporary public HTTPS host for Buffer...")
    upload_url = "https://tmpfiles.org/api/v1/upload"

    with open(vpath, "rb") as f:
        r = requests.post(upload_url, files={"file": f}, timeout=120)

    if r.status_code != 200:
        raise RuntimeError(f"Failed to upload video to temporary storage ({r.status_code}): {r.text}")

    data = r.json()
    raw_url = data.get("data", {}).get("url")
    if not raw_url:
        raise RuntimeError(f"Unexpected upload response: {data}")

    # Convert preview page URL to direct download URL (insert /dl/ after domain)
    # e.g., https://tmpfiles.org/12345/file.mp4 -> https://tmpfiles.org/dl/12345/file.mp4
    direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
    log(f"Public direct video URL generated: {direct_url}")
    return direct_url


def get_buffer_channels(access_token: str | None = None) -> list[dict]:
    """Retrieves all connected social channels (including TikTok) for the Buffer account."""
    token = access_token or os.environ.get("BUFFER_ACCESS_TOKEN")
    if not token:
        log("ERROR: BUFFER_ACCESS_TOKEN not found in environment.")
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    query_orgs = """
    query GetOrg {
      account {
        organizations {
          id
          name
        }
      }
    }
    """

    try:
        r = requests.post(BUFFER_GRAPHQL_URL, json={"query": query_orgs}, headers=headers, timeout=20)
        res = r.json()
        orgs = res.get("data", {}).get("account", {}).get("organizations", [])
        all_channels = []
        for org in orgs:
            org_id = org.get("id")
            if not org_id:
                continue
            query_ch = f"""
            query GetChannels {{
              channels(input: {{ organizationId: "{org_id}" }}) {{
                id
                name
                displayName
                service
              }}
            }}
            """
            r_ch = requests.post(BUFFER_GRAPHQL_URL, json={"query": query_ch}, headers=headers, timeout=20)
            res_ch = r_ch.json()
            channels = res_ch.get("data", {}).get("channels", [])
            all_channels.extend(channels)
        return all_channels
    except Exception as e:
        log(f"Error fetching Buffer channels: {e}")
        return []


def publish_to_tiktok_via_buffer(
    video_path: str | Path,
    caption: str,
    thumb_offset_ms: int = 2500,
    access_token: str | None = None,
    channel_id: str | None = None,
) -> dict:
    """
    Publishes a video to TikTok using Buffer's GraphQL API (Direct Publishing).
    1. Uploads video binary to direct temporary HTTPS storage.
    2. Sends createPost mutation with channelId, video asset, and action thumbnail offset.
    """
    token = access_token or os.environ.get("BUFFER_ACCESS_TOKEN")
    ch_id = channel_id or os.environ.get("BUFFER_TIKTOK_CHANNEL_ID")

    if not token:
        log("ERROR: BUFFER_ACCESS_TOKEN is missing. Skipping TikTok publishing.")
        return {"success": False, "error": "Missing BUFFER_ACCESS_TOKEN"}

    # Auto-discover TikTok channel if channel_id not explicitly configured
    if not ch_id:
        channels = get_buffer_channels(token)
        tiktok_ch = next((c for c in channels if str(c.get("service")).lower() == "tiktok"), None)
        if tiktok_ch:
            ch_id = tiktok_ch["id"]
            log(f"Auto-discovered TikTok channel in Buffer: '{tiktok_ch.get('displayName') or tiktok_ch.get('name')}' (ID: {ch_id})")
        else:
            log("ERROR: No TikTok channel connected in your Buffer account. Please connect TikTok at buffer.com.")
            return {"success": False, "error": "No TikTok channel found in Buffer account"}

    try:
        # Step 1: Upload to temporary direct HTTPS host
        direct_video_url = upload_to_temporary_public_url(video_path)

        # Step 2: Post to Buffer via GraphQL mutation
        log(f"Sending video to Buffer for TikTok publishing (Channel: {ch_id})...")
        mutation = """
        mutation CreateTikTokPost($input: CreatePostInput!) {
          createPost(input: $input) {
            ... on PostActionSuccess {
              post {
                id
                text
                status
              }
            }
            ... on MutationError {
              message
            }
          }
        }
        """

        variables = {
            "input": {
                "channelId": ch_id,
                "text": caption,
                "schedulingType": "automatic",
                "mode": "shareNow",
                "assets": [
                    {
                        "video": {
                            "url": direct_video_url,
                            "metadata": {
                                "thumbnailOffset": thumb_offset_ms
                            }
                        }
                    }
                ]
            }
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        r = requests.post(BUFFER_GRAPHQL_URL, json={"query": mutation, "variables": variables}, headers=headers, timeout=30)
        res = r.json()

        data = res.get("data", {}).get("createPost", {})
        if "post" in data:
            post_id = data["post"]["id"]
            log(f"SUCCESS: Video published to TikTok via Buffer! Post ID: {post_id}")
            return {"success": True, "post_id": post_id, "status": data["post"].get("status")}
        else:
            err_msg = data.get("message") or res.get("errors") or res
            log(f"ERROR publishing to Buffer TikTok: {err_msg}")
            return {"success": False, "error": str(err_msg)}

    except Exception as e:
        log(f"EXCEPTION publishing to TikTok via Buffer: {e}")
        return {"success": False, "error": str(e)}
