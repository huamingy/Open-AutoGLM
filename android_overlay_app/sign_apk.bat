@echo off
chcp 65001 >nul
echo ========================================
echo 🔐 AutoGLM Overlay APK签名脚本
echo ========================================
echo.

set "UNSIGNED_APK=build\outputs\apk\release\android_overlay_app-release-unsigned.apk"
set "SIGNED_APK=build\outputs\apk\release\android_overlay_app-release-signed.apk"
set "KEYSTORE=autoglm.keystore"
set "KEY_ALIAS=autoglm_key"

echo 🔍 检查APK文件...
if not exist "%UNSIGNED_APK%" (
    echo ❌ 未找到未签名的APK文件: %UNSIGNED_APK%
    echo 请先运行: gradlew.bat assembleRelease
    pause
    exit /b 1
)
echo ✅ APK文件存在

echo.
echo 🔑 检查签名密钥库...
if not exist "%KEYSTORE%" (
    echo 📝 创建新的签名密钥库...
    echo.
    echo 密钥库信息:
    echo - 密钥库文件: %KEYSTORE%
    echo - 密钥别名: %KEY_ALIAS%
    echo - 有效期: 10000天
    echo.

    echo 正在创建密钥库，请稍候...
    echo y| keytool -genkeypair -v -keystore "%KEYSTORE%" -alias "%KEY_ALIAS%" -keyalg RSA -keysize 2048 -validity 10000 -storepass autoglm123 -keypass autoglm123 -storetype PKCS12 -dname "CN=AutoGLM, OU=AI Assistant, O=AutoGLM Project, L=Unknown, ST=Unknown, C=CN"
    if %errorlevel% neq 0 (
        echo ❌ 密钥库创建失败
        pause
        exit /b 1
    )
    echo ✅ 密钥库创建成功
) else (
    echo ✅ 密钥库已存在
)

echo.
echo ✍️ 对APK进行签名...
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 -keystore "%KEYSTORE%" -storepass autoglm123 -keypass autoglm123 "%UNSIGNED_APK%" "%KEY_ALIAS%"
if %errorlevel% neq 0 (
    echo ❌ APK签名失败
    echo.
    echo 可能的原因:
    echo 1. jarsigner工具未找到
    echo 2. APK文件损坏
    echo 3. 密钥库文件损坏
    pause
    exit /b 1
)
echo ✅ APK签名成功

echo.
echo 📋 验证签名...
jarsigner -verify -verbose -certs "%UNSIGNED_APK%"
if %errorlevel% neq 0 (
    echo ❌ 签名验证失败
    pause
    exit /b 1
)
echo ✅ 签名验证成功

echo.
echo 📦 创建签名后的APK副本...
copy "%UNSIGNED_APK%" "%SIGNED_APK%" >nul
if %errorlevel% neq 0 (
    echo ❌ 文件复制失败
    pause
    exit /b 1
)
echo ✅ 签名APK创建成功

echo.
echo ========================================
echo 🎉 APK签名完成！
echo ========================================
echo.
echo 📁 文件位置:
echo 签名后的APK: %SIGNED_APK%
echo 密钥库文件: %KEYSTORE%
echo.
echo 💡 提示:
echo - 签名后的APK可以直接安装到Android设备
echo - 请妥善保管密钥库文件(%KEYSTORE%)
echo - 密钥库密码请牢记，用于后续更新签名
echo.
echo 🚀 现在可以安装签名后的APK了！
echo.
pause
