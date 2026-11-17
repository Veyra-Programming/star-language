use UI

app StarCounter

    variable count = 0

    UI.column(
        UI.title("🌟 Star Web Counter"),
        UI.card(
            UI.text("Interactive WebAssembly Application"),
            UI.button("Increment Counter", function()
                count = count + 1
            end)
        )
    )

end
