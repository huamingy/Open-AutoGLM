@echo off
echo ========================================
echo Java JDK 简单安装脚本
echo ========================================
echo.
echo 这个脚本将尝试多种方式安装Java JDK
echo.

echo [1/3] 尝试使用 winget 安装...
winget --version >nul 2>&1
if %errorlevel% == 0 (
    echo 发现 winget，正在安装 OpenJDK...
    winget install EclipseAdoptium.Temurin.11.JDK
    goto :verify
) else (
    echo winget 未找到，尝试其他方法...
)

echo.
echo [2/3] 尝试使用 Chocolatey 安装...
choco --version >nul 2>&1
if %errorlevel% == 0 (
    echo 发现 Chocolatey，正在安装 OpenJDK...
    choco install openjdk11 -y
    goto :verify
) else (
    echo Chocolatey 未找到
)

echo.
echo [3/3] 下载独立JDK安装包...
echo.
echo 将打开浏览器下载页面，请下载并安装 JDK 11
echo 下载地址：https://adoptium.net/temurin/releases/
echo.
echo 安装步骤：
echo 1. 选择 Windows x64
echo 2. 选择 JDK 11 (LTS)
echo 3. 下载 .msi 文件
echo 4. 运行安装
echo.
start https://adoptium.net/temurin/releases/
echo.
echo 下载完成后，请重新运行此脚本验证安装
echo 或者运行 android_overlay_app\build_and_install.bat
echo.
pause
exit /b 1

:verify
echo.
echo [验证] 检查Java安装...
java -version
if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo 🎉 Java JDK 安装成功！
    echo ========================================
    echo.
    echo 现在可以安装AutoGLM悬浮窗应用：
    echo.
    echo cd android_overlay_app
    echo build_and_install.bat
    echo.
) else (
    echo.
    echo ❌ Java安装失败
    echo 请手动安装JDK：https://adoptium.net/
    echo.
)
pause
