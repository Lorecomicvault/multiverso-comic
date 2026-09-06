"""
Comic Lore Vault - Autonomous Cloud Video Runner & Publisher
Anti-Duplication Engine: Guarantees zero repeated stories, characters arcs, or themes.
Brand: Comic Lore Vault (@comicloreevault)
"""

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

from .comic_fetcher import get_fandom_comic_art
from .pipeline import run_pipeline
from .publisher import publish_comic_video, DEFAULT_PAGE_ID, DEFAULT_IG_USER_ID

LEDGER_PATH = Path("published_ledger.json")

EDITORIAL_STORIES = [
    {
        "id": "batman_under_the_red_hood",
        "character": "Batman",
        "title": "Batman: Under the Red Hood - The Resurrection of Jason Todd",
        "theme_signature": "batman:red_hood:jason_todd_resurrection",
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
        "id": "batman_court_of_owls",
        "character": "Batman",
        "title": "Batman: The Court of Owls - Gotham's Dark Secret",
        "theme_signature": "batman:court_of_owls:talon_labyrinth",
        "description": "Batman discovers an ancient society that has controlled Gotham City from the shadows for centuries.",
        "hashtags": "#Batman #CourtOfOwls #Gotham #DCComics #ComicLoreVault #ComicBooks #Reels",
        "scenes": [
            "For generations, Gotham children whispered a nursery rhyme about the Court of Owls, an elite shadowy cabal rumored to govern the city in secret.",
            "Bruce Wayne always dismissed the legend as gothic folklore, until an immortal assassin called a Talon targeted him for public execution.",
            "Investigating their subterranean lairs, Batman plunged into an enormous subterranean labyrinth hidden deep beneath the bedrock of Gotham City.",
            "Trapped without food or water for eight torturous days, Bruce's psyche shattered as the Court watched his descent into madness from mirrored balconies.",
            "Just as the Talons moved in for the kill, Batman summoned the raw fury of his willpower, battling through dozens of undead assassins to break free.",
            "Escaping back to Wayne Manor, Bruce prepared for total war, unleashing heavy mechanised armor to reclaim the city from its ancient masters."
        ]
    },
    {
        "id": "flashpoint_thomas_wayne",
        "character": "Batman",
        "title": "Flashpoint: The Darker Knight - Thomas Wayne's Vengeance",
        "theme_signature": "flashpoint:thomas_wayne:letter_to_bruce",
        "description": "In an alternate timeline where Bruce died in Crime Alley, Thomas Wayne became a ruthless, lethal Batman.",
        "hashtags": "#Flashpoint #Batman #ThomasWayne #TheFlash #DCComics #ComicLoreVault #Shorts #Reels",
        "scenes": [
            "When Barry Allen shattered time to save his mother, he woke in a nightmare world where Bruce Wayne died in that dark alley instead.",
            "Consummed by sorrow, Thomas Wayne forged himself into a brutal Batman who dual-wielded twin firearms and executed Gotham's worst monsters without hesitation.",
            "Even more horrifying, Martha Wayne collapsed into madness over Bruce's death, slicing her own face into a grotesque grin to become this world's Joker.",
            "When Flash revealed the original timeline where Bruce lived to become Batman, Thomas dedicated everything to helping Barry restore reality.",
            "As the world burned in the apocalyptic war between Atlantis and Themyscira, Thomas sacrificed his life to buy Barry the precious seconds needed to run.",
            "Before dying, Thomas handed Barry a handwritten letter for Bruce, carrying a father's eternal love across the fractured multiverse."
        ]
    },
    {
        "id": "joker_killing_joke",
        "character": "Joker",
        "title": "The Joker: The Killing Joke - One Bad Day",
        "theme_signature": "joker:killing_joke:one_bad_day",
        "description": "The Joker's psychotic crusade to prove that all it takes is one bad day to drive the sanest man alive completely insane.",
        "hashtags": "#Joker #Batman #TheKillingJoke #DCComics #ComicLoreVault #DarkKnight #Reels",
        "scenes": [
            "Escaping Arkham Asylum once again, the Joker set out to prove his most twisted philosophical theory: sanity is just a fragile illusion waiting to shatter.",
            "Arriving unexpectedly at Barbara Gordon's apartment, Joker shot her point-blank through the spine, permanently paralyzing the young hero.",
            "He abducted Commissioner Gordon to an abandoned carnival, subjecting Jim to psychological torture designed to break his rational mind.",
            "Yet despite the horrors, Gordon refused to break, commanding Batman to bring the Joker in by the book to prove the law still stood.",
            "Tracking the clown through the hall of mirrors, Batman cornered the Joker, offering him one final chance at genuine rehabilitation.",
            "Joker solemnly declined with a tragic joke about two lunatics, and in the pouring rain, Batman and Joker shared a haunting, chilling laugh."
        ]
    },
    {
        "id": "injustice_superman_fall",
        "character": "Superman",
        "title": "Injustice: The Day Superman Lost Everything",
        "theme_signature": "superman:injustice:metropolis_nuke",
        "description": "The catastrophic tragedy that turned the world's greatest protector into Earth's most ruthless dictator.",
        "hashtags": "#Injustice #Superman #Batman #Joker #DCComics #ComicLoreVault #ComicTok #Reels",
        "scenes": [
            "Tired of losing to Batman, the Joker migrated to Metropolis with a horrific master plan aimed directly at the Man of Steel.",
            "Using Scarecrow's fear toxin laced with Kryptonite, Joker tricked Superman into believing he was battling the cosmic monster Doomsday.",
            "Flying the beast into the vacuum of space, the hallucination dissipated, and Clark looked down in sheer horror to find he had killed his pregnant wife, Lois Lane.",
            "Tied to Lois's heartbeat, a hidden nuclear warhead detonated instantly, vaporizing Metropolis into a smoking radioactive crater.",
            "Broken beyond repair, Superman flew into the police interrogation room and impaled the laughing Joker through his chest before Batman's eyes.",
            "From that ashes of grief rose the High Councillor, establishing a global tyrannical regime that pitted superhero against superhero forever."
        ]
    },
    {
        "id": "green_lantern_blackest_night",
        "character": "Green Lantern",
        "title": "Green Lantern: Blackest Night - The Dead Shall Rise",
        "theme_signature": "green_lantern:blackest_night:nekron",
        "description": "The cosmic prophecy fulfilled as black power rings raise fallen DC heroes from the dead to extinguish all life in the universe.",
        "hashtags": "#GreenLantern #BlackestNight #HalJordan #DCComics #ComicLoreVault #Zombies #Reels",
        "scenes": [
            "Across the cosmic sectors, an ancient prophecy echoed: the dead would rise, and the blackest night would swallow every spark of life.",
            "Raining down like obsidian hail, millions of Black Lantern rings desecrated graves across Earth and the cosmos, reanimating fallen heroes and villains.",
            "Hal Jordan and the surviving heroes faced the ghastly, rotting corpses of their loved ones, weaponizing pure emotional trauma to harvest their hearts.",
            "From the shadow realm emerged Nekron, the cosmic lord of the unliving, executing the Guardian of the Universe to snuff out the emotional spectrum.",
            "Uniting all seven lantern colors from will and fear to hope and rage, Hal channeled the celestial White Entity of creation.",
            "A burst of immaculate white light washed over existence, destroying the black lanterns and restoring life to the fallen champions."
        ]
    },
    {
        "id": "thor_god_butcher",
        "character": "Thor",
        "title": "Thor: The God Butcher - Gorr's Vow of Annihilation",
        "theme_signature": "thor:gorr:god_butcher_all_black",
        "description": "Gorr the God Butcher bonds with the All-Black Necrosword and embarks on a three-thousand-year crusade to massacre all deities.",
        "hashtags": "#Thor #Gorr #GodButcher #MarvelComics #ComicLoreVault #Avengers #Reels",
        "scenes": [
            "On a barren, dying planet, a mortal named Gorr watched his entire family starve while the gods he prayed to never answered.",
            "When two wounded gods crashed before him, Gorr bonded with the All-Black Necrosword, making a blood vow to butcher every deity in the cosmos.",
            "Millennia later, Thor discovered entire pantheons floating dead through space, their golden palaces soaked in silent darkness.",
            "Gorr forged the Godbomb, an apocalyptic engine capable of detonating across past, present, and future to eradicate all gods simultaneously.",
            "Uniting across time, young Viking Thor, modern Avenger Thor, and King Thor of the end times stood shoulder-to-shoulder against the butcher.",
            "Wielding two Mjolnirs imbued with the prayers of the universe, Thor shattered the Necrosword, ending Gorr's reign of vengeance."
        ]
    },
    {
        "id": "daredevil_born_again",
        "character": "Daredevil",
        "title": "Daredevil: Born Again - Kingpin Breaks Matt Murdock",
        "theme_signature": "daredevil:kingpin:born_again_rebirth",
        "description": "Frank Miller's masterpiece where Wilson Fisk systematically destroys Matt Murdock's entire life.",
        "hashtags": "#Daredevil #BornAgain #Kingpin #Marvel #ComicLoreVault #HellKitchen #Reels",
        "scenes": [
            "Desperate for a fix, Karen Page sold Daredevil's secret identity for thirty pieces of heroin, and the information quickly reached Wilson Fisk.",
            "The Kingpin didn't kill Matt Murdock right away; instead, he methodically dismantled his life piece by piece with chilling precision.",
            "Matt lost his law license, had his bank accounts frozen, his apartment building firebombed, and found himself homeless in the snow.",
            "Starving and teetering on madness, Murdock wandered the streets of Hell's Kitchen, nursing injuries until his long-lost mother nursed him back to life.",
            "Recognizing that a man with nothing left to lose is the most dangerous force on Earth, Matt donned his black mask once more.",
            "Daredevil dismantled the Kingpin's syndicate and defeated the super-soldier Nuke, standing tall as the unbreakable guardian of Hell's Kitchen."
        ]
    },
    {
        "id": "civil_war_death_of_cap",
        "character": "Captain America",
        "title": "Civil War: The Tragic Death of Captain America",
        "theme_signature": "captain_america:death:civil_war_courthouse",
        "description": "The heartbreaking aftermath of the superhero Civil War that led to Steve Rogers' assassination on the courthouse steps.",
        "hashtags": "#CaptainAmerica #CivilWar #IronMan #Marvel #ComicLoreVault #Avengers #Reels",
        "scenes": [
            "The superhuman Civil War fractured the superhero community into bitter factions, culminating in a brutal clash across Manhattan streets.",
            "Standing over an incapacitated Tony Stark, Captain America looked around and realized the battle was terrifying the very citizens he swore to protect.",
            "Unmasking himself, Steve Rogers surrendered unconditionally, willing to stand trial in federal court to bring peace to the divided nation.",
            "Ascending the courthouse steps in handcuffs, a high-caliber sniper round from Crossbones struck Steve in the shoulder.",
            "In the ensuing chaos, a brainwashed Sharon Carter fired three close-range shots into Steve's abdomen, ending the life of America's greatest sentinel.",
            "Kneeling beside Steve's casket, a devastated Tony Stark wept in solitary remorse, whispering the tragic truth: 'It wasn't worth it.'"
        ]
    },
    {
        "id": "secret_wars_god_emperor_doom",
        "character": "Doctor Doom",
        "title": "Secret Wars: God Emperor Doom Rules Battleworld",
        "theme_signature": "doctor_doom:secret_wars:battleworld_god",
        "description": "When the multiverse collapsed, Doctor Doom stole the power of the Beyonders and rebuilt existence in his own omnipotent image.",
        "hashtags": "#DoctorDoom #SecretWars #Marvel #MCU #ComicLoreVault #Multiverse #Reels",
        "scenes": [
            "As final Incursions eradicated every universe across the Marvel multiverse, existence ceased to exist, collapsing into infinite nothingness.",
            "Refusing total annihilation, Victor Von Doom confronted the omnipotent Beyonders, stealing their godlike power to stitch together Battleworld.",
            "Ruling as God Emperor Doom, Victor sat upon Yggdrasil with Doctor Strange as his high sheriff and an army of Thors as his cosmic enforcers.",
            "Yet even with absolute reality-warping power, Doom could never cure his deepest insecurity: his inferiority to Reed Richards.",
            "When Mister Fantastic led the survivors to challenge Doom's throne, Victor finally admitted aloud that Reed would have governed reality better.",
            "The cosmic power transferred to Richards, who gently dismantled Battleworld and resurrected the vibrant Marvel multiverse once more."
        ]
    },
    {
        "id": "wolverine_old_man_logan",
        "character": "Wolverine",
        "title": "Wolverine: Old Man Logan - The Massacre of the X-Men",
        "theme_signature": "wolverine:old_man_logan:xmen_massacre",
        "description": "The tragic flashback where Mysterio's twisted illusion tricks Wolverine into slaughtering his own beloved X-Men.",
        "hashtags": "#Wolverine #OldManLogan #XMen #Mysterio #MarvelComics #ComicLoreVault #ComicTok #Reels",
        "scenes": [
            "Fifty years after supervillains conquered the world, an aged Logan lives as a quiet farmer in the wasteland, refusing to ever pop his adamantium claws.",
            "That dark reluctance traces back to one tragic night at the Xavier Mansion, when alarms blared as forty villains suddenly stormed the gates.",
            "Believing the students were in mortal danger, Wolverine entered a blind berserker rage, slashing through the intruders room by room.",
            "Slicing down the final attacker, the smoke cleared as green mist faded: Mysterio appeared cackling, revealing he had clouded Logan's senses.",
            "Horrified, Logan looked around to discover the devastating truth: there were no villains. In the rain lay the slaughtered corpses of his beloved X-Men.",
            "Broken beyond repair, Logan wandered into the wilderness and placed his head on train tracks, but his healing factor refused to let him die."
        ],
        "scene_art_urls": [
            "https://static.wikia.nocookie.net/marveldatabase/images/a/a6/Wolverine_Vol_3_66_Wraparound_Textless.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/7/7f/Peter_Petruski_%28Earth-807128%29%2C_Norman_Osborn_%28Earth-807128%29%2C_James_Howlett_%28Earth-807128%29%2C_and_Kenuichio_Harada_%28Earth-807128%29_from_Wolverine_Vol_3_70_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/3/3a/Wolverine_Vol_3_70.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/c/cd/Jubilation_Lee_%28Earth-807128%29_and_James_Howlett_%28Earth-807128%29_from_Wolverine_Vol_3_70_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/b/b5/X-Men_%28Earth-807128%29_from_Wolverine_Vol_3_70_001.jpg",
            "https://static.wikia.nocookie.net/marveldatabase/images/5/57/James_Howlett_%28Earth-807128%29_from_Wolverine_Vol_3_72_002.jpg"
        ]
    },
    {
        "id": "venom_maximum_carnage",
        "character": "Carnage",
        "title": "Venom & Spider-Man: Maximum Carnage - Pure Psychotic Chaos",
        "theme_signature": "carnage:maximum_carnage:venom_spiderman_truce",
        "description": "When Cletus Kasady leads a psychotic family of serial killers through New York, mortal enemies Spider-Man and Venom forge an uneasy alliance.",
        "hashtags": "#Carnage #Venom #SpiderMan #MaximumCarnage #MarvelComics #ComicLoreVault #Reels",
        "scenes": [
            "Escaping the Ravencroft Institute, serial killer Cletus Kasady discovered his red alien symbiote had bonded directly to his bloodstream as Carnage.",
            "Gathering a twisted family of maniacs including Shriek and Doppelganger, Carnage launched a wave of pure uninhibited slaughter through Manhattan.",
            "Overwhelmed by the psychotic brutality, Spider-Man realized his moral code was ill-equipped to face monsters who slaughtered purely for entertainment.",
            "Arriving with monstrous rage, Venom confronted Peter, offering an unthinkable deal: an uneasy truce to tear Carnage limb from limb.",
            "Fighting back-to-back across the burning skyline, the web-slinger and the lethal protector clashed over whether justice required lethal vengeance.",
            "Using sonic beam weaponry, they neutralized Carnage's horde, saving New York while preserving the fine line between hero and executioner."
        ]
    }
]


