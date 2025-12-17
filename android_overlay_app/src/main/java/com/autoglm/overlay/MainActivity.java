package com.autoglm.overlay;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 开发模式检测和提示
        if (BuildConfig.DEVELOPER_MODE) {
            Toast.makeText(this, "🔧 开发模式已启用 - 日志更详细", Toast.LENGTH_LONG).show();
        }

        // 创建主界面布局
        LinearLayout mainLayout = new LinearLayout(this);
        mainLayout.setOrientation(LinearLayout.VERTICAL);
        mainLayout.setPadding(50, 50, 50, 50);

        // 标题
        TextView titleView = new TextView(this);
        titleView.setText("🤖 AutoGLM AI助手");
        titleView.setTextSize(24);
        titleView.setPadding(0, 0, 0, 40);
        titleView.setGravity(android.view.Gravity.CENTER);
        mainLayout.addView(titleView);

        // Web界面按钮
        Button webButton = new Button(this);
        webButton.setText("🌐 打开Web界面");
        webButton.setTextSize(16);
        webButton.setPadding(20, 20, 20, 20);
        webButton.setOnClickListener(v -> openWebInterface());
        mainLayout.addView(webButton);

        // 直接启动按钮
        Button directButton = new Button(this);
        directButton.setText("🚀 直接启动服务");
        directButton.setTextSize(16);
        directButton.setPadding(20, 20, 20, 20);
        directButton.setOnClickListener(v -> startDirectService());
        mainLayout.addView(directButton);

        // 调试工具按钮
        Button debugButton = new Button(this);
        debugButton.setText("🔧 调试工具");
        debugButton.setTextSize(16);
        debugButton.setPadding(20, 20, 20, 20);
        debugButton.setOnClickListener(v -> openDebugTool());
        mainLayout.addView(debugButton);

        // 设置按钮
        Button settingsButton = new Button(this);
        settingsButton.setText("⚙️ 无障碍设置");
        settingsButton.setTextSize(16);
        settingsButton.setPadding(20, 20, 20, 20);
        settingsButton.setOnClickListener(v -> openAccessibilitySettings());
        mainLayout.addView(settingsButton);

        setContentView(mainLayout);
    }

    private void openWebInterface() {
        // 检查无障碍服务权限
        if (!isAccessibilityServiceEnabled()) {
            Toast.makeText(this, "请先启用无障碍服务", Toast.LENGTH_LONG).show();
            openAccessibilitySettings();
            return;
        }

        // 启动无障碍服务
        Intent serviceIntent = new Intent(this, OverlayAccessibilityService.class);
        startService(serviceIntent);

        // 打开Web界面
        Intent webIntent = new Intent(this, WebViewActivity.class);
        startActivity(webIntent);
    }

    private void startDirectService() {
        // 检查无障碍服务权限
        if (!isAccessibilityServiceEnabled()) {
            // 跳转到无障碍设置页面
            Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
            startActivity(intent);
            Toast.makeText(this, "请启用 AutoGLM Overlay 无障碍服务", Toast.LENGTH_LONG).show();
        } else {
            Toast.makeText(this, "无障碍服务已启用，悬浮窗功能可用", Toast.LENGTH_SHORT).show();
        }

        // 启动无障碍服务
        Intent serviceIntent = new Intent(this, OverlayAccessibilityService.class);
        startService(serviceIntent);

        // 显示提示信息
        Toast.makeText(this, "悬浮窗服务已启动，请使用外部WebSocket连接", Toast.LENGTH_LONG).show();

        // 关闭Activity
        finish();
    }

    private void openDebugTool() {
        Intent intent = new Intent(this, DebugActivity.class);
        startActivity(intent);
    }

    private void openAccessibilitySettings() {
        Intent intent = new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS);
        startActivity(intent);
    }

    private boolean isAccessibilityServiceEnabled() {
        String serviceId = getPackageName() + "/" + OverlayAccessibilityService.class.getName();
        int accessibilityEnabled = 0;
        try {
            accessibilityEnabled = android.provider.Settings.Secure.getInt(
                getContentResolver(),
                android.provider.Settings.Secure.ACCESSIBILITY_ENABLED);
        } catch (Exception e) {
            // Ignore
        }

        if (accessibilityEnabled == 1) {
            String settingValue = android.provider.Settings.Secure.getString(
                getContentResolver(),
                android.provider.Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES);
            if (settingValue != null) {
                return settingValue.contains(serviceId);
            }
        }

        return false;
    }
}
