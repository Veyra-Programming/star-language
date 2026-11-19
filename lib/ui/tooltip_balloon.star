# Star Standard Library: ui/tooltip_balloon
# Description: Hover and focus tooltip balloon with directional arrow
# Author: Star Core Team
# Version: 1.0.0

class TooltipBalloon
    property name = "tooltip_balloon"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TooltipBalloon>"
    end
end

function create()
    return TooltipBalloon()
end

function describe()
    return "Hover and focus tooltip balloon with directional arrow"
end
