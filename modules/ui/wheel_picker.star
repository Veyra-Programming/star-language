# Star Standard Library: ui/wheel_picker
# Description: Scrollable 3D drum wheel picker for dates and lists
# Author: Star Core Team
# Version: 1.0.0

class WheelPicker
    property name = "wheel_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: WheelPicker>"
    end
end

function create()
    return WheelPicker()
end

function describe()
    return "Scrollable 3D drum wheel picker for dates and lists"
end
