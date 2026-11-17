# 🌟 Star UI 2.1 — Flagship Hardware-Accelerated Animation & Motion Showcase
# Demonstrates 60/120 FPS Easing Curves, Physics Springs, and Modern Widgets

use UI
use Animation
use Theme

component MotionShowcase
    state active_segment = 0
    state count = 42
    state rating_val = 5
    state current_step = 2
    state accordion_open = false
    state modal_open = false
    state celebration = false

    computed counter_label = "Interactive Counter: " + count
    computed celebration_text = "🎉 Total Points: " + (count * 100)

    render
        UI.column(
            # Top Ambient Header with Luminous Glow
            UI.glow("#00f0ff", 20,
                UI.card(
                    UI.row(
                        UI.column(
                            UI.title("🌟 Star Motion Studio", 1),
                            UI.text("Next-Generation 60/120 FPS Fluid Motion Engine")
                        ),
                        UI.spacer(),
                        UI.pulse(
                            0.96, 1.04, 1200,
                            UI.badge("⚡ HARDWARE ACCELERATED", "accent")
                        ),
                        UI.avatar("STAR", 42)
                    )
                )
            ),

            UI.spacer(14),

            # Segmented View Controller
            UI.segmented_control(["Animations", "Physics & Shimmer", "Components", "Live Canvas"], active_segment, function()
                active_segment = (active_segment + 1) % 4
            end),

            UI.spacer(12),

            # Hero Section: Shimmer & Micro-Interactions
            UI.row(
                UI.card(
                    UI.title("Sleek Shimmer & Skeletons", 2),
                    UI.text("Dynamic diagonal sweep placeholder animations for asynchronous states:"),
                    UI.shimmer(380, 28, 8),
                    UI.spacer(8),
                    UI.skeleton(260, 20, 6),
                    UI.spacer(8),
                    UI.row(
                        UI.badge("SPRING PHYSICS", "success"),
                        UI.badge("EASE IN-OUT", "primary"),
                        UI.badge("BOUNCE OUT", "warning")
                    )
                ),
                UI.card(
                    UI.title(counter_label, 2),
                    UI.text("Bouncing interactive counter with fluid spring physics:"),
                    UI.bounce(10.0, 800,
                        UI.progress(count, 100)
                    ),
                    UI.spacer(10),
                    UI.row(
                        UI.button("− Decrement", function()
                            count = count - 5
                        end),
                        UI.button("＋ Increment (+5)", function()
                            count = count + 5
                            celebration = true
                        end)
                    )
                )
            ),

            UI.spacer(14),

            # Interactive Stepper & Rating
            UI.card(
                UI.title("Progress Stepper & Star Rating", 2),
                UI.stepper(["Initialization", "Compile AST", "Bytecode VM", "Render 60 FPS"], current_step),
                UI.spacer(16),
                UI.row(
                    UI.text("Rate Experience:"),
                    UI.rating(rating_val, 5, function()
                        rating_val = (rating_val % 5) + 1
                    end),
                    UI.spacer(),
                    UI.button("Open Modal Dialog", function()
                        modal_open = true
                    end)
                )
            ),

            UI.spacer(12),

            # Collapsible Accordion & Code Block
            UI.accordion("Show Modern Star Language Code", accordion_open, function()
                accordion_open = not accordion_open
            end,
                UI.code_block("use UI\nuse Animation\n\ncomponent App\n    render\n        UI.pulse(0.95, 1.05, 1200,\n            UI.button(\"Launch Rocket\", launch)\n        )\n    end\nend", "star")
            ),

            UI.spacer(10),

            # Ticker Marquee & Celebration
            UI.marquee("⭐ Star UI 2.1 • Zero Dependencies • Universal Web, Desktop, Android & iOS • 60 FPS Certified ⭐", 50),

            # Confetti Celebration Trigger
            UI.confetti(40, celebration)
        )
    end
end

app MotionApp
    MotionShowcase()
end

