#!/usr/bin/env python3
"""
测试实时输出功能

模拟AI Agent的输出过程，验证WebSocket是否能实时显示每一行
"""

import time
import sys

# 设置编码以支持emoji
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def simulate_agent_output():
    """模拟AI Agent的完整输出过程"""

    # 系统检查
    print("Checking system requirements...")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("1. Checking ADB installation... OK (Android Debug Bridge version 1.0.41)")
    sys.stdout.flush()
    time.sleep(0.1)

    print("2. Checking connected devices... OK (1 device(s): emulator-5554)")
    sys.stdout.flush()
    time.sleep(0.1)

    print("3. Checking ADB Keyboard... OK")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("All system checks passed!\n")
    sys.stdout.flush()
    time.sleep(0.2)

    # 模型检查
    print("Checking model API...")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("1. Checking API connectivity (http://localhost:8000/v1)... OK")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("Model API checks passed!\n")
    sys.stdout.flush()
    time.sleep(0.2)

    # Agent头部信息
    print("=" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("Phone Agent - AI-powered phone automation")
    sys.stdout.flush()
    time.sleep(0.1)

    print("=" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("Model: autoglm-phone-9b")
    sys.stdout.flush()
    time.sleep(0.1)

    print("Base URL: http://localhost:8000/v1")
    sys.stdout.flush()
    time.sleep(0.1)

    print("Max Steps: 100")
    sys.stdout.flush()
    time.sleep(0.1)

    print("Language: cn")
    sys.stdout.flush()
    time.sleep(0.1)

    print("Device: emulator-5554 (auto-detected)")
    sys.stdout.flush()
    time.sleep(0.1)

    print("=" * 50)
    sys.stdout.flush()
    time.sleep(0.2)

    # 任务开始
    print("\nTask: 打开微信给张三发消息\n")
    sys.stdout.flush()
    time.sleep(0.3)

    # 第一步：启动应用
    print("\n" + "=" * 50)
    sys.stdout.flush()
    time.sleep(0.2)

    print("Thinking:")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("用户要求打开微信给张三发消息。我需要先启动微信应用。")
    sys.stdout.flush()
    time.sleep(0.2)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("Action:")
    sys.stdout.flush()
    time.sleep(0.1)

    print('{\n  "action": "Launch",\n  "app": "微信"\n}')
    sys.stdout.flush()
    time.sleep(0.1)

    print("=" * 50 + "\n")
    sys.stdout.flush()
    time.sleep(0.5)

    # 第二步：点击操作
    print("\n" + "=" * 50)
    sys.stdout.flush()
    time.sleep(0.2)

    print("Thinking:")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("微信已经打开，现在需要找到张三的聊天窗口并点击进入。")
    sys.stdout.flush()
    time.sleep(0.2)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("Action:")
    sys.stdout.flush()
    time.sleep(0.1)

    print('{\n  "action": "Tap",\n  "element": [300, 400]\n}')
    sys.stdout.flush()
    time.sleep(0.1)

    print("=" * 50 + "\n")
    sys.stdout.flush()
    time.sleep(0.5)

    # 第三步：输入文字
    print("\n" + "=" * 50)
    sys.stdout.flush()
    time.sleep(0.2)

    print("Thinking:")
    sys.stdout.flush()
    time.sleep(0.1)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("进入了张三的聊天窗口，现在需要输入消息内容。")
    sys.stdout.flush()
    time.sleep(0.2)

    print("-" * 50)
    sys.stdout.flush()
    time.sleep(0.1)

    print("Action:")
    sys.stdout.flush()
    time.sleep(0.1)

    print('{\n  "action": "Type",\n  "text": "你好！"\n}')
    sys.stdout.flush()
    time.sleep(0.1)

    print("=" * 50 + "\n")
    sys.stdout.flush()
    time.sleep(0.5)

    # 任务完成
    print("\n" + "Task Completed " + "=" * 38)
    sys.stdout.flush()
    time.sleep(0.2)

    print("Task completed: 已成功给张三发送消息")
    sys.stdout.flush()
    time.sleep(0.1)

    print("=" * 50 + "\n")
    sys.stdout.flush()
    time.sleep(0.2)

    print("Result: 已成功给张三发送消息")
    sys.stdout.flush()
    time.sleep(0.1)

if __name__ == "__main__":
    print("开始模拟AI Agent实时输出...")
    sys.stdout.flush()
    time.sleep(0.5)

    simulate_agent_output()

    print("\n✅ 模拟完成")
    sys.stdout.flush()
