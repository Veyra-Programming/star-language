# Star Standard Library: ui/popover_box
# Description: Rich contextual popover anchored to a trigger element
# Author: Star Core Team
# Version: 1.0.0

class PopoverBox
    property name = "popover_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PopoverBox>"
    end
end

function create()
    return PopoverBox()
end

function describe()
    return "Rich contextual popover anchored to a trigger element"
end
