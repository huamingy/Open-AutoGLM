#!/usr/bin/env python3
"""
AutoGLM WebSocket Server 启动脚本

启动WebSocket服务器，提供网页端实时控制界面
"""

import os
import sys

def main():
    """启动WebSocket服务器"""
    print("🚀 启动 AutoGLM WebSocket 服务器...")
    print("📝 启动命令: python ws.py")
    print("🌍 浏览器访问: http://localhost:8001")
    print("📄 控制页面: index.html")
    print("\n按 Ctrl+C 停止服务器\n")

    # 启动WebSocket服务器
    os.system(f"{sys.executable} ws.py")

if __name__ == "__main__":
    main()
