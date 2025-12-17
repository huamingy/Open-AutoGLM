#!/usr/bin/env python3
"""
Visual Feedback Demo / 可视化反馈演示

This script demonstrates the visual feedback feature that shows operation indicators
on the phone screen during AI agent operations.

这个脚本演示可视化反馈功能，在手机屏幕上显示AI操作的指示器。
"""

from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.config import get_messages
from phone_agent.model import ModelConfig


def main(lang: str = "cn"):
    msgs = get_messages(lang)

    print("=" * 60)
    print("Phone Agent - Visual Feedback Demo")
    print("=" * 60)

    # Configure model
    model_config = ModelConfig(
        base_url="http://localhost:8000/v1",
        model_name="autoglm-phone-9b",
        temperature=0.1,
    )

    # Configure Agent with visual feedback enabled
    agent_config = AgentConfig(
        max_steps=10,
        verbose=True,
        lang=lang,
        enable_visual_feedback=True,  # Enable visual feedback
    )

    # Create Agent
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
    )

    print("📱 Visual feedback enabled - operations will show on phone screen")
    print("🤖 Starting task execution...\n")

    # Execute task with visual feedback
    result = agent.run("打开美团外卖搜索附近的火锅店")

    print("\n" + "=" * 60)
    print(f"📊 {msgs['final_result']}: {result}")
    print("=" * 60)
    print("\n💡 Check your phone screen for visual indicators during operations!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Visual Feedback Demo")
    parser.add_argument("--lang", choices=["cn", "en"], default="cn",
                       help="Language (cn or en)")
    args = parser.parse_args()

    main(args.lang)
