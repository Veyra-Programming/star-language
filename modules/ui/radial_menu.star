# Star Standard Library: ui/radial_menu
# Description: Circular pie menu expanding around mouse cursor
# Author: Star Core Team
# Version: 1.0.0

class RadialMenu
    property name = "radial_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: RadialMenu>"
    end
end

function create()
    return RadialMenu()
end

function describe()
    return "Circular pie menu expanding around mouse cursor"
end
