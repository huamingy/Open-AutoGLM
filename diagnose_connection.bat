@echo off
chcp 65001 >nul
echo ========================================
echo 🔍 WebSocket连接诊断脚本
echo ========================================
echo.

set "SERVER_IP=192.168.2.12"
set "SERVER_PORT=8002"

echo 📡 检查服务器连接...
echo.

echo 🔍 1. 网络连通性测试...
ping -n 3 %SERVER_IP% >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 无法ping通服务器 %SERVER_IP%
    echo.
    echo 可能的原因:
    echo - 服务器未开机
    echo - 网络连接问题
    echo - 防火墙阻止ping
    echo - IP地址错误
    goto :network_failed
) else (
    echo ✅ 可以ping通服务器 %SERVER_IP%
)

echo.
echo 🔍 2. 端口连通性测试...
powershell -Command "Test-NetConnection -ComputerName %SERVER_IP% -Port %SERVER_PORT% -InformationLevel Quiet" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 端口 %SERVER_PORT% 不可访问
    echo.
    echo 可能的原因:
    echo - WebSocket服务器未启动
    echo - 防火墙阻止端口 %SERVER_PORT%
    echo - 服务器不在该端口运行
    goto :port_failed
) else (
    echo ✅ 端口 %SERVER_PORT% 可以访问
)

echo.
echo 🔍 3. WebSocket连接测试...
echo 尝试连接到: ws://%SERVER_IP%:%SERVER_PORT%/ws
echo.

powershell -Command "
try {
    $ws = New-Object System.Net.WebSockets.ClientWebSocket
    $cts = New-Object System.Threading.CancellationTokenSource
    $task = $ws.ConnectAsync('ws://%SERVER_IP%:%SERVER_PORT%/ws', $cts.Token)
    $timeout = $task.Wait(5000)
    if ($timeout -and $ws.State -eq 'Open') {
        Write-Host '✅ WebSocket连接成功'
        $ws.CloseAsync([System.Net.WebSockets.WebSocketCloseStatus]::NormalClosure, '', $cts.Token).Wait()
    } else {
        Write-Host '❌ WebSocket连接失败或超时'
        Write-Host '可能的原因:'
        Write-Host '- 服务器WebSocket服务未启动'
        Write-Host '- WebSocket路径不正确 (/ws)'
        Write-Host '- 服务器配置问题'
    }
} catch {
    Write-Host '❌ WebSocket连接异常:'
    Write-Host $_.Exception.Message
}
" 2>nul

echo.
echo 🔍 4. HTTP连接测试...
curl -s -o nul -w "%%{http_code}" http://%SERVER_IP%:%SERVER_PORT%/ >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ HTTP连接失败
    echo 可能的原因:
    echo - 服务器HTTP服务未启动
    echo - 端口配置错误
) else (
    echo ✅ HTTP连接正常
)

echo.
echo 🔍 5. 本地网络信息...
echo.
echo 当前IP地址:
ipconfig | findstr /R /C:"IPv4 Address"
echo.
echo 当前网络连接:
netstat -n | findstr :%SERVER_PORT% | findstr ESTABLISHED

echo.
echo ========================================
echo 📋 诊断建议
echo ========================================
echo.
echo 如果仍有连接问题，请检查:
echo.
echo 1. 📡 服务器状态:
echo    - 确认服务器 %SERVER_IP% 已开机并联网
echo    - 确认WebSocket服务器正在运行
echo.
echo 2. 🔧 服务器配置:
echo    - 确认服务器运行在端口 %SERVER_PORT%
echo    - 确认WebSocket路径为 /ws
echo    - 检查防火墙设置
echo.
echo 3. 🌐 网络配置:
echo    - 确认手机和服务器在同一网络
echo    - 检查是否有网络隔离或VPN
echo    - 尝试使用浏览器访问: http://%SERVER_IP%:%SERVER_PORT%
echo.
echo 4. 📱 手机设置:
echo    - 确认手机连接到正确的WiFi网络
echo    - 检查是否有代理设置
echo.
echo 5. 🔄 重启服务:
echo    - 在服务器上运行: python ws.py
echo    - 等待几秒钟让服务完全启动
echo.

goto :end

:network_failed
echo.
echo 💡 网络连接故障排除:
echo - 检查服务器IP地址是否正确
echo - 检查服务器是否开机
echo - 检查网络连接
echo - 尝试更换网络环境
goto :end

:port_failed
echo.
echo 💡 端口连接故障排除:
echo - 在服务器上确认WebSocket服务正在运行
echo - 检查防火墙是否阻止了端口 %SERVER_PORT%
echo - 确认服务器配置正确
echo - 尝试重启WebSocket服务
goto :end

:end
echo.
pause
