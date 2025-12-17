@echo off
chcp 65001 >nul
echo ========================================
echo 📱 AutoGLM 设备无线连接工具
echo ========================================
echo.

if "%~1"=="" (
    set "DEVICE_IP=192.168.2.233"
) else (
    set "DEVICE_IP=%~1"
)

if "%~2"=="" (
    set "ADB_PORT=5555"
) else (
    set "ADB_PORT=%~2"
)

echo 🔍 查找已连接设备...
adb devices
echo.

echo 📡 启用设备无线调试...
adb tcpip %ADB_PORT%
if %errorlevel% neq 0 (
    echo ❌ 启用无线调试失败
    echo 请确保设备已通过USB连接
    pause
    exit /b 1
)
echo ✅ 无线调试已启用 (端口: %ADB_PORT%)
echo.

echo 🔌 连接到设备: %DEVICE_IP%:%ADB_PORT%
adb connect %DEVICE_IP%:%ADB_PORT%
if %errorlevel% neq 0 (
    echo ❌ 设备连接失败
    echo 可能的原因:
    echo - 设备IP地址不正确
    echo - 设备未开启无线调试
    echo - 网络连接问题
    echo.
    echo 解决建议:
    echo 1. 检查设备IP: 设置 -> 关于手机 -> 状态信息
    echo 2. 确认USB连接正常
    echo 3. 尝试不同的端口号
    pause
    exit /b 1
)
echo ✅ 设备连接成功
echo.

echo 📋 当前连接的设备:
adb devices
echo.

echo ========================================
echo 🎉 设备连接完成！
echo ========================================
echo.
echo 💡 使用提示:
echo - 现在可以断开USB线缆
echo - 设备将通过WiFi连接
echo - 如需重新连接，只需运行: connect_device.bat
echo.
pause
