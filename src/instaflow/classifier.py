"""
InstaFlow Message Classifier.
Categorizes incoming Instagram Direct Messages into: COMMAND, LEAD_TRIGGER, REEL, TASK, REMINDER, RESOURCE, NOTE.
"""

from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional, Any, Dict, List

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def ig_id_to_shortcode(media_id: int) -> str:
    """Converts a 64-bit Instagram numeric media ID to an 11-character URL shortcode."""
    code = ""
    while media_id > 0:
        media_id, rem = divmod(media_id, 64)
        code = ALPHABET[rem] + code
    return code


@dataclass
class ClassifiedMessage:
    category: str  # "COMMAND", "LEAD_TRIGGER", "REEL", "TASK", "REMINDER", "RESOURCE", "NOTE"
    clean_content: str
    media_url: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = None


REEL_URL_REGEX = re.compile(
    r"(https?://(?:www\.)?instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)/?)",
    re.IGNORECASE
)

TASK_PREFIX_REGEX = re.compile(
    r"^(?:task|todo|test|action|must|\[\s*\]|-\s*\[\s*\])(?::|\s+)\s*",
    re.IGNORECASE
)

REMINDER_PREFIX_REGEX = re.compile(
    r"^(?:remind\s*me\s*to|remind\s*me|remind|reminder|alarm)(?::|\s+)\s*",
    re.IGNORECASE
)

LEAD_KEYWORD_REGEX = re.compile(
    r"^(?:code|link|notch|dwel|tools|guide|brain|setup|repo|prompt)$",
    re.IGNORECASE
)


def classify_message(
    text: str = "",
    item_type: str = "text",
    raw_item: Optional[Dict[str, Any]] = None
) -> ClassifiedMessage:
    """Classifies an incoming Instagram message into a structured category."""
    text = (text or "").strip()
    raw_item = raw_item or {}

    # 1. Check for interactive slash commands
    if text.startswith("/") or text.lower() in ("help", "start", "menu", "commands"):
        return ClassifiedMessage(
            category="COMMAND",
            clean_content=text,
            extra_metadata={"command": text.split()[0].lower()}
        )

    # 2. Check for ManyChat keyword lead triggers
    if LEAD_KEYWORD_REGEX.match(text):
        return ClassifiedMessage(
            category="LEAD_TRIGGER",
            clean_content=text,
            extra_metadata={"keyword": text.upper()}
        )

    # 3. Check for Reels / Video attachments
    media_share = raw_item.get("media_share", {})
    if item_type == "media_share" or media_share:
        code = media_share.get("code", "")
        caption_dict = media_share.get("caption") or {}
        caption_text = caption_dict.get("text", "") if isinstance(caption_dict, dict) else str(caption_dict)
        user_dict = media_share.get("user", {})
        creator_handle = user_dict.get("username", "")

        return ClassifiedMessage(
            category="REEL",
            clean_content=f"Instagram Reel: https://www.instagram.com/reel/{code}/",
            media_url=f"https://www.instagram.com/reel/{code}/" if code else None,
            extra_metadata={
                "shortcode": code,
                "creator": creator_handle,
                "caption": caption_text,
                "media_id": media_share.get("id"),
            }
        )

    # 4. Check for Reel URL in text
    reel_match = REEL_URL_REGEX.search(text)
    if reel_match:
        full_url = reel_match.group(1)
        shortcode = reel_match.group(2)
        return ClassifiedMessage(
            category="REEL",
            clean_content=text,
            media_url=full_url,
            extra_metadata={"shortcode": shortcode}
        )

    # 5. Check for Tasks
    task_match = TASK_PREFIX_REGEX.search(text)
    if task_match:
        clean = text[task_match.end():].strip()
        return ClassifiedMessage(
            category="TASK",
            clean_content=clean,
            extra_metadata={"raw_prefix": task_match.group(0).strip()}
        )

    # 6. Check for Reminders
    reminder_match = REMINDER_PREFIX_REGEX.search(text)
    if reminder_match:
        clean = text[reminder_match.end():].strip()
        return ClassifiedMessage(
            category="REMINDER",
            clean_content=clean,
            extra_metadata={"raw_prefix": reminder_match.group(0).strip()}
        )

    # 7. Check for general URL / Resource
    if "http://" in text or "https://" in text:
        return ClassifiedMessage(
            category="RESOURCE",
            clean_content=text,
            extra_metadata={"has_link": True}
        )

    # 8. Default: NOTE
    return ClassifiedMessage(
        category="NOTE",
        clean_content=text
    )
