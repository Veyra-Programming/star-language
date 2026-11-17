package org.starlang.hardware;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.BroadcastReceiver;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.hardware.camera2.CameraManager;
import android.net.ConnectivityManager;
import android.net.NetworkCapabilities;
import android.os.BatteryManager;
import android.os.Build;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.os.VibratorManager;
import android.util.DisplayMetrics;
import android.view.WindowManager;

/**
 * Enterprise Android Hardware Level Bridge.
 * Controls real device physical components: Haptics, Sensors, Torch, Battery,
 * Display Refresh Rate, Memory, CPU Architecture, and Connectivity.
 */
public class AndroidHardwareManager implements SensorEventListener {
    private static AndroidHardwareManager instance;

    private final Context context;
    private final SensorManager sensorManager;
    private final CameraManager cameraManager;
    private final BatteryManager batteryManager;
    private final ConnectivityManager connectivityManager;
    private final ActivityManager activityManager;
    private final ClipboardManager clipboardManager;
    private Vibrator vibrator;

    // Live Sensor Cache
    public float accelX = 0f, accelY = 0f, accelZ = 9.8f;
    public float gyroX = 0f, gyroY = 0f, gyroZ = 0f;
    public float ambientLux = 0f;
    public float proximityCm = 0f;

    private boolean isTorchOn = false;
    private String backCameraId = null;
    private boolean sensorsRegistered = false;

    public interface SensorListener {
        void onSensorUpdate(float ax, float ay, float az, float gx, float gy, float gz, float lux);
    }
    private SensorListener sensorListener;

    public static synchronized AndroidHardwareManager getInstance(Context context) {
        if (instance == null) {
            instance = new AndroidHardwareManager(context.getApplicationContext());
        }
        return instance;
    }

    private AndroidHardwareManager(Context ctx) {
        this.context = ctx;
        this.sensorManager = (SensorManager) ctx.getSystemService(Context.SENSOR_SERVICE);
        this.cameraManager = (CameraManager) ctx.getSystemService(Context.CAMERA_SERVICE);
        this.batteryManager = (BatteryManager) ctx.getSystemService(Context.BATTERY_SERVICE);
        this.connectivityManager = (ConnectivityManager) ctx.getSystemService(Context.CONNECTIVITY_SERVICE);
        this.activityManager = (ActivityManager) ctx.getSystemService(Context.ACTIVITY_SERVICE);
        this.clipboardManager = (ClipboardManager) ctx.getSystemService(Context.CLIPBOARD_SERVICE);

        initVibrator();
        initCamera();
    }

