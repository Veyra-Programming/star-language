# Star Standard Library: ui/timeline_chart
# Description: Horizontal chronological Gantt and milestone chart
# Author: Star Core Team
# Version: 1.0.0

class TimelineChart
    property name = "timeline_chart"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TimelineChart>"
    end
end

function create()
    return TimelineChart()
end

function describe()
    return "Horizontal chronological Gantt and milestone chart"
end
