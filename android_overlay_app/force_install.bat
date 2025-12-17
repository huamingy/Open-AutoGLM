@echo off
chcp 65001 >nul
echo ========================================
echo 🚨 AutoGLM 强制安装工具
echo ========================================
echo.

set "PACKAGE_NAME=com.autoglm.overlay"
set "APK_FILE=build\outputs\apk\debug\android_overlay_app-debug.apk"

echo 📱 检查设备连接...
adb devices | findstr "device"
if %errorlevel% neq 0 (
    echo ❌ 未检测到设备连接
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
    set /p selected_device="请输入设备ID: "
    if defined selected_device (
        set "ADB_CMD=adb -s %selected_device%"
    ) else (
        set "ADB_CMD=adb"
    )
) else (
    for /f "tokens=1" %%d in ('adb devices ^| findstr "device$"') do (
        set "ADB_CMD=adb -s %%d"
    )
)

echo.
echo 🔧 强制安装流程:
echo.

echo 1️⃣ 停止应用进程...
%ADB_CMD% shell am force-stop %PACKAGE_NAME%
timeout /t 1 /nobreak >nul

echo 2️⃣ 卸载旧版本...
%ADB_CMD% uninstall %PACKAGE_NAME%
timeout /t 1 /nobreak >nul

echo 3️⃣ 清理应用数据...
%ADB_CMD% shell pm clear %PACKAGE_NAME% 2>nul
timeout /t 1 /nobreak >nul

echo 4️⃣ 安装新版本 (无权限授予，避免卡住)...
%ADB_CMD% install -r "%APK_FILE%"
if %errorlevel% neq 0 (
    echo ❌ 安装失败
    echo.
    echo 🔧 尝试其他方法:
    echo.
    echo 方法1: 使用 -d 参数 (降级安装)
    %ADB_CMD% install -r -d "%APK_FILE%"
    if %errorlevel% neq 0 (
        echo ❌ 降级安装也失败
        echo.
        echo 方法2: 使用 -t 参数 (允许测试APK)
        %ADB_CMD% install -r -t "%APK_FILE%"
        if %errorlevel% neq 0 (
            echo ❌ 所有安装方法都失败
            echo.
            echo 💡 请手动检查:
            echo • 设备存储空间是否充足
            echo • 设备是否允许安装未知来源应用
            echo • ADB连接是否稳定
            pause
            exit /b 1
        )
    )
)

echo ✅ 安装成功
echo.

echo 5️⃣ 授予必要权限...
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.SYSTEM_ALERT_WINDOW
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.INTERNET
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.ACCESS_NETWORK_STATE

echo.
echo ========================================
echo 🎉 强制安装完成！
echo ========================================
echo.
echo 🚀 启动应用...
%ADB_CMD% shell am start -n %PACKAGE_NAME%/.MainActivity

pause
