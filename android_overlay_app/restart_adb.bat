@echo off
chcp 65001 >nul
echo ========================================
echo 🔄 ADB 服务重启工具
echo ========================================
echo.

echo 🛑 停止ADB服务...
adb kill-server
timeout /t 2 /nobreak >nul
echo ✅ ADB服务已停止
echo.

echo 🚀 启动ADB服务...
adb start-server
if %errorlevel% neq 0 (
    echo ❌ ADB服务启动失败
    echo 请检查ADB安装和环境变量
    pause
    exit /b 1
)
echo ✅ ADB服务已启动
echo.

echo 📱 等待设备连接...
timeout /t 3 /nobreak >nul

echo 📋 当前连接的设备:
adb devices
echo.

echo ========================================
echo 🎉 ADB服务重启完成！
echo ========================================
echo.
echo 💡 如果仍有连接问题，请尝试:
echo • 检查USB线缆连接
echo • 重启Android设备
echo • 使用WiFi连接: connect_device.bat
echo.
pause
