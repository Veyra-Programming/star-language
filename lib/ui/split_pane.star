# Star Standard Library: ui/split_pane
# Description: Resizable horizontal and vertical split divider view
# Author: Star Core Team
# Version: 1.0.0

class SplitPane
    property name = "split_pane"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SplitPane>"
    end
end

function create()
    return SplitPane()
end

function describe()
    return "Resizable horizontal and vertical split divider view"
end
