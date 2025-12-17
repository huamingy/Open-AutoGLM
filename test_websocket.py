#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket连接测试脚本
测试安卓应用连接到服务器的问题
"""

import asyncio
import websockets
import json
import sys
import time

async def test_websocket():
    """测试WebSocket连接"""
    uri = "ws://192.168.2.12:8002/ws"

    print("测试WebSocket连接...")
    print(f"连接地址: {uri}")
    print()

    try:
        async with websockets.connect(uri) as websocket:
            print("WebSocket连接成功！")

            # 发送测试消息
            test_message = "测试消息"
            print(f"发送测试消息: {test_message}")

            await websocket.send(test_message)
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
    print("AutoGLM WebSocket连接测试")
    print("=" * 50)

    # 测试连接
    success = await test_websocket()

    if success:
        print("\n服务器WebSocket服务正常运行")
        print("如果安卓应用仍然连接失败，请检查:")
        print("   - 手机和服务器是否在同一网络")
        print("   - 手机是否有代理设置")
        print("   - 应用是否有网络权限")
    else:
        print("\n服务器WebSocket服务异常")
        print("请确保服务器正在运行: python ws.py")

if __name__ == "__main__":
    asyncio.run(main())
