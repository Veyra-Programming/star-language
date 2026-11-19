# Star Standard Library: ui/density_contour
# Description: 2D elevation and mathematical density contour plot
# Author: Star Core Team
# Version: 1.0.0

class DensityContour
    property name = "density_contour"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DensityContour>"
    end
end

function create()
    return DensityContour()
end

function describe()
    return "2D elevation and mathematical density contour plot"
end
