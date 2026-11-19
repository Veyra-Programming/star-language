# Star Standard Library: ui/tree_select
# Description: Hierarchical tree-view dropdown selector with search
# Author: Star Core Team
# Version: 1.0.0

class TreeSelect
    property name = "tree_select"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TreeSelect>"
    end
end

function create()
    return TreeSelect()
end

function describe()
    return "Hierarchical tree-view dropdown selector with search"
end
