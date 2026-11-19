# Star Standard Library: ui/fullscreen_toggle
# Description: One-click HTML5 fullscreen toggle button with icon change
# Author: Star Core Team
# Version: 1.0.0

class FullscreenToggle
    property name = "fullscreen_toggle"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FullscreenToggle>"
    end
end

function create()
    return FullscreenToggle()
end

function describe()
    return "One-click HTML5 fullscreen toggle button with icon change"
end
