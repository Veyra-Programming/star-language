package org.starlang.go;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.drawable.GradientDrawable;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Vibrator;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.starlang.runtime.StarNativeBridge;
import org.starlang.runtime.StarSurfaceView;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Star Go Android Application Host (Expo Go Architecture).
 * Professional mobile development companion with QR scanning, LAN streaming,
 * offline interactive showcase, and floating Dev Menu.
 */
public class MainActivity extends Activity implements SensorEventListener {
    private static final String TAG = "StarGo";
    private static final int REQUEST_QR_SCAN = 101;
    private static final int REQUEST_PERMISSIONS_ALL = 201;
    private static final int REQUEST_CAMERA_FOR_SCAN = 202;
    private static final String PREFS_NAME = "star_go_prefs";
    private static final String KEY_RECENT = "recent_servers";

    private FrameLayout rootContainer;
    private View homeView;
    private FrameLayout appContainer;
    private StarSurfaceView currentSurfaceView;
    private PerformanceOverlay perfOverlay;
    private BundleDownloader downloader;
    private Vibrator vibrator;

    private SensorManager sensorManager;
    private Sensor accelerometer;
    private float lastX, lastY, lastZ;
    private long lastShakeTime;

    private String activeServerUrl = null;
    private boolean isAppRunning = false;
    private SharedPreferences prefs;

