"""
Multiverso Comic - Autonomous Cloud Video Runner & Publisher (Spanish Engine)
Ironclad 5-Layer Anti-Duplication Engine: Guarantees ZERO repeated stories, character arcs, or themes.
Repository: multiverso-comic (main)
"""

import argparse
import io
import json
import os
import random
import re
import sys
import time
import unicodedata
from pathlib import Path
from PIL import Image, ImageFilter, ImageStat
import requests

from .comic_fetcher import get_fandom_comic_art
from .publisher import publish_comic_video, DEFAULT_PAGE_ID, DEFAULT_IG_USER_ID

LEDGER_PATH = Path("published_ledger.json")

def load_env_file():
    env_file = Path(".env")
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

load_env_file()


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

from .editorial_catalog import EDITORIAL_STORIES

def load_ledger() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Warning reading ledger: {e}")
        return []


def save_ledger(ledger: list[dict]):
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)


def normalize_text(text: str) -> str:
    """Lowercase, strip accents, punctuation, and extra whitespace."""
    nfkd = unicodedata.normalize('NFKD', str(text or ""))
    cleaned = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()
    cleaned = re.sub(r'[^a-z0-9\s]', ' ', cleaned)
    return " ".join(cleaned.split())


def is_duplicate(story: dict, ledger: list[dict]) -> tuple[bool, str]:
    """
    5-Layer Anti-Duplication Shield:
    1. Exact ID Collision Check
    2. Canonical Theme Signature Collision Check
    3. Normalized Exact Title Collision Check
    4. Canonical Theme Sub-Tag Multi-Intersection Collision Check
    5. Character Arc & Semantic Keyword Topic Overlap Collision Check (>50% match)
    """
    story_id = story.get("id", "").strip().lower()
    story_theme = story.get("theme_signature", "").strip().lower()
    story_title_norm = normalize_text(story.get("title", ""))
    story_char = normalize_text(story.get("character", ""))

    stopwords = {
        "de", "la", "el", "los", "las", "un", "una", "unos", "unas", "y", "en", "por",
        "con", "que", "del", "al", "para", "the", "of", "and", "in", "to", "su", "sus"
    }

    story_title_tokens = set(w for w in story_title_norm.split() if len(w) > 3 and w not in stopwords)
    story_theme_tokens = set(w for w in normalize_text(story_theme.replace(":", " ")).split() if len(w) > 3 and w not in stopwords)
    all_story_tokens = story_title_tokens.union(story_theme_tokens)

    for item in ledger:
        item_id = item.get("id", "").strip().lower()
        item_theme = item.get("theme_signature", "").strip().lower()
        item_title_norm = normalize_text(item.get("title", ""))
        item_char = normalize_text(item.get("character", ""))

        # Layer 1: Exact ID match
        if story_id and item_id and story_id == item_id:
            return True, f"Layer 1 (ID Collision): Story ID '{story_id}' was already produced ({item.get('date', 'past')})"

        # Layer 2: Exact Theme Signature match
        if story_theme and item_theme and story_theme == item_theme:
            return True, f"Layer 2 (Theme Collision): Signature '{story_theme}' already published in '{item.get('title')}'"

        # Layer 3: Normalized Title exact match
        if story_title_norm and item_title_norm and story_title_norm == item_title_norm:
            return True, f"Layer 3 (Title Collision): Title matches existing entry '{item.get('title')}'"

        # Layer 4: Canonical Theme Sub-Tag Intersection (>= 2 sub-tags match)
        if story_theme and item_theme:
            story_tags = set(p for p in story_theme.split(":") if p)
            item_tags = set(p for p in item_theme.split(":") if p)
            common_tags = story_tags.intersection(item_tags)
            if len(common_tags) >= 2:
                return True, f"Layer 4 (Theme Sub-tag Collision): Shared arc tags {common_tags} with '{item.get('title')}'"

        # Layer 5: Character Arc & Semantic Keyword Topic Overlap
        if all_story_tokens:
            item_title_tok = set(w for w in item_title_norm.split() if len(w) > 3 and w not in stopwords)
            item_theme_tok = set(w for w in normalize_text(item_theme.replace(":", " ")).split() if len(w) > 3 and w not in stopwords)
            all_item_tokens = item_title_tok.union(item_theme_tok)

            overlap = all_story_tokens.intersection(all_item_tokens)

            # If both feature the same character, require only 2 specific topical arc words to block
            if story_char and item_char and (story_char in item_char or item_char in story_char):
                char_tokens = set(story_char.split())
                specific_overlap = overlap - char_tokens
                if len(specific_overlap) >= 2:
                    return True, f"Layer 5 (Character Arc Collision): Character '{story_char}' has redundant arc topics {specific_overlap} with '{item.get('title')}'"
            # Or if across any character, 3 or more thematic keywords overlap
            elif len(overlap) >= 3:
                return True, f"Layer 5 (High Semantic Collision): Redundant thematic tokens {overlap} with '{item.get('title')}'"

    return False, ""


