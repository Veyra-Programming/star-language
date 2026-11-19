# Star Standard Library: ui/stat_card
# Description: Executive metric KPI card with sparkline and percentage change
# Author: Star Core Team
# Version: 1.0.0

class StatCard
    property name = "stat_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StatCard>"
    end
end

function create()
    return StatCard()
end

function describe()
    return "Executive metric KPI card with sparkline and percentage change"
end
