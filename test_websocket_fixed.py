#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复后的WebSocket连接测试脚本
测试安卓应用格式的消息
"""

import asyncio
import websockets
import json
import sys

async def test_websocket_fixed():
    """测试修复后的WebSocket连接"""
    uri = "ws://192.168.2.12:8002/ws"

    print("测试修复后的WebSocket连接...")
    print(f"连接地址: {uri}")
    print()

    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")

            # 发送安卓应用格式的消息 (JSON格式)
            test_message = {"text": "测试消息"}
            print(f"发送JSON格式消息: {test_message}")

            await websocket.send(json.dumps(test_message))
            print("消息发送成功")

            # 等待服务器响应
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"收到服务器响应: {response}")
            except asyncio.TimeoutError:
                print("服务器没有及时响应")

            # 发送终止命令测试
            print("\n发送终止命令测试...")
            terminate_command = {"action": "terminate"}
            await websocket.send(json.dumps(terminate_command))
            print("终止命令发送成功")

            # 等待终止响应
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                print(f"收到终止响应: {response}")
            except asyncio.TimeoutError:
                print("终止命令没有响应")

    except Exception as e:
        print(f"WebSocket连接失败: {e}")
        print("\n可能的原因:")
        print("1. 服务器未启动")
        print("2. 端口被防火墙阻止")
        print("3. IP地址不正确")
        print("4. WebSocket路径错误")
        return False

    print("\nWebSocket测试完成！")
    return True

async def main():
    """主函数"""
    print("=" * 50)
    print("AutoGLM WebSocket连接测试 (修复版)")
    print("=" * 50)

    # 测试连接
    success = await test_websocket_fixed()

    if success:
        print("\n服务器WebSocket服务正常运行")
        print("安卓应用现在应该能够正常连接")
    else:
        print("\n服务器WebSocket服务异常")
        print("请确保服务器正在运行: python ws.py")

if __name__ == "__main__":
    asyncio.run(main())
