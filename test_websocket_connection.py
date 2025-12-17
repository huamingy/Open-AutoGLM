#!/usr/bin/env python3
"""
测试WebSocket连接是否正常工作
"""

import asyncio
import websockets
import json


async def test_websocket():
    """测试WebSocket连接"""
    try:
        # 连接到WebSocket服务器
        uri = "ws://localhost:8002/ws"
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")

            # 发送一个测试命令
            test_command = {"text": "echo hello"}
            await websocket.send(json.dumps(test_command))
            print(f"发送命令: {test_command}")

            # 接收响应
            try:
                response = await websocket.recv()
                print(f"收到响应: {response}")
            except Exception as e:
                print(f"接收响应失败: {e}")

            # 测试终止命令
            print("\n测试终止命令...")
            terminate_command = {"action": "terminate"}
            await websocket.send(json.dumps(terminate_command))
            print(f"发送终止命令: {terminate_command}")

            # 接收终止响应
            try:
                response = await websocket.recv()
                print(f"收到终止响应: {response}")
            except Exception as e:
                print(f"接收终止响应失败: {e}")

    except Exception as e:
        print(f"WebSocket连接失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("测试WebSocket连接...")
    asyncio.run(test_websocket())
    print("测试完成！")
