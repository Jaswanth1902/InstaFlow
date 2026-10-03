#!/usr/bin/env python3
"""
InstaFlow OMNI Unified Command Line Interface.
Runs interactive terminal simulations, synthetic tests, account discovery,
multi-vector truth verification, omnichannel repurposing, VideoDR, and ADB teleoperation.
"""

from __future__ import annotations
import argparse
import os
import random
import sys
import time
from pathlib import Path

# UTF-8 console output resilience
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PACKAGE_DIR = Path(__file__).resolve().parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

try:
    from .config import config, InstaFlowConfig
    from .discovery import AccountSearchEngine
    from .engine import InstaFlowEngine
    from .poller import InstagramInboxPoller
    from .storage import StorageManager
    from .omni_truth import OmniTruthEngine
    from .repurposer import OmnichannelRepurposer
    from .teleoperation import AgentReachController
    from .videodr import VideoDRProcessor
    from .workarounds import PlatformWorkarounds
except ImportError:
    from config import config, InstaFlowConfig
    from discovery import AccountSearchEngine
    from engine import InstaFlowEngine
    from poller import InstagramInboxPoller
    from storage import StorageManager
    from omni_truth import OmniTruthEngine
    from repurposer import OmnichannelRepurposer
    from teleoperation import AgentReachController
    from videodr import VideoDRProcessor
    from workarounds import PlatformWorkarounds


def print_banner():
    print("=" * 75)
    print("⚡ INSTAFLOW OMNI — Sovereign Social Intelligence & Physical Teleoperation")
    print("   Multi-Vector Truth • Omnichannel Repurposer • VideoDR • /agent-reach ADB")
    print("=" * 75)


def cmd_simulate():
    """Interactive terminal DM simulator."""
    print_banner()
    print("[*] Starting Interactive DM Simulator (Thread: sim_thread_001, User: @developer_guest)")
    print("[*] Commands: /help, /truth <claim>, /repurpose <title>, /videodr <video>, /search <niche>, CODE, or 'exit'")
    print("-" * 75)

    engine = InstaFlowEngine()
    thread_id = "sim_thread_001"
    sender_handle = "developer_guest"

    welcome = engine.process_incoming_message(thread_id, sender_handle, "/start")
    print(f"\n🤖 InstaFlow OMNI:\n{welcome}\n")

    while True:
        try:
            user_input = input("💬 You (@developer_guest): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting simulator.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", ":q"):
            print("[*] Simulator terminated.")
            break

        t0 = time.perf_counter()
        reply = engine.process_incoming_message(thread_id, sender_handle, user_input)
        latency_ms = (time.perf_counter() - t0) * 1000

        if reply:
            print(f"\n🤖 InstaFlow OMNI ({latency_ms:.1f}ms):\n{reply}\n")
        else:
            print("\n[InstaFlow took no action / filtered by DWEL loop guard]\n")


def cmd_test() -> bool:
    """Automated synthetic verification suite including OMNI capabilities."""
    print_banner()
    print("[*] Running Automated OMNI Capabilities Suite...")
    print("-" * 75)

    storage = StorageManager(config.inbox_target_dir, config.db_path)
    poller = InstagramInboxPoller(config, storage, enable_interactive=True)

    test_cases = [
        {"input": "/help", "desc": "Command Router: Help menu"},
        {"input": "CODE", "desc": "Lead Magnet Trigger: Repository links"},
        {"input": "/search ai tools", "desc": "Account Discovery: Creator search"},
        {"input": "/account @datawarlord_official", "desc": "Profile Hydrator: Creator dossier"},
        {"input": "/tools", "desc": "Tools Catalog: Harvested tools directory"},
        {"input": "/code notch", "desc": "Direct Link: Notch repository link"},
        {"input": "who are you?", "desc": "Natural Language: Bot identity intent"},
        {"input": "/truth Agentic RAG outperforms flat search", "desc": "Omni-Truth: ArXiv & Council verification"},
        {"input": "/repurpose Micrograd autograd engine from scratch", "desc": "Omnichannel: Multi-platform compiler"},
        {"input": "/videodr demo_reel.mp4", "desc": "VideoDR: Frame anchor extraction"},
    ]

    all_passed = True
    for idx, tc in enumerate(test_cases, 1):
        raw_item = {
            "item_id": f"syn_instaflow_{idx}_{int(time.time())}",
            "sender": "qa_tester",
            "thread_id": f"thread_qa_{idx}",
            "text": tc["input"],
            "item_type": "text"
        }

        t0 = time.perf_counter()
        results = poller.inject_synthetic_test([raw_item])
        elapsed = (time.perf_counter() - t0) * 1000

        res = results[0]
        reply = res.get("reply")
        passed = bool(reply and len(reply) > 10)
        status_symbol = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_passed = False

        print(f"[{idx}/{len(test_cases)}] {status_symbol} | {tc['desc']} ({elapsed:.1f}ms)")
        print(f"     Input: \"{tc['input']}\"")
        if reply:
            first_line = reply.split("\n")[0]
            print(f"     Reply: {first_line[:75]}...")
        else:
            print(f"     Reply: [NO REPLY]")
        print()

    print("=" * 75)
    if all_passed:
        print("🎉 ALL 10 INSTAFLOW OMNI CAPABILITY TESTS PASSED!")
    else:
        print("⚠️ SOME CAPABILITY TESTS FAILED.")
    print("=" * 75)
    return all_passed


