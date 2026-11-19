# Star Standard Library: ui/tab_strip
# Description: Browser-style draggable and closeable tab strip
# Author: Star Core Team
# Version: 1.0.0

class TabStrip
    property name = "tab_strip"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TabStrip>"
    end
end

function create()
    return TabStrip()
end

function describe()
    return "Browser-style draggable and closeable tab strip"
end
