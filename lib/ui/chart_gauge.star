# Star Standard Library: ui/chart_gauge
# Description: Semi-circular radial needle gauge with threshold color bands
# Author: Star Core Team
# Version: 1.0.0

class ChartGauge
    property name = "chart_gauge"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartGauge>"
    end
end

function create()
    return ChartGauge()
end

function describe()
    return "Semi-circular radial needle gauge with threshold color bands"
end
