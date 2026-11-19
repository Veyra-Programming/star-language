# Star Standard Library: ui/pan_zoom_viewer
# Description: Pinch-to-zoom and pan container for high-res images
# Author: Star Core Team
# Version: 1.0.0

class PanZoomViewer
    property name = "pan_zoom_viewer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PanZoomViewer>"
    end
end

function create()
    return PanZoomViewer()
end

function describe()
    return "Pinch-to-zoom and pan container for high-res images"
end
