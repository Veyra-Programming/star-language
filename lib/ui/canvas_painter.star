# Star Standard Library: ui/canvas_painter
# Description: Freehand drawing and painting canvas with brush sizes
# Author: Star Core Team
# Version: 1.0.0

class CanvasPainter
    property name = "canvas_painter"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CanvasPainter>"
    end
end

function create()
    return CanvasPainter()
end

function describe()
    return "Freehand drawing and painting canvas with brush sizes"
end
