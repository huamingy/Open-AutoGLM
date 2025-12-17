@echo off
chcp 65001 >nul
echo ========================================
echo Java JDK 安装向导
echo ========================================
echo.

echo 由于您的系统没有安装Java，我们将引导您完成安装。
echo.
echo 步骤：
echo 1. 打开浏览器下载JDK
echo 2. 安装JDK
echo 3. 验证安装
echo 4. 继续安装悬浮窗应用
echo.

echo 按任意键打开浏览器下载页面...
pause >nul

start https://adoptium.net/temurin/releases/?version=11

echo.
echo ========================================
echo 安装步骤：
echo ========================================
echo.
echo 1. 在打开的网页中选择：
echo    - Operating System: Windows
echo    - Architecture: x64
echo    - Version: 11 (LTS)
echo.
echo 2. 点击 "Latest LTS Release" 按钮
echo.
echo 3. 下载 OpenJDK11U-jdk_x64_windows_hotspot_*.msi 文件
echo.
echo 4. 双击下载的 .msi 文件安装
echo    - 按默认设置安装即可
echo.
echo 5. 安装完成后，关闭所有命令提示符窗口
echo.
echo 6. 重新打开命令提示符，运行：
echo    cd android_overlay_app
echo    build_and_install.bat
echo.

echo 安装完成后，请重新运行 build_and_install.bat
echo.
pause
