# Star Standard Library: ui/tab_carousel
# Description: Swipeable tabbed container with touch gestures
# Author: Star Core Team
# Version: 1.0.0

class TabCarousel
    property name = "tab_carousel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TabCarousel>"
    end
end

function create()
    return TabCarousel()
end

function describe()
    return "Swipeable tabbed container with touch gestures"
end
