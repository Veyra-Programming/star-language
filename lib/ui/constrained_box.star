# Star Standard Library: ui/constrained_box
# Description: Min/max width and height constraint enforcement box
# Author: Star Core Team
# Version: 1.0.0

class ConstrainedBox
    property name = "constrained_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ConstrainedBox>"
    end
end

function create()
    return ConstrainedBox()
end

function describe()
    return "Min/max width and height constraint enforcement box"
end
