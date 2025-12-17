# 🚨 WebSocket连接故障排除指南

## 问题现象

安卓应用显示 "WebSocket连接失败" 或一直显示 "WebSocket未连接"

## 🔍 诊断步骤

### 步骤1: 检查服务器状态

```bash
# 在服务器上运行
python ws.py
```

**预期结果**: 看到服务器启动信息，显示端口8002正在监听

### 步骤2: 检查网络连通性

```bash
# 在服务器上运行
simple_diagnose.bat
```

或手动检查：

```bash
# 1. 检查端口监听
netstat -ano | findstr :8002

# 2. 测试本地连接
curl http://127.0.0.1:8002/

# 3. 测试网络连接
ping 192.168.2.12
curl http://192.168.2.12:8002/
```

### 步骤3: 检查安卓设备

```bash
# 1. 确认手机和服务器在同一网络
ipconfig  # 查看服务器IP
# 在手机WiFi设置中确认连接的网络

# 2. 测试手机网络
# 在手机浏览器中访问: http://192.168.2.12:8002
```

## 🛠️ 常见解决方案

### 问题1: 服务器未启动

**现象**: 端口8002没有监听

**解决**:
```bash
cd /path/to/project
python ws.py
```

### 问题2: 防火墙阻止

**现象**: 端口可以本地访问，但远程无法访问

**解决**:
- Windows防火墙: 允许端口8002入站连接
- 路由器设置: 端口转发8002到服务器IP
- 公司网络: 联系IT管理员开放端口

### 问题3: IP地址错误

**现象**: 服务器运行正常，但连接192.168.2.12失败

**解决**:
- 确认服务器实际IP地址: `ipconfig`
- 更新安卓应用中的服务器地址
- 检查是否连接到正确的WiFi网络

### 问题4: 网络隔离

**现象**: 手机和服务器在不同网络段

**解决**:
- 确保手机连接到与服务器相同的WiFi
- 检查是否存在访客网络或隔离设置
- 尝试使用手机热点连接服务器

### 问题5: WebView兼容性

**现象**: 其他网络测试正常，但WebSocket仍然失败

**解决**:
- 更新安卓应用到最新版本
- 检查WebView组件是否为最新
- 在Chrome浏览器中测试WebSocket连接

## 🔧 高级诊断

### 检查WebSocket握手

```bash
# 使用curl测试WebSocket升级
curl -I -N -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" -H "Sec-WebSocket-Version: 13" http://192.168.2.12:8002/ws
```

**预期响应**:
```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
```

### 查看详细日志

```bash
# 服务器端日志
python ws.py 2>&1 | tee server.log

# 安卓端日志 (需要开发者选项)
adb logcat | grep -i websocket
```

### 网络抓包分析

使用Wireshark或tcpdump分析网络流量：

```bash
# Linux/Mac
tcpdump -i any port 8002 -w websocket_capture.pcap

# Windows (需要WinDump)
windump -i 1 port 8002 -w websocket_capture.pcap
```

## 📋 完整检查清单

- [ ] 服务器运行正常 (`python ws.py`)
- [ ] 端口8002正在监听 (`netstat -ano`)
- [ ] 本地HTTP访问正常 (`curl http://127.0.0.1:8002/`)
- [ ] 网络HTTP访问正常 (`curl http://192.168.2.12:8002/`)
- [ ] 防火墙允许端口8002
- [ ] 手机连接正确WiFi网络
- [ ] 安卓应用有网络权限
- [ ] WebView组件为最新版本

## 🚀 快速修复

如果遇到连接问题，按以下顺序操作：

### 1. 重启服务
```bash
# 停止现有服务
Ctrl+C

# 重启服务
python ws.py
```

### 2. 检查网络
```bash
# 运行诊断脚本
simple_diagnose.bat
```

### 3. 验证连接
```bash
# 在手机浏览器测试
http://192.168.2.12:8002
```

### 4. 重置应用
```bash
# 重新安装应用
adb install -r android_overlay_app-release-signed.apk

# 重启应用
adb shell am force-stop com.autoglm.overlay
adb shell am start -n com.autoglm.overlay/.MainActivity
```

## 📞 获取帮助

如果上述方法都无法解决问题：

1. **收集诊断信息**:
   - 服务器完整日志
   - 网络测试结果
   - 安卓设备信息

2. **提交问题**:
   - 详细描述问题现象
   - 提供诊断步骤结果
   - 说明网络环境配置

3. **联系支持**:
   - 检查项目GitHub Issues
   - 提供完整的错误信息和环境描述

---

## 🎯 预防措施

### 服务器部署
- 使用固定IP地址或域名
- 配置防火墙规则
- 设置自动启动服务
- 监控服务状态

### 网络配置
- 使用稳定的WiFi网络
- 避免网络切换
- 检查DNS解析
- 确认端口可用性

### 应用维护
- 保持应用更新
- 定期检查权限
- 清理应用缓存
- 重启设备测试

**记住**: 大多数WebSocket连接问题都是网络配置或服务器状态问题，通过系统性的诊断和修复，通常都能解决。 💪