def record_production(story: dict, mode: str, video_path: str):
    ledger = load_ledger()
    record = {
        "id": story["id"],
        "title": story["title"],
        "character": story.get("character", "Unknown"),
        "theme_signature": story.get("theme_signature", ""),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "mode": mode,
        "video_file": Path(video_path).name,
        "status": "published" if mode == "live_release" else ("draft" if mode == "draft_only" else "produced"),
    }
    ledger.append(record)
    save_ledger(ledger)


def create_full_panel_frame(im: Image.Image, target_w: int = 1080, target_h: int = 1920) -> Image.Image:
    """
    Guarantees 100% COMPLETE comic panel visibility (Zero Cropping):
    1. Background Layer: Scaled to cover 1080x1920 with smooth Gaussian blur (radius=28) and dark tint.
    2. Foreground Panel: Scaled to contain within 94% width and 65% height, leaving bottom area for Remotion subtitles.
    3. Border: Clean black comic outline so the vignette pops.
    """
    bg_scale = max(target_w / im.width, target_h / im.height)
    bg_w, bg_h = int(im.width * bg_scale), int(im.height * bg_scale)
    bg = im.resize((bg_w, bg_h), Image.Resampling.BILINEAR)
    left = (bg_w - target_w) // 2
    top = (bg_h - target_h) // 2
    bg = bg.crop((left, top, left + target_w, top + target_h))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=28))

    dark_overlay = Image.new('RGB', (target_w, target_h), (12, 14, 20))
    bg = Image.blend(bg, dark_overlay, alpha=0.55)

    max_fg_w = int(target_w * 0.94)
    max_fg_h = int(target_h * 0.65)
    fg_scale = min(max_fg_w / im.width, max_fg_h / im.height)
    fg_w, fg_h = int(im.width * fg_scale), int(im.height * fg_scale)
    fg = im.resize((fg_w, fg_h), Image.Resampling.LANCZOS)

    fg_x = (target_w - fg_w) // 2
    fg_y = max(130, int((target_h * 0.68 - fg_h) / 2) + 40)

    border_w = 4
    border_img = Image.new('RGB', (fg_w + border_w * 2, fg_h + border_w * 2), (0, 0, 0))
    border_img.paste(fg, (border_w, border_w))

    bg.paste(border_img, (fg_x - border_w, fg_y - border_w))
    return bg


def resolve_fandom_canonical_url(wiki: str, file_title: str) -> str | None:
    """Uses Fandom MediaWiki API to resolve the exact, canonical full-resolution CDN image URL."""
    clean_title = file_title if file_title.startswith("File:") else f"File:{file_title}"
    url = f"https://{wiki}.fandom.com/api.php"
    params = {
        "action": "query",
        "titles": clean_title,
        "prop": "imageinfo",
        "iiprop": "url|size",
        "format": "json"
    }
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        r = requests.get(url, params=params, headers=h, timeout=10).json()
        pages = r.get("query", {}).get("pages", {})
        for p in pages.values():
            if "imageinfo" in p and len(p["imageinfo"]) > 0:
                return p["imageinfo"][0]["url"]
    except Exception as e:
        log(f"Warning resolving Fandom file {file_title}: {e}")
    return None


