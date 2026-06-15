#!/usr/bin/env python3
"""Query multiple LLMs (ChatGPT + Gemini) and return their responses as JSON.

Usage: python3 scripts/query_llms.py "Your prompt here"

Requires .env file with:
  OPENAI_API_KEY=sk-...
  GEMINI_API_KEY=...

Optional .env overrides:
  OPENAI_MODEL=gpt-5-nano        (default)
  GEMINI_MODEL=gemini-3-flash-preview  (default)
"""

import json
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_env():
    """Load .env from CWD or project root."""
    for p in [Path(".env"), Path(__file__).parent.parent / ".env"]:
        if p.exists():
            for line in p.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
            break

def query_openai(prompt: str, model: str) -> dict:
    """Query OpenAI ChatGPT API."""
    try:
        import urllib.request
        key = os.environ.get("OPENAI_API_KEY")
        if not key:
            return {"model": "chatgpt", "error": "OPENAI_API_KEY not set"}

        data = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4096,
        }).encode()

        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            return {
                "model": f"chatgpt ({model})",
                "response": result["choices"][0]["message"]["content"],
            }
    except Exception as e:
        return {"model": f"chatgpt ({model})", "error": str(e)}

def query_gemini(prompt: str, model: str) -> dict:
    """Query Google Gemini API."""
    try:
        import urllib.request
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            return {"model": "gemini", "error": "GEMINI_API_KEY not set"}

        data = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 4096},
        }).encode()

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return {"model": f"gemini ({model})", "response": text}
    except Exception as e:
        return {"model": f"gemini ({model})", "error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/query_llms.py 'Your prompt'", file=sys.stderr)
        sys.exit(1)

    load_env()
    prompt = sys.argv[1]
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-5-nano")
    gemini_model = os.environ.get("GEMINI_MODEL", "gemini-3-flash-preview")

    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {
            pool.submit(query_openai, prompt, openai_model): "openai",
            pool.submit(query_gemini, prompt, gemini_model): "gemini",
        }
        for future in as_completed(futures):
            results.append(future.result())

    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
