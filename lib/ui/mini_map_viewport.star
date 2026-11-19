# Star Standard Library: ui/mini_map_viewport
# Description: Real-time navigation minimap with player indicator
# Author: Star Core Team
# Version: 1.0.0

class MiniMapViewport
    property name = "mini_map_viewport"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MiniMapViewport>"
    end
end

function create()
    return MiniMapViewport()
end

function describe()
    return "Real-time navigation minimap with player indicator"
end
