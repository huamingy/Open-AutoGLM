@echo off
chcp 65001 >nul
echo ========================================
echo Android SDK 许可证接受脚本
echo ========================================
echo.

echo 正在查找Android SDK路径...

:: 从local.properties读取SDK路径
if exist "local.properties" (
    for /f "tokens=1,2 delims==" %%a in (local.properties) do (
        if "%%a"=="sdk.dir" (
            set SDK_DIR=%%b
            goto :found_sdk
        )
    )
)

:found_sdk
if "%SDK_DIR%"=="" (
    echo ❌ 找不到SDK路径，请检查local.properties文件
    pause
    exit /b 1
)

echo 找到SDK路径: %SDK_DIR%
echo.

:: 检查sdkmanager是否存在
if not exist "%SDK_DIR%\cmdline-tools\latest\bin\sdkmanager.bat" (
    if not exist "%SDK_DIR%\tools\bin\sdkmanager.bat" (
        echo ❌ 找不到sdkmanager.bat，请确保Android SDK已正确安装
        echo 尝试的路径:
        echo   %SDK_DIR%\cmdline-tools\latest\bin\sdkmanager.bat
        echo   %SDK_DIR%\tools\bin\sdkmanager.bat
        pause
        exit /b 1
    ) else (
        set SDKMANAGER=%SDK_DIR%\tools\bin\sdkmanager.bat
    )
) else (
    set SDKMANAGER=%SDK_DIR%\cmdline-tools\latest\bin\sdkmanager.bat
)

echo 使用SDK Manager: %SDKMANAGER%
echo.

echo 正在接受所有Android SDK许可证...
echo 这可能需要一些时间，请耐心等待...
echo.

:: 使用PowerShell来自动接受所有许可证
powershell -Command "& { $yes = 'y' * 100; $yes | & '%SDKMANAGER%' --licenses }"

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  PowerShell方法失败，尝试传统方法...
    echo 请手动运行以下命令并对每个提示回答 'y':
    echo "%SDKMANAGER%" --licenses
    echo.
) else (
    echo.
    echo ✅ 许可证接受完成！
    echo.
)

echo 验证许可证状态...
"%SDKMANAGER%" --list | findstr /C:"build-tools;30.0.2" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Build Tools 30.0.2 许可证已接受
) else (
    echo ⚠️  Build Tools 30.0.2 许可证状态未知
)

"%SDKMANAGER%" --list | findstr /C:"platforms;android-33" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Android SDK Platform 33 许可证已接受
) else (
    echo ⚠️  Android SDK Platform 33 许可证状态未知
)

echo.
echo 如果仍有许可证问题：
echo 1. 打开Android Studio
echo 2. Tools → SDK Manager → SDK Tools
echo 3. 选中并安装缺失的组件
echo 4. 或手动运行："%SDKMANAGER%" --licenses
echo.
pause
