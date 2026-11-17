package org.starlang.go;

import android.Manifest;
import android.animation.ObjectAnimator;
import android.animation.ValueAnimator;
import android.app.Activity;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.graphics.ImageFormat;
import android.graphics.SurfaceTexture;
import android.graphics.drawable.GradientDrawable;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraCaptureSession;
import android.hardware.camera2.CameraCharacteristics;
import android.hardware.camera2.CameraDevice;
import android.hardware.camera2.CameraManager;
import android.hardware.camera2.CameraMetadata;
import android.hardware.camera2.CaptureRequest;
import android.hardware.camera2.params.StreamConfigurationMap;
import android.media.Image;
import android.media.ImageReader;
import android.os.Bundle;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.Looper;
import android.os.Vibrator;
import android.util.Log;
import android.util.Size;
import android.view.Gravity;
import android.view.Surface;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.LinearInterpolator;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.zxing.BarcodeFormat;
import com.google.zxing.BinaryBitmap;
import com.google.zxing.DecodeHintType;
import com.google.zxing.PlanarYUVLuminanceSource;
import com.google.zxing.Result;
import com.google.zxing.common.GlobalHistogramBinarizer;
import com.google.zxing.common.HybridBinarizer;
import com.google.zxing.qrcode.QRCodeReader;

import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

/**
 * Real-Device Hardware Camera2 Live QR Scanner Activity.
 * Streams real video onto a TextureView, and processes real-time camera frames
 * via ImageReader (YUV_420_888) with ZXing core decoding.
 * Optimized for terminal screens, dark IDEs, paper printouts, and direct URLs.
 */
public class QRScannerActivity extends Activity {
    private static final String TAG = "StarQRScanner";
    public static final String EXTRA_SCANNED_URL = "extra_scanned_url";
    private static final int REQUEST_CAMERA_PERMISSION = 301;

    // Camera2 Subsystem
    private TextureView textureView;
    private CameraDevice cameraDevice;
    private CameraCaptureSession captureSession;
    private CaptureRequest.Builder previewRequestBuilder;
    private Size previewSize;
    private Size scanSize;
    private String cameraId;
    private CameraCharacteristics cameraCharacteristics;
    private int sensorOrientation = 90;
    private HandlerThread backgroundThread;
    private Handler backgroundHandler;
    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private ImageReader imageReader;
    private boolean isTorchOn = false;

    // ZXing Live Video Frame Decoder
    private final QRCodeReader qrCodeReader = new QRCodeReader();
    private final Map<DecodeHintType, Object> decodeHints = new HashMap<>();
    private volatile boolean isScanning = true;
    private volatile boolean isDecoding = false;
    private long lastFrameProcessedTime = 0;
    private Vibrator vibrator;

    // UI Elements
    private FrameLayout rootFrame;
    private LinearLayout permWarningLayout;
    private Button torchBtn;
    private TextView scanStatusText;
    private ObjectAnimator laserAnimator;
    private EditText directInput;

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

        // Configure ZXing Hints for high accuracy & inverted screens (terminal screens)
        decodeHints.put(DecodeHintType.TRY_HARDER, Boolean.TRUE);
        decodeHints.put(DecodeHintType.ALSO_INVERTED, Boolean.TRUE);
        decodeHints.put(DecodeHintType.POSSIBLE_FORMATS, Collections.singletonList(BarcodeFormat.QR_CODE));

        try {
            vibrator = (Vibrator) getSystemService(Context.VIBRATOR_SERVICE);
        } catch (Exception ignored) {}

        rootFrame = new FrameLayout(this);
        rootFrame.setBackgroundColor(Color.parseColor("#090D16"));

