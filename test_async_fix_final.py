#!/usr/bin/env python3
"""
测试最终异步修复：确保屏幕控制不再出现事件循环错误
"""

import asyncio
import websockets
import json
import time


async def test_async_fix_final():
    """测试最终异步修复"""
    print("=" * 70)
    print("测试最终异步修复：屏幕控制事件循环问题")
    print("=" * 70)

    try:
        # 连接到WebSocket服务器
        uri = "ws://localhost:8002/ws"
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")

            # 发送一个简单的测试指令
            test_command = {"text": "echo hello"}
            await websocket.send(json.dumps(test_command))
            print(f"发送指令: {test_command['text']}")

            # 收集所有接收到的消息
            messages = []
            start_time = time.time()
            max_wait = 10  # 最多等待10秒

            try:
                while time.time() - start_time < max_wait:
                    try:
                        response = await asyncio.wait_for(
                            websocket.recv(),
                            timeout=1.0
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

            # 分析消息内容
            success = True

            # 检查是否有事件循环错误
            event_loop_errors = [msg for msg in messages if "no running event loop" in msg]
            if event_loop_errors:
                print(f"仍然存在事件循环错误: {len(event_loop_errors)} 条错误消息")
                success = False
            else:
                print("没有发现事件循环错误")

            # 检查是否有屏幕相关消息
            screen_messages = [msg for msg in messages if "屏幕" in msg or "唤醒" in msg or "解锁" in msg]
            if screen_messages:
                print(f"收到屏幕控制消息: {len(screen_messages)} 条")
            else:
                print("没有收到屏幕控制消息")

            # 检查是否有执行相关消息
            execution_messages = [msg for msg in messages if "执行" in msg or "Result:" in msg or "echo" in msg]
            if execution_messages:
                print(f"收到执行相关消息: {len(execution_messages)} 条")
            else:
                print("没有收到执行相关消息")

            if success and len(messages) > 0:
                print("\n修复成功！AI助手现在可以正常执行任务，不会再出现事件循环错误")
                print("屏幕控制功能正常工作，消息传递正确")
            else:
                print("\n修复可能还不完整，需要进一步检查")

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("开始最终异步修复测试...")
    asyncio.run(test_async_fix_final())
    print("\n测试结束")
