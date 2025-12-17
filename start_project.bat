@echo off
echo ========================================
echo AutoGLM 项目启动脚本
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 未安装！
    echo 请安装Python 3.8+: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo ✅ Python 已安装
    python --version
)

echo.
echo [2/4] 安装Python依赖...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    ) else (
        echo ✅ 依赖安装成功
    )
) else (
    echo ⚠️  未找到requirements.txt，跳过依赖安装
)

echo.
echo [3/4] 启动WebSocket服务器...
echo 服务器将在 http://localhost:8001 启动
echo 按 Ctrl+C 停止服务器
echo.
echo 启动中...

python ws.py

echo.
echo [4/4] 服务器已停止
echo 如需重新启动，请运行: python ws.py
pause
