# Star Standard Library: ui/drawer_sheet
# Description: Side-sliding drawer panel for details and forms
# Author: Star Core Team
# Version: 1.0.0

class DrawerSheet
    property name = "drawer_sheet"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DrawerSheet>"
    end
end

function create()
    return DrawerSheet()
end

function describe()
    return "Side-sliding drawer panel for details and forms"
end
