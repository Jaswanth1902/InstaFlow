"""
InstaFlow Direct Message Poller.
Connects to Instagram Web Direct API using web session cookies with dry-run and synthetic simulation.
"""

from __future__ import annotations
import json
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .classifier import classify_message
    from .config import InstaFlowConfig
    from .engine import InstaFlowEngine
    from .storage import StorageManager
except ImportError:
    from classifier import classify_message
    from config import InstaFlowConfig
    from engine import InstaFlowEngine
    from storage import StorageManager

IG_INBOX_URL = "https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder=&limit=10"


class InstagramInboxPoller:
    """Manages Instagram Direct Message synchronization and automated replies."""

    def __init__(self, config: InstaFlowConfig, storage: StorageManager, enable_interactive: bool = True):
        self.config = config
        self.storage = storage
        self.engine = InstaFlowEngine() if enable_interactive else None

    def _ensure_csrf(self):
        if not self.config.csrf_token and self.config.session_id:
            try:
                url = "https://www.instagram.com/"
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Cookie": f"sessionid={self.config.session_id}; ds_user_id={self.config.ds_user_id}",
                    }
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    cookies = resp.info().get_all('Set-Cookie') or []
                    for c in cookies:
                        if "csrftoken=" in c:
                            self.config.csrf_token = c.split("csrftoken=")[1].split(";")[0]
                            break
            except Exception:
                pass

    def _build_headers(self) -> Dict[str, str]:
        self._ensure_csrf()
        cookies = [
            f"sessionid={self.config.session_id}",
            f"ds_user_id={self.config.ds_user_id}",
            f"csrftoken={self.config.csrf_token}",
        ]
        return {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
            ),
            "X-IG-App-ID": "936619743392459",
            "Cookie": "; ".join(cookies),
            "X-CSRFToken": self.config.csrf_token,
            "Referer": "https://www.instagram.com/direct/inbox/",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def send_direct_message(self, thread_id: str, text: str) -> bool:
        """Dispatches an interactive text response to an Instagram DM thread."""
        if getattr(self.config, "dry_run", False):
            print(f"[DRY-RUN] Direct message to thread {thread_id}:\n{text}")
            return True

        if not self.config.session_id:
            print(f"[!] Cannot send DM: No INSTAGRAM_SESSION_ID configured.")
            return False

        self._ensure_csrf()
        url = "https://www.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
        headers = self._build_headers()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Referer"] = f"https://www.instagram.com/direct/t/{thread_id}/"
        headers["Origin"] = "https://www.instagram.com"
        headers["X-Requested-With"] = "XMLHttpRequest"

        client_context = str(uuid.uuid4())
        post_data = {
            "action": "send_item",
            "thread_ids": f"[{thread_id}]",
            "client_context": client_context,
            "text": text,
            "mutation_token": client_context,
        }
        data = urllib.parse.urlencode(post_data).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                if res.get("status") == "ok":
                    print(f"[+] Direct message dispatched to thread {thread_id}")
                    return True
                else:
                    print(f"[!] DM dispatch non-ok response: {res}")
        except Exception as e:
            print(f"[!] Failed to send direct message to thread {thread_id}: {e}")
        return False

    def fetch_inbox_threads(self) -> Optional[Dict[str, Any]]:
        if not self.config.session_id:
            return None

        combined_threads = []
        for folder in ["", "pending"]:
            url = f"https://www.instagram.com/api/v1/direct_v2/inbox/?persistentBadging=true&folder={folder}&limit=10"
            req = urllib.request.Request(url, headers=self._build_headers())
            try:
                with urllib.request.urlopen(req, timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    threads = data.get("inbox", {}).get("threads", [])
                    combined_threads.extend(threads)
            except Exception:
                pass

        unique_threads = []
        seen_ids = set()
        for t in combined_threads:
            tid = t.get("thread_id")
            if tid not in seen_ids:
                seen_ids.add(tid)
                unique_threads.append(t)

        return {"inbox": {"threads": unique_threads}}

    def process_threads_payload(self, inbox_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        inbox = inbox_data.get("inbox", {})
        threads = inbox.get("threads", [])
        results = []

        for thread in threads:
            thread_id = thread.get("thread_id", "")
            users = {u.get("pk"): u.get("username") for u in thread.get("users", [])}
            items = thread.get("items", [])

            for item in items:
                item_id = str(item.get("item_id", ""))
                sender_id = str(item.get("user_id", ""))
                sender_handle = users.get(int(sender_id) if sender_id.isdigit() else sender_id, "user")

                if self.config.allowed_senders and sender_handle.lower() not in self.config.allowed_senders:
                    continue

                if self.storage.is_message_processed(item_id):
                    continue

                item_type = item.get("item_type", "text")
                text = item.get("text", "")

                classified = classify_message(text=text, item_type=item_type, raw_item=item)

                res = self.storage.store_item(
                    message_id=item_id,
                    thread_id=thread_id,
                    sender_handle=sender_handle,
                    classified=classified,
                    download_media=self.config.download_reel_videos
                )

                reply_sent = False
                reply_text = None
                is_self = sender_id == str(self.config.ds_user_id)

                if not is_self and getattr(self.config, "enable_interactive_replies", True) and self.engine:
                    reply_text = self.engine.process_incoming_message(
                        thread_id=thread_id,
                        sender_handle=sender_handle,
                        message_text=text
                    )
                    if reply_text:
                        reply_sent = self.send_direct_message(thread_id, reply_text)

                results.append({
                    "item_id": item_id,
                    "sender": sender_handle,
                    "category": classified.category,
                    "preview": classified.clean_content[:50],
                    "status": res.get("status"),
                    "reply_sent": reply_sent,
                    "reply_preview": (reply_text[:60] + "...") if reply_text else None
                })

        return results

    def poll_once(self) -> List[Dict[str, Any]]:
        data = self.fetch_inbox_threads()
        if not data:
            return []
        return self.process_threads_payload(data)

    def inject_synthetic_test(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Dry-run test simulator injecting synthetic messages."""
        results = []
        for idx, item in enumerate(items):
            item_id = item.get("item_id", f"mock_{idx}_{int(time.time())}")
            sender_handle = item.get("sender", "developer_test")
            thread_id = item.get("thread_id", "test_thread_001")
            text = item.get("text", "")
            item_type = item.get("item_type", "text")

            classified = classify_message(text=text, item_type=item_type, raw_item=item.get("raw", {}))

            res = self.storage.store_item(
                message_id=item_id,
                thread_id=thread_id,
                sender_handle=sender_handle,
                classified=classified,
                download_media=False
            )

            reply_text = None
            if self.engine:
                reply_text = self.engine.process_incoming_message(
                    thread_id=thread_id,
                    sender_handle=sender_handle,
                    message_text=text
                )

            results.append({
                "item_id": item_id,
                "sender": sender_handle,
                "category": classified.category,
                "preview": classified.clean_content[:50],
                "status": res.get("status"),
                "reply": reply_text
            })
        return results
