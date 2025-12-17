# 🚀 Java JDK 安装指南

## 📋 为什么需要Java？

AutoGLM悬浮窗应用需要Java JDK来构建Android APK文件。Android开发使用Gradle构建工具，而Gradle需要Java运行环境。

## 🎯 推荐安装方式

### 方法1：Adoptium Temurin (推荐 - 免费开源)

#### Windows 安装步骤：

1. **访问下载页面**：
   打开浏览器访问：https://adoptium.net/

2. **选择版本**：
   - Platform: Windows
   - Architecture: x64
   - Version: 11 (LTS) 或 17 (LTS)

3. **下载并安装**：
   - 点击 "Latest LTS Release"
   - 下载 `.msi` 安装包
   - 双击运行安装包，按默认设置安装

4. **验证安装**：
   ```cmd
   java -version
   ```
   应该看到类似输出：
   ```
   openjdk version "11.0.19" 2023-04-18
   OpenJDK Runtime Environment Temurin-11.0.19+7 (build 11.0.19+7)
   OpenJDK 64-Bit Server VM Temurin-11.0.19+7 (build 11.0.19+7, mixed mode)
   ```

#### 设置环境变量（如果自动设置失败）：

1. 右键"此电脑" → "属性" → "高级系统设置"
2. 点击"环境变量"
3. 在"系统变量"中找到`Path`，点击"编辑"
4. 添加：`C:\Program Files\Eclipse Adoptium\jdk-11.0.19.7-hotspot\bin`
5. 点击"确定"保存

### 方法2：使用Chocolatey (Windows包管理器)

如果您已安装Chocolatey：

```cmd
# 安装OpenJDK 11
choco install openjdk11

# 验证安装
java -version
```

### 方法3：Oracle JDK (需要注册)

1. 访问：https://www.oracle.com/java/technologies/javase-downloads.html
2. 下载 JDK 11 或 17
3. 安装并设置环境变量

## 🔧 验证安装

打开命令提示符，运行：

```cmd
# 检查Java版本
java -version

# 检查javac编译器
javac -version

# 检查Java环境变量
echo %JAVA_HOME%
```

## 🚀 继续安装悬浮窗应用

Java安装完成后，继续运行：

```cmd
cd android_overlay_app
build_and_install.bat
```

## 🔍 故障排除

### 问题：'java' 不是内部或外部命令

**解决方案**：
1. 检查安装是否完成
2. 重新启动命令提示符
3. 手动设置环境变量：
   - 找到JDK安装路径（通常在 `C:\Program Files\Eclipse Adoptium\`）
   - 添加到系统PATH环境变量

### 问题：版本不兼容

**解决方案**：
- 确保安装的是JDK 8, 11, 或 17
- 避免安装JDK 18+（可能与某些构建工具不兼容）

### 问题：安装失败

**解决方案**：
- 以管理员身份运行安装程序
- 关闭所有Java相关的程序
- 清理临时文件后重试

## 📞 获取帮助

如果仍然遇到问题：

1. 确认您的Windows版本（64位）
2. 尝试重新启动计算机
3. 查看详细错误信息
4. 访问Adoptium社区：https://adoptium.net/support.html

---

**安装完成后，Java将不仅用于AutoGLM，还可以用于其他Android开发项目！** 🎉
