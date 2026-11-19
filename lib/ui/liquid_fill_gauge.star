# Star Standard Library: ui/liquid_fill_gauge
# Description: Animated wave liquid fill water droplet gauge
# Author: Star Core Team
# Version: 1.0.0

class LiquidFillGauge
    property name = "liquid_fill_gauge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: LiquidFillGauge>"
    end
end

function create()
    return LiquidFillGauge()
end

function describe()
    return "Animated wave liquid fill water droplet gauge"
end