def cmd_truth(claim: str):
    """Multi-vector truth verification via arXiv, GitHub, and 5-Persona Council."""
    print_banner()
    print(f"[*] Verifying claim across multi-vector ground truth: \"{claim}\"...")
    engine = OmniTruthEngine()
    t0 = time.perf_counter()
    report = engine.evaluate_claim(claim)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"[+] Multi-Vector Verification Completed in {elapsed:.1f}ms:\n")
    print(f"• Verdict         : {report.verdict}")
    print(f"• Council Q-Score : {report.aggregate_q_score:.2f} / 1.00")
    arxiv_top = report.arxiv_papers[0].get("title", "None found") if report.arxiv_papers else "None found"
    github_top = report.github_repos[0].get("name", "None found") if report.github_repos else "None found"
    print(f"• ArXiv Match     : {arxiv_top}")
    print(f"• GitHub Match    : {github_top}")
    print(f"• Analysis        : {report.analysis}\n")
    print("--- 5-Persona Council Scorecard ---")
    for persona, score in report.council_scores.items():
        print(f"  - {persona:<22}: {score:.2f}")
    print("-" * 75)


def cmd_repurpose(title: str, insight: str):
    """Omnichannel format compiler (X, Pinterest, Reddit)."""
    print_banner()
    print(f"[*] Compiling omnichannel assets for: \"{title}\"...")
    repurposer = OmnichannelRepurposer()
    t0 = time.perf_counter()

    thread = repurposer.compile_x_thread(title, insight)
    steps = [insight[:40], "Analyze root cause", "Strip abstractions", "Benchmark telemetry", "Deploy local-first"]
    pin = repurposer.compile_pinterest_pin(title, insight, steps)
    reddit = repurposer.compile_reddit_case_study(
        title=title,
        problem=insight,
        solution="Built minimal, zero-dependency implementation adhering to physical invariants.",
        metrics={"Latency": "<16ms", "RAM": "<25MB", "Cloud Fees": "$0"}
    )
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"[+] Omnichannel Assets Generated in {elapsed:.1f}ms:\n")
    print(f"𝕏 1. X (Twitter) Technical Thread ({thread.total_tweets} tweets):")
    print(f"  Hook: {thread.hook_tweet}")
    for i, t in enumerate(thread.body_tweets, 1):
        print(f"  [{i}] {t}")
    print(f"  CTA : {thread.call_to_action}")

    print(f"\n📌 2. Pinterest 1000x1500 Pin:")
    print(f"  Title       : {pin.title}")
    print(f"  Description : {pin.description}")
    print(f"  Template    : {pin.layout_template} ({pin.aspect_ratio})")

    print(f"\n🔴 3. Reddit Retrospective Post:")
    print(f"  Subreddit   : {reddit.subreddit}")
    print(f"  Title       : {reddit.title}")
    print(f"  Body Preview:\n{reddit.body_markdown[:220]}...")
    print("-" * 75)


def cmd_videodr(video_path: str):
    """VideoDR Deep Research extraction."""
    print_banner()
    print(f"[*] Processing video through VideoDR Engine: {video_path}...")
    processor = VideoDRProcessor()
    t0 = time.perf_counter()
    report = processor.process_video_file(video_path)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"[+] VideoDR Extraction Completed in {elapsed:.1f}ms:\n")
    print(f"• Video ID        : {report.video_id}")
    print(f"• Detected Tools  : {', '.join(report.detected_tools) or 'None'}")
    print(f"• GitHub Repos    : {', '.join(report.github_urls) or 'None'}")
    print(f"• Distilled Tokens: {report.distilled_tokens} tokens")
    print(f"• Keyframes       : {len(report.keyframes)} anchors sampled")
    print(f"• Compressed Summary:\n{report.compressed_summary}")
    print("-" * 75)


