# Star Standard Library: ui/chart_donut
# Description: Ring donut chart with centered aggregate total display
# Author: Star Core Team
# Version: 1.0.0

class ChartDonut
    property name = "chart_donut"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartDonut>"
    end
end

function create()
    return ChartDonut()
end

function describe()
    return "Ring donut chart with centered aggregate total display"
end
