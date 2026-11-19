# Star Standard Library: ui/filter_panel
# Description: Collapsible multi-criteria filter builder panel
# Author: Star Core Team
# Version: 1.0.0

class FilterPanel
    property name = "filter_panel"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: FilterPanel>"
    end
end

function create()
    return FilterPanel()
end

function describe()
    return "Collapsible multi-criteria filter builder panel"
end
