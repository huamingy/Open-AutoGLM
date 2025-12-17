@echo off
chcp 65001 >nul
echo ========================================
echo AutoGLM 悬浮窗应用安装脚本
echo ========================================
echo.

echo [1/5] 检查系统要求...
echo.

:: 检查Java
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Java 未找到！
    echo.
    echo 启动Java环境设置向导...
    echo.
    call quick_java_setup.bat
    echo.
    echo 如果已设置Java环境，请重启命令提示符后重新运行此脚本。
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Java 已安装
)

:: 检查Android SDK
echo.
echo [1/5] 检查Android SDK...
if not exist "local.properties" (
    echo 未找到local.properties文件，启动Android SDK设置向导...
    echo.
    call setup_sdk.bat
    if not exist "local.properties" (
        echo ❌ Android SDK设置失败
        pause
        exit /b 1
    )
)

:: 验证SDK配置
echo 验证Android SDK配置...
if exist "local.properties" (
    echo ✅ local.properties存在
    type local.properties
) else (
    echo ❌ local.properties不存在
    pause
    exit /b 1
)
) else (
    echo ✅ Java 已安装
    java -version
)

:: 检查ADB
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ADB 未安装！
    echo 请下载 Android SDK Platform Tools：
    echo https://developer.android.com/studio/releases/platform-tools
    echo 并将解压目录添加到 PATH 环境变量
    echo.
    pause
    exit /b 1
) else (
    echo ✅ ADB 已安装
)

:: 检查设备连接
echo.
echo [2/5] 检查设备连接...
adb devices > temp_devices.txt
findstr /C:"device" temp_devices.txt >nul
if %errorlevel% neq 0 (
    echo ❌ 未找到连接的Android设备！
    echo 请：
    echo 1. 连接Android设备
    echo 2. 启用USB调试
    echo 3. 允许USB调试授权
    echo.
    del temp_devices.txt
    pause
    exit /b 1
) else (
    echo ✅ 设备已连接
)
del temp_devices.txt

echo.
echo [3/5] 构建APK...

:: 查找现有APK文件
if exist "app\build\outputs\apk\debug\app-debug.apk" (
    set APK_PATH=app\build\outputs\apk\debug\app-debug.apk
    echo ✅ 找到现有APK: %APK_PATH%
    goto :found_apk
) else if exist "build\outputs\apk\debug\app-debug.apk" (
    set APK_PATH=build\outputs\apk\debug\app-debug.apk
    echo ✅ 找到现有APK: %APK_PATH%
    goto :found_apk
) else if exist "*.apk" (
    for %%f in (*.apk) do (
        set APK_PATH=%%f
        echo ✅ 找到现有APK: %%f
        goto :found_apk
    )
)

:: 没有找到APK，开始构建
echo 未找到现有APK，开始构建新的APK...
echo.

if exist "gradlew.bat" (
    echo.
    echo [3/5] 检查许可证状态...
    if exist "C:\Users\Administrator\AppData\Local\Android\Sdk\licenses\android-sdk-license" (
        echo ✅ Android SDK许可证已存在，跳过接受步骤
    ) else (
        echo ⚠️  未找到许可证文件，尝试接受许可证...
        call accept_licenses.bat
        if %errorlevel% neq 0 (
            echo ⚠️  许可证接受可能有问题，但继续构建...
        )
    )

    echo.
    echo [3/5] 构建APK...
    echo 使用Gradle Wrapper构建项目...
    call gradlew.bat clean build
    if %errorlevel% neq 0 (
        echo ❌ Gradle构建失败！
        echo 请检查Java版本和网络连接
        pause
        exit /b 1
    )
) else (
    echo ❌ 未找到Gradle Wrapper！
    echo 请确保所有文件都已正确下载
    pause
    exit /b 1
)

:: 再次查找APK
if exist "app\build\outputs\apk\debug\app-debug.apk" (
    set APK_PATH=app\build\outputs\apk\debug\app-debug.apk
) else if exist "build\outputs\apk\debug\app-debug.apk" (
    set APK_PATH=build\outputs\apk\debug\app-debug.apk
) else (
    echo ❌ 构建完成但未找到APK文件！
    echo 请检查构建日志
    pause
    exit /b 1
)

echo ✅ APK构建成功: %APK_PATH%

:found_apk
echo.
echo [4/5] 安装应用到设备...
echo 正在安装: %APK_PATH%

adb install -r "%APK_PATH%"
if %errorlevel% neq 0 (
    echo ❌ 应用安装失败！
    echo 请检查设备连接和USB调试权限
    pause
    exit /b 1
) else (
    echo ✅ 应用安装成功！
)

echo.
echo [5/5] 启动应用...
adb shell am start -n com.autoglm.overlay/.MainActivity
if %errorlevel% neq 0 (
    echo ❌ 应用启动失败！
    pause
    exit /b 1
) else (
    echo ✅ 应用启动成功！
)

echo.
echo ========================================
echo 🎉 安装完成！
echo ========================================
echo.
echo 📱 请在手机上完成以下设置：
echo.
echo 1. 设置 → 无障碍 → AutoGLM Overlay → 开启
echo 2. 设置 → 应用 → AutoGLM Overlay → 显示在其他应用上层 → 允许
echo.
echo 🧪 测试悬浮窗：
echo adb shell am broadcast -a com.autoglm.overlay.UPDATE --es title "测试" --es content "悬浮窗工作正常！" --es status "运行中"
echo.
echo 🚀 启动AI助手：
echo python ws.py
echo 浏览器访问: http://localhost:8001
echo.
pause
