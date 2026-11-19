# Star Standard Library: ui/jump_menu
# Description: Quick-jump floating index for alphabetical lists
# Author: Star Core Team
# Version: 1.0.0

class JumpMenu
    property name = "jump_menu"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: JumpMenu>"
    end
end

function create()
    return JumpMenu()
end

function describe()
    return "Quick-jump floating index for alphabetical lists"
end
