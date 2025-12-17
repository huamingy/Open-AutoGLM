# 🚀 AutoGLM 悬浮窗应用 - 完整安装指南

## 📱 效果预览

安装完成后，您将在手机屏幕上看到这样的悬浮窗：

```
┌─────────────────────────────────┐
│  ⚡ 执行中                       │
│                                 │
│  步骤 2                         │
│  点击位置(500, 800)             │
│                                 │
│         [⏹️ 终止任务]            │
└─────────────────────────────────┘
```

## 🎯 安装步骤（选择一个）

### 方法1：自动安装（推荐 - 最简单）

```bash
# 1. 确保Android设备已连接并启用USB调试
adb devices  # 应该显示您的设备

# 2. 运行自动安装脚本
cd android_overlay_app

# Windows:
build_and_install.bat

# Linux/Mac:
chmod +x build_and_install.sh
./build_and_install.sh
```

**这个脚本会自动完成所有步骤！**

### 方法2：手动安装

#### 2.1 构建APK

**选项A：使用Android Studio**
1. 下载 [Android Studio](https://developer.android.com/studio)
2. 安装并启动
3. 选择 "Open" → 选择 `android_overlay_app` 文件夹
4. 等待同步完成
5. Build → Build APK(s)
6. 找到APK：`app/build/outputs/apk/debug/app-debug.apk`

**选项B：使用命令行**
```bash
# 安装Gradle（如果没有）
choco install gradle  # Windows
# 或下载：https://gradle.org/releases/

# 构建APK
cd android_overlay_app
gradle build
```

#### 2.2 安装到手机

```bash
# 安装APK
adb install -r app/build/outputs/apk/debug/app-debug.apk

# 启动应用
adb shell am start -n com.autoglm.overlay/.MainActivity
```

### 方法3：预编译APK（如果可用）

如果项目提供了预编译的APK：

```bash
# 下载APK（假设存在）
wget https://example.com/autoglm-overlay.apk

# 安装
adb install autoglm-overlay.apk
adb shell am start -n com.autoglm.overlay/.MainActivity
```

## ⚙️ 手机权限设置

### 必须设置：

1. **无障碍服务**
   - 设置 → 无障碍 → AutoGLM Overlay → 开启
   - 这是悬浮窗工作的关键权限

2. **显示在其他应用上层**
   - 设置 → 应用 → AutoGLM Overlay → 显示在其他应用上层 → 允许
   - 允许悬浮窗显示在其他应用之上

### 可选设置：

3. **电池优化**
   - 设置 → 应用 → AutoGLM Overlay → 电池 → 不受限制
   - 防止系统杀死后台服务

## 🧪 测试安装

### 快速测试

```bash
# 运行测试脚本
cd android_overlay_app
test_overlay.bat  # Windows
# 或 ./test_overlay.sh  # Linux/Mac
```

这个脚本会发送测试广播，您应该在手机屏幕上看到悬浮窗出现、变化并消失。

### 手动测试

```bash
# 显示悬浮窗
adb shell am broadcast -a com.autoglm.overlay.UPDATE \
  --es title "测试" \
  --es content "悬浮窗工作正常！" \
  --es status "运行中"

# 隐藏悬浮窗
adb shell am broadcast -a com.autoglm.overlay.HIDE
```

## 🚀 与AI助手集成

1. **启动WebSocket服务器**
   ```bash
   python ws.py
   ```

2. **打开浏览器**
   - 访问：http://localhost:8001
   - 启用可视化反馈

3. **执行任务**
   - 输入："打开微信给张三发消息"
   - 点击执行
   - 观察手机屏幕上的悬浮窗！

## 🔧 故障排除

### 问题：悬浮窗不显示

**检查步骤：**
1. 确认无障碍服务已开启
2. 确认"显示在其他应用上层"权限已开启
3. 重启应用：`adb shell am start -n com.autoglm.overlay/.MainActivity`
4. 检查ADB广播：`adb shell am broadcast -a com.autoglm.overlay.UPDATE --es title "测试"`

### 问题：广播命令无效

**检查步骤：**
1. 确认应用正在运行
2. 确认广播action名称正确
3. 查看Android日志：`adb logcat | grep autoglm`

### 问题：应用安装失败

**检查步骤：**
1. 确认USB调试已开启
2. 允许USB调试授权
3. 更换USB端口或数据线
4. 确认APK文件完整

### 问题：构建APK失败

**检查步骤：**
1. 确认Java JDK 8+ 已安装
2. 确认Android SDK 已安装
3. 检查Gradle版本
4. 在Android Studio中检查错误信息

## 📋 系统要求

### 必须：
- ✅ Android 5.0+ (API 21+)
- ✅ Java JDK 8+
- ✅ Android SDK (ADB)

### 推荐：
- ✅ Android Studio (用于开发)
- ✅ Gradle 7.0+

## 🎉 成功标志

✅ **安装成功后您应该看到：**
- APK安装成功无错误
- 应用启动无崩溃
- 权限设置成功
- 测试广播后手机屏幕显示悬浮窗
- 与AI助手集成时实时显示状态

## 📞 获取帮助

如果遇到问题，请：
1. 检查上述故障排除步骤
2. 查看Android设备日志：`adb logcat`
3. 确认所有权限已正确设置
4. 尝试重启设备和重新安装

---

**享受AutoGLM的强大功能吧！🤖📱✨**
