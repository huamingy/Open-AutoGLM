#!/usr/bin/env python3
"""
测试最终修复：异步WebSocket消息处理
"""

import asyncio
import websockets
import json
import time


async def test_final_fix():
    """测试最终修复"""
    print("=" * 70)
    print("测试最终修复：异步WebSocket消息处理")
    print("=" * 70)

    try:
        # 连接到WebSocket服务器
        uri = "ws://localhost:8002/ws"
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")

            # 发送测试指令
            test_command = {"text": "echo test message"}
            await websocket.send(json.dumps(test_command))
            print(f"发送指令: {test_command['text']}")

            # 收集所有接收到的消息
            messages = []
            start_time = time.time()

            try:
                while time.time() - start_time < 15:  # 最多等待15秒
                    try:
                        response = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=2.0
                        )
                        messages.append(response)
                        print(f"收到消息: {response.strip()}")

                        # 如果收到错误消息或结果，说明执行完成了
                        if "执行出错" in response or "Result:" in response:
                            break

                    except asyncio.TimeoutError:
                        # 没有新消息，继续等待
                        continue

            except Exception as e:
                print(f"接收消息时出错: {e}")

            print(f"\n测试完成，共收到 {len(messages)} 条消息")

            # 分析消息
            screen_prep_messages = [msg for msg in messages if "屏幕" in msg]
            execution_messages = [msg for msg in messages if "执行" in msg or "Result:" in msg]

            print("\n消息分析:")
            print(f"  - 屏幕准备消息: {len(screen_prep_messages)} 条")
            print(f"  - 执行相关消息: {len(execution_messages)} 条")

            # 检查是否修复成功
            success = True
            error_messages = [msg for msg in messages if "执行出错" in msg and "no running event loop" in msg]

            if error_messages:
                print(f"仍然存在事件循环错误: {len(error_messages)} 条")
                success = False
            else:
                print("没有发现事件循环错误")

            if len(messages) > 0:
                print("WebSocket消息正常传递")
            else:
                print("没有收到任何消息")
                success = False

            if success:
                print("\n修复成功！AI助手现在可以正常处理屏幕控制了")
            else:
                print("\n修复可能还不完整")

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("开始最终修复测试...")
    asyncio.run(test_final_fix())
    print("\n测试结束")
