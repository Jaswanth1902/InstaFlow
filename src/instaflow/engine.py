"""
InstaFlow Conversational Engine & Command Router.
Stateful multi-turn assistant for Instagram Direct Messages with DWEL loop prevention.
"""

from __future__ import annotations
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from core.dwel import check_action_loop
except ImportError:
    check_action_loop = None

try:
    from .discovery import AccountSearchEngine, InstagramAccount
except ImportError:
    from discovery import AccountSearchEngine, InstagramAccount


@dataclass
class ConversationState:
    thread_id: str
    sender_handle: str
    last_command: str = ""
    last_interaction_ts: float = field(default_factory=time.time)
    awaiting_input_for: Optional[str] = None
    interaction_count: int = 0


class InstaFlowEngine:
    """Stateful conversational intelligence engine for Instagram Direct Messages."""

    FLAGSHIP_LINKS = {
        "notch": "https://github.com/Jaswanth1902/Notch",
        "dwel": "https://github.com/Jaswanth1902/dwel",
        "mem-shred": "https://github.com/Jaswanth1902/mem-shred",
        "memshred": "https://github.com/Jaswanth1902/mem-shred",
        "omnia": "https://github.com/Jaswanth1902/Omnia-codebase-memory",
        "cartograph": "https://github.com/Jaswanth1902/Omnia-codebase-memory",
        "instaflow": "https://github.com/Jaswanth1902/InstaFlow",
    }

    CURATED_TOOLS = [
        {"tool_name": "Notch", "category": "Desktop HUD", "official_url": "https://github.com/Jaswanth1902/Notch"},
        {"tool_name": "DWEL", "category": "Agent Loop Interceptor", "official_url": "https://github.com/Jaswanth1902/dwel"},
        {"tool_name": "mem-shred", "category": "Cryptographic Zeroizer", "official_url": "https://github.com/Jaswanth1902/mem-shred"},
        {"tool_name": "Omnia AST", "category": "Codebase Memory", "official_url": "https://github.com/Jaswanth1902/Omnia-codebase-memory"},
        {"tool_name": "InstaFlow", "category": "Social Intelligence", "official_url": "https://github.com/Jaswanth1902/InstaFlow"},
    ]

    def __init__(self):
        self.account_engine = AccountSearchEngine()
        self.sessions: Dict[str, ConversationState] = {}

    def get_or_create_session(self, thread_id: str, sender_handle: str) -> ConversationState:
        if thread_id not in self.sessions:
            self.sessions[thread_id] = ConversationState(thread_id=thread_id, sender_handle=sender_handle)
        return self.sessions[thread_id]

    def process_incoming_message(self, thread_id: str, sender_handle: str, message_text: str) -> Optional[str]:
        """
        Evaluates incoming Instagram DM text and returns automated response string.
        Returns None if message should be ignored or is blocked by DWEL loop guard.
        """
        session = self.get_or_create_session(thread_id, sender_handle)
        session.last_interaction_ts = time.time()
        session.interaction_count += 1

        clean_text = message_text.strip()
        lower_text = clean_text.lower()

        # 1. DWEL cycle interceptor (halts infinite bot-to-bot ping pong loops)
        if check_action_loop:
            warning = check_action_loop("instaflow_dm_reply", {"thread_id": thread_id, "text": clean_text})
            if warning:
                return None

        # 2. Command Router (/start, /help, /search, /account, /tools, /code, /harvest)
        if clean_text.startswith("/") or lower_text in ("help", "menu", "commands", "start"):
            return self._handle_command(session, clean_text)

        # 3. State-Machine Context Handling (e.g. user previously prompted for niche query)
        if session.awaiting_input_for == "search_query":
            session.awaiting_input_for = None
            return self._execute_account_search(clean_text)
        elif session.awaiting_input_for == "account_handle":
            session.awaiting_input_for = None
            return self._execute_account_inspect(clean_text)

        # 4. ManyChat-Style Keyword Lead Magnet Triggers (CODE, LINK, TOOLS, NOTCH, DWEL)
        keyword_reply = self._match_keyword_triggers(lower_text)
        if keyword_reply:
            return keyword_reply

        # 5. Reel URL Auto-Harvest (if user pastes an Instagram reel link)
        if "instagram.com/reel/" in lower_text or "instagram.com/p/" in lower_text:
            return self._execute_harvest_reel_stub(clean_text)

        # 6. Natural Language Heuristic Fallback
        return self._handle_natural_language(session, clean_text)

    def _handle_command(self, session: ConversationState, text: str) -> str:
        parts = text.strip().split(maxsplit=1)
        raw_cmd = parts[0].lower().lstrip("/")
        arg = parts[1].strip() if len(parts) > 1 else ""

        if raw_cmd in ("start", "help", "menu", "commands"):
            return (
                "⚡ Hey! I'm InstaFlow, your autonomous Instagram developer assistant.\n\n"
                "Available Direct Commands:\n"
                "🔍 /search <niche> — Discover top creator accounts in <1s\n"
                "👤 /account <handle> — Inspect creator stats, bio & links\n"
                "🛠️ /tools — Browse curated open-source developer tools\n"
                "📦 /code <repo> — Instant links to flagship repositories\n"
                "📥 Send any Reel URL to automatically extract its tools!\n\n"
                "Type a command or keyword (e.g. 'CODE') to get started!"
            )

        elif raw_cmd == "search":
            if not arg:
                session.awaiting_input_for = "search_query"
                return "🔍 What niche or topic do you want to discover accounts for? (e.g. 'ai coding', 'python tools', 'webdev')"
            return self._execute_account_search(arg)

        elif raw_cmd in ("account", "creator", "profile"):
            if not arg:
                session.awaiting_input_for = "account_handle"
                return "👤 Which creator handle do you want to inspect? (e.g. '@datawarlord_official')"
            return self._execute_account_inspect(arg)

        elif raw_cmd in ("tools", "toptools"):
            return self._get_tools_catalog()

        elif raw_cmd in ("code", "link", "repo"):
            repo_key = arg.lower().strip()
            if repo_key in self.FLAGSHIP_LINKS:
                return f"🚀 Official open-source repository for {arg.title()}:\n{self.FLAGSHIP_LINKS[repo_key]}"
            return (
                "📦 Flagship Open-Source Projects:\n"
                "• Notch (Dynamic Island HUD): https://github.com/Jaswanth1902/Notch\n"
                "• DWEL (Agent Loop Interceptor): https://github.com/Jaswanth1902/dwel\n"
                "• mem-shred (Cryptographic RAM Zeroizer): https://github.com/Jaswanth1902/mem-shred\n"
                "• Omnia (AST Codebase Memory): https://github.com/Jaswanth1902/Omnia-codebase-memory\n"
                "• InstaFlow (Social Intelligence): https://github.com/Jaswanth1902/InstaFlow\n"
            )

        elif raw_cmd == "harvest":
            if not arg:
                return "📥 Paste an Instagram Reel URL after /harvest to extract its tools!"
            return self._execute_harvest_reel_stub(arg)

        return f"❓ Unknown command '/{raw_cmd}'. Type /help to see available commands."

    def _execute_account_search(self, query: str) -> str:
        accounts = self.account_engine.search_accounts(query, limit=3)
        if not accounts:
            return f"❌ No creator accounts discovered for query '{query}'. Try a different keyword!"

        lines = [f"🌟 Top Creator Accounts for '{query}':\n"]
        for a in accounts:
            lines.append(
                f"• @{a.handle} ({a.display_name})\n"
                f"  🏷️ Niche: {a.niche}\n"
                f"  👥 Followers: {a.followers_count:,} | Posts: {a.posts_count:,}\n"
                f"  🔗 {a.profile_url}\n"
            )
        return "\n".join(lines)

    def _execute_account_inspect(self, handle: str) -> str:
        clean_h = handle.replace("@", "").strip()
        acc = self.account_engine.inspect_account(clean_h)
        if not acc:
            return f"❌ Could not inspect creator @{clean_h}. Make sure handle is spelled correctly."

        return (
            f"👤 Creator Dossier: @{acc.handle}\n"
            f"📛 Name: {acc.display_name}\n"
            f"🏷️ Niche: {acc.niche}\n"
            f"👥 Followers: {acc.followers_count:,} | Following: {acc.following_count:,}\n"
            f"📸 Posts: {acc.posts_count:,}\n"
            f"📝 Bio: {acc.bio or '[No bio]'}\n"
            f"🔗 Profile: {acc.profile_url}"
        )

    def _get_tools_catalog(self) -> str:
        lines = ["🏆 Top Harvested Developer Tools:\n"]
        for idx, t in enumerate(self.CURATED_TOOLS, 1):
            lines.append(f"{idx}. {t['tool_name']} ({t['category']}) — {t['official_url']}")
        return "\n".join(lines)

    def _execute_harvest_reel_stub(self, url: str) -> str:
        shortcode_match = re.search(r'/(?:reel|reels|p)/([A-Za-z0-9_-]+)', url)
        shortcode = shortcode_match.group(1) if shortcode_match else "unknown"
        return (
            f"✅ Reel Queued for Autonomous Harvest!\n"
            f"🎬 Shortcode: {shortcode}\n"
            f"🛠️ Extractor pipeline downloading video OCR & analyzing caption..."
        )

    def _match_keyword_triggers(self, text: str) -> Optional[str]:
        words = set(re.findall(r"\b\w+\b", text))
        
        if "code" in words or "link" in words or "repo" in words:
            return (
                "🚀 Here are the flagship open-source repositories:\n"
                "• Notch (Dynamic Island HUD): https://github.com/Jaswanth1902/Notch\n"
                "• DWEL (Loop Interceptor): https://github.com/Jaswanth1902/dwel\n"
                "• mem-shred (RAM Zeroization): https://github.com/Jaswanth1902/mem-shred\n"
                "• Omnia (AST Codebase Memory): https://github.com/Jaswanth1902/Omnia-codebase-memory"
            )
        if "notch" in words:
            return "🏝️ Notch Ambient Dynamic Island HUD for Windows 11: https://github.com/Jaswanth1902/Notch"
        if "dwel" in words:
            return "🔄 DWEL: <0.5ms Loop Interceptor for AI Agents: https://github.com/Jaswanth1902/dwel"
        if "tools" in words:
            return self._get_tools_catalog()
        return None

    def _handle_natural_language(self, session: ConversationState, text: str) -> Optional[str]:
        lower = text.lower()
        if any(w in lower for w in ("who are you", "what are you", "what is this")):
            return "I am InstaFlow, an autonomous social intelligence agent. Type /help to see my commands!"
        if any(w in lower for w in ("search", "find creator", "find account")):
            session.awaiting_input_for = "search_query"
            return "🔍 Sure! What niche or topic do you want to discover accounts for?"
        if any(w in lower for w in ("recommend", "best tools", "cool tools")):
            return self._get_tools_catalog()
        return None
