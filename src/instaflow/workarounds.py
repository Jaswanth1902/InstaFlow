"""
workarounds.py — Resilient Cross-Platform Unauthenticated Harvesters
Implements battle-tested, anti-ban workarounds across Twitter/X, Pinterest, Reddit, and Instagram.
"""

from __future__ import annotations
import urllib.request
import urllib.parse
import json
import re
import subprocess
from typing import Dict, List, Optional, Any


class PlatformWorkarounds:
    """Zero-credential, resilient data extractors across protected social platforms."""

    @staticmethod
    def fetch_twitter_syndication(tweet_id: str, timeout: int = 6) -> Dict[str, Any]:
        """Fetches full unauthenticated tweet data using Twitter's public Syndication CDN API."""
        url = f"https://cdn.syndication.twimg.com/tweet-result?id={tweet_id}&token=x"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {
                    "id": tweet_id,
                    "author": data.get("user", {}).get("screen_name", ""),
                    "author_name": data.get("user", {}).get("name", ""),
                    "text": data.get("text", ""),
                    "created_at": data.get("created_at", ""),
                    "likes": data.get("favorite_count", 0),
                    "status": "SUCCESS"
                }
        except Exception as e:
            return {"id": tweet_id, "error": str(e), "status": "FAILED"}

    @staticmethod
    def fetch_pinterest_rss(username: str, board_name: Optional[str] = None, timeout: int = 6) -> List[Dict[str, str]]:
        """Harvests public Pinterest board pins via native unauthenticated RSS feeds."""
        if board_name:
            clean_board = board_name.strip("/").replace(" ", "-")
            url = f"https://www.pinterest.com/{username}/{clean_board}.rss"
        else:
            url = f"https://www.pinterest.com/{username}/feed.rss"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        pins = []
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
                items = re.findall(r"<item>(.*?)</item>", content, re.DOTALL)
                for item in items[:10]:
                    title = re.search(r"<title>(.*?)</title>", item)
                    link = re.search(r"<link>(.*?)</link>", item)
                    desc = re.search(r"<description>(.*?)</description>", item)
                    pins.append({
                        "title": title.group(1).strip() if title else "Untitled Pin",
                        "link": link.group(1).strip() if link else "",
                        "description": desc.group(1).strip()[:200] if desc else ""
                    })
        except Exception as e:
            pins.append({"title": f"Pinterest RSS Fallback for {username}", "error": str(e), "link": ""})
        return pins

    @staticmethod
    def extract_instagram_reel_yt_dlp(reel_url: str) -> Dict[str, Any]:
        """Extracts reel metadata, title, audio stream, and duration via local yt-dlp binary."""
        try:
            cmd = ["yt-dlp", "--dump-json", "--no-warnings", reel_url]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=12, creationflags=0x08000000)
            if res.returncode == 0 and res.stdout:
                data = json.loads(res.stdout.splitlines()[0])
                return {
                    "id": data.get("id"),
                    "title": data.get("title", ""),
                    "description": data.get("description", ""),
                    "duration": data.get("duration", 0),
                    "uploader": data.get("uploader", ""),
                    "view_count": data.get("view_count", 0),
                    "status": "SUCCESS"
                }
            return {"error": res.stderr.strip() or "Non-zero exit code", "status": "FAILED"}
        except Exception as e:
            return {"error": str(e), "status": "FAILED"}
