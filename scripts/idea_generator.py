"""
idea_generator.py
Call Ollama/Llama3 to generate a full reel plan from a trending topic.
Usage: python idea_generator.py "<topic>"
Output: JSON with keys: title, scenes (list of 5), narration, caption, hashtags
"""
import sys, json, os, requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3")

PROMPT_TEMPLATE = """
You are a creative Instagram Reels scriptwriter.
Topic: {topic}

Return ONLY valid JSON with this exact structure:
{{
  "title": "Reel title (max 10 words)",
  "scenes": [
    {{"scene": 1, "description": "...", "image_prompt": "photorealistic, ..."}},
    {{"scene": 2, "description": "...", "image_prompt": "photorealistic, ..."}},
    {{"scene": 3, "description": "...", "image_prompt": "photorealistic, ..."}},
    {{"scene": 4, "description": "...", "image_prompt": "photorealistic, ..."}},
    {{"scene": 5, "description": "...", "image_prompt": "photorealistic, ..."}}
  ],
  "narration": "Full narration script (30 seconds, ~80 words)",
  "caption": "Instagram caption (150 chars max)",
  "hashtags": "#tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7 #tag8 #tag9 #tag10"
}}
"""

def generate_idea(topic: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(topic=topic)
    resp = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    raw = resp.json()["response"]
    # Extract JSON block
    start = raw.index("{")
    end = raw.rindex("}") + 1
    return json.loads(raw[start:end])

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI trends"
    result = generate_idea(topic)
    print(json.dumps(result, indent=2))
