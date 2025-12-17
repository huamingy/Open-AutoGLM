#!/usr/bin/env python3
"""
悬浮窗功能演示 / Overlay Feature Demo

This script demonstrates the overlay window feature that shows
real-time status and progress on the phone screen during task execution.

此脚本演示悬浮窗功能，在任务执行过程中在手机屏幕上显示实时状态。
"""

import time
from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.config import get_messages
from phone_agent.model import ModelConfig


def main(lang: str = "cn"):
    msgs = get_messages(lang)

    print("=" * 60)
    print("Phone Agent - Overlay Window Demo")
    print("=" * 60)

    # Configure model (use mock for demo)
    model_config = ModelConfig(
        base_url="http://localhost:8000/v1",
        model_name="autoglm-phone-9b",
        temperature=0.1,
    )

    # Configure Agent with visual feedback and overlay
    agent_config = AgentConfig(
        max_steps=5,  # Limit steps for demo
        verbose=True,
        lang=lang,
        enable_visual_feedback=True,  # Enable overlay window
    )

    # Create Agent
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )

    print("📱 Overlay window enabled - check your phone screen!")
    print("🪟 A floating window will show task progress and status")
    print("⏹️ You can terminate tasks anytime using the web interface")
    print("\nStarting demo task...\n")

    # Execute task with overlay display
    try:
        result = agent.run("打开微信查看第一条消息")

        print("\n" + "=" * 60)
        print(f"📊 {msgs['final_result']}: {result}")
        print("=" * 60)
        print("\n💡 The overlay window should have disappeared after task completion!")

    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        agent.terminate()

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Overlay Window Demo")
    parser.add_argument("--lang", choices=["cn", "en"], default="cn",
                       help="Language (cn or en)")
    args = parser.parse_args()

    main(args.lang)
