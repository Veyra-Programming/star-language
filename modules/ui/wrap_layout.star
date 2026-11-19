# Star Standard Library: ui/wrap_layout
# Description: Flexible wrap layout that flows children onto new lines
# Author: Star Core Team
# Version: 1.0.0

class WrapLayout
    property name = "wrap_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: WrapLayout>"
    end
end

function create()
    return WrapLayout()
end

function describe()
    return "Flexible wrap layout that flows children onto new lines"
end
