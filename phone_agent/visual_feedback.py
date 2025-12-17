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


def show_overlay_window(device_id: str | None, title: str, content: str, status: str = "运行中") -> None:
    """
    显示悬浮窗，展示AI当前状态和操作过程。

    Args:
        device_id: ADB设备ID
        title: 窗口标题
        content: 内容文本
        status: 状态 (运行中/思考中/执行中/完成/错误)
    """
    try:
        # 使用Android悬浮窗应用显示真正的悬浮窗
        # 发送广播到悬浮窗应用
        _run_adb_command([
            "shell", "am", "broadcast",
            "-a", "com.autoglm.overlay.UPDATE",
            "--es", "title", title,
            "--es", "content", content,
            "--es", "status", status
        ], device_id)

    except Exception:
        # 降级到通知方式
        try:
            status_icon = {
                "运行中": "⏳",
                "思考中": "🤔",
                "执行中": "⚡",
                "完成": "✅",
                "错误": "❌"
            }.get(status, "⏳")

            if len(content) > 100:
                content = content[:97] + "..."

            _run_adb_command([
                "shell", "cmd", "notification", "post",
                "-S", "bigtext",
                "-t", f"{status_icon} AI助手 - {title}",
                "-m", content,
                "--importance", "high",
                "--ongoing", "true",
                "ai_agent_overlay", "999"
            ], device_id)

        except Exception:
            pass


def update_overlay_content(device_id: str | None, title: str, content: str, status: str = "运行中") -> None:
    """
    更新悬浮窗内容。

    Args:
        device_id: ADB设备ID
        title: 新标题
        content: 新内容
        status: 新状态
    """
    show_overlay_window(device_id, title, content, status)


def show_overlay_with_actions(device_id: str | None, title: str, content: str,
                             status: str = "运行中", show_terminate: bool = True) -> None:
    """
    显示带有操作按钮的悬浮窗。

    Args:
        device_id: ADB设备ID
        title: 标题
        content: 内容
        status: 状态
        show_terminate: 是否显示终止按钮
    """
    try:
        status_icon = {
            "运行中": "⏳",
            "思考中": "🤔",
            "执行中": "⚡",
            "完成": "✅",
            "错误": "❌"
        }.get(status, "⏳")

        # 创建带有终止操作的通知
        base_cmd = [
            "shell", "cmd", "notification", "post",
            "-S", "bigtext",
            "-t", f"{status_icon} AI助手 - {title}",
            "-m", content,
            "--importance", "high",
            "--ongoing", "true",
            "ai_agent_overlay", "999"
        ]

        # 由于ADB通知系统限制，我们通过特殊标记来表示可终止
        if show_terminate:
            base_cmd.extend([
                "--alert-once", "true"  # 让通知只提醒一次
            ])

        _run_adb_command(base_cmd, device_id)

    except Exception:
        # 降级到简单通知
        show_overlay_window(device_id, title, content, status)


def hide_overlay_window(device_id: str | None) -> None:
    """
    隐藏悬浮窗。

    Args:
        device_id: ADB设备ID
    """
    try:
        # 发送广播到悬浮窗应用隐藏窗口
        _run_adb_command([
            "shell", "am", "broadcast",
            "-a", "com.autoglm.overlay.HIDE"
        ], device_id)
    except Exception:
        # 降级到取消通知
        try:
            _run_adb_command([
                "shell", "cmd", "notification", "cancel", "ai_agent_overlay", "999"
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
        self.overlay_visible = False

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

    def show_overlay(self, title: str, content: str, status: str = "运行中", show_terminate: bool = True) -> None:
        """Show overlay window if enabled."""
        if self.enabled:
            show_overlay_with_actions(self.device_id, title, content, status, show_terminate)
            self.overlay_visible = True

    def update_overlay(self, title: str, content: str, status: str = "运行中") -> None:
        """Update overlay content if visible."""
        if self.enabled and self.overlay_visible:
            update_overlay_content(self.device_id, title, content, status)

    def hide_overlay(self) -> None:
        """Hide overlay window."""
        if self.enabled:
            hide_overlay_window(self.device_id)
            self.overlay_visible = False

    def clear(self) -> None:
        """Clear all indicators if enabled."""
        if self.enabled:
            clear_indicators(self.device_id)
            self.overlay_visible = False
