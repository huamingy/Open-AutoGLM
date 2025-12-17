#!/usr/bin/env python3
"""
演示命令执行过程中的自动屏幕解锁功能
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phone_agent.adb import prepare_screen_for_operation, get_screen_state


def simulate_ai_operation_step(step_name, device_id):
    """模拟AI执行一个操作步骤，包括屏幕状态检查"""
    print(f"\n{'='*50}")
    print(f"执行步骤: {step_name}")
    print('='*50)

    # 步骤1: 检查屏幕状态并自动处理
    print("检查屏幕状态...")
    state = get_screen_state(device_id)

    print("当前屏幕状态:")
    print(f"  - 屏幕开启: {'是' if state['screen_on'] else '否'}")
    print(f"  - 屏幕唤醒: {'是' if state['awake'] else '否'}")
    print(f"  - 屏幕锁定: {'是' if state['screen_locked'] else '否'}")

    # 模拟AI执行前的屏幕准备
    print("\n准备屏幕进行AI操作...")
    success = prepare_screen_for_operation(device_id)

    if success:
        print("屏幕准备完成!")
        print("  - 屏幕已唤醒")
        print("  - 屏幕已解锁（如果之前锁定）")
        print("  - 已设置屏幕常亮（30分钟）")
    else:
        print("屏幕准备部分完成")

    # 步骤2: 模拟AI分析和操作
    print("\nAI正在分析屏幕内容...")
    print("   正在获取截图...")
    print("   正在识别界面元素...")
    print("   正在制定操作策略...")

    # 步骤3: 模拟执行操作
    print(f"\n执行操作: {step_name}")
    print("   发送ADB命令...")
    print("   等待操作完成...")
    print("   验证操作结果...")

    print(f"\n步骤 '{step_name}' 执行完成!")


def demo_auto_screen_unlock():
    """演示完整的自动屏幕解锁流程"""
    device_id = "192.168.2.233:5555"  # 根据实际情况修改

    print("=" * 70)
    print("AutoGLM 命令执行过程中的自动屏幕解锁演示")
    print("=" * 70)

    print("\n功能说明:")
    print("  在AI执行每个操作步骤前，自动检查并处理屏幕状态:")
    print("  - 检测屏幕是否休眠 -> 自动唤醒")
    print("  - 检测屏幕是否锁定 -> 自动解锁（无密码设备）")
    print("  - 确保屏幕保持常亮 -> 避免操作中断")
    print("  - 实时反馈操作状态 -> Web界面显示")

    print(f"\n测试设备ID: {device_id}")

    # 模拟AI执行过程
    steps = ["启动应用", "导航页面", "执行操作"]

    for i, step in enumerate(steps, 1):
        simulate_ai_operation_step(f"{i}. {step}", device_id)
        print("\n等待2秒进入下一步...")
        time.sleep(2)

    print("\n" + "=" * 70)
    print("演示完成!")

    print("\n实际效果:")
    print("  - AI执行任务时自动处理锁屏")
    print("  - 无需手动解锁屏幕")
    print("  - 操作过程更加流畅")


if __name__ == "__main__":
    demo_auto_screen_unlock()
