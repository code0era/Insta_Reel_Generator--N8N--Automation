"""
tts_generator.py
Generate narration audio using Coqui TTS HTTP API.
Usage: python tts_generator.py "<narration_text>" <output_wav_path>
"""
import sys, os, requests

TTS_API_URL = os.getenv("TTS_API_URL", "http://localhost:5002")

def generate_tts(text: str, out_path: str) -> str:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    resp = requests.get(
        f"{TTS_API_URL}/api/tts",
        params={"text": text},
        timeout=120,
    )
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)
    print(out_path)
    return out_path

if __name__ == "__main__":
    text = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "/app/output/audio/narration.wav"
    generate_tts(text, out_path)