def log(msg: str):
    print(f"[{time.strftime('%H:%M:%S')}] [CloudRunner] {msg}", flush=True)


def load_ledger() -> list[dict]:
    """Loads history of produced videos from published_ledger.json."""
    if not LEDGER_PATH.exists():
        return []
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log(f"Warning loading ledger: {e}")
        return []


def save_ledger(ledger: list[dict]):
    """Saves updated history to published_ledger.json."""
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2, ensure_ascii=False)
    log(f"Ledger updated: {len(ledger)} total entries.")


def is_duplicate(story: dict, ledger: list[dict]) -> tuple[bool, str]:
    """Checks if a story or theme has already been produced."""
    s_id = story.get("id", "").strip().lower()
    s_sig = story.get("theme_signature", "").strip().lower()
    s_title = re.sub(r"[^\w\s]", "", story.get("title", "").lower()).strip()

    for item in ledger:
        item_id = item.get("id", "").strip().lower()
        item_sig = item.get("theme_signature", "").strip().lower()
        item_title = re.sub(r"[^\w\s]", "", item.get("title", "").lower()).strip()

        if s_id and s_id == item_id:
            return True, f"ID match: '{s_id}' (produced {item.get('date', 'previously')})"
        if s_sig and s_sig == item_sig:
            return True, f"Theme match: '{s_sig}' (produced {item.get('date', 'previously')})"
        if s_title and (s_title in item_title or item_title in s_title):
            return True, f"Title match: '{item.get('title')}' (produced {item.get('date', 'previously')})"

    return False, ""


