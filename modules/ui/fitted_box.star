# Star Standard Library: ui/fitted_box
# Description: Container that scales and fits child widget proportionally
# Author: Star Core Team
# Version: 1.0.0

class FittedBox
    property name = "fitted_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FittedBox>"
    end
end

function create()
    return FittedBox()
end

function describe()
    return "Container that scales and fits child widget proportionally"
end
