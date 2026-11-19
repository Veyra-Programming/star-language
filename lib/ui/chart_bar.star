# Star Standard Library: ui/chart_bar
# Description: Vertical grouped and stacked multi-column bar chart
# Author: Star Core Team
# Version: 1.0.0

class ChartBar
    property name = "chart_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartBar>"
    end
end

function create()
    return ChartBar()
end

function describe()
    return "Vertical grouped and stacked multi-column bar chart"
end
