# Star Standard Library: ui/color_palette
# Description: RGB, HSL, Hex conversions and color contrast
# Author: Star Core Team
# Version: 1.0.0

class ColorPalette
    property name = "color_palette"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ColorPalette()
end

function describe()
    return "RGB, HSL, Hex conversions and color contrast"
end
