# Star Standard Library: ui/sub_navigation_bar
# Description: Secondary horizontal sub-nav for deep page routes
# Author: Star Core Team
# Version: 1.0.0

class SubNavigationBar
    property name = "sub_navigation_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SubNavigationBar>"
    end
end

function create()
    return SubNavigationBar()
end

function describe()
    return "Secondary horizontal sub-nav for deep page routes"
end
