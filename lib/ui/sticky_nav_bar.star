# Star Standard Library: ui/sticky_nav_bar
# Description: Top navigation bar that sticks on scroll with blur backdrop
# Author: Star Core Team
# Version: 1.0.0

class StickyNavBar
    property name = "sticky_nav_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StickyNavBar>"
    end
end

function create()
    return StickyNavBar()
end

function describe()
    return "Top navigation bar that sticks on scroll with blur backdrop"
end
