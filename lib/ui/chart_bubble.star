# Star Standard Library: ui/chart_bubble
# Description: Three-dimensional data bubble chart with variable radiuses
# Author: Star Core Team
# Version: 1.0.0

class ChartBubble
    property name = "chart_bubble"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartBubble>"
    end
end

function create()
    return ChartBubble()
end

function describe()
    return "Three-dimensional data bubble chart with variable radiuses"
end
