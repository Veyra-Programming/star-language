# Star Standard Library: ui/context_menu
# Description: Right-click contextual popup menu with divider groups
# Author: Star Core Team
# Version: 1.0.0

class ContextMenu
    property name = "context_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ContextMenu>"
    end
end

function create()
    return ContextMenu()
end

function describe()
    return "Right-click contextual popup menu with divider groups"
end
