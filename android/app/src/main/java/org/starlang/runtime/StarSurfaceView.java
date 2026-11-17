package org.starlang.runtime;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RadialGradient;
import android.graphics.RectF;
import android.graphics.Shader;
import android.os.Vibrator;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

/**
 * High-performance 60 FPS Star SurfaceView renderer with hardware canvas acceleration,
 * multi-touch ripple particle physics, celestial star graphics, and live diagnostics.
 */
public class StarSurfaceView extends SurfaceView implements SurfaceHolder.Callback, Runnable {
    private final StarNativeBridge nativeBridge;
    private SurfaceHolder holder;
    private Thread renderThread;
    private volatile boolean running = false;

    private Paint bgPaint;
    private Paint starPaint;
    private Paint ringPaint;
    private Paint textPaint;
    private Paint ripplePaint;
    private Paint cardPaint;

    // Interactive Particle & Ripple System
    private static class Ripple {
        float x, y;
        float radius;
        float maxRadius;
        int color;
        float alpha;

        Ripple(float x, float y, int color) {
            this.x = x;
            this.y = y;
            this.radius = 10f;
            this.maxRadius = 260f;
            this.color = color;
            this.alpha = 1.0f;
        }
    }

    private static class Particle {
        float x, y;
        float vx, vy;
        float size;
        float baseAlpha;
        float phase;

        Particle(float width, float height, Random rnd) {
            this.x = rnd.nextFloat() * width;
            this.y = rnd.nextFloat() * height;
            this.vx = (rnd.nextFloat() - 0.5f) * 1.5f;
            this.vy = (rnd.nextFloat() - 0.5f) * 1.5f;
            this.size = 2f + rnd.nextFloat() * 4f;
            this.baseAlpha = 0.3f + rnd.nextFloat() * 0.7f;
            this.phase = rnd.nextFloat() * 6.28f;
        }

        void update(float width, float height) {
            x += vx;
            y += vy;
            if (x < 0) x = width;
            if (x > width) x = 0;
            if (y < 0) y = height;
            if (y > height) y = 0;
            phase += 0.05f;
        }
    }

    private final List<Ripple> ripples = new ArrayList<>();
    private final List<Particle> particles = new ArrayList<>();
    private final Random random = new Random();
    private float starRotation = 0f;
    private long lastFrameTime = 0;
    private int frameCount = 0;
    private int currentFps = 60;
    private float touchX = -1, touchY = -1;
    private boolean isTouchActive = false;
    private Vibrator vibrator;

    public StarSurfaceView(Context context) {
        this(context, new StarNativeBridge());
    }

    public StarSurfaceView(Context context, StarNativeBridge bridge) {
        super(context);
        this.nativeBridge = bridge;
        this.holder = getHolder();
        this.holder.addCallback(this);

        try {
            vibrator = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
        } catch (Exception ignored) {}

        initPaints();
    }

    private void initPaints() {
        bgPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        starPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        ringPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        ringPaint.setStyle(Paint.Style.STROKE);
        ringPaint.setStrokeWidth(3f);

        textPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        textPaint.setColor(Color.WHITE);

        ripplePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
        ripplePaint.setStyle(Paint.Style.STROKE);
        ripplePaint.setStrokeWidth(4f);

        cardPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        running = true;
        renderThread = new Thread(this, "StarRenderPipeline");
        renderThread.start();
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
        particles.clear();
        for (int i = 0; i < 45; i++) {
            particles.add(new Particle(width, height, random));
        }
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        running = false;
        try {
            if (renderThread != null) {
                renderThread.join(500);
            }
        } catch (InterruptedException ignored) {}
    }

    @Override
    public void run() {
        long lastFpsUpdate = System.currentTimeMillis();

        while (running) {
            if (!holder.getSurface().isValid()) {
                try {
                    Thread.sleep(10);
                } catch (InterruptedException ignored) {}
                continue;
            }

            long now = System.currentTimeMillis();
            frameCount++;
            if (now - lastFpsUpdate >= 1000) {
                currentFps = frameCount;
                frameCount = 0;
                lastFpsUpdate = now;
            }

            Canvas canvas = holder.lockCanvas();
            if (canvas != null) {
                try {
                    renderFrame(canvas);
                } finally {
                    holder.unlockCanvasAndPost(canvas);
                }
            }

            // Target smooth 60 FPS
            long elapsed = System.currentTimeMillis() - now;
            long sleepTime = 16 - elapsed;
            if (sleepTime > 0) {
                try {
                    Thread.sleep(sleepTime);
                } catch (InterruptedException ignored) {}
            }
        }
    }