    private void initVibrator() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                VibratorManager vm = (VibratorManager) context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE);
                if (vm != null) {
                    vibrator = vm.getDefaultVibrator();
                }
            }
            if (vibrator == null) {
                vibrator = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
            }
        } catch (Exception ignored) {}
    }

    private void initCamera() {
        try {
            if (cameraManager != null) {
                for (String id : cameraManager.getCameraIdList()) {
                    // Usually "0" is the primary back camera with LED flash
                    backCameraId = id;
                    break;
                }
            }
        } catch (Exception ignored) {}
    }

    // =========================================================================
    // 1. REAL HAPTIC & VIBRATION PATTERNS
    // =========================================================================

    public void vibrateTick() {
        if (vibrator == null || !vibrator.hasVibrator()) return;
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                vibrator.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_TICK));
            } else {
                vibrator.vibrate(10);
            }
        } catch (Exception e) {
            vibrator.vibrate(10);
        }
    }

    public void vibrateClick() {
        if (vibrator == null || !vibrator.hasVibrator()) return;
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                vibrator.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK));
            } else {
                vibrator.vibrate(20);
            }
        } catch (Exception e) {
            vibrator.vibrate(20);
        }
    }

    public void vibrateHeavy() {
        if (vibrator == null || !vibrator.hasVibrator()) return;
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                vibrator.vibrate(VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK));
            } else {
                vibrator.vibrate(50);
            }
        } catch (Exception e) {
            vibrator.vibrate(50);
        }
    }

    public void vibrateSuccess() {
        if (vibrator == null || !vibrator.hasVibrator()) return;
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                long[] timings = new long[]{0, 25, 40, 35};
                int[] amplitudes = new int[]{0, 160, 0, 255};
                vibrator.vibrate(VibrationEffect.createWaveform(timings, amplitudes, -1));
            } else {
                vibrator.vibrate(new long[]{0, 25, 40, 35}, -1);
            }
        } catch (Exception e) {
            vibrator.vibrate(40);
        }
    }

    public void vibrateError() {
        if (vibrator == null || !vibrator.hasVibrator()) return;
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                long[] timings = new long[]{0, 50, 40, 50, 40, 70};
                int[] amplitudes = new int[]{0, 255, 0, 255, 0, 255};
                vibrator.vibrate(VibrationEffect.createWaveform(timings, amplitudes, -1));
            } else {
                vibrator.vibrate(new long[]{0, 50, 40, 50, 40, 70}, -1);
            }
        } catch (Exception e) {
            vibrator.vibrate(80);
        }
    }

    // =========================================================================
    // 2. REAL HARDWARE FLASHLIGHT / TORCH
    // =========================================================================

    public boolean toggleTorch() {
        return setTorchMode(!isTorchOn);
    }

    public boolean setTorchMode(boolean enable) {
        if (cameraManager == null || backCameraId == null) return false;
        try {
            cameraManager.setTorchMode(backCameraId, enable);
            isTorchOn = enable;
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isTorchActive() {
        return isTorchOn;
    }

    // =========================================================================
    // 3. SENSORS (ACCELEROMETER, GYROSCOPE, LIGHT, PROXIMITY)
    // =========================================================================

    public void startSensors(SensorListener listener) {
        this.sensorListener = listener;
        if (sensorManager == null || sensorsRegistered) return;

        Sensor accel = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        if (accel != null) sensorManager.registerListener(this, accel, SensorManager.SENSOR_DELAY_UI);

        Sensor gyro = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        if (gyro != null) sensorManager.registerListener(this, gyro, SensorManager.SENSOR_DELAY_UI);

        Sensor light = sensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
        if (light != null) sensorManager.registerListener(this, light, SensorManager.SENSOR_DELAY_UI);

        Sensor prox = sensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
        if (prox != null) sensorManager.registerListener(this, prox, SensorManager.SENSOR_DELAY_UI);

        sensorsRegistered = true;
    }

    public void stopSensors() {
        if (sensorManager != null && sensorsRegistered) {
            sensorManager.unregisterListener(this);
            sensorsRegistered = false;
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        int type = event.sensor.getType();
        if (type == Sensor.TYPE_ACCELEROMETER) {
            accelX = event.values[0];
            accelY = event.values[1];
            accelZ = event.values[2];
        } else if (type == Sensor.TYPE_GYROSCOPE) {
            gyroX = event.values[0];
            gyroY = event.values[1];
            gyroZ = event.values[2];
        } else if (type == Sensor.TYPE_LIGHT) {
            ambientLux = event.values[0];
        } else if (type == Sensor.TYPE_PROXIMITY) {
            proximityCm = event.values[0];
        }

        if (sensorListener != null) {
            sensorListener.onSensorUpdate(accelX, accelY, accelZ, gyroX, gyroY, gyroZ, ambientLux);
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {}

    // =========================================================================
    // 4. BATTERY & POWER TELEMETRY
    // =========================================================================

    public int getBatteryPercentage() {
        try {
            if (batteryManager != null) {
                return batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);
            }
            IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
            Intent bStatus = context.registerReceiver(null, ifilter);
            if (bStatus != null) {
                int level = bStatus.getIntExtra(BatteryManager.EXTRA_LEVEL, -1);
                int scale = bStatus.getIntExtra(BatteryManager.EXTRA_SCALE, -1);
                if (level >= 0 && scale > 0) {
                    return (int) ((level / (float) scale) * 100);
                }
            }
        } catch (Exception ignored) {}
        return 100;
    }

    public boolean isBatteryCharging() {
        try {
            IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
            Intent bStatus = context.registerReceiver(null, ifilter);
            if (bStatus != null) {
                int status = bStatus.getIntExtra(BatteryManager.EXTRA_STATUS, -1);
                return status == BatteryManager.BATTERY_STATUS_CHARGING ||
                       status == BatteryManager.BATTERY_STATUS_FULL;
            }
        } catch (Exception ignored) {}
        return false;
    }

    public float getBatteryTemperatureCelsius() {
        try {
            IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
            Intent bStatus = context.registerReceiver(null, ifilter);
            if (bStatus != null) {
                int temp = bStatus.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0);
                return temp / 10.0f; // in tenths of a degree Celsius
            }
        } catch (Exception ignored) {}
        return 28.0f;
    }

    public String getChargingPlugType() {
        try {
            IntentFilter ifilter = new IntentFilter(Intent.ACTION_BATTERY_CHANGED);
            Intent bStatus = context.registerReceiver(null, ifilter);
            if (bStatus != null) {
                int chargePlug = bStatus.getIntExtra(BatteryManager.EXTRA_PLUGGED, -1);
                if (chargePlug == BatteryManager.BATTERY_PLUGGED_USB) return "USB Fast Charge";
                if (chargePlug == BatteryManager.BATTERY_PLUGGED_AC) return "AC SuperCharge";
                if (chargePlug == BatteryManager.BATTERY_PLUGGED_WIRELESS) return "Wireless Fast Charge";
            }
        } catch (Exception ignored) {}
        return "Discharging (Battery)";
    }

    // =========================================================================
    // 5. DEVICE & SYSTEM METRICS
    // =========================================================================

    public String getDeviceModel() {
        return Build.MANUFACTURER.toUpperCase() + " " + Build.MODEL;
    }

    public String getCpuArchitecture() {
        if (Build.SUPPORTED_ABIS != null && Build.SUPPORTED_ABIS.length > 0) {
            return Build.SUPPORTED_ABIS[0];
        }
        return Build.CPU_ABI;
    }

    public String getAndroidVersion() {
        return "Android " + Build.VERSION.RELEASE + " (API " + Build.VERSION.SDK_INT + ")";
    }

    public long getTotalMemoryMB() {
        try {
            ActivityManager.MemoryInfo mi = new ActivityManager.MemoryInfo();
            if (activityManager != null) {
                activityManager.getMemoryInfo(mi);
                return mi.totalMem / (1024 * 1024);
            }
        } catch (Exception ignored) {}
        return 8192;
    }

    public long getAvailableMemoryMB() {
        try {
            ActivityManager.MemoryInfo mi = new ActivityManager.MemoryInfo();
            if (activityManager != null) {
                activityManager.getMemoryInfo(mi);
                return mi.availMem / (1024 * 1024);
            }
        } catch (Exception ignored) {}
        return 4096;
    }

    public float getDisplayRefreshRate(Activity activity) {
        try {
            if (activity != null) {
                return activity.getWindowManager().getDefaultDisplay().getRefreshRate();
            }
        } catch (Exception ignored) {}
        return 120.0f;
    }

    public void setKeepScreenOn(Activity activity, boolean keepOn) {
        try {
            if (activity != null) {
                if (keepOn) {
                    activity.getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                } else {
                    activity.getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                }
            }
        } catch (Exception ignored) {}
    }

    // =========================================================================
    // 6. NETWORK & CONNECTIVITY
    // =========================================================================

    public String getNetworkType() {
        try {
            if (connectivityManager != null) {
                android.net.Network net = connectivityManager.getActiveNetwork();
                if (net != null) {
                    NetworkCapabilities caps = connectivityManager.getNetworkCapabilities(net);
                    if (caps != null) {
                        if (caps.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) {
                            return "Wi-Fi (High-Speed)";
                        } else if (caps.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR)) {
                            return "5G NR / LTE Cellular";
                        } else if (caps.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)) {
                            return "Ethernet";
                        }
                    }
                }
            }
        } catch (Exception ignored) {}
        return "Offline / Disconnected";
    }

    public boolean isConnected() {
        try {
            if (connectivityManager != null) {
                android.net.Network net = connectivityManager.getActiveNetwork();
                return net != null;
            }
        } catch (Exception ignored) {}
        return false;
    }

    // =========================================================================
    // 7. CLIPBOARD
    // =========================================================================

    public void copyToClipboard(String text) {
        try {
            if (clipboardManager != null) {
                ClipData clip = ClipData.newPlainText("Star Language", text);
                clipboardManager.setPrimaryClip(clip);
            }
        } catch (Exception ignored) {}
    }

    public String pasteFromClipboard() {
        try {
            if (clipboardManager != null && clipboardManager.hasPrimaryClip()) {
                ClipData clip = clipboardManager.getPrimaryClip();
                if (clip != null && clip.getItemCount() > 0) {
                    CharSequence cs = clip.getItemAt(0).getText();
                    return cs != null ? cs.toString() : "";
                }
            }
        } catch (Exception ignored) {}
        return "";
    }
}

