#!/usr/bin/env python3
"""
测试命令执行过程中的自动屏幕解锁功能
"""

import sys
import os
import asyncio

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phone_agent import PhoneAgent
from phone_agent.agent import AgentConfig
from phone_agent.model import ModelConfig


class MockWebSocket:
    """模拟WebSocket用于测试"""
    def __init__(self):
        self.messages = []

    async def send_text(self, text):
        self.messages.append(text)
        print(f"[WebSocket] {text.strip()}")


async def test_auto_screen_unlock():
    """测试自动屏幕解锁功能"""
    print("=" * 60)
    print("测试命令执行过程中的自动屏幕解锁功能")
    print("=" * 60)

    # 创建模拟WebSocket
    mock_ws = MockWebSocket()

    # 创建Agent配置
    model_config = ModelConfig(
        base_url="https://open.bigmodel.cn/api/paas/v4",
        model_name="autoglm-phone",
        api_key="dummy_key_for_test"
    )

    agent_config = AgentConfig(
        device_id="192.168.2.233:5555",  # 根据实际情况修改
        verbose=True,
        enable_visual_feedback=False,  # 禁用以避免额外输出
    )

    # 创建PhoneAgent实例
    agent = PhoneAgent(
        model_config=model_config,
        agent_config=agent_config,
        websocket=mock_ws
    )

    print("\n模拟AI执行任务过程...")
    print("-" * 40)

    try:
        # 模拟执行步骤（这会触发屏幕状态检查）
        # 注意：这里不会真正执行AI推理，因为我们没有有效的API密钥
        print("开始执行步骤1...")

        # 手动调用屏幕检查方法来测试
        agent._ensure_screen_ready()

        print("\n屏幕检查完成！")
        print(f"WebSocket消息数量: {len(mock_ws.messages)}")

        if mock_ws.messages:
            print("\n发送的WebSocket消息:")
            for i, msg in enumerate(mock_ws.messages, 1):
                print(f"  {i}. {msg.strip()}")

    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("测试完成！")
    print("\n说明:")
    print("- 如果屏幕处于锁屏状态，会自动唤醒和解锁")
    print("- 解锁后会保持屏幕常亮")
    print("- 所有操作都会通过WebSocket实时反馈")


if __name__ == "__main__":
    asyncio.run(test_auto_screen_unlock())
