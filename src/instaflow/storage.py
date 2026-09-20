"""
InstaFlow Storage Manager.
Persists processed items, conversations, and discovered tools to SQLite WAL and Central Blackboard.
"""

from __future__ import annotations
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from core.blackboard import Blackboard
except ImportError:
    Blackboard = None


class StorageManager:
    """Zero-dependency SQLite WAL storage and Central Blackboard bridge."""

    def __init__(self, target_dir: str, db_path: str):
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.bb = Blackboard() if Blackboard else None
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS processed_messages (
                    message_id TEXT PRIMARY KEY,
                    thread_id TEXT,
                    sender_handle TEXT,
                    category TEXT,
                    clean_content TEXT,
                    media_url TEXT,
                    processed_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS harvested_tools (
                    tool_name TEXT PRIMARY KEY,
                    category TEXT,
                    official_url TEXT,
                    creator_handle TEXT,
                    discovered_at TEXT
                )
            """)
            conn.commit()

    def is_message_processed(self, message_id: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM processed_messages WHERE message_id = ?", (message_id,))
            return cur.fetchone() is not None

    def store_item(
        self,
        message_id: str,
        thread_id: str,
        sender_handle: str,
        classified: Any,
        download_media: bool = False
    ) -> Dict[str, Any]:
        now_iso = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR IGNORE INTO processed_messages 
                (message_id, thread_id, sender_handle, category, clean_content, media_url, processed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                message_id,
                thread_id,
                sender_handle,
                classified.category,
                classified.clean_content,
                classified.media_url or "",
                now_iso
            ))
            conn.commit()

        if self.bb:
            try:
                self.bb.set(
                    f"instaflow:item:{message_id}",
                    {
                        "thread_id": thread_id,
                        "sender": sender_handle,
                        "category": classified.category,
                        "preview": classified.clean_content[:100],
                        "processed_at": now_iso
                    },
                    scope="instaflow"
                )
            except Exception:
                pass

        return {"status": "SUCCESS", "message_id": message_id}

    def get_stats(self) -> Dict[str, Any]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM processed_messages")
            total = cur.fetchone()[0]

            cur.execute("SELECT category, COUNT(*) FROM processed_messages GROUP BY category")
            by_category = dict(cur.fetchall())

            return {"total_processed": total, "by_category": by_category}
