@echo off
chcp 65001 >nul
echo ========================================
echo 🛠️  AutoGLM 开发工具箱
echo ========================================
echo.
echo 快速开发工具一览:
echo.
echo 🚀 快速开发部署
echo    quick_dev.bat          - 一键构建、安装、启动
echo.
echo 🔍 诊断和检查
echo    quick_diagnose.bat     - 全面诊断设备和应用状态
echo    dev_log.bat           - 实时查看应用日志
echo.
echo 📦 安装和权限
echo    manual_install.bat     - 手动安装（多种选项）
echo    setup_permissions.bat  - 权限设置和授予
echo.
echo 📱 设备连接
echo    connect_device.bat     - 无线ADB连接设备
echo    restart_adb.bat       - 重启ADB服务
echo.
echo 📚 文档和配置
echo    README_DEV.md         - 详细开发指南
echo    dev_config.properties - 开发配置参数
echo.
echo ========================================
echo 🎯 推荐使用流程:
echo ========================================
echo.
echo 1. 📱 连接设备: connect_device.bat
echo 2. 🔍 诊断检查: quick_diagnose.bat
echo 3. 🚀 开发部署: quick_dev.bat
echo 4. 📊 查看日志: dev_log.bat (新终端)
echo.
echo 💡 遇到问题时:
echo • 运行 quick_diagnose.bat 诊断
echo • 使用 manual_install.bat 手动安装
echo • 运行 setup_permissions.bat 设置权限
echo.
echo ========================================
pause
