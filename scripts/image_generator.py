"""
image_generator.py
Send image prompts to Stable Diffusion (Automatic1111) API.
Usage: python image_generator.py "<prompt>" <scene_index> <output_dir>
Output: saves image to output_dir/scene_<n>.png
"""
import sys, os, base64, requests
from pathlib import Path

SD_API_URL = os.getenv("SD_API_URL", "http://localhost:7860")

def generate_image(prompt: str, scene_idx: int, output_dir: str) -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, low quality, watermark, text",
        "steps": 20,
        "width": 576,
        "height": 1024,   # 9:16 portrait for Reels
        "cfg_scale": 7,
        "sampler_name": "Euler a",
    }
    resp = requests.post(f"{SD_API_URL}/sdapi/v1/txt2img", json=payload, timeout=180)
    resp.raise_for_status()
    img_b64 = resp.json()["images"][0]
    out_path = os.path.join(output_dir, f"scene_{scene_idx:02d}.png")
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(out_path)
    return out_path

if __name__ == "__main__":
    prompt = sys.argv[1]
    idx = int(sys.argv[2])
    out_dir = sys.argv[3] if len(sys.argv) > 3 else "/app/output/images"
    generate_image(prompt, idx, out_dir)
