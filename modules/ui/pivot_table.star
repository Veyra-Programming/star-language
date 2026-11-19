# Star Standard Library: ui/pivot_table
# Description: Multi-dimensional pivot matrix with row/column groupings
# Author: Star Core Team
# Version: 1.0.0

class PivotTable
    property name = "pivot_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PivotTable>"
    end
end

function create()
    return PivotTable()
end

function describe()
    return "Multi-dimensional pivot matrix with row/column groupings"
end
