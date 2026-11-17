# Star Standard Library: media/color_convert
# Description: Color space transformations (RGB, HSV, CMYK)
# Author: Star Core Team
# Version: 1.0.0

class ColorConvert
    property name = "color_convert"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

end

function create()
    return ColorConvert()
end

function describe()
    return "Color space transformations (RGB, HSV, CMYK)"
end
