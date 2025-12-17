#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket自动连接和重连测试脚本
用于验证Android应用的自动连接功能
"""

import asyncio
import websockets
import json
import time
import sys

# 设置编码
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SERVER_IP = "192.168.2.12"
SERVER_PORT = 8002
WEBSOCKET_URL = f"ws://{SERVER_IP}:{SERVER_PORT}/ws"

async def test_websocket_connection():
    """测试WebSocket连接"""
    print("=" * 60)
    print("🔧 AutoGLM WebSocket自动连接和重连测试")
    print("=" * 60)
    print(f"服务器地址: {WEBSOCKET_URL}")
    print()

    connection_count = 0

    while True:
        try:
            connection_count += 1
            print(f"🔄 第 {connection_count} 次连接尝试...")

            async with websockets.connect(WEBSOCKET_URL) as websocket:
                print("✅ WebSocket连接成功！")
                print("📡 等待消息... (连接将保持5秒)")

                # 发送一个测试消息
                test_message = {"text": "WebSocket自动连接测试"}
                await websocket.send(json.dumps(test_message))
                print(f"📤 发送测试消息: {test_message}")

                # 等待服务器响应
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=3)
                    print(f"📥 收到服务器响应: {response}")
                except asyncio.TimeoutError:
                    print("⚠️  没有收到服务器响应")

                # 发送终止命令测试
                print("🛑 发送终止命令测试...")
                terminate_message = {"action": "terminate"}
                await websocket.send(json.dumps(terminate_message))
                print(f"📤 发送终止命令: {terminate_message}")

                # 等待终止响应
                try:
                    terminate_response = await asyncio.wait_for(websocket.recv(), timeout=2)
                    print(f"📥 收到终止响应: {terminate_response}")
                except asyncio.TimeoutError:
                    print("⚠️  终止命令没有响应")

                # 保持连接一段时间
                await asyncio.sleep(5)

        except websockets.exceptions.ConnectionClosedOK:
            print("🔌 连接正常关闭")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"❌ 连接异常关闭: {e}")
        except Exception as e:
            print(f"❌ 连接失败: {e}")

        print("⏰ 等待3秒后重连...")
        print("-" * 40)
        await asyncio.sleep(3)

if __name__ == "__main__":
    print("🚀 启动WebSocket自动连接和重连测试")
    print("💡 按 Ctrl+C 停止测试")
    print()

    try:
        asyncio.run(test_websocket_connection())
    except KeyboardInterrupt:
        print("\n🛑 测试停止")
        print("✅ WebSocket自动连接和重连测试完成")
