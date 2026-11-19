# Star Standard Library: ui/drawer_layout
# Description: Standard desktop split-screen drawer and canvas layout
# Author: Star Core Team
# Version: 1.0.0

class DrawerLayout
    property name = "drawer_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DrawerLayout>"
    end
end

function create()
    return DrawerLayout()
end

function describe()
    return "Standard desktop split-screen drawer and canvas layout"
end
