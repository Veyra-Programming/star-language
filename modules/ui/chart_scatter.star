# Star Standard Library: ui/chart_scatter
# Description: Multi-variable 2D scatter plot with trendline
# Author: Star Core Team
# Version: 1.0.0

class ChartScatter
    property name = "chart_scatter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartScatter>"
    end
end

function create()
    return ChartScatter()
end

function describe()
    return "Multi-variable 2D scatter plot with trendline"
end
