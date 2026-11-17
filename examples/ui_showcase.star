# 🌟 Star Language Universal UI Showcase
# Demonstrates pure Star declarative UI rendering across Desktop, Terminal, and Mobile

use UI
use Theme

component Dashboard
    state active_tab = 0
    state refresh_count = 1
    state notifications_enabled = true
    state performance_val = 60
    state hardware_accel = true
    
    computed status_badge = "System Active · Build #" + refresh_count
    computed revenue_text = "$" + (124000 + (refresh_count * 1500))
    computed users_text = "" + (14820 + (refresh_count * 240))

    render
        UI.column(
            # Top Navigation Bar & App Header
            UI.row(
                UI.column(
                    UI.title("🌟 Star Studio Enterprise"),
                    UI.text("Next-Generation Cross-Platform UI Engine")
                ),
                UI.spacer(),
                UI.badge("● LIVE CLOUD", "success"),
                UI.avatar("AK", 38)
            ),

            UI.divider(),

            # Navigation Tabs
            UI.tabs(["Overview", "Analytics", "Infrastructure", "Settings"], active_tab, function()
                active_tab = (active_tab + 1) % 4
            end),

            UI.divider(),

            # KPI Metrics Cards (Multi-Column Grid)
            UI.grid(
                3,
                UI.card(
                    UI.row(
                        UI.text("Total Revenue"),
                        UI.spacer(),
                        UI.badge("+18.4%", "success")
                    ),
                    UI.title(revenue_text),
                    UI.progress(78, 100)
                ),
                UI.card(
                    UI.row(
                        UI.text("Active Sessions"),
                        UI.spacer(),
                        UI.badge("Realtime", "accent")
                    ),
                    UI.title(users_text),
                    UI.progress(62, 100)
                ),
                UI.card(
                    UI.row(
                        UI.text("Frame Budget"),
                        UI.spacer(),
                        UI.badge("60 FPS", "primary")
                    ),
                    UI.title(performance_val + " FPS"),
                    UI.progress(performance_val, 120)
                )
            ),

            # Interactive Control Center
            UI.card(
                UI.title("🎛 Control Center & Runtime Parameters"),
                UI.text("Interact with reactive state controls below:"),
                UI.divider(),
                
                UI.row(
                    UI.text("Hardware WebGPU Acceleration"),
                    UI.spacer(),
                    UI.checkbox("Enabled", hardware_accel, function()
                        hardware_accel = not hardware_accel
                    end)
                ),

                UI.row(
                    UI.text("Live Cloud Notifications"),
                    UI.spacer(),
                    UI.switch(notifications_enabled, function()
                        notifications_enabled = not notifications_enabled
                    end)
                ),

                UI.row(
                    UI.text("GPU Frame Rate Target"),
                    UI.spacer(),
                    UI.slider(performance_val, 30, 120, function()
                        performance_val = 120
                    end)
                ),

                UI.divider(),

                UI.row(
                    UI.button("↻ Refresh Analytics", function()
                        refresh_count = refresh_count + 1
                    end),
                    UI.button("⚡ Fast Sync", function()
                        refresh_count = refresh_count + 5
                    end),
                    UI.spacer(),
                    UI.badge(status_badge, "primary")
                )
            ),

            # Status Banner & Toast
            UI.toast("Cross-platform layout verified: Desktop Native, WebGPU & Terminal ANSI conformant.", "info")
        )
    end
end

app ShowcaseApp
    Dashboard()
end
