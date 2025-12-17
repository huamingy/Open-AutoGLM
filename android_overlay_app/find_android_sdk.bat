@echo off
chcp 65001 >nul
echo ========================================
echo Android SDK 自动检测脚本
echo ========================================
echo.

echo [1/3] 检查ANDROID_SDK_ROOT环境变量...
if defined ANDROID_SDK_ROOT (
    echo ✅ ANDROID_SDK_ROOT: %ANDROID_SDK_ROOT%
    goto :create_local_properties
) else (
    echo ❌ ANDROID_SDK_ROOT 未设置
)

echo.
echo [2/3] 搜索常见Android SDK位置...

set "SDK_FOUND="

:: 检查常见位置
set "POSSIBLE_LOCATIONS=C:\Users\%USERNAME%\AppData\Local\Android\Sdk C:\Android\Sdk C:\Program Files\Android\Android Studio\Sdk C:\Users\%USERNAME%\Android\Sdk"

for %%i in (%POSSIBLE_LOCATIONS%) do (
    if exist "%%i\platform-tools\adb.exe" (
        echo ✅ 找到Android SDK: %%i
        set "SDK_FOUND=%%i"
        goto :found_sdk
    )
)

:: 检查PATH中的ADB
echo 检查PATH中的ADB...
where adb >nul 2>&1
if %errorlevel% == 0 (
    for /f "tokens=*" %%i in ('where adb') do (
        set "ADB_PATH=%%i"
        goto :parse_adb_path
    )
) else (
    echo ❌ 未在PATH中找到ADB
    goto :no_sdk_found
)

:parse_adb_path
:: 从ADB路径提取SDK路径
for %%i in ("%ADB_PATH%") do set "SDK_FROM_ADB=%%~dpi.."
if exist "%SDK_FROM_ADB%\platforms" (
    echo ✅ 从ADB路径推断SDK位置: %SDK_FROM_ADB%
    set "SDK_FOUND=%SDK_FROM_ADB%"
    goto :found_sdk
)

:no_sdk_found
echo.
echo ❌ 未找到Android SDK
echo.
echo 请手动安装Android SDK：
echo 1. 下载 Android Studio：https://developer.android.com/studio
echo 2. 安装时选择 "Android SDK"
echo 3. 或者单独下载 SDK：https://developer.android.com/studio/releases/platform-tools
echo.
echo 安装后重新运行此脚本。
echo.
pause
exit /b 1

:found_sdk
echo.
echo [3/3] 创建local.properties文件...

:create_local_properties
if not defined SDK_FOUND (
    echo ❌ 未找到SDK位置，请手动设置
    goto :manual_setup
)

:: 创建local.properties文件
echo # Android SDK location > local.properties
echo sdk.dir=%SDK_FOUND:\=\\% >> local.properties
echo.

if exist "local.properties" (
    echo ✅ local.properties 已创建
    echo 内容：
    type local.properties
) else (
    echo ❌ 创建local.properties失败
    goto :manual_setup
)

echo.
echo ========================================
echo 🎉 Android SDK 配置完成！
echo ========================================
echo.
echo 现在可以运行构建：
echo gradlew.bat clean build
echo.
pause
exit /b 0

:manual_setup
echo.
echo 手动设置local.properties：
echo 1. 找到您的Android SDK位置
echo 2. 编辑 local.properties 文件
echo 3. 添加：sdk.dir=C:\\path\\to\\your\\android\\sdk
echo.
echo 示例：
echo sdk.dir=C:\\Users\\Administrator\\AppData\\Local\\Android\\Sdk
echo.
pause
