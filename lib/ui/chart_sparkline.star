# Star Standard Library: ui/chart_sparkline
# Description: Miniature inline trend chart with min/max highlight dots
# Author: Star Core Team
# Version: 1.0.0

class ChartSparkline
    property name = "chart_sparkline"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartSparkline>"
    end
end

function create()
    return ChartSparkline()
end

function describe()
    return "Miniature inline trend chart with min/max highlight dots"
end
