"""
teleoperation.py — Declarative Android ADB Touch Compiler & Anti-Ban Physical Simulator
Compiles physical touchscreen swipe/tap gestures with human kinetic jitter emulation,
supporting direct local Android Debug Bridge (ADB) execution or remote reach execution.
"""

from __future__ import annotations
import math
import random
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class TouchPoint:
    x: int
    y: int
    duration_ms: int
    pressure: float
    jitter_applied: bool


class AgentReachController:
    """
    Manages physical touch simulation and declarative ADB command compilation.
    Bypasses behavioral anti-bot heuristics via Gaussian kinetic touch perturbation.
    """

    def __init__(self, reach_bin: Optional[str] = None, force_reach: bool = False):
        self.reach_bin = reach_bin or "reach"
        self._has_reach = force_reach or (reach_bin is not None) or (shutil.which(self.reach_bin) is not None)
        self._has_adb = shutil.which("adb") is not None

    @staticmethod
    def calculate_human_touch_point(
        x: int, y: int, jitter_radius: float = 3.5, max_width: int = 1080, max_height: int = 2400
    ) -> TouchPoint:
        """
        Applies a 2D Gaussian random offset and human touch duration variance
        to prevent static coordinate fingerprinting by mobile anti-bot systems.
        """
        # Box-Muller / Gaussian perturbation for natural finger radius
        dx = random.gauss(0, jitter_radius / 2.0)
        dy = random.gauss(0, jitter_radius / 2.0)
        perturbed_x = min(max_width, max(0, int(round(x + dx))))
        perturbed_y = min(max_height, max(0, int(round(y + dy))))
        # Human touch duration typically varies between 85ms and 145ms
        duration = int(random.uniform(90, 140))
        pressure = round(random.uniform(0.75, 0.95), 2)

        return TouchPoint(
            x=perturbed_x,
            y=perturbed_y,
            duration_ms=duration,
            pressure=pressure,
            jitter_applied=True
        )

    def build_adb_touch_command(
        self, target_node: str, x: int, y: int, duration_ms: Optional[int] = None, apply_jitter: bool = False
    ) -> List[str]:
        """Compiles a physical swipe/tap command for Android Debug Bridge."""
        if apply_jitter:
            pt = self.calculate_human_touch_point(x, y)
            final_x, final_y, dur = pt.x, pt.y, (duration_ms or pt.duration_ms)
        else:
            final_x, final_y, dur = x, y, (duration_ms or 120)

        cmd = ["input", "swipe", str(final_x), str(final_y), str(final_x), str(final_y), str(dur)]

        if self._has_reach:
            return [self.reach_bin, target_node, "exec", "--"] + cmd
        elif self._has_adb:
            return ["adb", "-s", target_node, "shell"] + cmd
        else:
            return ["adb", "shell"] + cmd

    def build_adb_type_command(self, target_node: str, text: str) -> List[str]:
        """Compiles a keyboard entry command, sanitizing spaces for Android shell input."""
        sanitized = text.replace(" ", "%s").replace("'", "\\'")
        cmd = ["input", "text", sanitized]

        if self._has_reach:
            return [self.reach_bin, target_node, "exec", "--"] + cmd
        elif self._has_adb:
            return ["adb", "-s", target_node, "shell"] + cmd
        else:
            return ["adb", "shell"] + cmd

    def build_headless_scrape_command(
        self, target_node: str, target_url: str, output_file: str
    ) -> List[str]:
        """Compiles an isolated scraper command payload."""
        cmd = [
            "python", "-m", "scrapling", "extract", "stealthy-fetch",
            target_url, output_file, "--ai-targeted"
        ]
        if self._has_reach:
            return [self.reach_bin, target_node, "exec", "--"] + cmd
        return cmd

    def simulate_touch_gesture(self, x: int, y: int) -> Dict[str, Any]:
        """Simulates and profiles human touch gesture physics without requiring connected hardware."""
        pt = self.calculate_human_touch_point(x, y)
        return {
            "mode": "DECLARATIVE_SIMULATOR",
            "original_target": (x, y),
            "simulated_touch": (pt.x, pt.y),
            "offset_applied": (pt.x - x, pt.y - y),
            "duration_ms": pt.duration_ms,
            "pressure": pt.pressure,
            "jitter_applied": pt.jitter_applied,
            "local_adb_available": self._has_adb,
            "reach_tunnel_available": self._has_reach,
            "status": "READY"
        }
