# Star Standard Library: ui/color_palette_wheel
# Description: Circular color spectrum wheel and hue slider
# Author: Star Core Team
# Version: 1.0.0

class ColorPaletteWheel
    property name = "color_palette_wheel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ColorPaletteWheel>"
    end
end

function create()
    return ColorPaletteWheel()
end

function describe()
    return "Circular color spectrum wheel and hue slider"
end
