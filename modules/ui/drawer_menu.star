# Star Standard Library: ui/drawer_menu
# Description: Slide-out navigation drawer with user profile header
# Author: Star Core Team
# Version: 1.0.0

class DrawerMenu
    property name = "drawer_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DrawerMenu>"
    end
end

function create()
    return DrawerMenu()
end

function describe()
    return "Slide-out navigation drawer with user profile header"
end
