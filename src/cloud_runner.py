"""
Comic Lore Vault - Autonomous Cloud Video Runner & Publisher
Designed for GitHub Actions CI/CD workflows and local CLI execution.
Brand: Comic Lore Vault (@comicloreevault)
"""

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

from .comic_fetcher import get_fandom_comic_art
from .pipeline import run_pipeline
from .publisher import publish_comic_video, DEFAULT_PAGE_ID, DEFAULT_IG_USER_ID

EDITORIAL_STORIES = [
    {
        "id": "under_the_red_hood",
        "character": "Batman",
        "title": "Batman: Under the Red Hood - The Return of Jason Todd",
        "description": "The explosive tragedy of Batman confronting his greatest failure: the resurrection of Jason Todd as the brutal vigilante Red Hood.",
        "hashtags": "#Batman #RedHood #JasonTodd #Joker #DCComics #ComicLoreVault #ComicTok #Reels",
        "scenes": [
            "In Gotham City, a ruthless new crime lord emerged from the shadows, seizing total control of the underworld under the identity of the Red Hood.",
            "Batman tracked the elusive vigilante across the Gotham skyline, stunned by his opponent's intimate knowledge of Wayne Enterprises gear and combat tactics.",
            "During an intense rooftop confrontation, the Red Hood severed his mask, revealing the impossible: Jason Todd, the second Robin, beaten to death by Joker years ago.",
            "Jason dragged Batman into a rundown apartment where a bloody Joker sat tied to a chair with a crowbar lying on the table.",
            "Tears in his eyes, Jason forced Batman to choose: kill the Joker to avenge him, or watch Jason pull the trigger himself.",
            "Refusing to cross his moral line, Batman disarmed Jason with a batarang, triggering a hidden bomb that leveled the building as Jason vanished into the smoke."
        ]
    },
    {
        "id": "death_of_superman",
        "character": "Superman",
        "title": "The Death of Superman - The Last Stand Against Doomsday",
        "description": "The day the Man of Steel gave his life to protect Metropolis from the unstoppable cosmic monster Doomsday.",
        "hashtags": "#Superman #Doomsday #DeathOfSuperman #JusticeLeague #DCComics #ComicLoreVault #ComicTok #Reels",
        "scenes": [
            "An unstoppable prehistoric behemoth named Doomsday clawed his way to Earth's surface, carving a catastrophic path of ruin toward Metropolis.",
            "The Justice League engaged the rampaging beast, only to be systematically incapacitated in seconds by Doomsday's unimaginable raw power.",
            "Recognizing the existential threat, Superman stood alone before the Daily Planet globe, absorbing devastating strikes that tore his invulnerable suit to shreds.",
            "Bleeding and exhausted, the Man of Steel dug his heels into the cratered pavement, realizing only absolute lethal force could halt the monster.",
            "With their final ounce of strength, Superman and Doomsday delivered simultaneous earth-shattering blows, snapping the creature's neck as shockwaves leveled the plaza.",
            "Doomsday collapsed dead, and Superman fell into Lois Lane's trembling arms, drawing his final breath as a weeping Metropolis mourned its greatest savior."
        ]
    },
    {
        "id": "infinity_gauntlet",
        "character": "Thanos",
        "title": "The Infinity Gauntlet - The Snap That Erased the Universe",
        "description": "Thanos the Mad Titan unites all six Infinity Stones and brings Marvel heroes to their absolute knees.",
        "hashtags": "#Thanos #InfinityGauntlet #Marvel #Avengers #ComicLoreVault #MarvelComics #Shorts #Reels",
        "scenes": [
            "Driven by a twisted romance to impress Lady Death, the Mad Titan Thanos forged the golden Infinity Gauntlet with all six cosmic stones.",
            "Hovering in deep space with gods and cosmic entities bound at his feet, Thanos raised his hand and snapped his fingers with chilling detachment.",
            "In an instant, half of all living souls across the universe disintegrated into silent ash, shattering families and planets into pandemonium.",
            "Earth's surviving Avengers, led by Captain America and Silver Surfer, mounted a desperate assault on Thanos' cosmic shrine.",
            "One by one, Earth's mightiest champions fell before reality-warping power: Thor turned to glass, Wolverine's adamantium melted, and Cap stood alone.",
            "Even facing universal oblivion, Steve Rogers stared down the Mad Titan with unwavering defiance, cementing the indelible spirit of the Marvel heroes."
        ]
    }
]


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [CloudRunner] {msg}", flush=True)


