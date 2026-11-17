use UI
use Mobile

app HelloMobile

    UI.safe_area(
        UI.column(
            UI.app_bar("🌟 Star Mobile"),
            UI.card(
                UI.title("Welcome to Star Mobile"),
                UI.text("Native Android & iOS from One Star Codebase."),
                UI.badge("Star 0.8", "primary")
            ),
            UI.button("Get Started", function()
                IO.println("Get Started tapped!")
            end)
        )
    )

end