    private static GradientDrawable makeCardDrawable(int bgColor, float radius, int strokeColor, int strokeWidth) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(bgColor);
        d.setCornerRadius(radius);
        if (strokeWidth > 0) {
            d.setStroke(strokeWidth, strokeColor);
        }
        return d;
    }

    private static GradientDrawable makeGradientButton(int startColor, int endColor, float radius) {
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
        prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        downloader = new BundleDownloader(this);

        try {
            vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        } catch (Exception ignored) {}

        rootContainer = new FrameLayout(this);
        rootContainer.setBackgroundColor(Color.parseColor("#090D16"));

        // Setup Shake Detector
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        if (sensorManager != null) {
            accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        }

        // Setup Views
        homeView = createHomeDashboardView();
        appContainer = new FrameLayout(this);
        perfOverlay = new PerformanceOverlay(this, appContainer);

        rootContainer.addView(homeView);
        setContentView(rootContainer);

        // Check for deep link intent (star://192.168.x.x:8123)
        handleIntent(getIntent());

        // Check & prompt hardware permissions
        checkAndRequestAllPermissions();
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleIntent(intent);
    }

    private void handleIntent(Intent intent) {
        if (intent != null && Intent.ACTION_VIEW.equals(intent.getAction())) {
            Uri data = intent.getData();
            if (data != null) {
                String url = data.toString();
                Log.i(TAG, "Launched via deep link: " + url);
                connectToServer(url);
            }
        }
    }

    private void haptic() {
        if (vibrator != null) {
            try {
                vibrator.vibrate(15);
            } catch (Exception ignored) {}
        }
    }

    private void checkAndRequestAllPermissions() {
        List<String> needed = new ArrayList<>();
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.CAMERA);
        }
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.ACCESS_FINE_LOCATION);
        }
        if (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            needed.add(Manifest.permission.ACCESS_COARSE_LOCATION);
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                needed.add(Manifest.permission.POST_NOTIFICATIONS);
            }
        }
        if (!needed.isEmpty()) {
            showPermissionExplanationDialog(needed.toArray(new String[0]));
        }
    }

    private void showPermissionExplanationDialog(final String[] permissions) {
        new AlertDialog.Builder(this)
            .setTitle("🛡️ Star Go Hardware Permissions")
            .setMessage(
                "Star Go requires device permissions to enable Expo Go-grade testing:\n\n" +
                "• 📷 Camera: Live QR Code scanning from your terminal\n" +
                "• 📍 Location: Real-time sensor & WiFi telemetry\n" +
                "• 🔔 Notifications: Live reload & build progress alerts\n\n" +
                "Please allow these permissions in the upcoming system prompt."
            )
            .setPositiveButton("Allow Permissions", (dialog, which) -> {
                requestPermissions(permissions, REQUEST_PERMISSIONS_ALL);
            })
            .setNegativeButton("Later", (dialog, which) -> dialog.dismiss())
            .show();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CAMERA_FOR_SCAN) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Camera granted! Opening scanner...", Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(this, QRScannerActivity.class);
                startActivityForResult(intent, REQUEST_QR_SCAN);
            } else {
                Toast.makeText(this, "Camera permission denied. Cannot scan QR code.", Toast.LENGTH_LONG).show();
            }
        } else if (requestCode == REQUEST_PERMISSIONS_ALL) {
            boolean allGranted = true;
            for (int res : grantResults) {
                if (res != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false;
                    break;
                }
            }
            if (allGranted) {
                Toast.makeText(this, "All permissions granted! Device hardware is ready.", Toast.LENGTH_SHORT).show();
            }
        }
    }

    private View createHomeDashboardView() {
        ScrollView scrollView = new ScrollView(this);
        scrollView.setFillViewport(true);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(40, 50, 40, 60);

        // 1. Sleek Brand Header Card
        LinearLayout headerCard = new LinearLayout(this);
        headerCard.setOrientation(LinearLayout.VERTICAL);
        headerCard.setPadding(44, 40, 44, 40);
        headerCard.setBackground(makeCardDrawable(Color.parseColor("#0F172A"), 28f, Color.parseColor("#1E293B"), 2));

        LinearLayout titleRow = new LinearLayout(this);
        titleRow.setOrientation(LinearLayout.HORIZONTAL);
        titleRow.setGravity(Gravity.CENTER_VERTICAL);

        TextView starIcon = new TextView(this);
        starIcon.setText("⭐ ");
        starIcon.setTextSize(32f);
        titleRow.addView(starIcon);

        TextView title = new TextView(this);
        title.setText("Star Go");
        title.setTextSize(28f);
        title.setTextColor(Color.parseColor("#38BDF8"));
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        titleRow.addView(title);

        TextView verBadge = new TextView(this);
        verBadge.setText(" v1.0.0 ");
        verBadge.setTextSize(11f);
        verBadge.setTextColor(Color.parseColor("#38BDF8"));
        verBadge.setBackground(makeCardDrawable(Color.parseColor("#1E293B"), 12f, Color.parseColor("#0284C7"), 1));
        verBadge.setPadding(12, 6, 12, 6);
        LinearLayout.LayoutParams verLp = new LinearLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT
        );
        verLp.setMargins(20, 0, 0, 0);
        verBadge.setLayoutParams(verLp);
        titleRow.addView(verBadge);
        headerCard.addView(titleRow);

        TextView subtitle = new TextView(this);
        subtitle.setText("Universal Mobile Companion • Expo Go Architecture");
        subtitle.setTextSize(13f);
        subtitle.setTextColor(Color.parseColor("#94A3B8"));
        subtitle.setPadding(0, 8, 0, 16);
        headerCard.addView(subtitle);

        // Status indicator row
        LinearLayout statusRow = new LinearLayout(this);
        statusRow.setOrientation(LinearLayout.HORIZONTAL);
        statusRow.setGravity(Gravity.CENTER_VERTICAL);

        View statusDot = new View(this);
        statusDot.setBackground(makeCardDrawable(Color.parseColor("#10B981"), 10f, 0, 0));
        statusRow.addView(statusDot, new LinearLayout.LayoutParams(16, 16));

        TextView statusText = new TextView(this);
        statusText.setText(" Star Runtime Engine Ready • Hardware Accelerated");
        statusText.setTextSize(11f);
        statusText.setTextColor(Color.parseColor("#34D399"));
        statusRow.addView(statusText);
        headerCard.addView(statusRow);

        layout.addView(headerCard);

        // Spacer
        View sp1 = new View(this);
        layout.addView(sp1, new LinearLayout.LayoutParams(1, 32));

        // 2. Direct Built-in Showcase Button (Zero setup / Instant demo)
        Button showcaseBtn = new Button(this);
        showcaseBtn.setText("🚀 Launch Built-in Star Showcase");
        showcaseBtn.setTextSize(16f);
        showcaseBtn.setTextColor(Color.WHITE);
        showcaseBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        showcaseBtn.setBackground(makeGradientButton(Color.parseColor("#4F46E5"), Color.parseColor("#7C3AED"), 24f));
        showcaseBtn.setPadding(32, 28, 32, 28);
        showcaseBtn.setOnClickListener(v -> {
            haptic();
            launchBuiltinShowcase();
        });
        layout.addView(showcaseBtn);

        // Spacer
        View sp2 = new View(this);
        layout.addView(sp2, new LinearLayout.LayoutParams(1, 24));

        // 3. QR Code Scan Button
        Button scanBtn = new Button(this);
        scanBtn.setText("📷 Scan Terminal QR Code");
        scanBtn.setTextSize(16f);
        scanBtn.setTextColor(Color.WHITE);
        scanBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        scanBtn.setBackground(makeGradientButton(Color.parseColor("#0284C7"), Color.parseColor("#0369A1"), 24f));
        scanBtn.setPadding(32, 28, 32, 28);
        scanBtn.setOnClickListener(v -> {
            haptic();
            if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_FOR_SCAN);
            } else {
                Intent intent = new Intent(this, QRScannerActivity.class);
                startActivityForResult(intent, REQUEST_QR_SCAN);
            }
        });
        layout.addView(scanBtn);

        // Spacer
        View sp3 = new View(this);
        layout.addView(sp3, new LinearLayout.LayoutParams(1, 24));

        // 4. Physical Hardware Inspector Button
        Button hwBtn = new Button(this);
        hwBtn.setText("⚡ Real Device Hardware Inspector");
        hwBtn.setTextSize(15f);
        hwBtn.setTextColor(Color.WHITE);
        hwBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        hwBtn.setBackground(makeGradientButton(Color.parseColor("#0F766E"), Color.parseColor("#0D9488"), 24f));
        hwBtn.setPadding(32, 26, 32, 26);
        hwBtn.setOnClickListener(v -> {
            haptic();
            Intent hwIntent = new Intent(this, org.starlang.hardware.HardwareInspectorActivity.class);
            startActivity(hwIntent);
        });
        layout.addView(hwBtn);

        // Spacer
        View sp4 = new View(this);
        layout.addView(sp4, new LinearLayout.LayoutParams(1, 24));

        // 5. Hardware Permissions Manager Button
        Button permBtn = new Button(this);
        permBtn.setText("🛡️ Setup Permissions (Camera & Location)");
        permBtn.setTextSize(14f);
        permBtn.setTextColor(Color.WHITE);
        permBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        permBtn.setBackground(makeGradientButton(Color.parseColor("#475569"), Color.parseColor("#334155"), 24f));
        permBtn.setPadding(32, 24, 32, 24);
        permBtn.setOnClickListener(v -> {
            haptic();
            checkAndRequestAllPermissions();
        });
        layout.addView(permBtn);

        // 4. Manual URL Entry Card
        TextView orText = new TextView(this);
        orText.setText("— OR ENTER DEV SERVER ADDRESS —");
        orText.setTextSize(11f);
        orText.setTextColor(Color.parseColor("#64748B"));
        orText.setGravity(Gravity.CENTER);
        orText.setPadding(0, 36, 0, 16);
        layout.addView(orText);

        final EditText urlInput = new EditText(this);
        urlInput.setHint("star://192.168.1.x:8123");
        urlInput.setHintTextColor(Color.parseColor("#475569"));
        urlInput.setTextColor(Color.WHITE);
        urlInput.setBackground(makeCardDrawable(Color.parseColor("#1E293B"), 20f, Color.parseColor("#334155"), 2));
        urlInput.setPadding(36, 26, 36, 26);
        layout.addView(urlInput);

        // Quick Preset Chips (Emulator / LAN / Localhost)
        HorizontalScrollView chipScroll = new HorizontalScrollView(this);
        chipScroll.setHorizontalScrollBarEnabled(false);
        LinearLayout chipLayout = new LinearLayout(this);
        chipLayout.setOrientation(LinearLayout.HORIZONTAL);
        chipLayout.setPadding(0, 16, 0, 16);

        String[] presets = new String[]{
            "star://10.0.2.2:8123",
            "star://192.168.31.2:8123",
            "star://localhost:8123"
        };
        String[] presetLabels = new String[]{
            "📱 Emulator (10.0.2.2)",
            "🌐 LAN (192.168.31.2)",
            "💻 Localhost"
        };

        for (int i = 0; i < presets.length; i++) {
            final String pUrl = presets[i];
            Button chip = new Button(this);
            chip.setText(presetLabels[i]);
            chip.setTextSize(12f);
            chip.setTextColor(Color.parseColor("#38BDF8"));
            chip.setBackground(makeCardDrawable(Color.parseColor("#0F172A"), 16f, Color.parseColor("#0284C7"), 1));
            chip.setPadding(24, 12, 24, 12);
            chip.setOnClickListener(v -> {
                haptic();
                urlInput.setText(pUrl);
                connectToServer(pUrl);
            });
            LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT
            );
            lp.setMargins(0, 0, 16, 0);
            chip.setLayoutParams(lp);
            chipLayout.addView(chip);
        }
        chipScroll.addView(chipLayout);
        layout.addView(chipScroll);

        Button connectBtn = new Button(this);
        connectBtn.setText("⚡ Connect to Server");
        connectBtn.setTextSize(15f);
        connectBtn.setTextColor(Color.WHITE);
        connectBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        connectBtn.setBackground(makeGradientButton(Color.parseColor("#059669"), Color.parseColor("#047857"), 24f));
        connectBtn.setPadding(32, 24, 32, 24);
        connectBtn.setOnClickListener(v -> {
            haptic();
            String url = urlInput.getText().toString().trim();
            if (!url.isEmpty()) {
                connectToServer(url);
            } else {
                Toast.makeText(this, "Please enter dev server URL", Toast.LENGTH_SHORT).show();
            }
        });
        layout.addView(connectBtn);

        // 5. Recent Projects Section
        TextView recentTitle = new TextView(this);
        recentTitle.setText("Recent Connections");
        recentTitle.setTextSize(16f);
        recentTitle.setTextColor(Color.parseColor("#F1F5F9"));
        recentTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        recentTitle.setPadding(0, 40, 0, 16);
        layout.addView(recentTitle);

        Set<String> recents = prefs.getStringSet(KEY_RECENT, new HashSet<>());
        if (recents.isEmpty()) {
            TextView emptyText = new TextView(this);
            emptyText.setText("No recent connections yet. Scan a terminal QR code or launch the built-in showcase!");
            emptyText.setTextSize(12f);
            emptyText.setTextColor(Color.parseColor("#64748B"));
            layout.addView(emptyText);
        } else {
            for (String rUrl : recents) {
                Button rBtn = new Button(this);
                rBtn.setText("🔗 " + rUrl);
                rBtn.setTextSize(13f);
                rBtn.setTextColor(Color.parseColor("#38BDF8"));
                rBtn.setBackground(makeCardDrawable(Color.parseColor("#1E293B"), 18f, Color.parseColor("#334155"), 1));
                rBtn.setPadding(28, 20, 28, 20);
                rBtn.setOnClickListener(v -> {
                    haptic();
                    connectToServer(rUrl);
                });
                LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.WRAP_CONTENT
                );
                lp.setMargins(0, 0, 0, 12);
                rBtn.setLayoutParams(lp);
                layout.addView(rBtn);
            }
        }

        scrollView.addView(layout);
        return scrollView;
    }

    public void launchBuiltinShowcase() {
        byte[] bundle = null;
        try {
            InputStream is = getAssets().open("app.starmobile");
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            byte[] buf = new byte[4096];
            int r;
            while ((r = is.read(buf)) != -1) {
                bos.write(buf, 0, r);
            }
            bundle = bos.toByteArray();
        } catch (Exception ignored) {}

        if (bundle == null || bundle.length == 0) {
            bundle = "STAR_SHOWCASE_DEMO".getBytes();
        }
        launchStarApp(bundle, "star://localhost:showcase");
    }

    public void connectToServer(String rawUrl) {
        final String resolved = rawUrl.trim();
        this.activeServerUrl = resolved;
        saveRecentServer(resolved);

        Toast.makeText(this, "Connecting to " + resolved + "...", Toast.LENGTH_SHORT).show();

        downloader.downloadBundle(resolved, new BundleDownloader.Callback() {
            @Override
            public void onSuccess(byte[] bundleBytes, File cachedFile) {
                launchStarApp(bundleBytes, resolved);
            }

            @Override
            public void onError(String error) {
                Toast.makeText(MainActivity.this, "Connection Error: " + error, Toast.LENGTH_LONG).show();
            }
        });
    }

    private void launchStarApp(byte[] bundleBytes, String serverUrl) {
        Log.i(TAG, "Launching Star Mobile App (" + bundleBytes.length + " bytes)");
        rootContainer.removeAllViews();
        appContainer.removeAllViews();

        DisplayMetrics dm = getResources().getDisplayMetrics();
        StarNativeBridge bridge = new StarNativeBridge();
        bridge.initRuntime("StarGoApp", dm.widthPixels, dm.heightPixels, dm.density);
        bridge.loadBytecode(bundleBytes);

        currentSurfaceView = new StarSurfaceView(this, bridge);
        appContainer.addView(currentSurfaceView);

        if (perfOverlay.isVisible()) {
            perfOverlay.setVisible(true);
        }

        // Add Floating Dev Menu Pill Button (for instant access without shaking)
        Button floatDevBtn = new Button(this);
        floatDevBtn.setText("⚡ Dev Menu");
        floatDevBtn.setTextSize(12f);
        floatDevBtn.setTextColor(Color.WHITE);
        floatDevBtn.setBackground(makeCardDrawable(Color.parseColor("#B30F172A"), 32f, Color.parseColor("#38BDF8"), 2));
        floatDevBtn.setPadding(24, 12, 24, 12);
        floatDevBtn.setOnClickListener(v -> {
            haptic();
            showDevMenu();
        });

        FrameLayout.LayoutParams floatLp = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT,
            ViewGroup.LayoutParams.WRAP_CONTENT,
            Gravity.BOTTOM | Gravity.END
        );
        floatLp.setMargins(0, 0, 36, 160);
        appContainer.addView(floatDevBtn, floatLp);

        rootContainer.addView(appContainer);
        isAppRunning = true;
        Toast.makeText(this, "Running live on Star Go! Shake device or tap 'Dev Menu'.", Toast.LENGTH_SHORT).show();
    }

    public void disconnectToHome() {
        isAppRunning = false;
        activeServerUrl = null;
        rootContainer.removeAllViews();
        homeView = createHomeDashboardView();
        rootContainer.addView(homeView);
    }

    public void reloadApp() {
        if (activeServerUrl != null) {
            connectToServer(activeServerUrl);
        }
    }

    private void saveRecentServer(String url) {
        Set<String> set = new HashSet<>(prefs.getStringSet(KEY_RECENT, new HashSet<>()));
        set.add(url);
        prefs.edit().putStringSet(KEY_RECENT, set).apply();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_QR_SCAN && resultCode == RESULT_OK && data != null) {
            String scannedUrl = data.getStringExtra(QRScannerActivity.EXTRA_SCANNED_URL);
            if (scannedUrl != null && !scannedUrl.isEmpty()) {
                connectToServer(scannedUrl);
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (sensorManager != null && accelerometer != null) {
            sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_UI);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (sensorManager != null) {
            sensorManager.unregisterListener(this);
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];

            float delta = Math.abs(x + y + z - lastX - lastY - lastZ);
            long now = System.currentTimeMillis();

            if (delta > 20 && (now - lastShakeTime > 1500)) {
                lastShakeTime = now;
                if (isAppRunning) {
                    showDevMenu();
                }
            }

            lastX = x;
            lastY = y;
            lastZ = z;
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {}

    private void showDevMenu() {
        DevMenuBottomSheet menu = new DevMenuBottomSheet(this, activeServerUrl, perfOverlay.isVisible(), new DevMenuBottomSheet.DevMenuListener() {
            @Override
            public void onReloadRequested() {
                reloadApp();
            }

            @Override
            public void onTogglePerfMonitor() {
                perfOverlay.setVisible(!perfOverlay.isVisible());
            }

            @Override
            public void onDisconnectRequested() {
                disconnectToHome();
            }
        });
        menu.show();
    }

    @Override
    public void onBackPressed() {
        if (isAppRunning) {
            showDevMenu();
        } else {
            super.onBackPressed();
        }
    }
}
