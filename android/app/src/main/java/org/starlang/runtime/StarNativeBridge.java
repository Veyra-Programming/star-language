package org.starlang.runtime;

public class StarNativeBridge {
    static {
        System.loadLibrary("starnative");
    }

    public native boolean initRuntime(String appName, int width, int height, float density);
    public native boolean loadBytecode(byte[] bytecode);
    public native void dispatchTouchEvent(int phase, int pointerId, float x, float y);
    public native byte[] renderFrame();
    public native void dispatchLifecycle(String state);
    public native boolean dispatchBackPress();
}
