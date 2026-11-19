# Star Standard Library: ui/sidebar_nav
# Description: Collapsible modern vertical sidebar navigation
# Author: Star Core Team
# Version: 1.0.0

class SidebarNav
    property name = "sidebar_nav"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SidebarNav>"
    end
end

function create()
    return SidebarNav()
end

function describe()
    return "Collapsible modern vertical sidebar navigation"
end
