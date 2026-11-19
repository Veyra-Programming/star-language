# Star Standard Library: ui/resizable_panel
# Description: Resizable side and bottom docking panels
# Author: Star Core Team
# Version: 1.0.0

class ResizablePanel
    property name = "resizable_panel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ResizablePanel>"
    end
end

function create()
    return ResizablePanel()
end

function describe()
    return "Resizable side and bottom docking panels"
end
