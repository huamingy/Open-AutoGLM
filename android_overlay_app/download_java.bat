@echo off
chcp 65001 >nul
echo ========================================
echo 自动下载并安装 Java JDK
echo ========================================
echo.

echo 这个脚本将下载并安装OpenJDK 11
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ 需要管理员权限才能安装软件
    echo 请右键点击此文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)

echo ✅ 管理员权限确认
echo.

REM 创建临时目录
if not exist "%TEMP%\autoglm_java" mkdir "%TEMP%\autoglm_java"
cd "%TEMP%\autoglm_java"

echo 下载OpenJDK 11...
echo.

REM 使用PowerShell下载
powershell -Command "& {try { Invoke-WebRequest -Uri 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21%%2B9/OpenJDK11U-jdk_x64_windows_hotspot_11.0.21_9.msi' -OutFile 'openjdk11.msi' -UseBasicParsing; Write-Host '下载完成' } catch { Write-Host '下载失败，请手动下载'; exit 1 }}"

if not exist "openjdk11.msi" (
    echo ❌ 下载失败
    echo.
    echo 请手动下载：
    echo https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21%2B9/OpenJDK11U-jdk_x64_windows_hotspot_11.0.21_9.msi
    echo.
    echo 下载完成后，将文件重命名为 openjdk11.msi 并放在此目录：
    echo %TEMP%\autoglm_java\
    echo.
    echo 然后重新运行此脚本。
    echo.
    pause
    exit /b 1
)

echo ✅ 下载成功
echo.

echo 正在安装Java JDK...
echo 安装程序将自动运行，请按默认设置安装...
echo.

REM 静默安装
msiexec /i "openjdk11.msi" /quiet /norestart ADDLOCAL=ALL

echo 等待安装完成...
timeout /t 15 /nobreak >nul

echo.
echo 验证安装...
java -version 2>nul
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
    echo 按任意键打开悬浮窗应用安装脚本...
    pause >nul
    
    REM 返回到android_overlay_app目录并运行安装脚本
    cd /d "E:\Project\autoGlm\Open-AutoGLM\android_overlay_app"
    call build_and_install.bat
) else (
    echo ❌ Java安装可能失败
    echo.
    echo 请尝试：
    echo 1. 手动运行安装程序：%TEMP%\autoglm_java\openjdk11.msi
    echo 2. 或访问 https://adoptium.net/ 手动下载安装
    echo.
    pause
)
