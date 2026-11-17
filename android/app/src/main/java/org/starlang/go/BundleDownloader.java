package org.starlang.go;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Downloads and caches live Star application bundles (.starmobile) over LAN/WiFi.
 */
public class BundleDownloader {
    private static final String TAG = "BundleDownloader";
    private final Context context;
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final Handler mainHandler = new Handler(Looper.getMainLooper());

    public interface Callback {
        void onSuccess(byte[] bundleBytes, File cachedFile);
        void onError(String error);
    }

    public BundleDownloader(Context context) {
        this.context = context;
    }

    public static String normalizeUrl(String rawUrl) {
        String url = rawUrl.trim();
        if (url.startsWith("star://")) {
            url = "http://" + url.substring(7);
        }
        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            url = "http://" + url;
        }
        if (!url.contains("/bundle") && !url.endsWith(".starmobile")) {
            if (url.endsWith("/")) {
                url = url + "bundle.starmobile";
            } else {
                url = url + "/bundle.starmobile";
            }
        }
        return url;
    }

    public void downloadBundle(String rawUrl, Callback callback) {
        final String resolvedUrl = normalizeUrl(rawUrl);
        Log.i(TAG, "Fetching Star mobile bundle from: " + resolvedUrl);

        executor.execute(() -> {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(resolvedUrl);
                conn = (HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(8000);
                conn.setReadTimeout(15000);
                conn.setRequestMethod("GET");
                conn.connect();

                int code = conn.getResponseCode();
                if (code != 200) {
                    throw new Exception("HTTP " + code + ": " + conn.getResponseMessage());
                }

                InputStream in = conn.getInputStream();
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                byte[] buf = new byte[8192];
                int n;
                while ((n = in.read(buf)) != -1) {
                    out.write(buf, 0, n);
                }
                in.close();

                byte[] bundleData = out.toByteArray();
                File cacheDir = new File(context.getCacheDir(), "star_go");
                if (!cacheDir.exists()) cacheDir.mkdirs();
                File cachedFile = new File(cacheDir, "current_app.starmobile");
                FileOutputStream fos = new FileOutputStream(cachedFile);
                fos.write(bundleData);
                fos.close();

                mainHandler.post(() -> callback.onSuccess(bundleData, cachedFile));

            } catch (Exception e) {
                Log.e(TAG, "Failed to download Star bundle: " + e.getMessage());
                mainHandler.post(() -> callback.onError(e.getMessage()));
            } finally {
                if (conn != null) conn.disconnect();
            }
        });
    }
}

