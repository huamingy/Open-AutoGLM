"""
Visual feedback utilities for displaying operation indicators on Android device screen.

This module provides functionality to show visual cues on the phone screen
during AI agent operations, such as tap targets, swipe paths, etc.
"""

import subprocess
import time
from typing import Optional


def _run_adb_command(cmd: list[str], device_id: str | None = None) -> None:
    """Execute ADB command with optional device ID."""
    if device_id:
        cmd = ["adb", "-s", device_id] + cmd
    else:
        cmd = ["adb"] + cmd

    try:
        subprocess.run(cmd, capture_output=True, timeout=5)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Ignore errors for visual feedback


def show_tap_indicator(device_id: str | None, x: int, y: int, duration: float = 0.5) -> None:
    """
    Show a tap indicator (circle) at the specified coordinates on the screen.

    Args:
        device_id: ADB device ID
        x, y: Coordinates to show indicator
        duration: How long to show the indicator in seconds
    """
    try:
        # Use Android notification to show tap location
        title = "🤖 AI 操作"
        text = f"点击位置: ({x}, {y})"

        _run_adb_command([
            "shell", "cmd", "notification", "post",
            "-S", "bigtext",
            "-t", title,
            "-m", text,
            "ai_agent_tap", "1"
        ], device_id)

        # Brief vibration for feedback
        _run_adb_command(["shell", "input", "vibrate", "150"], device_id)

    except Exception:
        # Fallback: use vibration only
        try:
            run_adb_command(["shell", "input", "vibrate", "150"], device_id)
        except:
            pass  # Ignore if vibration also fails


def show_swipe_indicator(device_id: str | None, start_x: int, start_y: int,
                        end_x: int, end_y: int, duration: float = 1.0) -> None:
    """
    Show a swipe indicator (arrow) from start to end coordinates.

    Args:
        device_id: ADB device ID
        start_x, start_y: Start coordinates
        end_x, end_y: End coordinates
        duration: How long to show the indicator in seconds
    """
    try:
        # Use Android notification to show swipe path
        title = "🤖 AI 操作 - 滑动"
        text = f"从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})"

        _run_adb_command([
            "shell", "cmd", "notification", "post",
            "-S", "bigtext",
            "-t", title,
            "-m", text,
            "ai_agent_swipe", "2"
        ], device_id)

        # Double vibration for swipe feedback
        _run_adb_command(["shell", "input", "vibrate", "200"], device_id)
        time.sleep(0.1)
        _run_adb_command(["shell", "input", "vibrate", "200"], device_id)

    except Exception:
        # Fallback: vibration pattern for swipe
        try:
            run_adb_command(["shell", "input", "vibrate", "200"], device_id)
            time.sleep(0.1)
            run_adb_command(["shell", "input", "vibrate", "200"], device_id)
        except:
            pass


def show_text_indicator(device_id: str | None, text: str, x: int, y: int,
                       duration: float = 2.0) -> None:
    """
    Show text indicator on screen (for operation descriptions).

    Args:
        device_id: ADB device ID
        text: Text to display
        x, y: Position coordinates
        duration: How long to show the text in seconds
    """
    try:
        # Use Android's toast or notification for text display
        run_adb_command([
            "shell", "am", "broadcast", "-a", "com.android.systemui.action.SHOW_TEXT",
            "--es", "text", text,
            "--ei", "x", str(x), "--ei", "y", str(y),
            "--el", "duration", str(int(duration * 1000))
        ], device_id)

    except Exception:
        # Fallback: use Android toast
        try:
            run_adb_command([
                "shell", "am", "broadcast", "-a", "android.intent.action.SHOW_TOAST",
                "--es", "text", text,
                "--ez", "long", "true" if len(text) > 20 else "false"
            ], device_id)
        except:
            pass


def clear_indicators(device_id: str | None) -> None:
    """
    Clear all visual indicators from screen.

    Args:
        device_id: ADB device ID
    """
    try:
        # Cancel notifications
        _run_adb_command([
            "shell", "cmd", "notification", "cancel", "ai_agent_tap", "1"
        ], device_id)
        _run_adb_command([
            "shell", "cmd", "notification", "cancel", "ai_agent_swipe", "2"
        ], device_id)
    except:
        pass


class VisualFeedbackManager:
    """
    Manager for visual feedback on Android device screen.
    """

    def __init__(self, device_id: str | None = None, enabled: bool = True):
        self.device_id = device_id
        self.enabled = enabled

    def show_tap(self, x: int, y: int, duration: float = 0.5) -> None:
        """Show tap indicator if enabled."""
        if self.enabled:
            show_tap_indicator(self.device_id, x, y, duration)

    def show_swipe(self, start_x: int, start_y: int, end_x: int, end_y: int,
                   duration: float = 1.0) -> None:
        """Show swipe indicator if enabled."""
        if self.enabled:
            show_swipe_indicator(self.device_id, start_x, start_y, end_x, end_y, duration)

    def show_text(self, text: str, x: int = 100, y: int = 100, duration: float = 2.0) -> None:
        """Show text indicator if enabled."""
        if self.enabled:
            show_text_indicator(self.device_id, text, x, y, duration)

    def clear(self) -> None:
        """Clear all indicators if enabled."""
        if self.enabled:
            clear_indicators(self.device_id)
