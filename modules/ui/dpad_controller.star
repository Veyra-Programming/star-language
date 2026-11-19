# Star Standard Library: ui/dpad_controller
# Description: 4-way and 8-way directional pad controller
# Author: Star Core Team
# Version: 1.0.0

class DpadController
    property name = "dpad_controller"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DpadController>"
    end
end

function create()
    return DpadController()
end

function describe()
    return "4-way and 8-way directional pad controller"
end
