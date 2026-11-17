package org.starlang.go;

import android.app.Dialog;
import android.content.Context;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

/**
 * Expo Go-equivalent floating developer menu triggered by device shake gesture.
 */
public class DevMenuBottomSheet extends Dialog {

    public interface DevMenuListener {
        void onReloadRequested();
        void onTogglePerfMonitor();
        void onDisconnectRequested();
    }

    private final String currentUrl;
    private final boolean isPerfVisible;
    private final DevMenuListener listener;

    private static GradientDrawable makeCard(int bgColor, float radius, int strokeColor, int strokeWidth) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(bgColor);
        d.setCornerRadius(radius);
        if (strokeWidth > 0) d.setStroke(strokeWidth, strokeColor);
        return d;
    }

    public DevMenuBottomSheet(Context context, String url, boolean perfVisible, DevMenuListener listener) {
        super(context);
        this.currentUrl = url != null ? url : "local://showcase";
        this.isPerfVisible = perfVisible;
        this.listener = listener;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);

        LinearLayout layout = new LinearLayout(getContext());
        layout.setOrientation(LinearLayout.VERTICAL);
        // Rounded top sheet
        GradientDrawable sheetBg = new GradientDrawable();
        sheetBg.setColor(Color.parseColor("#0F172A"));
        sheetBg.setCornerRadii(new float[]{36, 36, 36, 36, 0, 0, 0, 0});
        sheetBg.setStroke(2, Color.parseColor("#1E293B"));
        layout.setBackground(sheetBg);
        layout.setPadding(48, 36, 48, 56);

        // Top drag handle
        View handle = new View(getContext());
        handle.setBackground(makeCard(Color.parseColor("#475569"), 4f, 0, 0));
        LinearLayout.LayoutParams handleLp = new LinearLayout.LayoutParams(96, 8);
        handleLp.gravity = Gravity.CENTER_HORIZONTAL;
        handleLp.setMargins(0, 0, 0, 28);
        handle.setLayoutParams(handleLp);
        layout.addView(handle);

        TextView title = new TextView(getContext());
        title.setText("⭐ Star Go Developer Menu");
        title.setTextSize(19f);
        title.setTextColor(Color.parseColor("#38BDF8"));
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        title.setPadding(0, 0, 0, 8);
        layout.addView(title);

        TextView urlView = new TextView(getContext());
        urlView.setText("Active Session: " + currentUrl);
        urlView.setTextSize(12f);
        urlView.setTextColor(Color.parseColor("#94A3B8"));
        urlView.setPadding(0, 0, 0, 28);
        layout.addView(urlView);

        // Reload Button
        Button reloadBtn = createMenuButton("🔄 Reload App (Fast Refresh)", "#2563EB", v -> {
            dismiss();
            if (listener != null) listener.onReloadRequested();
        });
        layout.addView(reloadBtn);

        // Performance Monitor Toggle
        String perfLabel = isPerfVisible ? "⚡ Hide Performance HUD" : "⚡ Show Performance HUD";
        Button perfBtn = createMenuButton(perfLabel, "#1E293B", v -> {
            dismiss();
            if (listener != null) listener.onTogglePerfMonitor();
        });
        layout.addView(perfBtn);

        // Hardware Diagnostics Button
        Button hwBtn = createMenuButton("📱 Hardware Telemetry & Torch", "#0F766E", v -> {
            dismiss();
            android.content.Intent hwIntent = new android.content.Intent(getContext(), org.starlang.hardware.HardwareInspectorActivity.class);
            getContext().startActivity(hwIntent);
        });
        layout.addView(hwBtn);

        // Disconnect Button
        Button disconnectBtn = createMenuButton("🚪 Exit to Star Go Home", "#DC2626", v -> {
            dismiss();
            if (listener != null) listener.onDisconnectRequested();
        });
        layout.addView(disconnectBtn);

        setContentView(layout);

        Window window = getWindow();
        if (window != null) {
            window.setLayout(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            window.setGravity(Gravity.BOTTOM);
            window.setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        }
    }

    private Button createMenuButton(String label, String bgColor, View.OnClickListener onClick) {
        Button btn = new Button(getContext());
        btn.setText(label);
        btn.setTextColor(Color.WHITE);
        btn.setTextSize(14f);
        btn.setTypeface(null, android.graphics.Typeface.BOLD);
        btn.setBackground(makeCard(Color.parseColor(bgColor), 20f, Color.parseColor("#334155"), 1));
        btn.setPadding(28, 22, 28, 22);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.WRAP_CONTENT
        );
        lp.setMargins(0, 0, 0, 16);
        btn.setLayoutParams(lp);
        btn.setOnClickListener(onClick);
        return btn;
    }
}
