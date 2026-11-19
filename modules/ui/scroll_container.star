# Star Standard Library: ui/scroll_container
# Description: Customizable scroll view with custom styled scrollbars
# Author: Star Core Team
# Version: 1.0.0

class ScrollContainer
    property name = "scroll_container"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ScrollContainer>"
    end
end

function create()
    return ScrollContainer()
end

function describe()
    return "Customizable scroll view with custom styled scrollbars"
end
