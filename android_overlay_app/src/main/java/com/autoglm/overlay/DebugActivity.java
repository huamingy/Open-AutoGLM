package com.autoglm.overlay;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.LinearLayout;
import android.widget.Toast;
import android.view.View;
import android.view.ViewGroup;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class DebugActivity extends Activity {

    private TextView debugLog;
    private ScrollView scrollView;
    private EditText serverInput;
    private EditText portInput;
    private Button testConnectionBtn;
    private Button testWebSocketBtn;
    private Button clearLogBtn;
    private Button backBtn;

    private ExecutorService executor = Executors.newSingleThreadExecutor();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 创建主布局
        LinearLayout mainLayout = new LinearLayout(this);
        mainLayout.setOrientation(LinearLayout.VERTICAL);
        mainLayout.setPadding(20, 20, 20, 20);

        // 标题
        TextView titleView = new TextView(this);
        titleView.setText("🔧 WebSocket调试工具");
        titleView.setTextSize(20);
        titleView.setPadding(0, 0, 0, 20);
        mainLayout.addView(titleView);

        // 服务器配置区域
        LinearLayout configLayout = new LinearLayout(this);
        configLayout.setOrientation(LinearLayout.HORIZONTAL);
        configLayout.setPadding(0, 0, 0, 20);

        // 服务器地址输入
        serverInput = new EditText(this);
        serverInput.setHint("服务器地址");
        serverInput.setText("192.168.2.12");
        serverInput.setLayoutParams(new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1));
        configLayout.addView(serverInput);

        // 端口输入
        portInput = new EditText(this);
        portInput.setHint("端口");
        portInput.setText("8002");
        portInput.setLayoutParams(new LinearLayout.LayoutParams(150, ViewGroup.LayoutParams.WRAP_CONTENT));
        configLayout.addView(portInput);

        mainLayout.addView(configLayout);

        // 按钮区域
        LinearLayout buttonLayout = new LinearLayout(this);
        buttonLayout.setOrientation(LinearLayout.HORIZONTAL);
        buttonLayout.setPadding(0, 0, 0, 20);

        // 测试连接按钮
        testConnectionBtn = new Button(this);
        testConnectionBtn.setText("🌐 测试连接");
        testConnectionBtn.setOnClickListener(v -> testConnection());
        buttonLayout.addView(testConnectionBtn);

        // 测试WebSocket按钮
        testWebSocketBtn = new Button(this);
        testWebSocketBtn.setText("🔌 测试WebSocket");
        testWebSocketBtn.setOnClickListener(v -> testWebSocket());
        buttonLayout.addView(testWebSocketBtn);

        mainLayout.addView(buttonLayout);

        // 控制按钮区域
        LinearLayout controlLayout = new LinearLayout(this);
        controlLayout.setOrientation(LinearLayout.HORIZONTAL);
        controlLayout.setPadding(0, 0, 0, 20);

        // 清除日志按钮
        clearLogBtn = new Button(this);
        clearLogBtn.setText("🗑️ 清除日志");
        clearLogBtn.setOnClickListener(v -> clearLog());
        controlLayout.addView(clearLogBtn);

        // 返回按钮
        backBtn = new Button(this);
        backBtn.setText("⬅️ 返回");
        backBtn.setOnClickListener(v -> finish());
        controlLayout.addView(backBtn);

        mainLayout.addView(controlLayout);

        // 日志显示区域
        scrollView = new ScrollView(this);
        debugLog = new TextView(this);
        debugLog.setText("调试日志:\n");
        debugLog.setPadding(10, 10, 10, 10);
        debugLog.setBackgroundColor(0xFFEEEEEE);
        scrollView.addView(debugLog);
        scrollView.setLayoutParams(new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            0,
            1.0f
        ));

        mainLayout.addView(scrollView);

        setContentView(mainLayout);

        // 初始化日志
        log("调试工具已启动");
        log("默认服务器: 192.168.2.12:8002");
    }

    private void testConnection() {
        String server = serverInput.getText().toString().trim();
        String port = portInput.getText().toString().trim();

        if (server.isEmpty() || port.isEmpty()) {
            Toast.makeText(this, "请输入服务器地址和端口", Toast.LENGTH_SHORT).show();
            return;
        }

        log("开始测试HTTP连接: " + server + ":" + port);

        executor.execute(() -> {
            try {
                URL url = new URL("http://" + server + ":" + port + "/");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                conn.setRequestMethod("GET");

                int responseCode = conn.getResponseCode();
                String responseMessage = conn.getResponseMessage();

                runOnUiThread(() -> {
                    log("HTTP连接结果: " + responseCode + " " + responseMessage);
                    if (responseCode == 200 || responseCode == 404) {
                        log("✅ HTTP连接成功 - 服务器正在运行");
                    } else {
                        log("❌ HTTP连接失败 - 响应码: " + responseCode);
                    }
                });

                conn.disconnect();

            } catch (IOException e) {
                runOnUiThread(() -> {
                    log("❌ HTTP连接失败: " + e.getMessage());
                    log("可能的原因:");
                    log("  - 服务器未启动");
                    log("  - 端口被防火墙阻止");
                    log("  - 网络连接问题");
                });
            }
        });
    }

    private void testWebSocket() {
        String server = serverInput.getText().toString().trim();
        String port = portInput.getText().toString().trim();

        if (server.isEmpty() || port.isEmpty()) {
            Toast.makeText(this, "请输入服务器地址和端口", Toast.LENGTH_SHORT).show();
            return;
        }

        log("开始测试WebSocket连接: ws://" + server + ":" + port + "/ws");

        executor.execute(() -> {
            try {
                java.net.Socket socket = new java.net.Socket();
                socket.connect(new java.net.InetSocketAddress(server, Integer.parseInt(port)), 5000);

                runOnUiThread(() -> {
                    log("✅ TCP连接成功 - 端口" + port + "可以访问");
                    log("💡 WebSocket服务可能正常运行");
                    log("🔍 在浏览器中测试: http://" + server + ":" + port);
                });

                socket.close();

            } catch (Exception e) {
                runOnUiThread(() -> {
                    log("❌ WebSocket连接测试失败: " + e.getMessage());
                    log("可能的原因:");
                    log("  - WebSocket服务器未启动");
                    log("  - 端口被防火墙阻止");
                    log("  - 服务器不在该端口运行");
                });
            }
        });
    }

    private void clearLog() {
        debugLog.setText("调试日志:\n");
        log("日志已清除");
    }

    private void log(String message) {
        runOnUiThread(() -> {
            String currentText = debugLog.getText().toString();
            String timestamp = java.text.SimpleDateFormat.getTimeInstance().format(new java.util.Date());
            debugLog.setText(currentText + "[" + timestamp + "] " + message + "\n");

            // 自动滚动到底部
            scrollView.post(() -> scrollView.fullScroll(View.FOCUS_DOWN));
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (executor != null && !executor.isShutdown()) {
            executor.shutdown();
        }
    }
}
