# Star Standard Library: ui/watermark_overlay
# Description: Diagonal text and image security watermark overlay
# Author: Star Core Team
# Version: 1.0.0

class WatermarkOverlay
    property name = "watermark_overlay"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: WatermarkOverlay>"
    end
end

function create()
    return WatermarkOverlay()
end

function describe()
    return "Diagonal text and image security watermark overlay"
end
