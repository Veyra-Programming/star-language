# ==============================================================================
# 🌟 Star Programming Language — Natural English Generated Application
# File: examples/natural_english_demo.star
# Input Prompt: "Create a screen titled 'Star Sovereign Station' with an app bar
#               'Command Center', a card for 'Telemetry Mesh' showing '100% Operational',
#               and a button labeled 'Synchronize Node'"
# ==============================================================================

use UI

app UniversalApp

    # 1. State & Reactive Properties
    variable _operating_mode = "OPTIMAL_ONLINE"
    variable _counter = 0
    variable _latency_ms = 0.04

    # 2. Main Interface Header & Navigation
    UI.row(
        UI.title("Star Sovereign Station", 1, { "fg": "#00f0ff" }),
        UI.spacer(),
        UI.badge("STAR v1.3.0", "primary"),
        UI.badge("60 FPS", "success")
    )
    UI.divider()

    # 3. Telemetry & Continuity Cards
    UI.row(
        UI.card(
            UI.badge("CRDT MESH", "accent"),
            UI.title("Telemetry Mesh", 3),
            UI.text("100% Operational", { "fg": "#00ffaa" })
        ),
        UI.card(
            UI.badge("MERKLE WAL", "primary"),
            UI.title("Edge Storage", 3),
            UI.text("4.2 GB Merkle WAL", { "fg": "#00f0ff" })
        )
    )
    UI.divider()

    # 4. Interactive Actions & Event Handlers
    UI.row(
        UI.button("Synchronize Node", function()
            _counter = _counter + 1
            show "Synchronize Node triggered! Counter: " + _counter
        end)
    )

end
