# Star Standard Library: ui/matrix_grid
# Description: N-by-N data matrix viewer with cell heatmap highlighting
# Author: Star Core Team
# Version: 1.0.0

class MatrixGrid
    property name = "matrix_grid"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: MatrixGrid>"
    end
end

function create()
    return MatrixGrid()
end

function describe()
    return "N-by-N data matrix viewer with cell heatmap highlighting"
end
