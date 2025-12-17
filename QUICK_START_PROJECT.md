# 🚀 AutoGLM 项目快速启动指南

## 📋 项目概述

这是一个基于AutoGLM的手机AI助手项目，包含：
- 🐍 **Python后端** - AI推理和设备控制
- 🌐 **Web界面** - 用户操作界面
- 📱 **Android悬浮窗** - 手机端实时状态显示

## 🎯 最快启动方式

### 方法1：一键启动（推荐）

```bash
# Windows
start_project.bat

# Linux/Mac
python ws.py
```

### 方法2：手动启动

#### 步骤1：启动WebSocket服务器
```bash
# 确保Python环境正常
python --version  # 应该显示Python 3.x

# 安装依赖（如果还没有）
pip install -r requirements.txt

# 启动服务器
python ws.py
```

#### 步骤2：打开Web界面
服务器启动后：
1. 打开浏览器
2. 访问：`http://localhost:8001`
3. 享受AI助手功能！

## 📱 可选：启用手机悬浮窗

### 构建Android应用
```bash
cd android_overlay_app

# 设置Android SDK路径（如果还没有）
setup_sdk.bat

# 构建并安装
build_and_install.bat
```

### 使用悬浮窗功能
1. 启动悬浮窗应用
2. 在Web界面执行任务
3. 手机屏幕会显示AI思考过程！

## 🔧 系统要求

| 组件 | 要求 | 说明 |
|------|------|------|
| Python | 3.8+ | 后端运行环境 |
| Android SDK | 任意版本 | 构建悬浮窗应用（可选） |
| Java JDK | 8/11/17 | 构建Android应用（可选） |
| ADB | 已安装 | 与Android设备通信 |

## 🌟 功能特色

### 🤖 AI能力
- 📱 手机自动化操作
- 🧠 视觉理解界面
- 🎯 智能任务规划
- ⏹️ 实时任务控制
- 🔓 智能屏幕解锁
- 💡 自动保持亮屏
- 📸 优化的屏幕截图
- 🔄 自动错误重试
- 🔄 执行中自动解锁

### 🎨 界面体验
- 🌐 现代化Web界面
- 📊 实时状态显示
- 📱 手机悬浮窗反馈
- ⌨️ 便捷操作控制

### 🔧 开发友好
- 🐍 Python后端API
- 📡 WebSocket实时通信
- 📱 Android应用源码
- 🛠️ 完整的构建工具

## 🎮 使用示例

### 基本操作
1. **启动服务器**：`python ws.py`
2. **打开界面**：浏览器访问 `http://localhost:8001`
3. **连接设备**：确保Android设备通过USB连接
4. **发送指令**：输入"打开微信给张三发消息"
5. **观看执行**：实时查看AI操作过程

### 高级功能
- **悬浮窗显示**：手机屏幕显示AI状态
- **实时控制**：随时终止任务
- **多任务支持**：连续执行多个任务

## 🔍 故障排除

### 问题：服务器启动失败
```bash
# 检查Python
python --version

# 检查端口占用
netstat -ano | findstr :8001

# 尝试其他端口
python ws.py  # 修改代码中的端口
```

### 问题：设备连接失败
```bash
# 检查ADB
adb devices

# 重启ADB服务
adb kill-server
adb start-server

# 检查USB调试
# 手机：设置 → 开发者选项 → USB调试
```

### 问题：悬浮窗构建失败
```bash
# 检查Java
java -version

# 检查Android SDK
setup_sdk.bat

# 重新构建
cd android_overlay_app
build_and_install.bat
```

## 📚 项目结构

```
Open-AutoGLM/
├── main.py                 # Python主程序
├── ws.py                   # WebSocket服务器
├── index.html             # Web界面
├── phone_agent/           # AI代理核心
├── android_overlay_app/   # Android悬浮窗应用
├── examples/              # 示例代码
└── requirements.txt       # Python依赖
```

## 🎯 立即开始

**最快体验**：
```bash
# 1. 启动服务器
python ws.py

# 2. 打开浏览器
# http://localhost:8002

# 3. 开始使用AI助手！
```

---

**享受AutoGLM带来的智能体验！** 🤖📱✨

有任何问题，查看项目文档或寻求帮助！ 💪
