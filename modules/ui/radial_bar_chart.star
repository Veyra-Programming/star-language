# Star Standard Library: ui/radial_bar_chart
# Description: Concentric multi-colored radial bar chart
# Author: Star Core Team
# Version: 1.0.0

class RadialBarChart
    property name = "radial_bar_chart"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RadialBarChart>"
    end
end

function create()
    return RadialBarChart()
end

function describe()
    return "Concentric multi-colored radial bar chart"
end
