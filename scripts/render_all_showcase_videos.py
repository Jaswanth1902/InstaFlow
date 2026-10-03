"""
scripts/render_all_showcase_videos.py
Renders all three 20+ second showcase videos for InstaFlow (WCC Hackathon):
1. InstaFlow_Hero_Showcase.mp4 (39.5s, 720p) + Gnani Voiceover
2. InstaFlow_Happy_Flow.mp4 (37.5s, 720p) + Gnani Voiceover
3. InstaFlow_Unhappy_Flows.mp4 (37.0s, 720p) + Gnani Voiceover

Complies with Layer 0 Invariants (Law 8: CREATE_NO_WINDOW = 0x08000000).
"""

import os
import sys
import time
import shutil
import subprocess
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def render_video(name: str, html_file: Path, sfx_file: Path, out_mp4: Path, onetake_script: Path):
    inbox_dir = Path(r"C:\Users\jaswa\Antigravity\00_Inbox")
    inbox_dir.mkdir(parents=True, exist_ok=True)
    inbox_mp4 = inbox_dir / out_mp4.name
    
    print("\n" + "=" * 66)
    print(f"  RENDERING SHOWCASE VIDEO: {name}")
    print("=" * 66)
    print(f"HTML Composition : {html_file.name}")
    print(f"Gnani Voice Track: {sfx_file.name}")
    print(f"Output MP4 Target: {out_mp4.name}")
    
    cmd = [
        sys.executable,
        str(onetake_script),
        str(html_file),
        "--out", str(out_mp4),
        "--sfx", str(sfx_file),
        "--width", "1280",
        "--height", "720",
        "--shutter", "0",
        "--workers", "2"
    ]
    
    cflags = 0x08000000 if os.name == "nt" else 0
    t0 = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True, creationflags=cflags)
    
    print(f"[{name}] onetake exit code: {res.returncode}")
    if res.returncode != 0:
        print("stderr:", res.stderr[-500:])
        print("stdout:", res.stdout[-500:])
        return False
        
    if out_mp4.exists():
        sz = out_mp4.stat().st_size
        elapsed = time.time() - t0
        print(f"[OK] [{name}] Success: {out_mp4.name} ({sz:,} bytes in {elapsed:.1f}s)")
        shutil.copy2(out_mp4, inbox_mp4)
        print(f"[OK] Copied to inbox: {inbox_mp4}")
        return True
    else:
        print(f"[FAIL] [{name}] Failed: Output file was not created.")
        return False

def main():
    proj_dir = Path(__file__).resolve().parent.parent
    showcase_dir = proj_dir / "showcase"
    assets_dir = proj_dir / "assets" / "videos"
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    onetake_script = Path(r"C:\Users\jaswa\Antigravity\tools\onetake\scripts\render.py")
    if not onetake_script.exists():
        onetake_script = Path(r"C:\Users\jaswa\Antigravity\.agents\skills\onetake\scripts\render.py")
        
    videos = [
        {
            "name": "1. Hero Showcase (What, Detect, Resolve)",
            "html": showcase_dir / "hero_showcase.html",
            "sfx": showcase_dir / "audio" / "hero_narration.wav",
            "out": assets_dir / "InstaFlow_Hero_Showcase.mp4"
        },
        {
            "name": "2. Happy Flow (BitNet Quantization Pipeline)",
            "html": showcase_dir / "happy_flow.html",
            "sfx": showcase_dir / "audio" / "happy_flow_narration.wav",
            "out": assets_dir / "InstaFlow_Happy_Flow.mp4"
        },
        {
            "name": "3. Unhappy & Adversarial Flows (Scam & Fake Repo Quarantine)",
            "html": showcase_dir / "unhappy_flows.html",
            "sfx": showcase_dir / "audio" / "unhappy_flows_narration.wav",
            "out": assets_dir / "InstaFlow_Unhappy_Flows.mp4"
        }
    ]
    
    start_all = time.time()
    success_count = 0
    for v in videos:
        ok = render_video(v["name"], v["html"], v["sfx"], v["out"], onetake_script)
        if ok:
            success_count += 1
            
    print("\n" + "=" * 66)
    print(f"  RENDERING COMPLETE: {success_count}/{len(videos)} VIDEOS READY")
    print(f"  Total Duration: {time.time() - start_all:.1f}s")
    print("=" * 66)

if __name__ == "__main__":
    main()