def record_production(story: dict, mode: str, video_path: str):
    """Records newly produced video in the ledger."""
    ledger = load_ledger()
    entry = {
        "id": story["id"],
        "title": story["title"],
        "character": story["character"],
        "theme_signature": story.get("theme_signature", f"{story['character'].lower()}:{story['id']}"),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "mode": mode,
        "video_file": Path(video_path).name,
        "status": "published" if mode == "live_release" else "produced"
    }
    ledger.append(entry)
    save_ledger(ledger)


def build_cloud_generation(story: dict, work_dir: Path) -> dict:
    """Creates a local generation folder with downloaded comic panels and script.json."""
    gen_dir = work_dir / story["id"]
    gen_dir.mkdir(parents=True, exist_ok=True)

    curated_urls = story.get("scene_art_urls", [])
    if curated_urls:
        log(f"Using {len(curated_urls)} curated 1:1 comic panels for: {story['title']}")
        art_urls = curated_urls
    else:
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

    for idx, narration in enumerate(story["scenes"], start=1):
        sc_name = f"Escena_{idx:02d}"
        sc_dir = gen_dir / sc_name
        sc_dir.mkdir(parents=True, exist_ok=True)
        img_file = sc_dir / "imagen_01.jpg"

        saved = False
        if idx - 1 < len(art_urls):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                r = requests.get(art_urls[idx - 1], headers=headers, timeout=15)
                if r.status_code == 200 and len(r.content) > 10000:
                    import io
                    im = Image.open(io.BytesIO(r.content)).convert('RGB')
                    target_w, target_h = 1080, 1920
                    scale = max(target_w / im.width, target_h / im.height)
                    nw, nh = max(target_w, int(im.width * scale)), max(target_h, int(im.height * scale))
                    im_resized = im.resize((nw, nh), Image.Resampling.LANCZOS)
                    left = (nw - target_w) // 2
                    top = (nh - target_h) // 2
                    im_cropped = im_resized.crop((left, top, left + target_w, top + target_h))
                    im_cropped.save(img_file, quality=92)
                    saved = True
            except Exception as e:
                log(f"Warning processing image {idx}: {e}")
                saved = False

        if not saved or not img_file.exists():
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
    parser.add_argument("--draft", action="store_true", help="Save as unpublished draft on FB and skip public IG")
    parser.add_argument("--dry-run", action="store_true", help="Test workflow without video generation or publishing")
    args = parser.parse_args()

    log("Initializing Comic Lore Vault Cloud Engine with Anti-Duplication Protection...")
    log(f"Brand: Comic Lore Vault (@comicloreevault)")
    log(f"FB Page ID: {os.environ.get('FB_PAGE_ID', DEFAULT_PAGE_ID)}")
    log(f"IG Account ID: {os.environ.get('IG_USER_ID', DEFAULT_IG_USER_ID)}")

    ledger = load_ledger()
    log(f"Historical Ledger: {len(ledger)} previously produced videos registered.")

    # Story Selection & Anti-Duplication Verification
    if args.story_id and args.story_id != "any":
        selected = next((s for s in EDITORIAL_STORIES if s["id"] == args.story_id), None)
        if not selected:
            log(f"Error: Story ID '{args.story_id}' not found in catalog.")
            sys.exit(1)

        is_dup, reason = is_duplicate(selected, ledger)
        if is_dup:
            log(f"CRITICAL ANTI-DUPLICATION SHIELD: Story '{selected['title']}' rejected.")
            log(f"Reason: {reason}")
            log("No duplicate videos will ever be produced. Aborting safely.")
            sys.exit(0)
    else:
        # Filter available unproduced stories
        available = [s for s in EDITORIAL_STORIES if not is_duplicate(s, ledger)[0]]
        log(f"Available unproduced stories in catalog: {len(available)} / {len(EDITORIAL_STORIES)}")

        if not available:
            log("All cataloged stories have been produced! No duplicates permitted.")
            log("Add new storylines to EDITORIAL_STORIES before running next production.")
            sys.exit(0)

        selected = random.choice(available)

    log(f"Selected Unique Story: {selected['title']} (ID: {selected['id']})")

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

    mode_str = "render_only"
    if args.publish or os.environ.get("AUTO_PUBLISH", "").lower() in ("true", "1", "yes"):
        is_draft = args.draft or os.environ.get("DRAFT_ONLY", "").lower() in ("true", "1", "yes")
        mode_str = "draft_only" if is_draft else "live_release"
        log(f"Initiating publication to Comic Lore Vault (mode: {'DRAFT ONLY' if is_draft else 'LIVE PUBLIC'})...")
        publish_comic_video(
            video_path=final_video_path,
            title=selected["title"],
            description=selected["description"],
            hashtags=selected["hashtags"],
            draft_only=is_draft,
        )
    else:
        log("Publication skipped (render_only mode).")

    # Record in persistent ledger to ensure it can NEVER be repeated
    record_production(selected, mode_str, final_video_path)
    log(f"Anti-duplication registry updated: '{selected['id']}' locked permanently.")


if __name__ == "__main__":
    main()
