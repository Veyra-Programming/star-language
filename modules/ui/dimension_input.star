# Star Standard Library: ui/dimension_input
# Description: Width, height, depth 3D dimension input with unit toggle
# Author: Star Core Team
# Version: 1.0.0

class DimensionInput
    property name = "dimension_input"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DimensionInput>"
    end
end

function create()
    return DimensionInput()
end

function describe()
    return "Width, height, depth 3D dimension input with unit toggle"
end
