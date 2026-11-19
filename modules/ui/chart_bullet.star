# Star Standard Library: ui/chart_bullet
# Description: Performance target versus actual metric bullet chart
# Author: Star Core Team
# Version: 1.0.0

class ChartBullet
    property name = "chart_bullet"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ChartBullet>"
    end
end

function create()
    return ChartBullet()
end

function describe()
    return "Performance target versus actual metric bullet chart"
end
