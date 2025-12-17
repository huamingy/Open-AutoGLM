@echo off
chcp 65001 >nul
echo ========================================
echo 快速接受Android SDK许可证
echo ========================================
echo.

echo 查找SDK路径...

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
    echo ❌ 找不到SDK路径
    echo 请检查local.properties文件
    pause
    exit /b 1
)

echo SDK路径: %SDK_DIR%
echo.

:: 查找sdkmanager
if exist "%SDK_DIR%\cmdline-tools\latest\bin\sdkmanager.bat" (
    set SDKMANAGER="%SDK_DIR%\cmdline-tools\latest\bin\sdkmanager.bat"
) else if exist "%SDK_DIR%\tools\bin\sdkmanager.bat" (
    set SDKMANAGER="%SDK_DIR%\tools\bin\sdkmanager.bat"
) else (
    echo ❌ 找不到sdkmanager.bat
    echo 请确保Android SDK已正确安装
    pause
    exit /b 1
)

echo 正在接受Android SDK许可证...
echo.

:: 方法1：使用yes命令自动接受
echo y | %SDKMANAGER% --licenses

if %errorlevel% equ 0 (
    echo.
    echo ✅ 许可证接受完成！
) else (
    echo.
    echo ⚠️  自动接受可能失败
    echo 请手动运行以下命令：
    echo %SDKMANAGER% --licenses
    echo 然后对每个提示回答 'y'
)

echo.
pause
