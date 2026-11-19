# Star Standard Library: ui/chart_area
# Description: Gradient-filled multi-series area chart
# Author: Star Core Team
# Version: 1.0.0

class ChartArea
    property name = "chart_area"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartArea>"
    end
end

function create()
    return ChartArea()
end

function describe()
    return "Gradient-filled multi-series area chart"
end
