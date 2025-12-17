@echo off
echo ========================================
echo Java JDK 自动安装脚本
echo ========================================
echo.
echo 这个脚本将帮助您下载并安装Java JDK
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ 管理员权限：已确认
) else (
    echo ❌ 管理员权限：需要管理员权限
    echo 请右键点击此文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo.
echo [1/4] 检查网络连接...
ping -n 1 google.com >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ 网络连接：正常
) else (
    echo ❌ 网络连接：失败
    echo 请检查网络连接后重试
    pause
    exit /b 1
)

echo.
echo [2/4] 创建临时目录...
if not exist "%TEMP%\jdk_install" mkdir "%TEMP%\jdk_install"
cd "%TEMP%\jdk_install"
echo ✅ 创建目录：%TEMP%\jdk_install

echo.
echo [3/4] 下载OpenJDK 11...
echo 下载地址：https://github.com/adoptium/temurin11-binaries/releases/latest
echo.

REM 下载JDK
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.19%2B7/OpenJDK11U-jdk_x64_windows_hotspot_11.0.19_7.msi' -OutFile 'openjdk11.msi'}"

if exist "openjdk11.msi" (
    echo ✅ 下载完成：openjdk11.msi
) else (
    echo ❌ 下载失败
    echo 请手动下载：
    echo https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.19+7/OpenJDK11U-jdk_x64_windows_hotspot_11.0.19_7.msi
    pause
    exit /b 1
)

echo.
echo [4/4] 安装Java JDK...
echo 安装程序将自动启动，请按默认设置安装...
echo.

REM 安装MSI
start /wait msiexec /i "openjdk11.msi" /quiet /norestart

echo.
echo 等待安装完成...
timeout /t 10 /nobreak >nul

echo.
echo [5/5] 验证安装...
java -version
if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo 🎉 Java JDK 安装成功！
    echo ========================================
    echo.
    echo 现在可以继续安装AutoGLM悬浮窗应用：
    echo.
    echo cd android_overlay_app
    echo build_and_install.bat
    echo.
) else (
    echo.
    echo ❌ Java安装可能失败
    echo 请检查安装过程，或手动安装JDK
    echo 下载地址：https://adoptium.net/
    echo.
)

echo 按任意键返回...
pause >nul
