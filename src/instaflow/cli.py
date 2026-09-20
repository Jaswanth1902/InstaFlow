#!/usr/bin/env python3
"""
InstaFlow Unified Command Line Interface.
Runs interactive terminal simulations, synthetic tests, account discovery, and direct message polling.
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
except ImportError:
    from config import config, InstaFlowConfig
    from discovery import AccountSearchEngine
    from engine import InstaFlowEngine
    from poller import InstagramInboxPoller
    from storage import StorageManager


def print_banner():
    print("=" * 70)
    print("⚡ INSTAFLOW — Autonomous Instagram Direct & Lead Intelligence Agent")
    print("   Slash Commands • <1s Creator Discovery • $0 Cloud Subscriptions")
    print("=" * 70)


def cmd_simulate():
    """Interactive terminal DM simulator."""
    print_banner()
    print("[*] Starting Interactive DM Simulator (Thread: sim_thread_001, User: @developer_guest)")
    print("[*] Commands: /help, /search <niche>, /account <handle>, /tools, CODE, or 'exit'")
    print("-" * 70)

    engine = InstaFlowEngine()
    thread_id = "sim_thread_001"
    sender_handle = "developer_guest"

    welcome = engine.process_incoming_message(thread_id, sender_handle, "/start")
    print(f"\n🤖 InstaFlow:\n{welcome}\n")

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
            print(f"\n🤖 InstaFlow ({latency_ms:.1f}ms):\n{reply}\n")
        else:
            print("\n[InstaFlow took no action / filtered by DWEL loop guard]\n")


def cmd_test() -> bool:
    """Automated synthetic verification suite."""
    print_banner()
    print("[*] Running Automated Interactive Capabilities Suite...")
    print("-" * 70)

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

    print("=" * 70)
    if all_passed:
        print("🎉 ALL INSTAFLOW CAPABILITY TESTS PASSED!")
    else:
        print("⚠️ SOME CAPABILITY TESTS FAILED.")
    print("=" * 70)
    return all_passed


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
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="InstaFlow — Autonomous Instagram Direct & Lead Intelligence Agent")
    parser.add_argument("--simulate", action="store_true", help="Launch real-time interactive terminal DM simulation")
    parser.add_argument("--test", action="store_true", help="Run automated synthetic capability test suite")
    parser.add_argument("--search", type=str, metavar="QUERY", help="Search and discover creator accounts by niche")
    parser.add_argument("--account", type=str, metavar="HANDLE", help="Hydrate creator profile metadata and stats")
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
