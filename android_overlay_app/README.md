# AutoGLM Android 悬浮窗应用

这个Android应用在手机屏幕上显示真正的悬浮窗，展示AI助手的工作状态和进度。

## 功能特性

- 🪟 **真正的悬浮窗**：在手机屏幕顶部显示半透明悬浮窗
- 📊 **实时状态显示**：显示AI思考过程和当前操作
- ⏹️ **终止按钮**：悬浮窗内直接终止任务
- 🔄 **动态更新**：实时更新显示内容
- 🎨 **美观界面**：绿色边框，黑色半透明背景

## 🚀 快速开始

### 1. 一键安装（推荐）

```bash
# Windows
cd android_overlay_app
build_and_install.bat

# Linux/Mac
cd android_overlay_app
./build_and_install.sh
```

### 2. 手动安装

#### 步骤1：构建APK

**方法A：使用Android Studio**
1. 下载 [Android Studio](https://developer.android.com/studio)
2. 打开 `android_overlay_app` 文件夹
3. Build → Build APK(s)
4. 找到生成的APK文件

**方法B：使用命令行**
```bash
cd android_overlay_app
gradle build
```

#### 步骤2：安装到手机

```bash
adb install app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n com.autoglm.overlay/.MainActivity
```

## 构建步骤

### 方法1：使用Android Studio

1. 打开Android Studio
2. 选择 "Open an existing Android Studio project"
3. 选择 `android_overlay_app` 文件夹
4. 等待Gradle同步完成
5. 点击 "Build" -> "Build Bundle(s)/APK(s)" -> "Build APK(s)"
6. APK文件将在 `app/build/outputs/apk/debug/app-debug.apk` 生成

### 方法2：命令行构建

```bash
# 确保有Gradle
cd android_overlay_app

# 如果有gradlew脚本
./gradlew build

# 或者使用系统Gradle
gradle build
```

## 安装到手机

### 自动安装脚本

```bash
cd android_overlay_app
chmod +x build_and_install.sh
./build_and_install.sh
```

### 手动安装

1. 将APK文件传输到手机：
```bash
adb push app/build/outputs/apk/debug/app-debug.apk /sdcard/
```

2. 在手机上安装APK：
```bash
adb shell pm install /sdcard/app-debug.apk
```

3. 启动应用：
```bash
adb shell am start -n com.autoglm.overlay/.MainActivity
```

## 权限设置

应用需要以下权限：

1. **显示在其他应用上层**：设置 -> 应用 -> AutoGLM Overlay -> 显示在其他应用上层
2. **开机自启**（可选）：设置 -> 应用 -> AutoGLM Overlay -> 自动启动

## 使用方法

1. **启动WebSocket服务器**：
```bash
python ws.py
```

2. **在浏览器中打开控制台**：
   - 访问 `http://localhost:8001`
   - 启用可视化反馈

3. **执行任务**：
   - 输入指令并点击执行
   - 手机屏幕会显示悬浮窗

4. **终止任务**：
   - 点击悬浮窗中的"⏹️ 终止任务"按钮
   - 或在Web界面点击终止按钮

## 悬浮窗界面

```
┌─────────────────────────┐
│  🤔 思考中                │
│                         │
│  步骤 2                  │
│  用户要求打开微信...      │
│                         │
│  [⏹️ 终止任务]            │
└─────────────────────────┘
```

## 广播接口

应用通过广播接收控制命令：

- **更新悬浮窗**：
  ```bash
  adb shell am broadcast -a com.autoglm.overlay.UPDATE \
    --es title "步骤 1" \
    --es content "正在思考..." \
    --es status "思考中"
  ```

- **隐藏悬浮窗**：
  ```bash
  adb shell am broadcast -a com.autoglm.overlay.HIDE
  ```

- **终止信号**：
  ```bash
  adb shell am broadcast -a com.autoglm.overlay.TERMINATE
  ```

## 故障排除

### 悬浮窗不显示
1. 检查应用是否有"显示在其他应用上层"权限
2. 重启应用
3. 检查ADB连接

### 广播不生效
1. 确保应用正在运行
2. 检查广播action名称是否正确
3. 查看Android日志：`adb logcat | grep autoglm`

### 应用崩溃
1. 检查Android版本兼容性
2. 查看详细日志：`adb logcat`

## 自定义

### 修改外观
- 编辑 `res/layout/overlay_layout.xml` 调整布局
- 编辑 `res/drawable/overlay_background.xml` 修改背景样式

### 添加功能
- 修改 `MainActivity.java` 添加新的广播处理
- 在 `overlay_layout.xml` 中添加UI组件

## 许可证

与主项目保持一致。
