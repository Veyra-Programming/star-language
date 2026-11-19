# Star Standard Library: ui/physics_playground
# Description: 2D rigid-body physics simulation container
# Author: Star Core Team
# Version: 1.0.0

class PhysicsPlayground
    property name = "physics_playground"
    property version = "1.0.0"

    function info()
        return self.name + " v" + self.version
    end

    function get_version()
        return self.version
    end

    function render_component()
        return "<UIComponent: PhysicsPlayground>"
    end
end

function create()
    return PhysicsPlayground()
end

function describe()
    return "2D rigid-body physics simulation container"
end
