# Star Standard Library: ui/three_column_layout
# Description: Left navigation, center content, right sidebar layout
# Author: Star Core Team
# Version: 1.0.0

class ThreeColumnLayout
    property name = "three_column_layout"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: ThreeColumnLayout>"
    end
end

function create()
    return ThreeColumnLayout()
end

function describe()
    return "Left navigation, center content, right sidebar layout"
end
