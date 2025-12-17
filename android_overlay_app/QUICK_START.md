# ⚡ AutoGLM 悬浮窗 - 快速开始

## 🎯 3分钟搞定手机悬浮窗

### 0. 环境准备

脚本会自动检查并设置Java和Android SDK。如果遇到问题，请手动运行：

**Java环境检查**：
```bash
cd android_overlay_app
check_java.bat
```

**Android SDK设置**：
```bash
cd android_overlay_app
setup_sdk.bat
```

**环境要求**：
- ✅ Java JDK 8+ (自动检测)
- ✅ Android SDK (脚本会引导设置)
- ✅ ADB工具 (用于连接手机)

### 1. 一键安装悬浮窗应用

```bash
# Windows
cd android_overlay_app
build_and_install.bat

# Linux/Mac
cd android_overlay_app
chmod +x build_and_install.sh
./build_and_install.sh
```

**脚本会自动完成：**
- ✅ 检查Java和ADB
- ✅ 验证设备连接
- ✅ 查找APK文件
- ✅ 安装到手机
- ✅ 启动应用

### 2. 手机设置（2步）

1. **无障碍服务**：
   - 设置 → 无障碍 → AutoGLM Overlay → 开启

2. **悬浮窗权限**：
   - 设置 → 应用 → AutoGLM Overlay → 显示在其他应用上层 → 允许

### 3. 测试效果

```bash
# 测试悬浮窗
cd android_overlay_app

# Windows
test_overlay.bat

# Linux/Mac
chmod +x test_overlay.sh
./test_overlay.sh
```

### 4. 启动AI助手

```bash
# 启动服务器
python ws.py

# 浏览器访问
# http://localhost:8001

# 执行任务，享受悬浮窗效果！
```

## 📱 效果展示

安装完成后，您将看到：

```
┌─────────────────────────────────┐
│  🤔 思考中                       │
│                                 │
│  步骤 1                         │
│  正在分析屏幕内容...            │
│                                 │
│         [⏹️ 终止任务]            │
└─────────────────────────────────┘
```

## 🔧 系统要求

- ✅ Android 5.0+
- ✅ **Java JDK 8+** (支持JDK 8/11/17，用于构建APK)
- ✅ Android SDK (ADB)
- ✅ USB调试已开启

## 🚨 常见问题

### Q: 找不到APK文件？
**A:** 先构建APK：
```bash
cd android_overlay_app
gradle build
# 或在Android Studio中构建
```

### Q: 安装失败？
**A:** 检查：
- USB调试已开启
- 设备授权已允许
- 更换USB端口

### Q: 悬浮窗不显示？
**A:** 检查权限：
- 无障碍服务已开启
- 显示在其他应用上层已允许

## 📞 技术支持

如果遇到问题，请检查：
1. `adb devices` 显示设备
2. `java -version` 正常
3. 手机权限设置正确

---

**🎉 现在就开始享受AI悬浮窗体验吧！**
