@echo off
echo ========================================
echo Java环境检查脚本
echo ========================================
echo.

echo [1/3] 检查Java安装...
java -version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Java 已安装
    java -version
) else (
    echo ❌ Java 未找到
    echo.
    echo 请检查：
    echo 1. 是否已安装JDK
    echo 2. 环境变量PATH是否包含Java bin目录
    echo 3. 尝试重启命令提示符
    echo.
    goto :java_not_found
)

echo.
echo [2/3] 检查Javac编译器...
javac -version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Javac 已安装
    javac -version
) else (
    echo ❌ Javac 未找到
    echo.
    echo JDK可能不完整，请重新安装JDK（不是JRE）
)

echo.
echo [3/3] 检查环境变量...
echo JAVA_HOME: %JAVA_HOME%
echo.

if "%JAVA_HOME%" == "" (
    echo ⚠️  JAVA_HOME 未设置
    echo 这可能导致一些工具无法正常工作
) else (
    echo ✅ JAVA_HOME 已设置
)

echo.
echo ========================================
echo Java环境检查完成
echo ========================================
echo.
if exist "%JAVA_HOME%\bin\java.exe" (
    echo ✅ Java路径验证通过
) else (
    echo ⚠️  Java路径可能有问题
)

goto :end

:java_not_found
echo.
echo ========================================
echo Java安装指南
echo ========================================
echo.
echo 方法1 - 在线安装（推荐）：
echo 1. 访问：https://adoptium.net/temurin/releases/
echo 2. 选择：Windows x64, JDK 11 (LTS)
echo 3. 下载并安装
echo.
echo 方法2 - 使用Chocolatey（如果已安装）：
echo choco install openjdk11
echo.
echo 方法3 - 手动设置PATH：
echo 1. 找到Java安装目录（通常在 Program Files）
echo 2. 右键"此电脑" → "属性" → "高级系统设置"
echo 3. 点击"环境变量"
echo 4. 在"系统变量"中找到"Path"，点击"编辑"
echo 5. 添加Java bin目录，如：C:\Program Files\Eclipse Adoptium\jdk-11\bin
echo.
echo 安装完成后，重启命令提示符并重新运行此脚本。

:end
echo.
pause
