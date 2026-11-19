# Star Standard Library: ui/exportable_table
# Description: Data table with one-click CSV and JSON download buttons
# Author: Star Core Team
# Version: 1.0.0

class ExportableTable
    property name = "exportable_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ExportableTable>"
    end
end

function create()
    return ExportableTable()
end

function describe()
    return "Data table with one-click CSV and JSON download buttons"
end
