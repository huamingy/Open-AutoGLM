#!/bin/bash

echo "========================================"
echo "AutoGLM 悬浮窗应用安装脚本 (Linux/Mac)"
echo "========================================"
echo

echo "[1/5] 检查系统要求..."
echo

# 检查Java
if ! command -v java &> /dev/null; then
    echo "❌ Java 未安装！"
    echo "请安装 JDK 8+："
    echo "  Ubuntu/Debian: sudo apt install openjdk-11-jdk"
    echo "  macOS: brew install openjdk@11"
    echo "  或从 https://adoptium.net/ 下载"
    echo
    exit 1
else
    echo "✅ Java 已安装"
fi

# 检查ADB
if ! command -v adb &> /dev/null; then
    echo "❌ ADB 未安装！"
    echo "请安装 Android SDK Platform Tools："
    echo "  Ubuntu/Debian: sudo apt install android-tools-adb"
    echo "  macOS: brew install android-platform-tools"
    echo "  或从 https://developer.android.com/studio/releases/platform-tools 下载"
    echo
    exit 1
else
    echo "✅ ADB 已安装"
fi

# 检查设备连接
echo
echo "[2/5] 检查设备连接..."
if ! adb devices | grep -q "device$"; then
    echo "❌ 未找到连接的Android设备！"
    echo "请："
    echo "1. 连接Android设备"
    echo "2. 启用USB调试 (设置 → 开发者选项 → USB调试)"
    echo "3. 允许USB调试授权"
    echo
    exit 1
else
    echo "✅ 设备已连接"
fi

echo
echo "[3/5] 查找APK文件..."

# 查找APK文件
APK_PATH=""
if [ -f "app/build/outputs/apk/debug/app-debug.apk" ]; then
    APK_PATH="app/build/outputs/apk/debug/app-debug.apk"
    echo "✅ 找到APK: $APK_PATH"
elif [ -f "build/outputs/apk/debug/app-debug.apk" ]; then
    APK_PATH="build/outputs/apk/debug/app-debug.apk"
    echo "✅ 找到APK: $APK_PATH"
else
    # 查找任何APK文件
    APK_FILES=( *.apk )
    if [ ${#APK_FILES[@]} -gt 0 ]; then
        APK_PATH="${APK_FILES[0]}"
        echo "✅ 找到APK: $APK_PATH"
    else
        echo "❌ 未找到APK文件！"
        echo "请先构建应用："
        echo
        echo "方法1 - 使用Android Studio："
        echo "1. 打开 android_overlay_app 文件夹"
        echo "2. Build -> Build APK(s)"
        echo
        echo "方法2 - 使用Gradle："
        echo "gradle build"
        echo
        echo "然后重新运行此脚本"
        echo
        exit 1
    fi
fi

echo
echo "[4/5] 安装应用到设备..."
echo "正在安装: $APK_PATH"

if adb install -r "$APK_PATH"; then
    echo "✅ 应用安装成功！"
else
    echo "❌ 应用安装失败！"
    echo "请检查设备连接和USB调试权限"
    exit 1
fi

echo
echo "[5/5] 启动应用..."
if adb shell am start -n com.autoglm.overlay/.MainActivity; then
    echo "✅ 应用启动成功！"
else
    echo "❌ 应用启动失败！"
    exit 1
fi

echo
echo "========================================"
echo "🎉 安装完成！"
echo "========================================"
echo
echo "📱 请在手机上完成以下设置："
echo
echo "1. 设置 → 无障碍 → AutoGLM Overlay → 开启"
echo "2. 设置 → 应用 → AutoGLM Overlay → 显示在其他应用上层 → 允许"
echo
echo "🧪 测试悬浮窗："
echo "adb shell am broadcast -a com.autoglm.overlay.UPDATE \\"
echo "  --es title \"测试\" --es content \"悬浮窗工作正常！\" --es status \"运行中\""
echo
echo "🚀 启动AI助手："
echo "python ws.py"
echo "浏览器访问: http://localhost:8001"
echo
echo "按回车键继续..."
read