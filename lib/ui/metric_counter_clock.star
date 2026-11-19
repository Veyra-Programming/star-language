# Star Standard Library: ui/metric_counter_clock
# Description: Digital 7-segment LED style numeric counter clock
# Author: Star Core Team
# Version: 1.0.0

class MetricCounterClock
    property name = "metric_counter_clock"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MetricCounterClock>"
    end
end

function create()
    return MetricCounterClock()
end

function describe()
    return "Digital 7-segment LED style numeric counter clock"
end
