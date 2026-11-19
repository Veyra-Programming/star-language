# Star Standard Library: ui/sunburst_chart
# Description: Multi-level radial hierarchical sunburst diagram
# Author: Star Core Team
# Version: 1.0.0

class SunburstChart
    property name = "sunburst_chart"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SunburstChart>"
    end
end

function create()
    return SunburstChart()
end

function describe()
    return "Multi-level radial hierarchical sunburst diagram"
end
