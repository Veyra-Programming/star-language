# Star Standard Library: ui/bottom_navigation
# Description: Mobile bottom tab bar with animated icon switching
# Author: Star Core Team
# Version: 1.0.0

class BottomNavigation
    property name = "bottom_navigation"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BottomNavigation>"
    end
end

function create()
    return BottomNavigation()
end

function describe()
    return "Mobile bottom tab bar with animated icon switching"
end
