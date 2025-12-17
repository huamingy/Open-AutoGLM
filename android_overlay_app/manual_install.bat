@echo off
chcp 65001 >nul
echo ========================================
echo 📦 AutoGLM 手动安装工具
echo ========================================
echo.

set "PACKAGE_NAME=com.autoglm.overlay"
set "MAIN_ACTIVITY=%PACKAGE_NAME%/.MainActivity"
set "APK_FILE=build\outputs\apk\debug\android_overlay_app-debug.apk"

echo 🔍 检查APK文件...
if not exist "%APK_FILE%" (
    echo ❌ APK文件不存在: %APK_FILE%
    echo 请先运行构建脚本
    pause
    exit /b 1
)
echo ✅ APK文件存在
echo.

echo 📱 检查设备连接...
adb devices | findstr "device"
if %errorlevel% neq 0 (
    echo ❌ 未检测到设备连接
    echo 请确保设备已连接并开启USB调试
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

echo 🔧 选择安装方式:
echo [1] 正常安装 (推荐)
echo [2] 强制覆盖安装
echo [3] 先卸载再安装
echo [4] 仅授予权限
echo [5] 检查应用状态
echo.

set /p choice="请选择 (1-5): "

if "%choice%"=="1" goto normal_install
if "%choice%"=="2" goto force_install
if "%choice%"=="3" goto uninstall_install
if "%choice%"=="4" goto grant_permissions
if "%choice%"=="5" goto check_status
goto invalid_choice

:normal_install
echo.
echo 📦 执行正常安装...
%ADB_CMD% install -r -g "%APK_FILE%"
if %errorlevel% neq 0 (
    echo ❌ 安装失败 - 尝试自动修复签名冲突...
    echo.

    echo 🗑️ 卸载冲突的应用版本...
    %ADB_CMD% uninstall %PACKAGE_NAME%
    if %errorlevel% neq 0 (
        echo ⚠️ 卸载失败，可能应用不存在
    ) else (
        echo ✅ 冲突版本已卸载
    )

    echo.
    echo 📦 重新安装应用...
    %ADB_CMD% install -r -g "%APK_FILE%"
    if %errorlevel% neq 0 (
        echo ❌ 重新安装仍然失败
        goto install_failed
    ) else (
        echo ✅ 安装成功 (已自动修复签名冲突)
    )
)
goto install_success

:force_install
echo.
echo 📦 执行强制覆盖安装...
adb install -r -g --force-agent "%APK_FILE%"
if %errorlevel% neq 0 goto install_failed
goto install_success

:uninstall_install
echo.
echo 🗑️ 先卸载旧版本...
%ADB_CMD% uninstall %PACKAGE_NAME%
echo.
echo 📦 重新安装...
%ADB_CMD% install -r -g "%APK_FILE%"
if %errorlevel% neq 0 goto install_failed
goto install_success

:grant_permissions
echo.
echo 🔐 仅授予权限...
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.SYSTEM_ALERT_WINDOW
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.INTERNET
%ADB_CMD% shell pm grant %PACKAGE_NAME% android.permission.ACCESS_NETWORK_STATE
echo ✅ 权限已授予
goto end

:check_status
echo.
echo 📊 检查应用状态...
echo.
echo 📋 已安装的应用版本:
%ADB_CMD% shell dumpsys package %PACKAGE_NAME% | findstr "versionName"
echo.
echo 🔐 应用权限状态:
%ADB_CMD% shell dumpsys package %PACKAGE_NAME% | findstr "permission"
echo.
echo 🚀 应用运行状态:
%ADB_CMD% shell ps | findstr "%PACKAGE_NAME%"
goto end

:install_success
echo.
echo ✅ 安装成功！
echo.
echo 🚀 启动应用...
%ADB_CMD% shell am start -n %MAIN_ACTIVITY%
if %errorlevel% neq 0 (
    echo ⚠️ 应用启动失败，可能需要手动启动
) else (
    echo ✅ 应用已启动
)
goto end

:install_failed
echo.
echo ❌ 安装失败
echo.
echo 🔧 故障排除步骤:
echo.
echo 1️⃣ 检查设备设置:
echo    • 设置 -> 隐私/安全 -> 未知来源 -> 允许
echo    • 设置 -> 开发者选项 -> USB调试 -> 开启
echo    • 设置 -> 开发者选项 -> 无线ADB调试 -> 开启
echo.
echo 2️⃣ 尝试手动操作:
echo    adb kill-server
echo    adb start-server
echo    adb devices
echo.
echo 3️⃣ 清理旧版本:
echo    %ADB_CMD% uninstall %PACKAGE_NAME%
echo    adb install -r "%APK_FILE%"
echo.
echo 4️⃣ 检查存储空间:
echo    adb shell df /data
echo.
echo 5️⃣ 重启设备后重试
echo.
pause
exit /b 1

:invalid_choice
echo ❌ 无效选择，请输入1-5之间的数字
pause
exit /b 1

:end
echo.
echo ========================================
echo 🎉 操作完成！
echo ========================================
pause
