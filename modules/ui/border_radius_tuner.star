# Star Standard Library: ui/border_radius_tuner
# Description: Interactive 8-point border radius shaper
# Author: Star Core Team
# Version: 1.0.0

class BorderRadiusTuner
    property name = "border_radius_tuner"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BorderRadiusTuner>"
    end
end

function create()
    return BorderRadiusTuner()
end

function describe()
    return "Interactive 8-point border radius shaper"
end
