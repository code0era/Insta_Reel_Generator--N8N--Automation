# commit_all.ps1 — run once to commit every file and push to GitHub
Set-Location "C:\Users\syshu\Desktop\Code_Era\AGENTIC AI\instagram-reels-agent"

function Commit($file, $message) {
    git add $file
    git commit -m $message
    Write-Host "Committed: $file"
}

# ── Commit individual files ─────────────────────────────────
Commit ".gitignore"                  "chore: add .gitignore"
Commit "docker-compose.yml"          "feat: add docker-compose with all services"
Commit "Dockerfile.agent"            "feat: add Dockerfile.agent (Python 3.11 + FFmpeg)"
Commit ".env"                         "chore: add .env template (no secrets)"
Commit "scripts/requirements.txt"    "feat: add Python requirements"
Commit "scripts/trend_scraper.py"    "feat: add trend_scraper.py - Google Trends via pytrends"
Commit "scripts/idea_generator.py"   "feat: add idea_generator.py - LLM reel planner via Ollama/Llama3"
Commit "scripts/image_generator.py"  "feat: add image_generator.py - Stable Diffusion API integration"
Commit "scripts/tts_generator.py"    "feat: add tts_generator.py - Coqui TTS narration generator"
Commit "scripts/video_creator.py"    "feat: add video_creator.py - FFmpeg 30s reel builder"
Commit "scripts/instagram_poster.py" "feat: add instagram_poster.py - Instagram Graph API publisher"
Commit "scripts/notifier.py"         "feat: add notifier.py - Gmail SMTP notification"
Commit "scripts/pipeline.py"         "feat: add pipeline.py - full end-to-end orchestrator"
Commit "n8n/workflow.json"           "feat: add n8n workflow JSON - 11-node automation pipeline"
Commit "README.md"                   "docs: add README with setup, structure, and run instructions"

# ── Commit directory placeholder files ─────────────────────
git add "output/images/.gitkeep" "output/videos/.gitkeep" "output/audio/.gitkeep" "logs/.gitkeep" "music/.gitkeep"
git commit -m "chore: add .gitkeep placeholders for output/logs/music dirs"

# ── Push ──────────────────────────────────────────────────────
Write-Host "Pushing to GitHub..."
git branch -M main
git push -u origin main

Write-Host "All done! Check https://github.com/code0era/Insta_Reel_Generator--N8N--Automation"
