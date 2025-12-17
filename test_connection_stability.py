#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket连接稳定性测试
测试连接断开后的错误处理
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

async def test_connection_stability():
    """测试连接稳定性"""
    print("=" * 60)
    print("🔧 AutoGLM WebSocket连接稳定性测试")
    print("=" * 60)
    print(f"服务器地址: {WEBSOCKET_URL}")
    print()

    for i in range(3):
        print(f"🔄 第 {i+1} 次连接测试...")

        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                print("✅ WebSocket连接成功")

                # 发送一个测试命令
                test_message = {"text": "测试连接稳定性"}
                await websocket.send(json.dumps(test_message))
                print(f"📤 发送测试消息: {test_message}")

                # 等待一小段时间
                await asyncio.sleep(1)

                # 手动断开连接
                print("🔌 手动断开连接...")
                await websocket.close()
                print("✅ 连接已断开")

        except websockets.exceptions.ConnectionClosedOK:
            print("🔌 连接正常关闭")
        except Exception as e:
            print(f"❌ 连接测试失败: {e}")

        print("-" * 30)
        await asyncio.sleep(2)  # 等待2秒后再进行下一次测试

    print("🎉 连接稳定性测试完成")
    print("✅ 如果没有看到RuntimeError，说明修复成功！")

if __name__ == "__main__":
    try:
        asyncio.run(test_connection_stability())
    except KeyboardInterrupt:
        print("\n🛑 测试被用户中断")
