# Star Standard Library: ui/sticky_footer
# Description: Viewport layout where footer always sticks to bottom
# Author: Star Core Team
# Version: 1.0.0

class StickyFooter
    property name = "sticky_footer"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: StickyFooter>"
    end
end

function create()
    return StickyFooter()
end

function describe()
    return "Viewport layout where footer always sticks to bottom"
end