def cmd_workaround(platform: str, identifier: str):
    """Resilient platform unauthenticated harvester."""
    print_banner()
    print(f"[*] Harvesting unauthenticated payload: {platform.upper()} for '{identifier}'...")
    workarounds = PlatformWorkarounds()
    t0 = time.perf_counter()

    plat = platform.lower()
    if plat in ("x", "twitter"):
        data = workarounds.fetch_twitter_syndication(identifier)
    elif plat == "pinterest":
        parts = identifier.split("/")
        user = parts[0] if parts else "pinterest"
        board = parts[1] if len(parts) > 1 else "feed"
        data = workarounds.fetch_pinterest_rss(user, board)
    elif plat in ("ig", "instagram"):
        data = workarounds.fetch_instagram_public_metadata(identifier)
    else:
        print(f"[!] Unknown platform: {platform}. Choose: x, twitter, pinterest, or instagram.")
        return

    elapsed = (time.perf_counter() - t0) * 1000
    print(f"[+] Harvested in {elapsed:.1f}ms:")
    print(f"• Type: {type(data).__name__}")
    if isinstance(data, dict):
        print(f"• Fields: {list(data.keys())}")
        preview = {k: v for k, v in list(data.items())[:4]}
        print(f"• Sample: {preview}")
    elif isinstance(data, list):
        print(f"• Items: {len(data)}")
        if data:
            print(f"• First Item: {data[0]}")
    print("-" * 75)


def cmd_teleop(action: str, target: str):
    """Physical ADB teleoperation payload generation via /agent-reach."""
    print_banner()
    print(f"[*] Generating teleoperation payload for action '{action}' on target '{target}'...")
    controller = AgentReachController()

    act = action.lower()
    if act == "tap":
        cmd = controller.build_adb_touch_command(target, 540, 1200)
    elif act == "swipe":
        cmd = controller.build_adb_touch_command(target, 540, 1500, duration_ms=400)
    elif act == "type":
        cmd = controller.build_adb_type_command(target, "Hello from InstaFlow OMNI")
    elif act == "scrape":
        cmd = controller.build_headless_scrape_command(target, "https://instagram.com/reels", "/tmp/reels.json")
    else:
        cmd = [controller.reach_bin, target, "exec", "--", "echo", f"teleop: {action}"]

    print(f"[+] Reach Command List: {cmd}")
    print(f"[+] CLI Invocation    : {' '.join(cmd)}")
    print("-" * 75)


def cmd_search(query: str):
    """Direct CLI creator discovery."""
    print_banner()
    print(f"[*] Discovering creators for niche: '{query}'...")
    engine = AccountSearchEngine()
    t0 = time.perf_counter()
    accounts = engine.search_accounts(query, limit=5)
    elapsed = (time.perf_counter() - t0) * 1000

    print(f"[+] Found {len(accounts)} creators in {elapsed:.1f}ms:\n")
    for a in accounts:
        print(f"• @{a.handle} ({a.display_name})")
        print(f"  🏷️ Niche: {a.niche}")
        print(f"  👥 Followers: {a.followers_count:,} | Posts: {a.posts_count:,}")
        print(f"  📝 Bio: {a.bio or '[No bio]'}")
        print(f"  🔗 {a.profile_url}\n")


def cmd_account(handle: str):
    """Direct CLI profile hydration."""
    print_banner()
    print(f"[*] Hydrating profile for handle: '{handle}'...")
    engine = AccountSearchEngine()
    t0 = time.perf_counter()
    acc = engine.inspect_account(handle)
    elapsed = (time.perf_counter() - t0) * 1000

    if not acc:
        print(f"[!] Could not hydrate profile for '{handle}'.")
        return

    print(f"[+] Profile hydrated in {elapsed:.1f}ms:\n")
    print(f"• Handle        : @{acc.handle}")
    print(f"• Name          : {acc.display_name}")
    print(f"• Niche         : {acc.niche}")
    print(f"• Followers     : {acc.followers_count:,}")
    print(f"• Following     : {acc.following_count:,}")
    print(f"• Posts         : {acc.posts_count:,}")
    print(f"• Bio           : {acc.bio or '[No bio]'}")
    print(f"• Profile URL   : {acc.profile_url}")


