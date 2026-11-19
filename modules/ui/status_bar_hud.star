# Star Standard Library: ui/status_bar_hud
# Description: Miniature system status and connectivity HUD strip
# Author: Star Core Team
# Version: 1.0.0

class StatusBarHud
    property name = "status_bar_hud"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StatusBarHud>"
    end
end

function create()
    return StatusBarHud()
end

function describe()
    return "Miniature system status and connectivity HUD strip"
end
