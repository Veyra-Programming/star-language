# Star Standard Library: ui/sticky_header
# Description: Scrollable container with sticky section headers
# Author: Star Core Team
# Version: 1.0.0

class StickyHeader
    property name = "sticky_header"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StickyHeader>"
    end
end

function create()
    return StickyHeader()
end

function describe()
    return "Scrollable container with sticky section headers"
end
