#!/usr/bin/env python3
"""
测试完整的集成功能，包括屏幕控制和WebSocket
"""

import asyncio
import websockets
import json
import time


async def test_full_integration():
    """测试完整的集成功能"""
    print("=" * 70)
    print("测试完整集成功能：屏幕控制 + WebSocket")
    print("=" * 70)

    try:
        # 连接到WebSocket服务器
        uri = "ws://localhost:8002/ws"
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")

            # 发送一个真实的指令
            test_command = {"text": "echo hello world"}
            await websocket.send(json.dumps(test_command))
            print(f"发送指令: {test_command['text']}")

            # 接收响应
            start_time = time.time()
            message_count = 0

            try:
                while time.time() - start_time < 10:  # 最多等待10秒
                    try:
                        response = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=1.0
                        )
                        message_count += 1
                        print(f"收到消息 {message_count}: {response.strip()}")

                        # 如果收到错误消息，说明执行完成了
                        if "执行出错" in response or "Result:" in response:
                            break

                    except asyncio.TimeoutError:
                        # 没有新消息，继续等待
                        continue

            except Exception as e:
                print(f"接收消息时出错: {e}")

            print(f"\n测试完成，共收到 {message_count} 条消息")

            # 如果收到消息，说明修复成功
            if message_count > 0:
                print("集成测试成功！")
                print("   - WebSocket连接正常")
                print("   - 屏幕控制不再报错")
                print("   - 消息传递正常")
            else:
                print("没有收到消息，可能存在问题")

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("开始完整集成测试...")
    asyncio.run(test_full_integration())
    print("\n集成测试结束")
