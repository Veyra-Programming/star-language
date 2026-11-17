use UI
use Mobile

app HardwareBenchmark
    variable frame_count = 0
    variable toggle_active = true
    variable slider_val = 50.0

    UI.safe_area(
        UI.app_bar("Star Hardware Benchmark"),
        UI.scroll_view(
            UI.card(
                UI.title("60 FPS Stress Benchmark"),
                UI.text("Frame Counter: " + frame_count),
                UI.button("Increment Frames", function()
                    frame_count = frame_count + 1
                    Mobile.Haptics.impact("light")
                end)
            ),
            UI.card(
                UI.title("Interactive Controls"),
                UI.switch(toggle_active, function(val)
                    toggle_active = val
                end),
                UI.slider(slider_val, 0.0, 100.0, function(val)
                    slider_val = val
                end)
            ),
            UI.card(
                UI.title("Device Sensors"),
                UI.text("Battery: " + Mobile.Battery.level()),
                UI.text("Orientation: " + Mobile.Screen.orientation()),
                UI.text("Network: " + Mobile.Network.status())
            )
        ),
        UI.bottom_navigation(
            UI.button("Dashboard", None),
            UI.button("Metrics", None),
            UI.button("Settings", None)
        )
    )
end
