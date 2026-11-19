# Star Standard Library: ui/dockable_layout
# Description: Professional multi-dock IDE and workspace layout
# Author: Star Core Team
# Version: 1.0.0

class DockableLayout
    property name = "dockable_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: DockableLayout>"
    end
end

function create()
    return DockableLayout()
end

function describe()
    return "Professional multi-dock IDE and workspace layout"
end
