# Star Standard Library: ui/expandable_search
# Description: Collapsed search icon expanding into full search bar
# Author: Star Core Team
# Version: 1.0.0

class ExpandableSearch
    property name = "expandable_search"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ExpandableSearch>"
    end
end

function create()
    return ExpandableSearch()
end

function describe()
    return "Collapsed search icon expanding into full search bar"
end
