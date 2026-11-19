# Star Standard Library: ui/chart_radar
# Description: Spiderweb radar chart for multi-dimensional performance
# Author: Star Core Team
# Version: 1.0.0

class ChartRadar
    property name = "chart_radar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartRadar>"
    end
end

function create()
    return ChartRadar()
end

function describe()
    return "Spiderweb radar chart for multi-dimensional performance"
end
