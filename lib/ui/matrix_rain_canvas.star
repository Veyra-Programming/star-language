# Star Standard Library: ui/matrix_rain_canvas
# Description: Digital green Matrix code stream animation
# Author: Star Core Team
# Version: 1.0.0

class MatrixRainCanvas
    property name = "matrix_rain_canvas"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MatrixRainCanvas>"
    end
end

function create()
    return MatrixRainCanvas()
end

function describe()
    return "Digital green Matrix code stream animation"
end
