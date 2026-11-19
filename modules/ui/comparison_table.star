# Star Standard Library: ui/comparison_table
# Description: Feature matrix comparison table with checkmarks and tooltips
# Author: Star Core Team
# Version: 1.0.0

class ComparisonTable
    property name = "comparison_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ComparisonTable>"
    end
end

function create()
    return ComparisonTable()
end

function describe()
    return "Feature matrix comparison table with checkmarks and tooltips"
end
