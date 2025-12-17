# 🔧 安装卡住问题解决方案

## 🚨 如果安装卡住

### 快速解决方案

#### 方法1: 终止并强制安装 (推荐)
```bash
# 1. 按 Ctrl+C 中断当前安装
# 2. 运行强制安装脚本
force_install.bat
```

#### 方法2: 清理后重试
```bash
# 1. 按 Ctrl+C 中断当前安装
# 2. 清理ADB进程
kill_install.bat
# 3. 重新运行
quick_dev.bat
```

#### 方法3: 手动安装
```bash
# 1. 按 Ctrl+C 中断
# 2. 手动执行
adb uninstall com.autoglm.overlay
adb install -r build\outputs\apk\debug\android_overlay_app-debug.apk
```

## 🔍 常见原因

### 1. 权限授予卡住
**原因**: `-g` 参数在某些设备上会导致卡住
**解决**: 使用 `force_install.bat`，它先安装再授予权限

### 2. 设备无响应
**原因**: ADB连接不稳定或设备休眠
**解决**: 
- 运行 `kill_install.bat` 重启ADB
- 检查设备是否唤醒
- 重新连接设备

### 3. 存储空间不足
**原因**: 设备存储空间已满
**解决**: 
```bash
adb shell df /data
# 清理设备存储空间
```

### 4. 签名冲突
**原因**: 旧版本签名与新版本不匹配
**解决**: `force_install.bat` 会自动处理

## 🛠️ 工具说明

### force_install.bat
- ✅ 强制停止应用
- ✅ 完全卸载旧版本
- ✅ 清理应用数据
- ✅ 分步安装（避免卡住）
- ✅ 自动授予权限

### kill_install.bat
- ✅ 终止卡住的ADB进程
- ✅ 重启ADB服务
- ✅ 检查设备连接

## 💡 预防措施

### 开发时建议
1. **使用WiFi连接**: 更稳定，不易卡住
2. **保持设备唤醒**: 安装时不要锁屏
3. **定期清理**: 卸载旧版本再安装新版本
4. **使用force_install**: 如果经常卡住，直接用这个脚本

### 最佳实践
```bash
# 日常开发流程
1. quick_dev.bat          # 正常流程
2. 如果卡住 → force_install.bat  # 强制安装
3. 如果还不行 → kill_install.bat → force_install.bat  # 清理后强制安装
```

## 📋 检查清单

安装前检查：
- [ ] 设备已连接 (`adb devices`)
- [ ] 设备已唤醒（屏幕亮起）
- [ ] 存储空间充足
- [ ] 未知来源已开启
- [ ] ADB连接稳定

安装时注意：
- [ ] 不要锁屏
- [ ] 不要断开连接
- [ ] 如果超过30秒无响应，按 Ctrl+C 中断

安装后验证：
- [ ] 应用已安装 (`adb shell pm list packages | findstr autoglm`)
- [ ] 应用可以启动
- [ ] 权限已授予

## 🎯 快速命令参考

```bash
# 检查设备
adb devices

# 检查应用
adb shell pm list packages | findstr autoglm

# 强制安装
force_install.bat

# 清理重试
kill_install.bat

# 正常安装
quick_dev.bat
```
