# Star Standard Library: ui/center_container
# Description: Perfect horizontal and vertical centering wrapper
# Author: Star Core Team
# Version: 1.0.0

class CenterContainer
    property name = "center_container"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: CenterContainer>"
    end
end

function create()
    return CenterContainer()
end

function describe()
    return "Perfect horizontal and vertical centering wrapper"
end
