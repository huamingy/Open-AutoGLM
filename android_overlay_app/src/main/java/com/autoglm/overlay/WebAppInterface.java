package com.autoglm.overlay;

import android.content.Context;
import android.content.Intent;
import android.webkit.JavascriptInterface;

public class WebAppInterface {
    Context mContext;

    WebAppInterface(Context c) {
        mContext = c;
    }

    @JavascriptInterface
    public void showInOverlay(String message) {
        // 发送广播给悬浮窗显示消息
        Intent intent = new Intent("com.autoglm.overlay.UPDATE");
        intent.putExtra("title", "Web界面消息");
        intent.putExtra("content", message);
        intent.putExtra("status", "消息");
        mContext.sendBroadcast(intent);
    }

    @JavascriptInterface
    public void terminateTask() {
        // 发送终止广播
        Intent intent = new Intent("com.autoglm.overlay.TERMINATE");
        mContext.sendBroadcast(intent);
    }
}
