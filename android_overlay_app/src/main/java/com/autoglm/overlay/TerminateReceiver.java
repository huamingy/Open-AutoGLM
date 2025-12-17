package com.autoglm.overlay;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class TerminateReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        // 当接收到终止信号时，可以在这里添加处理逻辑
        // 比如发送HTTP请求到WebSocket服务器来终止任务

        // 这里可以调用系统服务或者发送网络请求
        // 由于这是广播接收器，我们可以启动一个服务或者发送HTTP请求

        // 示例：启动一个Intent来处理终止
        Intent terminateIntent = new Intent(context, TerminateService.class);
        context.startService(terminateIntent);
    }
}
