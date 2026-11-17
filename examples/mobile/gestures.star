use UI
use Mobile

app GestureExplorer

    variable status = "Perform any gesture (Tap, Swipe, Pan, DoubleTap, Pinch)"

    UI.safe_area(
        UI.column(
            UI.app_bar("Touch & Gesture Lab"),
            UI.card(
                UI.title("Interactive Surface"),
                UI.text(status)
            ),
            UI.row(
                UI.button("Simulate Tap", function()
                    status = "Tapped at center"
                end),
                UI.button("Simulate Swipe", function()
                    status = "Swiped Left (Velocity: 0.8 dp/ms)"
                end)
            )
        )
    )

end
