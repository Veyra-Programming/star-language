# Star Standard Library: ui/column_toggle_table
# Description: Data table with dynamic column visibility selector
# Author: Star Core Team
# Version: 1.0.0

class ColumnToggleTable
    property name = "column_toggle_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ColumnToggleTable>"
    end
end

function create()
    return ColumnToggleTable()
end

function describe()
    return "Data table with dynamic column visibility selector"
end
