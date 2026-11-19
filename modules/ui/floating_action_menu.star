# Star Standard Library: ui/floating_action_menu
# Description: Expandable floating action button (FAB) speed dial
# Author: Star Core Team
# Version: 1.0.0

class FloatingActionMenu
    property name = "floating_action_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FloatingActionMenu>"
    end
end

function create()
    return FloatingActionMenu()
end

function describe()
    return "Expandable floating action button (FAB) speed dial"
end
