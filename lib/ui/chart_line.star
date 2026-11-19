# Star Standard Library: ui/chart_line
# Description: Smooth curved and stepped multi-series line chart
# Author: Star Core Team
# Version: 1.0.0

class ChartLine
    property name = "chart_line"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartLine>"
    end
end

function create()
    return ChartLine()
end

function describe()
    return "Smooth curved and stepped multi-series line chart"
end
