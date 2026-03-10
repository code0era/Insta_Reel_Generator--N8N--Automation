"""
instagram_poster.py
Upload a video to Instagram as a Reel using the Graph API.

Steps (Facebook docs):
  1. POST /me/media (upload container)
  2. Poll until status = FINISHED
  3. POST /me/media_publish

Usage:
  python instagram_poster.py <video_path> "<caption>"
"""
import sys, os, time, requests

ACCESS_TOKEN = os.environ["INSTAGRAM_ACCESS_TOKEN"]
ACCOUNT_ID   = os.environ["INSTAGRAM_ACCOUNT_ID"]
BASE_URL     = f"https://graph.facebook.com/v18.0/{ACCOUNT_ID}"

def upload_reel(video_path: str, caption: str) -> str:
    # Must be a public URL; for local use, serve via ngrok or upload to cloud.
    # Here we expect VIDEO_URL env var pointing to a publicly accessible MP4.
    video_url = os.environ.get("VIDEO_URL", "")
    if not video_url:
        raise ValueError("VIDEO_URL env var must be set to a public URL of the MP4.")

    # 1. Create media container
    r = requests.post(f"{BASE_URL}/media", params={
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": ACCESS_TOKEN,
    })
    r.raise_for_status()
    container_id = r.json()["id"]

    # 2. Poll for status
    for _ in range(30):
        time.sleep(10)
        status_r = requests.get(f"https://graph.facebook.com/v18.0/{container_id}", params={
            "fields": "status_code",
            "access_token": ACCESS_TOKEN,
        })
        status_r.raise_for_status()
        code = status_r.json().get("status_code")
        if code == "FINISHED":
            break
        elif code == "ERROR":
            raise RuntimeError("Instagram upload failed during processing.")

    # 3. Publish
    pub_r = requests.post(f"{BASE_URL}/media_publish", params={
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN,
    })
    pub_r.raise_for_status()
    media_id = pub_r.json()["id"]
    print(f"Published Reel ID: {media_id}")
    return media_id

if __name__ == "__main__":
    video_path = sys.argv[1]
    caption    = sys.argv[2] if len(sys.argv) > 2 else ""
    upload_reel(video_path, caption)
