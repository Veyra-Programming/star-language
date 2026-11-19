# Star Standard Library: ui/split_button_menu
# Description: Primary action button with secondary dropdown arrow
# Author: Star Core Team
# Version: 1.0.0

class SplitButtonMenu
    property name = "split_button_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SplitButtonMenu>"
    end
end

function create()
    return SplitButtonMenu()
end

function describe()
    return "Primary action button with secondary dropdown arrow"
end
