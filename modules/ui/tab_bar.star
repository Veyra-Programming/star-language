# Star Standard Library: ui/tab_bar
# Description: Horizontal sliding tab bar with indicator underline
# Author: Star Core Team
# Version: 1.0.0

class TabBar
    property name = "tab_bar"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: TabBar>"
    end
end

function create()
    return TabBar()
end

function describe()
    return "Horizontal sliding tab bar with indicator underline"
end
