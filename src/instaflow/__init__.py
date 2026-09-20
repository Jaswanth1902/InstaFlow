"""
InstaFlow — Autonomous Instagram Direct & Lead Intelligence Agent.
Local Slash Commands, 1-Second Creator Discovery, ManyChat Lead Magnets & Reel Tool Harvester.
"""

__version__ = "0.1.0"
__author__ = "Jaswanth Reddy"
__license__ = "MIT"

from .engine import InstaFlowEngine, ConversationState
from .discovery import AccountSearchEngine, InstagramAccount
from .poller import InstagramInboxPoller
from .config import config, InstaFlowConfig

__all__ = [
    "InstaFlowEngine",
    "ConversationState",
    "AccountSearchEngine",
    "InstagramAccount",
    "InstagramInboxPoller",
    "config",
    "InstaFlowConfig",
]
