# Star Standard Library: ui/range_gauge
# Description: Min-max range gauge with colored safe/warning/critical zones
# Author: Star Core Team
# Version: 1.0.0

class RangeGauge
    property name = "range_gauge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RangeGauge>"
    end
end

function create()
    return RangeGauge()
end

function describe()
    return "Min-max range gauge with colored safe/warning/critical zones"
end