def build_cloud_generation(story: dict, work_dir: Path) -> dict:
    """Creates a local generation folder with downloaded comic panels and script.json."""
    gen_dir = work_dir / story["id"]
    gen_dir.mkdir(parents=True, exist_ok=True)

    log(f"Fetching comic art for character: {story['character']}...")
    try:
        art_urls = get_fandom_comic_art(story["character"], count=len(story["scenes"]) + 4)
    except Exception as e:
        log(f"Warning fetching art via Fandom: {e}")
        art_urls = []

    scenes_data = []
    scene_videos = []

    import requests
    from PIL import Image
    import io

    for idx, narration in enumerate(story["scenes"], start=1):
        sc_name = f"Escena_{idx:02d}"
        sc_dir = gen_dir / sc_name
        sc_dir.mkdir(parents=True, exist_ok=True)
        img_file = sc_dir / "imagen_01.jpg"

        # Download art or create high-contrast comic backdrop
        saved = False
        if idx - 1 < len(art_urls):
            try:
                r = requests.get(art_urls[idx - 1], timeout=10)
                if r.status_code == 200:
                    with open(img_file, "wb") as f:
                        f.write(r.content)
                    saved = True
            except Exception:
                saved = False

        if not saved or not img_file.exists():
            # Fallback high-contrast dark visual panel
            im = Image.new("RGB", (1080, 1920), color=(15, 18, 25))
            im.save(img_file, quality=92)

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

    script_data = {
        "metadata": {
            "title": story["title"],
            "description": story["description"],
            "hashtags": story["hashtags"],
            "voice": "en-US-Studio-Q"
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
    parser = argparse.ArgumentParser(description="Comic Lore Vault Autonomous Cloud Generation & Publisher")
    parser.add_argument("--story-id", type=str, help="Specific story ID to generate")
    parser.add_argument("--publish", action="store_true", help="Auto-publish to FB Page and IG after generation")
    parser.add_argument("--draft", action="store_true", help="Save as unpublished draft on FB and skip public IG (safe pre-launch verification)")
    parser.add_argument("--dry-run", action="store_true", help="Test workflow without video generation or publishing")
    args = parser.parse_args()

    log("Initializing Comic Lore Vault Cloud Engine...")
    log(f"Brand: Comic Lore Vault (@comicloreevault)")
    log(f"FB Page ID: {os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)}")
    log(f"IG Account ID: {os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)}")

    # Pick story
    if args.story_id:
        selected = next((s for s in EDITORIAL_STORIES if s["id"] == args.story_id), None)
        if not selected:
            log(f"Error: Story ID '{args.story_id}' not found.")
            sys.exit(1)
    else:
        selected = random.choice(EDITORIAL_STORIES)

    log(f"Selected Story: {selected['title']}")

    if args.dry_run:
        log("DRY RUN mode enabled. Verification successful. Exiting without render.")
        sys.exit(0)

    work_dir = Path("scratch_cloud_gen")
    work_dir.mkdir(parents=True, exist_ok=True)
    generation = build_cloud_generation(selected, work_dir)

    output_root = Path("output")
    output_root.mkdir(parents=True, exist_ok=True)

    log("Starting video compilation pipeline...")
    final_video_path = run_pipeline(
        generation=generation,
        output_name=selected["id"],
        voice="en-US-Studio-Q",
        output_root=str(output_root),
        final_video_dir=str(output_root / "finals")
    )

    log(f"Render completed: {final_video_path}")

    # Publish if requested
    if args.publish or os.environ.get("AUTO_PUBLISH", "").lower() in ("true", "1", "yes"):
        is_draft = args.draft or os.environ.get("DRAFT_ONLY", "").lower() in ("true", "1", "yes")
        log(f"Initiating publication to Comic Lore Vault (mode: {'DRAFT ONLY' if is_draft else 'LIVE PUBLIC'})...")
        publish_comic_video(
            video_path=final_video_path,
            title=selected["title"],
            description=selected["description"],
            hashtags=selected["hashtags"],
            draft_only=is_draft,
        )
    else:
        log("Publication skipped (set --publish or AUTO_PUBLISH=true to publish).")


if __name__ == "__main__":
    main()
