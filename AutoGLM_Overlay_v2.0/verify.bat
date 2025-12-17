@echo off
chcp 65001 >nul
echo ========================================
echo 🔍 AutoGLM Overlay 环境验证脚本
echo ========================================
echo.

echo 📱 检查ADB连接...
adb devices | findstr /v "List" | findstr "." >nul
if %errorlevel% neq 0 (
    echo ❌ 未检测到Android设备连接
    echo 请检查USB连接和USB调试设置
    goto :error
)
echo ✅ Android设备已连接

echo.
echo 📦 检查应用安装状态...
adb shell pm list packages | findstr "com.autoglm.overlay" >nul
if %errorlevel% neq 0 (
    echo ❌ AutoGLM Overlay应用未安装
    echo 请先运行 install.bat 安装应用
    goto :error
)
echo ✅ 应用已安装

echo.
echo ⚙️ 检查无障碍服务...
adb shell settings get secure enabled_accessibility_services | findstr "com.autoglm.overlay" >nul
if %errorlevel% neq 0 (
    echo ⚠️ 无障碍服务可能未开启
    echo 请在手机设置中开启: 设置 → 无障碍 → AutoGLM Overlay
) else (
    echo ✅ 无障碍服务已开启
)

echo.
echo 🪟 检查悬浮窗权限...
adb shell appops get com.autoglm.overlay SYSTEM_ALERT_WINDOW | findstr "allow" >nul
if %errorlevel% neq 0 (
    echo ⚠️ 悬浮窗权限可能未开启
    echo 请在应用设置中开启: 显示在其他应用上层
) else (
    echo ✅ 悬浮窗权限已开启
)

echo.
echo 🌐 检查网络连接...
ping -n 1 192.168.1.1 >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ 网络连接可能有问题
    echo 请检查WiFi连接
) else (
    echo ✅ 网络连接正常
)

echo.
echo ========================================
echo ✅ 环境验证完成
echo ========================================
echo.
echo 💡 提示:
echo - 如果有任何 ❌ 或 ⚠️ 标记，请根据提示解决
echo - 所有项目都 ✅ 表示环境配置正确
echo - 可以开始使用AutoGLM AI助手了！
echo.
goto :end

:error
echo.
echo ❌ 环境验证失败
echo 请解决上述问题后重试
echo.

:end
pause
