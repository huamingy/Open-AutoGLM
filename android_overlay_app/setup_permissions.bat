@echo off
chcp 65001 >nul
echo ========================================
echo 🔐 AutoGLM 权限设置工具
echo ========================================
echo.

set "PACKAGE_NAME=com.autoglm.overlay"

echo 📱 检查设备连接...
adb devices | findstr "device"
if %errorlevel% neq 0 (
    echo ❌ 未检测到设备连接
    echo 请确保设备已通过USB或WiFi连接
    pause
    exit /b 1
)

for /f %%i in ('adb devices ^| find /c "device"') do set device_count=%%i
if %device_count% gtr 1 (
    echo ⚠️ 检测到多个设备连接
    echo.
    echo 📋 可用的设备:
    for /f "tokens=1" %%d in ('adb devices ^| findstr "device$"') do (
        echo • %%d
    )
    echo.
    echo 💡 提示: 直接复制粘贴上面的设备ID
    echo.
    :device_input
    set /p selected_device="请输入设备ID (例如: 192.168.2.233:5555): "
    if defined selected_device (
        echo 测试设备连接: %selected_device%
        adb -s %selected_device% shell echo "test" >nul 2>&1
        if %errorlevel% equ 0 (
            set "ADB_CMD=adb -s %selected_device%"
            echo ✅ 已选择设备: %selected_device%
        ) else (
            echo ❌ 设备 '%selected_device%' 不可用或不存在
            echo 请从上面的列表中选择正确的设备ID
            goto device_input
        )
    ) else (
        echo ❌ 必须选择一个设备
        goto device_input
    )
) else (
    if %device_count% equ 1 (
        for /f "tokens=1" %%d in ('adb devices ^| findstr "device$"') do (
            set "ADB_CMD=adb -s %%d"
            echo ✅ 自动选择设备: %%d
        )
    ) else (
        set "ADB_CMD=adb"
        echo ✅ 设备已连接
    )
)
echo.

echo 🔧 检查应用是否已安装...
%ADB_CMD% shell pm list packages | findstr "%PACKAGE_NAME%"
if %errorlevel% neq 0 (
    echo ⚠️ 应用未安装，请先安装APK
    echo 运行: manual_install.bat
    pause
    exit /b 1
)
echo ✅ 应用已安装
echo.

echo 🔐 授予必要权限...

echo 📱 SYSTEM_ALERT_WINDOW (悬浮窗权限)...
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.SYSTEM_ALERT_WINDOW
if %errorlevel% neq 0 (
    echo ⚠️ 悬浮窗权限授予失败
    echo 请手动设置: 设置 -> 应用 -> AutoGLM Overlay -> 显示在其他应用上层 -> 允许
) else (
    echo ✅ 悬浮窗权限已授予
)

echo 🌐 INTERNET (网络权限)...
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.INTERNET
if %errorlevel% neq 0 (
    echo ⚠️ 网络权限授予失败
) else (
    echo ✅ 网络权限已授予
)

echo 📊 ACCESS_NETWORK_STATE (网络状态权限)...
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.ACCESS_NETWORK_STATE
if %errorlevel% neq 0 (
    echo ⚠️ 网络状态权限授予失败
) else (
    echo ✅ 网络状态权限已授予
)

echo 🔧 启用无障碍服务...
echo 请手动完成以下步骤:
echo 1. 打开 设置 -> 无障碍 -> AutoGLM Overlay
echo 2. 开启 AutoGLM Overlay 服务
echo 3. 确认服务已启用
echo.
echo 💡 按任意键继续...
pause >nul

echo 🔍 验证权限设置...

echo 📊 检查悬浮窗权限:
%ADB_CMD% shell dumpsys package %PACKAGE_NAME% | findstr "SYSTEM_ALERT_WINDOW" | findstr "granted=true"
if %errorlevel% neq 0 (
    echo ❌ 悬浮窗权限未正确设置
) else (
    echo ✅ 悬浮窗权限正常
)

echo 📊 检查无障碍服务:
%ADB_CMD% shell settings get secure enabled_accessibility_services | findstr "%PACKAGE_NAME%"
if %errorlevel% neq 0 (
    echo ❌ 无障碍服务未启用
) else (
    echo ✅ 无障碍服务已启用
)

echo.
echo 📋 权限设置完成！
echo.
echo 💡 如果仍有问题，请检查:
echo • 设备是否为Android 6.0以上版本
echo • 应用是否有系统级权限要求
echo • 设备是否为Root设备（可选）
echo.
echo 🎯 现在可以正常使用应用了！
echo.

pause
