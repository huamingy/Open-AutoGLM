#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket心跳包测试脚本
用于验证心跳包机制是否正常工作
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

async def test_heartbeat():
    """测试心跳包机制"""
    print("=" * 60)
    print("💓 AutoGLM WebSocket心跳包测试")
    print("=" * 60)
    print(f"服务器地址: {WEBSOCKET_URL}")
    print()

    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✅ WebSocket连接成功")
            print("等待心跳包测试... (将观察30秒)")
            print("-" * 40)

            start_time = time.time()
            ping_count = 0
            pong_count = 0

            while time.time() - start_time < 35:  # 测试35秒
                try:
                    # 设置较短的超时时间来接收消息
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)

                    print(f"📨 收到消息: {message[:50]}...")

                    # 解析消息
                    try:
                        data = json.loads(message)
                        if data.get("type") == "pong":
                            pong_count += 1
                            timestamp = data.get("timestamp", 0)
                            latency = int(time.time() * 1000) - timestamp
                            print(f"💚 收到心跳响应 #{pong_count} (延迟: {latency}ms)")
                        else:
                            print(f"📝 收到普通消息: {message}")
                    except json.JSONDecodeError:
                        print(f"📝 收到文本消息: {message}")

                except asyncio.TimeoutError:
                    # 超时，发送心跳包
                    ping_count += 1
                    ping_message = {"type": "ping", "timestamp": int(time.time() * 1000)}
                    await websocket.send(json.dumps(ping_message))
                    print(f"💓 发送心跳包 #{ping_count}: {ping_message}")

                except websockets.exceptions.ConnectionClosed:
                    print("❌ 连接被关闭")
                    break

            print("-" * 40)
            print("心跳包测试完成统计:")
            print(f"📤 发送心跳包: {ping_count} 次")
            print(f"📥 收到心跳响应: {pong_count} 次")
            print(".1f"            print(".1f")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"❌ 连接失败: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    print("🚀 启动WebSocket心跳包测试")
    print("💡 测试将持续约35秒，观察心跳包收发情况")
    print()

    try:
        asyncio.run(test_heartbeat())
    except KeyboardInterrupt:
        print("\n🛑 测试被用户中断")
        print("✅ 心跳包测试完成")
