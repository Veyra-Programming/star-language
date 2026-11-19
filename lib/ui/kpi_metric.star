# Star Standard Library: ui/kpi_metric
# Description: Key performance indicator display with goal progress bar
# Author: Star Core Team
# Version: 1.0.0

class KpiMetric
    property name = "kpi_metric"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: KpiMetric>"
    end
end

function create()
    return KpiMetric()
end

function describe()
    return "Key performance indicator display with goal progress bar"
end
