# Star Standard Library: ui/tree_view
# Description: Collapsible folder and file hierarchy tree view
# Author: Star Core Team
# Version: 1.0.0

class TreeView
    property name = "tree_view"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TreeView>"
    end
end

function create()
    return TreeView()
end

function describe()
    return "Collapsible folder and file hierarchy tree view"
end
