"""
Star Android SurfaceView & Skia/Canvas Renderer
Authoritative Reference: STAR_ANDROID.md (Section 4)
"""

from typing import List, Dict, Any, Optional, Tuple
from star_runtime.mobile.abi import MobileRenderOp
from star_backend.mobile.renderer import IMobileRenderer, MobileDrawCommand


class AndroidSurfaceRenderer(IMobileRenderer):
    """
    Android renderer mapping Star MobileDrawCommands onto Android Canvas / Skia surface.
    """
    def __init__(self, width: float = 390.0, height: float = 844.0):
        self.width = width
        self.height = height
        self.rendered_frames: List[List[MobileDrawCommand]] = []
        self._current_frame: List[MobileDrawCommand] = []
        self._is_rendering: bool = False

    def begin_frame(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self._current_frame = []
        self._is_rendering = True

    def execute_command(self, cmd: MobileDrawCommand) -> None:
        if self._is_rendering:
            self._current_frame.append(cmd)

    def end_frame(self) -> None:
        self.rendered_frames.append(list(self._current_frame))
        self._is_rendering = False

    @classmethod
    def generate_surface_view_java(cls) -> str:
        return """package org.starlang.runtime;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;

public class StarSurfaceView extends SurfaceView implements SurfaceHolder.Callback, Runnable {
    private final StarNativeBridge nativeBridge;
    private SurfaceHolder holder;
    private Thread renderThread;
    private boolean running = false;
    private Paint paint;

    public StarSurfaceView(Context context) {
        this(context, new StarNativeBridge());
    }

    public StarSurfaceView(Context context, StarNativeBridge bridge) {
        super(context);
        this.nativeBridge = bridge;
        this.holder = getHolder();
        this.holder.addCallback(this);
        this.paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        running = true;
        renderThread = new Thread(this);
        renderThread.start();
    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {}

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        running = false;
        try {
            renderThread.join();
        } catch (InterruptedException ignored) {}
    }

    @Override
    public void run() {
        while (running) {
            if (!holder.getSurface().isValid()) continue;
            Canvas canvas = holder.lockCanvas();
            if (canvas != null) {
                // Clear viewport
                canvas.drawColor(Color.parseColor("#121214"));
                
                // Fetch frame command stream from StarVM via JNI
                byte[] commandStream = nativeBridge.renderFrame();
                
                holder.unlockCanvasAndPost(canvas);
            }
            try {
                Thread.sleep(16); // Target ~60 FPS
            } catch (InterruptedException ignored) {}
        }
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        int action = event.getActionMasked();
        int pointerIndex = event.getActionIndex();
        int pointerId = event.getPointerId(pointerIndex);
        float x = event.getX(pointerIndex);
        float y = event.getY(pointerIndex);

        nativeBridge.dispatchTouchEvent(action, pointerId, x, y);
        return true;
    }
}
"""
