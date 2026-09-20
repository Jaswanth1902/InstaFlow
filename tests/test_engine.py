"""
Tests for InstaFlow Conversational Engine & Command Router.
"""

import sys
from pathlib import Path
import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from instaflow.engine import InstaFlowEngine


def test_command_help():
    engine = InstaFlowEngine()
    reply = engine.process_incoming_message("t1", "user1", "/help")
    assert reply is not None
    assert "/search" in reply
    assert "/account" in reply
    assert "/tools" in reply


def test_lead_magnet_code_trigger():
    engine = InstaFlowEngine()
    reply = engine.process_incoming_message("t2", "user2", "CODE")
    assert reply is not None
    assert "Notch" in reply
    assert "https://github.com/Jaswanth1902" in reply


def test_lead_magnet_notch_trigger():
    engine = InstaFlowEngine()
    reply = engine.process_incoming_message("t3", "user3", "notch")
    assert reply is not None
    assert "Dynamic Island" in reply
    assert "Jaswanth1902/Notch" in reply


def test_tools_catalog():
    engine = InstaFlowEngine()
    reply = engine.process_incoming_message("t4", "user4", "/tools")
    assert reply is not None
    assert "Top Harvested Developer Tools" in reply
    assert "DWEL" in reply


def test_multi_turn_state_search():
    engine = InstaFlowEngine()
    # Turn 1: user says /search without args
    prompt = engine.process_incoming_message("t5", "user5", "/search")
    assert "What niche" in prompt
    session = engine.sessions["t5"]
    assert session.awaiting_input_for == "search_query"

    # Turn 2: user provides niche
    result = engine.process_incoming_message("t5", "user5", "ai tools")
    assert result is not None
    assert session.awaiting_input_for is None


def test_natural_language_identity():
    engine = InstaFlowEngine()
    reply = engine.process_incoming_message("t6", "user6", "who are you?")
    assert reply is not None
    assert "InstaFlow" in reply
