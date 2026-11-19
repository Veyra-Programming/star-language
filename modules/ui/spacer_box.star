# Star Standard Library: ui/spacer_box
# Description: Flexible and fixed layout spacer widget
# Author: Star Core Team
# Version: 1.0.0

class SpacerBox
    property name = "spacer_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: SpacerBox>"
    end
end

function create()
    return SpacerBox()
end

function describe()
    return "Flexible and fixed layout spacer widget"
end
