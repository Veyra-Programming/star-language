# Star Standard Library: ui/virtual_keyboard
# Description: On-screen touch keyboard for kiosks and accessibility
# Author: Star Core Team
# Version: 1.0.0

class VirtualKeyboard
    property name = "virtual_keyboard"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: VirtualKeyboard>"
    end
end

function create()
    return VirtualKeyboard()
end

function describe()
    return "On-screen touch keyboard for kiosks and accessibility"
end
