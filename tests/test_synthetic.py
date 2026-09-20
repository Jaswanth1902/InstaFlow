"""
Tests for InstaFlow Synthetic Inbox Polling & Flow Execution.
"""

import sys
import tempfile
from pathlib import Path
import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from instaflow.config import InstaFlowConfig
from instaflow.storage import StorageManager
from instaflow.poller import InstagramInboxPoller


def test_synthetic_flow():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        tmp_path = Path(tmp_dir)
        cfg = InstaFlowConfig(
            inbox_target_dir=str(tmp_path / "inbox"),
            db_path=str(tmp_path / "test.db"),
            dry_run=True,
            enable_interactive_replies=True
        )
        storage = StorageManager(cfg.inbox_target_dir, cfg.db_path)
        poller = InstagramInboxPoller(cfg, storage, enable_interactive=True)

        items = [
            {"item_id": "m1", "sender": "user1", "thread_id": "t1", "text": "/help", "item_type": "text"},
            {"item_id": "m2", "sender": "user2", "thread_id": "t2", "text": "CODE", "item_type": "text"},
            {"item_id": "m3", "sender": "user3", "thread_id": "t3", "text": "task: review pr", "item_type": "text"},
        ]

        results = poller.inject_synthetic_test(items)
        assert len(results) == 3
        assert results[0]["category"] == "COMMAND"
        assert "/search" in results[0]["reply"]
        assert results[1]["category"] == "LEAD_TRIGGER"
        assert "Notch" in results[1]["reply"]
        assert results[2]["category"] == "TASK"

        stats = storage.get_stats()
        assert stats["total_processed"] == 3
