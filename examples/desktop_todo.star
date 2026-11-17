use UI
use Theme

component TodoApp
    state todo_count = 3
    state task_input = ""
    computed status_text = "Total Tasks: " + todo_count

    render
        UI.card(
            UI.title("Star Native Desktop Todo"),
            UI.badge(status_text),
            UI.divider(),
            UI.input("Enter a new task...", function()
                task_input = "New task"
            end),
            UI.button("Add Task", function()
                todo_count = todo_count + 1
            end)
        )
    end
end

app DesktopTodoApp
    TodoApp()
end
