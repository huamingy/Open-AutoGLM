package com.autoglm.overlay;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.Settings;
import android.widget.Toast;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

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

        // 关闭Activity
        finish();
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

    private void createOverlay() {
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);

        // 悬浮窗布局参数
        layoutParams = new WindowManager.LayoutParams();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            layoutParams.type = WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY;
        } else {
            layoutParams.type = WindowManager.LayoutParams.TYPE_PHONE;
        }

        layoutParams.format = PixelFormat.RGBA_8888;
        layoutParams.gravity = Gravity.TOP | Gravity.CENTER_HORIZONTAL;
        layoutParams.flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE |
                           WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL |
                           WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN;
        layoutParams.width = WindowManager.LayoutParams.MATCH_PARENT;
        layoutParams.height = WindowManager.LayoutParams.WRAP_CONTENT;
        layoutParams.x = 0;
        layoutParams.y = 100; // 距离顶部100px

        // 加载悬浮窗布局
        LayoutInflater inflater = LayoutInflater.from(this);
        overlayView = inflater.inflate(R.layout.overlay_layout, null);

        // 获取UI组件
        statusText = overlayView.findViewById(R.id.status_text);
        contentText = overlayView.findViewById(R.id.content_text);
        terminateButton = overlayView.findViewById(R.id.terminate_button);

        // 设置终止按钮点击事件
        terminateButton.setOnClickListener(v -> {
            // 发送终止广播
            Intent intent = new Intent(ACTION_TERMINATE);
            sendBroadcast(intent);

            // 显示终止反馈
            Toast.makeText(MainActivity.this, "任务终止请求已发送", Toast.LENGTH_SHORT).show();
        });

        // 添加悬浮窗到屏幕
        windowManager.addView(overlayView, layoutParams);

        // 初始隐藏悬浮窗
        overlayView.setVisibility(View.GONE);
    }

    private void registerBroadcastReceiver() {
        BroadcastReceiver receiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String action = intent.getAction();

                if (ACTION_UPDATE_OVERLAY.equals(action)) {
                    String title = intent.getStringExtra("title");
                    String content = intent.getStringExtra("content");
                    String status = intent.getStringExtra("status");

                    updateOverlay(title, content, status);
                } else if (ACTION_HIDE_OVERLAY.equals(action)) {
                    hideOverlay();
                }
            }
        };

        IntentFilter filter = new IntentFilter();
        filter.addAction(ACTION_UPDATE_OVERLAY);
        filter.addAction(ACTION_HIDE_OVERLAY);
        registerReceiver(receiver, filter);
    }

    private void updateOverlay(String title, String content, String status) {
        runOnUiThread(() -> {
            if (statusText != null && contentText != null && terminateButton != null) {
                // 设置状态和图标
                String statusWithIcon = getStatusWithIcon(status);
                statusText.setText(statusWithIcon);

                // 设置标题和内容
                contentText.setText(title + "\n" + content);

                // 显示悬浮窗
                overlayView.setVisibility(View.VISIBLE);
            }
        });
    }

    private void hideOverlay() {
        runOnUiThread(() -> {
            if (overlayView != null) {
                overlayView.setVisibility(View.GONE);
            }
        });
    }

    private String getStatusWithIcon(String status) {
        switch (status) {
            case "运行中": return "⏳ 运行中";
            case "思考中": return "🤔 思考中";
            case "执行中": return "⚡ 执行中";
            case "完成": return "✅ 完成";
            case "错误": return "❌ 错误";
            default: return "⏳ " + status;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (windowManager != null && overlayView != null) {
            windowManager.removeView(overlayView);
        }
    }
}
