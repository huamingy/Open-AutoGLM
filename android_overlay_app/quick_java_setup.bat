@echo off
chcp 65001 >nul
echo ========================================
echo Java JDK 快速设置向导
echo ========================================
echo.

echo 这个脚本将帮助您快速设置Java环境。
echo.
echo 请选择：
echo [1] 检查当前Java环境
echo [2] 下载并安装Java JDK 11
echo [3] 设置环境变量
echo [4] 退出
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 检查Java环境...
    call check_java.bat
    goto :end
)

if "%choice%"=="2" (
    echo.
    echo 启动Java下载安装...
    call download_java.bat
    goto :end
)

if "%choice%"=="3" (
    echo.
    echo 设置环境变量...
    echo.
    echo 请手动设置环境变量：
    echo 1. 右键"此电脑" → "属性" → "高级系统设置"
    echo 2. 点击"环境变量"
    echo 3. 在"系统变量"中找到"Path"，点击"编辑"
    echo 4. 添加Java bin目录，例如：
    echo    C:\Program Files\Eclipse Adoptium\jdk-11\bin
    echo.
    echo 设置完成后，请重启命令提示符。
    echo.
    pause
    goto :end
)

if "%choice%"=="4" (
    echo.
    echo 退出脚本。
    goto :end
)

echo 无效选择，请重新运行脚本。
:end
