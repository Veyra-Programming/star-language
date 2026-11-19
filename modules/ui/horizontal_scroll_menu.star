# Star Standard Library: ui/horizontal_scroll_menu
# Description: Touch-friendly edge-fading horizontal scroll menu
# Author: Star Core Team
# Version: 1.0.0

class HorizontalScrollMenu
    property name = "horizontal_scroll_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: HorizontalScrollMenu>"
    end
end

function create()
    return HorizontalScrollMenu()
end

function describe()
    return "Touch-friendly edge-fading horizontal scroll menu"
end
