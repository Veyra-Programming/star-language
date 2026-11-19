# Star Standard Library: ui/slider_range
# Description: Dual-thumb min/max range slider component
# Author: Star Core Team
# Version: 1.0.0

class SliderRange
    property name = "slider_range"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SliderRange>"
    end
end

function create()
    return SliderRange()
end

function describe()
    return "Dual-thumb min/max range slider component"
end
