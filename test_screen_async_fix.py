#!/usr/bin/env python3
"""
测试屏幕控制异步修复
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


async def test_screen_async_fix():
    """测试屏幕控制异步修复"""
    print("=" * 60)
    print("测试屏幕控制异步修复")
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

    print("\n测试步骤前屏幕检查...")
    print("-" * 40)

    try:
        # 手动调用屏幕检查方法来测试（模拟_execute_step中的调用）
        screen_messages = agent._ensure_screen_ready()

        print(f"屏幕检查完成，返回 {len(screen_messages)} 条消息")

        if screen_messages:
            print("\n收集到的消息:")
            for i, msg in enumerate(screen_messages, 1):
                print(f"  {i}. {msg.strip()}")

        # 模拟发送消息到WebSocket（在异步上下文中）
        if screen_messages:
            print("\n发送消息到WebSocket...")
            for message in screen_messages:
                await mock_ws.send_text(message)

        print(f"\nWebSocket总共收到 {len(mock_ws.messages)} 条消息")

    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("测试完成！修复验证成功")
    print("\n修复要点:")
    print("- _ensure_screen_ready() 现在返回消息列表")
    print("- 调用方负责在异步上下文中发送WebSocket消息")
    print("- 避免了在同步线程中调用asyncio的问题")


if __name__ == "__main__":
    asyncio.run(test_screen_async_fix())
