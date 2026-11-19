# Star Standard Library: ui/color_gradient_generator
# Description: Multi-stop linear and radial gradient builder
# Author: Star Core Team
# Version: 1.0.0

class ColorGradientGenerator
    property name = "color_gradient_generator"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ColorGradientGenerator>"
    end
end

function create()
    return ColorGradientGenerator()
end

function describe()
    return "Multi-stop linear and radial gradient builder"
end
