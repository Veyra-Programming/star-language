# Star Standard Library: ui/multi_axis_chart
# Description: Dual left-right Y-axis chart combining line and bar data
# Author: Star Core Team
# Version: 1.0.0

class MultiAxisChart
    property name = "multi_axis_chart"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MultiAxisChart>"
    end
end

function create()
    return MultiAxisChart()
end

function describe()
    return "Dual left-right Y-axis chart combining line and bar data"
end
