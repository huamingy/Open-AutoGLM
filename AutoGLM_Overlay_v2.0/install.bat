@echo off
chcp 65001 >nul
echo ========================================
echo 🤖 AutoGLM Overlay v2.0 (已签名) 快速安装脚本
echo ========================================
echo.

set "APK_FILE=android_overlay_app-release-unsigned.apk"

echo 🔍 检查ADB环境...
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到ADB，请确保Android SDK已正确安装
    echo.
    echo 请下载Android SDK Platform Tools:
    echo https://developer.android.com/studio/releases/platform-tools
    pause
    exit /b 1
)
echo ✅ ADB环境正常

echo.
echo 📱 检查设备连接...
adb devices | findstr /v "List" | findstr "." >nul
if %errorlevel% neq 0 (
    echo ❌ 未检测到连接的Android设备
    echo.
    echo 请确保:
    echo 1. 手机已连接电脑
    echo 2. USB调试已开启
    echo 3. 允许USB调试授权
    pause
    exit /b 1
)
echo ✅ 设备已连接

echo.
echo 📦 正在安装应用...
adb install -r "%APK_FILE%"
if %errorlevel% neq 0 (
    echo ❌ 应用安装失败
    echo.
    echo 可能的原因:
    echo 1. APK文件损坏
    echo 2. 存储空间不足
    echo 3. 应用已被其他证书签名
    pause
    exit /b 1
)
echo ✅ 应用安装成功

echo.
echo 🚀 启动应用...
adb shell am start -n com.autoglm.overlay/.MainActivity
if %errorlevel% neq 0 (
    echo ⚠️ 应用启动可能失败，请手动启动
)

echo.
echo ========================================
echo 🎉 安装完成！
echo ========================================
echo.
echo 📋 下一步操作:
echo 1. 在手机上打开 "AutoGLM Overlay" 应用
echo 2. 选择 "🌐 打开Web界面"
echo 3. 确保无障碍服务已开启
echo 4. 在电脑上运行: python ws.py
echo 5. 开始使用AI助手！
echo.
echo 🔗 更多信息请查看 README.md
echo.
pause
