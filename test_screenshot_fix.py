#!/usr/bin/env python3
"""
测试修复后的截图功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from phone_agent.adb import get_screenshot


def test_screenshot():
    """测试截图功能"""
    device_id = "192.168.2.233:5555"  # 根据实际情况修改

    print("测试截图功能...")
    print("=" * 50)

    try:
        print("正在获取截图...")
        screenshot = get_screenshot(device_id, timeout=15)

        print(f"截图获取成功!")
        print(f"  - 宽度: {screenshot.width}")
        print(f"  - 高度: {screenshot.height}")
        print(f"  - 是否敏感屏幕: {screenshot.is_sensitive}")
        print(f"  - 图片数据长度: {len(screenshot.base64_data)} 字符")

        if screenshot.is_sensitive:
            print("检测到敏感屏幕（可能是登录界面或支付页面）")
        else:
            print("普通屏幕，AI可以正常操作")

    except Exception as e:
        print(f"截图测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_screenshot()