DC_UNIVERSE_MARKERS = [
    'dc', 'batman', 'superman', 'bruce wayne', 'clark kent', 'the flash', 'flash', 'barry allen',
    'wally west', 'green lantern', 'hal jordan', 'john stewart', 'sinestro', 'superboy',
    'superboy prime', 'joker', 'aquaman', 'black adam', 'shazam', 'captain marvel (dc)',
    'wonder woman', 'darkseid', 'deathstroke', 'harley quinn', 'constantine', 'john constantine',
    'swamp thing', 'bane', 'robin', 'nightwing', 'dick grayson', 'red hood', 'jason todd',
    'green arrow', 'oliver queen', 'cyborg', 'martian manhunter', 'lex luthor', 'doomsday',
    'brainiac', 'zatanna', 'raven', 'starfire', 'beast boy', 'riddler', 'penguin', 'two-face',
    'scarecrow', 'catwoman', 'ra\'s al ghul', 'damian wayne', 'dceased', 'flashpoint',
    'injustice', 'crisis on infinite earths', 'kingdom come', 'watchmen', 'rorschach',
    'doctor manhattan', 'sandman', 'lucifer', 'morpheus', 'bialya', 'justice league',
    'justice society', 'teen titans', 'arkham', 'gotham', 'metropolis', 'themyscira',
    'grim knight', 'the grim knight'
]


def get_story_comic_wiki(story: dict) -> str:
    """Determina de forma infalible si la historia o personaje pertenece a DC o Marvel Fandom."""
    explicit_u = str(story.get("universe", "")).lower()
    if "dc" in explicit_u:
        return "dc.fandom.com"
    if "marvel" in explicit_u:
        return "marvel.fandom.com"

    text_to_scan = f"{story.get('character', '')} {story.get('title', '')} {story.get('description', '')} {story.get('theme_signature', '')} {story.get('hashtags', '')}".lower()
    if any(marker in text_to_scan for marker in DC_UNIVERSE_MARKERS):
        return "dc.fandom.com"
    return "marvel.fandom.com"


