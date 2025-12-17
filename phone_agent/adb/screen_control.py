"""
Screen control utilities for Android devices.

This module provides functionality to:
- Check screen state (on/off, locked/unlocked)
- Wake up screen
- Unlock screen (swipe to unlock for no-password devices)
- Keep screen awake during operations
"""

import subprocess
import time
from typing import Optional, Tuple

from phone_agent.adb.device import _get_adb_prefix


def get_screen_state(device_id: str | None = None) -> dict:
    """
    Get the current screen state.

    Returns:
        dict with keys:
        - 'screen_on': bool - True if screen is on
        - 'screen_locked': bool - True if screen is locked
        - 'awake': bool - True if screen is awake (not sleeping)
    """
    try:
        # Check if screen is on
        result = subprocess.run(
            (["adb", "-s", device_id] if device_id else ["adb"]) +
            ["shell", "dumpsys", "power"],
            capture_output=True, text=True, encoding='utf-8', timeout=5
        )

        screen_on = "mScreenOn=true" in result.stdout or "Display Power: state=ON" in result.stdout

        # Check if screen is awake
        awake = "mWakefulness=Awake" in result.stdout

        # Check if screen is locked
        result2 = subprocess.run(
            (["adb", "-s", device_id] if device_id else ["adb"]) +
            ["shell", "dumpsys", "window"],
            capture_output=True, text=True, encoding='utf-8', timeout=5
        )

        screen_locked = "mShowingDream=" in result2.stdout or "Keyguard" in result2.stdout

        return {
            'screen_on': screen_on,
            'screen_locked': screen_locked,
            'awake': awake
        }

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            'screen_on': False,
            'screen_locked': True,
            'awake': False
        }


def wake_screen(device_id: str | None = None) -> bool:
    """
    Wake up the screen if it's off.

    Returns:
        bool: True if screen was woken up or was already on
    """
    try:
        state = get_screen_state(device_id)

        if not state['awake']:
            # Press power button to wake screen
            subprocess.run(_get_adb_prefix(device_id) + ["shell", "input", "keyevent", "KEYCODE_POWER"],
                         capture_output=True, timeout=5)
            time.sleep(0.5)  # Wait for screen to turn on

            # Check again
            state = get_screen_state(device_id)
            return state['awake']

        return True

    except Exception:
        return False


def unlock_screen(device_id: str | None = None) -> bool:
    """
    Unlock the screen if it's locked (for no-password devices).

    This performs a swipe gesture to unlock the screen.
    Only works for devices without password/PIN/pattern lock.

    Returns:
        bool: True if screen was unlocked or was already unlocked
    """
    try:
        state = get_screen_state(device_id)

        if state['screen_locked']:
            # Try to unlock by swiping up from bottom
            # Get screen dimensions for proper swipe coordinates
            result = subprocess.run(
                (["adb", "-s", device_id] if device_id else ["adb"]) +
                ["shell", "wm", "size"],
                capture_output=True, text=True, encoding='utf-8', timeout=5
            )

            # Default coordinates if we can't get screen size
            screen_width = 1080
            screen_height = 1920

            if "Physical size:" in result.stdout:
                try:
                    size_str = result.stdout.split("Physical size:")[1].strip()
                    width_str, height_str = size_str.split("x")
                    screen_width = int(width_str)
                    screen_height = int(height_str)
                except:
                    pass  # Use default values

            # Swipe from bottom center up to unlock
            start_x = screen_width // 2
            start_y = int(screen_height * 0.8)  # 80% from top
            end_x = screen_width // 2
            end_y = int(screen_height * 0.2)    # 20% from top

            subprocess.run(_get_adb_prefix(device_id) + [
                "shell", "input", "swipe",
                str(start_x), str(start_y),
                str(end_x), str(end_y),
                "500"  # 500ms duration
            ], capture_output=True, timeout=5)

            time.sleep(1)  # Wait for unlock animation

            # Check if unlock was successful
            state = get_screen_state(device_id)
            return not state['screen_locked']

        return True

    except Exception:
        return False


def keep_screen_awake(device_id: str | None = None, duration_minutes: int = 30) -> bool:
    """
    Keep the screen awake for the specified duration.

    Args:
        device_id: ADB device ID
        duration_minutes: How long to keep screen awake (in minutes)

    Returns:
        bool: True if successful
    """
    try:
        # Disable screen timeout (keep awake)
        subprocess.run(_get_adb_prefix(device_id) + [
            "shell", "settings", "put", "system", "screen_off_timeout",
            str(duration_minutes * 60 * 1000)  # Convert to milliseconds
        ], capture_output=True, timeout=5)

        # Alternative: Use stay awake while charging setting
        subprocess.run(_get_adb_prefix(device_id) + [
            "shell", "settings", "put", "global", "stay_on_while_plugged_in", "3"
        ], capture_output=True, timeout=5)

        return True

    except Exception:
        return False


def restore_screen_timeout(device_id: str | None = None) -> bool:
    """
    Restore normal screen timeout settings.

    Returns:
        bool: True if successful
    """
    try:
        # Restore default screen timeout (usually 30 seconds or 1 minute)
        subprocess.run(_get_adb_prefix(device_id) + [
            "shell", "settings", "put", "system", "screen_off_timeout", "30000"
        ], capture_output=True, timeout=5)

        # Reset stay awake setting
        subprocess.run(_get_adb_prefix(device_id) + [
            "shell", "settings", "put", "global", "stay_on_while_plugged_in", "0"
        ], capture_output=True, timeout=5)

        return True

    except Exception:
        return False


def prepare_screen_for_operation(device_id: str | None = None) -> bool:
    """
    Prepare the screen for AI operation:
    1. Wake up screen if off
    2. Unlock screen if locked (no password required)
    3. Keep screen awake

    Returns:
        bool: True if screen is ready for operation
    """
    try:
        # Step 1: Wake up screen
        if not wake_screen(device_id):
            return False

        # Step 2: Unlock screen
        if not unlock_screen(device_id):
            return False

        # Step 3: Keep screen awake
        keep_screen_awake(device_id, 30)  # Keep awake for 30 minutes

        # Final check
        state = get_screen_state(device_id)
        return state['awake'] and not state['screen_locked']

    except Exception:
        return False


def cleanup_screen_settings(device_id: str | None = None) -> bool:
    """
    Clean up screen settings after operation.

    Returns:
        bool: True if successful
    """
    return restore_screen_timeout(device_id)
