"""Main PhoneAgent class for orchestrating phone automation."""

import json
import sys
import traceback
from dataclasses import dataclass
from typing import Any, Callable

from phone_agent.actions import ActionHandler
from phone_agent.actions.handler import do, finish, parse_action
from phone_agent.adb import get_current_app, get_screenshot
from phone_agent.config import get_messages, get_system_prompt
from phone_agent.model import ModelClient, ModelConfig
from phone_agent.model.client import MessageBuilder


@dataclass
class AgentConfig:
    """Configuration for the PhoneAgent."""

    max_steps: int = 100
    device_id: str | None = None
    lang: str = "cn"
    system_prompt: str | None = None
    verbose: bool = True
    enable_visual_feedback: bool = False

    def __post_init__(self):
        if self.system_prompt is None:
            self.system_prompt = get_system_prompt(self.lang)


@dataclass
class StepResult:
    """Result of a single agent step."""

    success: bool
    finished: bool
    action: dict[str, Any] | None
    thinking: str
    message: str | None = None


class PhoneAgent:
    """
    AI-powered agent for automating Android phone interactions.

    The agent uses a vision-language model to understand screen content
    and decide on actions to complete user tasks.

    Args:
        model_config: Configuration for the AI model.
        agent_config: Configuration for the agent behavior.
        confirmation_callback: Optional callback for sensitive action confirmation.
        takeover_callback: Optional callback for takeover requests.

    Example:
        >>> from phone_agent import PhoneAgent
        >>> from phone_agent.model import ModelConfig
        >>>
        >>> model_config = ModelConfig(base_url="http://localhost:8000/v1")
        >>> agent = PhoneAgent(model_config)
        >>> agent.run("Open WeChat and send a message to John")
    """

    def __init__(
        self,
        model_config: ModelConfig | None = None,
        agent_config: AgentConfig | None = None,
        confirmation_callback: Callable[[str], bool] | None = None,
        takeover_callback: Callable[[str], None] | None = None,
        websocket=None,  # WebSocket for real-time output
    ):
        self.model_config = model_config or ModelConfig()
        self.agent_config = agent_config or AgentConfig()

        self.model_client = ModelClient(self.model_config)
        self.action_handler = ActionHandler(
            device_id=self.agent_config.device_id,
            confirmation_callback=confirmation_callback,
            takeover_callback=takeover_callback,
            enable_visual_feedback=self.agent_config.enable_visual_feedback,
        )

        self._context: list[dict[str, Any]] = []
        self._step_count = 0
        self._websocket = websocket  # Store websocket for real-time output
        self._terminated = False  # 终止标志

    def run(self, task: str) -> str:
        """
        Run the agent to complete a task.

        Args:
            task: Natural language description of the task.

        Returns:
            Final message from the agent.
        """
        self._context = []
        self._step_count = 0

        # Show initial overlay
        if hasattr(self.action_handler, 'visual_feedback'):
            self.action_handler.visual_feedback.show_overlay(
                f"任务启动", f"正在执行: {task[:50]}...", "运行中", show_terminate=True
            )

        try:
            # First step with user prompt
            result = self._execute_step(task, is_first=True)

            if result.finished:
                # Hide overlay on completion
                if hasattr(self.action_handler, 'visual_feedback'):
                    self.action_handler.visual_feedback.show_overlay(
                        "任务完成", result.message or "任务已完成", "完成", show_terminate=False
                    )
                    # Auto hide after 3 seconds
                    import threading
                    def hide_overlay():
                        import time
                        time.sleep(3)
                        self.action_handler.visual_feedback.hide_overlay()
                    threading.Thread(target=hide_overlay, daemon=True).start()
                return result.message or "Task completed"

            # Continue until finished or max steps reached
            while self._step_count < self.agent_config.max_steps:
                # Check if terminated
                if self._terminated:
                    return "Task terminated by user"

                result = self._execute_step(is_first=False)

                if result.finished:
                    # Hide overlay on completion
                    if hasattr(self.action_handler, 'visual_feedback'):
                        self.action_handler.visual_feedback.show_overlay(
                            "任务完成", result.message or "任务已完成", "完成", show_terminate=False
                        )
                        # Auto hide after 3 seconds
                        import threading
                        def hide_overlay():
                            import time
                            time.sleep(3)
                            self.action_handler.visual_feedback.hide_overlay()
                        threading.Thread(target=hide_overlay, daemon=True).start()
                    return result.message or "Task completed"

            # Max steps reached
            if hasattr(self.action_handler, 'visual_feedback'):
                self.action_handler.visual_feedback.show_overlay(
                    "任务终止", "达到最大步骤数限制", "错误", show_terminate=False
                )
                # Auto hide after 3 seconds
                import threading
                def hide_overlay():
                    import time
                    time.sleep(3)
                    self.action_handler.visual_feedback.hide_overlay()
                threading.Thread(target=hide_overlay, daemon=True).start()
            return "Max steps reached"

        except Exception as e:
            # Show error in overlay
            if hasattr(self.action_handler, 'visual_feedback'):
                self.action_handler.visual_feedback.show_overlay(
                    "任务错误", f"执行出错: {str(e)[:50]}", "错误", show_terminate=False
                )
                # Auto hide after 5 seconds
                import threading
                def hide_overlay():
                    import time
                    time.sleep(5)
                    self.action_handler.visual_feedback.hide_overlay()
                threading.Thread(target=hide_overlay, daemon=True).start()
            raise
        finally:
            # Cleanup screen settings
            try:
                from phone_agent.adb import cleanup_screen_settings
                cleanup_screen_settings(self.agent_config.device_id)
            except Exception:
                pass  # Ignore cleanup errors

    def _ensure_screen_ready(self) -> None:
        """
        Ensure screen is ready for operation:
        - Wake up if asleep
        - Unlock if locked (no password required)
        - Keep screen awake

        Note: This method runs in a sync thread, so it uses print statements
        and relies on ws.py to capture output via output redirection.
        """
        try:
            from phone_agent.adb import get_screen_state, wake_screen, unlock_screen, keep_screen_awake

            # 检查屏幕状态
            state = get_screen_state(self.agent_config.device_id)

            screen_changed = False

            # 如果屏幕没有唤醒，唤醒它
            if not state['awake']:
                print("检测到屏幕休眠，正在唤醒...")

                if wake_screen(self.agent_config.device_id):
                    print("屏幕已唤醒")
                    screen_changed = True
                else:
                    print("屏幕唤醒失败")

            # 如果屏幕锁定（无密码），解锁它
            if state['screen_locked']:
                print("检测到屏幕锁定，正在解锁...")

                if unlock_screen(self.agent_config.device_id):
                    print("屏幕已解锁")
                    screen_changed = True
                else:
                    print("屏幕解锁失败（可能需要密码或PIN）")

            # 确保屏幕保持常亮
            keep_screen_awake(self.agent_config.device_id, 30)  # 30分钟

            # 如果屏幕状态发生了变化，等待一下让系统稳定
            if screen_changed:
                import time
                time.sleep(1.0)

        except Exception as e:
            print(f"屏幕状态检查失败: {e}")

    def terminate(self) -> None:
        """
        Terminate the currently running task.
        """
        self._terminated = True

        # Cleanup screen settings when terminated
        try:
            from phone_agent.adb import cleanup_screen_settings
            cleanup_screen_settings(self.agent_config.device_id)
        except Exception:
            pass  # Ignore cleanup errors
        if hasattr(self.action_handler, 'visual_feedback'):
            self.action_handler.visual_feedback.show_overlay(
                "任务终止", "用户手动终止任务", "错误", show_terminate=False
            )
            # Auto hide after 3 seconds
            import threading
            def hide_overlay():
                import time
                time.sleep(3)
                self.action_handler.visual_feedback.hide_overlay()
            threading.Thread(target=hide_overlay, daemon=True).start()

    def is_terminated(self) -> bool:
        """
        Check if the task has been terminated.

        Returns:
            True if terminated, False otherwise.
        """
        return self._terminated

    def step(self, task: str | None = None) -> StepResult:
        """
        Execute a single step of the agent.

        Useful for manual control or debugging.

        Args:
            task: Task description (only needed for first step).

        Returns:
            StepResult with step details.
        """
        is_first = len(self._context) == 0

        if is_first and not task:
            raise ValueError("Task is required for the first step")

        return self._execute_step(task, is_first)

    def reset(self) -> None:
        """Reset the agent state for a new task."""
        self._context = []
        self._step_count = 0

    def _execute_step(
        self, user_prompt: str | None = None, is_first: bool = False
    ) -> StepResult:
        """Execute a single step of the agent loop."""
        self._step_count += 1

        # 检查并处理屏幕状态（唤醒、解锁、保持常亮）
        # 注意：消息将通过output_queue发送，由ws.py在异步上下文中处理

        # Capture current screen state
        screenshot = get_screenshot(self.agent_config.device_id)
        current_app = get_current_app(self.agent_config.device_id)

        # Build messages
        if is_first:
            self._context.append(
                MessageBuilder.create_system_message(self.agent_config.system_prompt)
            )

            screen_info = MessageBuilder.build_screen_info(current_app)
            text_content = f"{user_prompt}\n\n{screen_info}"

            self._context.append(
                MessageBuilder.create_user_message(
                    text=text_content, image_base64=screenshot.base64_data
                )
            )
        else:
            screen_info = MessageBuilder.build_screen_info(current_app)
            text_content = f"** Screen Info **\n\n{screen_info}"

            self._context.append(
                MessageBuilder.create_user_message(
                    text=text_content, image_base64=screenshot.base64_data
                )
            )

        # Get model response
        try:
            response = self.model_client.request(self._context)
        except Exception as e:
            if self.agent_config.verbose:
                traceback.print_exc()
            return StepResult(
                success=False,
                finished=True,
                action=None,
                thinking="",
                message=f"Model error: {e}",
            )

        # Parse action from response
        try:
            action = parse_action(response.action)
        except ValueError:
            if self.agent_config.verbose:
                traceback.print_exc()
            action = finish(message=response.action)

        if self.agent_config.verbose:
            # Print thinking process
            msgs = get_messages(self.agent_config.lang)
            print("\n" + "=" * 50)
            sys.stdout.flush()
            print(f"💭 {msgs['thinking']}:")
            sys.stdout.flush()
            print("-" * 50)
            sys.stdout.flush()
            print(response.thinking)
            sys.stdout.flush()
            print("-" * 50)
            sys.stdout.flush()
            print(f"🎯 {msgs['action']}:")
            sys.stdout.flush()
            print(json.dumps(action, ensure_ascii=False, indent=2))
            sys.stdout.flush()
            print("=" * 50 + "\n")
            sys.stdout.flush()

        # Update overlay with current thinking
        if hasattr(self.action_handler, 'visual_feedback'):
            thinking_preview = response.thinking[:80] + "..." if len(response.thinking) > 80 else response.thinking
            self.action_handler.visual_feedback.update_overlay(
                f"步骤 {self._step_count}", f"思考: {thinking_preview}", "思考中"
            )

        # Remove image from context to save space
        self._context[-1] = MessageBuilder.remove_images_from_message(self._context[-1])

        # Update overlay with action being executed
        if hasattr(self.action_handler, 'visual_feedback'):
            action_desc = self._get_action_description(action)
            self.action_handler.visual_feedback.update_overlay(
                f"步骤 {self._step_count}", f"执行: {action_desc}", "执行中"
            )

        # Execute action
        try:
            result = self.action_handler.execute(
                action, screenshot.width, screenshot.height
            )
        except Exception as e:
            if self.agent_config.verbose:
                traceback.print_exc()
            result = self.action_handler.execute(
                finish(message=str(e)), screenshot.width, screenshot.height
            )

        # Add assistant response to context
        self._context.append(
            MessageBuilder.create_assistant_message(
                f"<think>{response.thinking}</think><answer>{response.action}</answer>"
            )
        )

        # Check if finished
        finished = action.get("_metadata") == "finish" or result.should_finish

        if finished and self.agent_config.verbose:
            msgs = get_messages(self.agent_config.lang)
            print("\n" + "🎉 " + "=" * 48)
            sys.stdout.flush()
            print(
                f"✅ {msgs['task_completed']}: {result.message or action.get('message', msgs['done'])}"
            )
            sys.stdout.flush()
            print("=" * 50 + "\n")
            sys.stdout.flush()

        return StepResult(
            success=result.success,
            finished=finished,
            action=action,
            thinking=response.thinking,
            message=result.message or action.get("message"),
        )

    @property
    def context(self) -> list[dict[str, Any]]:
        """Get the current conversation context."""
        return self._context.copy()

    def _get_action_description(self, action: dict) -> str:
        """Generate a human-readable description of the action."""
        if not action:
            return "未知操作"

        action_type = action.get("_metadata") or action.get("action", "unknown")

        if action_type == "do":
            real_action = action.get("action", "unknown")
            if real_action == "Launch":
                app = action.get("app", "应用")
                return f"启动{app}"
            elif real_action == "Tap":
                element = action.get("element", [])
                if element and len(element) >= 2:
                    return f"点击位置({element[0]}, {element[1]})"
                return "点击操作"
            elif real_action == "Type":
                text = action.get("text", "")
                return f"输入: {text[:20]}{'...' if len(text) > 20 else ''}"
            elif real_action == "Swipe":
                return "滑动操作"
            elif real_action == "Back":
                return "返回上一页"
            elif real_action == "Home":
                return "回到桌面"
            else:
                return f"{real_action}操作"
        elif action_type == "finish":
            message = action.get("message", "任务完成")
            return f"完成: {message[:30]}{'...' if len(message) > 30 else ''}"
        else:
            return f"{action_type}"

    @property
    def step_count(self) -> int:
        """Get the current step count."""
        return self._step_count
