# Star Standard Library: ui/chart_horizontal_bar
# Description: Horizontal ranked bar chart with value labels
# Author: Star Core Team
# Version: 1.0.0

class ChartHorizontalBar
    property name = "chart_horizontal_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartHorizontalBar>"
    end
end

function create()
    return ChartHorizontalBar()
end

function describe()
    return "Horizontal ranked bar chart with value labels"
end