        // 1. Fullscreen Live Camera View (TextureView)
        textureView = new TextureView(this);
        FrameLayout.LayoutParams tvLp = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT
        );
        textureView.setLayoutParams(tvLp);
        rootFrame.addView(textureView);

        // 2. Dark Translucent Mask with Center Transparent Viewfinder
        View darkMask = new View(this);
        darkMask.setBackgroundColor(Color.parseColor("#33000000"));
        rootFrame.addView(darkMask, new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT
        ));

        // 3. Top Header Bar (Back, Title, Flashlight Toggle)
        LinearLayout headerBar = createHeaderBar();
        FrameLayout.LayoutParams headerLp = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
        );
        headerLp.gravity = Gravity.TOP;
        headerLp.setMargins(24, 48, 24, 0);
        rootFrame.addView(headerBar, headerLp);

        // 4. Center Scanning Viewfinder Frame with Animated Laser Reticle
        FrameLayout reticleContainer = createReticleView();
        FrameLayout.LayoutParams reticleLp = new FrameLayout.LayoutParams(620, 620);
        reticleLp.gravity = Gravity.CENTER;
        reticleLp.setMargins(0, -60, 0, 0);
        rootFrame.addView(reticleContainer, reticleLp);

        // 5. Bottom Controls & Direct Link Panel
        View bottomControls = createBottomControls();
        FrameLayout.LayoutParams bottomLp = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT
        );
        bottomLp.gravity = Gravity.BOTTOM;
        rootFrame.addView(bottomControls, bottomLp);

        // 6. Permission Missing Alert View (shown if camera is denied)
        permWarningLayout = createPermissionWarningView();
        rootFrame.addView(permWarningLayout);

        setContentView(rootFrame);

        // Check Camera Permission
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            permWarningLayout.setVisibility(View.VISIBLE);
            requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION);
        } else {
            permWarningLayout.setVisibility(View.GONE);
        }
    }

    private LinearLayout createHeaderBar() {
        LinearLayout bar = new LinearLayout(this);
        bar.setOrientation(LinearLayout.HORIZONTAL);
        bar.setGravity(Gravity.CENTER_VERTICAL);
        bar.setPadding(16, 16, 16, 16);
        bar.setBackground(makeCard(Color.parseColor("#CC0F172A"), 32f, Color.parseColor("#334155"), 2));

        Button backBtn = new Button(this);
        backBtn.setText("←");
        backBtn.setTextSize(20f);
        backBtn.setTextColor(Color.WHITE);
        backBtn.setBackground(makeCard(Color.TRANSPARENT, 0, 0, 0));
        backBtn.setOnClickListener(v -> finish());
        bar.addView(backBtn, new LinearLayout.LayoutParams(120, 100));

        TextView title = new TextView(this);
        title.setText("📷 Live QR Scanner");
        title.setTextSize(17f);
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        title.setTextColor(Color.parseColor("#38BDF8"));
        LinearLayout.LayoutParams tLp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1.0f);
        title.setLayoutParams(tLp);
        bar.addView(title);

        torchBtn = new Button(this);
        torchBtn.setText("🔦 Flash");
        torchBtn.setTextSize(12f);
        torchBtn.setTextColor(Color.WHITE);
        torchBtn.setBackground(makeCard(Color.parseColor("#1E293B"), 20f, Color.parseColor("#64748B"), 1));
        torchBtn.setPadding(20, 8, 20, 8);
        torchBtn.setOnClickListener(v -> toggleTorch());
        bar.addView(torchBtn);

        return bar;
    }

    private FrameLayout createReticleView() {
        FrameLayout box = new FrameLayout(this);
        box.setBackground(makeCard(Color.parseColor("#1000F0FF"), 36f, Color.parseColor("#00F0FF"), 4));

        View laser = new View(this);
        laser.setBackgroundColor(Color.parseColor("#00F0FF"));
        FrameLayout.LayoutParams laserLp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 6);
        laserLp.setMargins(16, 20, 16, 0);
        laser.setLayoutParams(laserLp);
        box.addView(laser);

        laserAnimator = ObjectAnimator.ofFloat(laser, "translationY", 0f, 540f);
        laserAnimator.setDuration(1800);
        laserAnimator.setRepeatMode(ValueAnimator.REVERSE);
        laserAnimator.setRepeatCount(ValueAnimator.INFINITE);
        laserAnimator.setInterpolator(new LinearInterpolator());
        laserAnimator.start();

        scanStatusText = new TextView(this);
        scanStatusText.setText("⚡ Aligning Terminal QR...");
        scanStatusText.setTextSize(12f);
        scanStatusText.setTextColor(Color.parseColor("#38BDF8"));
        scanStatusText.setGravity(Gravity.CENTER);
        scanStatusText.setBackground(makeCard(Color.parseColor("#AA090D16"), 16f, Color.TRANSPARENT, 0));
        scanStatusText.setPadding(24, 8, 24, 8);
        FrameLayout.LayoutParams stLp = new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT
        );
        stLp.gravity = Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL;
        stLp.setMargins(0, 0, 0, 24);
        box.addView(scanStatusText, stLp);

        return box;
    }

    private View createBottomControls() {
        LinearLayout bottomPanel = new LinearLayout(this);
        bottomPanel.setOrientation(LinearLayout.VERTICAL);
        bottomPanel.setPadding(36, 24, 36, 36);
        bottomPanel.setBackground(makeCard(Color.parseColor("#EE0B1120"), 36f, Color.parseColor("#1E293B"), 2));

        TextView tip = new TextView(this);
        tip.setText("Point camera at your terminal screen QR code");
        tip.setTextSize(13f);
        tip.setTextColor(Color.parseColor("#94A3B8"));
        tip.setGravity(Gravity.CENTER);
        tip.setPadding(0, 0, 0, 16);
        bottomPanel.addView(tip);

        directInput = new EditText(this);
        directInput.setHint("star://192.168.31.2:8123");
        directInput.setText("star://192.168.31.2:8123");
        directInput.setHintTextColor(Color.parseColor("#475569"));
        directInput.setTextColor(Color.WHITE);
        directInput.setTextSize(14f);
        directInput.setBackground(makeCard(Color.parseColor("#1E293B"), 20f, Color.parseColor("#334155"), 2));
        directInput.setPadding(32, 20, 32, 20);
        bottomPanel.addView(directInput);

        LinearLayout btnRow = new LinearLayout(this);
        btnRow.setOrientation(LinearLayout.HORIZONTAL);
        btnRow.setPadding(0, 14, 0, 0);

        Button pasteBtn = new Button(this);
        pasteBtn.setText("📋 Paste");
        pasteBtn.setTextSize(13f);
        pasteBtn.setTextColor(Color.parseColor("#38BDF8"));
        pasteBtn.setBackground(makeCard(Color.parseColor("#0F172A"), 20f, Color.parseColor("#0284C7"), 1));
        pasteBtn.setOnClickListener(v -> {
            try {
                ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                if (cm != null && cm.hasPrimaryClip() && cm.getPrimaryClip().getItemCount() > 0) {
                    CharSequence clip = cm.getPrimaryClip().getItemAt(0).getText();
                    if (clip != null) {
                        directInput.setText(clip.toString());
                        Toast.makeText(this, "Pasted URL: " + clip, Toast.LENGTH_SHORT).show();
                    }
                }
            } catch (Exception e) {
                Toast.makeText(this, "Clipboard unavailable", Toast.LENGTH_SHORT).show();
            }
        });
        LinearLayout.LayoutParams pLp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1.0f);
        pLp.setMargins(0, 0, 12, 0);
        btnRow.addView(pasteBtn, pLp);

        Button connectBtn = new Button(this);
        connectBtn.setText("⚡ Load Build");
        connectBtn.setTextSize(14f);
        connectBtn.setTextColor(Color.WHITE);
        connectBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        connectBtn.setBackground(makeGradientBtn(Color.parseColor("#2563EB"), Color.parseColor("#1D4ED8"), 20f));
        connectBtn.setOnClickListener(v -> {
            String url = directInput.getText().toString().trim();
            if (url.isEmpty()) {
                url = "star://192.168.31.2:8123";
            }
            returnScannedUrl(url);
        });
        LinearLayout.LayoutParams cLp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1.5f);
        btnRow.addView(connectBtn, cLp);

        bottomPanel.addView(btnRow);

        return bottomPanel;
    }

    private LinearLayout createPermissionWarningView() {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setGravity(Gravity.CENTER);
        layout.setBackgroundColor(Color.parseColor("#EE0B1120"));
        layout.setPadding(48, 48, 48, 48);
        layout.setLayoutParams(new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT
        ));

        TextView icon = new TextView(this);
        icon.setText("📷");
        icon.setTextSize(54f);
        icon.setGravity(Gravity.CENTER);
        layout.addView(icon);

        TextView title = new TextView(this);
        title.setText("Camera Permission Required");
        title.setTextSize(20f);
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        title.setTextColor(Color.WHITE);
        title.setGravity(Gravity.CENTER);
        title.setPadding(0, 16, 0, 12);
        layout.addView(title);

        TextView desc = new TextView(this);
        desc.setText("To scan live QR codes directly from your computer screen, Star Go needs access to your device's camera.");
        desc.setTextSize(14f);
        desc.setTextColor(Color.parseColor("#94A3B8"));
        desc.setGravity(Gravity.CENTER);
        desc.setPadding(0, 0, 0, 32);
        layout.addView(desc);

        Button grantBtn = new Button(this);
        grantBtn.setText("🔐 Allow Camera Permission");
        grantBtn.setTextSize(15f);
        grantBtn.setTextColor(Color.WHITE);
        grantBtn.setTypeface(null, android.graphics.Typeface.BOLD);
        grantBtn.setBackground(makeGradientBtn(Color.parseColor("#0284C7"), Color.parseColor("#0369A1"), 24f));
        grantBtn.setPadding(32, 24, 32, 24);
        grantBtn.setOnClickListener(v -> {
            requestPermissions(new String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION);
        });
        layout.addView(grantBtn);

        return layout;
    }

    private void returnScannedUrl(String url) {
        isScanning = false;
        Intent result = new Intent();
        result.putExtra(EXTRA_SCANNED_URL, url);
        setResult(RESULT_OK, result);
        finish();
    }

    // =========================================================================
    // Real-Time Hardware Camera Frame QR Code Decoding Loop (ImageReader YUV)
    // =========================================================================

    private final ImageReader.OnImageAvailableListener onImageAvailableListener = new ImageReader.OnImageAvailableListener() {
        @Override
        public void onImageAvailable(ImageReader reader) {
            Image image = null;
            try {
                image = reader.acquireLatestImage();
                if (image == null || !isScanning || isDecoding) {
                    return;
                }

                // Throttle to ~8 FPS to prevent CPU thrashing
                long now = System.currentTimeMillis();
                if (now - lastFrameProcessedTime < 120) {
                    return;
                }
                lastFrameProcessedTime = now;
                isDecoding = true;

                processYuvFrame(image);

            } catch (Exception e) {
                Log.e(TAG, "Error acquiring camera frame", e);
            } finally {
                if (image != null) {
                    image.close();
                }
                isDecoding = false;
            }
        }
    };

    /**
     * Decode Y-channel luminance buffer directly with ZXing without Bitmap conversions.
     */
    private void processYuvFrame(Image image) {
        try {
            Image.Plane yPlane = image.getPlanes()[0];
            ByteBuffer buffer = yPlane.getBuffer();
            int width = image.getWidth();
            int height = image.getHeight();
            int rowStride = yPlane.getRowStride();

            byte[] yData;
            if (rowStride == width) {
                yData = new byte[buffer.remaining()];
                buffer.get(yData);
            } else {
                // Copy row by row to eliminate stride padding
                yData = new byte[width * height];
                int pos = 0;
                byte[] row = new byte[rowStride];
                for (int r = 0; r < height; r++) {
                    int toRead = Math.min(rowStride, buffer.remaining());
                    buffer.get(row, 0, toRead);
                    System.arraycopy(row, 0, yData, pos, width);
                    pos += width;
                }
            }

            // Sensor is landscape (e.g. 1280x720) with 90 deg rotation; rotate to portrait (720x1280)
            byte[] portraitY = rotateYUV90(yData, width, height);
            int pWidth = height;
            int pHeight = width;

            // Crop central 80% to align with screen viewfinder reticle
            int cropDim = Math.min(pWidth, pHeight) * 4 / 5;
            int cropX = Math.max(0, (pWidth - cropDim) / 2);
            int cropY = Math.max(0, (pHeight - cropDim) / 2);

            PlanarYUVLuminanceSource source = new PlanarYUVLuminanceSource(
                portraitY, pWidth, pHeight,
                cropX, cropY, cropDim, cropDim,
                false
            );

            Result result = decodeLuminance(source);

            // Fallback: decode full uncropped frame if reticle crop missed
            if (result == null) {
                PlanarYUVLuminanceSource fullSource = new PlanarYUVLuminanceSource(
                    portraitY, pWidth, pHeight,
                    0, 0, pWidth, pHeight,
                    false
                );
                result = decodeLuminance(fullSource);
            }

            // Fallback 2: decode unrotated landscape source (if phone tilted horizontally)
            if (result == null) {
                PlanarYUVLuminanceSource unrotatedSource = new PlanarYUVLuminanceSource(
                    yData, width, height,
                    0, 0, width, height,
                    false
                );
                result = decodeLuminance(unrotatedSource);
            }

            if (result != null && result.getText() != null) {
                final String text = result.getText().trim();
                Log.i(TAG, "⚡ Real QR Code successfully decoded: " + text);
                isScanning = false;
                runOnUiThread(() -> onQrCodeDetected(text));
            }

        } catch (Exception e) {
            Log.e(TAG, "Exception during YUV frame processing", e);
        }
    }

    /**
     * Tries HybridBinarizer, GlobalHistogramBinarizer, and inverted binarizers.
     */
    private Result decodeLuminance(PlanarYUVLuminanceSource source) {
        Result result = null;

        // 1. HybridBinarizer (Standard lighting)
        try {
            BinaryBitmap bb = new BinaryBitmap(new HybridBinarizer(source));
            result = qrCodeReader.decode(bb, decodeHints);
            if (result != null) return result;
        } catch (Exception ignored) {
        } finally {
            qrCodeReader.reset();
        }

        // 2. GlobalHistogramBinarizer (Terminal screens & computer monitors)
        try {
            BinaryBitmap bb = new BinaryBitmap(new GlobalHistogramBinarizer(source));
            result = qrCodeReader.decode(bb, decodeHints);
            if (result != null) return result;
        } catch (Exception ignored) {
        } finally {
            qrCodeReader.reset();
        }

        // 3. Inverted Luminance Source (White on black terminal text)
        try {
            BinaryBitmap bb = new BinaryBitmap(new GlobalHistogramBinarizer(source.invert()));
            result = qrCodeReader.decode(bb, decodeHints);
            if (result != null) return result;
        } catch (Exception ignored) {
        } finally {
            qrCodeReader.reset();
        }

        return null;
    }

    /**
     * Fast clockwise 90 degree rotation of grayscale byte buffer.
     */
    private static byte[] rotateYUV90(byte[] src, int width, int height) {
        byte[] dest = new byte[width * height];
        int i = 0;
        for (int x = 0; x < width; x++) {
            for (int y = height - 1; y >= 0; y--) {
                dest[i++] = src[y * width + x];
            }
        }
        return dest;
    }

    private void onQrCodeDetected(final String url) {
        if (vibrator != null) {
            try {
                vibrator.vibrate(60);
            } catch (Exception ignored) {}
        }
        if (scanStatusText != null) {
            scanStatusText.setText("✅ QR Code Detected!");
            scanStatusText.setTextColor(Color.parseColor("#10B981"));
        }
        Toast.makeText(this, "⚡ Scanned: " + url, Toast.LENGTH_SHORT).show();
        returnScannedUrl(url);
    }

    // ==========================================
    // Camera2 Subsystem Lifecycle
    // ==========================================

    private final TextureView.SurfaceTextureListener surfaceTextureListener = new TextureView.SurfaceTextureListener() {
        @Override
        public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
            safeOpenCamera();
        }

        @Override
        public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {}

        @Override
        public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
            return true;
        }

        @Override
        public void onSurfaceTextureUpdated(SurfaceTexture surface) {}
    };

    private final CameraDevice.StateCallback stateCallback = new CameraDevice.StateCallback() {
        @Override
        public void onOpened(CameraDevice camera) {
            cameraDevice = camera;
            createCameraPreviewSession();
        }

        @Override
        public void onDisconnected(CameraDevice camera) {
            camera.close();
            cameraDevice = null;
        }

        @Override
        public void onError(CameraDevice camera, int error) {
            camera.close();
            cameraDevice = null;
            Log.e(TAG, "Camera device error: " + error);
        }
    };

    private Size chooseOptimalPreviewSize(Size[] choices, int targetMaxW, int targetMaxH) {
        if (choices == null || choices.length == 0) return new Size(1280, 720);
        Size best = null;
        for (Size s : choices) {
            if (s.getWidth() <= targetMaxW && s.getHeight() <= targetMaxH) {
                if (best == null || (s.getWidth() * s.getHeight() > best.getWidth() * best.getHeight())) {
                    best = s;
                }
            }
        }
        return best != null ? best : choices[0];
    }

    private void safeOpenCamera() {
        if (!hasWindowFocus()) {
            // Postpone until window has gained foreground focus to avoid CAMERA_DISABLED (1)
            mainHandler.postDelayed(this::safeOpenCamera, 150);
            return;
        }
        openCamera();
    }

    private void openCamera() {
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            return;
        }
        if (cameraDevice != null) {
            return;
        }

        final CameraManager manager = (CameraManager) getSystemService(Context.CAMERA_SERVICE);
        if (manager == null) return;

        try {
            String selectedId = null;
            for (String id : manager.getCameraIdList()) {
                CameraCharacteristics chars = manager.getCameraCharacteristics(id);
                Integer facing = chars.get(CameraCharacteristics.LENS_FACING);
                if (facing != null && facing == CameraCharacteristics.LENS_FACING_BACK) {
                    selectedId = id;
                    cameraCharacteristics = chars;
                    break;
                }
            }
            if (selectedId == null && manager.getCameraIdList().length > 0) {
                selectedId = manager.getCameraIdList()[0];
                cameraCharacteristics = manager.getCameraCharacteristics(selectedId);
            }

            if (selectedId != null) {
                cameraId = selectedId;

                Integer sensorOrient = cameraCharacteristics.get(CameraCharacteristics.SENSOR_ORIENTATION);
                if (sensorOrient != null) {
                    sensorOrientation = sensorOrient;
                }

                StreamConfigurationMap map = cameraCharacteristics.get(CameraCharacteristics.SCALER_STREAM_CONFIGURATION_MAP);
                if (map != null) {
                    Size[] sizes = map.getOutputSizes(SurfaceTexture.class);
                    previewSize = chooseOptimalPreviewSize(sizes, 1920, 1080);
                    Log.i(TAG, "Selected preview size: " + previewSize.getWidth() + "x" + previewSize.getHeight());

                    Size[] yuvSizes = map.getOutputSizes(ImageFormat.YUV_420_888);
                    scanSize = chooseOptimalPreviewSize(yuvSizes, 1280, 720);
                    Log.i(TAG, "Selected scan frame size: " + scanSize.getWidth() + "x" + scanSize.getHeight());
                } else {
                    previewSize = new Size(1280, 720);
                    scanSize = new Size(1280, 720);
                }

                // Ensure torch is off before opening camera
                try {
                    manager.setTorchMode(cameraId, false);
                } catch (Exception ignored) {}

                // Prepare hardware ImageReader for real-time QR decoding
                if (imageReader != null) {
                    imageReader.close();
                }
                imageReader = ImageReader.newInstance(
                    scanSize.getWidth(), scanSize.getHeight(), ImageFormat.YUV_420_888, 2
                );
                imageReader.setOnImageAvailableListener(onImageAvailableListener, backgroundHandler);

                manager.openCamera(cameraId, stateCallback, backgroundHandler);
            }
        } catch (CameraAccessException e) {
            Log.e(TAG, "CameraAccessException opening camera, retrying...", e);
            mainHandler.postDelayed(this::safeOpenCamera, 300);
        } catch (SecurityException e) {
            Log.e(TAG, "SecurityException opening camera", e);
        }
    }

    private void createCameraPreviewSession() {
        if (cameraDevice == null || !textureView.isAvailable() || previewSize == null || imageReader == null) {
            return;
        }

        try {
            SurfaceTexture texture = textureView.getSurfaceTexture();
            texture.setDefaultBufferSize(previewSize.getWidth(), previewSize.getHeight());
            Surface previewSurface = new Surface(texture);
            Surface scanSurface = imageReader.getSurface();

            previewRequestBuilder = cameraDevice.createCaptureRequest(CameraDevice.TEMPLATE_PREVIEW);
            previewRequestBuilder.addTarget(previewSurface);
            previewRequestBuilder.addTarget(scanSurface);
            previewRequestBuilder.set(CaptureRequest.CONTROL_AF_MODE, CaptureRequest.CONTROL_AF_MODE_CONTINUOUS_PICTURE);
            previewRequestBuilder.set(CaptureRequest.CONTROL_MODE, CameraMetadata.CONTROL_MODE_AUTO);

            cameraDevice.createCaptureSession(
                Arrays.asList(previewSurface, scanSurface),
                new CameraCaptureSession.StateCallback() {
                    @Override
                    public void onConfigured(CameraCaptureSession session) {
                        if (cameraDevice == null) return;
                        captureSession = session;
                        try {
                            captureSession.setRepeatingRequest(previewRequestBuilder.build(), null, backgroundHandler);
                            Log.i(TAG, "Camera preview session live with continuous ImageReader stream!");
                        } catch (Exception e) {
                            Log.e(TAG, "Failed to start camera preview repeating request", e);
                        }
                    }

                    @Override
                    public void onConfigureFailed(CameraCaptureSession session) {
                        Log.e(TAG, "Camera session configuration failed");
                    }
                },
                backgroundHandler
            );
        } catch (Exception e) {
            Log.e(TAG, "Error configuring camera preview session", e);
        }
    }

    private void toggleTorch() {
        if (previewRequestBuilder == null || captureSession == null) {
            Toast.makeText(this, "Camera not ready for torch", Toast.LENGTH_SHORT).show();
            return;
        }

        try {
            isTorchOn = !isTorchOn;
            previewRequestBuilder.set(
                CaptureRequest.FLASH_MODE,
                isTorchOn ? CaptureRequest.FLASH_MODE_TORCH : CaptureRequest.FLASH_MODE_OFF
            );
            captureSession.setRepeatingRequest(previewRequestBuilder.build(), null, backgroundHandler);
            torchBtn.setText(isTorchOn ? "🔦 Flash ON" : "🔦 Flash");
            torchBtn.setBackground(makeCard(
                isTorchOn ? Color.parseColor("#F59E0B") : Color.parseColor("#1E293B"),
                20f,
                Color.parseColor("#64748B"),
                1
            ));
        } catch (Exception e) {
            Log.e(TAG, "Torch toggle error", e);
        }
    }

    private void closeCamera() {
        if (captureSession != null) {
            try {
                captureSession.close();
            } catch (Exception ignored) {}
            captureSession = null;
        }
        if (cameraDevice != null) {
            try {
                cameraDevice.close();
            } catch (Exception ignored) {}
            cameraDevice = null;
        }
        if (imageReader != null) {
            try {
                imageReader.close();
            } catch (Exception ignored) {}
            imageReader = null;
        }
    }

    private void startBackgroundThread() {
        backgroundThread = new HandlerThread("CameraBackground");
        backgroundThread.start();
        backgroundHandler = new Handler(backgroundThread.getLooper());
    }

    private void stopBackgroundThread() {
        if (backgroundThread != null) {
            backgroundThread.quitSafely();
            try {
                backgroundThread.join();
                backgroundThread = null;
                backgroundHandler = null;
            } catch (InterruptedException e) {
                Log.e(TAG, "Error stopping background thread", e);
            }
        }
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus && cameraDevice == null && textureView != null && textureView.isAvailable()) {
            openCamera();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        isScanning = true;
        if (backgroundThread == null) {
            startBackgroundThread();
        }
        if (textureView.isAvailable()) {
            safeOpenCamera();
        } else {
            textureView.setSurfaceTextureListener(surfaceTextureListener);
        }
        if (laserAnimator != null && !laserAnimator.isStarted()) {
            laserAnimator.start();
        }
    }

    @Override
    protected void onPause() {
        isScanning = false;
        closeCamera();
        if (laserAnimator != null) {
            laserAnimator.cancel();
        }
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        isScanning = false;
        stopBackgroundThread();
        super.onDestroy();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CAMERA_PERMISSION) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                permWarningLayout.setVisibility(View.GONE);
                if (textureView.isAvailable()) {
                    safeOpenCamera();
                } else {
                    textureView.setSurfaceTextureListener(surfaceTextureListener);
                }
            } else {
                permWarningLayout.setVisibility(View.VISIBLE);
                Toast.makeText(this, "Camera permission is needed for live scanning", Toast.LENGTH_LONG).show();
            }
        }
    }
}
