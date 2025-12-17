#!/usr/bin/env python3
"""
测试屏幕控制功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phone_agent.adb import (
    get_screen_state,
    wake_screen,
    unlock_screen,
    keep_screen_awake,
    restore_screen_timeout,
    prepare_screen_for_operation,
    cleanup_screen_settings,
)


def test_screen_functions():
    """测试屏幕控制功能"""
    device_id = "192.168.2.233:5555"  # 根据实际情况修改

    print("测试屏幕控制功能...")
    print("=" * 50)

    # 1. 检查当前屏幕状态
    print("1. 检查屏幕状态:")
    try:
        state = get_screen_state(device_id)
        print(f"   屏幕开启: {state['screen_on']}")
        print(f"   屏幕锁定: {state['screen_locked']}")
        print(f"   屏幕唤醒: {state['awake']}")
    except Exception as e:
        print(f"   获取状态失败: {e}")

    # 2. 唤醒屏幕
    print("\n2. 唤醒屏幕:")
    try:
        success = wake_screen(device_id)
        print(f"   唤醒结果: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"   唤醒失败: {e}")

    # 3. 解锁屏幕
    print("\n3. 解锁屏幕:")
    try:
        success = unlock_screen(device_id)
        print(f"   解锁结果: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"   解锁失败: {e}")

    # 4. 保持屏幕常亮
    print("\n4. 保持屏幕常亮:")
    try:
        success = keep_screen_awake(device_id, 5)  # 5分钟
        print(f"   设置结果: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"   设置失败: {e}")

    # 5. 准备屏幕进行操作
    print("\n5. 完整屏幕准备:")
    try:
        success = prepare_screen_for_operation(device_id)
        print(f"   准备结果: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"   准备失败: {e}")

    # 6. 最终状态检查
    print("\n6. 最终屏幕状态:")
    try:
        state = get_screen_state(device_id)
        print(f"   屏幕开启: {state['screen_on']}")
        print(f"   屏幕锁定: {state['screen_locked']}")
        print(f"   屏幕唤醒: {state['awake']}")
    except Exception as e:
        print(f"   获取状态失败: {e}")

    # 7. 清理设置
    print("\n7. 清理屏幕设置:")
    try:
        success = cleanup_screen_settings(device_id)
        print(f"   清理结果: {'成功' if success else '失败'}")
    except Exception as e:
        print(f"   清理失败: {e}")

    print("\n" + "=" * 50)
    print("测试完成！")


if __name__ == "__main__":
    test_screen_functions()
