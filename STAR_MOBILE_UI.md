# 📱 STAR MOBILE UI SPECIFICATION & GUIDE
**Specification Version: 0.8.0**  
**Status: Authoritative Standard for Mobile UI Components & Layouts**

---

## 1. Overview

Star Mobile UI extends the universal Star Declarative UI model (`use UI`) with mobile-first abstractions:
- **`UI.safe_area`**: Automatic hardware inset padding for notches, dynamic islands, and home indicator bars.
- **`UI.scroll_view`**: Fluid scrollable container with momentum physics.
- **`UI.app_bar`**: Native-styled mobile navigation header bar.
- **`UI.bottom_navigation`**: Multi-tab bottom navigation controller.
- **`UI.switch`**: Touch-optimized toggle switch with state binding.
- **`UI.slider`**: Continuous value slider.
- **`UI.action_sheet`**: Bottom modal action picker.

All components automatically calculate touch bounding boxes with a **minimum $44 \times 44\text{ dp}$ target** to guarantee accessibility compliance.

---

## 2. Adaptive Unit System

Star layouts automatically resolve responsive units across any device display:

| Unit | Name | Behavior |
| :--- | :--- | :--- |
| `dp` | Density-independent Pixels | Scaled by screen pixel ratio ($1\text{ dp} = 1\text{ px}$ at 160 DPI). |
| `sp` | Scale-independent Pixels | Scaled by device density AND user accessibility font preferences. |
| `%` | Percentage | Fractional proportion of parent container dimensions. |
| `px` | Physical Pixels | Exact hardware screen pixels. |

---

## 3. Component Reference

### 3.1 Safe Area Container
```text
UI.safe_area(
    ...children
)
```
Automatically applies device top/bottom/left/right insets so UI content never clips under hardware cutouts.

### 3.2 Scroll View Container
```text
UI.scroll_view(
    ...children,
    orientation = "vertical"  // "vertical" | "horizontal"
)
```

### 3.3 App Bar
```text
UI.app_bar(
    title: Text,
    leading: StarVirtualNode = nil,
    actions: List[StarVirtualNode] = []
)
```

### 3.4 Bottom Navigation Bar
```text
UI.bottom_navigation(
    items: List[Text],
    selected: Integer,
    onSelect: Function(index)
)
```

### 3.5 Switch & Slider
```text
UI.switch(value: Boolean, onChange: Function(checked))
UI.slider(min: Decimal, max: Decimal, value: Decimal, onChange: Function(newVal))
```

---

## 4. Complete Application Example

```text
use UI
use Mobile

app MobileTodoApp

    variable todos = ["Learn Star", "Build Mobile App", "Ship to Store"]
    variable filterCompleted = false

    UI.safe_area(
        UI.column(
            UI.app_bar("Star Task Manager"),
            
            UI.card(
                UI.row(
                    UI.text("Hide Completed"),
                    UI.switch(filterCompleted, function(checked)
                        filterCompleted = checked
                    end)
                )
            ),

            UI.scroll_view(
                UI.column(
                    UI.card(UI.text("1. " + todos[0])),
                    UI.card(UI.text("2. " + todos[1])),
                    UI.card(UI.text("3. " + todos[2]))
                )
            ),

            UI.bottom_navigation(
                ["Tasks", "Calendar", "Settings"],
                0,
                function(idx)
                    IO.println("Selected tab: " + idx)
                end
            )
        )
    )

end
```
