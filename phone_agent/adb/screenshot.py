"""Screenshot utilities for capturing Android device screen."""

import base64
import os
import subprocess
import tempfile
import uuid
from dataclasses import dataclass
from io import BytesIO
from typing import Tuple

from PIL import Image


@dataclass
class Screenshot:
    """Represents a captured screenshot."""

    base64_data: str
    width: int
    height: int
    is_sensitive: bool = False


def get_screenshot(device_id: str | None = None, timeout: int = 15) -> Screenshot:
    """
    Capture a screenshot from the connected Android device.

    Args:
        device_id: Optional ADB device ID for multi-device setups.
        timeout: Timeout in seconds for screenshot operations.

    Returns:
        Screenshot object containing base64 data and dimensions.

    Note:
        If the screenshot fails (e.g., on sensitive screens like payment pages),
        a black fallback image is returned with is_sensitive=True.
    """
    temp_path = os.path.join(tempfile.gettempdir(), f"screenshot_{uuid.uuid4()}.png")
    adb_prefix = _get_adb_prefix(device_id)

    # Try up to 3 times with increasing timeout
    for attempt in range(3):
        current_timeout = timeout + (attempt * 5)  # 15s, 20s, 25s

        try:
            # First, check if device is responsive
            device_check = subprocess.run(
                adb_prefix + ["shell", "echo", "test"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=5,
            )
            if device_check.returncode != 0:
                print(f"Device not responsive (attempt {attempt + 1}/3)")
                if attempt < 2:  # Not the last attempt
                    import time
                    time.sleep(1)
                    continue

            # Execute screenshot command
            result = subprocess.run(
                adb_prefix + ["shell", "screencap", "-p", "/sdcard/tmp.png"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=current_timeout,
            )

            # Check for screenshot failure (sensitive screen)
            output = result.stdout + result.stderr
            if "Status: -1" in output or "Failed" in output or result.returncode != 0:
                return _create_fallback_screenshot(is_sensitive=True)

            # Pull screenshot to local temp path with retry
            for pull_attempt in range(2):
                try:
                    pull_result = subprocess.run(
                        adb_prefix + ["pull", "/sdcard/tmp.png", temp_path],
                        capture_output=True,
                        text=True,
                        encoding='utf-8',
                        timeout=min(current_timeout, 10),  # Max 10s for pull
                    )

                    if pull_result.returncode == 0 and os.path.exists(temp_path):
                        break  # Pull successful

                    if pull_attempt < 1:  # Not the last attempt
                        import time
                        time.sleep(0.5)

                except subprocess.TimeoutExpired:
                    if pull_attempt < 1:
                        continue
                    raise

            if not os.path.exists(temp_path):
                return _create_fallback_screenshot(is_sensitive=False)

            # Verify file is not empty
            if os.path.getsize(temp_path) == 0:
                os.remove(temp_path)
                return _create_fallback_screenshot(is_sensitive=False)

            # Read and encode image
            img = Image.open(temp_path)
            width, height = img.size

            buffered = BytesIO()
            img.save(buffered, format="PNG")
            base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Cleanup
            os.remove(temp_path)

            return Screenshot(
                base64_data=base64_data, width=width, height=height, is_sensitive=False
            )

        except subprocess.TimeoutExpired as e:
            print(f"Screenshot timeout (attempt {attempt + 1}/3): {e}")
            if attempt < 2:  # Not the last attempt
                import time
                time.sleep(1)
                continue
            # Last attempt failed
            break

        except Exception as e:
            print(f"Screenshot error (attempt {attempt + 1}/3): {e}")
            if attempt < 2:  # Not the last attempt
                import time
                time.sleep(1)
                continue
            # Last attempt failed
            break

    # All attempts failed, return fallback
    print("All screenshot attempts failed, using fallback")
    return _create_fallback_screenshot(is_sensitive=False)


def _get_adb_prefix(device_id: str | None) -> list:
    """Get ADB command prefix with optional device specifier."""
    if device_id:
        return ["adb", "-s", device_id]
    return ["adb"]


def _create_fallback_screenshot(is_sensitive: bool) -> Screenshot:
    """Create a black fallback image when screenshot fails."""
    default_width, default_height = 1080, 2400

    black_img = Image.new("RGB", (default_width, default_height), color="black")
    buffered = BytesIO()
    black_img.save(buffered, format="PNG")
    base64_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return Screenshot(
        base64_data=base64_data,
        width=default_width,
        height=default_height,
        is_sensitive=is_sensitive,
    )
