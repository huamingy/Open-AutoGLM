package com.autoglm.overlay;

import android.accessibilityservice.AccessibilityService;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.PixelFormat;
import android.os.Build;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.view.accessibility.AccessibilityEvent;
import android.widget.Button;
import android.widget.TextView;

public class OverlayAccessibilityService extends AccessibilityService {

    private static final String ACTION_UPDATE_OVERLAY = "com.autoglm.overlay.UPDATE";
    private static final String ACTION_HIDE_OVERLAY = "com.autoglm.overlay.HIDE";
    private static final String ACTION_TERMINATE = "com.autoglm.overlay.TERMINATE";

    private WindowManager windowManager;
    private View overlayView;
    private WindowManager.LayoutParams layoutParams;

    private TextView statusText;
    private TextView contentText;
    private Button terminateButton;

    @Override
    public void onCreate() {
        super.onCreate();

        // 创建悬浮窗
        createOverlay();

        // 注册广播接收器
        registerBroadcastReceiver();
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent event) {
        // 处理辅助功能事件（可选）
    }

    @Override
    public void onInterrupt() {
        // 服务中断处理
        hideOverlay();
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        hideOverlay();
    }

    private void createOverlay() {
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);

        // 悬浮窗布局参数
        layoutParams = new WindowManager.LayoutParams();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            layoutParams.type = WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY;
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
        if (overlayView != null) {
            overlayView.post(() -> {
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
    }

    private void hideOverlay() {
        if (overlayView != null) {
            overlayView.post(() -> {
                overlayView.setVisibility(View.GONE);
            });
        }
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
}