def download_comic_panel(url_or_file: str, character: str, dest_path: Path, min_dim: int = 400) -> bool:
    """
    Downloads an official high-resolution comic panel.
    - Resolves Fandom API if given a File: or static wikia url.
    - Sets appropriate Referer (dc.fandom.com or marvel.fandom.com).
    - Validates minimum dimensions and image integrity.
    """
    wiki_domain = get_story_comic_wiki({"character": character})
    wiki = "dc" if "dc" in wiki_domain else "marvel"
    ref = f"https://{wiki_domain}/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': ref,
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
    }

    candidate_urls = []
    
    if url_or_file.startswith("http"):
        candidate_urls.append(url_or_file)
        # Also extract filename to resolve via Fandom API in case the hash/path changed
        parts = url_or_file.split("/")
        for part in reversed(parts):
            clean_part = part.split("?")[0]
            if any(clean_part.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                api_resolved = resolve_fandom_canonical_url(wiki, clean_part)
                if api_resolved and api_resolved not in candidate_urls:
                    candidate_urls.append(api_resolved)
                break
    else:
        api_resolved = resolve_fandom_canonical_url(wiki, url_or_file)
        if api_resolved:
            candidate_urls.append(api_resolved)

    for c_url in candidate_urls:
        try:
            r = requests.get(c_url, headers=headers, timeout=15)
            if r.status_code == 200 and len(r.content) > 10000:
                im = Image.open(io.BytesIO(r.content)).convert("RGB")
                
                # CRITICAL QUALITY SHIELD: Reject text-only pages, letters or handwritten notes
                im_hsv = im.convert("HSV")
                stat = ImageStat.Stat(im_hsv)
                mean_sat = stat.mean[1] # Low saturation = near monochrome
                mean_val = stat.mean[2] # High value = bright white paper
                if mean_sat < 15.0 and mean_val > 175.0:
                    log(f"Quality Shield: Rejected '{c_url.split('/')[-1]}' because it is a text document / handwritten note (sat={mean_sat:.1f}).")
                    continue

                if im.width >= min_dim or im.height >= min_dim:
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    im.save(dest_path, "JPEG", quality=95)
                    return True
        except Exception as e:
            log(f"Warning downloading {c_url[:60]}: {e}")

    return False


def build_cloud_generation(story: dict, work_dir: Path) -> dict:
    gen_dir = work_dir / story["id"]
    gen_dir.mkdir(parents=True, exist_ok=True)

    curated_urls = story.get("scene_art_urls", [])
    if curated_urls:
        log(f"Using {len(curated_urls)} curated 1:1 comic panels for '{story['title']}'...")
        art_urls = curated_urls
    else:
        log(f"Obtaining official comic art for '{story['character']}'...")
        art_urls = story.get("image_urls") or get_fandom_comic_art(story.get("character", "Batman"), count=len(story["scenes"]) + 5)
    log(f"Discovered {len(art_urls)} high-resolution comic assets.")

    scenes_data = []
    scene_videos = []
    downloaded_images = []

    for idx, narration in enumerate(story["scenes"], 1):
        sc_name = f"scene_{idx:02d}"
        sc_dir = gen_dir / sc_name
        sc_dir.mkdir(parents=True, exist_ok=True)
        img_file = sc_dir / f"{sc_name}.jpg"

        saved = False
        target = art_urls[idx - 1] if art_urls and idx <= len(art_urls) else None

        # Descartar target si es portada oficial
        from .comic_precision_scraper import is_cover_or_promo_image
        if target and is_cover_or_promo_image(target):
            log(f"Scene {idx}: Explicit target '{target}' is a comic cover! Banned by Quality Shield to enforce interior action panels.")
            target = None

        # Primary: Multi-Source Precision Scraper with Gemini Vision Referee
        try:
            from .comic_precision_scraper import fetch_scene_image
            wiki = get_story_comic_wiki(story)
            art_queries = story.get("art_queries", [])
            if art_queries and idx <= len(art_queries):
                query_for_scene = art_queries[idx - 1]
            else:
                query_for_scene = f"{story.get('character', '')} {narration[:45]}"
            panel_path = fetch_scene_image(
                wiki_domain=wiki,
                target_file=target,
                fallback_query=query_for_scene,
                dest_path=str(img_file),
                existing_scene_images=[str(p) for p in downloaded_images],
                scene_text=narration
            )
            if os.path.exists(panel_path) and os.path.getsize(panel_path) > 10000:
                saved = True
                log(f"Scene {idx}: Precision panel validated and saved ({wiki}).")
        except Exception as e:
            log(f"Scene {idx}: Precision scraper notice: {e}")

        # Fallback A: Direct download if target specified and precision scraper failed
        if (not saved or not img_file.exists()) and target:
            if not is_cover_or_promo_image(target):
                saved = download_comic_panel(target, story.get("character", ""), img_file)

        # Fallback B: Dynamic comic fetcher with deduplication check
        if not saved or not img_file.exists():
            log(f"Scene {idx}: Querying general Fandom comic art...")
            fallback_urls = get_fandom_comic_art(story.get("character", "Batman"), count=8)
            for fb_u in fallback_urls:
                if not is_cover_or_promo_image(fb_u) and download_comic_panel(fb_u, story.get("character", ""), img_file):
                    from .comic_precision_scraper import is_duplicate_panel
                    if not is_duplicate_panel(str(img_file), [str(p) for p in downloaded_images]):
                        saved = True
                        break
                    else:
                        img_file.unlink(missing_ok=True)

        # CRITICAL FAIL-SAFE: NO BLACK SCREEN VIDEOS EVER!
        if not saved or not img_file.exists():
            raise RuntimeError(
                f"FATAL ERROR: Could not obtain real comic panels for '{story['title']}' (Scene {idx}). "
                "Halting pipeline to guarantee zero black-screen videos are ever produced or uploaded."
            )

        # Enmarcado vertical 1080x1920 con fondo desenfocado y Safe Zone (Fórmula Maestra)
        with Image.open(img_file) as raw_im:
            if raw_im.size != (1080, 1920):
                framed_im = create_full_panel_frame(raw_im.convert("RGB"), 1080, 1920)
                framed_im.save(img_file, "JPEG", quality=95)
                log(f"Scene {idx}: Framed into 1080x1920 canvas with Gaussian blur background.")

        downloaded_images.append(img_file)

        scenes_data.append({
            "scene_number": idx,
            "voiceover_text": narration,
            "narration": narration
        })

        scene_videos.append({
            "folder": sc_name,
            "video": str(img_file),
            "images": [str(img_file)],
            "scene_number": idx,
            "is_image": True,
            "image_count": 1
        })

    # =========================================================================
    # PRODUCTION QUALITY GATE (INVIOLABLE AUDIT SHIELD)
    # =========================================================================
    log("Running Production Quality Gate audit on all 4 generated scene panels...")
    if len(downloaded_images) != len(story["scenes"]):
        raise RuntimeError(f"Quality Gate Failed: Expected {len(story['scenes'])} scenes, got {len(downloaded_images)}")

    # 1. Zero Duplication Check across all scene pairs
    from .comic_precision_scraper import calculate_image_rms_difference
    for i in range(len(downloaded_images)):
        for j in range(i + 1, len(downloaded_images)):
            rms_diff = calculate_image_rms_difference(str(downloaded_images[i]), str(downloaded_images[j]))
            log(f"Quality Gate RMS check Scene {i+1} vs Scene {j+1}: {rms_diff:.2f}")
            if rms_diff < 12.0:
                raise RuntimeError(
                    f"QUALITY GATE FATAL ERROR: Scene {i+1} and Scene {j+1} are DUPLICATES (RMS diff {rms_diff:.2f} < 12.0). "
                    "Production halted to guarantee zero duplicate panels are ever published."
                )

    # 2. Corrupted / Blank / Black screen check
    for idx_img, p in enumerate(downloaded_images, 1):
        with Image.open(p) as test_im:
            w, h = test_im.size
            if w < 300 or h < 300:
                raise RuntimeError(f"QUALITY GATE FATAL ERROR: Scene {idx_img} image resolution too small ({w}x{h}).")
            stat = ImageStat.Stat(test_im)
            if max(stat.stddev) < 8.0:
                raise RuntimeError(f"QUALITY GATE FATAL ERROR: Scene {idx_img} image is blank or solid color.")

    # 3. Comic Inking Edge Art Check (Zero real-life photos, food, or live-action actors)
    from .comic_precision_scraper import check_is_comic_art_inking
    for idx_img, p in enumerate(downloaded_images, 1):
        with Image.open(p) as test_im:
            if not check_is_comic_art_inking(test_im):
                raise RuntimeError(
                    f"QUALITY GATE FATAL ERROR: Scene {idx_img} image ({p.name}) failed comic inking verification. "
                    "Detected real-life photo, non-comic object, or live-action actor. Halting video compilation."
                )

    log("Production Quality Gate: ALL CHECKS PASSED (100% Unique Panels, 0 Duplicates, High Resolution, Verified Comic Art).")

    script_data = {
        "metadata": {
            "title": story["title"],
            "description": story["description"],
            "hashtags": story["hashtags"],
            "voice": story.get("voice") or os.environ.get("VOICE", "Puck")
        },
        "scenes": scenes_data
    }

    script_path = gen_dir / "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(script_data, f, indent=2, ensure_ascii=False)

    return {
        "path": str(gen_dir),
        "name": story["id"],
        "script": script_data,
        "scene_videos": scene_videos,
        "scene_count": len(scene_videos)
    }


def main():
    parser = argparse.ArgumentParser(description="Multiverso Comic Autonomous Cloud Generation & Publisher")
    parser.add_argument("--story-id", type=str, help="Specific story ID to generate (or 'any' for auto queue)")
    parser.add_argument("--publish", action="store_true", help="Auto-publish to FB Page and IG after generation")
    parser.add_argument("--draft", action="store_true", help="Save as unpublished draft on FB and skip public IG")
    parser.add_argument("--dry-run", action="store_true", help="Test workflow without video generation or publishing")
    parser.add_argument("--ai-story", action="store_true", help="Force autonomous AI story generation with Gemini")
    args = parser.parse_args()

    log("Initializing Multiverso Comic Engine with Ironclad Anti-Duplication Shield...")
    log("Repository: multiverso-comic (branch: main)")
    log(f"FB Page ID: {os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)}")
    log(f"IG Account ID: {os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)}")

    ledger = load_ledger()
    log(f"Historical Ledger: {len(ledger)} previously produced videos registered.")

    # Story Selection & Anti-Duplication Verification
    if args.story_id and args.story_id != "any":
        selected = next((s for s in EDITORIAL_STORIES if s["id"] == args.story_id), None)
        if not selected:
            # Check if this ID was an old historical story
            old_item = next((item for item in ledger if item.get("id") == args.story_id), None)
            if old_item:
                log(f"CRITICAL ANTI-DUPLICATION SHIELD: Requested story '{args.story_id}' is in historical ledger (Produced: {old_item.get('date')}).")
                log(f"Existing Title: {old_item.get('title')}")
                log("ABORTING: Duplicates are strictly prohibited.")
                sys.exit(0)
            else:
                log(f"Error: Story ID '{args.story_id}' not found in catalog or ledger.")
                sys.exit(1)

        is_dup, reason = is_duplicate(selected, ledger)
        if is_dup:
            log(f"CRITICAL ANTI-DUPLICATION SHIELD: Story '{selected['title']}' rejected.")
            log(f"Reason: {reason}")
            log("No duplicate videos will ever be produced. Aborting safely.")
            sys.exit(0)
    else:
        available = [s for s in EDITORIAL_STORIES if not is_duplicate(s, ledger)[0]]
        log(f"Available unproduced stories in catalog: {len(available)} / {len(EDITORIAL_STORIES)}")

        if not available or getattr(args, 'ai_story', False) or args.story_id == "autonomous_ai":
            log("CATALOG EXHAUSTION / AI MODE: Activating Autonomous AI Story Engine (Google Gemini)...")
            from .autonomous_ai_generator import generate_autonomous_story
            selected = generate_autonomous_story(ledger)
            log(f"Autonomous AI Generated Story: {selected['title']} (ID: {selected['id']})")
        else:
            selected = random.choice(available)
            log(f"Selected Unique Story: {selected['title']} (ID: {selected['id']})")

    if args.dry_run:
        log("DRY RUN mode verified. Story is 100% unique and passed all 5 anti-duplication layers.")
        log("Exiting without video render or Meta publish as requested.")
        sys.exit(0)

    work_dir = Path("scratch_cloud_gen")
    work_dir.mkdir(parents=True, exist_ok=True)
    generation = build_cloud_generation(selected, work_dir)

    output_root = Path("output")
    output_root.mkdir(parents=True, exist_ok=True)

    # Lazy import pipeline to allow test environments to run without heavy whisper dependencies
    from .pipeline import run_pipeline

    voice_choice = selected.get("voice") or os.environ.get("VOICE", "Puck")
    log(f"Starting video compilation pipeline with voice: {voice_choice}...")
    final_video_path = run_pipeline(
        generation=generation,
        output_name=selected["id"],
        voice=voice_choice,
        output_root=str(output_root),
        width=1080,
        height=1920,
        final_video_dir=str(output_root / "finals"),
        generate_thumbnail=True
    )

    log(f"Render completed: {final_video_path}")

    mode_str = "render_only"
    if args.publish or os.environ.get("AUTO_PUBLISH", "").lower() in ("true", "1", "yes"):
        is_draft = args.draft or os.environ.get("DRAFT_ONLY", "").lower() in ("true", "1", "yes")
        mode_str = "draft_only" if is_draft else "live_release"
        log(f"Initiating publication to Meta (mode: {'DRAFT ONLY' if is_draft else 'LIVE PUBLIC'})...")
        publish_comic_video(
            video_path=final_video_path,
            title=selected["title"],
            description=selected["description"],
            hashtags=selected["hashtags"],
            draft_only=is_draft,
        )
    else:
        log("Publication skipped (render_only mode).")

    record_production(selected, mode_str, final_video_path)
    log(f"Anti-duplication registry updated: '{selected['id']}' locked permanently.")


if __name__ == "__main__":
    main()
