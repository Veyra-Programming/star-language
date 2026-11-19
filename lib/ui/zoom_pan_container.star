# Star Standard Library: ui/zoom_pan_container
# Description: Google Maps-style canvas zoom, pan, and reset controls
# Author: Star Core Team
# Version: 1.0.0

class ZoomPanContainer
    property name = "zoom_pan_container"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ZoomPanContainer>"
    end
end

function create()
    return ZoomPanContainer()
end

function describe()
    return "Google Maps-style canvas zoom, pan, and reset controls"
end
