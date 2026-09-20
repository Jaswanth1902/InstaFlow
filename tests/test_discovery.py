"""
Tests for InstaFlow Account Discovery & Creator Profile Hydrator.
"""

import sys
from pathlib import Path
import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from instaflow.discovery import AccountSearchEngine, InstagramAccount


def test_extract_handle_from_url():
    engine = AccountSearchEngine()
    handle = engine._extract_handle_from_url("https://www.instagram.com/datawarlord_official/")
    assert handle == "datawarlord_official"


def test_excluded_handles():
    engine = AccountSearchEngine()
    handle = engine._extract_handle_from_url("https://www.instagram.com/explore/")
    assert handle is None


def test_parse_count():
    engine = AccountSearchEngine()
    assert engine._parse_count("262K") == 262000
    assert engine._parse_count("1.5M") == 1500000
    assert engine._parse_count("534") == 534


def test_classify_niche():
    engine = AccountSearchEngine()
    assert engine._classify_niche("AI agents and LLMs") == "AI & Agents"
    assert engine._classify_niche("Python scripts and fastapi") == "Python & Backend"
    assert engine._classify_niche("React components and CSS") == "Web Development"


def test_inspect_account_live():
    engine = AccountSearchEngine()
    acc = engine.inspect_account("datawarlord_official")
    assert acc is not None
    assert acc.handle == "datawarlord_official"
    assert acc.followers_count > 100000
