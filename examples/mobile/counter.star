use UI
use Mobile

app MobileCounter

    variable count = 0

    UI.safe_area(
        UI.column(
            UI.app_bar("Mobile Counter"),
            UI.card(
                UI.title("Taps & Haptics"),
                UI.text("Current Count: " + count),
                UI.row(
                    UI.button("- Decrement", function()
                        count = count - 1
                        Mobile.Vibrate()
                    end),
                    UI.button("+ Increment", function()
                        count = count + 1
                        Mobile.Vibrate()
                    end)
                )
            )
        )
    )

end
