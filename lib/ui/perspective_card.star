# Star Standard Library: ui/perspective_card
# Description: 3D tilt card that tracks mouse hover tilt angle
# Author: Star Core Team
# Version: 1.0.0

class PerspectiveCard
    property name = "perspective_card"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PerspectiveCard>"
    end
end

function create()
    return PerspectiveCard()
end

function describe()
    return "3D tilt card that tracks mouse hover tilt angle"
end
