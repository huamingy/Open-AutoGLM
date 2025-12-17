@echo off
chcp 65001 >nul
echo ========================================
echo 🔍 简单网络连接诊断
echo ========================================
echo.

set "SERVER_IP=192.168.2.12"
set "SERVER_PORT=8002"

echo 📡 测试服务器: %SERVER_IP%:%SERVER_PORT%
echo.

echo 🔍 1. Ping测试...
ping -n 2 %SERVER_IP% >nul
if %errorlevel% equ 0 (
    echo ✅ Ping成功 - 网络连通正常
) else (
    echo ❌ Ping失败 - 网络连接问题
    echo 建议检查: 服务器是否开机，IP地址是否正确
)

echo.
echo 🔍 2. 端口测试...
powershell -Command "try { $tcp = New-Object System.Net.Sockets.TcpClient; $tcp.Connect('%SERVER_IP%', %SERVER_PORT%); echo '✅ 端口连接成功 - WebSocket服务可能正常'; $tcp.Close() } catch { echo '❌ 端口连接失败 - WebSocket服务未启动或防火墙阻止' }" 2>nul

echo.
echo 🔍 3. HTTP测试...
curl -s --max-time 5 -o nul -w "HTTP状态码: %%{http_code}\n" http://%SERVER_IP%:%SERVER_PORT%/ 2>nul
if %errorlevel% equ 0 (
    echo ✅ HTTP连接成功
) else (
    echo ❌ HTTP连接失败
    echo 建议检查: 服务器是否运行Web服务
)

echo.
echo 🔍 4. 本地网络信息...
echo.
echo 您的IP地址:
ipconfig | findstr /R /C:"IPv4 Address"

echo.
echo ========================================
echo 📋 故障排除建议
echo ========================================
echo.
echo 如果WebSocket连接失败，请按以下顺序检查:
echo.
echo 1️⃣ 📡 服务器状态:
echo    - 确认服务器 %SERVER_IP% 已开机并联网
echo    - 确认WebSocket服务器正在运行
echo.
echo 2️⃣ 🔧 服务器配置:
echo    - 确认服务器运行在端口 %SERVER_PORT%
echo    - 确认WebSocket路径为 /ws
echo    - 检查防火墙设置
echo.
echo 3️⃣ 🌐 网络配置:
echo    - 确认手机和服务器在同一WiFi网络
echo    - 检查是否有网络隔离
echo    - 尝试使用浏览器访问: http://%SERVER_IP%:%SERVER_PORT%
echo.
echo 4️⃣ 📱 手机设置:
echo    - 确认手机连接到正确的WiFi
echo    - 检查是否有代理设置
echo.
echo 5️⃣ 🔄 重启服务:
echo    - 在服务器上运行: python ws.py
echo    - 等待10秒让服务完全启动
echo.

pause
