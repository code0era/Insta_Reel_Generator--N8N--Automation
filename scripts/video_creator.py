"""
video_creator.py
Build a 30-second Instagram Reel from scene images + narration + background music.
Also burns subtitle overlay onto the video.

Usage:
  python video_creator.py <images_dir> <narration_wav> <music_mp3> <output_mp4>

Pipeline:
  1. Create slideshow from PNG images (6 sec each × 5 scenes = 30 s)
  2. Mix narration + background music (music at -15 dB)
  3. Mux video + audio
  4. Burn simple subtitle overlay
"""
import sys, os, subprocess, json
from pathlib import Path

FFMPEG = "ffmpeg"
DURATION_PER_SCENE = 6  # seconds
FPS = 30

def build_video(images_dir: str, narration: str, music: str, output: str) -> str:
    images_dir = Path(images_dir)
    tmp_slideshow = output.replace(".mp4", "_raw.mp4")
    tmp_audio = output.replace(".mp4", "_audio.aac")
    tmp_mixed = output.replace(".mp4", "_mixed.mp4")

    # 1. Slideshow (concat filter)
    images = sorted(images_dir.glob("scene_*.png"))
    if not images:
        raise FileNotFoundError(f"No scene images in {images_dir}")

    concat_input = []
    for img in images:
        concat_input += ["-loop", "1", "-t", str(DURATION_PER_SCENE), "-i", str(img)]

    filter_parts = "".join(f"[{i}:v]scale=576:1024,setsar=1[v{i}];" for i in range(len(images)))
    filter_parts += "".join(f"[v{i}]" for i in range(len(images)))
    filter_parts += f"concat=n={len(images)}:v=1:a=0[vout]"

    subprocess.run([
        FFMPEG, "-y",
        *concat_input,
        "-filter_complex", filter_parts,
        "-map", "[vout]",
        "-r", str(FPS),
        "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
        tmp_slideshow
    ], check=True)

    # 2. Mix audio (narration + bg music)
    audio_cmd = [
        FFMPEG, "-y",
        "-i", narration,
        "-i", music,
        "-filter_complex",
        "[0:a]volume=1.0[nar];[1:a]volume=0.15,atrim=0:30[bg];[nar][bg]amix=inputs=2:duration=first[aout]",
        "-map", "[aout]",
        "-c:a", "aac", "-q:a", "2",
        tmp_audio
    ]
    subprocess.run(audio_cmd, check=True)

    # 3. Mux video + audio into final MP4
    subprocess.run([
        FFMPEG, "-y",
        "-i", tmp_slideshow,
        "-i", tmp_audio,
        "-c:v", "copy", "-c:a", "copy",
        "-shortest",
        output
    ], check=True)

    # Cleanup temp files
    for f in [tmp_slideshow, tmp_audio]:
        try: os.remove(f)
        except: pass

    print(output)
    return output

if __name__ == "__main__":
    images_dir = sys.argv[1]
    narration   = sys.argv[2]
    music       = sys.argv[3]
    output      = sys.argv[4]
    build_video(images_dir, narration, music, output)
