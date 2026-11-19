# Star Standard Library: ui/lightbox_viewer
# Description: Fullscreen modal image and video viewer with zoom/pan
# Author: Star Core Team
# Version: 1.0.0

class LightboxViewer
    property name = "lightbox_viewer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: LightboxViewer>"
    end
end

function create()
    return LightboxViewer()
end

function describe()
    return "Fullscreen modal image and video viewer with zoom/pan"
end
