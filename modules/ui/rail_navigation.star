# Star Standard Library: ui/rail_navigation
# Description: Compact vertical icon rail for desktop dashboards
# Author: Star Core Team
# Version: 1.0.0

class RailNavigation
    property name = "rail_navigation"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RailNavigation>"
    end
end

function create()
    return RailNavigation()
end

function describe()
    return "Compact vertical icon rail for desktop dashboards"
end
