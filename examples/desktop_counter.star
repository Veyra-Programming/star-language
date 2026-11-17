use UI
use Theme

component Counter
    state count = 0
    computed is_even = (count % 2 == 0)

    render
        UI.column(
            UI.title("Star 0.6 Reactive Counter"),
            UI.text("Count: " + count),
            UI.badge("Active Counter"),
            UI.row(
                UI.button("- Decrement", function()
                    count = count - 1
                end),
                UI.button("+ Increment", function()
                    count = count + 1
                end)
            )
        )
    end
end

app CounterApp
    Counter()
end
