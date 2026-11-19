# Star Standard Library: ui/collapsible_menu
# Description: Nested multi-level dropdown menu tree
# Author: Star Core Team
# Version: 1.0.0

class CollapsibleMenu
    property name = "collapsible_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CollapsibleMenu>"
    end
end

function create()
    return CollapsibleMenu()
end

function describe()
    return "Nested multi-level dropdown menu tree"
end
