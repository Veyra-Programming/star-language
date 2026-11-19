# Star Standard Library: ui/progress_hud
# Description: Centered semi-transparent activity HUD with spinner
# Author: Star Core Team
# Version: 1.0.0

class ProgressHud
    property name = "progress_hud"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ProgressHud>"
    end
end

function create()
    return ProgressHud()
end

function describe()
    return "Centered semi-transparent activity HUD with spinner"
end
