@echo off
chcp 65001 >nul
echo ========================================
echo Android SDK 手动设置向导
echo ========================================
echo.

echo 由于无法自动检测到Android SDK位置，
echo 请您手动指定Android SDK的安装路径。
echo.

echo 请从以下选项中选择：
echo.

:menu
echo [1] 使用默认路径 (C:\Users\%USERNAME%\AppData\Local\Android\Sdk)
echo [2] 使用自定义路径
echo [3] 查看常见安装位置
echo [4] 退出
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    set "SDK_PATH=C:\Users\%USERNAME%\AppData\Local\Android\Sdk"
    goto :validate_path
)

if "%choice%"=="2" (
    echo.
    echo 请输入Android SDK的完整路径：
    echo 示例：C:\Android\Sdk
    echo        C:\Program Files\Android\Android Studio\Sdk
    echo.
    set /p SDK_PATH="路径: "
    goto :validate_path
)

if "%choice%"=="3" (
    echo.
    echo 常见的Android SDK安装位置：
    echo.
    echo 1. C:\Users\%USERNAME%\AppData\Local\Android\Sdk
    echo    (Android Studio默认安装位置)
    echo.
    echo 2. C:\Android\Sdk
    echo    (手动安装的常见位置)
    echo.
    echo 3. C:\Program Files\Android\Android Studio\Sdk
    echo    (Android Studio程序目录)
    echo.
    echo 4. C:\Users\%USERNAME%\Android\Sdk
    echo    (用户目录)
    echo.
    echo 5. 检查ADB位置来推断SDK位置：
    echo    where adb (在命令提示符中运行)
    echo.
    goto :menu
)

if "%choice%"=="4" (
    echo.
    echo 退出设置。
    goto :end
)

echo 无效选择，请重新选择。
goto :menu

:validate_path
echo.
echo 检查路径: %SDK_PATH%
echo.

:: 检查路径是否存在
if not exist "%SDK_PATH%" (
    echo ❌ 路径不存在: %SDK_PATH%
    echo.
    echo 请确认路径正确，然后重试。
    goto :menu
)

:: 检查是否是有效的SDK目录
if not exist "%SDK_PATH%\platforms" (
    echo ❌ 不是有效的Android SDK目录
    echo 缺少 platforms 目录
    goto :menu
)

if not exist "%SDK_PATH%\platform-tools" (
    echo ❌ 不是有效的Android SDK目录
    echo 缺少 platform-tools 目录
    goto :menu
)

echo ✅ 找到有效的Android SDK: %SDK_PATH%
echo.

:: 创建local.properties文件
echo # Android SDK location > local.properties
echo sdk.dir=%SDK_PATH:\=\\% >> local.properties

echo ✅ local.properties 已创建
echo 内容：
type local.properties
echo.

echo ========================================
echo 🎉 Android SDK 设置完成！
echo ========================================
echo.
echo 现在可以构建Android应用：
echo gradlew.bat clean build
echo.
echo 或运行完整安装脚本：
echo build_and_install.bat
echo.

:end
pause