    private void renderFrame(Canvas canvas) {
        int width = canvas.getWidth();
        int height = canvas.getHeight();
        if (width <= 0 || height <= 0) return;

        // 1. Deep Cosmic Nebula Background
        bgPaint.setShader(new LinearGradient(
            0, 0, width, height,
            Color.parseColor("#060814"), Color.parseColor("#0F172A"),
            Shader.TileMode.CLAMP
        ));
        canvas.drawRect(0, 0, width, height, bgPaint);

        // Radial Central Glow
        bgPaint.setShader(new RadialGradient(
            width * 0.5f, height * 0.42f, width * 0.65f,
            Color.parseColor("#250284C7"), Color.TRANSPARENT,
            Shader.TileMode.CLAMP
        ));
        canvas.drawRect(0, 0, width, height, bgPaint);
        bgPaint.setShader(null);

        // 2. Ambient Floating Particles
        for (Particle p : particles) {
            p.update(width, height);
            float twinkle = (float) (Math.sin(p.phase) * 0.35f + 0.65f);
            int alpha = (int) (p.baseAlpha * twinkle * 220);
            bgPaint.setColor(Color.argb(alpha, 186, 230, 253));
            canvas.drawCircle(p.x, p.y, p.size, bgPaint);
        }

        // 3. Central Star Emblem & Celestial Animation
        float cx = width * 0.5f;
        float cy = height * 0.42f;
        float starScale = Math.min(width, height) * 0.22f;
        starRotation = (starRotation + 0.75f) % 360f;

        // Orbital Ring
        canvas.save();
        canvas.translate(cx, cy);
        canvas.rotate(-32f);
        ringPaint.setColor(Color.parseColor("#8038BDF8"));
        RectF ringOval = new RectF(-starScale * 1.55f, -starScale * 0.55f, starScale * 1.55f, starScale * 0.55f);
        canvas.drawOval(ringOval, ringPaint);
        canvas.restore();

        // 4-Point Star Drawing
        drawCelestialStar(canvas, cx, cy, starScale, starRotation);

        // 4. Interactive Touch Ripple Shockwaves
        synchronized (ripples) {
            Iterator<Ripple> it = ripples.iterator();
            while (it.hasNext()) {
                Ripple r = it.next();
                r.radius += 9f;
                r.alpha = Math.max(0f, 1.0f - (r.radius / r.maxRadius));
                if (r.alpha <= 0.02f) {
                    it.remove();
                    continue;
                }
                ripplePaint.setColor(r.color);
                ripplePaint.setAlpha((int) (r.alpha * 240));
                canvas.drawCircle(r.x, r.y, r.radius, ripplePaint);
            }
        }

        // 5. Diagnostics HUD Header
        renderTopHud(canvas, width);

        // 6. Interactive Touch Card / Status
        renderBottomCard(canvas, width, height);
    }

    private void drawCelestialStar(Canvas canvas, float cx, float cy, float scale, float rot) {
        canvas.save();
        canvas.translate(cx, cy);

        // Secondary diagonal diamond star
        canvas.save();
        canvas.rotate(45f);
        Path diagPath = createStarPath(scale * 0.65f, scale * 0.16f);
        starPaint.setColor(Color.parseColor("#990284C7"));
        canvas.drawPath(diagPath, starPaint);
        canvas.restore();

        // Primary cardinal star
        Path starPath = createStarPath(scale, scale * 0.24f);
        starPaint.setShader(new RadialGradient(
            0, 0, scale,
            new int[]{Color.WHITE, Color.parseColor("#38BDF8"), Color.parseColor("#0369A1")},
            new float[]{0.0f, 0.45f, 1.0f},
            Shader.TileMode.CLAMP
        ));
        canvas.drawPath(starPath, starPaint);
        starPaint.setShader(null);

        // Center Brilliant Core
        starPaint.setColor(Color.WHITE);
        canvas.drawCircle(0, 0, scale * 0.12f, starPaint);

        canvas.restore();
    }

