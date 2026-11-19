# Star Standard Library: ui/svg_canvas_view
# Description: Scalable Vector Graphics (SVG) interactive path viewer
# Author: Star Core Team
# Version: 1.0.0

class SvgCanvasView
    property name = "svg_canvas_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SvgCanvasView>"
    end
end

function create()
    return SvgCanvasView()
end

function describe()
    return "Scalable Vector Graphics (SVG) interactive path viewer"
end
