@echo off
echo ========================================
echo AutoGLM 悬浮窗测试脚本
echo ========================================
echo.

echo [1/3] 检查ADB连接...
adb devices > temp_devices.txt
findstr /C:"device" temp_devices.txt >nul
if %errorlevel% neq 0 (
    echo ❌ 未找到连接的Android设备！
    del temp_devices.txt
    pause
    exit /b 1
)
del temp_devices.txt
echo ✅ 设备已连接

echo.
echo [2/3] 测试悬浮窗显示...
echo.

echo 发送"思考中"状态...
adb shell am broadcast -a com.autoglm.overlay.UPDATE --es title "步骤 1" --es content "正在分析用户需求..." --es status "思考中"
timeout /t 3 /nobreak >nul

echo 发送"执行中"状态...
adb shell am broadcast -a com.autoglm.overlay.UPDATE --es title "步骤 2" --es content "点击位置(300, 400)" --es status "执行中"
timeout /t 3 /nobreak >nul

echo 发送"完成"状态...
adb shell am broadcast -a com.autoglm.overlay.UPDATE --es title "任务完成" --es content "已成功打开应用！" --es status "完成"
timeout /t 3 /nobreak >nul

echo.
echo [3/3] 隐藏悬浮窗...
adb shell am broadcast -a com.autoglm.overlay.HIDE

echo.
echo ========================================
echo ✅ 测试完成！
echo ========================================
echo.
echo 如果您看到了悬浮窗在手机屏幕上显示和变化，
echo 说明悬浮窗功能工作正常！
echo.
echo 现在可以启动AI助手进行完整测试：
echo python ws.py
echo.
pause
