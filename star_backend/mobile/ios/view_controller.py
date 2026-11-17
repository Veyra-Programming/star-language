"""
Star iOS UIKit View Controller & Lifecycle Integration
Authoritative Reference: STAR_IOS.md (Section 3)
"""

from typing import Optional, Dict, Any, Callable
from star_sdk.mobile.lifecycle import get_lifecycle, MobileLifecycle, LifecycleState
from star_backend.mobile.lifecycle_bridge import MobileLifecycleBridge
from star_sdk.mobile.dimensions import ScreenMetrics
from star_sdk.mobile.safe_area import SafeAreaInsets


class StarViewController:
    """
    Host view controller abstraction managing UIKit UIViewController lifecycle,
    Dynamic Island / safe-area insets updates, and orientation changes.
    """
    def __init__(
        self,
        app_name: str = "StarApp",
        metrics: Optional[ScreenMetrics] = None,
        insets: Optional[SafeAreaInsets] = None,
        lifecycle_bridge: Optional[MobileLifecycleBridge] = None
    ):
        self.app_name = app_name
        self.metrics = metrics or ScreenMetrics(width_dp=393.0, height_dp=852.0, density_scale=3.0) # iPhone 15/16 Pro baseline
        self.insets = insets or SafeAreaInsets(top=59.0, bottom=34.0, left=0.0, right=0.0) # Dynamic island inset
        self.lifecycle_bridge = lifecycle_bridge or MobileLifecycleBridge()
        self.state: str = "initialized"
        self.is_active: bool = False

    def view_did_load(self) -> None:
        self.state = "loaded"

    def view_did_appear(self) -> None:
        self.state = "resumed"
        self.is_active = True
        self.lifecycle_bridge.on_native_resume()

    def view_did_disappear(self) -> None:
        self.state = "paused"
        self.is_active = False
        self.lifecycle_bridge.on_native_pause()

    def view_will_terminate(self) -> None:
        self.state = "detached"
        self.is_active = False
        self.lifecycle_bridge.on_native_destroy()

    def did_receive_memory_warning(self) -> None:
        self.lifecycle_bridge.on_native_memory_warning()

    def safe_area_insets_did_change(self, top: float, bottom: float, left: float, right: float) -> None:
        self.insets.top = top
        self.insets.bottom = bottom
        self.insets.left = left
        self.insets.right = right

    @classmethod
    def generate_app_delegate_swift(cls, app_name: str) -> str:
        return f"""import UIKit

@main
public class AppDelegate: UIResponder, UIApplicationDelegate {{
    public var window: UIWindow?

    public func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
    ) -> Bool {{
        window = UIWindow(frame: UIScreen.main.bounds)
        let viewController = StarViewController()
        window?.rootViewController = viewController
        window?.makeKeyAndVisible()
        return true
    }}

    public func applicationDidBecomeActive(_ application: UIApplication) {{
        StarNativeBridge.shared.dispatchLifecycle("resumed")
    }}

    public func applicationWillResignActive(_ application: UIApplication) {{
        StarNativeBridge.shared.dispatchLifecycle("paused")
    }}

    public func applicationDidEnterBackground(_ application: UIApplication) {{
        StarNativeBridge.shared.dispatchLifecycle("paused")
    }}

    public func applicationWillTerminate(_ application: UIApplication) {{
        StarNativeBridge.shared.dispatchLifecycle("detached")
    }}
}}
"""

    @classmethod
    def generate_view_controller_swift(cls, app_name: str) -> str:
        return f"""import UIKit
import MetalKit

public class StarViewController: UIViewController {{
    private var metalView: StarMetalView!

    public override func viewDidLoad() {{
        super.viewDidLoad()
        view.backgroundColor = UIColor(red: 0.07, green: 0.07, blue: 0.08, alpha: 1.0)

        let screenSize = UIScreen.main.bounds.size
        let screenScale = Float(UIScreen.main.scale)

        // Initialize StarVM runtime
        StarNativeBridge.shared.initRuntime(
            appName: "{app_name}",
            width: Float(screenSize.width),
            height: Float(screenSize.height),
            scale: screenScale
        )

        // Mount Metal View
        metalView = StarMetalView(frame: view.bounds)
        metalView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(metalView)

        // Load embedded .starmobile bundle
        if let bundleURL = Bundle.main.url(forResource: "app", withExtension: "starmobile"),
           let bundleData = try? Data(contentsOf: bundleURL) {{
            StarNativeBridge.shared.loadBytecode(bundleData)
        }}
    }}

    public override func viewSafeAreaInsetsDidChange() {{
        super.viewSafeAreaInsetsDidChange()
        let insets = view.safeAreaInsets
        StarNativeBridge.shared.setSafeArea(
            top: Float(insets.top),
            bottom: Float(insets.bottom),
            left: Float(insets.left),
            right: Float(insets.right)
        )
    }}

    public override func didReceiveMemoryWarning() {{
        super.didReceiveMemoryWarning()
        StarNativeBridge.shared.dispatchLifecycle("memory_warning")
    }}

    public override var preferredStatusBarStyle: UIStatusBarStyle {{
        return .lightContent
    }}
}}
"""
