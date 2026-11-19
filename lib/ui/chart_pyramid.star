# Star Standard Library: ui/chart_pyramid
# Description: Population and hierarchical demographic pyramid chart
# Author: Star Core Team
# Version: 1.0.0

class ChartPyramid
    property name = "chart_pyramid"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartPyramid>"
    end
end

function create()
    return ChartPyramid()
end

function describe()
    return "Population and hierarchical demographic pyramid chart"
end
