#!/usr/bin/env python3
"""
屏幕控制功能演示脚本

这个脚本演示了AutoGLM项目中新增的屏幕控制功能：
- 自动唤醒锁屏
- 无密码解锁屏幕
- 保持屏幕常亮
"""

import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, ".")

from phone_agent.adb import prepare_screen_for_operation, cleanup_screen_settings


def demo_screen_control():
    """演示屏幕控制功能"""
    device_id = "192.168.2.233:5555"  # 请根据实际情况修改设备ID

    print("=" * 60)
    print("AutoGLM 屏幕控制功能演示")
    print("=" * 60)

    print("\n功能说明:")
    print("  - 自动检测屏幕状态")
    print("  - 唤醒锁屏设备")
    print("  - 无密码解锁屏幕")
    print("  - 保持屏幕常亮")
    print("  - 任务结束自动清理")

    print("\n当前设备ID:", device_id)
    print("提示: 如果设备已解锁且亮屏，解锁步骤会跳过")

    print("\n开始屏幕准备...")
    print("-" * 40)

    # 步骤1: 准备屏幕
    try:
        success = prepare_screen_for_operation(device_id)
        if success:
            print("屏幕准备成功！")
            print("   - 屏幕已唤醒")
            print("   - 屏幕已解锁（如果之前锁定）")
            print("   - 已设置屏幕常亮")
        else:
            print("屏幕准备部分成功")
            print("   可能某些设置需要手动确认")
    except Exception as e:
        print(f"屏幕准备失败: {e}")
        return

    print("\n等待10秒模拟AI操作...")
    for i in range(10, 0, -1):
        print(f"   剩余 {i} 秒...", end="\r")
        time.sleep(1)
    print("   操作完成！        ")

    print("\n清理屏幕设置...")
    print("-" * 40)

    # 步骤2: 清理设置
    try:
        success = cleanup_screen_settings(device_id)
        if success:
            print("屏幕设置已清理！")
            print("   - 恢复正常息屏时间")
            print("   - 重置充电时保持亮屏设置")
        else:
            print("清理可能不完整")
    except Exception as e:
        print(f"清理失败: {e}")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("\n使用说明:")
    print("   这个功能已集成到PhoneAgent中")
    print("   每次AI执行任务时会自动调用")
    print("   无需手动干预，享受无缝体验！")

    print("\n技术实现:")
    print("   - ADB shell命令控制屏幕")
    print("   - 自动检测设备分辨率")
    print("   - 滑动解锁适配不同设备")
    print("   - 智能超时和错误处理")


if __name__ == "__main__":
    demo_screen_control()
