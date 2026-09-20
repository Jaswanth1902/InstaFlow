"""
InstaFlow configuration loader.
Loads credentials and operating settings from environment variables or .env file.
"""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


def load_env_file(dotenv_path: Path) -> None:
    """Minimal standard library .env loader without third-party dependencies."""
    if not dotenv_path.is_file():
        return
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            if key not in os.environ:
                os.environ[key] = val


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
load_env_file(ENV_FILE)


def _get_allowed_senders() -> List[str]:
    raw = os.getenv("ALLOWED_SENDER_USERNAMES", "")
    return [s.strip().lower() for s in raw.split(",") if s.strip()]


@dataclass
class InstaFlowConfig:
    session_id: str = os.getenv("INSTAGRAM_SESSION_ID", "")
    ds_user_id: str = os.getenv("INSTAGRAM_DS_USER_ID", "")
    csrf_token: str = os.getenv("INSTAGRAM_CSRF_TOKEN", "")
    poll_interval: int = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
    poll_jitter: int = int(os.getenv("POLL_JITTER_SECONDS", "5"))
    inbox_target_dir: str = os.getenv(
        "INBOX_TARGET_DIR",
        str(PROJECT_ROOT / "data" / "inbox")
    )
    allowed_senders: List[str] = field(default_factory=_get_allowed_senders)
    download_reel_videos: bool = os.getenv("DOWNLOAD_REEL_VIDEOS", "false").lower() in ("true", "1", "yes")
    max_reel_size_mb: int = int(os.getenv("MAX_REEL_SIZE_MB", "150"))
    enable_interactive_replies: bool = os.getenv("ENABLE_INTERACTIVE_REPLIES", "true").lower() in ("true", "1", "yes")
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes")
    db_path: str = str(PROJECT_ROOT / "data" / "instaflow_ledger.db")


config = InstaFlowConfig()
