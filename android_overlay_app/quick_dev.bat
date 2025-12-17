@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 AutoGLM 快速开发工具
echo ========================================
echo.

set "DEVICE_IP=192.168.2.233"
set "ADB_PORT=5555"

echo 📱 连接设备: %DEVICE_IP%:%ADB_PORT%
adb connect %DEVICE_IP%:%ADB_PORT%
if %errorlevel% neq 0 (
    echo ❌ 设备连接失败
    echo 尝试继续使用已连接的设备...
)

echo 📋 检查设备连接状态...
adb devices | findstr "device"
if %errorlevel% neq 0 (
    echo ❌ 无设备连接
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

echo 🔨 快速构建Debug版本...
call gradlew.bat assembleDebug --no-daemon --parallel
if %errorlevel% neq 0 (
    echo ❌ 构建失败
    pause
    exit /b 1
)
echo ✅ 构建成功
echo.

echo 📦 安装APK...
echo 🔐 授予所有权限并安装...
echo 💡 提示: 如果安装卡住，请按 Ctrl+C 中断，然后运行 force_install.bat
echo.

REM 先尝试简单安装（不带-g参数，避免卡住）
echo 尝试安装 (如果卡住超过30秒，请按 Ctrl+C 中断)...
%ADB_CMD% install -r build\outputs\apk\debug\android_overlay_app-debug.apk
if %errorlevel% neq 0 (
    echo ⚠️ 安装失败 - 尝试自动修复...
    echo.

    echo 🗑️ 卸载旧版本应用...
    %ADB_CMD% uninstall com.autoglm.overlay
    if %errorlevel% neq 0 (
        echo ⚠️ 卸载失败，可能应用不存在
    ) else (
        echo ✅ 旧版本已卸载
    )

    echo.
    echo 📦 重新安装应用...
    %ADB_CMD% install -r build\outputs\apk\debug\android_overlay_app-debug.apk
    if %errorlevel% neq 0 (
        echo ❌ 重新安装仍然失败
        echo.
        echo 🔧 请尝试:
        echo • 运行 force_install.bat (强制安装)
        echo • 或运行 kill_install.bat (清理后重试)
        echo.
        pause
        exit /b 1
    ) else (
        echo ✅ 安装成功 (已自动修复签名冲突)
    )
) else (
    echo ✅ 安装成功
)

REM 安装成功后授予权限
echo.
echo 🔐 授予必要权限...
%ADB_CMD% shell pm grant com.autoglm.overlay android.permission.SYSTEM_ALERT_WINDOW 2>nul
%ADB_CMD% shell pm grant com.autoglm.overlay android.permission.INTERNET 2>nul
%ADB_CMD% shell pm grant com.autoglm.overlay android.permission.ACCESS_NETWORK_STATE 2>nul
echo ✅ 权限已授予
echo ✅ 安装成功
echo.

echo 🚀 启动应用...
%ADB_CMD% shell am start -n com.autoglm.overlay/.MainActivity
if %errorlevel% neq 0 (
    echo ❌ 启动失败
    pause
    exit /b 1
)
echo ✅ 应用已启动
echo.

echo ========================================
echo 🎉 开发部署完成！
echo ========================================
echo.
echo 💡 提示:
echo - 修改代码后再次运行此脚本即可快速更新
echo - 应用将在开发模式下运行，日志更详细
echo - 如需查看实时日志: adb logcat | findstr "autoglm"
echo.
pause