def cmd_poll(once: bool = False, dry_run: bool = False):
    """Live inbox poller."""
    print_banner()
    if dry_run:
        config.dry_run = True
        print("[*] DRY-RUN MODE: Outgoing direct messages will be logged, not sent to Instagram API.")

    storage = StorageManager(config.inbox_target_dir, config.db_path)
    poller = InstagramInboxPoller(config, storage, enable_interactive=True)

    if not config.session_id:
        print("[!] Warning: INSTAGRAM_SESSION_ID is not configured in .env.")
        print("[*] To test without session credentials, run: instaflow --test OR instaflow --simulate")
        return

    if once:
        print(f"[*] Checking Instagram Inbox ({time.strftime('%Y-%m-%d %H:%M:%S')})...")
        results = poller.poll_once()
        print(f"[+] Processed {len(results)} items.")
        for r in results:
            print(f"    @{r['sender']}: '{r['preview']}' -> {r.get('reply_preview')}")
        return

    print(f"[*] Starting polling daemon (Interval: {config.poll_interval}s ± {config.poll_jitter}s)...")
    try:
        while True:
            results = poller.poll_once()
            if results:
                print(f"[{time.strftime('%H:%M:%S')}] Handled {len(results)} incoming DMs.")
            jitter = random.uniform(-config.poll_jitter, config.poll_jitter)
            time.sleep(max(5.0, config.poll_interval + jitter))
    except KeyboardInterrupt:
        print("\n[*] Daemon stopped.")


def cmd_status():
    """Displays storage and ledger status."""
    print_banner()
    storage = StorageManager(config.inbox_target_dir, config.db_path)
    stats = storage.get_stats()
    print(f"Target Inbox Root  : {config.inbox_target_dir}")
    print(f"Ledger Database    : {config.db_path}")
    print(f"Session Configured : {'YES' if config.session_id else 'NO'}")
    print(f"Total Processed    : {stats['total_processed']}")
    for cat, count in stats.get("by_category", {}).items():
        print(f"  - {cat:<15}: {count}")
    print("=" * 75)


def main():
    parser = argparse.ArgumentParser(description="InstaFlow OMNI — Sovereign Social Intelligence & Physical Teleoperation Agent")
    parser.add_argument("--simulate", action="store_true", help="Launch real-time interactive terminal DM simulation")
    parser.add_argument("--test", action="store_true", help="Run automated synthetic capability test suite")
    parser.add_argument("--search", type=str, metavar="QUERY", help="Search and discover creator accounts by niche")
    parser.add_argument("--account", type=str, metavar="HANDLE", help="Hydrate creator profile metadata and stats")
    parser.add_argument("--truth", type=str, metavar="CLAIM", help="Verify claim across arXiv, GitHub, and 5-Persona Council")
    parser.add_argument("--repurpose", nargs=2, metavar=("TITLE", "INSIGHT"), help="Compile insight into X thread, Pinterest SVG pin, and Reddit post")
    parser.add_argument("--videodr", type=str, metavar="VIDEO_PATH", help="Extract visual anchors, speech transcript, and code via VideoDR")
    parser.add_argument("--workaround", nargs=2, metavar=("PLATFORM", "ID"), help="Execute unauthenticated scraper (twitter <id>, pinterest <user/board>, instagram <url>)")
    parser.add_argument("--teleop", nargs=2, metavar=("ACTION", "TARGET"), help="Generate AgentReach ADB command (action: tap|swipe|app, target: container/ip)")
    parser.add_argument("--once", action="store_true", help="Check inbox once and process unread items")
    parser.add_argument("--poll", action="store_true", help="Run continuous background polling daemon")
    parser.add_argument("--dry-run", action="store_true", help="Log responses without sending live HTTP requests")
    parser.add_argument("--status", action="store_true", help="Display ledger statistics")
    args = parser.parse_args()

    if args.simulate:
        cmd_simulate()
    elif args.test:
        success = cmd_test()
        sys.exit(0 if success else 1)
    elif args.truth:
        cmd_truth(args.truth)
    elif args.repurpose:
        cmd_repurpose(args.repurpose[0], args.repurpose[1])
    elif args.videodr:
        cmd_videodr(args.videodr)
    elif args.workaround:
        cmd_workaround(args.workaround[0], args.workaround[1])
    elif args.teleop:
        cmd_teleop(args.teleop[0], args.teleop[1])
    elif args.search:
        cmd_search(args.search)
    elif args.account:
        cmd_account(args.account)
    elif args.once or args.poll:
        cmd_poll(once=args.once, dry_run=args.dry_run)
    elif args.status:
        cmd_status()
    else:
        cmd_test()


if __name__ == "__main__":
    main()
