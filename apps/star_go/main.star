# 🌟 Star Go — Universal Mobile Companion (Expo Go Architecture)
# Tests Android & iOS applications live over WiFi with Terminal QR Code Scanning

use UI
use Animation
use Mobile

component StarGoApp
    state server_url = "star://192.168.1.15:8088"
    state scan_modal_open = false
    state perf_hud_active = true
    state is_connected = false
    state connected_app_name = "ui_motion_showcase"
    state frame_rate = 60

    render
        UI.column(
            # Top Ambient Glow Header
            UI.glow("#00f0ff", 22,
                UI.card(
                    UI.row(
                        UI.column(
                            UI.title("⭐ Star Go", 1),
                            UI.text("Universal Live Dev Companion • Expo Go Architecture")
                        ),
                        UI.spacer(),
                        UI.pulse(0.95, 1.05, 1000,
                            UI.badge("● LIVE DEV", "success")
                        )
                    )
                )
            ),

            UI.spacer(14),

            # Primary QR Scan Action Hero
            UI.card(
                UI.title("📱 Connect to Development Server", 2),
                UI.text("Scan the QR code displayed in your terminal by running 'star go':"),
                UI.spacer(10),
                UI.row(
                    UI.bounce(8.0, 900,
                        UI.button("📷 Scan Terminal QR Code", function()
                            scan_modal_open = true
                            Mobile.Vibrate()
                        end)
                    ),
                    UI.spacer(10),
                    UI.button("⚡ Fast Connect", function()
                        is_connected = true
                        Mobile.Vibrate()
                    end)
                )
            ),

            UI.spacer(12),

            # Manual URL Entry
            UI.card(
                UI.title("🔗 Manual Server Address", 2),
                UI.row(
                    UI.badge("URL", "primary"),
                    UI.text(server_url),
                    UI.spacer(),
                    UI.button("Edit", function()
                        server_url = "star://192.168.31.2:8088"
                    end)
                )
            ),

            UI.spacer(12),

            # Performance HUD & Dev Tools
            UI.card(
                UI.row(
                    UI.column(
                        UI.title("⚡ Performance HUD & Live State", 3),
                        UI.text("Real-time GPU surface rendering telemetry:")
                    ),
                    UI.spacer(),
                    UI.segmented_control(["HUD On", "HUD Off"], 0, function()
                        perf_hud_active = not perf_hud_active
                    end)
                ),
                UI.spacer(8),
                UI.row(
                    UI.badge("TARGET: 60.0 FPS", "success"),
                    UI.badge("FRAME: 12.4 ms", "accent"),
                    UI.badge("SPRING PHYSICS: ACTIVE", "warning"),
                    UI.badge("FAST REFRESH: ON", "primary")
                )
            ),

            UI.spacer(12),

            # Recent Projects List
            UI.card(
                UI.title("Recent Development Projects", 2),
                UI.row(
                    UI.column(
                        UI.title("🌟 Motion & Animation Showcase", 3),
                        UI.text("star://192.168.31.2:8088 • Last synced 2m ago")
                    ),
                    UI.spacer(),
                    UI.button("Re-connect", function()
                        is_connected = true
                    end)
                ),
                UI.spacer(8),
                UI.row(
                    UI.column(
                        UI.title("🛒 Flutter E-Commerce Demo", 3),
                        UI.text("star://192.168.31.2:8089 • Last synced 1h ago")
                    ),
                    UI.spacer(),
                    UI.button("Re-connect", function()
                        is_connected = true
                    end)
                )
            ),

            UI.spacer(12),

            # Shake Hint Drawer / Footer
            UI.card(
                UI.row(
                    UI.badge("PRO TIP", "warning"),
                    UI.text("💡 Shake your device or press 'm' in terminal to toggle the Developer Menu.")
                )
            ),

            # Camera Viewfinder Modal
            UI.modal(
                "📷 Camera QR Scanner Viewfinder",
                "Point your camera lens at the QR code printed in the 'star go' terminal to connect instantly over LAN.",
                scan_modal_open,
                function()
                    scan_modal_open = false
                    is_connected = true
                end,
                function()
                    scan_modal_open = false
                end
            )
        )
    end
end

app StarGo
    StarGoApp()
end
