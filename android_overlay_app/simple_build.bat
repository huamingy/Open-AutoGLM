@echo off
chcp 65001 >nul
echo ========================================
echo 简单Android应用构建脚本
echo ========================================
echo.

echo 检查Java...
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Java未找到！
    echo 请先安装Java JDK 8+
    pause
    exit /b 1
) else (
    echo ✅ Java已安装
)

echo.
echo 检查Android SDK许可证...
if exist "C:\Users\Administrator\AppData\Local\Android\Sdk\licenses\android-sdk-license" (
    echo ✅ 许可证已存在
) else (
    echo ❌ 未找到许可证
    echo 请先运行Android Studio并接受SDK许可证
    pause
    exit /b 1
)

echo.
echo 开始构建APK...
echo.

if exist "gradlew.bat" (
    echo 使用Gradle Wrapper构建...
    call gradlew.bat clean build --no-daemon
) else (
    echo ❌ 未找到gradlew.bat
    echo 请确保所有文件都已正确下载
    pause
    exit /b 1
)

if %errorlevel% equ 0 (
    echo.
    echo ✅ 构建成功！
    echo.

    :: 查找APK文件
    if exist "app\build\outputs\apk\debug\app-debug.apk" (
        echo APK文件位置: %cd%\app\build\outputs\apk\debug\app-debug.apk
        set APK_PATH=%cd%\app\build\outputs\apk\debug\app-debug.apk
        goto :install_apk
    )

    echo 查找APK文件...
    for /r %%f in (*.apk) do (
        echo 找到APK: %%f
        set APK_PATH=%%f
        goto :install_apk
    )

    echo ❌ 未找到APK文件
    goto :end

    :install_apk
    echo.
    echo 安装APK到设备...
    echo.

    :: 检查ADB
    adb version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ ADB未找到
        goto :end
    )

    :: 检查设备连接
    adb devices | findstr /C:"device" >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ 未找到连接的Android设备
        echo 请确保：
        echo 1. USB调试已开启
        echo 2. 设备已连接并授权
        goto :end
    )

    echo 安装APK...
    adb install -r "%APK_PATH%"
    if %errorlevel% equ 0 (
        echo ✅ APK安装成功！

        echo.
        echo 启动应用...
        adb shell am start -n com.autoglm.overlay/.MainActivity

        echo.
        echo 🎉 安装完成！
        echo.
        echo 请在手机上完成以下设置：
        echo 1. 设置 → 无障碍 → AutoGLM Overlay → 开启
        echo 2. 设置 → 应用 → AutoGLM Overlay → 显示在其他应用上层 → 允许
        echo.
        echo 然后就可以在AI助手执行任务时看到悬浮窗了！

    ) else (
        echo ❌ APK安装失败
        echo 请检查设备连接和USB调试设置
    )

) else (
    echo.
    echo ❌ 构建失败！
    echo 请检查错误信息
)

:end
echo.
pause
