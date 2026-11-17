use UI
use Mobile

app MobileTodo

    variable filterDone = false
    variable currentTab = 0

    UI.safe_area(
        UI.column(
            UI.app_bar("Star Mobile Tasks"),

            UI.card(
                UI.row(
                    UI.text("Filter Done"),
                    UI.switch(filterDone, function(checked)
                        filterDone = checked
                    end)
                )
            ),

            UI.scroll_view(
                UI.column(
                    UI.card(UI.text("✓ 1. Design STAR_MOBILE.md")),
                    UI.card(UI.text("✓ 2. Implement Gesture Engine")),
                    UI.card(UI.text("⏳ 3. Android & iOS Runtime Bridges"))
                )
            ),

            UI.bottom_navigation(
                ["Tasks", "Analytics", "Settings"],
                currentTab,
                function(idx)
                    currentTab = idx
                end
            )
        )
    )

end
