"""Unit tests for platform workarounds in InstaFlow."""

import sys
from pathlib import Path
import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from instaflow.workarounds import PlatformWorkarounds


def test_twitter_syndication_workaround():
    # Test unauthenticated tweet extraction
    res = PlatformWorkarounds.fetch_twitter_syndication(tweet_id="20", timeout=5)
    assert "status" in res
    if res["status"] == "SUCCESS":
        assert res["author"] == "jack"
        assert "just setting up my twttr" in res["text"]


def test_pinterest_rss_workaround():
    # Test unauthenticated Pinterest RSS extraction
    pins = PlatformWorkarounds.fetch_pinterest_rss(username="pinterest", timeout=5)
    assert isinstance(pins, list)
    assert len(pins) > 0
    assert "title" in pins[0]


def test_instagram_yt_dlp_workaround():
    # Test with invalid url to verify clean error handling without crashing
    res = PlatformWorkarounds.extract_instagram_reel_yt_dlp("https://instagram.com/reel/invalid_mock_test")
    assert "status" in res
    assert res["status"] in ("SUCCESS", "FAILED")
