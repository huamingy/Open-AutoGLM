#!/usr/bin/env python3
"""
测试WebSocket实时输出功能
"""

import asyncio
import sys
import io

class WebSocketOutput:
    def __init__(self):
        self.buffer = ""
        self.lines_sent = []

    def write(self, text):
        if text:
            self.buffer += text
            # Send complete lines immediately
            while '\n' in self.buffer:
                line, self.buffer = self.buffer.split('\n', 1)
                if line.strip():  # Only send non-empty lines
                    self.lines_sent.append(line)
                    # 直接写到stderr避免递归
                    sys.stderr.write(f'[实时发送] {line}\n')
                    sys.stderr.flush()

    def flush(self):
        if self.buffer:
            self.lines_sent.append(self.buffer)
            sys.stderr.write(f'[刷新发送] {self.buffer}\n')
            sys.stderr.flush()
            self.buffer = ""

    def isatty(self):
        return False

def simulate_agent_output():
    """模拟AI Agent的输出"""
    print("🔍 Checking system requirements...")
    print("-" * 50)
    print("1. Checking ADB installation... ✅ OK")
    print("2. Checking connected devices... ✅ OK")
    print("3. Checking ADB Keyboard... ✅ OK")
    print("-" * 50)
    print("✅ All system checks passed!\n")

    print("=" * 50)
    print("Phone Agent - AI-powered phone automation")
    print("=" * 50)
    print("Model: autoglm-phone")
    print("Device: emulator-5554")
    print("=" * 50)
    print("\nTask: 打开微信给张三发消息\n")

    print("\n" + "=" * 50)
    print("💭 思考过程:")
    print("-" * 50)
    print("用户要求打开微信给张三发消息。我需要先启动微信应用。")
    print("-" * 50)
    print("🎯 执行动作:")
    print('{\n  "action": "Launch",\n  "app": "微信"\n}')
    print("=" * 50 + "\n")

    print("\n" + "=" * 50)
    print("💭 思考过程:")
    print("-" * 50)
    print("微信已经打开，现在需要找到张三的聊天窗口并点击进入。")
    print("-" * 50)
    print("🎯 执行动作:")
    print('{\n  "action": "Tap",\n  "element": [300, 400]\n}')
    print("=" * 50 + "\n")

    print("\n" + "🎉 " + "=" * 48)
    print("✅ 任务完成: 已成功给张三发送消息")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    print("测试WebSocket实时输出...")
    print("=" * 50)

    # 重定向输出
    old_stdout = sys.stdout
    ws_output = WebSocketOutput()
    sys.stdout = ws_output

    try:
        simulate_agent_output()
        ws_output.flush()  # 确保最后的内容被发送
    finally:
        sys.stdout = old_stdout

    print("\n测试完成！")
