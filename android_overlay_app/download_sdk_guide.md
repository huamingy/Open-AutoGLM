# 🚀 Android SDK 下载安装完整指南

## 📋 目录
- [方法1：Android Studio（推荐）](#方法1android-studio推荐)
- [方法2：独立SDK工具](#方法2独立sdk工具)
- [方法3：命令行安装](#方法3命令行安装)
- [验证安装](#验证安装)
- [故障排除](#故障排除)

---

## 方法1：Android Studio（推荐）

### 📥 下载
1. 访问官网：https://developer.android.com/studio
2. 点击 **"Download Android Studio"**
3. 选择 **Windows版本**，下载 `.exe` 安装包

### 🛠️ 安装步骤

#### 步骤1：运行安装程序
```bash
# 双击下载的 android-studio-xxx.exe
# 按照向导安装
```

#### 步骤2：启动Android Studio
- 首次启动会显示设置向导
- 选择 **"Standard"** 安装类型
- 等待组件下载完成

#### 步骤3：验证安装
```bash
# 检查SDK位置
# Android Studio -> File -> Settings -> Appearance & Behavior -> System Settings -> Android SDK

# 通常位置：
# C:\Users\[用户名]\AppData\Local\Android\Sdk
```

### ✅ 优势
- ✅ 一站式解决方案
- ✅ 自动配置环境变量
- ✅ 包含所有开发工具
- ✅ 图形化界面友好

---

## 方法2：独立SDK工具

### 📥 下载Platform Tools
1. 访问：https://developer.android.com/studio/releases/platform-tools
2. 下载 **SDK Platform-Tools for Windows**
3. 解压到自定义目录（如 `F:\development\AndroidSDK`）

### 📥 下载完整SDK
1. 访问：https://developer.android.com/studio/releases
2. 找到 **"Command line tools only"**
3. 下载 `commandlinetools-win-xxx.zip`
4. 解压到目录

### 🛠️ 配置SDK

#### 创建目录结构
```bash
# 假设解压到 F:\development\AndroidSDK
mkdir F:\development\AndroidSDK
cd F:\development\AndroidSDK

# 解压commandlinetools到此目录
# 结构应该是：
# F:\development\AndroidSDK\
#   ├── cmdline-tools\
#   │   └── latest\
#   │       ├── bin\
#   │       ├── lib\
#   │       └── source.properties
#   └── platform-tools\
#       ├── adb.exe
#       └── ...
```

#### 安装SDK组件
```bash
# 进入cmdline-tools目录
cd F:\development\AndroidSDK\cmdline-tools\latest\bin

# 安装基本组件（需要Java）
sdkmanager.bat "platform-tools" "platforms;android-33" "build-tools;33.0.2"

# 接受许可证
sdkmanager.bat --licenses
```

#### 设置环境变量
```bash
# 添加到系统PATH：
# F:\development\AndroidSDK\platform-tools
# F:\development\AndroidSDK\cmdline-tools\latest\bin

# 创建ANDROID_SDK_ROOT环境变量：
# ANDROID_SDK_ROOT=F:\development\AndroidSDK
```

### ✅ 优势
- ✅ 轻量级安装
- ✅ 自定义安装位置
- ✅ 只安装需要的组件

---

## 方法3：命令行安装

### 使用Chocolatey（Windows包管理器）
```bash
# 安装Chocolatey（如果没有）
# powershell: Set-ExecutionPolicy Bypass -Scope Process; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# 安装Android SDK
choco install android-sdk
```

### 使用SDKMAN（跨平台）
```bash
# Linux/Mac
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install android
```

---

## 验证安装

### 🧪 测试ADB
```bash
adb version
# 应该显示版本信息
```

### 🧪 测试SDK
```bash
# 检查SDK位置
echo %ANDROID_SDK_ROOT%

# 列出已安装组件
sdkmanager.bat --list_installed
```

### 🧪 连接设备
```bash
adb devices
# 应该显示连接的设备
```

---

## 故障排除

### 问题：Java未找到
```
解决方案：
1. 安装JDK 8/11/17
2. 设置JAVA_HOME环境变量
3. 参考：android_overlay_app\check_java.bat
```

### 问题：SDK组件下载失败
```
解决方案：
1. 检查网络连接
2. 配置代理（如果需要）
3. 手动下载组件包
```

### 问题：环境变量不生效
```
解决方案：
1. 重启命令提示符
2. 重启计算机
3. 检查变量值是否正确
```

### 问题：ADB设备未授权
```
解决方案：
1. 手机上允许USB调试
2. 选择"允许"USB调试授权
3. 更换USB端口或数据线
```

---

## 📋 系统要求

- **操作系统**：Windows 7/8/10/11 (64位)
- **内存**：至少4GB RAM
- **存储空间**：至少2GB可用空间
- **Java**：JDK 8/11/17

## 🎯 推荐配置

| 组件 | 版本 | 用途 |
|------|------|------|
| Android API | 33 | 应用开发API |
| Build Tools | 33.0.2 | 编译工具 |
| Platform Tools | 最新 | ADB等工具 |

---

## 🚀 下一步

安装完成后：

1. **设置SDK路径**：
   ```bash
   cd android_overlay_app
   notepad local.properties
   # 添加：sdk.dir=F:\\development\\AndroidSDK
   ```

2. **构建悬浮窗应用**：
   ```bash
   build_and_install.bat
   ```

3. **享受功能**！🎉📱

---

**有任何安装问题，请告诉我具体错误信息！** 💪

