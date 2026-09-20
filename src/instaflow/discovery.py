"""
InstaFlow Account Discovery & Creator Profile Hydrator.
Discovers creator accounts by keyword/niche via search engine dorking and hydrates profiles in <1s.
"""

from __future__ import annotations
import html as html_lib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Central Blackboard optional import
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from core.blackboard import Blackboard
except ImportError:
    Blackboard = None


@dataclass
class InstagramAccount:
    handle: str
    display_name: str = ""
    bio: str = ""
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    external_url: str = ""
    niche: str = "Developer"
    profile_url: str = ""
    is_verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AccountSearchEngine:
    """Discovers and hydrates Instagram creator accounts without requiring login or API keys."""

    SOCIAL_HEADERS = {
        "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    DDG_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://duckduckgo.com/",
    }

    EXCLUDED_HANDLES = {
        "p", "reel", "reels", "explore", "stories", "tv", "accounts", "about",
        "developer", "legal", "terms", "privacy", "directory", "tags", "locations"
    }

    def __init__(self, blackboard: Optional[Blackboard] = None):
        self.bb = blackboard or (Blackboard() if Blackboard else None)

    def search_accounts(self, query: str, limit: int = 5, timeout_sec: float = 10.0) -> List[InstagramAccount]:
        """Discovers creator accounts by keyword/topic using search engine dorking."""
        discovered_handles: List[str] = []
        clean_query = query.strip()
        encoded_q = urllib.parse.quote_plus(f"site:instagram.com {clean_query}")
        ddg_url = f"https://html.duckduckgo.com/html/?q={encoded_q}"

        req = urllib.request.Request(ddg_url, headers=self.DDG_HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                html = resp.read().decode("utf-8", errors="replace")

            # Extract URLs from DDG result snippets
            raw_urls = re.findall(r'href="(?:/l/\?uddg=)?(https?%3A%2F%2F[^"&]+|https?://[^"&]+)', html)
            for u in raw_urls:
                decoded_u = urllib.parse.unquote(u) if "%3A" in u else u
                handle = self._extract_handle_from_url(decoded_u)
                if handle and handle not in discovered_handles and handle not in self.EXCLUDED_HANDLES:
                    discovered_handles.append(handle)
                    if len(discovered_handles) >= limit * 2:
                        break

            # Fallback regex for direct profile links
            if not discovered_handles:
                matches = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})/?', html)
                for m in matches:
                    low = m.lower()
                    if low not in self.EXCLUDED_HANDLES and low not in discovered_handles:
                        discovered_handles.append(low)
                        if len(discovered_handles) >= limit * 2:
                            break
        except Exception:
            pass

        accounts: List[InstagramAccount] = []
        for handle in discovered_handles[:limit]:
            acc = self.inspect_account(handle, niche_hint=query)
            if acc:
                accounts.append(acc)

        return accounts

    def inspect_account(self, handle: str, niche_hint: str = "Developer", timeout_sec: float = 6.0) -> Optional[InstagramAccount]:
        """Hydrates account metadata (bio, followers, posts, name) via OpenGraph preview."""
        clean_handle = handle.replace("@", "").strip().lower()
        if not clean_handle or clean_handle in self.EXCLUDED_HANDLES:
            return None

        url = f"https://www.instagram.com/{clean_handle}/"
        req = urllib.request.Request(url, headers=self.SOCIAL_HEADERS)

        try:
            with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
                html = resp.read().decode("utf-8", errors="replace")
        except Exception:
            return None

        desc_match = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', html, re.I)
        title_match = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html, re.I)

        followers = 0
        following = 0
        posts = 0
        bio = ""
        display_name = clean_handle

        if desc_match:
            raw_desc = html_lib.unescape(desc_match.group(1))
            stat_match = re.search(r'([\d\.,KMkm]+)\s+Followers,\s+([\d\.,KMkm]+)\s+Following,\s+([\d\.,KMkm]+)\s+Posts', raw_desc)
            if stat_match:
                followers = self._parse_count(stat_match.group(1))
                following = self._parse_count(stat_match.group(2))
                posts = self._parse_count(stat_match.group(3))
            
            if "See Instagram photos and videos from" in raw_desc:
                parts = raw_desc.split("photos and videos from", 1)
                if len(parts) > 1:
                    bio = parts[1].strip().lstrip("-").strip()
            elif "-" in raw_desc:
                bio_part = raw_desc.split("-", 1)[-1].strip()
                if not any(k in bio_part for k in ["Followers", "Following", "Posts"]):
                    bio = bio_part

        if title_match:
            raw_title = html_lib.unescape(title_match.group(1))
            name_match = re.match(r'^(.*?)\s*\(@', raw_title)
            if name_match:
                display_name = name_match.group(1).strip()

        account = InstagramAccount(
            handle=clean_handle,
            display_name=display_name,
            bio=bio[:300],
            followers_count=followers,
            following_count=following,
            posts_count=posts,
            profile_url=url,
            niche=self._classify_niche(f"{display_name} {bio} {niche_hint}")
        )

        if self.bb:
            try:
                self.bb.set(
                    f"instaflow:creator:{clean_handle}",
                    account.to_dict(),
                    scope="instaflow"
                )
            except Exception:
                pass

        return account

    def _extract_handle_from_url(self, url: str) -> Optional[str]:
        m = re.search(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})(?:/|\?|$)', url)
        if m:
            h = m.group(1).lower()
            if h not in self.EXCLUDED_HANDLES:
                return h
        return None

    def _parse_count(self, text: str) -> int:
        t = text.strip().upper().replace(",", "")
        multiplier = 1
        if "K" in t:
            multiplier = 1000
            t = t.replace("K", "")
        elif "M" in t:
            multiplier = 1000000
            t = t.replace("M", "")
        try:
            return int(float(t) * multiplier)
        except ValueError:
            return 0

    def _classify_niche(self, text: str) -> str:
        low = text.lower()
        if any(w in low for w in ("ai", "agent", "llm", "machine learning", "deep learning", "neural")):
            return "AI & Agents"
        if any(w in low for w in ("python", "scripting", "backend", "fastapi", "django")):
            return "Python & Backend"
        if any(w in low for w in ("web", "frontend", "react", "nextjs", "javascript", "css", "ui")):
            return "Web Development"
        if any(w in low for w in ("devops", "cloud", "docker", "kubernetes", "aws", "linux")):
            return "DevOps & Infrastructure"
        if any(w in low for w in ("tool", "productivity", "automation", "workflow", "system")):
            return "Developer Tools"
        return "Developer"
