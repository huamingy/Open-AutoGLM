@echo off
echo WebSocket快速测试
echo ===================

echo 测试连接到: ws://192.168.2.12:8002/ws
echo.

echo 1. 检查端口...
netstat -ano | findstr :8002 | findstr LISTENING >nul
if %errorlevel% equ 0 (
    echo 服务器端口正在监听
) else (
    echo 服务器端口未监听
)

echo.
echo 2. 测试HTTP连接...
curl -s --max-time 3 http://192.168.2.12:8002/ >nul 2>&1
if %errorlevel% equ 0 (
    echo HTTP连接正常
) else (
    echo HTTP连接失败
)

echo.
echo 3. 建议检查:
echo - 确保服务器运行: python ws.py
echo - 确保手机和电脑在同一网络
echo - 检查防火墙设置
echo - 确认IP地址正确

pause
