package com.autoglm.overlay;

import android.app.IntentService;
import android.content.Intent;
import android.util.Log;

import java.io.IOException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class TerminateService extends IntentService {

    private static final String TAG = "TerminateService";

    public TerminateService() {
        super("TerminateService");
    }

    @Override
    protected void onHandleIntent(Intent intent) {
        // 发送HTTP请求到WebSocket服务器终止任务
        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url("http://192.168.2.12:8002/terminate") // WebSocket服务器地址
                .post(okhttp3.RequestBody.create("", okhttp3.MediaType.parse("application/json")))
                .build();

        try {
            Response response = client.newCall(request).execute();
            Log.d(TAG, "Terminate request sent, response: " + response.code());
        } catch (IOException e) {
            Log.e(TAG, "Failed to send terminate request", e);
        }
    }
}
