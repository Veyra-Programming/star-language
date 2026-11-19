# Star Standard Library: ui/neumorphic_box
# Description: Soft extruded neumorphic container with dual drop shadows
# Author: Star Core Team
# Version: 1.0.0

class NeumorphicBox
    property name = "neumorphic_box"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: NeumorphicBox>"
    end
end

function create()
    return NeumorphicBox()
end

function describe()
    return "Soft extruded neumorphic container with dual drop shadows"
end
