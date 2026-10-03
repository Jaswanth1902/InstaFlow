"""
scripts/generate_video_narrations.py
Synthesizes professional Indian English voiceovers for the three InstaFlow WCC Hackathon showcase videos:
1. Hero Showcase (What, Detect, Resolve) (~32s)
2. Happy Flow (BitNet Quantization Pipeline) (~32s)
3. Unhappy & Adversarial Flows (Scam & Fake Repo Quarantine) (~32s)

Uses the Gnani.ai Vachana Voice Platform API (Timbre v2.5, voice: Kartik, en-IN).
Complies with Layer 0 Invariants (Law 16: Silent credential ingestion from credentials.env).
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

proj_dir = Path(__file__).resolve().parent.parent
# Load Gnani key from AcuDiag credentials or environment
cred_path = Path(r"C:\Users\jaswa\Antigravity\01_Projects\AcuDiag\credentials\credentials.env")

def get_gnani_key():
    if not cred_path.exists():
        return ""
    with open(cred_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("GNANI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"\'')
    return ""

SCRIPTS = {
    "hero": {
        "text": (
            "In today's creator economy, technical Instagram reels and AI tutorials suffer from rampant misinformation, "
            "fake benchmarks, and unverified repository claims. "
            "Meet InstaFlow: the OMNI truth verification and autonomous cross-platform repurposing engine for developers. "
            "Using real-time lexical overlap against the live arXiv preprint API, live GitHub code indexing, and container-level video probing, "
            "InstaFlow isolates genuine open-source engineering from vaporware. "
            "With Fetch.ai Agentverse protocol synchronization and human-kinetic teleoperation, "
            "verified technical reels are autonomously transformed into executive carousels and technical briefs. "
            "Welcome to ground-truth social engineering."
        ),
        "voice": "Kartik",
        "lang": "en-IN",
        "out": proj_dir / "showcase" / "audio" / "hero_narration.wav"
    },
    "happy_flow": {
        "text": (
            "In this happy flow, a developer bookmarks a viral Instagram reel demonstrating a breakthrough BitNet quantization algorithm. "
            "InstaFlow immediately extracts video container metadata and audio transcripts via VideoDR. "
            "Next, our OMNI-Truth engine queries the live arXiv API, matching key tokens like ternary weights and matrix multiplication "
            "with a ninety-four percent lexical confidence score, while GitHub Search API validates the repository. "
            "With truth mathematically established, InstaFlow's repurposer generates a publication-ready five-slide carousel SVG, "
            "creates an executive technical brief, and queues cross-platform teleoperation with human-like Gaussian touch jitter."
        ),
        "voice": "Kartik",
        "lang": "en-IN",
        "out": proj_dir / "showcase" / "audio" / "happy_flow_narration.wav"
    },
    "unhappy_flows": {
        "text": (
            "In our adversarial unhappy flows, InstaFlow actively defends developers against scam tutorials, fake repos, and viral vaporware. "
            "When a user submits a deceptive reel promising ten thousand dollars a day with a secret automated trading bot, "
            "InstaFlow's OMNI-Truth engine cross-references academic preprints and finds zero lexical overlap. "
            "Simultaneously, live GitHub search reveals no genuine repository, and our scam heuristic penalizes deceptive financial keywords, "
            "dropping credibility to point zero five. "
            "InstaFlow instantly triggers Quarantine Lockdown, halts all publishing pipelines, "
            "and emits a forensic audit report exposing the claims as fabricated slop."
        ),
        "voice": "Kartik",
        "lang": "en-IN",
        "out": proj_dir / "showcase" / "audio" / "unhappy_flows_narration.wav"
    }
}

def synthesize(api_key: str, text: str, voice: str, lang: str, out_path: Path):
    tts_url = "https://api.vachana.ai/api/v1/tts/inference"
    payload = {
        "text": text,
        "voice": voice,
        "model": "timbre-v2.5",
        "language": lang,
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 24000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav"
        }
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "X-API-Key-ID": api_key,
        "User-Agent": "InstaFlow-Client/1.0"
    }
    req = urllib.request.Request(tts_url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        audio_bytes = resp.read()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(audio_bytes)
        return len(audio_bytes)

def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("==================================================================")
    print("  INSTAFLOW WCC: GNANI VACHANA VOICE PLATFORM AUDIO SYNTHESIS")
    print("==================================================================")
    api_key = get_gnani_key()
    if not api_key:
        print("Error: Could not locate GNANI_API_KEY in credentials.")
        sys.exit(1)
        
    for key, spec in SCRIPTS.items():
        print(f"Synthesizing [{key}] voiceover...")
        print(f"Voice: {spec['voice']} ({spec['lang']})")
        sz = synthesize(api_key, spec["text"], spec["voice"], spec["lang"], spec["out"])
        dur = (sz - 44) / 48000.0
        print(f"[OK] {spec['out'].name}: {sz:,} bytes, {dur:.2f}s (Target: >20s)")
        print("-" * 60)

if __name__ == "__main__":
    main()
