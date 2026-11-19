# Star Standard Library: ui/chart_treemap
# Description: Hierarchical nested rectangle treemap chart
# Author: Star Core Team
# Version: 1.0.0

class ChartTreemap
    property name = "chart_treemap"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartTreemap>"
    end
end

function create()
    return ChartTreemap()
end

function describe()
    return "Hierarchical nested rectangle treemap chart"
end
