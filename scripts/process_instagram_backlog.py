import os
import sys
import json
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Ensure root in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.publisher import publish_to_instagram_reels

BACKLOG_FILE = Path(__file__).resolve().parent.parent / "instagram_backlog_items.json"
LEDGER_FILE = Path(__file__).resolve().parent.parent / "published_ledger.json"

LOCAL_TZ = timezone(timedelta(hours=-5))

def log(msg: str):
    now_str = datetime.now(LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now_str} -05:00] [IG Backlog] {msg}", flush=True)

def load_data():
    if not BACKLOG_FILE.exists():
        log(f"ERROR: Backlog file not found: {BACKLOG_FILE}")
        return [], []
    with open(BACKLOG_FILE, "r", encoding="utf-8") as f:
        backlog = json.load(f)
    ledger = []
    if LEDGER_FILE.exists():
        with open(LEDGER_FILE, "r", encoding="utf-8") as f:
            ledger = json.load(f)
    return backlog, ledger

def save_data(backlog, ledger):
    with open(BACKLOG_FILE, "w", encoding="utf-8") as f:
        json.dump(backlog, f, indent=2, ensure_ascii=False)
    with open(LEDGER_FILE, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)

def push_github_update():
    """If running in GitHub Actions, commit and push changes."""
    if os.environ.get("GITHUB_ACTIONS"):
        log("Running in GitHub Actions environment. Committing backlog and ledger...")
        import subprocess
        try:
            subprocess.run(["git", "config", "user.name", "ComicLoreVault Engine"], check=True)
            subprocess.run(["git", "config", "user.email", "Lorecomicvault@users.noreply.github.com"], check=True)
            subprocess.run(["git", "add", str(BACKLOG_FILE), str(LEDGER_FILE)], check=True)
            subprocess.run(["git", "commit", "-m", "chore(instagram): registrar publicacion de reel del backlog [skip ci]"], check=True)
            for _ in range(3):
                res = subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=False)
                res_push = subprocess.run(["git", "push", "origin", "main"], check=False)
                if res.returncode == 0 and res_push.returncode == 0:
                    log("SUCCESS: Pushed update to origin/main.")
                    break
                time.sleep(3)
        except Exception as e:
            log(f"Warning committing to GitHub Actions: {e}")

def publish_item(item, backlog, ledger):
    slot = item["slot"]
    title = item["title"]
    desc = item["description"]
    tags = item["hashtags"]
    video_url = item["video_url"]
    caption = f"{title}\n\n{desc}\n\n{tags}".strip()

    log("=" * 60)
    log(f"PUBLISHING SLOT {slot}: '{title}' to Instagram Reels...")
    log(f"Video URL: {video_url}")
    log("=" * 60)

    res = publish_to_instagram_reels(
        video_url=video_url,
        caption=caption,
        thumb_offset_ms=2500
    )

    if res.get("success"):
        permalink = res.get("permalink")
        log(f"SUCCESS! Slot {slot} published to Instagram! URL: {permalink}")
        item["status"] = "published"
        item["published_at"] = datetime.now(LOCAL_TZ).isoformat()
        item["instagram_url"] = permalink

        # Update ledger
        for e in ledger:
            if e.get("id") == item["id"]:
                if "social_links" not in e:
                    e["social_links"] = {}
                e["social_links"]["instagram"] = permalink

        save_data(backlog, ledger)
        push_github_update()
        return True
    else:
        log(f"ERROR publishing Slot {slot}: {res}")
        return False

def run_single_due_check():
    """Finds the next item that is due (scheduled_at <= now) and publishes it."""
    backlog, ledger = load_data()
    now_local = datetime.now(LOCAL_TZ)

    for item in backlog:
        slot_id = item["id"]
        # Double check if ledger already has it
        ledger_entry = next((e for e in ledger if e.get("id") == slot_id), None)
        if ledger_entry and ledger_entry.get("social_links", {}).get("instagram"):
            item["status"] = "published"
            item["instagram_url"] = ledger_entry["social_links"]["instagram"]
            continue

        if item.get("status") == "published":
            continue

        sched_dt = datetime.fromisoformat(item["scheduled_at"])
        if now_local >= sched_dt:
            log(f"Item Slot {item['slot']} is due for publication (scheduled: {sched_dt}, current: {now_local})")
            return publish_item(item, backlog, ledger)
        else:
            diff = (sched_dt - now_local).total_seconds()
            log(f"Next due item is Slot {item['slot']} at {sched_dt} (in {diff/3600:.2f} hours). Nothing to publish now.")
            return True

    log("All backlog items are already published! Nothing to do.")
    return True

def run_continuous_daemon():
    """Runs a persistent daemon that waits for each scheduled slot and publishes on time."""
    log("Starting persistent Instagram Backlog Daemon...")
    while True:
        backlog, ledger = load_data()
        now_local = datetime.now(LOCAL_TZ)
        next_item = None

        for item in backlog:
            slot_id = item["id"]
            ledger_entry = next((e for e in ledger if e.get("id") == slot_id), None)
            if ledger_entry and ledger_entry.get("social_links", {}).get("instagram"):
                item["status"] = "published"
                item["instagram_url"] = ledger_entry["social_links"]["instagram"]
                continue

            if item.get("status") != "published":
                next_item = item
                break

        if not next_item:
            log("ALL BACKLOG ITEMS HAVE BEEN PUBLISHED! Daemon exiting with mission accomplished.")
            break

        sched_dt = datetime.fromisoformat(next_item["scheduled_at"])
        delay = (sched_dt - now_local).total_seconds()

        if delay > 0:
            log(f"Next item to publish: Slot {next_item['slot']} ('{next_item['title'][:40]}...').")
            log(f"Waiting {delay:.0f}s ({delay/3600:.2f} hours) until {sched_dt.strftime('%Y-%m-%d %H:%M:%S')}...")
            # Sleep in chunks to allow responsive logging
            while delay > 0:
                sleep_chunk = min(delay, 300)
                time.sleep(sleep_chunk)
                now_local = datetime.now(LOCAL_TZ)
                delay = (sched_dt - now_local).total_seconds()

        # Due now: publish!
        log(f"Time reached! Publishing Slot {next_item['slot']} now...")
        success = publish_item(next_item, backlog, ledger)
        if not success:
            log("Retrying once in 60s...")
            time.sleep(60)
            publish_item(next_item, backlog, ledger)

        # Brief pause between iterations
        time.sleep(10)

if __name__ == "__main__":
    if "--daemon" in sys.argv:
        run_continuous_daemon()
    else:
        run_single_due_check()
