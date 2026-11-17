use UI
use Mobile

app ResponsiveMobile

    variable width = Mobile.Screen.width_dp()
    variable height = Mobile.Screen.height_dp()
    variable orient = Mobile.Screen.orientation()

    UI.safe_area(
        UI.column(
            UI.app_bar("Adaptive Sizing"),
            UI.card(
                UI.title("Display Metrics"),
                UI.text("Width: " + width + " dp"),
                UI.text("Height: " + height + " dp"),
                UI.text("Orientation: " + orient)
            ),
            UI.button("Rotate Screen", function()
                Mobile.Screen.rotate("toggle")
                width = Mobile.Screen.width_dp()
                height = Mobile.Screen.height_dp()
                orient = Mobile.Screen.orientation()
            end)
        )
    )

end
