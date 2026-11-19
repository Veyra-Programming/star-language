# Star Standard Library: ui/color_picker
# Description: Hex, RGB, HSL and gradient interactive color picker
# Author: Star Core Team
# Version: 1.0.0

class ColorPicker
    property name = "color_picker"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ColorPicker>"
    end
end

function create()
    return ColorPicker()
end

function describe()
    return "Hex, RGB, HSL and gradient interactive color picker"
end
