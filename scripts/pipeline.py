"""
pipeline.py
Full end-to-end orchestrator — called by n8n (Execute Command node) or directly.
Usage: python pipeline.py
"""
import os, json, datetime, subprocess, sys
from pathlib import Path

OUTPUT_BASE = os.getenv("OUTPUT_DIR", "/app/output")
MUSIC_FILE  = os.getenv("MUSIC_FILE", "/app/music/background.mp3")
SCRIPTS     = "/app/scripts"   # inside Docker; adjust for local runs

def run(script: str, *args) -> str:
    """Run a Python script and return stripped stdout."""
    result = subprocess.run(
        ["python", script, *args],
        capture_output=True, text=True, check=True
    )
    return result.stdout.strip()

def log(msg: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    Path("/app/logs/pipeline.log").parent.mkdir(parents=True, exist_ok=True)
    with open("/app/logs/pipeline.log", "a") as f:
        f.write(line + "\n")

def main():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    img_dir   = f"{OUTPUT_BASE}/images/{timestamp}"
    vid_path  = f"{OUTPUT_BASE}/videos/reel_{timestamp}.mp4"
    wav_path  = f"{OUTPUT_BASE}/audio/narration_{timestamp}.wav"
    Path(img_dir).mkdir(parents=True, exist_ok=True)

    # 1. Trending topic
    log("Fetching trending topic...")
    raw = run(f"{SCRIPTS}/trend_scraper.py")
    topic = json.loads(raw)["topic"]
    log(f"Topic: {topic}")

    # 2. Generate reel idea
    log("Generating reel idea via LLM...")
    idea_raw = run(f"{SCRIPTS}/idea_generator.py", topic)
    idea = json.loads(idea_raw)
    log(f"Title: {idea['title']}")

    # 3. Generate images (5 scenes in parallel via subprocess)
    log("Generating scene images via Stable Diffusion...")
    procs = []
    for scene in idea["scenes"]:
        p = subprocess.Popen(
            ["python", f"{SCRIPTS}/image_generator.py",
             scene["image_prompt"], str(scene["scene"]), img_dir],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        procs.append(p)
    for p in procs:
        p.wait()
        if p.returncode != 0:
            log(f"WARNING: SD image gen failed: {p.stderr.read().decode()}")

    # 4. Generate TTS narration
    log("Generating narration audio via Coqui TTS...")
    run(f"{SCRIPTS}/tts_generator.py", idea["narration"], wav_path)

    # 5. Build video
    log("Building 30-second reel with FFmpeg...")
    run(f"{SCRIPTS}/video_creator.py", img_dir, wav_path, MUSIC_FILE, vid_path)

    # 6. Post to Instagram
    log("Posting to Instagram...")
    caption = f"{idea['caption']}\n\n{idea['hashtags']}"
    run(f"{SCRIPTS}/instagram_poster.py", vid_path, caption)

    # 7. Send notification
    log("Sending email notification...")
    subject = f"✅ Reel Posted: {idea['title']}"
    body = f"Topic: {topic}\nCaption: {caption}\nVideo: {vid_path}"
    run(f"{SCRIPTS}/notifier.py", subject, body)

    log("Pipeline complete!")

if __name__ == "__main__":
    main()
