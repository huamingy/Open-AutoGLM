@echo off
chcp 65001 >nul
echo ========================================
echo 📊 AutoGLM 开发日志查看器
echo ========================================
echo.

echo 🔍 正在查看应用日志...
echo (按 Ctrl+C 停止查看)
echo.

adb logcat -c
adb logcat | findstr -i "autoglm\|websocket\|webview\|android_interface"
