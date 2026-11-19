# Star Standard Library: ui/collapsible_panel
# Description: Expandable header panel with toggle chevron
# Author: Star Core Team
# Version: 1.0.0

class CollapsiblePanel
    property name = "collapsible_panel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CollapsiblePanel>"
    end
end

function create()
    return CollapsiblePanel()
end

function describe()
    return "Expandable header panel with toggle chevron"
end
