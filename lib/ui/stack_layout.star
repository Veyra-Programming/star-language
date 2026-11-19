# Star Standard Library: ui/stack_layout
# Description: Layered Z-index overlapping stack container
# Author: Star Core Team
# Version: 1.0.0

class StackLayout
    property name = "stack_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StackLayout>"
    end
end

function create()
    return StackLayout()
end

function describe()
    return "Layered Z-index overlapping stack container"
end
