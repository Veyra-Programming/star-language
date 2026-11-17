package org.starlang.go;

import android.content.Context;
import android.graphics.Color;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.TextView;

/**
 * Real-time performance monitor overlay (FPS, Frame Time, Memory).
 */
public class PerformanceOverlay {
    private final FrameLayout container;
    private final TextView statsView;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private boolean isVisible = false;
    private long lastFrameTime = System.nanoTime();
    private int frameCount = 0;
    private double currentFps = 60.0;

    public PerformanceOverlay(Context context, FrameLayout root) {
        this.container = root;

        statsView = new TextView(context);
        statsView.setBackgroundColor(Color.parseColor("#CC090D16"));
        statsView.setTextColor(Color.parseColor("#38BDF8"));
        statsView.setTextSize(11f);
        statsView.setPadding(24, 16, 24, 16);
        statsView.setTypeface(android.graphics.Typeface.MONOSPACE);

        FrameLayout.LayoutParams lp = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        );
        lp.gravity = Gravity.TOP | Gravity.END;
        lp.topMargin = 48;
        lp.rightMargin = 24;
        statsView.setLayoutParams(lp);

        updateText();
    }

    public void setVisible(boolean visible) {
        this.isVisible = visible;
        if (visible) {
            if (statsView.getParent() == null) {
                container.addView(statsView);
            }
            startTicker();
        } else {
            container.removeView(statsView);
        }
    }

    public boolean isVisible() {
        return isVisible;
    }

    public void onFrameRendered() {
        frameCount++;
        long now = System.nanoTime();
        long diff = now - lastFrameTime;
        if (diff >= 1_000_000_000L) { // 1 second
            currentFps = (frameCount * 1_000_000_000.0) / diff;
            frameCount = 0;
            lastFrameTime = now;
            updateText();
        }
    }

    private void updateText() {
        Runtime runtime = Runtime.getRuntime();
        long usedMem = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
        double frameTimeMs = 1000.0 / Math.max(1.0, currentFps);

        String text = String.format("⚡ Star 1.3.0\nFPS:  %.1f\nTIME: %.1f ms\nMEM:  %d MB",
                currentFps, frameTimeMs, usedMem);
        statsView.setText(text);
    }

    private void startTicker() {
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                if (isVisible) {
                    updateText();
                    handler.postDelayed(this, 1000);
                }
            }
        }, 1000);
    }
}

