@echo off
chcp 65001 >nul
echo ========================================
echo 🛑 终止卡住的安装进程
echo ========================================
echo.

echo 🔍 查找ADB进程...
tasklist | findstr "adb.exe"
if %errorlevel% neq 0 (
    echo ⚠️ 未找到ADB进程
) else (
    echo 📋 找到ADB进程，正在终止...
    taskkill /F /IM adb.exe 2>nul
    if %errorlevel% equ 0 (
        echo ✅ ADB进程已终止
    ) else (
        echo ⚠️ 终止失败或进程不存在
    )
)

echo.
echo 🔄 重启ADB服务...
timeout /t 2 /nobreak >nul
adb kill-server
timeout /t 1 /nobreak >nul
adb start-server

echo.
echo 📱 检查设备连接...
adb devices

echo.
echo ========================================
echo ✅ 清理完成！
echo ========================================
echo.
echo 💡 现在可以:
echo • 重新运行 quick_dev.bat
echo • 或使用 force_install.bat 强制安装
echo.
pause
