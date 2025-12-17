@echo off
echo ========================================
echo 构建Android悬浮窗应用
echo ========================================
echo.

cd android_overlay_app

echo 清理旧构建...
call gradlew.bat clean

echo.
echo 构建APK...
call gradlew.bat build

if %errorlevel% equ 0 (
    echo.
    echo ✅ 构建成功！
    echo APK文件位置: android_overlay_app\app\build\outputs\apk\debug\app-debug.apk
) else (
    echo.
    echo ❌ 构建失败！
    echo 请检查错误信息
)

echo.
pause