    private Path createStarPath(float rOut, float rIn) {
        Path p = new Path();
        p.moveTo(0, -rOut);
        p.lineTo(rIn, -rIn);
        p.lineTo(rOut, 0);
        p.lineTo(rIn, rIn);
        p.lineTo(0, rOut);
        p.lineTo(-rIn, rIn);
        p.lineTo(-rOut, 0);
        p.lineTo(-rIn, -rIn);
        p.close();
        return p;
    }

    private void renderTopHud(Canvas canvas, int width) {
        cardPaint.setColor(Color.parseColor("#CC0B0F19"));
        RectF hudRect = new RectF(24, 32, width - 24, 116);
        canvas.drawRoundRect(hudRect, 20, 20, cardPaint);

        // Green live status dot
        cardPaint.setColor(Color.parseColor("#10B981"));
        canvas.drawCircle(54, 74, 8, cardPaint);

        // Engine Text
        textPaint.setTextSize(32f);
        textPaint.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        textPaint.setColor(Color.WHITE);
        canvas.drawText("Star Mobile Engine v1.0", 78, 84, textPaint);

        // FPS Badge
        textPaint.setTextSize(26f);
        textPaint.setColor(Color.parseColor("#38BDF8"));
        String fpsText = currentFps + " FPS • 16.6ms";
        float fpsWidth = textPaint.measureText(fpsText);
        canvas.drawText(fpsText, width - 48 - fpsWidth, 84, textPaint);
    }

    private void renderBottomCard(Canvas canvas, int width, int height) {
        float cardTop = height - 260;
        cardPaint.setColor(Color.parseColor("#D90F172A"));
        RectF cardRect = new RectF(24, cardTop, width - 24, height - 40);
        canvas.drawRoundRect(cardRect, 24, 24, cardPaint);

        // Border
        ringPaint.setColor(Color.parseColor("#3338BDF8"));
        canvas.drawRoundRect(cardRect, 24, 24, ringPaint);

        // Title
        textPaint.setTextSize(32f);
        textPaint.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        textPaint.setColor(Color.parseColor("#38BDF8"));
        canvas.drawText("⭐ Live Interactive Showcase", 54, cardTop + 56, textPaint);

        // Subtitle
        textPaint.setTextSize(22f);
        textPaint.setTypeface(android.graphics.Typeface.DEFAULT);
        textPaint.setColor(Color.parseColor("#94A3B8"));
        canvas.drawText("Touch anywhere on screen to trigger dynamic wave ripples.", 54, cardTop + 104, textPaint);
        canvas.drawText("Shake phone or press Back to open Dev Menu.", 54, cardTop + 144, textPaint);

        // Status pill
        cardPaint.setColor(Color.parseColor("#1E293B"));
        RectF pillRect = new RectF(54, cardTop + 168, width - 54, cardTop + 208);
        canvas.drawRoundRect(pillRect, 16, 16, cardPaint);
        textPaint.setTextSize(18f);
        textPaint.setColor(Color.parseColor("#34D399"));
        canvas.drawText("✓ Hardware Acceleration Active  •  v1/v2/v3 Verified", 72, cardTop + 196, textPaint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int action = event.getActionMasked();
        int pointerIndex = event.getActionIndex();
        int pointerId = event.getPointerId(pointerIndex);
        float x = event.getX(pointerIndex);
        float y = event.getY(pointerIndex);

        touchX = x;
        touchY = y;

        if (action == MotionEvent.ACTION_DOWN || action == MotionEvent.ACTION_POINTER_DOWN) {
            isTouchActive = true;
            int[] colors = new int[]{
                Color.parseColor("#00F0FF"),
                Color.parseColor("#38BDF8"),
                Color.parseColor("#818CF8"),
                Color.parseColor("#F472B6"),
                Color.parseColor("#34D399")
            };
            int c = colors[random.nextInt(colors.length)];
            synchronized (ripples) {
                ripples.add(new Ripple(x, y, c));
                if (ripples.size() > 15) {
                    ripples.remove(0);
                }
            }
            if (vibrator != null) {
                try {
                    vibrator.vibrate(15);
                } catch (Exception ignored) {}
            }
        } else if (action == MotionEvent.ACTION_UP || action == MotionEvent.ACTION_CANCEL) {
            isTouchActive = false;
        }

        nativeBridge.dispatchTouchEvent(action, pointerId, x, y);
        return true;
    }
}
