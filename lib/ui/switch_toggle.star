# Star Standard Library: ui/switch_toggle
# Description: Animated iOS and Material style toggle switch
# Author: Star Core Team
# Version: 1.0.0

class SwitchToggle
    property name = "switch_toggle"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SwitchToggle>"
    end
end

function create()
    return SwitchToggle()
end

function describe()
    return "Animated iOS and Material style toggle switch"
end
