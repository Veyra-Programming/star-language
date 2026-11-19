# Star Standard Library: ui/gradient_canvas
# Description: Animated shifting mesh gradient background
# Author: Star Core Team
# Version: 1.0.0

class GradientCanvas
    property name = "gradient_canvas"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: GradientCanvas>"
    end
end

function create()
    return GradientCanvas()
end

function describe()
    return "Animated shifting mesh gradient background"
end
