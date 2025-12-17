package com.autoglm.overlay;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class WebViewActivity extends Activity {

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 创建WebView
        webView = new WebView(this);
        setContentView(webView);

        // 配置WebView
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        webSettings.setAllowUniversalAccessFromFileURLs(true);
        webSettings.setAllowFileAccessFromFileURLs(true);

        // 调试模式配置
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
            WebView.setWebContentsDebuggingEnabled(true);
        }

        // 开发模式日志增强
        if (BuildConfig.DEVELOPER_MODE) {
            android.util.Log.d("AutoGLM-DEV", "WebView调试模式已启用");
        }

        // 添加JavaScript接口
        webView.addJavascriptInterface(new WebAppInterface(this), "AndroidInterface");

        // 设置WebView客户端
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                super.onReceivedError(view, errorCode, description, failingUrl);
                System.out.println("WebView Error: " + errorCode + " - " + description + " - " + failingUrl);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                System.out.println("WebView Page Finished: " + url);
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onConsoleMessage(android.webkit.ConsoleMessage consoleMessage) {
                android.util.Log.d("WebView", consoleMessage.message() + " -- From line "
                        + consoleMessage.lineNumber() + " of "
                        + consoleMessage.sourceId());
                System.out.println("WebView Console: " + consoleMessage.message());
                return true;
            }
        });

        // 加载HTML内容
        String htmlContent = getHtmlContent();
        webView.loadDataWithBaseURL("http://192.168.2.12:8002", htmlContent, "text/html", "UTF-8", null);
    }

    private String getHtmlContent() {
        return "<!DOCTYPE html>\n" +
                "<html lang=\"zh-CN\">\n" +
                "<head>\n" +
                "    <meta charset=\"UTF-8\">\n" +
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n" +
                "    <title>AutoGLM AI助手</title>\n" +
                "    <style>\n" +
                "        body {\n" +
                "            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\n" +
                "            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n" +
                "            margin: 0;\n" +
                "            padding: 20px;\n" +
                "            min-height: 100vh;\n" +
                "            color: #333;\n" +
                "        }\n" +
                "        .container {\n" +
                "            max-width: 800px;\n" +
                "            margin: 0 auto;\n" +
                "            background: rgba(255, 255, 255, 0.95);\n" +
                "            border-radius: 20px;\n" +
                "            padding: 30px;\n" +
                "            box-shadow: 0 20px 40px rgba(0,0,0,0.1);\n" +
                "        }\n" +
                "        h1 {\n" +
                "            text-align: center;\n" +
                "            color: #4a5568;\n" +
                "            margin-bottom: 30px;\n" +
                "            font-size: 2.5em;\n" +
                "            text-shadow: 0 2px 4px rgba(0,0,0,0.1);\n" +
                "        }\n" +
                "        .input-group {\n" +
                "            margin-bottom: 20px;\n" +
                "        }\n" +
                "        label {\n" +
                "            display: block;\n" +
                "            margin-bottom: 8px;\n" +
                "            font-weight: 600;\n" +
                "            color: #2d3748;\n" +
                "        }\n" +
                "        textarea {\n" +
                "            width: 100%;\n" +
                "            padding: 15px;\n" +
                "            border: 2px solid #e2e8f0;\n" +
                "            border-radius: 10px;\n" +
                "            font-size: 16px;\n" +
                "            resize: vertical;\n" +
                "            min-height: 100px;\n" +
                "            transition: border-color 0.3s ease;\n" +
                "            box-sizing: border-box;\n" +
                "        }\n" +
                "        textarea:focus {\n" +
                "            outline: none;\n" +
                "            border-color: #667eea;\n" +
                "            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);\n" +
                "        }\n" +
                "        .button-group {\n" +
                "            display: flex;\n" +
                "            gap: 15px;\n" +
                "            margin-bottom: 20px;\n" +
                "        }\n" +
                "        button {\n" +
                "            flex: 1;\n" +
                "            padding: 15px 25px;\n" +
                "            border: none;\n" +
                "            border-radius: 10px;\n" +
                "            font-size: 16px;\n" +
                "            font-weight: 600;\n" +
                "            cursor: pointer;\n" +
                "            transition: all 0.3s ease;\n" +
                "            text-transform: uppercase;\n" +
                "            letter-spacing: 0.5px;\n" +
                "        }\n" +
                "        .btn-primary {\n" +
                "            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n" +
                "            color: white;\n" +
                "        }\n" +
                "        .btn-primary:hover {\n" +
                "            transform: translateY(-2px);\n" +
                "            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);\n" +
                "        }\n" +
                "        .btn-danger {\n" +
                "            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);\n" +
                "            color: white;\n" +
                "        }\n" +
                "        .btn-danger:hover {\n" +
                "            transform: translateY(-2px);\n" +
                "            box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);\n" +
                "        }\n" +
                "        .output-container {\n" +
                "            background: #f8f9fa;\n" +
                "            border: 2px solid #e9ecef;\n" +
                "            border-radius: 10px;\n" +
                "            padding: 20px;\n" +
                "            margin-top: 20px;\n" +
                "            max-height: 400px;\n" +
                "            overflow-y: auto;\n" +
                "        }\n" +
                "        .output-text {\n" +
                "            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;\n" +
                "            font-size: 14px;\n" +
                "            line-height: 1.6;\n" +
                "            white-space: pre-wrap;\n" +
                "            word-wrap: break-word;\n" +
                "        }\n" +
                "        .status {\n" +
                "            text-align: center;\n" +
                "            margin: 10px 0;\n" +
                "            padding: 10px;\n" +
                "            border-radius: 5px;\n" +
                "            font-weight: bold;\n" +
                "        }\n" +
                "        .status.connected {\n" +
                "            background-color: #d4edda;\n" +
                "            color: #155724;\n" +
                "            border: 1px solid #c3e6cb;\n" +
                "        }\n" +
                "        .status.disconnected {\n" +
                "            background-color: #f8d7da;\n" +
                "            color: #721c24;\n" +
                "            border: 1px solid #f5c6cb;\n" +
                "        }\n" +
                "        .loading {\n" +
                "            display: inline-block;\n" +
                "            width: 20px;\n" +
                "            height: 20px;\n" +
                "            border: 3px solid #f3f3f3;\n" +
                "            border-top: 3px solid #667eea;\n" +
                "            border-radius: 50%;\n" +
                "            animation: spin 1s linear infinite;\n" +
                "            margin-right: 10px;\n" +
                "        }\n" +
                "        @keyframes spin {\n" +
                "            0% { transform: rotate(0deg); }\n" +
                "            100% { transform: rotate(360deg); }\n" +
                "        }\n" +
                "        .emoji {\n" +
                "            font-size: 1.2em;\n" +
                "        }\n" +
                "        @media (max-width: 600px) {\n" +
                "            .container {\n" +
                "                padding: 20px;\n" +
                "            }\n" +
                "            h1 {\n" +
                "                font-size: 2em;\n" +
                "            }\n" +
                "            .button-group {\n" +
                "                flex-direction: column;\n" +
                "            }\n" +
                "        }\n" +
                "    </style>\n" +
                "</head>\n" +
                "<body>\n" +
                "    <div class=\"container\">\n" +
                "        <h1>🤖 AutoGLM AI助手</h1>\n" +
                "        \n" +
                "        <div class=\"input-group\">\n" +
                "            <label for=\"taskInput\">📝 请输入任务指令：</label>\n" +
                "            <textarea id=\"taskInput\" placeholder=\"例如：打开微信，给张三发消息：你好\"></textarea>\n" +
                "        </div>\n" +
                "        \n" +
                "        <div class=\"button-group\">\n" +
                "            <button id=\"connectButton\" class=\"btn-secondary\">🔗 连接</button>\n" +
                "            <button class=\"btn-primary\" onclick=\"sendCommand()\">🚀 执行指令</button>\n" +
                "            <button class=\"btn-danger\" onclick=\"terminate()\">⏹️ 终止任务</button>\n" +
                "        </div>\n" +
                "        \n" +
                "        <div id=\"status\" class=\"status disconnected\">📡 WebSocket未连接</div>\n" +
                "        \n" +
                "        <div class=\"output-container\">\n" +
                "            <div id=\"output\" class=\"output-text\">等待指令...</div>\n" +
                "        </div>\n" +
                "    </div>\n" +
                "\n" +
                "    <script>\n" +
                "        let ws = null;\n" +
                "        let reconnectInterval = null;\n" +
                "        let heartbeatInterval = null;\n" +
                "        let lastHeartbeatResponse = Date.now();\n" +
                "        const HEARTBEAT_INTERVAL = 30000; // 30秒发送一次心跳\n" +
                "        const HEARTBEAT_TIMEOUT = 10000; // 10秒超时\n" +
                "\n" +
        "        function getWebSocketUrl() {\n" +
        "            // 直接使用固定的服务器地址，避免WebView环境下的hostname问题\n" +
        "            return `ws://192.168.2.12:8002/ws`;\n" +
        "        }\n" +
                "\n" +
                "        function connectWebSocket() {\n" +
                "            if (ws && ws.readyState === WebSocket.OPEN) {\n" +
                "                return;\n" +
                "            }\n" +
                "\n" +
                "            const url = getWebSocketUrl();\n" +
                "            console.log('Attempting to connect to:', url);\n" +
                "            \n" +
                "            try {\n" +
                "                ws = new WebSocket(url);\n" +
                "                \n" +
                "                ws.onopen = function(event) {\n" +
                "                    console.log('WebSocket connected successfully');\n" +
                "                    updateStatus('connected', 'WebSocket已连接');\n" +
                "                    clearInterval(reconnectInterval);\n" +
                "                    // 不自动启动心跳包，让用户控制\n" +
                "                };\n" +
                "\n" +
                "            ws.onmessage = function(event) {\n" +
                "                const message = event.data;\n" +
                "                console.log('Received:', message);\n" +
                "\n" +
                "                // 处理心跳包响应\n" +
                "                try {\n" +
                "                    const data = JSON.parse(message);\n" +
                "                    if (data.type === 'pong') {\n" +
                "                        lastHeartbeatResponse = Date.now();\n" +
                "                        console.log('💚 收到心跳响应');\n" +
                "                        return; // 心跳包响应不显示在界面上\n" +
                "                    }\n" +
                "                } catch (e) {\n" +
                "                    // 不是JSON消息，继续正常处理\n" +
                "                }\n" +
                "\n" +
                "                addOutput(message);\n" +
                "                // 发送消息给Android应用显示在悬浮窗\n" +
                "                if (window.AndroidInterface) {\n" +
                "                    window.AndroidInterface.showInOverlay(message);\n" +
                "                }\n" +
                "            };\n" +
                "\n" +
                "            ws.onclose = function(event) {\n" +
                "                console.log('WebSocket closed');\n" +
                "                updateStatus('disconnected', '📡 WebSocket连接断开，正在重连...');\n" +
                "                stopHeartbeat();\n" +
                "                scheduleReconnect();\n" +
                "            };\n" +
                "\n" +
                "            ws.onerror = function(error) {\n" +
                "                console.error('WebSocket error:', error);\n" +
                "                updateStatus('disconnected', '❌ WebSocket连接错误');\n" +
                "            };\n" +
                "        }\n" +
                "\n" +
                "        function scheduleReconnect() {\n" +
                "            if (reconnectInterval) clearInterval(reconnectInterval);\n" +
                "            reconnectInterval = setInterval(function() {\n" +
                "                connectWebSocket();\n" +
                "            }, 3000);\n" +
                "        }\n" +
                "\n" +
                "        function startHeartbeat() {\n" +
                "            console.log('启动心跳包机制');\n" +
                "            stopHeartbeat(); // 确保没有重复的定时器\n" +
                "\n" +
                "            lastHeartbeatResponse = Date.now();\n" +
                "\n" +
                "            heartbeatInterval = setInterval(function() {\n" +
                "                if (ws && ws.readyState === WebSocket.OPEN) {\n" +
                "                    // 发送心跳包\n" +
                "                    const heartbeatMessage = { type: 'ping', timestamp: Date.now() };\n" +
                "                    ws.send(JSON.stringify(heartbeatMessage));\n" +
                "                    console.log('💓 发送心跳包');\n" +
                "\n" +
                "                    // 检查上次心跳响应是否超时\n" +
                "                    const now = Date.now();\n" +
                "                    if (now - lastHeartbeatResponse > HEARTBEAT_TIMEOUT) {\n" +
                "                        console.log('💔 心跳超时，重新连接');\n" +
                "                        stopHeartbeat();\n" +
                "                        ws.close();\n" +
                "                        return;\n" +
                "                    }\n" +
                "                } else {\n" +
                "                    console.log('💔 连接已断开，停止心跳');\n" +
                "                    stopHeartbeat();\n" +
                "                }\n" +
                "            }, HEARTBEAT_INTERVAL);\n" +
                "        }\n" +
                "\n" +
                "        function stopHeartbeat() {\n" +
                "            if (heartbeatInterval) {\n" +
                "                clearInterval(heartbeatInterval);\n" +
                "                heartbeatInterval = null;\n" +
                "                console.log('停止心跳包机制');\n" +
                "            }\n" +
                "        }\n" +
                "\n" +
                "        function updateStatus(className, text) {\n" +
                "            const statusElement = document.getElementById('status');\n" +
                "            statusElement.className = 'status ' + className;\n" +
                "            statusElement.textContent = text;\n" +
                "        }\n" +
                "\n" +
                "        function addOutput(text) {\n" +
                "            const outputElement = document.getElementById('output');\n" +
                "            outputElement.textContent += text + '\\n';\n" +
                "            outputElement.scrollTop = outputElement.scrollHeight;\n" +
                "        }\n" +
                "\n" +
                "        function sendCommand() {\n" +
                "            const taskInput = document.getElementById('taskInput');\n" +
                "            const command = taskInput.value.trim();\n" +
                "            \n" +
                "            if (!command) {\n" +
                "                alert('请输入任务指令');\n" +
                "                return;\n" +
                "            }\n" +
                "            \n" +
                "            if (ws && ws.readyState === WebSocket.OPEN) {\n" +
                "                // 首次发送命令时启动心跳包\n" +
                "                if (!heartbeatInterval) {\n" +
                "                    startHeartbeat();\n" +
                "                    console.log('首次发送命令，启动心跳包机制');\n" +
                "                }\n" +
                "\n" +
                "                ws.send(JSON.stringify({ text: command }));\n" +
                "                addOutput('🚀 发送指令: ' + command + '\\n');\n" +
                "                taskInput.value = '';\n" +
                "            } else {\n" +
                "                addOutput('❌ WebSocket未连接，请稍后重试\\n');\n" +
                "            }\n" +
                "        }\n" +
                "\n" +
                "        function terminate() {\n" +
                "            if (ws && ws.readyState === WebSocket.OPEN) {\n" +
                "                ws.send(JSON.stringify({ action: 'terminate' }));\n" +
                "                addOutput('✅ 任务终止请求已发送\\n');\n" +
                "            } else {\n" +
                "                addOutput('❌ WebSocket未连接，无法终止任务\\n');\n" +
                "            }\n" +
                "        }\n" +
                "\n" +
                "        // 页面加载完成后初始化，但不自动连接\n" +
                "        document.addEventListener('DOMContentLoaded', function() {\n" +
                "            console.log('页面加载完成，等待用户手动连接...');\n" +
                "            // 不自动连接，让用户手动控制\n" +
                "            \n" +
                "            // 支持回车发送\n" +
                "            document.getElementById('taskInput').addEventListener('keypress', function(e) {\n" +
                "                if (e.key === 'Enter' && !e.shiftKey) {\n" +
                "                    e.preventDefault();\n" +
                "                    sendCommand();\n" +
                "                }\n" +
                "            });\n" +
                "            \n" +
                "            // 绑定连接按钮\n" +
                "            document.getElementById('connectButton').addEventListener('click', function() {\n" +
                "                connectWebSocket();\n" +
                "            });\n" +
                "        });\n" +
                "\n" +
                "        // 额外的自动重连机制：每30秒检查一次连接状态\n" +
                "        setInterval(function() {\n" +
                "            if (!ws || ws.readyState === WebSocket.CLOSED || ws.readyState === WebSocket.CLOSING) {\n" +
                "                console.log('检测到WebSocket未连接，尝试重连...');\n" +
                "                connectWebSocket();\n" +
                "            }\n" +
                "        }, 30000);\n" +
                "    </script>\n" +
                "</body>\n" +
                "</html>";
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (webView != null) {
            webView.destroy();
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
