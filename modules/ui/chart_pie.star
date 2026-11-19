# Star Standard Library: ui/chart_pie
# Description: Multi-segment circular pie chart with hover explode effect
# Author: Star Core Team
# Version: 1.0.0

class ChartPie
    property name = "chart_pie"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartPie>"
    end
end

function create()
    return ChartPie()
end

function describe()
    return "Multi-segment circular pie chart with hover explode effect"
end
