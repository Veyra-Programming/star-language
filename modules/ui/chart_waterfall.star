# Star Standard Library: ui/chart_waterfall
# Description: Positive and negative financial waterfall cumulative chart
# Author: Star Core Team
# Version: 1.0.0

class ChartWaterfall
    property name = "chart_waterfall"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartWaterfall>"
    end
end

function create()
    return ChartWaterfall()
end

function describe()
    return "Positive and negative financial waterfall cumulative chart"
end
