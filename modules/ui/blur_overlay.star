# Star Standard Library: ui/blur_overlay
# Description: Frosted glass backdrop blur modal blocker
# Author: Star Core Team
# Version: 1.0.0

class BlurOverlay
    property name = "blur_overlay"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: BlurOverlay>"
    end
end

function create()
    return BlurOverlay()
end

function describe()
    return "Frosted glass backdrop blur modal blocker"
end
