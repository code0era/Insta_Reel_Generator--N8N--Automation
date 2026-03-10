# 🎬 Instagram Reels Automation Agent

> Fully local, free-stack AI pipeline — generates and posts 30-second Instagram Reels automatically every few hours.

## Stack

| Layer | Tool |
|---|---|
| Automation engine | n8n |
| LLM | Ollama + Llama3 |
| Image generation | Stable Diffusion (Automatic1111) |
| Video processing | FFmpeg |
| Voice | Coqui TTS |
| Social posting | Instagram Graph API |
| Notifications | Gmail SMTP |
| Deployment | Docker Compose |

---

## Project Structure

```
instagram-reels-agent/
├── docker-compose.yml       # All services
├── Dockerfile.agent         # Python agent image
├── .env                     # Credentials (never commit real values)
├── scripts/
│   ├── requirements.txt
│   ├── trend_scraper.py     # 1. Google Trends → trending topic
│   ├── idea_generator.py    # 2. Ollama/Llama3 → reel plan JSON
│   ├── image_generator.py   # 3. SD API → 5 scene images
│   ├── tts_generator.py     # 4. Coqui TTS → narration WAV
│   ├── video_creator.py     # 5. FFmpeg → 30s MP4
│   ├── instagram_poster.py  # 6. Graph API → post reel
│   ├── notifier.py          # 7. Gmail SMTP → confirmation
│   └── pipeline.py          # Full orchestrator (runs all steps)
├── n8n/
│   └── workflow.json        # Import into n8n UI
├── output/
│   ├── images/              # Generated scene PNGs
│   ├── videos/              # Final MP4 reels
│   └── audio/               # Narration WAVs
├── music/                   # background.mp3 (add your own)
└── logs/                    # pipeline.log
```

---

## Setup

### 1. Fill in credentials

Edit `.env`:
```
INSTAGRAM_ACCESS_TOKEN=your_token
INSTAGRAM_ACCOUNT_ID=your_account_id
GMAIL_USER=you@gmail.com
GMAIL_APP_PASSWORD=your_app_password
NOTIFY_EMAIL=you@gmail.com
```

> **Instagram**: You need a [Meta Developer App](https://developers.facebook.com/) with a Page-linked Instagram Professional account.  
> **Gmail**: Use an [App Password](https://myaccount.google.com/apppasswords), NOT your real password.

### 2. Add background music

Place any royalty-free MP3 at:
```
music/background.mp3
```

### 3. Pull the Llama3 model

```bash
docker compose up -d ollama
docker exec ollama ollama pull llama3
```

### 4. Start all services

```bash
docker compose up -d
```

Services:
- **n8n** → http://localhost:5678 (admin / admin123)
- **Stable Diffusion** → http://localhost:7860
- **Ollama** → http://localhost:11434
- **Coqui TTS** → http://localhost:5002

### 5. Import n8n workflow

1. Open http://localhost:5678
2. Go to **Workflows → Import from file**
3. Select `n8n/workflow.json`
4. **Activate** the workflow

---

## Manual Run (without n8n)

```bash
docker exec reels-agent python /app/scripts/pipeline.py
```

---

## How It Works

```
Schedule (every 6h)
  → trend_scraper.py    # trending topic
  → idea_generator.py   # LLM: title + 5 scenes + narration + caption
  → image_generator.py  # SD: 1 image per scene (576×1024 px)
  → tts_generator.py    # Coqui: narration WAV
  → video_creator.py    # FFmpeg: slideshow + audio mix = 30s MP4
  → instagram_poster.py # Graph API: upload + publish reel
  → notifier.py         # Gmail: confirmation email
```

---

## Notes

- Instagram Graph API requires the video to be at a **public URL** (`VIDEO_URL` env var). Use [ngrok](https://ngrok.com/) or [MinIO](https://min.io/) to serve the local file publicly.
- SD image generation takes ~2–5 min per scene on CPU; use a GPU for speed.
- Logs: `logs/pipeline.log`
