package org.starlang.hardware;

import android.app.Activity;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

/**
 * Real Device Hardware Diagnostics & Telemetry Studio.
 * Live sensor streams, flashlight toggle, haptic bench, battery telemetry,
 * 120Hz display refresh readout, and system performance specs.
 */
public class HardwareInspectorActivity extends Activity {
    private AndroidHardwareManager hw;
    private final Handler handler = new Handler(Looper.getMainLooper());

    private TextView accelText;
    private TextView gyroText;
    private TextView luxText;
    private TextView batteryText;
    private TextView batteryStatusText;
    private TextView networkText;
    private Button torchBtn;

    private static GradientDrawable makeCard(int bgColor, float radius, int strokeColor, int strokeWidth) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(bgColor);
        d.setCornerRadius(radius);
        if (strokeWidth > 0) d.setStroke(strokeWidth, strokeColor);
        return d;
    }

    private static GradientDrawable makeGradientBtn(int startColor, int endColor, float radius) {
        GradientDrawable d = new GradientDrawable(
            GradientDrawable.Orientation.LEFT_RIGHT,
            new int[]{startColor, endColor}
        );
        d.setCornerRadius(radius);
        return d;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        hw = AndroidHardwareManager.getInstance(this);

        ScrollView scrollView = new ScrollView(this);
        scrollView.setFillViewport(true);
        scrollView.setBackgroundColor(Color.parseColor("#090D16"));

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 48, 36, 60);

        // Header
        LinearLayout headerRow = new LinearLayout(this);
        headerRow.setOrientation(LinearLayout.HORIZONTAL);
        headerRow.setGravity(Gravity.CENTER_VERTICAL);
        headerRow.setPadding(0, 0, 0, 32);

        Button backBtn = new Button(this);
        backBtn.setText("← Back");
        backBtn.setTextColor(Color.WHITE);
        backBtn.setTextSize(13f);
        backBtn.setBackground(makeCard(Color.parseColor("#1E293B"), 18f, Color.parseColor("#334155"), 1));
        backBtn.setPadding(24, 14, 24, 14);
        backBtn.setOnClickListener(v -> finish());
        headerRow.addView(backBtn);

        TextView title = new TextView(this);
        title.setText("  ⚡ Hardware Inspector");
        title.setTextSize(22f);
        title.setTextColor(Color.parseColor("#38BDF8"));
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        headerRow.addView(title);
        root.addView(headerRow);

        // 1. Device Specs Card
        LinearLayout specsCard = new LinearLayout(this);
        specsCard.setOrientation(LinearLayout.VERTICAL);
        specsCard.setBackground(makeCard(Color.parseColor("#0F172A"), 24f, Color.parseColor("#1E293B"), 2));
        specsCard.setPadding(36, 32, 36, 32);

        TextView specsTitle = new TextView(this);
        specsTitle.setText("📱 Physical Device Specifications");
        specsTitle.setTextSize(16f);
        specsTitle.setTextColor(Color.WHITE);
        specsTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        specsTitle.setPadding(0, 0, 0, 16);
        specsCard.addView(specsTitle);

        float hz = hw.getDisplayRefreshRate(this);
        long totalRam = hw.getTotalMemoryMB();
        long availRam = hw.getAvailableMemoryMB();

        addSpecRow(specsCard, "Device Model:", hw.getDeviceModel());
        addSpecRow(specsCard, "CPU Architecture:", hw.getCpuArchitecture() + " (64-bit ARM)");
        addSpecRow(specsCard, "OS Platform:", hw.getAndroidVersion());
        addSpecRow(specsCard, "Display Refresh Rate:", String.format("%.0f Hz (Ultra Vision Display)", hz));
        addSpecRow(specsCard, "Memory (RAM):", String.format("%.1f GB Free / %.1f GB Total", availRam / 1024.0, totalRam / 1024.0));
        root.addView(specsCard);

        addSpacer(root, 24);

        // 2. Real Hardware Flashlight Controller
        LinearLayout torchCard = new LinearLayout(this);
        torchCard.setOrientation(LinearLayout.VERTICAL);
        torchCard.setBackground(makeCard(Color.parseColor("#0F172A"), 24f, Color.parseColor("#1E293B"), 2));
        torchCard.setPadding(36, 32, 36, 32);

        TextView torchTitle = new TextView(this);
        torchTitle.setText("🔦 Hardware Flashlight (Torch)");
        torchTitle.setTextSize(16f);
        torchTitle.setTextColor(Color.WHITE);
        torchTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        torchTitle.setPadding(0, 0, 0, 8);
        torchCard.addView(torchTitle);

        TextView torchSub = new TextView(this);
        torchSub.setText("Direct physical Camera LED flash control:");
        torchSub.setTextSize(12f);
        torchSub.setTextColor(Color.parseColor("#94A3B8"));
        torchSub.setPadding(0, 0, 0, 18);
        torchCard.addView(torchSub);

        torchBtn = new Button(this);
        torchBtn.setText("💡 Turn Flashlight ON");
        torchBtn.setTextSize(15f);
        torchBtn.setTextColor(Color.WHITE);
        torchBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        torchBtn.setBackground(makeGradientBtn(Color.parseColor("#D97706"), Color.parseColor("#B45309"), 22f));
        torchBtn.setPadding(32, 24, 32, 24);
        torchBtn.setOnClickListener(v -> {
            hw.vibrateClick();
            boolean newState = hw.toggleTorch();
            updateTorchButton(newState);
        });
        torchCard.addView(torchBtn);
        root.addView(torchCard);

        addSpacer(root, 24);

        // 3. Precision Haptic Bench Card
        LinearLayout hapticCard = new LinearLayout(this);
        hapticCard.setOrientation(LinearLayout.VERTICAL);
        hapticCard.setBackground(makeCard(Color.parseColor("#0F172A"), 24f, Color.parseColor("#1E293B"), 2));
        hapticCard.setPadding(36, 32, 36, 32);

        TextView hapticTitle = new TextView(this);
        hapticTitle.setText("📳 Precision Haptic & Vibration Engine");
        hapticTitle.setTextSize(16f);
        hapticTitle.setTextColor(Color.WHITE);
        hapticTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        hapticTitle.setPadding(0, 0, 0, 8);
        hapticCard.addView(hapticTitle);

        TextView hapticSub = new TextView(this);
        hapticSub.setText("Tap each button to feel customized vibration waveforms:");
        hapticSub.setTextSize(12f);
        hapticSub.setTextColor(Color.parseColor("#94A3B8"));
        hapticSub.setPadding(0, 0, 0, 18);
        hapticCard.addView(hapticSub);

        LinearLayout hapticRow1 = new LinearLayout(this);
        hapticRow1.setOrientation(LinearLayout.HORIZONTAL);
        Button btnTick = createHapticBtn("Tick (Light)", v -> hw.vibrateTick());
        Button btnClick = createHapticBtn("Click (Medium)", v -> hw.vibrateClick());
        hapticRow1.addView(btnTick, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        hapticRow1.addView(btnClick, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        hapticCard.addView(hapticRow1);

        LinearLayout hapticRow2 = new LinearLayout(this);
        hapticRow2.setOrientation(LinearLayout.HORIZONTAL);
        hapticRow2.setPadding(0, 12, 0, 0);
        Button btnHeavy = createHapticBtn("💥 Heavy Thud", v -> hw.vibrateHeavy());
        Button btnSuccess = createHapticBtn("✨ Success Burst", v -> hw.vibrateSuccess());
        hapticRow2.addView(btnHeavy, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        hapticRow2.addView(btnSuccess, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        hapticCard.addView(hapticRow2);

        LinearLayout hapticRow3 = new LinearLayout(this);
        hapticRow3.setOrientation(LinearLayout.HORIZONTAL);
        hapticRow3.setPadding(0, 12, 0, 0);
        Button btnError = createHapticBtn("❌ Error Waveform", v -> hw.vibrateError());
        hapticRow3.addView(btnError, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        hapticCard.addView(hapticRow3);

        root.addView(hapticCard);

        addSpacer(root, 24);

        // 4. Live Sensor Streams
        LinearLayout sensorCard = new LinearLayout(this);
        sensorCard.setOrientation(LinearLayout.VERTICAL);
        sensorCard.setBackground(makeCard(Color.parseColor("#0F172A"), 24f, Color.parseColor("#1E293B"), 2));
        sensorCard.setPadding(36, 32, 36, 32);

        TextView sensorTitle = new TextView(this);
        sensorTitle.setText("🧭 Live Real-Time Sensor Telemetry");
        sensorTitle.setTextSize(16f);
        sensorTitle.setTextColor(Color.WHITE);
        sensorTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        sensorTitle.setPadding(0, 0, 0, 16);
        sensorCard.addView(sensorTitle);

        accelText = new TextView(this);
        accelText.setText("Accelerometer (m/s²): X: 0.00 | Y: 0.00 | Z: 9.80");
        accelText.setTextSize(13f);
        accelText.setTextColor(Color.parseColor("#38BDF8"));
        accelText.setPadding(0, 0, 0, 10);
        sensorCard.addView(accelText);

        gyroText = new TextView(this);
        gyroText.setText("Gyroscope (rad/s): X: 0.00 | Y: 0.00 | Z: 0.00");
        gyroText.setTextSize(13f);
        gyroText.setTextColor(Color.parseColor("#A78BFA"));
        gyroText.setPadding(0, 0, 0, 10);
        sensorCard.addView(gyroText);

        luxText = new TextView(this);
        luxText.setText("Ambient Light Sensor: 0.0 Lux");
        luxText.setTextSize(13f);
        luxText.setTextColor(Color.parseColor("#FBBF24"));
        sensorCard.addView(luxText);

        root.addView(sensorCard);

        addSpacer(root, 24);

        // 5. Battery & Power Telemetry
        LinearLayout batteryCard = new LinearLayout(this);
        batteryCard.setOrientation(LinearLayout.VERTICAL);
        batteryCard.setBackground(makeCard(Color.parseColor("#0F172A"), 24f, Color.parseColor("#1E293B"), 2));
        batteryCard.setPadding(36, 32, 36, 32);

        TextView bTitle = new TextView(this);
        bTitle.setText("🔋 Battery & Power Telemetry");
        bTitle.setTextSize(16f);
        bTitle.setTextColor(Color.WHITE);
        bTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        bTitle.setPadding(0, 0, 0, 16);
        batteryCard.addView(bTitle);

        batteryText = new TextView(this);
        batteryText.setText(String.format("Battery Level: %d%% • Temp: %.1f°C", hw.getBatteryPercentage(), hw.getBatteryTemperatureCelsius()));
        batteryText.setTextSize(14f);
        batteryText.setTextColor(Color.parseColor("#34D399"));
        batteryText.setPadding(0, 0, 0, 10);
        batteryCard.addView(batteryText);

        batteryStatusText = new TextView(this);
        batteryStatusText.setText("Charging State: " + hw.getChargingPlugType());
        batteryStatusText.setTextSize(13f);
        batteryStatusText.setTextColor(Color.parseColor("#94A3B8"));
        batteryCard.addView(batteryStatusText);

        root.addView(batteryCard);

        addSpacer(root, 24);

        // 6. Network Telemetry
        LinearLayout netCard = new LinearLayout(this);
        netCard.setOrientation(LinearLayout.VERTICAL);
        netCard.setBackground(makeCard(Color.parseColor("#0F172A"), 24f, Color.parseColor("#1E293B"), 2));
        netCard.setPadding(36, 32, 36, 32);

        TextView netTitle = new TextView(this);
        netTitle.setText("🌐 Network & Connectivity");
        netTitle.setTextSize(16f);
        netTitle.setTextColor(Color.WHITE);
        netTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        netTitle.setPadding(0, 0, 0, 12);
        netCard.addView(netTitle);

        networkText = new TextView(this);
        networkText.setText("Active Interface: " + hw.getNetworkType());
        networkText.setTextSize(13f);
        networkText.setTextColor(Color.parseColor("#38BDF8"));
        netCard.addView(networkText);

        root.addView(netCard);

        scrollView.addView(root);
        setContentView(scrollView);
    }

    private Button createHapticBtn(String text, View.OnClickListener clk) {
        Button b = new Button(this);
        b.setText(text);
        b.setTextColor(Color.WHITE);
        b.setTextSize(12f);
        b.setBackground(makeCard(Color.parseColor("#1E293B"), 16f, Color.parseColor("#334155"), 1));
        b.setPadding(16, 16, 16, 16);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        lp.setMargins(6, 0, 6, 0);
        b.setLayoutParams(lp);
        b.setOnClickListener(clk);
        return b;
    }

    private void updateTorchButton(boolean active) {
        if (active) {
            torchBtn.setText("💡 Flashlight is ON (Tap to Turn OFF)");
            torchBtn.setBackground(makeGradientBtn(Color.parseColor("#EF4444"), Color.parseColor("#B91C1C"), 22f));
        } else {
            torchBtn.setText("💡 Turn Flashlight ON");
            torchBtn.setBackground(makeGradientBtn(Color.parseColor("#D97706"), Color.parseColor("#B45309"), 22f));
        }
    }

    private void addSpecRow(LinearLayout parent, String key, String val) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setPadding(0, 4, 0, 4);

        TextView k = new TextView(this);
        k.setText(key + " ");
        k.setTextSize(12f);
        k.setTextColor(Color.parseColor("#94A3B8"));
        row.addView(k);

        TextView v = new TextView(this);
        v.setText(val);
        v.setTextSize(12f);
        v.setTextColor(Color.parseColor("#E2E8F0"));
        v.setTypeface(null, android.graphics.Typeface.BOLD);
        row.addView(v);

        parent.addView(row);
    }

    private void addSpacer(LinearLayout parent, int dp) {
        View sp = new View(this);
        parent.addView(sp, new LinearLayout.LayoutParams(1, dp));
    }

    @Override
    protected void onResume() {
        super.onResume();
        hw.startSensors((ax, ay, az, gx, gy, gz, lux) -> {
            handler.post(() -> {
                if (accelText != null) {
                    accelText.setText(String.format("Accelerometer (m/s²): X: %+.2f | Y: %+.2f | Z: %+.2f", ax, ay, az));
                }
                if (gyroText != null) {
                    gyroText.setText(String.format("Gyroscope (rad/s): X: %+.2f | Y: %+.2f | Z: %+.2f", gx, gy, gz));
                }
                if (luxText != null) {
                    luxText.setText(String.format("Ambient Light Sensor: %.1f Lux", lux));
                }
            });
        });
    }

    @Override
    protected void onPause() {
        super.onPause();
        hw.stopSensors();
        hw.setTorchMode(false);
    }
}

