"""Unit tests for InstaFlow OMNI capabilities."""

import sys
from pathlib import Path
import pytest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from instaflow.omni_truth import OmniTruthEngine, TruthVerdict
from instaflow.teleoperation import AgentReachController
from instaflow.repurposer import OmnichannelRepurposer
from instaflow.videodr import VideoDRProcessor


def test_omni_truth_evaluation():
    engine = OmniTruthEngine(timeout=5)
    
    # Valid technical claim
    verdict = engine.evaluate_claim("Speculative decoding in local LLMs with KV cache reuse")
    assert isinstance(verdict, TruthVerdict)
    assert verdict.aggregate_q_score >= 0.80
    assert "architect" in verdict.council_scores
    assert "contrarian" in verdict.council_scores
    
    # Spam / crypto claim
    bad_verdict = engine.evaluate_claim("Guaranteed 100x free money crypto bot")
    assert bad_verdict.verdict == "REJECTED_SLOP"
    assert bad_verdict.aggregate_q_score < 0.70


def test_agent_reach_controller_commands():
    controller = AgentReachController(reach_bin="reach")
    
    # Physical ADB touch
    touch_cmd = controller.build_adb_touch_command("android-worker-1", 540, 1200, 150)
    assert "reach" in touch_cmd[0]
    assert touch_cmd[1] == "android-worker-1"
    assert "swipe" in touch_cmd
    assert "1200" in touch_cmd
    
    # Text typing
    type_cmd = controller.build_adb_type_command("android-worker-1", "hello world")
    assert "hello%sworld" in type_cmd[-1]
    
    # Headless scraping worker
    scrape_cmd = controller.build_headless_scrape_command("scraper-node-0", "https://instagram.com/p/test", "out.md")
    assert "stealthy-fetch" in scrape_cmd


def test_omnichannel_repurposer_x_thread():
    thread = OmnichannelRepurposer.compile_x_thread(
        title="SQLite WAL Mode",
        core_insight="Enabling WAL mode allows concurrent readers without blocking writes.",
        code_snippet="PRAGMA journal_mode=WAL;\nPRAGMA synchronous=NORMAL;"
    )
    assert thread.total_tweets >= 5
    assert "🧵👇" in thread.hook_tweet
    assert "journal_mode=WAL" in thread.body_tweets[2]


def test_omnichannel_repurposer_pinterest_pin():
    pin = OmnichannelRepurposer.compile_pinterest_pin(
        title="FastAPI + SQLite Architecture",
        summary="High-performance local microservices under 20ms response times.",
        steps=["Setup SQLite WAL database", "Define Pydantic schemas", "Wire async connection pool", "Profile memory bounds"]
    )
    assert pin.aspect_ratio == "2:3"
    assert "<svg" in pin.visual_blueprint_svg
    assert "developer cheat sheet" in pin.keywords
    assert "FastAPI + SQLite Architecture" in pin.title


def test_omnichannel_repurposer_reddit_case_study():
    post = OmnichannelRepurposer.compile_reddit_case_study(
        title="Why we abandoned ManyChat for local Python daemons",
        problem="Frequent token invalidations, $50/mo fee, and zero developer intelligence.",
        solution="Built InstaFlow with sub-16ms direct polling and DWEL cycle detection.",
        metrics={"Latency": "14.2ms", "RAM": "21MB", "Cost": "$0"}
    )
    assert post.subreddit == "r/LocalLLaMA"
    assert "### Background & Context" in post.body_markdown
    assert "- **Latency**: 14.2ms" in post.body_markdown


def test_videodr_processor():
    report = VideoDRProcessor.process_reel(
        video_id="reel_12345",
        speech_transcript="Check out this new tool built on top of FastAPI and Docker at https://github.com/test/repo",
        ocr_frames=[
            {"timestamp_sec": 4.5, "text": "def init():\n    return FastAPI()", "anchor_type": "code_editor"},
            {"timestamp_sec": 12.0, "text": "docker run -p 8000:8000 app", "anchor_type": "terminal"}
        ]
    )
    assert report.video_id == "reel_12345"
    assert "fastapi" in report.detected_tools
    assert "docker" in report.detected_tools
    assert "https://github.com/test/repo" in report.github_urls
    assert len(report.keyframes) == 2
    assert report.distilled_tokens < 400


def test_agentverse_bridge_manifest_and_envelopes():
    from instaflow.agentverse_bridge import AgentverseBridge, AgentverseMessageEnvelope
    
    bridge = AgentverseBridge(agent_name="instaflow_test_node")
    assert bridge.agent_address.startswith("agent1q")
    assert len(bridge.agent_address) > 10
    
    # Manifest verification
    manifest = bridge.export_agent_manifest()
    assert manifest["name"] == "instaflow_test_node"
    assert manifest["protocol"]["name"] == "instaflow_social_intelligence_v1"
    assert len(manifest["capabilities"]) >= 3
    assert manifest["economic_model"]["cloud_spend"] == 0.0

    # Inbound envelope
    inbound = bridge.wrap_incoming_request(
        sender="agent1q999xyz",
        action="verify_truth",
        params={"claim": "Test claim"}
    )
    assert inbound.target_address == bridge.agent_address
    assert inbound.message_type == "verify_truth"
    
    # Outbound envelope
    outbound = bridge.wrap_outgoing_response(
        target="agent1q999xyz",
        action="verify_truth",
        result={"verdict": "APPROVED", "q_score": 0.92}
    )
    assert outbound.message_type == "verify_truth_response"
    assert "payload" in outbound.to_json()
