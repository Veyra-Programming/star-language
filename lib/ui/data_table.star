# Star Standard Library: ui/data_table
# Description: High-performance sorting, filtering, and selectable data table
# Author: Star Core Team
# Version: 1.0.0

class DataTable
    property name = "data_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DataTable>"
    end
end

function create()
    return DataTable()
end

function describe()
    return "High-performance sorting, filtering, and selectable data table"
end
