# Star Standard Library: ui/gantt_chart
# Description: Project management timeline chart with dependencies and milestones
# Author: Star Core Team
# Version: 1.0.0

class GanttChart
    property name = "gantt_chart"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: GanttChart>"
    end
end

function create()
    return GanttChart()
end

function describe()
    return "Project management timeline chart with dependencies and milestones"
end
