#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试编码修复是否有效
"""

import subprocess
import sys

def test_encoding_fix():
    """测试ADB命令的编码处理"""
    print("Testing ADB command encoding fix...", file=sys.stdout, flush=True)

    try:
        # 测试一个简单的ADB命令
        result = subprocess.run(
            ["adb", "version"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )

        if result.returncode == 0:
            print("SUCCESS: ADB command executed successfully, no encoding errors", file=sys.stdout, flush=True)
            print(f"Version info: {result.stdout[:100]}...", file=sys.stdout, flush=True)
        else:
            print(f"FAILED: ADB command failed: {result.stderr}", file=sys.stdout, flush=True)

    except FileNotFoundError:
        print("WARNING: ADB not found, skipping test", file=sys.stdout, flush=True)
    except Exception as e:
        print(f"ERROR: Test failed: {e}", file=sys.stdout, flush=True)

    print("Encoding fix test completed", file=sys.stdout, flush=True)

if __name__ == "__main__":
    test_encoding_fix()
