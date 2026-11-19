# Star Standard Library: ui/tree_table
# Description: Hierarchical expandable tree data table with indent guides
# Author: Star Core Team
# Version: 1.0.0

class TreeTable
    property name = "tree_table"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TreeTable>"
    end
end

function create()
    return TreeTable()
end

function describe()
    return "Hierarchical expandable tree data table with indent guides"
end
