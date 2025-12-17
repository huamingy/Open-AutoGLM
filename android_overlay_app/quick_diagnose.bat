@echo off
chcp 65001 >nul
echo ========================================
echo 🔍 AutoGLM 快速诊断工具
echo ========================================
echo.

set "PACKAGE_NAME=com.autoglm.overlay"
set "APK_FILE=build\outputs\apk\debug\android_overlay_app-debug.apk"

echo 📱 1. 检查设备连接...
adb devices | findstr "device"
if %errorlevel% neq 0 (
    echo ❌ 设备未连接
    echo 解决方案:
    echo • 确保USB线缆连接正常
    echo • 或使用WiFi连接: connect_device.bat
    goto end
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

echo 📦 2. 检查APK文件...
if not exist "%APK_FILE%" (
    echo ❌ APK文件不存在
    echo 解决方案:
    echo • 运行构建: gradlew.bat assembleDebug
    goto end
)
echo ✅ APK文件存在 (%APK_FILE%)
echo.

echo 📋 3. 检查应用安装状态...
%ADB_CMD% shell pm list packages | findstr "%PACKAGE_NAME%"
if %errorlevel% neq 0 (
    echo ⚠️ 应用未安装
) else (
    echo ✅ 应用已安装
)
echo.

echo 🔐 4. 检查关键权限...
echo.

echo 📱 悬浮窗权限:
%ADB_CMD% shell dumpsys package %PACKAGE_NAME% 2>nul | findstr "SYSTEM_ALERT_WINDOW" | findstr "granted=true"
if %errorlevel% neq 0 (
    echo ❌ 悬浮窗权限未授予
    echo 解决方案: 设置 -> 应用 -> AutoGLM Overlay -> 显示在其他应用上层
) else (
    echo ✅ 悬浮窗权限已授予
)

echo 🌐 网络权限:
%ADB_CMD% shell dumpsys package %PACKAGE_NAME% 2>nul | findstr "INTERNET" | findstr "granted=true"
if %errorlevel% neq 0 (
    echo ❌ 网络权限未授予
) else (
    echo ✅ 网络权限已授予
)
echo.

echo ♿ 5. 检查无障碍服务...
%ADB_CMD% shell settings get secure enabled_accessibility_services 2>nul | findstr "%PACKAGE_NAME%"
if %errorlevel% neq 0 (
    echo ❌ 无障碍服务未启用
    echo 解决方案: 设置 -> 无障碍 -> AutoGLM Overlay -> 开启
) else (
    echo ✅ 无障碍服务已启用
)
echo.

echo 💾 6. 检查存储空间...
for /f "tokens=*" %%i in ('%ADB_CMD% shell df /data ^| findstr "/data"') do (
    echo 存储空间: %%i
)
echo.

echo 📊 7. 检查应用运行状态...
%ADB_CMD% shell ps 2>nul | findstr "%PACKAGE_NAME%"
if %errorlevel% neq 0 (
    echo ⚠️ 应用未运行
) else (
    echo ✅ 应用正在运行
)
echo.

echo 🎯 诊断完成！
echo.
echo 💡 根据上述结果选择解决方案:
echo.
echo 如果应用未安装:
echo • 运行: manual_install.bat
echo.
echo 如果权限未授予:
echo • 运行: setup_permissions.bat
echo.
echo 如果其他问题:
echo • 查看详细日志: dev_log.bat
echo • 重启设备后重试
echo.

:end
echo ========================================
pause
