"""
Star Android Activity Lifecycle Integration
Authoritative Reference: STAR_ANDROID.md (Section 3)
"""

from typing import Optional, Dict, Any, Callable
from star_sdk.mobile.lifecycle import get_lifecycle, MobileLifecycle, LifecycleState
from star_backend.mobile.lifecycle_bridge import MobileLifecycleBridge
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets


class StarActivity:
    """
    Host activity abstraction managing the Android OS Activity lifecycle,
    window geometry, configuration changes, and hardware back button dispatching.
    """
    def __init__(
        self,
        package_name: str = "org.starlang.app",
        metrics: Optional[ScreenMetrics] = None,
        insets: Optional[SafeAreaInsets] = None,
        lifecycle_bridge: Optional[MobileLifecycleBridge] = None
    ):
        self.package_name = package_name
        self.metrics = metrics or ScreenMetrics(width_dp=390.0, height_dp=844.0, density_scale=2.0)
        self.insets = insets or SafeAreaInsets(top=47.0, bottom=34.0, left=0.0, right=0.0)
        self.lifecycle_bridge = lifecycle_bridge or MobileLifecycleBridge()
        self.is_active: bool = False
        self.state: str = "initialized"

    def on_create(self) -> None:
        self.state = "created"

    def on_start(self) -> None:
        self.state = "started"

    def on_resume(self) -> None:
        self.is_active = True
        self.state = "resumed"
        self.lifecycle_bridge.on_native_resume()

    def on_pause(self) -> None:
        self.is_active = False
        self.state = "paused"
        self.lifecycle_bridge.on_native_pause()

    def on_stop(self) -> None:
        self.state = "stopped"

    def on_destroy(self) -> None:
        self.is_active = False
        self.state = "destroyed"
        self.lifecycle_bridge.on_native_destroy()

    def on_back_pressed(self) -> bool:
        """Dispatches hardware back press. Returns True if consumed by the Star application."""
        return self.lifecycle_bridge.on_native_back_press()

    def on_low_memory(self) -> None:
        self.lifecycle_bridge.on_native_memory_warning()

    def on_configuration_changed(self, new_orientation: str) -> None:
        self.metrics.rotate(new_orientation)

    @classmethod
    def generate_main_activity_java(cls, package_name: str, app_name: str) -> str:
        return f"""package {package_name};

import android.os.Bundle;
import android.app.Activity;
import android.content.res.Configuration;
import android.view.MotionEvent;
import android.view.Window;
import android.view.WindowManager;
import org.starlang.runtime.StarNativeBridge;
import org.starlang.runtime.StarSurfaceView;

public class MainActivity extends Activity {{
    private StarNativeBridge nativeBridge;
    private StarSurfaceView surfaceView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                             WindowManager.LayoutParams.FLAG_FULLSCREEN);

        nativeBridge = new StarNativeBridge();
        surfaceView = new StarSurfaceView(this, nativeBridge);
        setContentView(surfaceView);

        int width = getResources().getDisplayMetrics().widthPixels;
        int height = getResources().getDisplayMetrics().heightPixels;
        float density = getResources().getDisplayMetrics().density;

        nativeBridge.initRuntime("{app_name}", width, height, density);
    }}

    @Override
    protected void onResume() {{
        super.onResume();
        nativeBridge.dispatchLifecycle("resumed");
    }}

    @Override
    protected void onPause() {{
        super.onPause();
        nativeBridge.dispatchLifecycle("paused");
    }}

    @Override
    protected void onDestroy() {{
        super.onDestroy();
        nativeBridge.dispatchLifecycle("detached");
    }}

    @Override
    public void onBackPressed() {{
        boolean consumed = nativeBridge.dispatchBackPress();
        if (!consumed) {{
            super.onBackPressed();
        }}
    }}
}}
"""
